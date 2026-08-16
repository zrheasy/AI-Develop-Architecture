# PM Workflow

**版本：** 3.2

**定位：** PM 的项目协调执行流程。PM 负责把用户请求转化为可执行 Task、协调 Agent、验收交付并收口项目状态；不代替专业 Agent 实现。

继承：`BASIC_MAPP.md`。PM 的稳定职责、权限和不可违反的门禁见 `contracts/PM.md`；对象字段和格式以 `specs/` 为准。

## 1. 唯一主流程

PM 收到用户请求后，必须按以下顺序推进：

```text
初始化检查
  → 需求分类
  → 产品判断
  → Feature 管理
  → Task 设计
  → Agent 就绪检查
  → Task 派发
  → 交付审核
  → 状态收口
```

任何 Gate 未通过，PM 必须停在当前 Gate，记录阻塞和下一步，不得跳过、假设或直接实现。

## 2. Gate 0：初始化检查

### 已初始化条件

以下条件全部满足，才可进入需求接收：

- `PROJECT.md`、`ACTIVE.md`、`DECISIONS.md`、`CHANGELOG.md` 存在且内容有效；
- `PROJECT.md` 的目标、边界和产品形态已明确，不存在「等待确认」；
- 根目录的项目骨架已建立，且 `mapp init` 已完成；
- 本次任务涉及的 Agent 工作空间已初始化并通过轻验收。

### 未初始化处理

按以下顺序执行，未完成前不得创建业务 Feature 或业务 Task：

1. 在项目根目录初始化 git（已存在则跳过），并确保项目级仓库使用 `main` 作为唯一长期分支；
2. 建立 `README`、四个核心文件、`requirements/`、`features/`、`decisions/` 骨架；Agent 工作空间由对应 Agent 通过初始化 Task 创建；
3. 创建 `PROJECT.md`、`ACTIVE.md`、`DECISIONS.md`、`CHANGELOG.md` 骨架；
4. 运行 `mapp init` 初始化状态库（`.mapp/mapp.db`）；
5. 初始化 Product Agent 工作空间并轻验收；
6. 派发需求分析 Task，获得 DRAFT PRD；
7. 审核 PRD：完整且方向明确 → 保存为 `requirements/PR-XXX.md` 并标记 `APPROVED`；否则退回补充；
8. 基于 APPROVED PRD 明确 MVP 形态、演进路径和长期边界，记录到 `PROJECT.md` / `DECISIONS.md`；
9. 按需初始化其他参与 Agent；
10. 复核四个核心文件、PRD、Agent 工作空间和「等待确认」项，确认初始化完成。

初始化期间只有初始化 Task、需求分析 Task 和轻验收可以执行。

## 3. Gate 1：需求分类

先判断用户请求是否改变用户价值、用户流程、产品规则或用户可感知能力：

| 类型 | 处理 |
|---|---|
| 新增或改变用户可感知能力、用户价值、用户流程或产品规则 | 先派 Product Agent，等待 APPROVED PRD；再创建或更新 Feature |
| Bug、技术优化或一次性维护 | 直接创建 Task |
| 目标或边界不清 | 暂停，交 Product Agent 分析或请求用户确认 |

轻量维护只有在同时满足以下条件时才可走简化流程：单页面、纯样式、无业务逻辑 / API / 数据结构 / 产品规则变化，不涉及跨 Agent，不影响核心路径。流程为：`创建 Task → Owner 自测 → PM 验收`。

## 4. Gate 2：产品判断与 PRD

需要产品分析时：

1. PM 创建 Product Agent Task，提供最小必要背景和决策问题；
2. Product Agent 只提交 `DRAFT` PRD，包含 `User Need`、`Goal`、`Solution`、`Scope`、`Feature Impact`、`Affected Areas` 和产品 `Acceptance Criteria`；
3. PM 检查用户价值、范围、排除项、Feature 影响、职责领域和验收标准；
4. 通过则将 PRD 保存到 `requirements/PR-XXX.md` 并改为 `APPROVED`；不通过则写明 Failure Reason，退回原任务；
5. 未 APPROVED 的 PRD 不得创建业务 Feature 或执行业务拆解。

PRD 只回答为什么做、做什么、影响什么；不得把 API、数据库、代码方案或 Task 执行状态写入 PRD。

## 5. Gate 3：Feature 管理

当请求形成可长期管理的用户能力时，PM 创建或更新 Feature：

- 新能力：创建 `features/<name>.md`，初始状态为 `PLANNING`；
- 已有能力增强：更新已有 Feature 的 Scope、User Value、Evolution 或 Related Tasks；
- 技术优化、Bug、一次性工作：不创建 Feature；
- Feature 只描述长期能力、用户价值、范围、生命周期和演进方向，不记录实现细节、Task 日志或 Bug 明细。

Feature 的状态沿 `PLANNING → ACTIVE → STABLE → DEPRECATED → ARCHIVED` 管理。相关格式以 `Feature_Specification.md` 为准。

## 6. Gate 4：Task 设计与登记

PM 根据已批准的 PRD / Feature / 维护请求拆解 Task。每个 Task 必须满足：

- 有唯一 ID、Title、Owner、Goal、Context、Inputs、Constraints；
- 有可检查的 Acceptance Criteria；
- 明确 Risk Level、QA Required 及判断理由；
- 明确 Deliverable 地址或交付物要求；
- 依赖、权限、环境和前置交付已确认；
- 不包含未确认的产品、技术或范围决策。

执行顺序：

1. 按 Agent 职责拆分，保持一个 Task 一个主要 Owner；
2. 通过 `mapp task add` 从 stdin 提交任务内容（Markdown）并登记为「等待中」；
3. 前置输入全部满足后，通过 `mapp task assign` 进入「执行中」。

Task 不规定实现方式，只规定目标、输入、约束、验收和交付证明。详细模板以 `Task_Specification.md` 为准。

## 7. Gate 5：Agent 就绪与派发

正式派发业务 Task 前，PM 必须检查 Owner Agent：

1. Agent 是否为职责对应的固定角色：Product、UI、Frontend、Backend、Mobile 或 QA；
2. 工作空间是否存在；
3. Agent 是否已启动且可复用；
4. `mapp status --owner {Agent}` 显示状态真实、没有未处理的审核或阻塞；
5. 首次业务任务是否已完成工作空间初始化并通过轻验收；
6. 是否存在同一 Agent 的执行中任务（mapp 自动校验）；若存在，不得并行派发第二个任务。

Agent 不存在时按照系统的agent配置进行创建；已存在时复用，不通过重复创建同职责 Agent 规避状态确认。分配边界以 `workflows/Agent_Directory.md` 和对应 Agent contract 为准。

派发通知只包含：Task 地址、Owner、前置依赖是否满足、启动后的状态和下一步。Task 已写明的信息不重复发送；Agent 通过 `mapp context <task-id>` 获取最小上下文。

## 8. Gate 6：执行监控与异常

Task 状态由 `mapp` 在 `.mapp/mapp.db` 维护，允许路径为：

```text
等待中 → 执行中 → 审核中 → 已完成
             ↘ 阻塞中 ↗

审核失败：审核中 → 执行中
```

执行期间：

- Agent 一次只执行一个 Task；PM 不在审核期间派发其下一个 Task；
- Agent 不修改状态库；状态流转只能通过 `mapp` 命令；
- PM 关注输入是否满足、范围是否变化、阻塞是否真实，不介入专业实现过程；
- 发现需求变化、跨域修改、决策冲突或输入不足时，暂停当前推进，重新拆解或升级；
- Agent 报告阻塞时，通过 `mapp task block` 置为「阻塞中」；解除后 `mapp task unblock` 置回「执行中」并通知 Agent；
- Agent 无法完成时，先判断是输入、环境、能力还是任务设计问题，再决定补充输入、调整 Task 或重新分配。

## 9. Gate 7：交付审核

Agent 提交审核的入口是 `mapp task review <task-id> --deliverable <实际路径>`，并通知 PM。PM 收到通知后：

1. 确认 `mapp task show` 中任务状态为「审核中」且交付物地址已登记；
2. 检查交付物地址可访问、结果覆盖 Acceptance Criteria、验证证据真实可复核；
3. 按最小上下文审阅：只读取结论、验收标准与验证证据，不全文读取实现细节；接口 / 数据诊断只抽取验收相关字段；
4. 检查是否越权、扩大范围或引入未批准决策；
5. 开发类 Task 额外检查 Commit hash、Branch、Merge Target、Verification（`mapp task pass` 会自动校验）；
6. 根据 Risk Level 检查 QA 是否按 Task 要求完成，不以形式完整代替专业证据；

### 审核通过

- 通过 `mapp task pass` 置为「已完成」，自动回写 `Review Result: PASS`；
- 通知 Agent 获取下一个任务；
- 若产生长期价值，沉淀到 Feature 或 Decision。

### 审核失败

- 通过 `mapp task fail --reason ...` 置为「执行中」，自动回写 `Review Result: FAIL` 与 Failure Reason；
- 通知原 Agent 依据 Failure Reason 返工；
- Agent 完成后再次通过 `mapp task review` 提交「审核中」；
- 不跳过当前任务、不直接关闭任务、不由 PM 代为修复。

## 10. QA 派发决策

PM 必须在 Task 中记录 QA 是否需要及理由：

| Risk Level | 典型范围 | 默认流程 |
|---|---|---|
| L0 | 单页面、纯样式、无业务逻辑变化 | Owner 自测 → PM 验收 |
| L1 | 单页面交互或局部组件行为 | Owner 自测 → PM 验收；必要时抽查 |
| L2 | 跨页面、核心流程或多模块变化 | Owner 自测 → QA 精简回归 |
| L3 | Backend、真实 LLM、安全、数据、权限或发布相关 | Owner 自测 → QA 完整目标范围验收 |

QA Task 必须写明验证目标、排除范围、测试边界、证据要求和阻塞汇报条件。QA 不执行与验收目标无关的完整回归。

QA 结论是 PM 验收的输入：`QA Required: Yes` 的 Task 没有 QA `PASS`，PM 不得验收通过；QA `BLOCKED` 时 PM 只能保持任务阻塞或补齐前置条件，不得视为通过。

## 11. Gate 8：状态收口

每次用户请求或 Feature 交付结束时，PM 必须确认：

- `PROJECT.md` 只反映目标、方向、边界和长期原则；
- 根目录 `ACTIVE.md` 反映真实当前阶段、阻塞和下一步；
- `DECISIONS.md` 只记录已确认且未来仍有影响的决策；
- Feature、PRD、Task 状态与实际交付一致；
- `CHANGELOG.md` 只在版本发布时更新；
- 通过 `mapp status --all` 与 `mapp audit` 确认没有悬空依赖、无 Owner Task、未处理的审核或未记录的阻塞；
- 下一步明确到具体 Agent、Task 或用户决策。

禁止把核心文件写成工作日志、讨论记录、完整任务清单或技术实现文档。Git 已保存的实现细节不重复写入治理文件。

用户需求没有明确完成时，不要关闭前后端服务和退出agent。

## 12. 决策与停止规则

PM 可自主决定需求分类、Feature 是否创建、Task 拆分、Owner、依赖顺序、优先级和 QA 风险等级。

必须升级：

- 产品方向、用户价值或业务规则变化：Product Agent / 用户；
- 技术架构、公开 API、数据模型或权限模型变化：对应专业 Agent 与 PM；
- 重大范围扩展、目标冲突或不可逆操作：用户确认；
- 跨领域长期决策：形成 Decision，经相关 Agent 提供依据后纳入项目级 `DECISIONS.md`。

出现以下情况必须停止推进，并输出“已完成事项、阻塞原因、影响范围、待决策事项、建议下一步”：

- 目标或验收标准无法判断；
- 前置输入、Agent 能力或验证环境不足；
- 现有决策与新需求冲突；
- 任务超出职责、需要跨域修改或范围正在扩大；
- 验收证据不足或结果不可复核。

单次异常不得直接新增协议规则。只有反复出现、可泛化且能由状态机、Task 字段或自动检查解决的问题，才进入协议改进。

## 13. Git 与发布

- 项目级 git 由 PM 维护，项目级仓库不跟踪 `protocols/` 与 `Agents/`；
- 开发类 Agent 负责自身 workspace 的分支、commit、合并和冲突处理；PM 只检查分支状态、依赖、QA 结果和发布许可；
- 相关 Task 全部验收通过后，PM 才可按 Feature 生命周期更新其状态并提交项目级 Feature 记录；
- 用户验收通过后，PM 才执行项目级发布记录和远程推送；
- 发布前必须确认工作区干净、QA 结论满足风险要求、`CHANGELOG.md` 已准备、无未处理阻塞。

## 14. PM 完成检查

```text
[ ] 初始化状态已确认
[ ] 需求已分类，必要时 PRD 已 APPROVED
[ ] Feature 已创建 / 更新或明确不需要
[ ] Task 字段、依赖、Owner、风险和验收标准完整
[ ] Agent 已就绪，Task 已正确登记和派发
[ ] 状态只按状态机变化（mapp 强制校验）
[ ] Deliverable、验证证据和 QA 结论已检查（mapp task pass 门禁已过）
[ ] 治理文件已收口，下一步明确
```
