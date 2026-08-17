# MAPP 项目文档库

本仓库是一套 AI 多 Agent 协作协议（MAPP），不是软件产品，所有Agent都要严格遵守协议规定。注意：本文件不加入git。

## 协议入口

协议文档统一存放于 `protocols/`，唯一入口是 `protocols/README.md`。

## 目录与命名规范

| 目录 / 文件 | 说明 | 维护者 |
|---|---|---|
| `PROJECT.md` / `ACTIVE.md` / `DECISIONS.md` / `CHANGELOG.md` | 项目级核心文件（全大写，协议身份标识） | PM |
| `.mapp/mapp.db` | 状态库：Task / Feature / PRD / Decision 内容与状态统一存储 | PM |
| `mapp/` | 工作流 CLI（Python 标准库）：状态机、门禁、审计、最小上下文注入 | PM |
| `Agents/{Agent}/deliverables/` | 任务交付物，命名 `TASK-{Agent}-{序号}-{英文描述}.md` | 执行 Agent |
| `Agents/{Agent}/` | Agent工作空间，由各Agent独立维护 | 执行 Agent |
| `protocols/` | 协议文档（只读引用，项目级 git 不跟踪） | — |

命名约定：

- Task / Feature / PRD / Decision 已全部迁入 `.mapp/mapp.db`，存量目录已删除；新对象一律通过 `mapp` 命令创建。
- 对象内容与状态通过 `mapp` 命令读写数据库，不手工编辑 `.mapp/mapp.db`。
- 任务 ID 格式：`TASK-{Agent}-{序号}`，如 `TASK-FE-001`。
- 交付物文件名使用英文 kebab-case，如 `TASK-BE-001-api-spec.md`；文档内容保持中文。

## 阅读规则

1. 唯一入口：`protocols/README.md`，先读它。
2. 再按其中「阅读顺序」继续。
3. 只读自己角色的链路，其他角色文档按需才读。
4. 按顺序阅读，不要跳读，不要通读全部文档。
5. 标注「按需」的文档需要时才读；标注「不存在时跳过」的文件不存在则直接跳过。
