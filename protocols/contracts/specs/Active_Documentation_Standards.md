# ACTIVE.md Standard

**版本：** 2.0

---

# 1. 作用

记录项目当前执行上下文：当前正在做什么、下一步做什么。

---

# 2. 标准结构

```markdown
# Active State

## Current Goal
当前最重要目标。

## Current Phase
Planning / Implementation / Review。

## Task Status
执行中 / 审核中。

## Active Work
当前进行中的工作。

## Next Action
下一步行动。

## Blockers
当前阻塞。

## Deliverables
任务状态为「审核中」时填写交付物地址。

## Task Index
固定指针：tasks/{Agent}/INDEX.md（PM 维护，Agent 不修改）。

## Related Context
Feature / Task / Decision 引用。

## Last Updated
更新时间。
```

---

# 3. 更新规则

- 目标、阶段、下一步、阻塞变化时更新。
- 任务完成：Task Status 更新为「审核中」，填写 Deliverables，通知 PM。
- 审核失败：重新执行当前任务，Task Status 更新为「执行中」。
- 审核通过：Next Action 更新为读取下一个「执行中」任务。
- 保持简短、当前、可执行。

---

# 4. 不记录

历史过程、完整任务列表、技术实现细节、已完成工作的日志。任务内容与状态保存在 `tasks/`，技术决策保存在 `DECISIONS.md` 或 Task Deliverable。

---

# 5. 核心原则

记录「现在发生什么」，不记录「过去发生什么」，不定义「应该如何实现」。
