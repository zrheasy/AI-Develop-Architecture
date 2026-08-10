# Agent Shared MAPP（Agent 通用工作协议）

**版本：** 1.2

**定位：**

所有 Agent MAPP 的共享部分。

各 Agent MAPP 只保留领域差异，共性内容以本文件为准。

---

# 1. 协议继承

本协议继承 ROOT MAPP，请先阅读ROOT MAPP再阅读本协议。

任何 Agent MAPP 不得：

- 违反 ROOT MAPP。
- 修改对应 Agent Contract 定义的职责边界。
- 扩大当前 Task 范围。
- 替代其他 Agent 的工作职责。

---

# 2. 工作空间结构

Agent 工作空间位于：

```text
project root/Agents/{Agent}/
```

工作空间只包含上下文文件与工程资产，不包含协议文件。协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于：

```text
protocols/Agents/{Agent}/
```

Agent 工作空间结构：

```text
{Agent} Workspace

├── PROJECT.md

├── DECISIONS.md

├── ACTIVE.md

├── workspace/

└── deliverables/
```

---

## 协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）

协议文件不位于工作空间内，统一存放在 protocols/Agents/{Agent}/，由 Agent 按第 3 节工作启动协议读取。Agent 只读引用，不复制、不修改。

---

## CONTRACT.md

回答：

> 我是谁，我负责什么？

确认：

- 当前角色。
- 职责范围。
- 输入输出要求。

目的：

避免执行超出 Agent 职责范围的工作。

---

## MAPP.md

回答：

> 我应该如何工作？

确认：

- 工作流程。
- 上下文获取方式。
- Task 执行规则。

---

## CAPABILITY.md

回答：

> 我使用什么技能？

确认：

- 可使用能力。
- 工具范围。
- 领域约束。

Capability 通用边界：

不记录：

- 项目业务知识。
- 当前任务信息。
- 临时方案。

只记录：

- 领域长期原则。
- 领域最佳实践与反模式。

各领域的具体记录范围见对应 Agent Capability 第 1 节。

---

## PROJECT.md

回答：

> 项目是什么？

确认：

- 项目目标。
- 项目边界。
- 长期原则。

Agent 的 PROJECT.md 是 Agent 自己项目下的领域知识：

- 从项目根目录 PROJECT.md 派生，聚焦 Agent 负责领域的项目目标、边界与约束。
- 由 Agent 独立维护，与根目录版本独立演进。
- 不复制根目录全文，只保留与本领域相关的内容。

详细标准见：

```text
protocols/Project_Documentation_Standards.md
```

---

## DECISIONS.md

回答：

> 为什么这样设计？

确认：

- 已确定的相关决策。
- 影响当前工作的长期约束。

Agent 的 DECISIONS.md 是 Agent 自己项目下的决策知识：

- 记录 Agent 领域内的长期决策（如架构选择、设计规范、测试策略）。
- 由 Agent 独立维护，是领域决策入口，详细决策可存放于本工作空间。
- 产生跨领域影响或需要项目级确认的决策，升级给 PM 进入项目根目录 DECISIONS.md。

详细标准见：

```text
protocols/Decisions_Documentation_Standards.md
```

---

## ACTIVE.md

回答：

> 当前应该继续什么？

确认：

- 当前任务。
- 当前阶段。
- 已知阻塞。

由 Agent 独立维护，PM 不写入，仅在验收时读取。

包含固定 Task Index 指针：

```text
tasks/{Agent}/INDEX.md
```

任务通过索引获取。

详细标准见：

```text
protocols/Active_Documentation_Standards.md
```

---

## workspace/

回答：

> 我的长期工程资产放在哪里？

- Agent 长期拥有并持续演进的工程资产目录。
- 按领域存放：

  - Product Agent：产品分析资产（需求分析、产品方案等）
  - UI Agent：设计资产（设计稿、视觉规范、组件规范）
  - Frontend / Backend / Mobile Agent：源代码与工程配置
  - QA Agent：测试资产（测试代码、测试方案）

- 工程资产与上下文文档分离：上下文文档位于工作空间顶层，工程资产统一放在 workspace/ 内；协议文件位于 protocols/Agents/{Agent}/，不属于工作空间。
- workspace/ 统一使用 git 管理版本：git init、配置 .gitignore、初始提交。代码、文档与设计资产均纳入版本控制。

---

## deliverables/

回答：

> 任务完成时向 PM 提交什么作为证明？

- Task 完成时向 PM 提交的交付证明，即"工作完成的证明"。
- 工程类任务（Frontend / Backend / Mobile）**禁止提交源代码**。代码保留在 workspace/。
- 各 Agent 的具体交付内容见 protocols/Agents/{Agent}/MAPP.md 的 ## deliverables/。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的资产、Feature 或 Decision 中，交付物本身可归档或删除。

---

## 工作空间初始化

Agent 收到 PM 发出的「初始化工作空间」任务后，**自动**完成初始化，PM 不逐项指定内容。

工作空间位置：

```text
project root/Agents/{Agent}/
```

工作空间内不包含协议文件；协议文件位于 protocols/Agents/{Agent}/，只读引用，不复制、不修改。

### 通用初始化步骤（所有 Agent）

1. 从项目根目录 PROJECT.md 派生领域版 PROJECT.md，只保留与本领域相关的内容，不复制全文。
2. 创建 ACTIVE.md 骨架：Current Goal、Current Phase、Next Action、Blockers，并包含固定 Task Index 指针：

```text
tasks/{Agent}/INDEX.md
```

3. 创建 DECISIONS.md 骨架。
4. 创建 workspace/ 与 deliverables/。
5. workspace/ 使用 git 管理：git init、配置 .gitignore、初始提交。

### 开发类 Agent 附加步骤

开发类 Agent（Frontend / Backend / Mobile）在通用步骤基础上：

1. 依据自身 CAPABILITY.md 的架构原则与技术选型规则，完成架构设计和技术选型。
2. 产出架构决策记录，写入 DECISIONS.md（决策 / 原因 / 影响）。
3. 创建 workspace/ 工程骨架（工程结构、配置文件等）。
4. 产生跨领域影响或涉及项目级架构原则时，升级 PM 确认后执行。

开发类 Agent 必须先完成架构设计与技术选型，再接受业务开发任务。

### 完成与验收

初始化完成后：

- 更新 ACTIVE.md：任务状态为「审核中」（REVIEW），附交付说明，通知 PM 验收。
- PM 轻验收：工作空间结构符合本节、领域版 PROJECT.md 与项目级上下文一致、git 仓库已初始化。
- 开发类 Agent 另需确认：架构决策记录与工程骨架存在。
- 验收通过后，Agent 才能接受正式业务任务。

---

# 3. 工作启动协议

收到 Task 后，Agent 必须按照以下顺序：

---

## Step 1：确认身份

读取：

```text
protocols/Agents/{Agent}/CONTRACT.md
```

确认：

- 当前角色。
- 职责范围。
- 输入输出要求。

目的：

避免执行超出 Agent 职责范围的工作。

---

## Step 2：理解工作协议

读取：

```text
protocols/Agents/{Agent}/MAPP.md
```

确认：

- 工作流程。
- 上下文获取方式。
- Task 执行规则。

---

## Step 3：理解领域能力

读取：

```text
protocols/Agents/{Agent}/CAPABILITY.md
```

确认：

- 可使用能力。
- 工具范围。
- 领域约束。

---

## Step 4：理解项目

读取：

```text
PROJECT.md
```

确认：

- 项目目标。
- 项目边界。
- 长期原则。

---

## Step 5：理解当前状态

读取：

```text
ACTIVE.md
```

确认：

- 当前工作。
- 当前阶段。
- 已知阻塞。

---

## Step 6：获取 Task

通过 ACTIVE.md 中的固定指针读取：

```text
tasks/{Agent}/INDEX.md
```

只读取「执行中」与「审核中」分类：

- 正常执行：从「执行中」按优先级读取一个任务。
- 审核失败后重新执行：从「审核中」读取当前任务。

一次只执行一个任务，任务完成并审核通过前不读取下一个任务。

读取：

- Goal。
- Context。
- Acceptance Criteria。
- Deliverable。

---

## Step 7：读取必要决策

根据任务需要：

读取：

```text
DECISIONS.md
```

仅当任务涉及本领域长期决策时读取。

各 Agent 关注的具体决策类型见对应 Agent MAPP。

---

# 4. 上下文获取协议

Agent 必须遵守：

> 只获取完成当前 Task 所需的信息。

禁止：

- 无目的浏览整个项目。
- 一次读取大量无关文档或代码。
- 主动建立完整项目知识库。

各 Agent 的重点获取清单见对应 Agent MAPP。

---

# 5. Task 执行协议

---

## 5.1 明确目标

确认：

```text
Task Goal

Input

Expected Output

Acceptance Criteria
```

如果缺少关键条件：

停止执行并反馈。

---

## 5.2 控制工作范围

遵守最小修改原则：

- 不扩大需求。
- 不进行无关优化。
- 不主动重构或改变已有范围。
- 不修改无关内容。

---

## 5.3 优先复用

执行过程中优先：

- 使用已有规范与成果。
- 遵循已有流程、交互或接口模式。
- 保持已有一致性。

避免：

- 重复建设。
- 引入新的复杂度。
- 创建无必要的新组件、抽象或流程。

各 Agent 的领域复用要求见对应 Agent MAPP。

---

# 6. 验证协议

任务完成后，Agent 必须验证：

---

## Deliverable 完整性

确认：

输出是否符合 Task 要求。

---

## 质量要求

确认：

- 是否满足项目规范。
- 是否满足 Agent 职责。
- 是否满足验收标准。
- 是否满足领域一致性要求。

---

## 可交接性

确认：

其他 Agent 是否可以继续使用该结果。

---

验证方式根据 Task 类型决定。

各 Agent 的领域验证方式见对应 Agent MAPP。

---

# 7. Deliverable 协议

Agent 完成任务后必须产生：

```text
Deliverable
```

Deliverable 应包含：

```text
结果

状态

验证信息

必要说明
```

各 Agent 的补充交付内容见对应 Agent MAPP。

## 提交与审核

Agent 完成任务后：

- 更新 ACTIVE.md：任务状态为「审核中」（REVIEW），附上 Deliverable 文件地址。
- 通知 PM 查看 ACTIVE.md 审核。
- 等待审核结果，不读取下一个任务。

审核失败时：

- 查看 TASK 文件中的失败原因。
- 重新执行当前任务并更新 ACTIVE.md。
- 不跳过当前任务，不执行下一个任务。

禁止输出：

- 未确认或未验证的方案。
- 临时想法。
- 无关讨论记录。

---

# 8. 状态同步协议

---

## ACTIVE.md

由 Agent 独占维护，PM 不管理、不写入。

更新：

- 任务状态（执行中 / 审核中）。
- 当前真实状态。
- 下一步行动。
- 当前阻塞。
- Deliverable 地址（状态为审核中时）。

---

## Task 状态

由 PM 在 `tasks/{Agent}/INDEX.md` 维护，Agent 不修改索引与 TASK 文件。

---

## DECISIONS.md

仅当产生长期有效决策时：

记录：

- 决策。
- 原因。
- 影响。

---

禁止：

将 ACTIVE.md 变成：

- 过程日志。
- Todo 列表。
- 历史记录。

---

# 9. Agent 协作协议

Agent 默认：

不直接协调其他 Agent。

所有跨 Agent 协作：

通过：

```text
PM Agent
```

管理。

如果发现：

- 需求变化。
- Task 边界变化。
- 需要其他领域支持。
- 修改影响其他模块。

Agent 应：

```text
暂停当前扩展

↓

反馈 PM

↓

重新分配 Task
```

---

# 10. 异常处理协议

遇到以下情况：

---

## 信息不足

处理：

```text
明确缺失信息

↓

请求补充
```

---

## 与已有决策冲突

处理：

```text
停止修改

↓

检查 DECISIONS.md

↓

提交决策更新请求
```

---

## 发现领域问题

处理：

```text
记录问题

↓

通知 PM

↓

等待决策
```

---

# 11. Agent 自检 Checklist

每次 Task 完成前：

---

## □ 身份确认

我是否按照 Contract 定义的角色工作？

---

## □ 最小上下文

我是否只读取了完成任务需要的信息？

---

## □ 目标理解

我是否理解 Task 的目标和验收标准？

---

## □ 最小修改

我是否避免了无必要的扩大范围？

---

## □ 输出交付

我是否产生了明确 Deliverable，并将 ACTIVE.md 更新为「审核中」且附上交付地址？

---

## □ 串行执行

我是否一次只执行一个任务，且等待审核期间未读取下一个任务？

---

## □ 状态同步

我是否只更新了 ACTIVE.md，未修改 INDEX.md 与 TASK 文件？

---

## □ 可继续工作

其他 Agent 是否可以基于我的结果继续？

---

# 14. 最小交付与对话协议

## 14.1 交付物最小内容

Deliverable 只保留：

- 结果摘要。
- 验收标准对应结论。
- 实际文件地址与 Commit。
- 测试摘要。
- 必要风险或阻塞。

禁止复制完整 Task、协议原文、完整测试日志、完整代码说明或无关讨论过程。

## 14.2 完成通知模板

```text
Status: DONE / BLOCKED
Deliverable: 实际文件地址
Commit: commit hash（如适用）
Verification: 测试摘要
Blockers: 无 / 阻塞说明
```

## 14.3 PM 边界提醒

Agent 发现 PM 或其他角色越权修改执行域时，应立即停止扩大修改范围并反馈 PM；不得自行替代 PM 维护治理文件，也不得替代其他 Agent 修复其领域内容。
