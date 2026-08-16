# DECISIONS.md Standard

**版本：** 2.0

---

# 1. 作用

项目长期决策索引，帮助 Agent 理解「为什么采用当前设计方向」。

---

# 2. 结构

`DECISIONS.md` 只作为索引，详细决策存放于 `decisions/`：

```markdown
# Decisions Index

## <领域>
相关决策说明。
File: decisions/<topic>.md
```

决策文件格式：

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
- Agent 不读取所有 Decision：从索引找到相关领域，再读对应文件。

---

# 5. 核心原则

记录「为什么这样设计」，不记录「曾经发生过什么」。
