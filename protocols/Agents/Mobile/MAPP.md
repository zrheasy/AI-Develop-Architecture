# Mobile Agent MAPP（Mobile Agent Minimal AI Project Protocol）

**版本：** 1.1

**定位：**

本协议只保留 Mobile Agent 的领域差异。

---

# 1. 协议继承

本协议继承Agent Shared MAPP，请先阅读Agent Shared MAPP再阅读本协议。

---

# 2. 工作空间结构

工作空间结构、各文件作用与 workspace/ 说明见 protocols/Agent_Shared_MAPP.md 第 2 节。

协议文件（CONTRACT.md / MAPP.md / CAPABILITY.md）统一存放于 protocols/Agents/Mobile/，不位于工作空间内。

Mobile Agent 工作空间：

```text
project root/Mobile/

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

- Task 完成时向 PM 提交的移动端实现交付证明，即"工作完成的证明"。
- **禁止提交源代码**。代码保留在 workspace/，提交以下交付证明：

  - Git Commit（代码已完成并提交的记录）
  - App 安装包（测试包或构建产物）
  - 页面与交互变化说明
  - 平台兼容性与测试结果

- 交付物应让 QA Agent 可直接安装验证。
- deliverables/ 不是长期资产目录：任务验收后，长期价值沉淀到 workspace/ 的代码、Feature 或 Decision 中，交付物本身可归档或删除。

---

# 3. 工作启动协议

启动流程见 protocols/Agent_Shared_MAPP.md 第 3 节。

Mobile Agent 读取 DECISIONS.md 时，关注以下决策类型：

- 移动端架构。
- 平台设计原则。
- 用户体验约束。
- 技术约束。

---

# 4. 上下文获取协议

通用原则见 protocols/Agent_Shared_MAPP.md 第 4 节。

Mobile Agent 重点获取：

- Task 目标。
- 移动端需求。
- 页面流程。
- 交互要求。
- 平台约束。
- 相关组件。
- 相关接口。
- 验收标准。

---

# 5. Task 执行协议

通用执行规则见 protocols/Agent_Shared_MAPP.md 第 5 节。

Mobile Agent 领域要求：

## 控制工作范围

- 不进行无关优化。
- 不主动重构已有系统。
- 不修改无关页面或功能。

## 优先复用

- 使用已有移动端组件。
- 遵循已有设计规范。
- 保持已有交互模式。
- 复用已有接口能力。
- 遵循平台规范。

---

# 6. 验证协议

通用验证框架见 protocols/Agent_Shared_MAPP.md 第 6 节。

Mobile Agent 验证方式：

- 应用构建检查。
- 页面展示检查。
- 用户流程检查。
- 平台兼容性检查。
- 设备运行验证。

---

# 7. Deliverable 协议

通用交付要求见 protocols/Agent_Shared_MAPP.md 第 7 节。

Mobile Task 根据需要补充：

- 页面变化。
- 组件变化。
- 平台变化。
- 接口依赖。
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

# 11. Mobile Agent 自检 Checklist

见 protocols/Agent_Shared_MAPP.md 第 11 节。
