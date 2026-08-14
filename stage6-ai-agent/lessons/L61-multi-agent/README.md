# L61: 多智能体编排 (Multi-Agent Orchestration)

> **课程编号**: L61  
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时  
> **难度**: ⭐⭐⭐⭐⭐ (高级)

> **课程定位**: Stage 5 AI Agent 终极模块 - 使用 LangGraph 构建生产级多智能体系统

---

## 📋 前置知识

- [L54: Agent 基础](../L54-agent-basics/)
- [L56: LangChain 基础](../L56-langchain/)
- [L58: LangGraph 进阶](../L58-langgraph-adv/)

## 📚 课程概览

- **位置**: Stage 6 / 第 8 课
- **学习时长**: 4-5 小时
- **难度**: ⭐⭐⭐⭐⭐
- **前置课程**: L60 Agent 规划
## 🔗 下一步

完成本课后继续学习：

- [L62: LangGraph 服务端部署](../L62-langgraph-server/README.md)

> 📖 **学习路径提示**：L62 将学习 LangGraph 的服务端部署和 API 封装。
- **课程主题**: 多智能体协作与编排模式

本 README 是课程入口地图。详细概念、代码讲解和练习说明以 `lesson.md` 为准；这里帮助你快速判断学习顺序、运行路径和完成标准。

---

## 🎯 学习目标

完成本课程后，你将掌握：

1. ✅ **LangGraph 状态机编程** - 使用声明式图结构定义 Agent 工作流
2. ✅ **Supervisor 路由模式** - 实现主管 Agent 协调多个专家 Agent
3. ✅ **Human-in-the-Loop** - 在关键节点引入人类审核与决策
4. ✅ **状态持久化** - 使用 Checkpointer 实现工作流的中断与恢复
5. ✅ **生产化测试** - 使用 Mock 隔离外部依赖，实现离线测试

---

## 📚 核心架构

### 架构 1: 单节点 Agent 状态机

_(详细代码见 lesson.md)_

**核心概念**:

- `StateGraph`: 定义状态结构和节点
- `add_node()`: 添加处理节点
- `add_edge()`: 添加确定性边
- `compile()`: 编译为可执行图

---

### 架构 2: Supervisor 路由模式

_(详细代码见 lesson.md)_

**核心概念**:

- `add_conditional_edges()`: 动态路由
- `ToolNode`: 将工具包装为节点
- 循环工作流: `should_continue` 判断

---

### 架构 3: Human-in-the-Loop

_(详细代码见 lesson.md)_

**核心概念**:

- `interrupt_before=[...]`: 在指定节点前中断
- `MemorySaver`: 内存检查点保存器
- `graph.invoke(..., config)`: 使用线程 ID 恢复状态

---

## 🚀 快速开始

### 环境准备

_(详细代码见 lesson.md)_

---

## 📝 课程内容

### 示例 1: 基础 Agent 节点 (`examples/basic_agent_node_01.py`)

**学习重点**:

- LangGraph 状态定义（TypedDict + Annotated）
- 添加节点和边
- 编译和执行图

**运行输出**:

```
🤖 Agent 思考中...
✅ 任务完成: [Agent 回复内容]
📊 最终状态: {...}
```

---

### 示例 2: Supervisor 路由 (`examples/supervisor_router_02.py`)

**学习重点**:

- 条件边（Conditional Edges）
- 动态路由到不同 Agent
- 循环工作流（直到任务完成）

**运行输出**:

_(详细代码见 lesson.md)_

---

### 示例 3: Human-in-the-Loop (`examples/human_in_the_loop_03.py`)

**学习重点**:

- 在关键节点中断执行
- 等待人类输入
- 恢复执行并继续工作流

**运行输出**:

_(详细代码见 lesson.md)_

---

## 🏋️ 练习题

### 练习: 研究员 + 审稿人双 Agent 写作流

**需求**:
实现一个学术写作助手，包含两个 Agent：

1. **Researcher Agent**: 根据主题生成初稿
2. **Reviewer Agent**: 审核初稿，提出修改建议

**工作流**:

```
START → researcher → reviewer → [判断] → researcher (修改) 或 END
                                   ↑            ↓
                                   └────────────┘
                                  (最多迭代 3 次)
```

**要求**:

- 使用 Supervisor 模式协调两个 Agent
- 实现迭代修改机制（最多 3 轮）
- 在最终提交前引入 Human-in-the-Loop

**文件位置**:

- 练习模板: `exercises/research_writing_flow.py`
- 参考答案: `solutions/research_writing_flow.py`

---

## 📖 延伸阅读

### 官方文档

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [Multi-Agent 设计模式](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [Human-in-the-Loop 指南](https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/)

### 相关课程

- **L57: RAG 向量数据库** - 为 Agent 提供知识检索能力
- **L54: Agent 基础** - 单 Agent 系统的构建
- **L65: SSE 流式响应** - 实时反馈用户

---

## 💡 核心知识点摘要

### 第一章: 多智能体协作模式

单 Agent 能力有限，多 Agent 分工协作解决复杂任务。
Manager-Worker、Pipeline、Debate 等编排模式适合不同场景。
课程展示如何设计 Agent 间通信协议、任务分配策略、冲突解决机制。

### 第二章: LangGraph 多智能体实现

LangGraph 的状态图模型天然支持多 Agent 编排。
条件路由、并行执行、循环反馈实现复杂交互流程。
课程实战多 Agent 系统，每个 Agent 专注单一职责，通过状态共享协作。

### 第三章: 生产级编排优化

超时控制、失败重试、优先级调度保证系统稳定性。
Agent 池管理、负载均衡、动态扩缩容应对高并发。
课程展示如何构建支持百级并发的多 Agent 系统，处理各种异常场景。

### 最佳实践总结

本课最后的总结章节把教程内容收敛成可执行清单。学习时不要只复制示例代码，要把清单转化为自己的检查流程：输入是什么、输出是什么、失败时如何定位。

### 练习题定位

练习题用于把概念转成工程能力。建议先独立完成 `exercises/`，再对照 `solutions/` 检查边界处理、类型注解、错误信息和测试覆盖。

---

## 📁 文件导航

| 目录       | 说明     |
| ---------- | -------- |
| examples/  | 示例代码 |
| exercises/ | 练习题   |
| solutions/ | 参考答案 |
| tests/     | 单元测试 |

---

## ✅ 完成标准

- [ ] 完成所有练习题
- [ ] 通过全部测试：`pytest tests/ -v`

---

## 🔗 下一步

完成本课后继续学习：

- [L62: LangGraph 高级模式与生产部署](../L62-langgraph-server/README.md)
- L62 会学习 LangGraph 的高级模式与生产部署最佳实践。
