# Agent Workflow

**版本：** 1.1

**定位：** 所有 Agent 的通用协作流程。各 Agent 只保留领域差异（见 `contracts/agents/`）。

继承：`BASIC_MAPP.md`。

---

# 1. 工作空间结构

Agent 工作空间位于 `Agents/{Agent}/`，只包含上下文文件与工程资产，不包含协议文件：

```text
{Agent} Workspace
├── PROJECT.md      # 领域版项目上下文（派生自根目录，只保留本领域相关内容）
├── DECISIONS.md    # 领域长期决策入口
├── ACTIVE.md       # 当前工作状态（Agent 独占维护）
├── workspace/      # 长期工程资产（git 管理）
└── deliverables/   # 任务完成时提交 PM 的证明
```

协议文件统一存放于 `protocols/`，Agent 只读引用，不复制、不修改。

## deliverables/

- 工程类 Agent（Frontend / Backend / Mobile）禁止提交源代码，代码保留在 workspace/。
- 各 Agent 具体交付内容见 `contracts/agents/` 对应文档。
- 不是长期资产目录：验收后长期价值沉淀到 workspace/、Feature 或 Decision，交付物可归档或删除。

## 工作空间初始化

Agent 收到 PM「初始化工作空间」任务后自动完成：派生领域 PROJECT.md、创建 ACTIVE.md / DECISIONS.md 骨架、创建 workspace/ 与 deliverables/、workspace/ 执行 git init + .gitignore + 初始提交。

开发类 Agent（Frontend / Backend / Mobile）附加：依据自身领域规范完成架构设计与技术选型，产出架构决策写入 DECISIONS.md，创建工程骨架；跨领域影响升级 PM 确认。

完成后更新 ACTIVE.md 为「审核中」并通知 PM 轻验收。验收通过前不接受正式业务任务。

---

# 2. 工作启动协议

收到 Task 后按顺序：

1. 读取 `contracts/agents/{Agent}.md`：确认身份、职责、权限。
2. 读取本文件：确认工作流程。
3. 读取同一份 Agent 文档的领域规范：确认能力与约束。
4. 读取 PROJECT.md：理解项目目标与边界。
5. 读取 ACTIVE.md：理解当前状态与阻塞。
6. 通过 ACTIVE.md 固定指针读取 `tasks/{Agent}/INDEX.md`，只读「执行中」（按优先级取一个）或「审核中」（重新执行当前任务）。
7. 按需读取 DECISIONS.md（仅任务涉及领域长期决策时）。

---

# 3. 上下文获取

只获取完成当前 Task 所需信息。禁止：无目的浏览项目、一次读取大量无关文档、主动建立完整项目知识库。

---

# 4. Task 执行

- 明确 Goal / Input / Expected Output / Acceptance Criteria，缺少关键条件则停止并反馈。
- 最小修改：不扩大需求、不无关优化、不主动重构、不修改无关内容。
- 优先复用：已有规范、流程、交互、接口模式；避免重复建设与不必要复杂度。

---

# 5. 验证

确认：Deliverable 完整、满足项目规范与验收标准、领域一致、可被下一 Agent 继续使用。领域验证方式见各 Agent 文档。

---

# 6. Deliverable 与提交

Deliverable 包含：结果、状态、验证信息、必要说明（最小格式见 `contracts/Agent_Shared_Contract.md` 最小输出）。

完成流程：

1. 更新 ACTIVE.md：任务状态「审核中」（REVIEW），附 Deliverable 地址。
2. 通知 PM 审核。
3. 等待审核结果，不读取下一个任务。
4. 审核失败：查看 TASK 失败原因，重新执行并更新 ACTIVE.md，不跳任务。

禁止输出：未确认或未验证的方案、临时想法、无关讨论记录。

---

# 7. 状态同步

- ACTIVE.md：Agent 独占维护，更新任务状态、真实状态、下一步、阻塞、Deliverable 地址（审核中时）。
- Task 状态：由 PM 在 INDEX.md 维护，Agent 不修改索引与 TASK 文件。
- DECISIONS.md：仅产生长期有效决策时记录（决策 / 原因 / 影响）。
- 禁止把 ACTIVE.md 变成过程日志、Todo 列表或历史记录。

---

# 8. 协作与异常

- 默认不直接协调其他 Agent，所有跨 Agent 协作经 PM。
- 发现需求变化、Task 边界变化、需要其他领域支持、修改影响其他模块：暂停扩展 → 反馈 PM → 重新分配 Task。
- 信息不足：明确缺失信息，请求补充。
- 与已有决策冲突：停止修改 → 检查 DECISIONS.md → 提交决策更新请求。
- 发现领域问题：记录 → 通知 PM → 等待决策。

---

# 9. 分支与提交协议（开发类 Agent）

## 适用范围

本协议仅适用于开发类 Agent（Frontend / Backend / Mobile）。其他 Agent（Product / UI / QA）的工作空间 git 只保留 main 分支，不创建 dev / feature 等分支。

## 长期分支

- `main`：已上线或可发布代码，只允许通过 `dev` 合并进入。
- `dev`：当前开发集成分支，包含已完成但尚未上线的 Feature。
- 禁止直接在 main / dev 上开发功能。

## Feature 分支生命周期

```text
dev → feature/<feature-slug> → dev → main
```

1. 从最新 dev 创建 `feature/<feature-slug>`。
2. 在 Feature 分支执行所属 Task，每项 Task 至少一个 commit。
3. Feature 完成并通过自检后合并回 dev（合并前先同步最新 dev）。
4. QA 验收通过、工作区干净、发布记录准备完成后，将 dev 合并到 main。

分支命名：`feature/<feature-slug>`、`fix/<task-id>`、`hotfix/<issue-id>`（完成后必须同时合并到 main 与 dev）。

## Commit 与合并

- 每项 Task 前必须提交 commit，并在 Deliverable 与 ACTIVE.md 记录 commit hash、分支名、合并目标分支、测试摘要。
- Commit 只包含当前 Task 改动，使用 Conventional Commit。
- 分支创建、commit、合并与冲突处理由对应开发 Agent 负责；PM 只确认分支状态、Task 依赖、QA 结果与发布许可，不直接修改或合并代码。

## 既有 workspace 迁移

已存在 workspace 缺少 main / dev 时，开始下一项开发 Task 前由对应开发 Agent 迁移：保留现有代码与历史、确定 main 基线、从 main 创建 dev。

---

# 10. 自检清单

每次 Task 完成前确认：

- 身份：按 Agent 文档定义的角色工作。
- 最小上下文：只读取了完成任务所需信息。
- 目标理解：理解 Task 目标与验收标准。
- 最小修改：避免无必要扩大范围。
- 输出交付：产生明确 Deliverable，ACTIVE.md 更新为「审核中」并附地址。
- 串行执行：一次只执行一个任务，等待审核期间不读取下一个。
- 状态同步：只更新 ACTIVE.md，未修改 INDEX.md 与 TASK 文件。
- 可继续工作：其他 Agent 可基于我的结果继续。
