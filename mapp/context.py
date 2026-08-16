"""阶段二：最小上下文注入。只输出 Task 内容与引用的输入文件。"""

import os
import re

from mapp import taskfile

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


def resolve_ref(project_root, ref):
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


def render_context(project_root, task):
    lines = [
        f"# 最小上下文: {task['id']}（{task['title']}）",
        "",
        f"Owner: {task['owner']}",
        "",
        "## Task 内容",
        "",
    ]
    lines.append(taskfile.render_task(task))

    for ref in collect_refs(task["context"]):
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
