import contextlib
import io
import os
import sys
import tempfile
import unittest

from mapp.cli import main

FEATURE_TEXT = """# Daily Events Digest

## Goal
每天输出 3~5 个中文 AI 大事件。

## User Value
用户每天 3 分钟掌握重要进展。

## Scope
Included:
- 每日抓取与筛选

Excluded:
- 本周趋势

## Status
PLANNING

## Owner
PM Agent
"""

PRD_TEXT = """# Product Requirement

## ID
PR-001

## Title
AI 大事件 MVP

## User Need
用户需要省时的 AI 信息入口。

## Goal
让用户每天 3 分钟掌握重要事件。

## Solution
每日大事件日报。

## Scope
Included: 日报
Excluded: 趋势

## Feature Impact
Action: CREATE
Feature: daily-events-digest

## Affected Areas
- Product
- Backend

## Acceptance Criteria
- 可查看日报

## Status
DRAFT

## Owner
Product Agent
"""

DECISION_TEXT = """# LLM 供应商

## Context
流水线需要 LLM。

## Decision
统一使用 deepseek-v4-flash。

## Impact
按该模型适配。
"""


class ObjectsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        main(["--project", self.root, "init"])

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, stdin_text=None, expect_error=False):
        old_stdin = sys.stdin
        if stdin_text is not None:
            sys.stdin = io.StringIO(stdin_text)
        try:
            if expect_error:
                with self.assertRaises(SystemExit):
                    main(["--project", self.root] + list(args))
            else:
                main(["--project", self.root] + list(args))
        finally:
            sys.stdin = old_stdin

    def capture(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["--project", self.root] + list(args))
        return buf.getvalue()

    def test_feature_full_lifecycle(self):
        self.run_cli("feature", "add", stdin_text=FEATURE_TEXT)
        out = self.capture("feature", "list")
        self.assertIn("daily-events-digest", out)
        self.assertIn("PLANNING", out)
        self.run_cli("feature", "status", "daily-events-digest", "ACTIVE")
        out = self.capture("feature", "list")
        self.assertIn("ACTIVE", out)
        self.run_cli("feature", "status", "daily-events-digest", "PLANNING", expect_error=True)
        out = self.capture("feature", "show", "daily-events-digest")
        self.assertIn("每天输出 3~5 个中文 AI 大事件", out)

    def test_prd_status_machine(self):
        self.run_cli("prd", "add", stdin_text=PRD_TEXT)
        self.run_cli("prd", "status", "PR-001", "APPROVED")
        out = self.capture("prd", "list")
        self.assertIn("APPROVED", out)
        self.run_cli("prd", "status", "PR-001", "DRAFT", expect_error=True)
        self.run_cli("prd", "status", "PR-001", "ARCHIVED")

    def test_decision_add_show(self):
        self.run_cli("decision", "add", stdin_text=DECISION_TEXT)
        out = self.capture("decision", "list")
        self.assertIn("llm-", out)
        out = self.capture("decision", "list")
        topic_line = next(line for line in out.splitlines() if line.startswith("| llm"))
        topic = topic_line.split("|")[1].strip()
        out = self.capture("decision", "show", topic)
        self.assertIn("统一使用 deepseek-v4-flash", out)

    def test_import_idempotent(self):
        feat_dir = os.path.join(self.root, "features")
        dec_dir = os.path.join(self.root, "decisions")
        os.makedirs(feat_dir, exist_ok=True)
        os.makedirs(dec_dir, exist_ok=True)
        with open(os.path.join(feat_dir, "daily-events-digest.md"), "w", encoding="utf-8") as fh:
            fh.write(FEATURE_TEXT)
        with open(os.path.join(dec_dir, "llm-provider.md"), "w", encoding="utf-8") as fh:
            fh.write(DECISION_TEXT)
        self.run_cli("feature", "import", "features")
        self.run_cli("decision", "import", "decisions")
        self.run_cli("feature", "import", "features")
        self.run_cli("decision", "import", "decisions")
        out = self.capture("feature", "list")
        self.assertEqual(out.count("daily-events-digest"), 1)
