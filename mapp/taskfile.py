"""解析 MAPP 任务 Markdown 文本（stdin / import 用），返回字段字典。"""

import re

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")


def _split_sections(text):
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def parse_task(text):
    """把任务 Markdown 文本解析为字段字典；缺失必填字段抛 ValueError。"""
    sec = _split_sections(text)
    missing = [k for k in ("ID", "Title", "Owner", "Goal", "Risk Level") if k not in sec]
    if missing:
        raise ValueError(f"缺少必要字段: {', '.join(missing)}")
    risk = sec["Risk Level"].strip().upper()
    if risk not in ("L0", "L1", "L2", "L3"):
        raise ValueError(f"Risk Level 非法: {risk!r}")
    qa_sec = sec.get("QA Required", "")
    return {
        "id": sec["ID"].strip(),
        "title": sec["Title"].strip(),
        "owner_raw": sec["Owner"].strip(),
        "goal": sec["Goal"].strip(),
        "risk_level": risk,
        "qa_required": qa_sec.strip().upper().startswith("YES"),
        "qa_reason": qa_sec,
        "acceptance": sec.get("Acceptance Criteria", "").strip(),
        "context": sec.get("Context", "").strip(),
        "deliverable_spec": sec.get("Deliverable", "").strip(),
    }


def render_task(task):
    """从数据库字段生成任务 Markdown 文本（供 context / show 使用）。"""
    lines = [
        "# Task",
        "",
        "## ID",
        task["id"],
        "",
        "## Title",
        task["title"],
        "",
        "## Owner",
        task["owner"],
        "",
        "## Goal",
        task.get("goal") or "",
        "",
        "## Context",
        task.get("context") or "",
        "",
        "## Risk Level",
        task.get("risk_level") or "",
        "",
        "## QA Required",
        task.get("qa_reason") or ("Yes" if task.get("qa_required") else "No"),
        "",
        "## Acceptance Criteria",
        task.get("acceptance") or "",
        "",
        "## Deliverable",
        task.get("deliverable_spec") or "",
        "",
        "## Review Result",
        task.get("review_result") or "",
        "",
        "## Failure Reason",
        task.get("failure_reason") or "",
    ]
    return "\n".join(lines)
