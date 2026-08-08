# Agent Directory

**版本：** 1.0

**定位：**

PM Agent 的 Agent 指挥目录（快速参考）。

PM 进行需求分类、Task 拆解与 Agent 分配时，通过本目录快速确定：

- 项目中有哪些 Agent。
- 每个 Agent 负责什么。
- 可以分配什么类型的任务。
- 会交付什么结果。
- 不应该分配什么任务。

本目录仅 PM 使用，其他 Agent 无需读取。

详细职责定义见各 Agent Contract：

```text
protocols/Agents/{Agent}/Contract.md
```

**维护规则：**

- 本目录是快速引用，不是真相来源。
- Agent Contract 是唯一真相来源。
- Agent Contract 变更（角色、职责、交付、边界）时，必须同步更新本目录。
- 边界存疑时，以 Agent Contract 为准。

---

# Agent 一览

| Agent | 定位 | PM 可分配的任务 | 交付给 PM 的结果 | 边界（不可分配） |
|---|---|---|---|---|
| Product Agent | 产品需求分析 | 需求分析、产品方案、用户流程、验收标准 | Product Requirement | 技术实现、UI 设计、代码开发 |
| UI Agent | UI 设计与交互 | 界面设计、交互设计、组件与视觉规范 | 设计方案、交互说明、规范 | 产品决策、前端/移动端实现 |
| Frontend Agent | Web 前端实现 | 页面与交互实现、前端组件与工程 | Git Commit、Web 测试地址、变化说明 | 产品需求、UI 设计、Backend |
| Backend Agent | 服务端实现 | API、业务逻辑、数据模型 | Git Commit、API 文档、测试结果 | 产品需求、UI/UX、前端/移动端实现 |
| Mobile Agent | 移动端实现 | 页面与交互实现、客户端能力 | Git Commit、App 安装包、测试结果 | 产品需求、UI 设计、Backend |
| QA Agent | 质量验证 | 功能验证、回归测试、验收验证 | 测试报告、问题报告、风险说明 | 产品需求、代码修复、架构决策 |
