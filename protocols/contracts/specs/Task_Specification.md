# Task Specification

**版本：** 2.2

## 1. 定义

Task 是连接 PM、Agent 与 Deliverable 的临时执行契约，定义：

- Agent 要完成的目标；
- 完成所需的输入与约束；
- 判断完成的验收标准；
- 需要提交的交付物与验证证据。

Task 定义结果，不规定具体实现方式。

## 2. 存储结构

`tasks/{Agent}/` 包含：

- `INDEX.md`：任务索引，由 PM 维护任务状态、优先级和文件地址；
- `TASK-XXX.md`：任务文件，由 PM 创建和维护。

任务文件始终原地存放，状态只以 `INDEX.md` 为准，不随状态移动文件。

## 3. 状态机

```text
等待中 → 执行中 → 审核中 → 已完成
             ↘ 阻塞中 ↗

审核失败：审核中 → 执行中
```

| 状态 | 含义 | Agent 行为 |
|---|---|---|
| 等待中 | 任务已创建，但前置输入尚未完备 | 不读取、不执行 |
| 执行中 | 前置输入已完备，可以开始执行 | 按优先级获取并执行一个任务 |
| 审核中 | Agent 已提交交付物，等待 PM 验收 | 等待审核结果；不得读取或执行下一个任务 |
| 阻塞中 | 当前任务因输入、环境、权限或依赖无法继续 | 填写阻塞信息并等待 PM 解除；不得继续猜测或扩大范围 |
| 已完成 | PM 已验收通过 | 不再执行；长期价值沉淀到 Feature 或 Decision |

PM 在 `INDEX.md` 维护状态。Agent 不修改 `INDEX.md`，也不自行翻转任务状态。

## 4. 任务模板

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
Inputs:
Constraints:

## Risk Level
L0 / L1 / L2 / L3

## QA Required
Yes / No
Reason:

## Acceptance Criteria
- ...

## Deliverable
- [交付物说明](../../Agents/{Agent}/deliverables/TASK-XXX-description.md)

## Review Result
PASS / FAIL

## Failure Reason
```

### 字段要求

- `Goal`：说明任务要达成的结果。
- `Context`：仅提供完成任务所需的背景、输入和约束。
- `Risk Level`：标记任务风险等级，用于决定验证深度。
- `QA Required`：说明是否需要 QA 参与，并记录判断理由。
- `Acceptance Criteria`：必须可检查，不使用“适当”“完整”等无法判断的表述。
- `Deliverable`：记录可直接访问的实际交付物地址，不得只写抽象类型。
- `Review Result`：由 PM 在验收后填写；未验收时留空。
- `Failure Reason`：仅在验收失败时填写具体原因。

当 `QA Required` 为 `Yes` 时，QA 必须提交 `PASS`；没有 QA `PASS`，PM 不得将 Task 标记为「已完成」。QA `BLOCKED` 时，Task 保持「阻塞中」，不得以 Owner 自测替代。

### 特殊验证要求

当 `Risk Level` 为 L0 且 `QA Required` 为 No 时，Owner Agent 必须完成与改动直接相关的最小自测，至少执行以下一项：必要的单元测试、构建检查或浏览器检查。Deliverable 必须记录实际验证命令与结果。PM 只检查任务范围、交付完整性和验证证据，不因形式完整性自动创建 QA Task。

QA Task 必须明确验证目标、排除范围、测试边界、所需证据以及阻塞时的汇报条件。QA 不执行与验收目标无关的完整回归。

## 5. PM 创建与分配

1. 分析需求：确认关联 Feature、Owner、风险等级和前置输入。
2. 创建任务文件，填写目标、上下文、验收标准和交付要求。
3. 在 `INDEX.md` 登记为「等待中」。
4. 前置输入完备后，将任务翻转为「执行中」并通知 Owner Agent。

前置输入不足时，PM 不得将任务翻转为「执行中」。

## 6. Agent 获取与执行

Agent 通过自身 `ACTIVE.md` 中的固定指针读取 `INDEX.md`，只获取：

- 「执行中」中优先级最高的一个任务；或
- 当前 `ACTIVE.md` 指向的返工任务。

Agent 读取任务的 `Goal`、`Context`、`Acceptance Criteria` 和 `Deliverable` 后，自主决定实现方案、执行步骤与技术选择。

一次只执行一个任务。完成后提交审核，等待审核期间不读取下一个任务；审核失败时 PM 将状态改为「执行中」，Agent 依据 `Failure Reason` 重新执行当前任务。

如果发现输入不足、需求变化或任务超出职责范围，暂停执行并反馈 PM，不自行扩大任务范围。

## 7. 完成与验收

### Agent

1. 完成验收标准要求的结果和验证。
2. 生成 Deliverable，并记录验证信息。
3. 更新自身 `ACTIVE.md` 为「审核中」，附 Deliverable 地址。
4. 通知 PM 验收并等待结果。

无法继续时，更新自身 `ACTIVE.md` 为「阻塞中」，写明阻塞原因、影响和所需处理，并通知 PM；不提交为完成。

### PM

- 验收通过：将 `INDEX.md` 状态改为「已完成」，在 Task 中记录 `PASS`，通知 Agent 获取下一个任务。
- 验收失败：在 Task 中记录 `FAIL` 和具体 `Failure Reason`，将 `INDEX.md` 改为「执行中」，通知原 Agent 返工。
- 收到阻塞通知：将 `INDEX.md` 改为「阻塞中」；阻塞解除后改为「执行中」并通知 Agent。

## 8. 开发类 Task 的版本交付

开发类 Task 的 Deliverable 必须包含：

- Commit hash；
- Branch；
- Merge Target；
- Verification。

缺少 Commit hash 的开发类 Task 不得通过验收。
