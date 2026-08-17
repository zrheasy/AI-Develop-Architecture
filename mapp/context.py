"""阶段二：最小上下文注入。只输出 Task 内容与引用的输入文件。"""

import os
import re

from mapp import objects, taskfile

TOKEN_RE = re.compile(r"[^\s,、，()\[\]]+\.md")
SEARCH_DIRS = ("", "decisions", "features", "requirements", "protocols", "tasks", "Agents")


def collect_refs(context_text):
    """从 Context 中提取 .md 引用（排除 URL）。"""
    seen = set()
    refs = []
    for m in TOKEN_RE.finditer(context_text or ""):
        ref = m.group(0).strip("`\"'")
        if ref.startswith(("http://", "https://")):
            continue
        if ref not in seen:
            seen.add(ref)
            refs.append(ref)
    return refs


def collect_feature_refs(context_text):
    """从 Context 的 `Feature:` 行提取 Feature 名（不带 .md）。"""
    names = []
    for line in (context_text or "").splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("feature:"):
            value = stripped[len("feature:"):].strip()
            for part in re.split(r"[/,，]", value):
                part = part.strip().strip("`\"'")
                if part and part not in names:
                    names.append(part)
    return names


def resolve_ref(project_root, ref):
    """先从数据库解析 Feature / PRD / Decision 引用，再回退文件系统。"""
    candidates = []
    if ref.startswith(("/", "./", "../")):
        candidates.append(os.path.join(project_root, ref))
    else:
        for d in SEARCH_DIRS:
            candidates.append(os.path.join(project_root, d, ref))
        candidates.append(os.path.join(project_root, os.path.basename(ref)))
    for cand in candidates:
        norm = os.path.normpath(cand)
        if os.path.isfile(norm):
            return norm
    return None


def _render_ref_summary(row, kind):
    """输出对象的关键字段摘要（缓存友好，远小于全文）。"""
    if kind == "feature":
        return "\n".join([
            f"# Feature: {row['name']}（{row['title']}）",
            "",
            f"Status: {row['status']}",
            f"Goal: {row['goal']}",
        ])
    if kind == "prd":
        return "\n".join([
            f"# PRD: {row['id']}（{row['title']}）",
            "",
            f"Status: {row['status']}",
            f"User Need: {row['user_need']}",
            f"Goal: {row['goal']}",
        ])
    if kind == "decision":
        return "\n".join([
            f"# Decision: {row['topic']}（{row['title']}）",
            "",
            f"Decision: {row['decision']}",
        ])
    return ""


def _resolve_db_ref_full(conn, ref):
    """返回 (内容, 类型) 或 None；内容为全文（供懒加载 ref show 使用）。"""
    name = ref
    if name.startswith("features/"):
        name = name[len("features/"):]
    elif name.startswith("requirements/"):
        name = name[len("requirements/"):]
    elif name.startswith("decisions/"):
        name = name[len("decisions/"):]
    name = name.removesuffix(".md")

    row = conn.execute("SELECT * FROM features WHERE name = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_feature(dict(row)), "feature", dict(row)
    row = conn.execute("SELECT * FROM prds WHERE id = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_prd(dict(row)), "prd", dict(row)
    row = conn.execute("SELECT * FROM decisions WHERE topic = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_decision(dict(row)), "decision", dict(row)
    return None


def _resolve_db_ref(conn, ref):
    """兼容旧接口：返回全文内容或 None。"""
    result = _resolve_db_ref_full(conn, ref)
    return result[0] if result else None


def collect_task_refs(task):
    """收集 Task 声明的全部引用（.md 路径 + Feature: 行），保序去重。"""
    refs = collect_refs(task["context"])
    for name in collect_feature_refs(task["context"]):
        if name not in refs:
            refs.append(name)
    return refs


def render_context(conn, project_root, task, fields=None, refs_mode="full"):
    """最小上下文注入。

    fields: Task 字段白名单（None=全部）；refs_mode: full=全量注入 / summary=摘要 / none=不注入。
    """
    lines = [
        f"# 最小上下文: {task['id']}（{task['title']}）",
        "",
        f"Owner: {task['owner']}",
        "",
        "## Task 内容",
        "",
    ]
    lines.append(taskfile.render_task(task, fields=fields))

    if refs_mode == "none":
        return "\n".join(lines)

    for ref in collect_task_refs(task):
        db_result = _resolve_db_ref_full(conn, ref)
        if db_result is not None:
            db_content, _kind, row = db_result
            lines.append("")
            if refs_mode == "summary":
                lines.append(f"## 引用摘要: {ref}（数据库）")
                lines.append("")
                lines.append(_render_ref_summary(row, _kind))
            else:
                lines.append(f"## 引用: {ref}（数据库）")
                lines.append("")
                lines.append(db_content)
            continue
        path = resolve_ref(project_root, ref)
        lines.append("")
        if path is None:
            lines.append(f"## 引用（未找到）: {ref}")
            continue
        with open(path, encoding="utf-8") as fh:
            content = fh.read().rstrip()
        if refs_mode == "summary":
            first_lines = [ln for ln in content.splitlines() if ln.strip()][:6]
            lines.append(f"## 引用摘要: {ref}（文件）")
            lines.append("")
            lines.append("\n".join(first_lines))
        else:
            lines.append(f"## 引用: {ref}（文件）")
            lines.append("")
            lines.append(content)
    return "\n".join(lines)


def _resolve_db_ref(conn, ref):
    """按 Feature 名 / PRD ID / Decision topic 从数据库取内容。"""
    name = ref
    if name.startswith("features/"):
        name = name[len("features/"):]
    elif name.startswith("requirements/"):
        name = name[len("requirements/"):]
    elif name.startswith("decisions/"):
        name = name[len("decisions/"):]
    name = name.removesuffix(".md")

    row = conn.execute("SELECT * FROM features WHERE name = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_feature(dict(row))
    row = conn.execute("SELECT * FROM prds WHERE id = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_prd(dict(row))
    row = conn.execute("SELECT * FROM decisions WHERE topic = ?", (name,)).fetchone()
    if row is not None:
        return objects.render_decision(dict(row))
    return None
