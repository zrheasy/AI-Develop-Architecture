# Product Requirement Specification

**版本：** 2.1

## 1. 定义

Product Requirement（PR）是 Product Agent 对用户需求进行分析后形成的产品决策摘要，帮助 PM 判断 Feature 变化、参与领域和 Task 拆解方式。

PR 只回答：为什么做、做什么、影响什么；不描述技术实现，也不替代 Task。

## 2. 标准结构

```markdown
# Product Requirement

## ID
PR-XXX

## Title

## User Need
一句话说明用户为什么需要。

## Goal
产品希望达到的结果。

## Solution
产品应提供的能力，不写技术实现。

## Scope
Included: ...
Excluded: ...

## Feature Impact
Action: CREATE / UPDATE
Feature: <名称>
Change: <能力变化>

## Affected Areas
- Product / UI / Frontend / Backend / Mobile / QA

## Acceptance Criteria
- ...

## Status
DRAFT / APPROVED / ARCHIVED

## Owner
Product Agent
```

### 字段要求

- `User Need`：描述用户问题或需求，不直接写解决方案；
- `Goal`：描述期望产生的产品结果；
- `Solution`：描述用户可使用的产品能力，不写 API、数据库或代码方案；
- `Scope`：明确本次包含和排除的范围；
- `Feature Impact`：说明创建新 Feature 还是更新已有 Feature；
- `Affected Areas`：只标记受影响的职责领域，不拆具体 Task；
- `Acceptance Criteria`：描述产品结果必须满足的可检查条件；
- `Status`：由 Product Agent 创建为 `DRAFT`，经 PM 审核后变为 `APPROVED`。

## 3. Product Agent 与 PM 流程

1. Product Agent 分析用户需求，创建 `DRAFT` PR。
2. PM 检查用户价值、产品方案、范围、Feature 影响、受影响领域和验收标准。
3. 信息完整且方向明确时，PM 将 PR 标记为 `APPROVED` 并保存至 `requirements/PR-XXX.md`；否则退回补充。
4. PM 根据已批准的 PR 创建或更新 Feature，并按 `Affected Areas` 拆解 Task。
5. Task 的交付和验收依据 PR 的产品验收标准执行；PR 本身不记录 Task 执行状态。

## 4. 存储与保留

Product Agent 交付后，PR 先以 `DRAFT` 状态存在；PM 审核通过后保存至 `requirements/PR-XXX.md`。

已批准的 PR 默认保留。当 PR 已被新决策取代，或仅包含一次性、临时调整且不再影响未来工作时，可以标记为 `ARCHIVED`。
