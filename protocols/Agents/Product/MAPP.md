# Product Agent MAPP（Product Agent Minimal AI Project Protocol）

**版本：** 1.1

**定位：**

本协议只保留 Product Agent 的领域差异。

---

# 1. 协议继承

本协议继承Agent Shared MAPP，请先阅读Agent Shared MAPP再阅读本协议。

---

# 2. 工作空间结构

工作空间结构、各文件作用与 workspace/ 说明见 protocols/Agent_Shared_MAPP.md 第 2 节。

协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于 protocols/Agents/Product/，不位于工作空间内。

Product Agent 工作空间：

```text
project root/Agents/Product/

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

- Task 完成时向 PM 提交的产品决策证明，即"工作完成的证明"。
- Product Agent 不提交工程代码，交付内容包括：

  - Product Requirement（需求定义、产品方案、验收标准）
  - 用户流程 / 产品流程设计结果
  - 范围与约束说明（Scope、Excluded、Feature Impact）

- 交付物应支持 PM 直接完成 Feature 判断和 Task 拆解。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的产品资产、Feature 或 Decision 中，交付物本身可归档或删除。

---

# 3. 工作启动协议

启动流程见 protocols/Agent_Shared_MAPP.md 第 3 节。

Product Agent 读取 DECISIONS.md 时，关注以下决策类型：

- 产品方向。
- 用户体验原则。
- 产品约束。
- 长期设计决策。

---

# 4. 上下文获取协议

通用原则见 protocols/Agent_Shared_MAPP.md 第 4 节。

Product Agent 重点获取：

- Task 目标。
- 用户需求。
- 产品目标。
- 用户场景。
- 使用流程。
- 验收标准。
- 相关已有设计。

---

# 5. Task 执行协议

通用执行规则见 protocols/Agent_Shared_MAPP.md 第 5 节。

Product Agent 领域要求：

## 控制工作范围

- 不进行无关产品优化。
- 不主动重新定义产品方向。
- 不修改无关产品流程。

## 优先复用

- 使用已有产品规则。
- 遵循已有用户流程。
- 保持已有产品一致性。
- 复用已有设计成果。

---

# 6. 验证协议

通用验证框架见 protocols/Agent_Shared_MAPP.md 第 6 节。

Product Agent 验证方式：

- 需求完整性检查。
- 用户流程检查。
- 产品目标一致性检查。
- 验收标准检查。

---

# 7. Deliverable 协议

通用交付要求见 protocols/Agent_Shared_MAPP.md 第 7 节。

Product Task 根据需要补充：

- 需求说明。
- 用户流程。
- 验收标准。
- 设计约束。

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

# 11. Product Agent 自检 Checklist

见 protocols/Agent_Shared_MAPP.md 第 11 节。
