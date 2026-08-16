import contextlib
import io
import os
import tempfile
import unittest

from mapp.cli import main

BACKEND_TASK = """# Task

## ID
TASK-BE-100

## Title
测试后端任务

## Owner
Backend Agent

## Goal
完成测试目标。

## Context
Feature: daily-events-digest
Inputs:
- decisions/llm-provider.md
Constraints:
- 不改变 API 契约

## Risk Level
L2

## QA Required
Yes
Reason: 测试 QA 门禁

## Acceptance Criteria
- 结果可检查

## Deliverable
- [交付说明](../../Agents/Backend/deliverables/TASK-BE-100.md)

## Review Result

## Failure Reason
"""

FRONTEND_TASK = """# Task

## ID
TASK-FE-100

## Title
测试前端任务

## Owner
Frontend Agent

## Goal
完成前端测试目标。

## Context
Feature: daily-events-digest
Inputs:
- features/daily-events-digest.md
Constraints:
- 不改变 API 契约

## Risk Level
L0

## QA Required
No
Reason: 纯样式

## Acceptance Criteria
- 页面可渲染

## Deliverable
- [交付说明](../../Agents/Frontend/deliverables/TASK-FE-100.md)

## Review Result

## Failure Reason
"""


class MappFlowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        for agent in ("Backend", "Frontend"):
            os.makedirs(os.path.join(self.root, "tasks", agent), exist_ok=True)
        os.makedirs(os.path.join(self.root, "decisions"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "features"), exist_ok=True)
        self.be_file = os.path.join(self.root, "tasks", "Backend", "TASK-BE-100.md")
        self.fe_file = os.path.join(self.root, "tasks", "Frontend", "TASK-FE-100.md")
        with open(self.be_file, "w", encoding="utf-8") as fh:
            fh.write(BACKEND_TASK)
        with open(self.fe_file, "w", encoding="utf-8") as fh:
            fh.write(FRONTEND_TASK)
        with open(os.path.join(self.root, "decisions", "llm-provider.md"), "w", encoding="utf-8") as fh:
            fh.write("# LLM Provider\n\n选择 deepseek-v4-flash。\n")
        with open(os.path.join(self.root, "features", "daily-events-digest.md"), "w", encoding="utf-8") as fh:
            fh.write("# Feature: daily-events-digest\n\n每日事件日报。\n")
        main(["--project", self.root, "init"])

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, expect_error=False):
        argv = ["--project", self.root] + list(args)
        if expect_error:
            with self.assertRaises(SystemExit):
                main(argv)
            return
        main(argv)

    def capture(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["--project", self.root] + list(args))
        return buf.getvalue()

    def make_deliverable(self, agent, task_id):
        path = os.path.join(self.root, "Agents", agent, "deliverables", f"{task_id}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# 交付说明\n\n## 结论\n验收标准全部满足。\n")
        return os.path.relpath(path, self.root)

    def test_add_and_index(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        index_path = os.path.join(self.root, "tasks", "Backend", "INDEX.md")
        self.assertTrue(os.path.exists(index_path))
        content = open(index_path, encoding="utf-8").read()
        self.assertIn("TASK-BE-100", content)
        self.assertIn("等待中", content)

    def test_assign_requires_complete_fields(self):
        text = open(self.be_file, encoding="utf-8").read()
        text = text.replace(
            "## Deliverable\n- [交付说明](../../Agents/Backend/deliverables/TASK-BE-100.md)\n",
            "## Deliverable\n",
        )
        with open(self.be_file, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        self.run_cli("task", "assign", "TASK-BE-100", expect_error=True)

    def test_full_flow_with_qa_gate(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        self.run_cli("task", "assign", "TASK-BE-100")
        deliverable = self.make_deliverable("Backend", "TASK-BE-100")
        self.run_cli("task", "review", "TASK-BE-100", "--deliverable", deliverable)
        # QA Required=Yes 无 QA PASS → 不得验收通过
        self.run_cli("task", "pass", "TASK-BE-100", expect_error=True)
        # 开发类 Task 无 Commit 信息 → 不得验收通过
        self.run_cli("qa", "TASK-BE-100", "--result", "PASS", "--report", "Agents/QA/deliverables/report.md")
        self.run_cli(
            "task", "commit", "TASK-BE-100",
            "--hash", "beef001", "--branch", "feature/live-data", "--target", "dev", "--verification", "pytest ok",
        )
        self.run_cli("task", "pass", "TASK-BE-100")
        # 已完成任务不可再次派发
        self.run_cli("task", "assign", "TASK-BE-100", expect_error=True)
        out = self.capture("audit", "--task", "TASK-BE-100")
        self.assertIn("等待中 → 执行中", out)
        self.assertIn("执行中 → 审核中", out)
        self.assertIn("审核中 → 已完成", out)

    def test_dev_commit_gate(self):
        self.run_cli("task", "add", "tasks/Frontend/TASK-FE-100.md")
        self.run_cli("task", "assign", "TASK-FE-100")
        deliverable = self.make_deliverable("Frontend", "TASK-FE-100")
        self.run_cli("task", "review", "TASK-FE-100", "--deliverable", deliverable)
        self.run_cli("task", "pass", "TASK-FE-100", expect_error=True)
        self.run_cli(
            "task", "commit", "TASK-FE-100",
            "--hash", "abc123", "--branch", "feature/x", "--target", "dev", "--verification", "pytest ok",
        )
        self.run_cli("task", "pass", "TASK-FE-100")

    def test_no_parallel(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        second = os.path.join(self.root, "tasks", "Backend", "TASK-BE-101.md")
        text = (
            open(self.be_file, encoding="utf-8").read()
            .replace("TASK-BE-100", "TASK-BE-101")
            .replace("测试后端任务", "第二个任务")
        )
        with open(second, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-101.md")
        self.run_cli("task", "assign", "TASK-BE-100")
        self.run_cli("task", "assign", "TASK-BE-101", expect_error=True)

    def test_block_unblock(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        self.run_cli("task", "assign", "TASK-BE-100")
        self.run_cli("task", "block", "TASK-BE-100", "--reason", "环境不可用")
        out = self.capture("task", "list", "--status", "阻塞中")
        self.assertIn("TASK-BE-100", out)
        self.run_cli("task", "unblock", "TASK-BE-100")
        out = self.capture("task", "list", "--status", "执行中")
        self.assertIn("TASK-BE-100", out)

    def test_fail_patches_file_and_returns_to_executing(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        self.run_cli("task", "assign", "TASK-BE-100")
        deliverable = self.make_deliverable("Backend", "TASK-BE-100")
        self.run_cli("task", "review", "TASK-BE-100", "--deliverable", deliverable)
        self.run_cli("task", "fail", "TASK-BE-100", "--reason", "验收证据不足")
        content = open(self.be_file, encoding="utf-8").read()
        self.assertIn("FAIL", content)
        self.assertIn("验收证据不足", content)
        self.run_cli("task", "review", "TASK-BE-100", "--deliverable", deliverable)

    def test_qa_blocked_flips_task(self):
        self.run_cli("task", "add", "tasks/Backend/TASK-BE-100.md")
        self.run_cli("task", "assign", "TASK-BE-100")
        deliverable = self.make_deliverable("Backend", "TASK-BE-100")
        self.run_cli("task", "review", "TASK-BE-100", "--deliverable", deliverable)
        self.run_cli("qa", "TASK-BE-100", "--result", "BLOCKED", "--report", "Agents/QA/deliverables/blocked.md")
        out = self.capture("task", "list", "--status", "阻塞中")
        self.assertIn("TASK-BE-100", out)
