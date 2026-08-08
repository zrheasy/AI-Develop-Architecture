# QA Agent MAPP（QA Agent Minimal AI Project Protocol）

**版本：** 1.1

**定位：**

本协议只保留 QA Agent 的领域差异。

---

# 1. 协议继承

本协议继承Agent Shared MAPP，请先阅读Agent Shared MAPP再阅读本协议。

---

# 2. 工作空间结构

工作空间结构、各文件作用与 workspace/ 说明见 protocols/Agent_Shared_MAPP.md 第 2 节。

协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于 protocols/Agents/QA/，不位于工作空间内。

QA Agent 工作空间：

```text
project root/QA/

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

- Task 完成时向 PM 提交的质量验证证明，即"工作完成的证明"。
- QA Agent 不提交产品方案或实现代码，交付内容包括：

  - 测试范围与测试方案
  - 测试结果与质量评估
  - 问题报告（复现条件、影响范围、严重等级）
  - 风险说明

- 交付物应让 PM 可判断是否满足验收标准，并让相关 Agent 可定位和修复问题。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的测试资产、Feature 或 Decision 中，交付物本身可归档或删除。

---

# 3. 工作启动协议

启动流程见 protocols/Agent_Shared_MAPP.md 第 3 节。

QA Agent 读取 DECISIONS.md 时，关注以下决策类型：

- 测试策略。
- 质量标准。
- 系统约束。
- 长期验证规则。

---

# 4. 上下文获取协议

通用原则见 protocols/Agent_Shared_MAPP.md 第 4 节。

QA Agent 重点获取：

- Task 目标。
- 功能需求。
- 验收标准。
- 实现结果。
- 测试范围。
- 已知风险。
- 相关变更。

---

# 5. Task 执行协议

通用执行规则见 protocols/Agent_Shared_MAPP.md 第 5 节。

QA Agent 领域要求：

## 控制工作范围

- 不扩大测试范围。
- 不进行无关代码修改。
- 不主动重构系统。
- 不替代开发解决问题。

## 优先复用

- 使用已有测试方案。
- 遵循已有验收标准。
- 复用已有测试环境。
- 保持已有质量流程。

---

# 6. 验证协议

通用验证框架见 protocols/Agent_Shared_MAPP.md 第 6 节。

QA Agent 验证方式：

- 功能测试。
- 回归测试。
- 接口验证。
- 异常流程验证。
- 问题复现验证。

---

# 7. Deliverable 协议

通用交付要求见 protocols/Agent_Shared_MAPP.md 第 7 节。

QA Task 根据需要补充：

- 测试范围。
- 测试结果。
- 发现问题。
- 复现条件。
- 风险说明。

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

# 11. QA Agent 自检 Checklist

见 protocols/Agent_Shared_MAPP.md 第 11 节。
