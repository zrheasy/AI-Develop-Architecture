# Feature Specification

**版本：** 2.0

---

# 1. 定义

Feature 是用户可感知、可独立验收、可长期演进的软件能力单元。PM 用它管理产品能力，不管理执行任务、不描述技术实现。

核心关系：`User Request → Product Requirement → Feature → Task → Deliverable`

---

# 2. 与 Product Requirement 的边界

| 对象 | 回答 | 负责 |
|---|---|---|
| Product Requirement | 为什么做、解决什么问题 | 用户需求、产品方案、范围限制 |
| Feature | 产品具备什么长期能力 | 能力定义、范围、生命周期、演进 |

---

# 3. 划分原则

- 按用户能力划分（如 Authentication、Payment），不按技术实现（如 OAuth API、Login Button）。
- 满足：用户可理解、具备独立价值、可独立验收、生命周期超过单个 Task、可持续演进。
- 颗粒度：Product Area → Feature → Task；过细导致泛滥，过粗导致边界模糊。

---

# 4. Owner 与生命周期

Owner：PM Agent。

生命周期：PLANNING → ACTIVE → STABLE → DEPRECATED → ARCHIVED。

---

# 5. 创建与更新规则

创建：需求形成新的用户能力（如新增支付）。

不创建：已有 Feature 扩展（更新 Scope）、技术优化（Task）、Bug 修复（Task）。

更新：仅当 Scope 变化、Status 变化、产品方向变化时。

---

# 6. Evolution

记录能力历史与未来方向：

```markdown
## Evolution
History:
- Added Email Login

Future:
- Passkey Support
```

---

# 7. 删除、归档与合并

- 不直接删除，默认流程 ACTIVE → DEPRECATED → ARCHIVED。
- 允许删除：错误创建、重复创建、无实际产品意义。
- 合并条件：用户价值高度重叠、管理边界不清、无独立生命周期。

---

# 8. 与其他对象边界

| 对象 | 职责 |
|---|---|
| Feature | 长期产品能力 |
| Task | 当前执行工作 |
| Deliverable | 执行结果证明 |
| Decision | 长期决策原因 |
| Release | 发布版本（Feature 可跨多个 Release 演进） |

---

# 9. 文件与内容规范

文件：`features/<name>.md`，保持简洁：

```markdown
# Feature Name

## Goal
## User Value
## Scope
Included: ...
Excluded: ...
## Status
PLANNING / ACTIVE / STABLE / DEPRECATED
## Owner
PM Agent
## Related Decisions
## Evolution
```

Feature 不记录：Task 执行状态、开发日志、Bug、技术实现细节。
