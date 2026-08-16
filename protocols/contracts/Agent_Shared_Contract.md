# Agent Shared Contract

**版本：** 2.2

**定位：** PM 与所有 Agent 的共享条款。各角色只保留领域差异（见 `contracts/`）。

---

# 1. 职责边界

- 不越权：不修改其他 Agent 职责范围，不替代其他专业角色，不修改未经授权的长期决策。
- 不扩大职责：发现需求缺失、范围变化或跨领域问题时，反馈 PM，由 PM 重新分配 Task。

---

# 2. 执行域边界

## 数据库访问边界

- 数据库（schema、表、数据、迁移、造数、数据修复）的写操作仅由 Backend Agent 执行；其他 Agent（Product / UI / Frontend / Mobile / QA）只能读取数据库，不得执行任何写操作。
- 其他 Agent 确需写入数据库时，必须向用户申请写权限，经用户批准后方可执行，并记录变更原因与范围。
- Backend Agent 的数据库写操作也必须以 Task 授权为准，不得超出任务范围修改数据。

---

# 3. 最小输入

PM 通知 Agent 时只发送执行任务所必需的信息，内容不超过100字：

- Task 文件地址。
- Owner Agent。
- 前置依赖是否满足。
- 其他必须信息。

---

# 4. 最小输出

Agent 对 PM 的完成通知只包含，内容不超过100字：

```text
Status: REVIEW / BLOCKED
Deliverable: 实际文件地址 / 无（阻塞时）
Blockers: 无 / 阻塞说明
```