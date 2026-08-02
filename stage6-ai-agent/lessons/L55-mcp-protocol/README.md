# L55: MCP 协议入门

> **课程编号**: L55
> **所属阶段**: Stage 6 - AI Agent 开发  
> **预计时长**: 6 小时  
> **难度**: ⭐⭐⭐⭐ (中高级)

---

MCP（Model Context Protocol）是 **Anthropic 推出的 AI Agent 与外部工具/资源连接的标准协议**。

> 💡 **为什么 MCP 很重要**：
>
> - 它让 Agent 工具可以**跨 LLM 复用**（不再绑死 OpenAI / Claude / Gemini）
> - Claude Desktop 已原生支持，未来 ChatGPT 也会跟进
> - 写一个 MCP Server = 给所有 LLM 加上能力

## 📌 课程结构

**第一部分：协议思想**

- 用纯 Python 模拟 MCP 角色
- 理解 Host/Server/Client/Tool 边界
- 示例：`examples/tool_server.py`, `examples/tool_client.py`

**第二部分：SDK 实战** ✅ 生产推荐

- 使用 `mcp` Python SDK
- FastMCP server 开发
- ClientSession 调用
- 示例：`examples/04_mcp_sdk_server.py`, `examples/05_mcp_sdk_client.py`

---

## 📚 课程概览

- **位置**: Stage 5 / 第 9 课
- **学习时长**: 4 小时
- **难度**: ⭐⭐⭐⭐
- **前置课程**: L59 Agent 部署与监控
- **后续课程**: Stage 5 完结
- **课程主题**: Model Context Protocol (MCP) 标准化 Agent 工具集成

本 README 是课程入口地图。详细概念、代码讲解和练习说明以 `lesson.md` 为准；这里帮助你快速判断学习顺序、运行路径和完成标准。

---

## 🎯 学习目标

1. ✅ 理解 Tool Calling（OpenAI 风格）与 MCP（标准协议）的差异
2. ✅ 掌握 MCP 五大角色：Host / Client / Server / Tool / Resource
3. ✅ 实现一个极简本地 MCP Server（暴露 1-2 个 Tool）
4. ✅ 编写 Agent 调用 MCP Tool 的桥接层
5. ✅ 理解 MCP 的权限、安全、版本兼容边界
6. ✅ 知道如何把自己的 MCP Server 接入 Claude Desktop

---

## 📋 前置知识

- [L53: Agent 基础与工具调用](../L54-agent-basics/) — Tool Calling
- [L54: LangGraph](../L58-langgraph-adv/) — Agent 工作流
- [L61: 多智能体编排](../L61-multi-agent/) — Agent 协作模式
- 基础 JSON-RPC 概念

---

## 💡 核心知识点摘要

### 第一章: MCP 协议基础

MCP 是 Anthropic 提出的标准化 Agent 工具协议。
统一的接口规范让工具可跨 Agent 框架复用，降低集成成本。
课程详解 MCP 的 JSON-RPC 通信、工具注册、参数验证、错误处理机制。

### 第二章: MCP Server 实现

MCP Server 暴露工具集，Client 通过协议调用。
@mcp.tool 装饰器声明工具，自动生成 schema 和文档。
课程实战构建文件搜索、数据库查询、API 调用等生产级 MCP 工具。

### 第三章: Agent 工具集成

LangChain/LlamaIndex 原生支持 MCP，零代码集成工具。
动态工具发现、权限控制、审计日志保证安全性。
课程展示如何用 MCP 快速扩展 Agent 能力，构建可插拔的工具生态。

### 最佳实践总结

本课最后的总结章节把教程内容收敛成可执行清单。学习时不要只复制示例代码，要把清单转化为自己的检查流程：输入是什么、输出是什么、失败时如何定位。

### 练习题定位

练习题用于把概念转成工程能力。建议先独立完成 `exercises/`，再对照 `solutions/` 检查边界处理、类型注解、错误信息和测试覆盖。

---

## 📁 文件导航

| 文件                            | 说明                                 |
| ------------------------------- | ------------------------------------ |
| `examples/tool_server.py`       | 协议思想：极简 MCP Server 模拟       |
| `examples/tool_client.py`       | 协议思想：Client 调用 Server         |
| `examples/agent_tool_bridge.py` | Agent 调用 MCP Tool 的桥接层         |
| `examples/04_mcp_sdk_server.py` | SDK 实战：FastMCP server ✅ 推荐     |
| `examples/05_mcp_sdk_client.py` | SDK 实战：ClientSession 调用 ✅ 推荐 |
| `exercises/`                    | 写一个文件搜索 Tool / 加权限校验     |
| `solutions/`                    | 参考答案                             |
| `tests/`                        | 单元测试                             |

## 依赖

```bash
uv add mcp
```

---

## 🚀 快速开始

```bash
# 跑示例 Server
PYTHONPATH=. uv run python stage6-ai-agent/lessons/L55-mcp-protocol/examples/tool_server.py

# 跑测试
PYTHONPATH=. uv run pytest stage6-ai-agent/lessons/L55-mcp-protocol/tests/ --no-cov -v
```

要接入 Claude Desktop 实战，参考[官方 SDK](https://modelcontextprotocol.io/)。

---

## 📚 核心概念

### MCP 五大角色

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│     Host     │  ──→    │    Client    │  ──→    │    Server    │
│ (Claude Desktop)        │ (内部连接器)  │  (你写的)│
│  / VS Code)  │  ←──    │              │  ←──    │              │
└──────────────┘         └──────────────┘         └──────────────┘
                                                          │
                                                  Tools / Resources / Prompts
```

| 角色         | 说明                                                |
| ------------ | --------------------------------------------------- |
| **Host**     | 承载用户交互的应用（Claude Desktop / VS Code 插件） |
| **Client**   | Host 内部的 MCP 协议层（一般你不用关心）            |
| **Server**   | **你写的**，暴露 Tools/Resources/Prompts            |
| **Tool**     | 可执行动作（查天气、发邮件、搜文件）                |
| **Resource** | 可读取的上下文（文件内容、数据库行）                |
| **Prompt**   | 预设的提示词模板                                    |

### MCP vs OpenAI Tool Calling

| 维度         | OpenAI Tool Calling | MCP                  |
| ------------ | ------------------- | -------------------- |
| 标准化       | OpenAI 私有格式     | 跨 LLM 标准          |
| 工具定义位置 | Prompt 里           | 独立 Server 进程     |
| 复用         | 绑死 OpenAI         | 任何支持 MCP 的 Host |
| 部署         | 跟 LLM 调用一起     | 独立进程，可复用     |
| 适合         | 单次调用、简单工具  | 长期工具集、跨场景   |

---

## 🚨 常见难点

| 难点                       | 表现                       | 解决                       |
| -------------------------- | -------------------------- | -------------------------- |
| Server 进程不能 print 调试 | 输出污染 stdio 协议        | 用 stderr 或 logging       |
| JSON Schema 写错           | Claude 看不到工具          | 用 Pydantic + 严格类型     |
| 工具调用结果太大           | LLM context 爆掉           | 分块返回 + Resource 引用   |
| 权限不当                   | Tool 误删用户文件          | 永远在 Tool 内做白名单校验 |
| 版本兼容                   | 协议升级后旧 Server 跑不动 | 看 MCP 协议版本号          |

---

## ✅ 完成标准

- [ ] 能解释 Tool Calling 与 MCP 的根本差异（标准 vs 私有）
- [ ] 能用纯 Python 实现一个最小 MCP Server（≥ 2 个 Tool）
- [ ] 能为工具增加输入校验 + 权限边界
- [ ] 知道如何把 Server 配置到 Claude Desktop（理论即可）
- [ ] 通过全部 pytest 测试

---

## 💼 接单价值

MCP 是 2025-2026 的**新蓝海**：

- 给企业内部系统写 MCP Server，让员工用 Claude Desktop 直接查询
- 单价 ¥10000-30000/项目（替代传统的"AI 助手定制"）
- 这块还没多少人会，**早入场早吃肉**

---

## 🔗 Stage 5 已完成

L60 是课程主线最后一节。下一步：

- 综合作品：[项目 2 - AI Fullstack Capstone](../../../projects/02-ai-fullstack-capstone/) 实战
- 兼职变现：[`extensions/freelance-toolkit/`](../../../extensions/freelance-toolkit/) 自由职业工具包
- 求职准备：[`extensions/multimodal-agent/`](../../../extensions/multimodal-agent/) AI 工程师技能树
- 选修方向：[`extensions/`](../../../extensions/) 选 1 个职业方向继续深耕

🎉 恭喜完成 60 节课程！
