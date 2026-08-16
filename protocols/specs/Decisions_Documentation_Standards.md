# DECISIONS.md Standard

**版本：** 2.0

---

# 1. 作用

项目长期决策索引，帮助 Agent 理解「为什么采用当前设计方向」。

---

# 2. 结构

`DECISIONS.md` 只作为索引；详细决策统一存于 `.mapp/mapp.db` 的 `decisions` 表，通过 `mapp decision` 命令管理（`add` 从 stdin 登记、`list` / `show` 查询、`import` 导入存量文件）。存量 `decisions/<topic>.md` 文件可用 `mapp decision import` 一次性导入后不再维护。

stdin 提交内容格式：

```markdown
# Decision Topic

## Context
背景。

## Decision
最终决策。

## Impact
影响范围。
```

---

# 3. 创建规则

满足任一条件即可创建：
- 长期影响未来开发;
- 影响多个 Agent 或 Feature;
- 不知道它会容易做错。

---

# 4. 维护规则

- 不保存历史，历史由 Git 保存。
- 有长期价值保留，无价值删除，内容重复合并。
- Agent 不读取所有 Decision：通过 `mapp decision list` 找到相关领域，再用 `mapp decision show <topic>` 读取。

---

# 5. 核心原则

记录「为什么这样设计」，不记录「曾经发生过什么」。
