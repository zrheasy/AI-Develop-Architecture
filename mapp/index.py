"""从数据库生成各 Agent 的 INDEX.md（生成视图）。"""

import os

from mapp.state import label


def render_index(conn, owner):
    rows = conn.execute(
        "SELECT id, title, status, priority, file FROM tasks WHERE owner = ? "
        "ORDER BY priority ASC, id ASC",
        (owner,),
    ).fetchall()
    lines = [
        f"# Task Index — {owner}",
        "",
        "| ID | Title | Status | Priority | File |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        fname = os.path.basename(row["file"])
        lines.append(f"| {row['id']} | {row['title']} | {label(row['status'])} | {row['priority']} | {fname} |")
    if not rows:
        lines.append("| - | - | - | - | - |")
    return "\n".join(lines) + "\n"


def write_index(conn, owner, project_root):
    content = render_index(conn, owner)
    path = os.path.join(project_root, "tasks", owner, "INDEX.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path
