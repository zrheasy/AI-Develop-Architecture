"""Task 状态机与不变量定义。"""

WAITING = "WAITING"
EXECUTING = "EXECUTING"
REVIEWING = "REVIEWING"
BLOCKED = "BLOCKED"
DONE = "DONE"

ALL_STATUSES = (WAITING, EXECUTING, REVIEWING, BLOCKED, DONE)

STATUS_LABELS = {
    WAITING: "等待中",
    EXECUTING: "执行中",
    REVIEWING: "审核中",
    BLOCKED: "阻塞中",
    DONE: "已完成",
}

TRANSITIONS = {
    WAITING: {EXECUTING},
    EXECUTING: {REVIEWING, BLOCKED},
    BLOCKED: {EXECUTING},
    REVIEWING: {EXECUTING, DONE},
    DONE: set(),
}

AGENT_NAMES = ("Product", "UI", "Frontend", "Backend", "Mobile", "QA")
DEV_AGENTS = ("Frontend", "Backend", "Mobile")
ACTIVE_STATUSES = (EXECUTING, REVIEWING, BLOCKED)


def can_transition(from_status, to_status):
    return to_status in TRANSITIONS.get(from_status, set())


def label(status):
    return STATUS_LABELS.get(status, status)


def normalize_owner(raw):
    """把任务文件中的 Owner 文本（如 Backend Agent）规范化为 Agent 名。"""
    name = (raw or "").strip().replace(" Agent", "").strip()
    for agent in AGENT_NAMES:
        if agent.lower() == name.lower():
            return agent
    raise ValueError(f"未知 Owner: {raw!r}，应为 {', '.join(AGENT_NAMES)} 之一")
