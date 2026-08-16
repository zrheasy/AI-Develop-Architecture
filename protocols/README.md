# MAPP 项目文档库

本仓库是一套 AI 多 Agent 协作协议（MAPP），本文件是唯一入口；

---

# 1. 协议结构

| 层 | 目录 | 回答 | 内容 |
|---|---|---|---|
| 职责与规范 | `protocols/contracts/` | 每个角色是谁、负责什么、如何规范 | PM 与各 Agent 身份职责、共享契约 |
| 对象规格 | `protocols/specs/` | Feature / Task / PRD 及文档如何规范 | 对象字段、格式与文档标准 |
| 协作流程 | `protocols/workflows/` | 项目如何运转 | PM 流程、Agent 通用流程、Agent 指挥目录 |
| 机械执行 | `mapp/` | 状态机、门禁、审计与最小上下文注入 | 命令见 `mapp/README.md` |

---

# 2. 核心对象

```text
User Request → Product Requirement → Feature → Task → Deliverable
```

| 对象 | 定义 | 负责人 | 位置 | 权威来源 |
|---|---|---|---|---|
| Project | 整个软件项目 | PM Agent | PROJECT.md | 文件 |
| Product Requirement | 产品决策摘要 | Product Agent | requirements/ | 文件（mapp 登记） |
| Feature | 长期产品能力 | PM Agent | features/ | 文件 |
| Task | 临时执行契约 | PM Agent | tasks/{Agent}/ | `.mapp/mapp.db`（`mapp task list` 读取） |
| Deliverable | 工作完成的证明 | 执行 Agent | Agents/{Agent}/deliverables/ | 文件 + mapp 登记 |
| Decision | 长期项目决策 | PM / 相关 Agent | decisions/ | 文件 |
| Release | 产品发布版本 | PM Agent | CHANGELOG.md | 文件 |

---

# 3. 项目与工作空间

- 协议文档统一存放于 `protocols/`：`contracts/`（职责与规范）、`specs/`（对象规格）、`workflows/`（协作流程）、`BASIC_MAPP.md`（顶层理念）。
- Agent 工作空间位于根目录 `Agents/{Agent}/`，不包含协议文件，只包含 `PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `workspace/` / `deliverables/`。
- 项目级运行时文件（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`、`tasks/`、`features/`、`requirements/`、`decisions/`）不属于协议文档，位于项目根目录，由 PM 创建与维护。

---

# 4. 阅读顺序

只读取当前角色和当前任务所需的最小上下文，不通读无关文档。任务相关上下文由 `mapp context <task-id>` 注入（Task 内容 + 引用输入），不自行扩大阅读范围。

- PM：`BASIC_MAPP.md` → `contracts/PM.md` → `contracts/Agent_Shared_Contract.md` → `workflows/PM_Workflow.md` → `PROJECT.md` → `ACTIVE.md` → 按需其他文档。
- Agent：`BASIC_MAPP.md` → `contracts/{Agent}.md` → `contracts/Agent_Shared_Contract.md` → `workflows/Agent_Workflow.md` → `Agents/{Agent}/PROJECT.md` → `Agents/{Agent}/ACTIVE.md` → 按需其他文档。

---

# 5. 按需文档

| 场景 | 文档 |
|---|---|
| PM 管理 Feature / Task / PRD | `specs/Feature_Specification.md`、`specs/Task_Specification.md`、`specs/Product_Requirement_Specification.md` |
| 维护核心文件 | `specs/Project_Documentation_Standards.md`、`specs/Active_Documentation_Standards.md`、`specs/Decisions_Documentation_Standards.md` |
| 做重要决策 | `DECISIONS.md`|
| PM 分配 Agent | `workflows/Agent_Directory.md` |
| 交付说明格式与验收 | `specs/Delivery_Standards.md` |
| 发布记录 | `CHANGELOG.md` |

---

# 6. 流程总览

新项目：PM 判断初始化状态 → 建立项目骨架和四个核心文件 → `mapp init` 初始化状态库 → 初始化 Product Agent 并产出 `DRAFT` PRD → PM 审核为 `APPROVED` → 明确产品形态与项目边界 → 按需初始化其他 Agent → 进入业务流程。

已有项目：User Request → PM 初始化检查与需求分类 → 必要时取得 `APPROVED` PRD → 创建或更新 Feature → `mapp task add` 创建 Task 并登记 → `mapp task assign` 派发 → Agent 经 `mapp context` 获取最小上下文并执行 → 验证并提交 Deliverable（`mapp task review`）→ PM 验收（`mapp task pass / fail`）→ 状态收口（`mapp status / audit`）。

状态、权限和交付证据以 `specs/Task_Specification.md`、`workflows/PM_Workflow.md`、`workflows/Agent_Workflow.md` 和 `mapp/README.md` 为准；本 README 只做导航，不重复定义规则。

详细入口：

- PM：`workflows/PM_Workflow.md`
- 非 PM Agent：`workflows/Agent_Workflow.md`
- 角色职责：`contracts/{Agent}.md`
- 对象格式：`specs/`
