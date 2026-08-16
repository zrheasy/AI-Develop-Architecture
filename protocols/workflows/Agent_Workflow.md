# Agent Workflow

**版本：** 2.0

**定位：** 所有非 PM Agent 的统一任务执行流程。Product、UI、Frontend、Backend、Mobile、QA 只在各自 contract 中补充领域门禁，不重复定义本流程。

继承：`BASIC_MAPP.md`。角色职责、领域输入、专业验证和交付差异以 `contracts/{Agent}.md` 为准；Task 字段和状态以 `specs/Task_Specification.md` 为准。

## 1. 工作空间边界

每个 Agent 只在自身工作空间工作：

```text
Agents/{Agent}/
├── PROJECT.md       # 本领域项目上下文
├── ACTIVE.md        # 当前唯一运行状态
├── DECISIONS.md     # 本领域长期决策入口
├── workspace/       # 长期工程资产；开发类 Agent 的源代码在此
└── deliverables/    # 提交 PM 的结果证明，不复制开发源代码
```

协议文件位于 `protocols/`，只读引用，不复制、不修改。Agent 不得修改：

- PM 治理域：`PROJECT.md`、根目录 `ACTIVE.md`、`DECISIONS.md`、`CHANGELOG.md`、`requirements/`、`features/`、`tasks/`、`decisions/`；
- 其他 Agent 的工作空间；
- 未被当前 Task 授权的代码、配置或长期决策。

跨域需求、输入变化或需要其他 Agent 支持时，暂停并反馈 PM，由 PM 调整或重新创建 Task。

## 2. 初始化工作空间

首次收到「初始化工作空间」Task 时，按以下顺序执行：

1. 读取 BASIC、共享契约、本 Agent contract 和本流程；
2. 创建领域版 `PROJECT.md`、`ACTIVE.md`、`DECISIONS.md` 骨架；
3. 创建 `workspace/` 与 `deliverables/`；
4. 开发类 Agent 在 `workspace/` 初始化独立 git、`.gitignore`、`main` / `dev` 基线和工程骨架；Product / UI / QA 工作空间只保留 `main`；
5. 按领域 contract 完成初始化所需的产品、设计、质量或工程准备；
6. 检查目录、文件、权限和初始状态；
7. 通过 `mapp task review` 提交初始化交付物地址（轻验收任务），通知 PM 轻验收。

初始化未通过 PM 验收前：

- 不接受正式业务 Task；
- 不读取或执行下一个 Task；
- 不自行宣告工作空间可用。

## 3. 任务启动门禁

收到正式 Task 后，按以下最小顺序恢复上下文：

1. 读取 `BASIC_MAPP.md`、`contracts/Agent_Shared_Contract.md`、`workflows/Agent_Workflow.md`；
2. 读取自身 `contracts/{Agent}.md` 与领域版 `PROJECT.md`，确认职责与项目边界；
3. 通过 `mapp task list --owner {Agent} --status 执行中` 确认自己的执行中任务；返工只处理 PM 已退回的当前任务；
4. 通过 `mapp context <task-id>` 获取最小上下文（Task 全文 + 引用输入），不阅读引用之外的文件；
5. 仅在当前 Task 明确涉及且 mapp context 未包含时，才按需读取 `DECISIONS.md`、PRD、Feature 或接口契约。

以下情况不得开始执行：

- mapp 中任务状态不是「执行中」（等待中 / 阻塞中 / 审核中 / 已完成）；
- 不是当前 Agent 的 Owner；
- 已有另一个 Task 处于执行中、审核中或阻塞中；
- Task 缺少目标、输入、约束、验收标准或交付要求；
- 前置依赖未满足，或阻塞尚未解除；
- 当前 Task 与职责、长期决策或工作空间边界冲突。

发现问题时，立即向 PM 输出缺失项、影响和需要的处理，不自行猜测或顺手修正治理文件。

## 4. 单任务执行循环

每次只执行一个 Task，按以下循环推进：

```text
确认目标
  → 获取最小上下文
  → 形成任务内方案
  → 执行最小修改
  → 验证验收标准
  → 生成 Deliverable
  → 提交审核
```

执行约束：

- 先确认 Goal、Acceptance Criteria 和 Out of Scope，再开始修改；
- 优先复用已有代码、设计、接口、测试和工程模式；
- 只修改完成当前 Task 所必需的内容，不主动重构、优化或处理无关问题；
- 领域 contract 允许的内部实现由 Agent 自主决定；跨域或长期影响决策必须升级；
- 不把临时方案、未确认候选或未验证结果当作完成输出。

## 5. 上下文恢复点

Agent 不依赖长期记忆维持协议合规。出现以下任一情况时，必须重新运行 `mapp context <task-id>` 和 `mapp task list --owner {Agent}`，必要时重新读取相关 contract：

- 开始执行前；
- 上下文压缩、会话恢复或长时间中断后；
- 完成一段较长实现或验证后；
- 任务范围、依赖、阻塞或下一步发生变化时；
- 提交审核前。

恢复时只确认五项：`Task`、`Goal`、`当前状态`、`下一步`、`禁止事项`。如果当前工作与其中任一项不一致，先暂停并反馈 PM。

## 6. 验证门禁

Agent 必须按 Task 的 Risk Level、Acceptance Criteria 和自身 contract 完成最小有效验证：

1. 先完成快速检查，确认结果不是明显错误；
2. 再执行验收标准要求的高价值验证；
3. 优先复用已有自动化测试和有效证据，不重复无价值的测试；
4. 只验证当前 Task 范围，不扩展为无关的完整回归、性能测试或安全审计；
5. 记录实际命令、环境、版本、输入 / 设备和结果。

验证必须证明：

- 结果覆盖 Acceptance Criteria；
- 领域约束和项目边界未被破坏；
- Deliverable 可访问且内容足以让下一 Agent 继续工作；
- 已知限制、残余风险和未完成项均已明确。

当验证预计较长时，先报告快速检查结果和当前阻塞，再继续高价值验证；不得在没有阶段性反馈的情况下长时间等待。

环境阻塞时，立即报告：已完成验证、未完成范围、阻塞原因、对结论的影响和需要 PM 决定的事项。环境问题不能被包装成 PASS。

## 7. 交付与提交审核

提交审核前必须完成：

1. 按 `specs/Delivery_Standards.md` 生成交付说明，记录结果、验证信息、已知限制和后续事项；
2. 开发类 Task 记录 Commit hash、Branch、Merge Target、Verification；
3. 非开发类 Task 按领域 contract 记录对应交付证明；
4. 确认没有修改 `INDEX.md`、Task 文件或其他 Agent 工作空间；
5. 通过 `mapp task review <task-id> --deliverable <实际路径>` 提交审核（自动翻转状态并登记交付物）；
6. 按共享契约通知 PM：

```text
Status: REVIEW
Deliverable: 实际文件地址
Blockers: 无 / 阻塞说明
```

提交后必须等待 PM 审核，不读取、不执行下一个 Task，不把“已提交”称为“已完成”。任务状态以 `.mapp/mapp.db` 为准，不再手工双写 `ACTIVE.md` 的 Task Status。

## 8. 审核失败与返工

PM 退回时：

1. 读取 Task 中的 `Failure Reason`；
2. 确认返工范围和新的验收条件；
3. 等待 PM 通过 `mapp task fail` 将状态改为「执行中」（自动回写 `Review Result: FAIL` 与 Failure Reason）；
4. 只修复 Failure Reason 指定的问题；
5. 重新执行必要验证并更新 Deliverable；
6. 再次通过 `mapp task review` 提交 PM。

PM 维护的 Task 状态由 PM 负责，Agent 不修改、不跳过、不关闭失败任务。返工中发现新的需求或跨域问题时，暂停并反馈 PM，不顺手扩大范围。

## 9. 阻塞处理

无法继续时，Agent 将阻塞原因、影响、已完成项、未完成项和所需处理通知 PM；PM 通过 `mapp task block` 置为「阻塞中」，阻塞解除后通过 `mapp task unblock` 置回「执行中」并通知 Agent。阻塞期间不得继续实现、提交审核或读取下一个 Task。

## 10. 状态同步规则

任务状态唯一权威是 `.mapp/mapp.db`，由 `mapp` 命令维护；`INDEX.md` 由 `mapp index` 生成，Agent 不手工修改。

Agent 只维护自身 `ACTIVE.md`（领域目标、下一步与阻塞说明）和在自身工作空间内产生的长期领域资产：

- `ACTIVE.md` 不再维护 Task Status 字段（以 mapp 为准），避免双写漂移；
- 状态变化通过 mapp 命令完成（review / block / unblock），不在 `ACTIVE.md` 中重复记录状态；
- 不记录工作日志、完整 Todo、讨论过程、已完成历史或技术细节；
- 产生未来仍影响领域工作的稳定决策时，记录到自身 `DECISIONS.md`，并将跨领域决策升级 PM；
- 长期设计、产品、测试或工程资产沉淀到 `workspace/`，不要把交付物当作长期知识库。

## 11. 协作与异常

默认不直接指挥其他 Agent，跨 Agent 协作通过 PM 完成。出现以下情况必须暂停：

- 需求、验收标准或输入不明确；
- Task 超出职责、范围或工作空间权限；
- 需要修改其他 Agent、项目治理域或源代码之外的文件；
- 与已有决策、接口、设计或产品规则冲突；
- 发现安全、数据完整性、核心流程或严重质量风险；
- 验证环境不可用，无法形成可信结论。

异常反馈必须包含：已确认事实、已完成工作、阻塞原因、影响范围、未完成项和需要 PM / 用户决定的事项。禁止用临时规则、隐式假设或直接改别人的文件绕过阻塞。

## 12. 开发类 Agent 的分支与提交

适用：Frontend、Backend、Mobile。

### 分支基线

- `main`：已上线或可发布代码；
- `dev`：当前开发集成分支；
- 禁止直接在 `main` 或 `dev` 上开发功能。

### Task 分支

```text
dev → feature/<feature-slug> → dev → main
```

- 新 Feature 从最新 `dev` 创建 `feature/<feature-slug>`；
- Bug / 维护使用 `fix/<task-id>`；紧急问题使用 `hotfix/<issue-id>`，完成后同时合并到 `main` 与 `dev`；
- 每项 Task 至少一个 commit，commit 只包含当前 Task，使用 Conventional Commit；
- Feature 合并 `dev` 前由开发 Agent 完成自检并同步最新 `dev`；
- QA 验收通过、工作区干净、发布记录准备完成后，才允许 `dev` 合并到 `main`；
- 分支创建、commit、合并和冲突处理由开发 Agent 负责，PM 只检查结果和发布许可。

### 既有 workspace

若开发 workspace 缺少 `main` / `dev`：

1. 保留现有代码和历史；
2. 确认 `main` 基线；
3. 从 `main` 创建 `dev`；
4. 完成迁移并验证后，才开始下一项开发 Task。

## 13. 非开发类 Agent 的分支

适用：Product、UI、QA。

- 工作空间 git 只保留 `main`；
- 不创建 `dev`、Feature 分支或临时开发分支；
- 领域资产和交付物在自身 workspace 内维护；
- 交付内容以对应 Agent contract 为准。

## 14. 完成检查

每次提交审核前确认：

```text
[ ] 身份、职责和执行域正确
[ ] mapp 中当前 Task 状态为「执行中」且是唯一任务
[ ] 已通过 mapp context 理解 Goal、Inputs、Constraints、Acceptance Criteria
[ ] 只读取和修改了最小必要范围
[ ] 未越权、未扩大范围、未跳过依赖
[ ] 结果与验证证据真实可复核
[ ] Deliverable 已生成且可被后续工作继续使用
[ ] 已通过 mapp task review 提交并附交付物地址
[ ] 未修改 INDEX.md 或 Task 文件
[ ] 已通知 PM，并等待审核
```
