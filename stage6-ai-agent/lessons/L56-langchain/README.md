# L56: 从数据到 AI — LangChain 基础与应用编排

> **课程编号**: L56
> **所属阶段**: Stage 6 - AI Agent 开发  
> **预计时长**: 6-7 小时  
> **难度**: ⭐⭐⭐☆☆ (中级)
> **前置课程**: L49（RAG 基础）, L51（RAG 向量数据库）

> 💡 **桥梁课程**: 本课程是 Stage 4（数据智能）→ Stage 5（AI Agent）的关键桥接点。
> 新增 Part 0 帮数据分析师/工程师从零理解 LLM 并完成第一次 API 调用。详见 [lesson.md](lesson.md)。

---

## 📚 课程概览

- **位置**: Stage 5 / 第 1 课
- **学习时长**: 4-5 小时
- **难度**: ⭐⭐⭐⭐☆
- **前置课程**: L51 RAG 系统
## 🔗 下一步

完成本课后继续学习：

- [L57: RAG 与向量数据库](../L57-rag-vector/README.md)

> 📖 **学习路径提示**：L57 将学习 RAG 架构和向量数据库。
- **课程主题**: 用 LCEL、Prompt、Chain 和输出解析构建 LLM 应用管道

本 README 是课程入口地图。详细概念、代码讲解和练习说明以 `lesson.md` 为准；这里帮助你快速判断学习顺序、运行路径和完成标准。

## 🎯 学习目标

完成本课程后，你将掌握：

1. ✅ 理解 LangChain 的 Runnable 接口和 LCEL 管道表达式
2. ✅ 使用 ChatPromptTemplate、Few-Shot Prompt 和模板变量管理提示词
3. ✅ 组合 Sequential、Parallel 和 Router Chain
4. ✅ 使用 Pydantic、JSON 和 Structured Output 解析模型输出
5. ✅ 集成 OpenAI、Ollama 或本地模型并支持流式/异步调用

## 📋 前置知识

- 理解 LLM 调用的输入、输出、温度和模型参数
- 完成 RAG 课程，知道检索增强生成的基本链路
- 熟悉 Python 类型注解、Pydantic 模型和异步基础
- 准备可用的模型服务或 mock 对象用于本地测试

## 🗂️ 文件导航

| 文件                              | 用途                        |
| --------------------------------- | --------------------------- |
| `lesson.md`                       | 详细教程（422 行）          |
| `examples/01_langchain_basics.py` | 演示本课核心 API 和完整流程 |
| `exercises/01_qa_chain.py`        | 需要你补全的实践项目        |
| `solutions/01_qa_chain.py`        | 对应练习的参考实现          |
| `tests/test_qa_chain.py`          | 验证示例、练习和边界行为    |

> 说明：表格只列出本课需要直接关注的文件，`.gitkeep`、`__pycache__` 等占位或缓存文件不列入学习路径。

## 💡 核心知识点摘要

### 第一章: LCEL 表达式语言

LCEL 用管道符把 prompt、LLM 和 parser 串成 Runnable。
它统一支持 `invoke`、`batch`、`stream` 和 `ainvoke`，让同步、批量、流式与异步调用使用同一套接口。

### 第二章: Prompt 工程

Prompt 模板把系统消息、人类消息、变量和示例统一管理。
课程覆盖 ChatPromptTemplate、Few-Shot Prompt 和模板变量，强调提示词要可复用、可测试、可版本化。

### 第三章: Chain 组合模式

复杂应用不是单条链。
Sequential Chain 处理多步骤，Parallel Chain 并行执行独立任务，Router Chain 根据输入选择路径。
组合模式决定应用可维护性。

### 第四章: 输出解析与结构化

LLM 原始文本难以直接进入业务流程。
Pydantic、JSON parser 和 Structured Output 能把回答转成可验证对象，降低下游解析失败率。

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
- [ ] 能解释以下关键词：LCEL、Runnable、ChatPromptTemplate、Chain 组合、Structured Output

## 🔗 后续课程

- **L53 Agent 基础与工具调用**：继续把本课能力应用到下一阶段主题中。

## 🔗 下一步

完成本课后继续学习：

- [L57: RAG 向量数据库](../L57-rag-vector/README.md)
- L57 会学习 RAG（检索增强生成）与向量数据库，实现基于私有知识的 AI 问答。
