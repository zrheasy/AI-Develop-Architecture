# PROJECT.md Standard

**版本：** 2.0

---

# 1. 作用

定义项目稳定上下文，回答「这是一个什么项目」，让任何 Agent 在最短时间内理解项目目的、目标、边界与核心原则。

---

# 2. 标准结构

```markdown
# Project Name

## Overview
一句话描述项目。

## Mission
项目长期使命（为什么存在）。

## Product Vision
产品希望提供的长期价值。

## Scope
### In Scope
### Out of Scope

## Core Principles
项目长期原则。

## Technology Context
技术栈、平台、系统组成（不描述实现细节与当前任务）。

## Architecture Overview（工程类项目必填）
架构设计说明：系统组成、模块边界与关键关系（不描述实现细节）。

## Key Technologies（工程类项目必填）
关键技术说明：关键技术选型与采用原因。

## Project Structure
项目主要结构说明。

## Current Phase
MVP / Growth / Maintenance 等。
```

---

# 3. 记录规则

- 只保存长期稳定信息：目标、方向、范围、长期约束、技术背景。
- 工程类项目应记录架构设计说明（Architecture Overview）与关键技术说明（Key Technologies）。
- 不记录：当前任务、开发进度、临时问题、历史过程、决策讨论。
- 不复制 Feature / Decision / Task 已有信息。

---

# 4. 质量标准

- 稳定：不频繁修改。
- 简洁：Agent 30 秒内理解。
- 有效：未来半年仍然有效。

---

# 5. 更新条件

仅当项目目标、产品方向、项目边界、长期原则变化时更新；普通需求不更新。
