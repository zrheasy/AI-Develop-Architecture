# Task Specification

**版本：1.2**

---

# 1. Task 定义

Task 是 AI 原生研发流程中的**临时执行契约**。

用于连接：

```text
PM

↓

Agent

↓

Deliverable
```

Task 的目标：

> 明确 Agent 需要完成什么，以及什么结果算完成。

Task 不负责定义实现方式。

---

# 2. Task 与项目对象关系

项目结构：

```text
Project

├── protocols
│
├── features
│
├── TASKS
│
│   ├── UI
│   ├── Mobile
│   ├── Backend
│   └── QA
│
└── {Agent}
```

关系：

|对象|职责|
|-|-|
|Feature|管理长期产品能力|
|Task|管理 Agent 当前工作|
|Deliverable|证明工作完成|
|Decision|保存长期设计决策|

---

# 3. Task 核心原则

## 3.1 Task 管理 What，不管理 How

Task 只定义：

- Goal
- Context
- Acceptance Criteria
- Deliverable

不定义：

- 技术方案
- 实现步骤
- 文件修改方式
- 工具选择

---

## 3.2 Task 不属于 Feature

Feature 不关心：

- 哪个 Agent 完成。
- 创建了多少 Task。
- 执行过程如何。

Feature 只关注：

> 产品能力是否存在。

---

## 3.3 Task 是临时对象

生命周期：

```text
Create（等待中）

↓

Execute（执行中）

↓

Deliverable（审核中）

↓

Review 通过（已完成）
```

Task 完成后：

- 结果进入代码、设计、文档。
- 长期价值进入 Feature 或 Decision。
- Task 可以消失。

---

# 4. Task 存储结构

Task 与 Feature 同级：

```text
Project/

├── protocols/（协议文档，只读引用）

├── features/

├── tasks/

│   ├── UI/
│   │
│   │   ├── INDEX.md
│   │   └── TASK-XXX.md
│   │
│   ├── Mobile/
│   │
│   │   ├── INDEX.md
│   │   └── TASK-XXX.md
│   │
│   ├── Backend/
│   │
│   └── QA/
│
└── Agents/{Agent}/（Agent 工作空间，不包含协议文件）
```

Task 按 Agent 分类，任务文件原地存放，不按状态移动。

每个 `tasks/{Agent}/` 包含：

- `INDEX.md`：任务索引，由 PM 维护，按状态分类记录任务地址与优先级。
- `TASK-XXX.md`：任务文件，由 PM 创建与写入。

原因：

- 明确 Owner。
- 降低 Agent 查找成本。
- 符合 Agent 职责边界。
- 任务状态不依赖文件位置，避免文件移动造成索引失真。

---

# 5. Task 状态

Task 状态由 PM 在 `tasks/{Agent}/INDEX.md` 中维护，按状态分类记录任务地址。

状态分类：

```text
等待中

↓

执行中

↓

审核中

↓

已完成
```

---

## 等待中

任务已创建，等待前置输入完备（PRD、UI 规范、API 契约等）。

Agent 不读取该分类。

## 执行中

前置输入完备，PM 已将任务翻转为执行状态。

Agent 从该分类按优先级读取任务执行。

## 审核中

Agent 已完成并提交，等待 PM 审核；或审核失败后 Agent 重新执行中。

任务保留在审核中分类，不因审核失败移回执行中。

## 已完成

PM 审核通过，任务结束。

普通任务可删除，长期价值沉淀至 Feature / Decision。

审核结果（PASS / FAIL）与失败原因记录在 TASK 文件中。

---

# 6. Task 标准模板

```markdown
# Task


## ID

TASK-XXX


## Title

任务名称


## Owner

负责 Agent


## Goal

需要完成的目标。


## Context

必要背景：

Feature:

Background:

Constraints:


## Acceptance Criteria

完成标准：

- 
- 


## Deliverable

需要交付：

- 


## Review Result

PASS / FAIL


## Failure Reason

审核失败时由 PM 填写。
```

## 6.1 Deliverable 地址要求

Task 完成后，Task 文件必须记录可直接访问的实际交付物地址。`Deliverable` 不得只写抽象类型，例如「API 文档」或「Git Commit」。

标准格式：

```markdown
## Deliverable

- [交付说明](../../Agents/{Agent}/deliverables/TASK-XXX-description.md)
- Commit: `abc1234`
- Verification: `41 passed`
```

交付物文档只记录结果、必要说明、验证摘要和风险；完整过程、代码细节与测试日志保留在代码、测试资产或 Agent workspace 中，不在 Deliverable 中重复。

---

# 7. PM 创建 Task 流程

## Step 1：分析需求

判断：

- 是否已有 Feature。
- 是否需要哪个 Agent。
- 是否缺少前置输入。

---

## Step 2：确定 Owner Agent

根据 Agent Contract 分配。

例如：

|需求|Agent|
|-|-|
|设计背景图|UI Agent|
|实现页面修改|Mobile Agent|
|接口开发|Backend Agent|
|验证功能|QA Agent|

---

## Step 3：创建 Task

创建任务文件并保存至：

```text
tasks/{Agent}/
```

例如：

```text
tasks/UI/TASK-APP-WELCOME-UI-001.md
```

在 `tasks/{Agent}/INDEX.md` 中登记为「等待中」。

---

## Step 4：翻转为执行中

前置输入完备后（PRD、UI 规范、API 契约等），PM 将索引状态由「等待中」更新为「执行中」，并通知 Agent。

Agent 不自行判断前置输入是否完备，不自行翻转状态。

---

# 8. Agent 获取 Task

Agent 不搜索任务，不直接浏览 `tasks/` 目录。

通过自己的 ACTIVE.md 中的固定 Task Index 指针读取：

```text
tasks/{Agent}/INDEX.md
```

INDEX.md 由 PM 维护。

Agent 只读取「执行中」与「审核中」分类：

- 正常执行：从「执行中」按优先级读取一个任务。
- 审核失败后重新执行：从「审核中」读取当前任务。

Agent 工作流程：

```text
protocols/Agents/{Agent}/CONTRACT.md

↓

protocols/Agents/{Agent}/MAPP.md

↓

protocols/Agents/{Agent}/CAPABILITY.md

↓

PROJECT.md

↓

ACTIVE.md

↓

TASK INDEX（tasks/{Agent}/INDEX.md）

↓

TASK

↓

DECISIONS.md（按需）
```

执行规则：

- 一次只执行一个任务。
- 任务完成前不读取下一个任务。
- 等待 PM 审核期间不读取下一个任务。
- 审核失败时重新执行当前任务，不跳任务。

Agent 读取：

- Goal
- Context
- Acceptance Criteria
- Deliverable

然后自主决定：

- 实现方案。
- 执行步骤。
- 技术选择。

---

# 9. Task 更新规则

TASK 文件由 PM 创建与写入，Agent 不修改。

## PM 更新

- INDEX.md：任务状态分类（等待中 / 执行中 / 审核中 / 已完成）与优先级顺序。
- TASK 文件：Review Result（PASS / FAIL）与 Failure Reason。
- Acceptance Criteria（需求变化时）。

优先级调整时，PM 在 INDEX.md 中调整顺序并追加备注（日期与原因）。

## Agent 更新

- 自己的 ACTIVE.md：任务状态（执行中 / 审核中）、下一步行动、阻塞、Deliverable 地址。
- 不修改 TASK 文件。
- 不修改 INDEX.md。

原因：

Task 是执行契约，不是过程记录；INDEX.md 是任务状态的唯一真相来源。

---

# 10. Task 完成处理

## Agent 提交

Agent 完成任务后：

1. 更新自己的 ACTIVE.md：任务状态为「审核中」（REVIEW），附上 Deliverable 文件地址。
2. 通知 PM 查看 ACTIVE.md 进行审核。
3. 等待审核结果，不读取下一个任务。

## PM 审核

PM 查看 Agent 的 ACTIVE.md，对照验收标准审核。

### 审核通过

- INDEX.md 状态更新为「已完成」。
- TASK 文件记录 Review Result：PASS。
- 通知 Agent，Agent 读取下一个「执行中」任务。

### 审核失败

- TASK 文件记录 Review Result：FAIL，并填写 Failure Reason。
- 索引条目保留在「审核中」，不移回「执行中」。
- 通知 Agent 查看失败原因并重新执行。

Agent 重新执行完成后，再次更新 ACTIVE.md 为「审核中」并提交，流程循环直至通过。

---

## 普通任务

例如：

- 修改颜色。
- 替换图片。
- UI 微调。

处理：

INDEX.md 移入「已完成」，任务文件可删除。

---

## 长期价值任务

例如：

- 新增系统能力。
- 产生架构决策。

处理：

更新 Feature / Decision，INDEX.md 移入「已完成」，任务文件可删除。

---

# 11. 最终原则

```text
Feature

管理：

系统有什么能力


Task

管理：

现在让哪个 Agent 做什么


Deliverable

证明：

工作已经完成
```

最终流程：

```text
User Request

↓

PM Analysis

↓

Create Task + INDEX 登记「等待中」

↓

PM 翻转「执行中」并通知 Agent

↓

Agent ACTIVE.md → INDEX.md 获取 Task

↓

Agent Execution

↓

Agent 更新 ACTIVE 为「审核中」+ Deliverable 地址

↓

PM Review

↓

通过 → INDEX「已完成」/ 失败 → TASK 记录原因，Agent 重新执行
```

核心原则：

> PM 管理目标和验收，Agent 管理实现和执行，Task 只是连接两者的临时契约。

---

# 12. Task 对话与职责边界

## PM 派发消息

PM 派发消息只引用 Task 文件和必要依赖，不复制 Task 中已有的背景、约束和验收标准。

## Agent 完成消息

Agent 完成消息必须使用最小格式：

```text
Status: DONE / BLOCKED
Deliverable: 实际文件地址
Commit: commit hash（如适用）
Verification: 测试摘要
Blockers: 无 / 阻塞说明
```

## 文件边界

- PM 维护治理域：`PROJECT.md`、`ACTIVE.md`、`DECISIONS.md`、`CHANGELOG.md`、`requirements/`、`features/`、`tasks/`。
- Agent 维护执行域：`Agents/{Agent}/workspace/`、`Agents/{Agent}/deliverables/` 及自身 `ACTIVE.md`。
- PM 不得直接修改执行域代码、测试、配置或设计资产。
- Agent 不得修改 PM 维护的 Task、INDEX、Feature 或 Product Requirement；发现问题必须反馈 PM。
