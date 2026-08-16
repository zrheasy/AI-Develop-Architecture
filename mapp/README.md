# mapp — MAPP 工作流命令行

`mapp` 用 Python 标准库（argparse + sqlite3，零第三方依赖）实现。它将协议中的状态机、门禁与最小上下文注入机械化，状态数据存入 SQLite（Python 自带稳定版本，无需下载）。

## 运行

```bash
python -m mapp --project <项目根目录> <命令>
```

不传 `--project` 时默认使用当前目录。`--project` 必须放在子命令之前。

## 初始化

```bash
python -m mapp --project . init
```

创建 `.mapp/mapp.db` 并写入六个 Agent 记录。

## 命令

| 命令 | 作用 |
|---|---|
| `init` | 初始化数据库 |
| `task add <file> [--priority P]` | 登记任务为「等待中」 |
| `task assign <id>` | 等待中→执行中（校验前置字段与并行不变量） |
| `task review <id> --deliverable <path>` | 执行中→审核中（Agent 提交入口） |
| `task block <id> --reason ...` | 执行中→阻塞中 |
| `task unblock <id>` | 阻塞中→执行中 |
| `task fail <id> --reason ...` | 审核中→执行中（记录 FAIL，回写任务文件） |
| `task pass <id>` | 审核中→已完成（校验 QA 与 Commit 门禁，回写任务文件） |
| `task commit <id> --hash ... --branch ... --target ... [--verification ...]` | 记录开发类 Commit 信息 |
| `task show <id>` / `task list [--owner O] [--status S]` | 查询任务 |
| `qa <id> --result PASS\|FAIL\|BLOCKED [--report path]` | 记录 QA 结论；BLOCKED 自动置任务阻塞 |
| `status [--owner O]` | 查看 Agent 与任务状态（替代逐个读 ACTIVE / INDEX） |
| `audit [--task id] [--limit N]` | 状态流转审计 |
| `context <id>` | 最小上下文注入：Task 内容 + 引用输入 |

## 强制不变量

- 状态只允许按状态机流转，且只能通过 mapp 命令。
- 同一 Agent 同时只能有一个执行中 / 审核中 / 阻塞中任务。
- 缺少 Goal / Context / Acceptance Criteria / Deliverable 不得进入执行中。
- QA Required=Yes 无 QA PASS 不得验收通过；QA BLOCKED 置任务阻塞。
- 开发类（Frontend / Backend / Mobile）缺 Commit hash / Branch / Merge Target / Verification 不得验收通过。
- 任务文件位置必须与 Owner 对应（`tasks/{Owner}/TASK-*.md`），ID 必须与文件名一致。

## 协议衔接

- 状态唯一权威：`.mapp/mapp.db`；任务列表通过 `mapp task list` 读取，不再生成 INDEX.md。
- PM 通过 `mapp status --all` / `mapp audit` 监控，不逐个读取 Agent 的 ACTIVE.md。
- Agent 通过 `mapp context <task-id>` 获取最小上下文，不自行阅读其他文档。
- 规则与门禁定义见 `protocols/specs/Task_Specification.md`、`protocols/workflows/PM_Workflow.md`、`protocols/workflows/Agent_Workflow.md`。
