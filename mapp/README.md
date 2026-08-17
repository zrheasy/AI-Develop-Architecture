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
| `task add [--priority P]` | 从 stdin 登记任务为「等待中」 |
| `task import <dir>` | 从目录批量导入存量任务（幂等，重复跳过） |
| `task assign <id>` | 等待中→执行中（校验前置字段与并行不变量） |
| `task review <id> --deliverable <path>` | 执行中→审核中（Agent 提交入口） |
| `task block <id> --reason ...` | 执行中→阻塞中 |
| `task unblock <id>` | 阻塞中→执行中 |
| `task fail <id> --reason ...` | 审核中→执行中（记录 FAIL 与 Failure Reason） |
| `task pass <id>` | 审核中→已完成（校验 QA 与 Commit 门禁） |
| `task commit <id> --hash ... --branch ... --target ... [--verification ...]` | 记录开发类 Commit 信息 |
| `task show <id>` / `task list [--owner O] [--status S]` | 查询任务 |
| `qa <id> --result PASS\|FAIL\|BLOCKED [--report path]` | 记录 QA 结论；BLOCKED 自动置任务阻塞 |
| `status [--owner O] [--task id]` | 查看 Agent 与任务状态（`--task` 单查输出稳定，利于缓存） |
| `audit [--task id] [--limit N] [--with-time]` | 状态流转审计（默认省略时间戳以保持前缀稳定） |
| `context <id> [--fields ...] [--refs full\|summary\|none]` | 最小上下文注入：字段可选、引用分级 |
| `ref show <ref> [--summary]` | 懒加载单个引用内容（Feature / PRD / Decision / 文件） |
| `feature add/status/list/show/import` | Feature 入库管理（生命周期状态机强制） |
| `prd add/status/list/show/import` | PRD 入库管理（DRAFT→APPROVED→ARCHIVED） |
| `decision add/list/show/remove/import` | Decision 入库管理（上限 50 条，`remove` 释放空间） |

## 强制不变量

- 状态只允许按状态机流转，且只能通过 mapp 命令。
- 同一 Agent 同时只能有一个执行中 / 审核中 / 阻塞中任务。
- 缺少 Goal / Context / Acceptance Criteria / Deliverable 不得进入执行中。
- QA Required=Yes 无 QA PASS 不得验收通过；QA BLOCKED 置任务阻塞。
- 开发类（Frontend / Backend / Mobile）缺 Commit hash / Branch / Merge Target / Verification 不得验收通过。
- 任务内容与状态统一存于数据库；`mapp task import` 可一次性导入存量任务文件（幂等，重复跳过）。

## 协议衔接

- 状态唯一权威：`.mapp/mapp.db`；任务列表通过 `mapp task list` 读取，不再生成 INDEX.md。
- PM 通过 `mapp status --all` / `mapp audit` 监控，不逐个读取 Agent 的 ACTIVE.md。
- Agent 通过 `mapp context <task-id>` 获取任务本体（默认引用摘要，`mapp ref show` 懒加载细节），不自行阅读其他文档。
- Feature / PRD / Decision 统一存于数据库；存量文件用对应 `import` 一次性导入后不再维护。
- 规则与门禁定义见 `protocols/specs/Task_Specification.md`、`protocols/workflows/PM_Workflow.md`、`protocols/workflows/Agent_Workflow.md`。
