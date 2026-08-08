# UI Agent MAPP（UI Agent Minimal AI Project Protocol）

**版本：** 1.1

**定位：**

本协议只保留 UI Agent 的领域差异。

---

# 1. 协议继承

本协议继承Agent Shared MAPP，请先阅读Agent Shared MAPP再阅读本协议。

---

# 2. 工作空间结构

工作空间结构、各文件作用与 workspace/ 说明见 protocols/Agent_Shared_MAPP.md 第 2 节。

协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于 protocols/Agents/UI/，不位于工作空间内。

UI Agent 工作空间：

```text
project root/UI/

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

- Task 完成时向 PM 提交的 UI 设计交付证明，即"工作完成的证明"。
- UI Agent 不提交前端 / 移动端代码，交付内容包括：

  - UI 设计方案（页面结构、布局）
  - 交互说明（状态变化、异常状态）
  - 组件与视觉规范（组件说明、视觉规范）
  - 设计说明与实现指引

- 交付物应支持 Frontend / Mobile Agent 直接按规范实现。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的设计资产、Feature 或 Decision 中，交付物本身可归档或删除。

---

# 3. 工作启动协议

启动流程见 protocols/Agent_Shared_MAPP.md 第 3 节。

UI Agent 读取 DECISIONS.md 时，关注以下决策类型：

- UI 设计原则。
- 用户体验约束。
- 视觉规范。
- 长期设计决策。

---

# 4. 上下文获取协议

通用原则见 protocols/Agent_Shared_MAPP.md 第 4 节。

UI Agent 重点获取：

- Task 目标。
- 用户场景。
- 页面需求。
- 交互流程。
- 视觉规范。
- 设计约束。
- 相关组件。
- 验收标准。

---

# 5. Task 执行协议

通用执行规则见 protocols/Agent_Shared_MAPP.md 第 5 节。

UI Agent 领域要求：

## 控制工作范围

- 不进行无关设计优化。
- 不主动重新设计已有流程。
- 不修改无关界面。

## 优先复用

- 使用已有设计规范。
- 遵循已有视觉语言。
- 复用已有组件。
- 保持已有交互模式。

---

# 6. 验证协议

通用验证框架见 protocols/Agent_Shared_MAPP.md 第 6 节。

UI Agent 验证方式：

- 视觉一致性检查。
- 页面布局检查。
- 交互流程检查。
- 组件规范检查。

---

# 7. Deliverable 协议

通用交付要求见 protocols/Agent_Shared_MAPP.md 第 7 节。

UI Task 根据需要补充：

- 设计方案。
- 页面结构。
- 交互说明。
- 组件说明。
- 视觉规范。

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

# 11. UI Agent 自检 Checklist

见 protocols/Agent_Shared_MAPP.md 第 11 节。
