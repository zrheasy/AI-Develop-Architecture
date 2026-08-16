"""解析与回写 MAPP 任务 markdown 文件。"""

import os
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


def parse_task(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    sec = _split_sections(text)
    missing = [k for k in ("ID", "Title", "Owner", "Goal", "Risk Level") if k not in sec]
    if missing:
        raise ValueError(f"{path}: 缺少必要字段 {', '.join(missing)}")
    risk = sec["Risk Level"].strip().upper()
    if risk not in ("L0", "L1", "L2", "L3"):
        raise ValueError(f"{path}: Risk Level 非法 {risk!r}")
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
        "deliverable": sec.get("Deliverable", "").strip(),
        "file": os.path.abspath(path),
    }


def patch_review_result(path, result, failure_reason=None):
    """回写任务文件的 Review Result / Failure Reason（由 PM 命令执行）。"""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    out = []
    i = 0
    replaced_result = False
    replaced_reason = False
    while i < len(lines):
        m = SECTION_RE.match(lines[i])
        if m and m.group(1).strip() == "Review Result":
            out.append(lines[i])
            i += 1
            while i < len(lines) and not SECTION_RE.match(lines[i]):
                i += 1
            out.append(result)
            replaced_result = True
            continue
        if m and m.group(1).strip() == "Failure Reason":
            out.append(lines[i])
            i += 1
            while i < len(lines) and not SECTION_RE.match(lines[i]):
                i += 1
            out.append(failure_reason or "")
            replaced_reason = True
            continue
        out.append(lines[i])
        i += 1

    if not replaced_result:
        out.extend(["", "## Review Result", result])
    if not replaced_reason:
        out.extend(["", "## Failure Reason", failure_reason or ""])

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
