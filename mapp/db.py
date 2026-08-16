"""SQLite 持久化：schema、连接与初始化。"""

import os
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS agents (
    name         TEXT PRIMARY KEY,
    status       TEXT NOT NULL DEFAULT 'idle',
    current_task TEXT,
    updated_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    owner           TEXT NOT NULL REFERENCES agents(name),
    status          TEXT NOT NULL,
    risk_level      TEXT NOT NULL,
    qa_required     INTEGER NOT NULL DEFAULT 0,
    qa_reason       TEXT NOT NULL DEFAULT '',
    priority        TEXT NOT NULL DEFAULT 'P1',
    goal            TEXT NOT NULL DEFAULT '',
    context         TEXT NOT NULL DEFAULT '',
    acceptance      TEXT NOT NULL DEFAULT '',
    deliverable_spec TEXT NOT NULL DEFAULT '',
    deliverable     TEXT,
    commit_hash     TEXT,
    branch          TEXT,
    merge_target    TEXT,
    verification    TEXT,
    review_result   TEXT,
    failure_reason  TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS task_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id     TEXT NOT NULL REFERENCES tasks(id),
    from_status TEXT,
    to_status   TEXT NOT NULL,
    actor       TEXT NOT NULL,
    reason      TEXT,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS qa_results (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id    TEXT NOT NULL REFERENCES tasks(id),
    result     TEXT NOT NULL CHECK (result IN ('PASS','FAIL','BLOCKED')),
    report     TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS features (
    name              TEXT PRIMARY KEY,
    title             TEXT NOT NULL,
    goal              TEXT NOT NULL DEFAULT '',
    user_value        TEXT NOT NULL DEFAULT '',
    scope             TEXT NOT NULL DEFAULT '',
    status            TEXT NOT NULL DEFAULT 'PLANNING',
    owner             TEXT NOT NULL DEFAULT 'PM Agent',
    related_decisions TEXT NOT NULL DEFAULT '',
    evolution         TEXT NOT NULL DEFAULT '',
    created_at        TEXT NOT NULL,
    updated_at        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prds (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    user_need      TEXT NOT NULL DEFAULT '',
    goal           TEXT NOT NULL DEFAULT '',
    solution       TEXT NOT NULL DEFAULT '',
    scope          TEXT NOT NULL DEFAULT '',
    feature_impact TEXT NOT NULL DEFAULT '',
    affected_areas TEXT NOT NULL DEFAULT '',
    acceptance     TEXT NOT NULL DEFAULT '',
    status         TEXT NOT NULL DEFAULT 'DRAFT',
    owner          TEXT NOT NULL DEFAULT 'Product Agent',
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decisions (
    topic      TEXT PRIMARY KEY,
    title      TEXT NOT NULL,
    context    TEXT NOT NULL DEFAULT '',
    decision   TEXT NOT NULL DEFAULT '',
    impact     TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feature_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    feature     TEXT NOT NULL REFERENCES features(name),
    from_status TEXT,
    to_status   TEXT NOT NULL,
    actor       TEXT NOT NULL,
    reason      TEXT,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prd_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    prd_id      TEXT NOT NULL REFERENCES prds(id),
    from_status TEXT,
    to_status   TEXT NOT NULL,
    actor       TEXT NOT NULL,
    reason      TEXT,
    created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_owner ON tasks(owner);
CREATE INDEX IF NOT EXISTS idx_events_task ON task_events(task_id);
CREATE INDEX IF NOT EXISTS idx_features_status ON features(status);
CREATE INDEX IF NOT EXISTS idx_prds_status ON prds(status);
"""


def default_db_path(project_root):
    return os.path.join(project_root, ".mapp", "mapp.db")


def connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        _migrate(conn)
        conn.commit()
    finally:
        conn.close()


def _migrate(conn):
    """旧库（含 file 列、缺内容列）平滑升级：补充内容列并移除 file 列。"""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(tasks)").fetchall()}
    for col, decl in (
        ("goal", "TEXT NOT NULL DEFAULT ''"),
        ("context", "TEXT NOT NULL DEFAULT ''"),
        ("acceptance", "TEXT NOT NULL DEFAULT ''"),
        ("deliverable_spec", "TEXT NOT NULL DEFAULT ''"),
    ):
        if col not in cols:
            conn.execute(f"ALTER TABLE tasks ADD COLUMN {col} {decl}")
    if "file" in cols:
        conn.execute("ALTER TABLE tasks DROP COLUMN file")


def now():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


def seed_agents(conn):
    from mapp.state import AGENT_NAMES

    for name in AGENT_NAMES:
        conn.execute(
            "INSERT OR IGNORE INTO agents(name, status, updated_at) VALUES (?, 'idle', ?)",
            (name, now()),
        )
    conn.commit()
