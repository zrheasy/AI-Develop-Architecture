# Agent Shared Contract

**版本：** 2.0

**定位：** 所有 Agent 文档的共享条款。各 Agent 只保留领域差异（见 `contracts/agents/`）。

---

# 1. 职责边界

- 不越权：不修改其他 Agent 职责范围，不替代其他专业角色，不修改未经授权的长期决策。
- 不扩大职责：发现需求缺失、范围变化或跨领域问题时，反馈 PM，由 PM 重新分配 Task。

---

# 2. 执行域边界

Agent 只修改自身执行域文件（`Agents/{Agent}/workspace/`、`Agents/{Agent}/deliverables/`）和自身 `ACTIVE.md`，不得修改：

- PM 维护的 `tasks/`、`requirements/`、`features/`、项目级核心文件。
- 其他 Agent 的 workspace、deliverables 或决策文件。

需要跨域修改时，反馈 PM，由 PM 创建或调整对应 Task。

---

# 3. 最小输出

Agent 对 PM 的完成通知只包含：

```text
Status: DONE / BLOCKED
Deliverable: 实际文件地址
Commit: commit hash（如适用）
Verification: 测试摘要
Blockers: 无 / 阻塞说明
```

Task 已提供的信息不在通知中重复展开。

---

# 4. Contract 维护

仅当 Agent 职责、组织结构、长期能力范围变化时更新本文件；不因单个 Task、临时需求或一次方案修改。
