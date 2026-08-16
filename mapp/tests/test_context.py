import os
import contextlib
import io
import sys
import tempfile
import unittest

from mapp.cli import main
from mapp.tests.test_workflow import BACKEND_TASK


class ContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "tasks", "Backend"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "decisions"), exist_ok=True)
        with open(os.path.join(self.root, "decisions", "llm-provider.md"), "w", encoding="utf-8") as fh:
            fh.write("# LLM Provider\n\n选择 deepseek-v4-flash。\n")
        main(["--project", self.root, "init"])

    def tearDown(self):
        self.tmp.cleanup()

    def capture(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(["--project", self.root] + list(args))
        return buf.getvalue()

    def add_task(self, text):
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(text)
        try:
            main(["--project", self.root, "task", "add"])
        finally:
            sys.stdin = old_stdin

    def test_context_includes_task_and_refs(self):
        self.add_task(BACKEND_TASK)
        out = self.capture("context", "TASK-BE-100")
        self.assertIn("TASK-BE-100", out)
        self.assertIn("decisions/llm-provider.md", out)
        self.assertIn("选择 deepseek-v4-flash", out)
        # 不包含其他无关文档
        self.assertNotIn("ACTIVE.md", out)

    def test_context_reports_missing_ref(self):
        text = BACKEND_TASK.replace("llm-provider.md", "nonexistent.md")
        self.add_task(text)
        out = self.capture("context", "TASK-BE-100")
        self.assertIn("引用（未找到）: decisions/nonexistent.md", out)
