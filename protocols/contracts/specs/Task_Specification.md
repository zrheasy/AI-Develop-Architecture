# Task Specification

**版本：** 2.0

---

# 1. 定义

Task 是临时执行契约，连接 PM → Agent → Deliverable。它定义 Agent 完成什么、什么结果算完成，不定义实现方式。

---

# 2. 存储结构

`tasks/{Agent}/` 包含：

- `INDEX.md`：任务索引，由 PM 维护，按状态分类记录任务地址与优先级。
- `TASK-XXX.md`：任务文件，由 PM 创建与写入。

任务文件原地存放，不按状态移动；状态不依赖文件位置。

---

# 3. 状态机（唯一真相来源）

状态由 PM 在 `INDEX.md` 中维护：

```text
等待中 → 执行中 → 审核中 → 已完成
```

| 状态 | 含义 | Agent 行为 |
|---|---|---|
| 等待中 | 已创建，等待前置输入完备 | 不读取该分类 |
| 执行中 | 前置输入完备，已翻转 | 按优先级读取执行 |
| 审核中 | 已提交待审核，或审核失败后重新执行中 | 保留在审核中，不因失败移回执行中 |
| 已完成 | 审核通过 | 任务文件可删除，长期价值沉淀到 Feature / Decision |

---

# 4. 标准模板

```markdown
# Task

## ID
TASK-XXX

## Title

## Owner

## Goal

## Context
Feature:
Background:
Constraints:

## Risk Level
L0 / L1 / L2 / L3

## QA Required
Yes / No

## QA Decision Reason
说明是否需要 QA，以及判断依据。

## Acceptance Criteria
- ...

## Deliverable
- [交付说明](../../Agents/{Agent}/deliverables/TASK-XXX-description.md)
- Commit: `abc1234`
- Verification: `41 passed`

## Review Result
PASS / FAIL

## Failure Reason
```

Deliverable 必须记录可直接访问的实际交付物地址，不得只写抽象类型（如「API 文档」）。

## 轻量 Task 的验证要求

当 Task 为 L0 且 QA Required 为 No 时，Owner Agent 必须完成与改动直接相关的最小自测；自测至少包含必要的单元测试、构建或浏览器检查之一；Deliverable 必须记录实际验证命令与结果；PM 只检查范围、交付完整性和验证证据；不得因为形式完整性自动创建 QA Task。

## QA 验证范围控制

QA Task 必须明确验证目标、不验证的范围、最大样本数或测试边界、必须输出的证据和阻塞时的汇报条件。QA 不得重复执行与验收目标无关的完整回归。

---

# 5. PM 创建流程

1. 分析需求：是否已有 Feature、需要哪个 Agent、是否缺少前置输入。
2. 确定 Owner：按 Agent 文档 / Agent Directory 分配。
3. 创建任务文件并登记 INDEX.md 为「等待中」。
4. 前置输入完备后翻转为「执行中」并通知 Agent。

Agent 不自行判断前置输入是否完备，不自行翻转状态。

---

# 6. Agent 获取与执行

通过自身 ACTIVE.md 的固定指针读取 INDEX.md，只读取「执行中」（按优先级取一个）与「审核中」（重新执行当前任务）。

读取 Goal / Context / Acceptance Criteria / Deliverable，然后自主决定实现方案、执行步骤与技术选择。

规则：一次只执行一个任务；完成或等待审核期间不读取下一个任务；审核失败重新执行当前任务，不跳任务。

---

# 7. 更新与文件边界

PM 更新：INDEX.md（状态、优先级，调整时追加日期与原因备注）、TASK 文件（Review Result / Failure Reason / Acceptance Criteria）。

Agent 更新：自身 ACTIVE.md（任务状态、下一步、阻塞、Deliverable 地址）。不修改 TASK 文件与 INDEX.md。

---

# 8. 完成处理

- Agent：更新 ACTIVE.md 为「审核中」并附 Deliverable 地址，通知 PM，等待审核。
- PM 通过：INDEX.md 移入「已完成」，TASK 记录 PASS，通知 Agent 读取下一个任务。
- PM 失败：TASK 记录 FAIL 与 Failure Reason，索引保留「审核中」，通知 Agent 重新执行。

---

# 9. 开发类 Task 版本交付要求

Deliverable 必须包含 Commit、Branch、Merge Target、Verification；无 commit hash 的 Task 不得通过验收。

分支流程（详见 `workflows/Agent_Workflow.md` 分支协议）：`dev → feature/<feature-slug> → dev → main`。
