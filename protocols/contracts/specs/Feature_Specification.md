# Feature Specification

**版本：** 2.1

## 1. 定义

Feature 是用户可感知、可独立验收、可长期演进的软件能力单元。PM 用 Feature 管理产品能力，不管理具体任务，不描述技术实现。

核心关系：`User Request → Product Requirement → Feature → Task → Deliverable`

## 2. 与 Product Requirement 的边界

| 对象 | 回答 | 负责内容 |
|---|---|---|
| Product Requirement | 为什么做、做什么 | 用户需求、产品方案、范围和验收标准 |
| Feature | 产品长期具备什么能力 | 能力定义、产品范围、生命周期和演进方向 |

Product Requirement 可以创建或更新 Feature；Feature 不重复记录需求分析过程。

## 3. 划分原则

按用户能力划分，例如 Authentication、Payment，不按技术实现划分，例如 OAuth API、Login Button。

一个 Feature 应同时满足：

- 用户可以理解；
- 具备独立用户价值；
- 可以独立验收；
- 生命周期超过单个 Task；
- 未来可能持续演进。

建议层级：`Product Area → Feature → Task`。过细会造成 Feature 泛滥，过粗会导致边界模糊。

## 4. Owner 与生命周期

Owner：PM Agent。

生命周期：

```text
PLANNING → ACTIVE → STABLE → DEPRECATED → ARCHIVED
```

- `PLANNING`：已定义，尚未进入实施；
- `ACTIVE`：正在建设或持续迭代；
- `STABLE`：能力稳定维护；
- `DEPRECATED`：计划停止使用或被替代；
- `ARCHIVED`：不再维护，仅保留历史记录。

## 5. 创建与更新

### 创建

当需求形成新的、可长期管理的用户能力时创建 Feature。

### 不创建

- 已有 Feature 的范围扩展：更新已有 Feature；
- 技术优化：直接创建 Task；
- Bug 修复：直接创建 Task；
- 不具备独立用户价值的一次性工作：直接创建 Task。

### 更新

仅在以下内容变化时更新 Feature：

- 能力范围；
- 生命周期状态；
- 用户价值或产品方向；
- 关联 Task 或长期决策；
- 演进方向。

Feature 不记录 Task 的执行过程或实时状态。

## 6. 演进记录

只记录影响长期能力理解的历史和未来方向，不记录开发日志或讨论过程。

```markdown
## Evolution

History:
- Added Email Login

Future:
- Passkey Support
```

## 7. 删除、归档与合并

- 默认不直接删除，使用 `ACTIVE → DEPRECATED → ARCHIVED`；
- 错误创建、重复创建或无实际产品意义的 Feature 可以删除；
- 当两个 Feature 的用户价值高度重叠、管理边界不清且没有独立生命周期时，可以合并。

## 8. 文件与内容规范

文件：`features/<name>.md`。

```markdown
# Feature Name

## Goal

## User Value

## Scope
Included: ...
Excluded: ...

## Status
PLANNING / ACTIVE / STABLE / DEPRECATED / ARCHIVED

## Owner
PM Agent

## Related Decisions

## Evolution
History:
- ...
Future:
- ...
```

Feature 不记录：Task 执行状态、开发日志、Bug 明细和技术实现细节。
