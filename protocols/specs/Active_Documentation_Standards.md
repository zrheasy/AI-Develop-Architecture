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

## Status
空闲（任务状态以 `.mapp/mapp.db` 为准，不在此重复维护）。

## Active Work
当前进行中的工作。

## Next Action
下一步行动。

## Blockers
当前阻塞。

## Deliverables
任务状态为「审核中」时由 `mapp task review` 登记交付物地址；此处只做引用说明，状态以 `.mapp/mapp.db` 为准。

## Task Index
由 `mapp index` 生成，固定指针：tasks/{Agent}/INDEX.md（PM 维护，Agent 不修改）。

## Related Context
Feature / Task / Decision 引用。

## Last Updated
更新时间。
```

---

# 3. 更新规则

- 目标、阶段、下一步、阻塞变化时更新。
- 任务完成：通过 `mapp task review` 提交，状态与交付物由 mapp 登记，通知 PM。
- 审核失败：PM 将 Task 改为「执行中」后，重新执行当前任务。
- 任务阻塞：PM 通过 `mapp task block` 置为「阻塞中」，通知 PM；阻塞解除后 `mapp task unblock` 改回「执行中」。
- 审核通过：Next Action 更新为通过 `mapp task list --status 执行中` 获取下一个任务。
- 保持简短、当前、可执行。

---

# 4. 不记录

历史过程、完整任务列表、技术实现细节、已完成工作的日志。任务内容与状态保存在 `tasks/`，技术决策保存在 `DECISIONS.md` 或 Task Deliverable。

---

# 5. 核心原则

记录「现在发生什么」，不记录「过去发生什么」，不定义「应该如何实现」。
