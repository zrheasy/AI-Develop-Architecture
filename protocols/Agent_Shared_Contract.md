# Agent Shared Contract（Agent 通用契约条款）

**版本：** 1.1

**定位：**

所有 Agent Contract 的共享条款。

各 Agent Contract 只保留领域差异，公共条款以本文件为准。

---

# 1. Agent Boundary Rules

所有 Agent 必须遵守：

---

## 不越权

Agent 不得：

- 修改其他 Agent 的职责范围。
- 替代其他专业角色。
- 修改未经授权的长期决策。

---

## 不扩大职责

如果发现：

- 需求缺失。
- 范围变化。
- 其他领域问题。

应：

```text
反馈 PM Agent

↓

重新分配 Task
```

---

# 1.1 最小输出与执行域边界

## Agent 输出

Agent 对 PM 的完成通知只包含：

- 状态：`DONE` 或 `BLOCKED`。
- 实际 Deliverable 地址。
- Commit（如适用）。
- 测试摘要。
- 阻塞项（如有）。

Task 已提供的信息不在通知中重复展开。

## 执行域边界

Agent 只修改自身负责的执行域文件和自身 `ACTIVE.md`，不得修改：

- PM 维护的 `tasks/`、`requirements/`、`features/`、项目级核心文件。
- 其他 Agent 的 workspace、deliverables 或决策文件。

需要跨域修改时，必须反馈 PM，由 PM 创建或调整对应 Task。

---

# 2. Contract Maintenance

Agent Contract 更新规则：

只有以下情况需要修改：

- Agent 职责发生变化。
- 组织结构调整。
- 长期能力范围变化。

不应因为：

- 单个 Task。
- 临时需求。
- 一次方案。

修改 Contract。
