# ACTIVE.md Standard

**Version:** 1.0

---

# 1. Purpose

ACTIVE.md 是项目的当前执行上下文。

用于帮助 Agent 快速理解：

> 当前正在做什么，以及下一步应该做什么。

---

# 2. Principle

ACTIVE.md 只记录当前有效状态。

记录：

- 当前目标。
- 当前阶段。
- 当前工作。
- 下一步行动。
- 当前阻塞。

不记录：

- 历史过程。
- 完整任务列表。
- 技术实现细节。
- 已完成工作的日志。

---

# 3. Structure

```markdown
# Active State


## Current Goal

当前阶段最重要目标。


## Current Phase

当前阶段：

Planning

Implementation

Review


## Task Status

当前任务状态：

执行中 / 审核中


## Active Work

当前正在进行的工作。


## Next Action

下一步行动。


## Blockers

当前阻塞。


## Deliverables

当前任务完成后交付物地址（状态为审核中时填写）。


## Task Index

固定指针，由 PM 维护，Agent 不修改：

tasks/{Agent}/INDEX.md


## Related Context

Feature:

Task:

Decision:


## Last Updated

更新时间。
```

---

# 4. Example

```markdown
# Active State


## Current Goal

完成 Authentication Feature 扩展。


## Current Phase

Implementation


## Task Status

审核中


## Active Work

Google Login integration。


## Next Action

等待 Backend Task 完成后进行联调。


## Blockers

OAuth configuration pending。


## Deliverables

deliverables/google-login-result.md


## Task Index

tasks/Frontend/INDEX.md


## Related Context

Feature:

features/authentication.md


Task:

TASK-AUTH-BE-001


Decision:

decisions/authentication.md


## Last Updated

2026-08-06
```

---

# 5. Update Rules

以下情况更新 ACTIVE.md：

- 当前目标变化。
- 工作阶段变化。
- 下一步行动变化。
- 出现或解除阻塞。
- 任务完成：Task Status 更新为「审核中」，填写 Deliverables 地址，通知 PM。
- 审核失败：重新执行当前任务，Task Status 更新为「执行中」。
- 审核通过：更新 Next Action 为读取下一个「执行中」任务。

保持：

- 简短。
- 当前。
- 可执行。

---

# 6. Do Not Record

不要记录：

## History

例如：

```
昨天完成：

- API设计
- UI修改
```

---

## Task Details

任务内容与状态保存在：

```
tasks/{Agent}/
tasks/{Agent}/INDEX.md
```

ACTIVE.md 只提供 Task Index 指针，不复制任务内容。

---

## Technical Decisions

技术方案保存：

```
DECISIONS.md
```

或 Task Deliverable。

---

# 7. Agent Usage

Agent 工作流程：

```
PROJECT.md

↓

ACTIVE.md

↓

TASK INDEX（tasks/{Agent}/INDEX.md）

↓

Task

↓

相关 Decision
```

Agent 通过 ACTIVE.md 中的 Task Index 指针获取任务入口，只读取「执行中」与「审核中」分类。

---

# 8. Quality Checklist

创建或更新 ACTIVE.md 前确认：

□ Agent 是否能快速知道当前目标？

□ 是否只包含当前状态？

□ 是否删除历史信息？

□ 是否提供下一步行动？

□ 是否关联正确的 Feature / Task / Decision？

□ 任务完成时是否将 Task Status 更新为「审核中」并附上 Deliverable 地址？

□ 是否通过 Task Index 获取任务，而非直接浏览任务目录？

---

# 9. Core Principle

ACTIVE.md 记录：

> 现在发生什么。

不记录：

> 过去发生什么。

不定义：

> 应该如何实现。
