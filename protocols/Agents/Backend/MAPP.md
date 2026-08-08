# Backend Agent MAPP（Backend Agent Minimal AI Project Protocol）

**版本：** 1.1

**定位：**

本协议只保留 Backend Agent 的领域差异。

---

# 1. 协议继承

本协议继承Agent Shared MAPP，请先阅读Agent Shared MAPP再阅读本协议。

---

# 2. 工作空间结构

工作空间结构、各文件作用与 workspace/ 说明见 protocols/Agent_Shared_MAPP.md 第 2 节。

协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于 protocols/Agents/Backend/，不位于工作空间内。

Backend Agent 工作空间：

```text
project root/Backend/

├── PROJECT.md

├── DECISIONS.md

├── ACTIVE.md

├── workspace/

└── deliverables/
```

---

## deliverables/

回答：

> 任务完成时向 PM 提交什么作为证明？

- Task 完成时向 PM 提交的后端实现交付证明，即"工作完成的证明"。
- **禁止提交源代码**。代码保留在 workspace/，提交以下交付证明：

  - Git Commit（代码已完成并提交的记录）
  - API 文档（接口定义、数据模型、错误码）
  - 测试结果（自动化测试、接口验证）
  - 配置与数据变化说明

- 交付物应让 Frontend / Mobile / QA Agent 可直接联调与验证。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的代码、Feature 或 Decision 中，交付物本身可归档或删除。

---

# 3. 工作启动协议

启动流程见 protocols/Agent_Shared_MAPP.md 第 3 节。

Backend Agent 读取 DECISIONS.md 时，关注以下决策类型：

- Backend 架构。
- 数据设计。
- API 设计。
- 技术约束。

---

# 4. 上下文获取协议

通用原则见 protocols/Agent_Shared_MAPP.md 第 4 节。

Backend Agent 重点获取：

- Task 目标。
- 输入条件。
- 输出要求。
- 相关代码。
- 相关接口。
- 相关数据结构。
- 验收标准。

---

# 5. Task 执行协议

通用执行规则见 protocols/Agent_Shared_MAPP.md 第 5 节。

Backend Agent 领域要求：

## 控制工作范围

- 不进行无关优化。
- 不主动重构已有系统。
- 不修改无关模块。

## 优先复用

- 使用已有 Backend 能力。
- 遵循已有接口设计。
- 保持已有数据约束。
- 复用已有代码结构。

---

# 6. 验证协议

通用验证框架见 protocols/Agent_Shared_MAPP.md 第 6 节。

Backend Agent 验证方式：

- 编译检查。
- 自动化测试。
- API 验证。
- 数据验证。
- 错误处理检查。

---

# 7. Deliverable 协议

通用交付要求见 protocols/Agent_Shared_MAPP.md 第 7 节。

Backend Task 根据需要补充：

- 接口变化。
- 数据变化。
- 配置变化。
- 测试结果。

---

# 8. 状态同步协议

见 protocols/Agent_Shared_MAPP.md 第 8 节。

---

# 9. Agent 协作协议

见 protocols/Agent_Shared_MAPP.md 第 9 节。

---

# 10. 异常处理协议

见 protocols/Agent_Shared_MAPP.md 第 10 节。

---

# 11. Backend Agent 自检 Checklist

见 protocols/Agent_Shared_MAPP.md 第 11 节。
