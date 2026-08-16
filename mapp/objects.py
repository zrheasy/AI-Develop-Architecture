"""Feature / PRD / Decision 的 Markdown 解析与渲染（入库用）。"""

import re

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")

FEATURE_STATUSES = ("PLANNING", "ACTIVE", "STABLE", "DEPRECATED", "ARCHIVED")
FEATURE_TRANSITIONS = {
    "PLANNING": {"ACTIVE"},
    "ACTIVE": {"STABLE", "DEPRECATED"},
    "STABLE": {"DEPRECATED"},
    "DEPRECATED": {"ARCHIVED"},
    "ARCHIVED": set(),
}

PRD_STATUSES = ("DRAFT", "APPROVED", "ARCHIVED")
PRD_TRANSITIONS = {
    "DRAFT": {"APPROVED"},
    "APPROVED": {"ARCHIVED"},
    "ARCHIVED": set(),
}


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


def _h1_title(text):
    for line in text.splitlines():
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    return ""


def _slugify(text):
    """转 kebab-case：小写、空格/下划线转连字符、去标点。中文保留。"""
    out = []
    for ch in text.lower().strip():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "_", "/", "\\"):
            out.append("-")
    value = "".join(out)
    while "--" in value:
        value = value.replace("--", "-")
    return value.strip("-")


def parse_feature(text, default_name=None):
    sec = _split_sections(text)
    missing = [k for k in ("Goal",) if k not in sec]
    if missing:
        raise ValueError(f"缺少必要字段: {', '.join(missing)}")
    status = sec.get("Status", "PLANNING").strip().upper()
    if status not in FEATURE_STATUSES:
        raise ValueError(f"Feature Status 非法: {status!r}")
    name = sec.get("Name", "").strip() or (default_name or "") or _slugify(_h1_title(text))
    if not name:
        raise ValueError("缺少 Name（可用 --name 指定，或写入 ## Name / H1 标题）")
    title = sec.get("Title", "").strip() or _h1_title(text) or name
    return {
        "name": name,
        "title": title,
        "goal": sec.get("Goal", "").strip(),
        "user_value": sec.get("User Value", "").strip(),
        "scope": sec.get("Scope", "").strip(),
        "status": status,
        "owner": sec.get("Owner", "PM Agent").strip(),
        "related_decisions": sec.get("Related Decisions", "").strip(),
        "evolution": sec.get("Evolution", "").strip(),
    }


def render_feature(row):
    return "\n".join([
        "# " + (row["title"] or row["name"]),
        "",
        "## Name",
        row["name"],
        "",
        "## Title",
        row["title"],
        "",
        "## Goal",
        row.get("goal") or "",
        "",
        "## User Value",
        row.get("user_value") or "",
        "",
        "## Scope",
        row.get("scope") or "",
        "",
        "## Status",
        row.get("status") or "PLANNING",
        "",
        "## Owner",
        row.get("owner") or "PM Agent",
        "",
        "## Related Decisions",
        row.get("related_decisions") or "",
        "",
        "## Evolution",
        row.get("evolution") or "",
    ])


def parse_prd(text):
    sec = _split_sections(text)
    missing = [k for k in ("ID", "Title", "User Need", "Goal") if k not in sec]
    if missing:
        raise ValueError(f"缺少必要字段: {', '.join(missing)}")
    status = sec.get("Status", "DRAFT").strip().upper()
    if status not in PRD_STATUSES:
        raise ValueError(f"PRD Status 非法: {status!r}")
    return {
        "id": sec["ID"].strip(),
        "title": sec["Title"].strip(),
        "user_need": sec.get("User Need", "").strip(),
        "goal": sec.get("Goal", "").strip(),
        "solution": sec.get("Solution", "").strip(),
        "scope": sec.get("Scope", "").strip(),
        "feature_impact": sec.get("Feature Impact", "").strip(),
        "affected_areas": sec.get("Affected Areas", "").strip(),
        "acceptance": sec.get("Acceptance Criteria", "").strip(),
        "status": status,
        "owner": sec.get("Owner", "Product Agent").strip(),
    }


def render_prd(row):
    return "\n".join([
        "# Product Requirement",
        "",
        "## ID",
        row["id"],
        "",
        "## Title",
        row["title"],
        "",
        "## User Need",
        row.get("user_need") or "",
        "",
        "## Goal",
        row.get("goal") or "",
        "",
        "## Solution",
        row.get("solution") or "",
        "",
        "## Scope",
        row.get("scope") or "",
        "",
        "## Feature Impact",
        row.get("feature_impact") or "",
        "",
        "## Affected Areas",
        row.get("affected_areas") or "",
        "",
        "## Acceptance Criteria",
        row.get("acceptance") or "",
        "",
        "## Status",
        row.get("status") or "DRAFT",
        "",
        "## Owner",
        row.get("owner") or "Product Agent",
    ])


def parse_decision(text, default_topic=None):
    sec = _split_sections(text)
    missing = [k for k in ("Decision",) if k not in sec]
    if missing:
        raise ValueError(f"缺少必要字段: {', '.join(missing)}")
    h1 = _h1_title(text)
    if h1.startswith("Decision Topic:"):
        h1 = h1[len("Decision Topic:"):].strip()
    topic = sec.get("Topic", "").strip() or (default_topic or "") or _slugify(h1)
    if not topic:
        raise ValueError("缺少 Topic（可用 --topic 指定，或写入 ## Topic / H1 标题）")
    title = sec.get("Title", "").strip() or h1 or topic
    if title.startswith("Decision Topic:"):
        title = title[len("Decision Topic:"):].strip()
    return {
        "topic": topic,
        "title": title,
        "context": sec.get("Context", "").strip(),
        "decision": sec["Decision"].strip(),
        "impact": sec.get("Impact", "").strip(),
    }


def render_decision(row):
    return "\n".join([
        "# " + (row["title"] or row["topic"]),
        "",
        "## Topic",
        row["topic"],
        "",
        "## Title",
        row["title"],
        "",
        "## Context",
        row.get("context") or "",
        "",
        "## Decision",
        row.get("decision") or "",
        "",
        "## Impact",
        row.get("impact") or "",
    ])
