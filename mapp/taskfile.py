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


TASK_FIELD_KEYS = (
    "id", "title", "owner", "goal", "context", "risk_level",
    "qa", "acceptance", "deliverable", "review", "failure",
)


def render_task(task, fields=None):
    """从数据库字段生成任务 Markdown 文本；fields 为 None 时输出全部字段。"""
    allowed = set(fields) if fields is not None else None
    parts = ["# Task", ""]

    def add(key, heading, value):
        if allowed is not None and key not in allowed:
            return
        parts.extend([heading, value or "", ""])

    add("id", "## ID", task["id"])
    add("title", "## Title", task["title"])
    add("owner", "## Owner", task["owner"])
    add("goal", "## Goal", task.get("goal") or "")
    add("context", "## Context", task.get("context") or "")
    add("risk_level", "## Risk Level", task.get("risk_level") or "")
    add("qa", "## QA Required", task.get("qa_reason") or ("Yes" if task.get("qa_required") else "No"))
    add("acceptance", "## Acceptance Criteria", task.get("acceptance") or "")
    add("deliverable", "## Deliverable", task.get("deliverable_spec") or "")
    add("review", "## Review Result", task.get("review_result") or "")
    add("failure", "## Failure Reason", task.get("failure_reason") or "")
    return "\n".join(parts)
