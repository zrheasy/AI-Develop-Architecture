"""mapp 命令行入口。"""

import argparse
import os
import sys

from mapp import context as ctx_mod
from mapp import db, taskfile
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
        if value == st or value == lab:
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
        "SELECT id FROM tasks WHERE owner = ? AND status IN ('executing', 'reviewing', 'blocked')",
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
    _agent_status(conn, row["owner"], "executing", args.id)
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
    _agent_status(conn, row["owner"], "reviewing", args.id)
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
    _agent_status(conn, row["owner"], "blocked", args.id)
    conn.commit()
    conn.close()
    print(f"{args.id} → 阻塞中: {args.reason}")


def cmd_task_unblock(args):
    conn, root = _get_conn(args)
    row = _get_task(conn, args.id)
    if row["status"] != BLOCKED:
        raise SystemExit(f"{args.id} 当前为 {label(row['status'])}，只有阻塞中任务可解除")
    _flip(conn, row, EXECUTING, args.actor, args.reason or "阻塞解除")
    _agent_status(conn, row["owner"], "executing", args.id)
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
    _agent_status(conn, row["owner"], "executing", args.id)
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
    _agent_status(conn, row["owner"], "idle", None)
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
        _agent_status(conn, row["owner"], "blocked", args.id)
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
    print(ctx_mod.render_context(root, task))
    conn.close()


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
