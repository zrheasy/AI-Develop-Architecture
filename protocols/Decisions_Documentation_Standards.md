# DECISIONS.md Standard

**Version:** 1.0

---

# 1. Purpose

DECISIONS.md 是项目的长期决策索引。

用于帮助 Agent 理解：

> 为什么项目采用当前设计方向。

只记录仍然影响未来工作的关键 Decision。

---

# 2. Principle

DECISIONS.md：

记录：

- 长期有效的设计决策。
- 影响多个 Feature / Agent 的原则。
- 未来需要遵守的约束。

不记录：

- Task执行过程。
- Feature内容。
- 临时方案。
- 讨论历史。

---

# 3. Structure

DECISIONS.md 只作为索引。

详细 Decision 存放：

```
decisions/
```

结构：

```
Project/

├── DECISIONS.md

└── decisions/

    ├── authentication.md

    ├── architecture.md

    └── api.md
```

---

# 4. Index Format

示例：

```markdown
# Decisions Index


## Authentication

身份认证相关决策。

File:

decisions/authentication.md


## Architecture

系统架构相关决策。

File:

decisions/architecture.md
```

---

# 5. Decision File Format

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

# 6. Creation Rules

创建 Decision 前确认：

- 是否会长期影响未来开发？
- 是否会影响多个 Agent 或 Feature？
- 如果 Agent 不知道它，是否容易做错？

满足任一条件，可以创建。

---

# 7. Maintenance Rules

DECISIONS.md 不保存历史。

规则：

- 有长期价值 → 保留。
- 无长期价值 → 删除。
- 内容重复 → 合并。

历史由 Git 保存。

---

# 8. Agent Usage

Agent 不读取所有 Decision。

流程：

```
DECISIONS.md

↓

找到相关领域

↓

读取对应 Decision 文件
```

---

# 9. Core Principle

Decision 记录：

> 为什么这样设计。

不记录：

> 曾经发生过什么。