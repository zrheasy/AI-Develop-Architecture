# Product Requirement Specification

**版本：** 2.0

---

# 1. 定义

Product Requirement 是 Product Agent 对用户需求分析后输出的产品决策摘要，帮助 PM 快速判断 Feature 变化、所需 Agent 与 Task 拆解方式。

只回答：为什么做、做什么、影响什么。不负责：如何实现、怎么开发。

---

# 2. 标准结构

```markdown
# Product Requirement

## ID
PR-XXX

## Title

## User Need
一句话：用户为什么需要。

## Goal
产品希望达到的结果。

## Solution
产品应提供什么能力（不要写技术实现，如「调用 Google OAuth API」）。

## Scope
Included: ...
Excluded: ...

## Feature Impact
Action: CREATE / UPDATE
Feature: <名称>
Change: <能力变化>

## Affected Areas
- UI / Frontend / Backend / Mobile / QA（只标 Required，不描述具体任务）

## Acceptance Criteria
产品验收标准。

## Status
DRAFT / APPROVED

## Owner
Product Agent
```

---

# 3. PM 处理流程

1. Feature 判断：新能力 → Create / Update Feature。
2. Task 拆解：按 Affected Areas 创建对应 Agent 的 Task。
3. 验收：按 Acceptance Criteria 确认 Deliverable。

---

# 4. 存储与生命周期

Product Agent 交付 → PM 审核 → 保存至 `requirements/PR-XXX.md`。

生命周期：Draft → Approved → Completed → Archived / Retained。

完成后：对未来产品演进有参考价值、包含重要产品决策、影响长期 Feature 规划的保留；一次性或临时调整的归档或删除。
