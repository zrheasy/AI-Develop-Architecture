# AI 原生软件研发组织架构与工作流程

**Version: 3.0**

本文件是整套架构的导读。

详细规则见本文档引用的各协议文件，不在此重复展开。

---

# 1. 设计目标

本架构用于 AI Agent 驱动的软件研发项目。

核心目标：

- 降低 AI 工作上下文复杂度。
- 明确 Agent 职责边界。
- 支持长期持续研发。
- 支持多 Agent 并行协作。
- 实现产品能力、执行任务、技术实现的分离。
- 避免传统项目管理中的流程负担。

核心原则：

> **需求驱动，Feature 管理产品能力，Task 管理执行变化，Agent 负责专业执行。**

---

# 2. 核心设计思想

AI 原生研发组织由四个层次组成：

```text
Project Governance

        ↓

Product Management

        ↓

Agent Execution

        ↓

Task Delivery
```

核心对象：

```text
Project

├── Product Requirement
│
├── Feature
│
├── Task
│
├── Decision
│
└── Release
```

---

# 3. 核心对象模型

| 对象 | 定义 | 负责人 | 位置 | 详细规格 |
|---|---|---|---|---|
| Project | 整个软件项目 | PM Agent | PROJECT.md | protocols/Project_Documentation_Standards.md |
| Product Requirement | 产品决策摘要 | Product Agent | requirements/ | protocols/Product_Requirement_Specification.md |
| Feature | 长期产品能力 | PM Agent | features/ | protocols/Feature_Specification.md |
| Task | 临时执行契约 | PM Agent | tasks/{Agent}/ | protocols/Task_Specification.md |
| Deliverable | 工作完成的证明 | 执行 Agent | {Agent}/deliverables/ | protocols/Agent_Shared_MAPP.md |
| Decision | 长期项目决策 | PM / 相关 Agent | decisions/ | protocols/Decisions_Documentation_Standards.md |
| Release | 产品发布版本 | PM Agent | CHANGELOG.md | — |

核心关系：

```text
User Request → Product Requirement → Feature → Task → Deliverable
```

---

# 4. 协议体系

| 协议 | 文件 | 解决 | 说明 |
|---|---|---|---|
| ROOT MAPP | protocols/ROOT_MAPP.md | AI 应该如何工作 | 顶层协议，最小上下文原则 |
| Agent Shared MAPP | protocols/Agent_Shared_MAPP.md | Agent 如何通用工作 | 各 Agent MAPP 只保留领域差异 |
| Agent Contract | protocols/Agents/{Agent}/Contract.md | Agent 是谁 | 角色、职责、边界、决策权限 |
| Agent Shared Contract | protocols/Agent_Shared_Contract.md | 公共契约条款 | 边界规则、维护规则 |
| Agent MAPP | protocols/Agents/{Agent}/MAPP.md | Agent 如何执行 | 领域差异与共享引用 |
| Agent Capability | protocols/Agents/{Agent}/Capability.md | 领域长期规则 | 技术原则、选型、反模式 |
| PM Contract | protocols/PM_Contract.md | PM 是谁 | 组织角色与职责 |
| PM Operating Protocol | protocols/PM_Operating_Protocol.md | PM 如何运行项目 | 需求到验收的完整流程 |
| Agent Directory | protocols/Agent_Directory.md | PM 指挥哪些 Agent | 分配快速参考 |

获取知识路径见第 5 节。

协议继承关系：

```text
ROOT MAPP

   ↑ 继承

Agent Shared MAPP            PM Operating Protocol

   ↑ 继承

Agent MAPP
```

规则：

- ROOT MAPP 是唯一项目级协议，独立定义，不依赖其他协议。
- Agent Shared MAPP 与 PM Operating Protocol 继承 ROOT MAPP。
- Agent MAPP 继承 Agent Shared MAPP，并通过它继承 ROOT MAPP。
- Agent Shared MAPP 引导 Agent 阅读 ROOT MAPP 与 Agent Shared MAPP。
- Agent Contract / PM Contract 定义身份与职责边界。
- Task Requirement 是具体执行输入，服从所在协议链的全部规则。

---

# 5. 获取知识路径

获取知识路径是 Agent / PM 进入项目时读取协议文档的权威顺序。

PM：

```text
PM_Contract → PM_Operating_Protocol → 其他协议文档
```

Agent：

```text
Agent_Contract → Agent MAPP → CAPABILITY → PROJECT → ACTIVE → TASK → DECISIONS
```

说明：

- 路径为 Agent / PM 进入项目时的知识获取顺序。
- DECISIONS 按需读取，仅当任务涉及长期决策时。
- 路径只描述阅读顺序，不是对象流转关系；对象流转见第 10 节系统模型。

---

# 6. Agent 组织模型

整体结构：

```text
                         User

                           |

                           ▼

                       PM Agent

                    (Control Plane)

                           |

        ┌──────────────────┼──────────────────┐

        ▼                  ▼                  ▼


 Product Agent        Feature管理        Task管理


        |

        ▼


 Product Requirement


                           |

                           ▼


                    Execution Plane


        ┌──────────────┬──────────────┬──────────────┐


        ▼              ▼              ▼


    UI Agent     Developer Agent    QA Agent


                       |

          ┌────────────┼────────────┐

          ▼            ▼            ▼


     Frontend     Backend       Mobile


                       |

                       ▼


                 Deliverable


                       |

                       ▼


                  PM Review
```

---

# 7. Agent 职责模型

| Agent | 定位 | 负责 | 不负责 |
|---|---|---|---|
| PM Agent | Control Plane | 需求入口、Feature/Task 管理、Agent 协调、状态维护 | 产品方案、技术实现、代码开发 |
| Product Agent | Product Plane | 需求分析、产品方案、用户流程、验收标准 | 技术实现、UI 设计、开发执行 |
| UI Agent | Execution Plane | UI 设计、交互设计、视觉规范 | 产品决策、前端实现 |
| Developer Agents（Frontend / Backend / Mobile） | Execution Plane | 按 Task 实现功能、输出 Deliverable、技术验证 | 产品范围、Feature 定义、长期架构决策 |
| QA Agent | Execution Plane | 功能验证、流程测试、质量反馈 | 需求定义、代码修复、架构决策 |

详细职责见各 Agent Contract 与 PM Contract。

---

# 8. 工作空间结构

每个 Agent 的工作空间位于：

```text
project root/{Agent}/
```

工作空间结构、各文件作用、workspace/ 与 deliverables/ 的说明见：

```text
protocols/Agent_Shared_MAPP.md 第 2 节
```

---

# 9. 标准工作流程

```text
阶段0 项目初始化与产品形态定义（新项目）

新项目 → PM 判断项目是否已初始化，未初始化则启动初始化

新项目 → PM 创建目录骨架与 PROJECT.md / ACTIVE.md / DECISIONS.md / CHANGELOG.md

新项目 → PM 初始化 Product Agent 工作空间

新项目 → Product Agent 需求分析 → PRD

新项目 → PM 基于 PRD 进行产品形态规划（不确定时询问用户）→ 完善 PROJECT.md

新项目 → 其他 Agent 工作空间按需初始化

已有项目 → 跳过

阶段1 需求进入

User Request → PM Agent


阶段2 需求判断

PM 判断是否需要产品分析


阶段3 Feature 管理

新能力 → 创建 Feature

已有能力扩展 → 更新 Feature Scope

技术优化 / Bug 修复 → 直接创建 Task


阶段4 Task 创建

根据 Product Requirement 创建 tasks/{Agent}/ 任务，登记 INDEX.md（等待中 → 执行中）


阶段5 Agent 执行

Agent 读取 CONTRACT → MAPP → CAPABILITY → PROJECT → ACTIVE → TASK INDEX → TASK → DECISIONS（按需）

执行 → 验证 → 输出 Deliverable


阶段6 PM 验收

确认用户目标、Product Requirement、Task 验收标准


阶段7 状态维护

PM 更新 TASK INDEX / DECISIONS.md / Feature Evolution；Agent 更新自身 ACTIVE.md
```

新项目必须先完成阶段 0，再进入阶段 1；已有项目直接进入阶段 1。

项目启动流程见 protocols/PM_Operating_Protocol.md 第 4 节。

详细流程见：

```text
protocols/PM_Operating_Protocol.md
```

---

# 10. 系统模型

```text
User

↓

Product Requirement

↓

Feature

↓

Task

↓

Deliverable

↓

Feature Evolution
```

注：本图描述对象流转与系统组成，不是获取知识路径。获取知识路径见第 5 节。

---

# 总结

AI 原生软件研发组织最终模型：

> MAPP 管理 AI 工作方式，Contract 定义 Agent 身份，Operating Protocol 定义角色运行方式，Product Agent 定义产品方案，PM 管理产品能力和执行任务，Developer Agent 负责技术实现，Deliverable 证明工作完成。

核心分工：

| 对象 | 负责 |
|-|-|
| Product Requirement | 为什么做、做什么 |
| Feature | 产品长期能力 |
| Task | 当前执行工作 |
| Deliverable | 执行结果 |
| Decision | 长期决策 |
| Release | 发布版本 |

最终目标：

> 让 AI Agent 在最小上下文中长期协作，同时保持产品能力、执行过程和技术实现的清晰分离。
