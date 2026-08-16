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


def render_context(conn, project_root, task):
    lines = [
        f"# 最小上下文: {task['id']}（{task['title']}）",
        "",
        f"Owner: {task['owner']}",
        "",
        "## Task 内容",
        "",
    ]
    lines.append(taskfile.render_task(task))

    refs = collect_refs(task["context"])
    for name in collect_feature_refs(task["context"]):
        if name not in refs:
            refs.append(name)

    for ref in refs:
        db_content = _resolve_db_ref(conn, ref)
        if db_content is not None:
            lines.append("")
            lines.append(f"## 引用: {ref}（数据库）")
            lines.append("")
            lines.append(db_content)
            continue
        path = resolve_ref(project_root, ref)
        lines.append("")
        if path is None:
            lines.append(f"## 引用（未找到）: {ref}")
            continue
        lines.append(f"## 引用: {ref}")
        lines.append("")
        with open(path, encoding="utf-8") as fh:
            lines.append(fh.read().rstrip())
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
