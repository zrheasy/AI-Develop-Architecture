# MAPP 项目文档库

本仓库是一套 AI 多 Agent 协作协议（MAPP），不是软件产品。协议文档统一存放于 `protocols/`，本文件是唯一入口；项目根目录只保留仓库说明（`AGENTS.md`）。

> 本文件是协议文档的入口导读，不是项目级 PROJECT.md；实际软件项目的 PROJECT.md 由 PM 在项目启动时创建于项目根目录。

---

# 1. 协议两层模型

| 层 | 目录 | 回答 | 内容 |
|---|---|---|---|
| 职责与规范 | `protocols/contracts/` | 每个角色是谁、负责什么、如何规范 | PM 与各 Agent 身份职责、共享契约、对象规格 |
| 协作流程 | `protocols/workflows/` | 项目如何运转 | PM 流程、Agent 通用流程、Agent 指挥目录 |

顶层理念：`protocols/BASIC_MAPP.md`，所有协议继承的最小工作协议，先读它。

---

# 2. 核心对象模型

```text
User Request → Product Requirement → Feature → Task → Deliverable
```

| 对象 | 定义 | 负责人 | 位置 |
|---|---|---|---|
| Project | 整个软件项目 | PM Agent | PROJECT.md |
| Product Requirement | 产品决策摘要 | Product Agent | requirements/ |
| Feature | 长期产品能力 | PM Agent | features/ |
| Task | 临时执行契约 | PM Agent | tasks/{Agent}/ |
| Deliverable | 工作完成的证明 | 执行 Agent | Agents/{Agent}/deliverables/ |
| Decision | 长期项目决策 | PM / 相关 Agent | decisions/ |
| Release | 产品发布版本 | PM Agent | CHANGELOG.md |

---

# 3. 目录结构

- 协议文档统一存放于 `protocols/`：`contracts/`（职责与规范）、`workflows/`（协作流程）、`BASIC_MAPP.md`（顶层理念）。
- Agent 工作空间位于根目录 `Agents/{Agent}/`，不包含协议文件，只包含 `PROJECT.md` / `DECISIONS.md` / `ACTIVE.md` / `workspace/` / `deliverables/`。
- 项目级运行时文件（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`、`tasks/`、`features/`、`requirements/`、`decisions/`）不属于协议文档，位于项目根目录，由 PM 创建与维护。

---

# 4. 阅读顺序

先读 `BASIC_MAPP.md`，再按角色读取对应文档；不要跳读，不要通读全部文档。

## PM

1. `BASIC_MAPP.md`
2. `contracts/agents/PM.md`
3. `contracts/Agent_Shared_Contract.md`
4. `workflows/PM_Workflow.md`
5. `PROJECT.md`（不存在时由 PM 创建）
6. `ACTIVE.md`（不存在时由 PM 创建）
7. `DECISIONS.md`（按需，不存在时由 PM 创建骨架）
8. `workflows/Agent_Directory.md`（分配 Agent 时）
9. `contracts/specs/`（管理 Feature / Task / PRD 时按需）

## Agent

六个 Agent（Product / UI / Frontend / Backend / Mobile / QA）顺序相同，仅替换 `{Agent}`：

1. `BASIC_MAPP.md`
2. `contracts/agents/{Agent}.md`
3. `contracts/Agent_Shared_Contract.md`
4. `workflows/Agent_Workflow.md`
5. `PROJECT.md` 或 `Agents/{Agent}/PROJECT.md`（不存在时跳过）
6. `ACTIVE.md` 或 `Agents/{Agent}/ACTIVE.md`（不存在时跳过）
7. `tasks/{Agent}/INDEX.md`（不存在时跳过）
8. `DECISIONS.md` 或 `Agents/{Agent}/DECISIONS.md`（按需，不存在时跳过）

---

# 5. 按需读取

| 场景 | 文档 |
|---|---|
| PM 管理 Feature / Task / PRD | `contracts/specs/Feature_Specification.md`、`Task_Specification.md`、`Product_Requirement_Specification.md` |
| 维护三个核心文件 | `contracts/specs/Project_Documentation_Standards.md`、`Active_Documentation_Standards.md`、`Decisions_Documentation_Standards.md` |
| PM 分配 Agent | `workflows/Agent_Directory.md` |
| 发布记录 | `CHANGELOG.md`（新项目由 PM 创建初始记录） |

---

# 6. 标准工作流程

新项目：PM 判断初始化状态 → 未初始化则执行项目启动协议（建骨架、四个核心文件、初始化 Product 工作空间、需求分析出 PRD、产品形态规划）→ 按需初始化其他 Agent 工作空间 → 进入业务需求流程。

已有项目：User Request → PM 判断是否需要产品分析 → Feature 管理（新能力创建 / 已有能力扩展 / 技术优化与 Bug 直接建 Task）→ 创建 Task 并登记 INDEX.md（等待中 → 执行中）→ Agent 执行 → 交付（ACTIVE.md 审核中 + Deliverable）→ PM 验收 → 状态维护。

详细流程见 `workflows/PM_Workflow.md` 与 `workflows/Agent_Workflow.md`。
