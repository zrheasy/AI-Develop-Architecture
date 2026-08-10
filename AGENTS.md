# MAPP 项目文档库

本仓库是一套 AI 多 Agent 协作协议（MAPP），不是软件产品。注意：本文件不加入git。

## 目录结构

- 协议文档统一存放于 `protocols/`，项目根目录只保留本 README 作为文档索引。
- 协议按角色分为项目级协议（`protocols/`）与各 Agent 协议（`protocols/Agents/{Agent}/`）。
- Agent 工作空间位于根目录 `Agents/{Agent}/`，工作空间内不包含协议文件，只包含 `PROJECT.md` / `DECISIONS.md` / `ACTIVE.md` / `workspace/` / `deliverables/`。
- 项目级运行时文件（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`、`tasks/`、`features/`、`requirements/`、`decisions/`）不属于协议文档，位于项目根目录，由 PM 创建与维护。

## 目录与命名规范

| 目录 / 文件 | 说明 | 维护者 |
|---|---|---|
| `PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md` | 项目级核心文件（全大写，协议身份标识） | PM |
| `features/` | Feature 能力定义（小写，单数文件名，如 `global-events-feed.md`） | PM |
| `tasks/{Agent}/` | 任务索引与任务文件（`INDEX.md` + `TASK-XXX.md`） | PM |
| `requirements/` | Product Requirement（`PR-XXX.md`） | PM（落库） |
| `decisions/` | 长期决策（小写文件名，如 `event-content-language.md`） | PM / 相关 Agent |
| `Agents/{Agent}/deliverables/` | 任务交付物，命名 `TASK-{Agent}-{序号}-{英文描述}.md` | 执行 Agent |
| `protocols/` | 协议文档（只读引用，项目级 git 不跟踪） | — |

命名约定：

- 目录统一全小写：`tasks/`、`features/`、`requirements/`、`decisions/`。
- 任务 ID 格式：`TASK-{Agent}-{序号}`，如 `TASK-FE-001`。
- 交付物文件名使用英文 kebab-case，如 `TASK-BE-001-api-spec.md`；文档内容保持中文。
- Agent 工作空间（`Agents/{Agent}/`）由各 Agent 独立维护版本，不纳入项目级 git。

## 阅读规则

1. 唯一入口：`protocols/AI_Development_Architecture.md`，先读它。
2. 再按其中第 5 节「获取知识路径」继续。
3. 只读自己角色的链路，其他角色文档按需才读。
4. 按顺序阅读，不要跳读，不要通读全部文档。
5. 标注「按需」的文档需要时才读；标注「不存在时跳过」的文件不存在则直接跳过；项目级核心文件（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`）不存在时由 PM 创建，见 `protocols/PM_Operating_Protocol.md`「项目启动协议」。

## PM 阅读顺序

1. `protocols/AI_Development_Architecture.md`
2. `protocols/PM_Contract.md`
3. `protocols/ROOT_MAPP.md`
4. `protocols/PM_Operating_Protocol.md`
5. `PROJECT.md`（不存在时由 PM 创建）
6. `ACTIVE.md`（不存在时由 PM 创建）
7. `DECISIONS.md`（按需，不存在时由 PM 创建骨架）

## Agent 阅读顺序

六个 Agent（Product / UI / Frontend / Backend / Mobile / QA）顺序相同，仅替换 `{Agent}`。

1. `protocols/AI_Development_Architecture.md`
2. `protocols/Agents/{Agent}/Contract.md`
3. `protocols/Agent_Shared_Contract.md`
4. `protocols/ROOT_MAPP.md`
5. `protocols/Agent_Shared_MAPP.md`
6. `protocols/Agents/{Agent}/MAPP.md`
7. `protocols/Agents/{Agent}/Capability.md`
8. `PROJECT.md` 或 `Agents/{Agent}/PROJECT.md`（不存在时跳过）
9. `ACTIVE.md` 或 `Agents/{Agent}/ACTIVE.md`（不存在时跳过）
10. `tasks/{Agent}/INDEX.md`（不存在时跳过）
11. `DECISIONS.md` 或 `Agents/{Agent}/DECISIONS.md`（按需，不存在时跳过）

## 按需读取

| 场景 | 文档 |
|---|---|
| PM 分配 Agent | `protocols/Agent_Directory.md` |
| PM 管理 Feature / Task / Product Requirement | `protocols/Feature_Specification.md`、`protocols/Task_Specification.md`、`protocols/Product_Requirement_Specification.md` |
| 维护三个核心文件 | `protocols/Project_Documentation_Standards.md`、`protocols/Active_Documentation_Standards.md`、`protocols/Decisions_Documentation_Standards.md` |
| 发布记录 | `CHANGELOG.md`（新项目由 PM 创建初始记录） |


## PM派发任务规则

正式派发业务任务前，应先启动并初始化对应 Agent，再进行任务派发：
- 派 product agent 执行产品经理的任务。
- 派 ui agent 执行UI的任务。
- 派 qa agent 执行QA的任务。
- 派 backend agent 执行后端的任务。
- 派 frontend agent 执行前端的任务。
- 派 mobile agent 执行移动端的任务。