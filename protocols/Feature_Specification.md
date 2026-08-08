# Feature Specification

**Version:** 1.2

---

# 1. Definition

Feature 是用户可感知、可独立验收、可长期演进的软件能力单元。

Feature 用于：

- PM 管理产品能力。
- 用户理解产品能力。
- 跟踪产品长期演进。

Feature 不用于：

- 管理具体执行任务。
- 描述技术实现。
- 记录开发过程。

核心关系：

```text
User Request

↓

Product Requirement

↓

Feature

↓

Task

↓

Deliverable
```

---

# 2. Feature 与 Product Requirement

## Product Requirement

定义：

> 为什么做，以及需要解决什么问题。

负责：

- 用户需求。
- 用户价值。
- 产品目标。
- 产品方案。
- 范围限制。

---

## Feature

定义：

> 产品具备什么长期能力。

负责：

- 能力定义。
- 能力范围。
- 生命周期管理。
- 能力演进方向。

---

关系：

一个 Product Requirement 可以：

- 创建新的 Feature。
- 扩展已有 Feature。
- 不产生 Feature。

示例：

用户需求：

```text
支持 Google 登录
```

PM 分析：

已有：

```text
Feature:

Authentication
```

处理：

更新：

```text
Authentication Scope:

+ Google Login
```

创建 Task：

```text
Implement Google OAuth Login
```

---

# 3. Feature 划分原则

## 3.1 按用户能力划分

Feature 应代表：

> 用户能够理解的一项完整能力。

正确：

```text
Authentication

Payment

Notification

Search
```

错误：

```text
OAuth API

Login Button

Database Migration
```

---

## 3.2 Feature 判断标准

一个 Feature 应满足：

- 用户可以理解。
- 具备独立价值。
- 可以独立验收。
- 生命周期超过单个 Task。
- 可以持续演进。

---

## 3.3 Feature 颗粒度

Feature 不应：

过细：

```text
Google OAuth API

Login Button
```

导致 Feature 泛滥。

过粗：

```text
User System

Business System
```

导致能力边界模糊。

推荐：

```text
Product Area

↓

Feature

↓

Task
```

---

# 4. Feature Owner

Feature 默认负责人：

```text
PM Agent
```

职责：

- 创建 Feature。
- 更新 Feature。
- 管理 Feature 生命周期。
- 保证 Feature 描述准确。

其他 Agent：

- 可以提供分析和建议。
- 不直接修改 Feature 定义。

---

# 5. Feature 生命周期

Feature 生命周期：

```text
PLANNING

↓

ACTIVE

↓

STABLE

↓

DEPRECATED

↓

ARCHIVED
```

---

## PLANNING

能力已确定，但尚未投入使用。

---

## ACTIVE

能力正在开发或持续演进。

---

## STABLE

能力成熟，进入稳定维护阶段。

---

## DEPRECATED

能力不再继续发展，但仍存在于系统。

---

## ARCHIVED

能力已退出当前产品。

---

# 6. Feature 创建规则

PM 创建 Feature 的条件：

## 创建 Feature

当需求形成新的用户能力。

例如：

```text
新增支付能力

↓

Create Payment Feature
```

---

## 不创建 Feature

以下情况不创建：

### 已有 Feature 扩展

例如：

```text
Authentication

新增 Google Login
```

处理：

更新 Feature。

---

### 技术优化

例如：

```text
优化数据库查询

↓

Task
```

---

### Bug 修复

例如：

```text
修复登录异常

↓

Task
```

---

# 7. Feature 更新规则

Feature 只在以下情况更新：

---

## 7.1 Scope 变化

当前能力范围变化。

例如：

```text
Authentication

新增:

- Google Login
```

---

## 7.2 Status 变化

例如：

```text
PLANNING

↓

ACTIVE
```

---

## 7.3 产品方向变化

包括：

- Goal 修改。
- User Value 修改。
- Scope 调整。
- Evolution 更新。

---

Feature 不记录：

- Task 执行状态。
- 开发日志。
- Bug记录。
- 技术实现细节。

---

# 8. Feature Evolution

Evolution 用于记录 Feature 的能力演进。

它不是独立对象。

作用：

- 记录能力历史变化。
- 记录未来发展方向。
- 帮助 PM 和 Agent 理解长期上下文。

示例：

```markdown
## Evolution

History:

- Added Email Login
- Added Google Login
- Added Session Management


Future:

- Apple Login
- Passkey Support
```

---

# 9. Feature 与 Task 状态隔离

Feature 状态：

表示：

> 能力生命周期。

Task 状态：

表示：

> 执行进度。

两者独立。

示例：

```text
Feature:

Authentication

Status:

ACTIVE


Task:

TASK-AUTH-BE-001（记录于 tasks/Backend/INDEX.md）

Status:

已完成
```

Task 完成不会改变 Feature 生命周期。

---

# 10. Feature 删除与归档规则

Feature 不直接删除。

默认流程：

```text
ACTIVE

↓

DEPRECATED

↓

ARCHIVED
```

---

允许删除：

- 错误创建。
- 重复创建。
- 无实际产品意义。

---

# 11. Feature 合并规则

当两个 Feature：

- 用户价值高度重叠。
- 管理边界不清晰。
- 无独立生命周期。

应进行合并。

示例：

原：

```text
User Account

User Profile
```

合并：

```text
Account Management
```

---

# 12. Feature 与 Release

Feature ≠ Release。

Release：

> 产品发布版本。

Feature：

> 产品长期能力。

一个 Feature 可以跨多个 Release 演进。

示例：

```text
Release 1:

Authentication

- Email Login


Release 2:

Authentication

- Google Login
```

仍属于：

```text
Authentication Feature
```

---

# 13. Feature 文件结构

推荐：

```text
features/

├── authentication.md

├── payment.md

└── notification.md
```

---

# 14. Feature 内容规范

Feature 文件保持简洁：

```markdown
# Feature Name


## Goal

为什么存在。


## User Value

用户获得什么价值。


## Scope

Included:

-

Excluded:

-


## Status

PLANNING / ACTIVE / STABLE / DEPRECATED


## Owner

PM Agent


## Related Decisions

相关长期决策。


## Evolution

能力历史和未来方向。
```

---

# 15. Feature 与其他对象边界

|对象|职责|
|-|-|
|Project|定义项目目标|
|Product Area|组织产品能力|
|Product Requirement|定义需求和产品方案|
|Feature|定义长期产品能力|
|Task|定义具体执行工作|
|Deliverable|定义执行结果|
|Decision|记录长期决策原因|
|Release|定义发布版本|

---

# 16. PM Feature 管理原则

PM 管理 Feature 时遵守：

1. Feature 管理能力，不管理任务。
2. 优先扩展已有 Feature，而不是创建新 Feature。
3. 保持 Feature 简洁稳定。
4. 不复制 Task、Decision 和开发记录。
5. 使用 Feature 描述产品当前具备的能力。
6. 使用 Evolution 记录能力演进。
7. 使用 Deprecated 和 Archived 管理能力退出。

最终目标：

> 维护产品能力地图，而不是维护需求列表。