# Agent Shared Contract

**版本：** 2.1

**定位：** PM 与所有 Agent 的共享条款。各角色只保留领域差异（见 `contracts/agents/`）。

---

# 1. 职责边界

- 不越权：不修改其他 Agent 职责范围，不替代其他专业角色，不修改未经授权的长期决策。
- 不扩大职责：发现需求缺失、范围变化或跨领域问题时，反馈 PM，由 PM 重新分配 Task。

---

# 2. 执行域边界

## Agent 执行域

Agent 只修改自身执行域（`Agents/{Agent}/`）内的文件，不得修改：

- PM 维护的 `tasks/`、`requirements/`、`features/`、项目级核心文件。
- 其他 Agent 的工作空间（`Agents/{其他Agent}/`）或决策文件。

需要跨域修改时，反馈 PM，由 PM 创建或调整对应 Task。

## PM 执行域

PM 只维护治理域（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`、`requirements/`、`features/`、`tasks/`、`decisions/`），不得修改任何 Agent 工作空间（`Agents/{Agent}/`）内的文件。

用户反馈产品问题时，PM 应创建或调整对应 Task，协调相关 Agent 解决；不得直接修改 Agent 工作空间代为实现或修复。

---

# 3. 最小输入

PM 通知 Agent 时只发送完成任务所必需的信息：

- Task 文件地址。
- Owner Agent。
- 前置依赖是否满足。
- 启动或完成后的下一状态。

Task 已提供的信息不在通知中重复展开。

---

# 4. 最小输出

Agent 对 PM 的完成通知只包含：

```text
Status: REVIEW / BLOCKED
Deliverable: 实际文件地址 / 无（阻塞时）
Blockers: 无 / 阻塞说明
```

Deliverable 已提供的信息不在通知中重复展开。
