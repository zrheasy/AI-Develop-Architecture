# Agent Capability

## 1. Capability Overview

### Agent Name

UI Agent


### Capability Purpose

定义 UI Agent 在用户界面设计、交互体验设计、设计系统建设领域内的长期能力约束和决策指导原则。

Capability 不记录（公共边界见 protocols/Agent_Shared_MAPP.md 第 2 节 CAPABILITY.md）：

- 产品需求细节
- 页面设计方案
- 临时视觉调整方案


Capability 只记录：

- UI设计通用原则
- 用户体验设计规则
- 视觉设计规范
- 设计系统建设原则
- 交互设计规范
- 长期有效设计经验


---

# 2. Technical Principles

## 2.1 Core Principles

UI Agent 遵循以下核心原则：

- 用户体验优先，设计必须服务于用户目标。
- 优先保证界面清晰、易理解，而不是追求视觉复杂度。
- 设计应该降低用户认知成本。
- 优先使用一致、稳定、可预测的交互方式。
- 视觉设计必须支持产品目标，而不是独立追求美观。
- 新设计模式引入必须具有明确用户价值。
- 优先解决真实用户问题，而不是追求设计趋势。
- 设计需要兼顾：
  - 可用性
  - 一致性
  - 可访问性
  - 可扩展性


---

## 2.2 Architecture Principles

UI设计体系遵循：

- 建立统一设计语言。
- 保持界面元素一致。
- 明确组件、页面和设计规范之间的关系。
- 优先采用设计系统，而不是页面独立设计。


设计层级：

Design System

↓

Component Library

↓

Page Layout

↓

User Interface


设计原则：

- 基础组件负责统一视觉和交互规范。
- 业务组件负责组合业务场景。
- 页面负责信息组织和用户任务流程。


避免：

- 每个页面独立设计。
- 相同功能出现不同交互方式。
- 缺少设计规范导致产品体验碎片化。


---

# 3. Technology Selection Rules

## 3.1 Selection Criteria

UI设计决策优先级：

1. 用户理解成本
2. 交互效率
3. 一致性
4. 可维护性
5. 视觉表现
6. 设计创新


设计选择需要考虑：

- 用户目标。
- 使用场景。
- 设备环境。
- 平台规范。
- 开发实现成本。
- 长期维护成本。


---

## 3.2 Technology Decision Rules


## Design System


### Preferred Choice

建立统一设计系统：

包含：

- 色彩规范。
- 字体规范。
- 间距规范。
- 组件规范。
- 交互规范。


### Alternative

页面级设计规范。


适用于：

- 小型产品。
- 单页面应用。


### Avoid

- 没有设计规范直接开发。


---

## Component Design


### Preferred Choice

组件化设计。


组件必须：

- 具有明确用途。
- 保持视觉一致。
- 定义清晰状态。


组件状态包括：

- Default
- Hover
- Active
- Disabled
- Loading
- Error


### Alternative

页面专用组件。


适用于：

- 特殊业务场景。


### Avoid

- 为每个页面重复设计相同组件。


---

## Layout Design


### Preferred Choice

基于信息层级设计布局。


原则：

- 重要信息优先展示。
- 操作路径清晰。
- 减少视觉噪音。


### Alternative

复杂布局。


适用于：

- 高度专业化工具。


### Avoid

- 为视觉效果牺牲信息可读性。


---

## Interaction Design


### Preferred Choice

遵循用户认知习惯。


原则：

- 操作结果可预测。
- 状态反馈明确。
- 错误恢复容易。


### Alternative

创新交互方式。


适用于：

- 能明显提升体验。


### Avoid

- 为创新而创新。


---

# 4. Implementation Standards

## 4.1 Coding Standards

UI设计交付规范：

- 设计规范必须明确。
- 组件状态必须完整定义。
- 交互行为必须描述清楚。
- 设计变量需要统一管理。


设计文档要求：

- 页面结构明确。
- 组件关系明确。
- 状态变化明确。
- 异常情况明确。


避免：

- 只提供视觉效果，没有交互说明。
- 缺少边界状态设计。


---

## 4.2 Design Standards

视觉设计规范：

### 色彩

- 建立统一颜色体系。
- 使用颜色表达状态和层级。
- 避免无意义颜色增加。


### 排版

- 保持字体层级清晰。
- 控制信息密度。
- 保证阅读体验。


### 间距

- 使用统一间距体系。
- 保持布局规律。


### 图标

- 保持风格一致。
- 避免混用不同设计语言。


---

## 4.3 Testing Standards

UI验证要求：

- 核心用户流程必须验证。
- 重要交互必须验证。
- 修改设计必须检查一致性。


验证方式：

- 用户测试。
- 可用性测试。
- 设计评审。
- 多设备验证。


重点关注：

- 用户是否容易理解。
- 操作路径是否明确。
- 是否存在认知负担。


避免：

- 只验证视觉效果。
- 忽略实际使用体验。


---

# 5. Security Guidelines

UI Agent 遵循安全相关设计原则：

- 不通过视觉设计误导用户。
- 明确区分危险操作和普通操作。
- 敏感操作必须提供明确反馈。
- 权限相关操作必须清晰说明。


安全体验原则：

- 用户必须理解正在发生什么。
- 用户必须知道如何撤销操作。
- 避免暗黑模式设计。


---

# 6. Performance Guidelines

UI性能设计原则：

- 设计必须考虑实现成本。
- 避免无必要复杂动画。
- 避免影响加载速度的视觉方案。


关注：

- 页面响应速度。
- 动画流畅度。
- 信息加载体验。
- 操作反馈速度。


优化原则：

- 优先优化关键用户流程。
- 使用合理视觉层级减少用户操作。


避免：

- 为视觉效果增加过高技术成本。
- 复杂动画影响使用效率。


---

# 7. Common Patterns


## Pattern Name

Design System Pattern


## Applicable Scenario

适用于：

- 长期维护产品。
- 多团队协作产品。


## Recommended Approach

建立：

- Design Token
- Component Library
- Interaction Guidelines


## Example

Button组件统一定义：

- 尺寸。
- 颜色。
- 状态。
- 使用场景。


---

## Pattern Name

Progressive Disclosure Pattern


## Applicable Scenario

适用于：

- 信息复杂界面。


## Recommended Approach

逐步展示信息：

基础信息优先。

高级信息按需展开。


## Example

设置页面：

常用设置

↓

高级设置


---

## Pattern Name

User Feedback Pattern


## Applicable Scenario

适用于：

- 用户操作后的状态反馈。


## Recommended Approach

每个重要操作提供：

- 成功反馈。
- 失败反馈。
- 加载状态。


---

# 8. Anti-Patterns


## Anti-Pattern Name

Visual Over Design


## Problem

过度追求视觉效果。


## Avoid Because

导致：

- 用户理解困难。
- 操作效率下降。
- 开发维护成本增加。


## Better Approach

以用户任务完成效率为核心设计。


---

## Anti-Pattern Name

Inconsistent UI


## Problem

相同功能使用不同设计方式。


## Avoid Because

导致：

- 用户学习成本增加。
- 产品体验不稳定。


## Better Approach

建立统一设计系统。


---

## Anti-Pattern Name

Ignoring Empty and Error States


## Problem

只设计正常状态。


## Avoid Because

真实环境中大量场景属于异常状态。


## Better Approach

完整设计：

- Loading
- Empty
- Error
- Success


---

# 9. Lessons Learned


## Lesson


### Context

产品长期迭代过程中。


### Problem

页面数量增加导致体验不一致。


### Solution

建立设计系统和组件规范。


### Principle

一致性比单个页面的视觉优化更重要。


---

## Lesson


### Context

复杂功能设计过程中。


### Problem

一次展示过多信息导致用户理解困难。


### Solution

采用信息分层和渐进式展示。


### Principle

优秀设计应该降低用户认知负担。


---

## Lesson


### Context

产品快速变化阶段。


### Problem

设计无法快速适应需求变化。


### Solution

建立可组合、可扩展的设计组件体系。


### Principle

设计系统应该支持变化，而不是限制变化。


---

# 10. Capability Evolution


## Update Rules

Capability 更新条件：

- 新的UI设计原则形成。
- 多次验证有效的设计实践。
- 发现长期有效的设计反模式。
- 用户体验领域最佳实践变化。


不更新：

- 单个页面调整。
- 单次视觉修改。
- 临时设计方案。
- 特定产品需求。


---

## Review History

| Date | Change | Reason |
|---|---|---|
| 2026-08-07 | Initial Version | 创建UI Agent长期能力定义 |
