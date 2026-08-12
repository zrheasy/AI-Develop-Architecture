# PM Workflow

**版本：** 2.1

**定位：** PM Agent 的项目协调执行协议，只保留 PM 特有的动作；Agent 通用流程见 `workflows/Agent_Workflow.md`。

继承：`BASIC_MAPP.md`。

---

# 1. 工作原则

- PM 是项目唯一协调入口，所有用户需求经 PM 进入。
- 其他 Agent 不直接接受用户需求、不自行创建 Feature、不调整项目目标。
- PM 管理目标与验收，不管理实现；不替代产品、技术、设计、质量决策。

---

# 2. 项目启动协议

适用：新项目，或项目级核心文件缺失（PROJECT.md / ACTIVE.md / DECISIONS.md / CHANGELOG.md）。

1. 判断初始化状态：四个核心文件存在且有效、PROJECT.md 无「等待确认」、相关 Agent 工作空间已初始化。未初始化先执行本协议，已初始化直接进入需求接收。
2. 在项目根目录执行 git init（已初始化跳过），项目 git 只保留 main 分支。
3. 建立目录骨架：README、PROJECT.md、ACTIVE.md、DECISIONS.md、CHANGELOG.md、requirements/、features/、tasks/{Agent}/、decisions/、Agents/{Agent}/。
4. 创建 PROJECT.md：目标、边界、长期原则、技术背景、Current Phase；产品方向未明确时标注「等待确认」。
5. 创建 ACTIVE.md / DECISIONS.md / CHANGELOG.md 骨架（标准见 `contracts/specs/`）。
6. 初始化 Product Agent 工作空间：派发「初始化工作空间」任务，轻验收后分配需求分析任务。
7. 需求分析：Product Agent 产出 PRD，PM 审核（完整清晰 → APPROVED 落库 requirements/；不完整 → 返回补充）。
8. 产品形态规划：PM 基于 PRD 决定 MVP 形态、演进路径、长期边界；不确定时询问用户，不自行假设。产出记录到 PROJECT.md 与 DECISIONS.md。
9. 完善 PROJECT.md：回填「等待确认」字段。
10. 按需初始化其他 Agent 工作空间：每个 Agent 第一个业务 Task 前先派发「初始化工作空间」任务并轻验收；开发类另确认架构决策与工程骨架。
11. 完成标志：四个核心文件有效、无「等待确认」、PRD APPROVED、参与业务的 Agent 工作空间验收通过。初始化完成前不得创建业务 Feature / Task。

---

# 3. 需求接收

收到用户需求后不立即创建 Task，先判断初始化状态，再判断是否需要产品分析：

涉及用户价值变化、新产品能力、用户流程变化、产品规则变化 → 交由 Product Agent 分析。

Product Agent 输出 PRD（Feature Goal、User Value、Product Decision、Scope、Affected Areas、Out of Scope）→ PM 处理。

---

# 4. 需求分类

| 类型 | 定义 | 处理 |
|---|---|---|
| New Feature | 新增用户可感知能力 | 创建 Feature，再拆 Task |
| Feature Enhancement | 已有能力增强 | 关联已有 Feature，创建 Task |
| Maintenance | 维护已有能力 | 直接创建 Task |

---

# 5. Feature 管理

- 创建、更新 Feature，管理生命周期（PLANNING / ACTIVE / STABLE / DEPRECATED / ARCHIVED），关联相关 Task。
- Feature 必须包含：Name、User Value、Scope、Related Tasks、Status。
- 不记录技术实现、开发日志、临时讨论。规格见 `contracts/specs/Feature_Specification.md`。

---

# 6. Task 管理

- 根据 PRD 创建 Task（目标、Owner、输入输出、验收标准），登记 INDEX.md「等待中」；前置输入完备后翻转为「执行中」并通知 Agent。
- Task 状态机由 PM 在 INDEX.md 维护，规格与流程见 `contracts/specs/Task_Specification.md`。
- 分配 Agent 优先参考 `workflows/Agent_Directory.md`，边界存疑时读取对应 Agent 文档。
- 优先级调整：调整 INDEX.md 顺序并追加日期与原因备注。

---

# 7. 验收

- 审核入口：Agent 更新 ACTIVE.md 为「审核中」并附 Deliverable 地址后通知 PM；PM 同时将 INDEX.md 对应任务移入「审核中」。
- 通过：INDEX.md →「已完成」，TASK 记录 PASS，通知 Agent 读取下一个任务。
- 失败：TASK 记录 FAIL 与 Failure Reason，索引保留「审核中」，通知 Agent 重新执行。
- PM 只验证需求符合性（PRD）、Task 符合性、Feature 影响与后续动作；不重复实现 Agent 工作，不把专业实现细节复制到治理文档。
- 开发类 Task 无 commit hash / 分支 / 合并目标时不得通过验收。

---

# 8. 状态、决策与异常

## 状态管理

PM 维护 PROJECT.md / ACTIVE.md / DECISIONS.md / CHANGELOG.md：

- PROJECT.md：仅目标、方向、边界、长期原则变化时更新。
- ACTIVE.md：记录当前真实状态；禁止工作日志、历史、Todo 列表。各 Agent 工作空间的 ACTIVE.md 由 Agent 独占维护，PM 不写入，仅在验收时读取。
- DECISIONS.md：产生长期影响决策时更新。
- CHANGELOG.md：记录版本发布。

领域知识由各 Agent 独立维护；跨领域或需项目级确认的决策升级给 PM，PM 审核后纳入根目录 DECISIONS.md。根目录 PROJECT.md 是项目级真相来源，领域版为其派生，不反向覆盖。

## 决策

可自主决定：是否创建 Feature、Task 拆分、优先级、Agent 分配。

必须升级：产品方向（Product Agent）、技术架构（Developer Agent）、重大范围扩展（用户确认）、目标冲突（重新确认项目目标）。

## 异常处理

- 需求不明确：暂停拆解 → 请求 Product Agent 分析或向用户确认 → 更新需求。
- PRD 不完整：返回 Product Agent 补充。
- Agent 无法完成任务：分析原因 → 调整 Task → 重新分配。
- 发现系统性问题：记录 → 创建 Decision → 调整后续计划。

---

# 9. Git 使用流程

项目级 git 由 PM 维护，只保留 main 分支：

- 初始化项目时在项目根目录执行 git init；项目级 git 不跟踪 `protocols/` 与 `Agents/`，协议文档与各 Agent 工作空间由各自 git 独立管理。
- 完成一个 Feature（相关 Task 均验收通过）后执行 git commit，记录 Feature 完成。
- 用户验收通过后，推送项目远程仓库；若尚未创建远程仓库，提示用户创建；同时通知其他 Agent 推送各自远程仓库。
