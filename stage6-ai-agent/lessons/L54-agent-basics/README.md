# L54: Agent 基础与工具调用

> **课程编号**: L54
> **所属阶段**: Stage 6 - AI Agent 开发  
> **预计时长**: 4-5 小时  
> **难度**: ⭐⭐⭐⭐☆ (中高级)

---

## 📚 课程概览

- **位置**: Stage 5 / 第 2 课
- **学习时长**: 4-5 小时
- **难度**: ⭐⭐⭐⭐☆
- **前置课程**: L52 LangChain 基础
- **后续课程**: L54 LangGraph 状态机
- **课程主题**: 让 LLM 通过工具执行外部动作，形成可观察的 Agent 循环

本 README 是课程入口地图。详细概念、代码讲解和练习说明以 `lesson.md` 为准；这里帮助你快速判断学习顺序、运行路径和完成标准。

## 🎯 学习目标

完成本课程后，你将掌握：

1. ✅ 理解 Agent = LLM + Tools + Memory + Planning 的核心模型
2. ✅ 掌握 ReAct 的 Thought、Action、Observation 循环
3. ✅ 使用 @tool 和 StructuredTool 设计安全工具接口
4. ✅ 实现基础 ReAct Agent 和 OpenAI Functions Agent
5. ✅ 加入异步、流式、回调、错误重试和 Token 追踪

## 📋 前置知识

- 熟悉 LangChain Chain、Prompt 和输出解析器
- 理解函数调用、参数校验和错误处理
- 知道外部 API、搜索、计算器等工具的安全边界
- 具备调试日志和 pytest 基础

## 🗂️ 文件导航

| 文件                          | 用途                        |
| ----------------------------- | --------------------------- |
| `lesson.md`                   | 详细教程（479 行）          |
| `examples/01_agent_tools.py`  | 演示本课核心 API 和完整流程 |
| `exercises/01_agent_tools.py` | 需要你补全的实践项目        |
| `solutions/01_agent_tools.py` | 对应练习的参考实现          |
| `tests/test_agent_tools.py`   | 验证示例、练习和边界行为    |

> 说明：表格只列出本课需要直接关注的文件，`.gitkeep`、`__pycache__` 等占位或缓存文件不列入学习路径。

## 💡 核心知识点摘要

### 第一章: Agent 核心概念

Agent 不是一次性问答，而是 LLM 在目标驱动下反复思考、选择工具、观察结果并继续推理。
ReAct 模式把推理过程拆成 Thought、Action 和 Observation。

### 第二章: 工具系统设计

工具是 Agent 能力边界。
课程从 `@tool` 装饰器到 StructuredTool，强调参数 schema、文档字符串、错误返回和权限限制，避免工具设计模糊导致模型误用。

### 第三章: ReAct Agent 实现

实现部分覆盖基础 Agent、OpenAI Functions Agent 和执行结果结构。
你会看到中间步骤、工具调用输入输出，以及如何解释 Agent 为什么选择某个工具。

### 第四章: 生产化实践

生产 Agent 需要异步执行、流式输出、自定义回调、重试和 Token 追踪。
课程把演示代码推进到可观测、可调试、可控成本的工程形态。

### 最佳实践总结

本课最后的总结章节把教程内容收敛成可执行清单。学习时不要只复制示例代码，要把清单转化为自己的检查流程：输入是什么、输出是什么、失败时如何定位。

### 练习题定位

练习题用于把概念转成工程能力。建议先独立完成 `exercises/`，再对照 `solutions/` 检查边界处理、类型注解、错误信息和测试覆盖。

## 🚀 快速开始

_(详细代码见 lesson.md)_

## 📊 完成标准

- [ ] 阅读完 `lesson.md`，能复述每一章的核心问题
- [ ] 运行所有 `examples/` 脚本，并理解输出含义
- [ ] 完成 `exercises/` 练习，代码不依赖硬编码答案
- [ ] 对照 `solutions/`，修正命名、结构、边界处理和类型注解
- [ ] `pytest tests/ -v` 全部通过
- [ ] 能解释以下关键词：Agent Loop、ReAct、Tool Calling、StructuredTool、Token 追踪

## 🔗 后续课程

- **L54 LangGraph 状态机**：继续把本课能力应用到下一阶段主题中。

## 🔗 下一步

完成本课后继续学习：

- [L55: MCP 协议入门](../L55-mcp-protocol/README.md)
- L55 会学习 MCP（Model Context Protocol），理解 Agent 与工具的标准化通信协议。
