"""mapp 命令行入口。"""

import argparse
import os
import sys

from mapp import context as ctx_mod
from mapp import db, taskfile
from mapp import objects
from mapp.state import (
    AGENT_NAMES,
    DEV_AGENTS,
    STATUS_LABELS,
    WAITING,
    EXECUTING,
    REVIEWING,
    BLOCKED,
    DONE,
    label,
    normalize_owner,
)


def _resolve(project_root, path):
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(project_root, path))


def _get_conn(args):
    root = os.path.abspath(args.project or os.getcwd())
    path = db.default_db_path(root)
    if not os.path.exists(path):
        raise SystemExit(f"未初始化：请先运行 `python -m mapp --project {root} init`")
    return db.connect(path), root


def _get_task(conn, task_id):
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise SystemExit(f"任务不存在: {task_id}")
    return row


def _record(conn, task_id, from_status, to_status, actor, reason=None):
    conn.execute(
        "INSERT INTO task_events(task_id, from_status, to_status, actor, reason, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (task_id, from_status, to_status, actor, reason, db.now()),
    )


def _flip(conn, row, to_status, actor, reason=None, extra=None):
    _record(conn, row["id"], row["status"], to_status, actor, reason)
    sets = ["status = ?", "updated_at = ?"]
    params = [to_status, db.now()]
    if extra:
        for col, val in extra.items():
            sets.append(f"{col} = ?")
            params.append(val)
    params.append(row["id"])
    conn.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?", params)


def _agent_status(conn, owner, status, current_task):
    conn.execute(
        "UPDATE agents SET status = ?, current_task = ?, updated_at = ? WHERE name = ?",
        (status, current_task, db.now(), owner),
    )


def _parse_status(value):
    for st, lab in STATUS_LABELS.items():
        if value.upper() == st or value == lab:
            return st
    raise SystemExit(f"未知状态: {value}")


def cmd_init(args):
    root = os.path.abspath(args.project or os.getcwd())
    path = db.default_db_path(root)
    db.init_db(path)
    conn = db.connect(path)
    try:
        db.seed_agents(conn)
    finally:
        conn.close()
    print(f"已初始化 mapp 数据库: {path}")


def _insert_task(conn, parsed, priority, actor="PM"):
    """校验并把解析后的任务写入数据库；已存在则抛错。"""
    owner = normalize_owner(parsed["owner_raw"])
    if conn.execute("SELECT 1 FROM tasks WHERE id = ?", (parsed["id"],)).fetchone():
        raise SystemExit(f"任务已存在: {parsed['id']}")
    now = db.now()
    conn.execute(
        "INSERT INTO tasks(id, title, owner, status, risk_level, qa_required, qa_reason, "
        "priority, goal, context, acceptance, deliverable_spec, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (parsed["id"], parsed["title"], owner, WAITING, parsed["risk_level"],
         int(parsed["qa_required"]), parsed["qa_reason"], priority,
         parsed["goal"], parsed["context"], parsed["acceptance"], parsed["deliverable_spec"],
         now, now),
    )
    _record(conn, parsed["id"], None, WAITING, actor, "创建任务")


def cmd_task_add(args):
    conn, root = _get_conn(args)
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("stdin 为空：请通过管道粘贴任务 Markdown")
    parsed = taskfile.parse_task(text)
    _insert_task(conn, parsed, args.priority)
    owner = normalize_owner(parsed["owner_raw"])
    conn.commit()
    conn.close()
    print(f"已登记 {parsed['id']}（等待中），可用 `mapp task list --owner {owner}` 查看")


def cmd_task_import(args):
    conn, root = _get_conn(args)
    src = _resolve(root, args.dir)
    if not os.path.isdir(src):
        raise SystemExit(f"目录不存在: {src}")
    added, skipped, failed = 0, 0, []
    for dirpath, _dirs, files in os.walk(src):
        for name in sorted(files):
            if not (name.startswith("TASK-") and name.endswith(".md")):
                continue
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    parsed = taskfile.parse_task(fh.read())
                _insert_task(conn, parsed, "P1", actor="IMPORT")
                added += 1
            except SystemExit:
                skipped += 1
            except ValueError as exc:
                skipped += 1
                failed.append(f"{os.path.relpath(path, root)}: {exc}")
    conn.commit()
    conn.close()
    print(f"导入完成: 新增 {added}，跳过 {skipped}")
    for item in failed:
        print(f"  - {item}")


def cmd_task_assign(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != WAITING:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只能从 等待中 派发")
    active = conn.execute(
        "SELECT id FROM tasks WHERE owner = ? AND status IN ('EXECUTING', 'REVIEWING', 'BLOCKED')",
        (row["owner"],),
    ).fetchall()
    if active:
        raise SystemExit(f"{row['owner']} 已有进行中任务 {', '.join(r['id'] for r in active)}，不得并行派发")
    missing = [
        name
        for name, value in (
            ("Goal", row["goal"]),
            ("Context", row["context"]),
            ("Acceptance Criteria", row["acceptance"]),
            ("Deliverable", row["deliverable_spec"]),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"{args.id} 缺少前置字段 {', '.join(missing)}，不得进入执行中")
    _flip(conn, row, EXECUTING, args.actor, "PM 派发")
    _agent_status(conn, row["owner"], "EXECUTING", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 执行中（{row['owner']}）")


def cmd_task_review(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != EXECUTING:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有执行中任务可提交审核")
    dpath = _resolve(root, args.deliverable)
    if not os.path.exists(dpath):
        raise SystemExit(f"交付物不存在: {dpath}")
    _flip(conn, row, REVIEWING, args.actor, f"提交审核: {dpath}", {"deliverable": dpath})
    _agent_status(conn, row["owner"], "REVIEWING", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 审核中（交付物: {dpath}）")


def cmd_task_block(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != EXECUTING:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有执行中任务可阻塞")
    if not (args.reason or "").strip():
        raise SystemExit("--reason 必填")
    _flip(conn, row, BLOCKED, args.actor, args.reason)
    _agent_status(conn, row["owner"], "BLOCKED", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 阻塞中: {args.reason}")


def cmd_task_unblock(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != BLOCKED:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有阻塞中任务可解除")
    _flip(conn, row, EXECUTING, args.actor, args.reason or "阻塞解除")
    _agent_status(conn, row["owner"], "EXECUTING", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 执行中")


def cmd_task_fail(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != REVIEWING:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有审核中任务可验收失败")
    if not (args.reason or "").strip():
        raise SystemExit("--reason 必填")
    _flip(
        conn, row, EXECUTING, args.actor, args.reason,
        {"review_result": "FAIL", "failure_reason": args.reason},
    )
    _agent_status(conn, row["owner"], "EXECUTING", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 执行中（FAIL）")


def cmd_task_pass(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != REVIEWING:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有审核中任务可验收通过")
    if row["qa_required"]:
        qa = conn.execute(
            "SELECT result FROM qa_results WHERE task_id = ? ORDER BY id DESC LIMIT 1",
            (args.id,),
        ).fetchone()
        if qa is None or qa["result"] != "PASS":
            raise SystemExit("QA Required=Yes：缺少 QA PASS，不得验收通过")
    if row["owner"] in DEV_AGENTS:
        missing = [
            name
            for name, value in (
                ("Commit hash", row["commit_hash"]),
                ("Branch", row["branch"]),
                ("Merge Target", row["merge_target"]),
                ("Verification", row["verification"]),
            )
            if not value
        ]
        if missing:
            raise SystemExit(f"开发类 Task 缺少 {', '.join(missing)}，不得验收通过")
    _flip(conn, row, DONE, args.actor, "验收通过", {"review_result": "PASS"})
    _agent_status(conn, row["owner"], "IDLE", None)
    # 任务完成时清理对应审计记录：task_events 只保留未完成任务的流转历史
    conn.execute("DELETE FROM task_events WHERE task_id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"{args.id} → 已完成（PASS）")


def cmd_task_commit(args):
    conn, root = _get_conn(args)
    _get_task(conn, args.id)
    conn.execute(
        "UPDATE tasks SET commit_hash = ?, branch = ?, merge_target = ?, verification = ?, updated_at = ? WHERE id = ?",
        (args.hash, args.branch, args.target, args.verification or "", db.now(), args.id),
    )
    conn.commit()
    conn.close()
    print(f"{args.id} Commit 信息已记录")


def cmd_qa(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    result = args.result.upper()
    if result not in ("PASS", "FAIL", "BLOCKED"):
        raise SystemExit(f"QA 结论必须是 PASS / FAIL / BLOCKED: {result}")
    report = _resolve(root, args.report) if args.report else None
    conn.execute(
        "INSERT INTO qa_results(task_id, result, report, created_at) VALUES (?, ?, ?, ?)",
        (args.id, result, report, db.now()),
    )
    if result == "BLOCKED" and row["status"] in (EXECUTING, REVIEWING):
        _flip(conn, row, BLOCKED, "QA", "QA BLOCKED")
        _agent_status(conn, row["owner"], "BLOCKED", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} QA 结论已记录: {result}")


def cmd_task_show(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    print(f"Status: {label(row['status'])}")
    print(f"Priority: {row['priority']}")
    if row["deliverable"]:
        print(f"Deliverable: {row['deliverable']}")
    if row["commit_hash"]:
        print(f"Commit: {row['commit_hash']}  Branch: {row['branch']} → {row['merge_target']}")
    if row["review_result"]:
        print(f"Review Result: {row['review_result']}")
    if row["failure_reason"]:
        print(f"Failure Reason: {row['failure_reason']}")
    print("")
    print(taskfile.render_task(dict(row)))
    conn.close()


def cmd_task_list(args):
    conn, root = _get_conn(args)
    sql = "SELECT id, title, owner, status, priority FROM tasks"
    conds, params = [], []
    if args.owner:
        conds.append("owner = ?")
        params.append(normalize_owner(args.owner))
    if args.status:
        conds.append("status = ?")
        params.append(_parse_status(args.status))
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY priority ASC, id ASC"
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("无任务")
    else:
        print("| ID | Title | Owner | Status | Priority |")
        print("|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['id']} | {r['title']} | {r['owner']} | {label(r['status'])} | {r['priority']} |")
    conn.close()


def cmd_status(args):
    conn, root = _get_conn(args)
    owners = [normalize_owner(args.owner)] if args.owner else list(AGENT_NAMES)
    for owner in owners:
        row = conn.execute("SELECT status, current_task FROM agents WHERE name = ?", (owner,)).fetchone()
        if row is None:
            print(f"{owner}: 未初始化")
            continue
        current = row["current_task"] or "-"
        print(f"{owner}: {row['status']}（当前任务: {current}）")
    print("")
    counts = conn.execute("SELECT status, COUNT(*) AS c FROM tasks GROUP BY status ORDER BY status").fetchall()
    if counts:
        parts = [f"{label(r['status'])} {r['c']}" for r in counts]
        print("任务统计: " + " / ".join(parts))
    else:
        print("任务统计: 无")
    conn.close()


def cmd_audit(args):
    conn, root = _get_conn(args)
    sql = "SELECT * FROM task_events"
    conds, params = [], []
    if args.task:
        conds.append("task_id = ?")
        params.append(args.task)
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(args.limit)
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("无审计记录")
    for r in rows:
        frm = label(r["from_status"]) if r["from_status"] else "-"
        to = label(r["to_status"])
        reason = f" | {r['reason']}" if r["reason"] else ""
        print(f"{r['created_at']} {r['task_id']} {frm} → {to} by {r['actor']}{reason}")
    conn.close()


def cmd_context(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    task = dict(row)
    task["owner"] = normalize_owner(row["owner"]) + " Agent"
    print(ctx_mod.render_context(conn, root, task))
    conn.close()


# ---------- Feature ----------

FEATURE_STATUSES = ("PLANNING", "ACTIVE", "STABLE", "DEPRECATED", "ARCHIVED")


def _insert_feature(conn, parsed, actor="PM"):
    if conn.execute("SELECT 1 FROM features WHERE name = ?", (parsed["name"],)).fetchone():
        raise SystemExit(f"Feature 已存在: {parsed['name']}")
    now = db.now()
    conn.execute(
        "INSERT INTO features(name, title, goal, user_value, scope, status, owner, "
        "related_decisions, evolution, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (parsed["name"], parsed["title"], parsed["goal"], parsed["user_value"],
         parsed["scope"], parsed["status"], parsed["owner"],
         parsed["related_decisions"], parsed["evolution"], now, now),
    )
    conn.execute(
        "INSERT INTO feature_events(feature, from_status, to_status, actor, reason, created_at) "
        "VALUES (?, NULL, ?, ?, ?, ?)",
        (parsed["name"], parsed["status"], actor, "创建 Feature", now),
    )


def cmd_feature_add(args):
    conn, root = _get_conn(args)
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("stdin 为空：请通过管道粘贴 Feature Markdown")
    parsed = objects.parse_feature(text, default_name=args.name)
    _insert_feature(conn, parsed)
    conn.commit()
    conn.close()
    print(f"已登记 Feature {parsed['name']}（{parsed['status']}）")


def cmd_feature_status(args):
    conn, root = _get_conn(args)
    row = conn.execute("SELECT * FROM features WHERE name = ?", (args.name,)).fetchone()
    if row is None:
        raise SystemExit(f"Feature 不存在: {args.name}")
    to_status = args.status.upper()
    if to_status not in FEATURE_STATUSES:
        raise SystemExit(f"状态非法: {to_status}")
    if to_status not in objects.FEATURE_TRANSITIONS.get(row["status"], set()):
        raise SystemExit(f"不允许 {row['status']} → {to_status}")
    now = db.now()
    conn.execute(
        "INSERT INTO feature_events(feature, from_status, to_status, actor, reason, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (args.name, row["status"], to_status, "PM", args.reason or "状态变更", now),
    )
    conn.execute(
        "UPDATE features SET status = ?, updated_at = ? WHERE name = ?",
        (to_status, now, args.name),
    )
    conn.commit()
    conn.close()
    print(f"Feature {args.name}: {row['status']} → {to_status}")


def cmd_feature_list(args):
    conn, root = _get_conn(args)
    sql = "SELECT name, title, status FROM features"
    conds, params = [], []
    if args.status:
        conds.append("status = ?")
        params.append(args.status.upper())
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY name"
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("无 Feature")
    else:
        print("| Name | Title | Status |")
        print("|---|---|---|")
        for r in rows:
            print(f"| {r['name']} | {r['title']} | {r['status']} |")
    conn.close()


def cmd_feature_show(args):
    conn, root = _get_conn(args)
    row = conn.execute("SELECT * FROM features WHERE name = ?", (args.name,)).fetchone()
    if row is None:
        raise SystemExit(f"Feature 不存在: {args.name}")
    print(objects.render_feature(dict(row)))
    conn.close()


def cmd_feature_import(args):
    conn, root = _get_conn(args)
    src = _resolve(root, args.dir)
    if not os.path.isdir(src):
        raise SystemExit(f"目录不存在: {src}")
    added, skipped, failed = 0, 0, []
    for name in sorted(os.listdir(src)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(src, name)
        try:
            with open(path, encoding="utf-8") as fh:
                parsed = objects.parse_feature(fh.read(), default_name=name.removesuffix(".md"))
            _insert_feature(conn, parsed, actor="IMPORT")
            added += 1
        except SystemExit:
            skipped += 1
        except ValueError as exc:
            skipped += 1
            failed.append(f"{name}: {exc}")
    conn.commit()
    conn.close()
    print(f"Feature 导入完成: 新增 {added}，跳过 {skipped}")
    for item in failed:
        print(f"  - {item}")


# ---------- PRD ----------

PRD_STATUSES = ("DRAFT", "APPROVED", "ARCHIVED")


def _insert_prd(conn, parsed, actor="PM"):
    if conn.execute("SELECT 1 FROM prds WHERE id = ?", (parsed["id"],)).fetchone():
        raise SystemExit(f"PRD 已存在: {parsed['id']}")
    now = db.now()
    conn.execute(
        "INSERT INTO prds(id, title, user_need, goal, solution, scope, feature_impact, "
        "affected_areas, acceptance, status, owner, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (parsed["id"], parsed["title"], parsed["user_need"], parsed["goal"],
         parsed["solution"], parsed["scope"], parsed["feature_impact"],
         parsed["affected_areas"], parsed["acceptance"], parsed["status"],
         parsed["owner"], now, now),
    )
    conn.execute(
        "INSERT INTO prd_events(prd_id, from_status, to_status, actor, reason, created_at) "
        "VALUES (?, NULL, ?, ?, ?, ?)",
        (parsed["id"], parsed["status"], actor, "创建 PRD", now),
    )


def cmd_prd_add(args):
    conn, root = _get_conn(args)
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("stdin 为空：请通过管道粘贴 PRD Markdown")
    parsed = objects.parse_prd(text)
    _insert_prd(conn, parsed)
    conn.commit()
    conn.close()
    print(f"已登记 PRD {parsed['id']}（{parsed['status']}）")


def cmd_prd_status(args):
    conn, root = _get_conn(args)
    row = conn.execute("SELECT * FROM prds WHERE id = ?", (args.id,)).fetchone()
    if row is None:
        raise SystemExit(f"PRD 不存在: {args.id}")
    to_status = args.status.upper()
    if to_status not in PRD_STATUSES:
        raise SystemExit(f"状态非法: {to_status}")
    if to_status not in objects.PRD_TRANSITIONS.get(row["status"], set()):
        raise SystemExit(f"不允许 {row['status']} → {to_status}")
    now = db.now()
    conn.execute(
        "INSERT INTO prd_events(prd_id, from_status, to_status, actor, reason, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (args.id, row["status"], to_status, "PM", args.reason or "状态变更", now),
    )
    conn.execute(
        "UPDATE prds SET status = ?, updated_at = ? WHERE id = ?",
        (to_status, now, args.id),
    )
    conn.commit()
    conn.close()
    print(f"PRD {args.id}: {row['status']} → {to_status}")


def cmd_prd_list(args):
    conn, root = _get_conn(args)
    sql = "SELECT id, title, status FROM prds"
    conds, params = [], []
    if args.status:
        conds.append("status = ?")
        params.append(args.status.upper())
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("无 PRD")
    else:
        print("| ID | Title | Status |")
        print("|---|---|---|")
        for r in rows:
            print(f"| {r['id']} | {r['title']} | {r['status']} |")
    conn.close()


def cmd_prd_show(args):
    conn, root = _get_conn(args)
    row = conn.execute("SELECT * FROM prds WHERE id = ?", (args.id,)).fetchone()
    if row is None:
        raise SystemExit(f"PRD 不存在: {args.id}")
    print(objects.render_prd(dict(row)))
    conn.close()


def cmd_prd_import(args):
    conn, root = _get_conn(args)
    src = _resolve(root, args.dir)
    if not os.path.isdir(src):
        raise SystemExit(f"目录不存在: {src}")
    added, skipped, failed = 0, 0, []
    for name in sorted(os.listdir(src)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(src, name)
        try:
            with open(path, encoding="utf-8") as fh:
                parsed = objects.parse_prd(fh.read())
            _insert_prd(conn, parsed, actor="IMPORT")
            added += 1
        except SystemExit:
            skipped += 1
        except ValueError as exc:
            skipped += 1
            failed.append(f"{name}: {exc}")
    conn.commit()
    conn.close()
    print(f"PRD 导入完成: 新增 {added}，跳过 {skipped}")
    for item in failed:
        print(f"  - {item}")


# ---------- Decision ----------


def _insert_decision(conn, parsed, actor="PM"):
    if conn.execute("SELECT 1 FROM decisions WHERE topic = ?", (parsed["topic"],)).fetchone():
        raise SystemExit(f"Decision 已存在: {parsed['topic']}")
    now = db.now()
    conn.execute(
        "INSERT INTO decisions(topic, title, context, decision, impact, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (parsed["topic"], parsed["title"], parsed["context"], parsed["decision"],
         parsed["impact"], now, now),
    )


def cmd_decision_add(args):
    conn, root = _get_conn(args)
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("stdin 为空：请通过管道粘贴 Decision Markdown")
    parsed = objects.parse_decision(text, default_topic=args.topic)
    _insert_decision(conn, parsed)
    conn.commit()
    conn.close()
    print(f"已登记 Decision {parsed['topic']}")


def cmd_decision_list(args):
    conn, root = _get_conn(args)
    rows = conn.execute("SELECT topic, title FROM decisions ORDER BY topic").fetchall()
    if not rows:
        print("无 Decision")
    else:
        print("| Topic | Title |")
        print("|---|---|")
        for r in rows:
            print(f"| {r['topic']} | {r['title']} |")
    conn.close()


def cmd_decision_show(args):
    conn, root = _get_conn(args)
    row = conn.execute("SELECT * FROM decisions WHERE topic = ?", (args.topic,)).fetchone()
    if row is None:
        raise SystemExit(f"Decision 不存在: {args.topic}")
    print(objects.render_decision(dict(row)))
    conn.close()


def cmd_decision_import(args):
    conn, root = _get_conn(args)
    src = _resolve(root, args.dir)
    if not os.path.isdir(src):
        raise SystemExit(f"目录不存在: {src}")
    added, skipped, failed = 0, 0, []
    for name in sorted(os.listdir(src)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(src, name)
        try:
            with open(path, encoding="utf-8") as fh:
                parsed = objects.parse_decision(fh.read(), default_topic=name.removesuffix(".md"))
            _insert_decision(conn, parsed, actor="IMPORT")
            added += 1
        except SystemExit:
            skipped += 1
        except ValueError as exc:
            skipped += 1
            failed.append(f"{name}: {exc}")
    conn.commit()
    conn.close()
    print(f"Decision 导入完成: 新增 {added}，跳过 {skipped}")
    for item in failed:
        print(f"  - {item}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mapp",
        description="MAPP 工作流命令行：状态机、审计与最小上下文注入",
    )
    parser.add_argument("--project", default=None, help="项目根目录（默认当前目录）")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="初始化 mapp 数据库").set_defaults(func=cmd_init)

    task = sub.add_parser("task", help="任务状态管理")
    tsub = task.add_subparsers(dest="task_command", required=True)

    p = tsub.add_parser("add", help="从 stdin 登记任务（等待中）")
    p.add_argument("--priority", default="P1", help="优先级（默认 P1）")
    p.set_defaults(func=cmd_task_add)

    p = tsub.add_parser("import", help="从目录批量导入存量任务（TASK-*.md）")
    p.add_argument("dir", help="任务目录（含存量 TASK-*.md）")
    p.set_defaults(func=cmd_task_import)

    p = tsub.add_parser("assign", help="派发任务（等待中→执行中）")
    p.add_argument("id")
    p.add_argument("--actor", default="PM")
    p.set_defaults(func=cmd_task_assign)

    p = tsub.add_parser("review", help="提交审核（执行中→审核中）")
    p.add_argument("id")
    p.add_argument("--deliverable", required=True, help="交付物实际路径（相对项目根目录）")
    p.add_argument("--actor", default="Agent")
    p.set_defaults(func=cmd_task_review)

    p = tsub.add_parser("block", help="阻塞任务（执行中→阻塞中）")
    p.add_argument("id")
    p.add_argument("--reason", required=True)
    p.add_argument("--actor", default="PM")
    p.set_defaults(func=cmd_task_block)

    p = tsub.add_parser("unblock", help="解除阻塞（阻塞中→执行中）")
    p.add_argument("id")
    p.add_argument("--reason", default=None)
    p.add_argument("--actor", default="PM")
    p.set_defaults(func=cmd_task_unblock)

    p = tsub.add_parser("fail", help="验收失败（审核中→执行中）")
    p.add_argument("id")
    p.add_argument("--reason", required=True)
    p.add_argument("--actor", default="PM")
    p.set_defaults(func=cmd_task_fail)

    p = tsub.add_parser("pass", help="验收通过（审核中→已完成）")
    p.add_argument("id")
    p.add_argument("--actor", default="PM")
    p.set_defaults(func=cmd_task_pass)

    p = tsub.add_parser("commit", help="记录开发类 Task 的 Commit 信息")
    p.add_argument("id")
    p.add_argument("--hash", required=True)
    p.add_argument("--branch", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--verification", default=None)
    p.set_defaults(func=cmd_task_commit)

    p = tsub.add_parser("show", help="查看任务详情")
    p.add_argument("id")
    p.set_defaults(func=cmd_task_show)

    p = tsub.add_parser("list", help="列出任务")
    p.add_argument("--owner", default=None)
    p.add_argument("--status", default=None)
    p.set_defaults(func=cmd_task_list)

    p = sub.add_parser("qa", help="记录 QA 结论")
    p.add_argument("id")
    p.add_argument("--result", required=True, choices=["PASS", "FAIL", "BLOCKED"])
    p.add_argument("--report", default=None)
    p.set_defaults(func=cmd_qa)

    p = sub.add_parser("status", help="查看 Agent 与任务状态")
    p.add_argument("--owner", default=None)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("audit", help="查看状态流转审计")
    p.add_argument("--task", default=None)
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("context", help="输出任务的最小上下文（Task + 引用输入）")
    p.add_argument("id")
    p.set_defaults(func=cmd_context)

    feature = sub.add_parser("feature", help="Feature 管理（数据库存储）")
    fsub = feature.add_subparsers(dest="feature_command", required=True)
    p = fsub.add_parser("add", help="从 stdin 登记 Feature")
    p.add_argument("--name", default=None, help="Feature 名（kebab-case）；缺省取 H1 标题转写")
    p.set_defaults(func=cmd_feature_add)
    p = fsub.add_parser("status", help="变更 Feature 生命周期状态")
    p.add_argument("name")
    p.add_argument("status", choices=["PLANNING", "ACTIVE", "STABLE", "DEPRECATED", "ARCHIVED"])
    p.add_argument("--reason", default=None)
    p.set_defaults(func=cmd_feature_status)
    p = fsub.add_parser("list", help="列出 Feature")
    p.add_argument("--status", default=None)
    p.set_defaults(func=cmd_feature_list)
    p = fsub.add_parser("show", help="查看 Feature 内容")
    p.add_argument("name")
    p.set_defaults(func=cmd_feature_show)
    p = fsub.add_parser("import", help="从目录导入存量 Feature 文件")
    p.add_argument("dir")
    p.set_defaults(func=cmd_feature_import)

    prd = sub.add_parser("prd", help="PRD 管理（数据库存储）")
    psub = prd.add_subparsers(dest="prd_command", required=True)
    p = psub.add_parser("add", help="从 stdin 登记 PRD")
    p.set_defaults(func=cmd_prd_add)
    p = psub.add_parser("status", help="变更 PRD 状态")
    p.add_argument("id")
    p.add_argument("status", choices=["DRAFT", "APPROVED", "ARCHIVED"])
    p.add_argument("--reason", default=None)
    p.set_defaults(func=cmd_prd_status)
    p = psub.add_parser("list", help="列出 PRD")
    p.add_argument("--status", default=None)
    p.set_defaults(func=cmd_prd_list)
    p = psub.add_parser("show", help="查看 PRD 内容")
    p.add_argument("id")
    p.set_defaults(func=cmd_prd_show)
    p = psub.add_parser("import", help="从目录导入存量 PRD 文件")
    p.add_argument("dir")
    p.set_defaults(func=cmd_prd_import)

    decision = sub.add_parser("decision", help="Decision 管理（数据库存储）")
    dsub = decision.add_subparsers(dest="decision_command", required=True)
    p = dsub.add_parser("add", help="从 stdin 登记 Decision")
    p.add_argument("--topic", default=None, help="Decision topic（kebab-case）；缺省取 H1 标题转写")
    p.set_defaults(func=cmd_decision_add)
    p = dsub.add_parser("list", help="列出 Decision")
    p.set_defaults(func=cmd_decision_list)
    p = dsub.add_parser("show", help="查看 Decision 内容")
    p.add_argument("topic")
    p.set_defaults(func=cmd_decision_show)
    p = dsub.add_parser("import", help="从目录导入存量 Decision 文件")
    p.add_argument("dir")
    p.set_defaults(func=cmd_decision_import)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 - 统一转成 CLI 错误
        parser.exit(2, f"错误: {exc}\n")
    return 0
