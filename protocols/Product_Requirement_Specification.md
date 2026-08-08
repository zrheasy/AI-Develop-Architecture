# Product Requirement Specification

**Version: 1.1**

---

# 1. Definition

Product Requirement 是：

> Product Agent 对用户需求进行分析后输出的产品决策摘要。

目标：

帮助 PM 快速判断：

- 是否需要创建/更新 Feature。
- 需要哪些 Agent。
- 如何拆解 Task。

---

# 2. 核心职责

Product Requirement 只负责：

```text
为什么做？

做什么？

影响什么？
```

不负责：

```text
如何实现？

怎么开发？

开发过程？
```

---

# 3. 标准结构

文件：

```text
requirements/

└── PR-XXX.md
```

模板：

```markdown
# Product Requirement


## ID

PR-XXX


## Title

需求名称


## User Need

用户需求和问题。


## Goal

希望达成的产品目标。


## Solution

产品方案。


## Scope

Included:

-

Excluded:

-


## Feature Impact

Create / Update:

Feature Name


## Affected Areas

- UI
- Frontend
- Backend
- Mobile
- QA


## Acceptance Criteria

产品验收标准。


## Status

DRAFT / APPROVED


## Owner

Product Agent
```

---

# 4. 字段说明

## User Need

回答：

> 为什么用户需要它？

只需要一句话。

例如：

```text
用户希望使用已有账号快速登录，减少注册步骤。
```

---

## Goal

回答：

> 产品希望达到什么结果？

例如：

```text
降低登录流程复杂度，提高用户进入系统的成功率。
```

---

## Solution

回答：

> 产品应该提供什么能力？

这是最重要字段。

例如：

```text
增加 Google 登录方式。

用户可以选择 Google 账号完成登录。

保留原有邮箱登录。
```

注意：

不要写：

```text
调用 Google OAuth API
```

这是技术实现。

---

## Scope

回答：

> 这次需求边界是什么？

例如：

Included:

```text
- Google Login
```

Excluded:

```text
- Apple Login
- 社交账号绑定
```

目的：

防止 Task 扩大范围。

---

## Feature Impact

这是 PM 最关注的信息。

格式：

```text
Action:

CREATE / UPDATE


Feature:

Authentication


Change:

Add Google Login capability
```

例如：

已有：

```text
Authentication Feature
```

结果：

```text
UPDATE

Scope:

+ Google Login
```

而不是创建：

```text
Google Login Feature
```

---

## Affected Areas

用于 PM 分配 Task。

例如：

```text
UI

Frontend

Backend

QA
```

不需要描述具体任务。

错误：

```text
Backend:

Implement OAuth callback API
```

正确：

```text
Backend:

Required
```

---

## Acceptance Criteria

用于 PM 验收。

例如：

```text
- 用户可以使用Google账号登录。

- 登录成功后进入系统。

- 原登录方式正常工作。
```

---

# 5. Google Login 示例

```markdown
# Product Requirement


## ID

PR-AUTH-001


## Title

Google Login


## User Need

用户希望使用已有Google账号快速登录。


## Goal

降低登录成本，提高登录成功率。


## Solution

增加Google登录入口。

用户可以通过Google账号完成登录。

保留邮箱登录方式。


## Scope

Included:

- Google Login


Excluded:

- Apple Login


## Feature Impact

Action:

UPDATE


Feature:

Authentication


Change:

Add Google Login capability


## Affected Areas

- UI
- Frontend
- Backend
- QA


## Acceptance Criteria

- 用户可以完成Google登录。

- 原邮箱登录正常。


## Status

APPROVED


## Owner

Product Agent
```

---

# 6. PM收到后的处理流程

PM读取 Product Requirement 后：

只需要完成三个判断：

## 判断1：Feature

```text
是否新能力？

↓

Create Feature

或

Update Feature
```

---

## 判断2：Task

根据：

```text
Affected Areas
```

创建：

```text
UI Task

Frontend Task

Backend Task

QA Task
```

---

## 判断3：验收

根据：

```text
Acceptance Criteria
```

确认 Deliverable。

---

# 7. Storage and Lifecycle

## Storage

Product Requirement 由 Product Agent 输出后：

1. Product Agent 将 Product Requirement 交付给 PM。
2. PM 审核后，将其复制保存至：

```text
requirements/

└── PR-XXX.md
```

3. `Product_Requirements` 目录用于保存项目中的 Product Requirement 记录。

---

## Lifecycle

Product Requirement 的生命周期：

```text
Draft

↓

Approved

↓

Completed

↓

Archived / Retained
```

规则：

- 开发过程中：
  - Product Requirement 用于支持 Feature 判断、Task 拆解和 PM 验收。

- 需求完成后：
  - PM 判断是否具有长期产品参考价值。

保留：

- 对未来产品演进有参考价值。
- 包含重要产品决策。
- 影响长期 Feature 规划。

归档或删除：

- 一次性需求分析。
- 临时调整。
- 无长期参考价值的需求。