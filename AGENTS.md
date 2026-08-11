# MAPP 项目文档库

本仓库是一套 AI 多 Agent 协作协议（MAPP），不是软件产品。注意：本文件不加入git。

## 协议入口

协议文档统一存放于 `protocols/`，唯一入口是 `protocols/README.md`：先读它，再按其中「阅读顺序」按角色读取对应文档。协议按两层组织（职责与规范 `protocols/contracts/`、协作流程 `protocols/workflows/`），详细结构、阅读顺序与按需读取见该入口文档。

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

1. 唯一入口：`protocols/README.md`，先读它。
2. 再按其中「阅读顺序」继续。
3. 只读自己角色的链路，其他角色文档按需才读。
4. 按顺序阅读，不要跳读，不要通读全部文档。
5. 标注「按需」的文档需要时才读；标注「不存在时跳过」的文件不存在则直接跳过；项目级核心文件（`PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md`）不存在时由 PM 创建，见 `protocols/workflows/PM_Workflow.md`「项目启动协议」。

## PM派发任务规则

正式派发业务任务前，应先启动并初始化对应 Agent，再进行任务派发：
- 派 product agent 执行产品经理的任务。
- 派 ui agent 执行UI的任务。
- 派 qa agent 执行QA的任务。
- 派 backend agent 执行后端的任务。
- 派 frontend agent 执行前端的任务。
- 派 mobile agent 执行移动端的任务。
