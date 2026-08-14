L54: Agent 基础与工具调用 - 详细教程

> **课程编号**: L54
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐（AI Agent 专家级）
> **前置课程**: 无（Stage 6 入口）
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

## 📚 前置知识

**本课程无前置要求，可直接学习。**

---

> **课程定位**: Stage 6 AI Agent 系统 - 从 LLM 到自主 Agent
> **后续课程**: L55 MCP 协议（理解标准化工具集成）  
> **学习时长**: 4-5 小时

---

---

## 📚 目录

- [第一章：Agent 核心概念](#第一章agent-核心概念)
- [第二章：工具系统设计](#第二章工具系统设计)
- [第三章：ReAct Agent 实现](#第三章react-agent-实现)
- [第四章：生产化实践](#第四章生产化实践)

---

## 第一章：Agent 核心概念

### 1.1 什么是 Agent？

**Agent = LLM + Tools + Memory + Planning**

```yaml
用户输入
   ↓
Agent 循环:
1. 思考 (Thought): LLM 分析任务
2. 行动 (Action): 选择工具执行
3. 观察 (Observation): 获取工具结果
   ↓
重复直到任务完成
   ↓
最终答案
```python
---

### 1.2 ReAct 模式

**ReAct = Reasoning + Acting**

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# ReAct Prompt 模板
react_prompt = PromptTemplate.from_template("""
你是一个助手，可以使用以下工具：

{tools}

使用这种格式：

Question: 用户问题
Thought: 思考需要做什么
Action: 工具名称
Action Input: 工具输入
Observation: 工具输出
... (重复思考/行动/观察)
Thought: 我现在知道最终答案
Final Answer: 最终答案

开始！

Question: {input}
{agent_scratchpad}
""")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_react_agent(llm, tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```text
---

### 1.3 Agent 执行流程

```python
# Agent 执行示例
result = executor.invoke({"input": "北京的天气如何？明天的气温是多少？"})

# 内部执行流程:
# 1. Thought: 需要查询天气信息
# 2. Action: weather_tool
# 3. Action Input: {"city": "北京", "date": "今天"}
# 4. Observation: 今天晴天，20°C
# 5. Thought: 还需要查询明天的气温
# 6. Action: weather_tool
# 7. Action Input: {"city": "北京", "date": "明天"}
# 8. Observation: 明天多云，18°C
# 9. Thought: 我现在知道答案了
# 10. Final Answer: 北京今天晴天20°C，明天多云18°C
```python
---

## 第二章：工具系统设计

### 2.1 使用 @tool 装饰器

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """
    搜索工具：在网络上搜索信息

    Args:
        query: 搜索查询词

    Returns:
        搜索结果摘要
    """
    # 模拟搜索
    return f"关于 '{query}' 的搜索结果..."

@tool
def calculator(expression: str) -> str:
    """
    计算器工具：计算数学表达式

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"

    Returns:
        计算结果
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"
```python
**关键点**:

- ✅ 函数名 = 工具名
- ✅ Docstring 第一行 = 工具描述 (LLM 看到的)
- ✅ 类型注解必填 (Args/Returns)

---

### 2.2 StructuredTool (复杂参数)

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# 定义参数结构
class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")
    date: str = Field(description="日期，如 '今天' 或 '明天'")

def get_weather(city: str, date: str) -> str:
    """查询天气信息"""
    return f"{city} {date}的天气: 晴天，20°C"

# 创建结构化工具
weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="weather",
    description="查询指定城市和日期的天气",
    args_schema=WeatherInput
)
```python
---

### 2.3 Instructor: 结构化输出的工业级方案

**Instructor** 是基于 Pydantic 的结构化输出库，提供自动重试、验证失败重试循环，是 Agent 稳定性的核心保障。

```python
# 安装: uv add instructor

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

# 1. 定义输出结构
class WeatherResponse(BaseModel):
    city: str = Field(description="城市名称")
    date: str = Field(description="查询日期")
    weather: str = Field(description="天气状况")
    temperature: int = Field(description="温度（摄氏度）")
    humidity: int = Field(description="湿度（百分比）", default=50)

# 2. 启用 Instructor
client = instructor.patch(OpenAI(), mode=instructor.Mode.TOOLS)

# 3. 提取结构化数据（自动重试直到成功）
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个天气信息提取助手"},
        {"role": "user", "content": "北京今天天气晴朗，温度25度，湿度40%。"}
    ],
    response_model=WeatherResponse,
)

print(response.model_dump())
# WeatherResponse(city='北京', date='今天', weather='晴朗', temperature=25, humidity=40)
```

### 2.4 Instructor + Tool Calling 集成

```python
import instructor
from pydantic import BaseModel, Field
from typing import Literal
from openai import OpenAI

# 定义工具输出的数据模型
class SearchResult(BaseModel):
    title: str = Field(description="搜索结果标题")
    url: str = Field(description="网页链接")
    snippet: str = Field(description="内容摘要")

class WeatherInfo(BaseModel):
    city: str
    temperature: int
    condition: str

# 联合模式：自动选择正确的输出模型
class AgentResponse(BaseModel):
    decision: Literal["search", "weather", "general"] = Field(
        description="决策：search=搜索，weather=查天气，general=直接回答"
    )
    search_result: SearchResult | None = None
    weather_info: WeatherInfo | None = None
    answer: str | None = None

client = instructor.patch(OpenAI(), mode=instructor.Mode.TOOLS)

def agent_with_structured_output(user_query: str) -> AgentResponse:
    """带结构化输出的 Agent"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "分析用户查询，选择合适的行动"},
            {"role": "user", "content": user_query}
        ],
        response_model=AgentResponse,
        max_retries=3  # 自动重试直到验证通过
    )
    return response

# 使用
result = agent_with_structured_output("北京天气怎么样？")
if result.weather_info:
    print(f"{result.weather_info.city}: {result.weather_info.temperature}°C")
```

### 2.5 验证失败重试循环

Instructor 的核心价值：**当 LLM 返回不符合 Schema 时，自动重试直到成功**。

```python
from instructor.errors import ModelError
import time

def agent_with_retry(prompt: str, max_attempts: int = 5):
    """带重试循环的 Agent"""
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_model=AgentResponse,
            )
            return response  # 验证通过，返回结果

        except ModelError as e:
            # 验证失败，记录并重试
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_attempts - 1:
                raise RuntimeError(f"Max retries ({max_attempts}) exceeded")
            time.sleep(0.5 * (attempt + 1))  # 指数退避

# 典型错误场景：
# - LLM 返回 "25度" 而非数字 25
# - LLM 返回 "北京" 而非有效城市代码
# - LLM 遗漏必需字段
```

**Instructor vs 原生 StructuredTool**:

| 特性 | StructuredTool | Instructor |
|------|-----------------|------------|
| 自动重试 | ❌ 需手动实现 | ✅ 内置 |
| Schema 验证 | ✅ | ✅ |
| Pydantic v2 支持 | ✅ | ✅ |
| Tool Calling 集成 | 基础 | 高级（联合模式） |
| 错误恢复 | 需手动 | 自动重试循环 |
| 生产稳定性 | 一般 | **极高** |

---

### 2.6 工具最佳实践

```python
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    发送邮件工具

    Args:
        to: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文

    Returns:
        发送状态
    """
    # ✅ 输入验证
    if "@" not in to:
        return "错误: 邮箱格式不正确"

    # ✅ 日志记录
    print(f"[Tool] 发送邮件到 {to}")

    # ✅ 错误处理
    try:
        # 实际发送逻辑
        return f"✅ 邮件已发送到 {to}"
    except Exception as e:
        return f"❌ 发送失败: {e}"
```python
**工具设计原则**:

- ✅ 单一职责 (一个工具做一件事)
- ✅ 清晰描述 (LLM 能理解何时使用)
- ✅ 输入验证 (防止非法输入)
- ✅ 错误处理 (返回友好错误信息)

---

## 第三章：ReAct Agent 实现

### 3.1 基础 Agent

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain import hub

# 1. 定义工具
tools = [search, calculator, weather_tool]

# 2. 加载 ReAct Prompt
prompt = hub.pull("hwchase17/react")

# 3. 创建 LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 4. 创建 Agent
agent = create_react_agent(llm, tools, prompt)

# 5. 创建执行器
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,           # 显示思考过程
    max_iterations=10,      # 最大迭代次数
    handle_parsing_errors=True  # 处理解析错误
)

# 6. 执行
result = executor.invoke({"input": "搜索 Python 3.13 新特性，并总结"})
print(result["output"])
```python
---

### 3.2 OpenAI Functions Agent (推荐)

```python
from langchain.agents import create_openai_functions_agent

# OpenAI Functions 原生支持
agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = executor.invoke({"input": "计算 (25 + 17) * 3"})
```python
**优势**:

- ✅ 原生函数调用 (更准确)
- ✅ 更快的响应速度
- ✅ 更好的工具选择

---

### 3.3 Agent 输出详解

```python
result = executor.invoke({"input": "北京天气如何？"})

# 完整输出
print(result)
# {
#     "input": "北京天气如何？",
#     "output": "北京今天晴天，20°C",
#     "intermediate_steps": [
#         (AgentAction(tool="weather", tool_input="北京 今天"), "晴天，20°C")
#     ]
# }

# 仅获取最终答案
print(result["output"])

# 获取执行步骤
for action, observation in result["intermediate_steps"]:
    print(f"工具: {action.tool}")
    print(f"输入: {action.tool_input}")
    print(f"输出: {observation}")
```python
---

## 第四章：生产化实践

### 4.1 异步 Agent

```python
import asyncio

# 异步执行
async def run_agent():
    result = await executor.ainvoke({"input": "查询天气"})
    return result

result = asyncio.run(run_agent())
```python
---

### 4.2 流式输出

```python
# 流式执行 (实时显示思考过程)
for chunk in executor.stream({"input": "搜索 LangChain 教程"}):
    if "output" in chunk:
        print(chunk["output"], end="", flush=True)
```python
---

### 4.3 自定义回调

```python
from langchain.callbacks import StdOutCallbackHandler

class CustomCallback(StdOutCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n🔧 调用工具: {serialized['name']}")
        print(f"📥 输入: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"📤 输出: {output}\n")

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[CustomCallback()],
    verbose=False  # 使用自定义回调
)
```python
---

### 4.4 错误处理与重试

```python
from langchain.agents import AgentExecutor

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=15,              # 最大迭代
    max_execution_time=60,          # 最大执行时间 (秒)
    early_stopping_method="generate",  # 提前停止策略
    handle_parsing_errors=True,     # 解析错误处理
    return_intermediate_steps=True  # 返回中间步骤
)

try:
    result = executor.invoke({"input": "复杂任务"})
except Exception as e:
    print(f"Agent 执行失败: {e}")
```python
---

### 4.5 Token 追踪

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = executor.invoke({"input": "查询信息并总结"})

    print(f"总 Token: {cb.total_tokens}")
    print(f"提示 Token: {cb.prompt_tokens}")
    print(f"完成 Token: {cb.completion_tokens}")
    print(f"总成本: ${cb.total_cost:.4f}")
```text
---

## 第五章：Agent 性能优化

### 5.1 缓存优化

```python
from functools import lru_cache
from typing import Optional

class CachedAgent:
    """带缓存的 Agent"""

    def __init__(self, agent):
        self.agent = agent
        self._cache = {}

    async def run_with_cache(self, query: str, session_id: str) -> str:
        """带缓存的执行"""
        cache_key = f"{session_id}:{query}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = await self.agent.arun(query, session_id=session_id)
        self._cache[cache_key] = result
        return result

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
```

### 5.2 并行工具调用

```python
import asyncio

async def parallel_tool_execution(tools: list[callable], args: list[dict]) -> list:
    """并行执行多个工具"""
    tasks = [tool(**arg) for tool, arg in zip(tools, args)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# 使用
results = await parallel_tool_execution(
    [search_tool, weather_tool, news_tool],
    [{"query": "Python"}, {"city": "北京"}, {"topic": "AI"}]
)
```

### 5.3 批处理优化

```python
class BatchAgent:
    """批处理 Agent"""

    def __init__(self, agent, batch_size: int = 5):
        self.agent = agent
        self.batch_size = batch_size

    async def process_batch(self, queries: list[str]) -> list[str]:
        """批量处理查询"""
        results = []
        for i in range(0, len(queries), self.batch_size):
            batch = queries[i:i + self.batch_size]
            batch_results = await asyncio.gather(
                *[self.agent.arun(q) for q in batch]
            )
            results.extend(batch_results)
        return results
```

### 5.4 工具超时控制

```python
import asyncio

async def tool_with_timeout(tool: callable, timeout: float = 30.0, **kwargs):
    """带超时的工具调用"""
    try:
        return await asyncio.wait_for(tool(**kwargs), timeout=timeout)
    except asyncio.TimeoutError:
        return {"error": f"工具执行超时 ({timeout}s)"}

# 使用
result = await tool_with_timeout(
    slow_tool,
    timeout=10.0,
    param="value"
)
```

---

## 🎯 最佳实践总结

### ✅ Agent 开发清单

- [ ] 工具描述清晰简洁
- [ ] 输入参数类型注解完整
- [ ] 工具执行时间 < 10 秒
- [ ] 错误信息对 LLM 友好
- [ ] 设置合理的 max_iterations
- [ ] 使用 verbose=True 调试
- [ ] 异步执行长时间任务

### Agent 设计模式

**模式 1: 单工具 Agent**

```text
简单查询 → 单一工具 → 返回结果
```python
**模式 2: 多步推理 Agent**

```text
复杂任务 → 工具1 → 工具2 → 综合结果
```python
**模式 3: 路由 Agent**

```text
用户请求 → 分析类型 → 路由到专家 Agent
```

---

## 🔗 延伸阅读

### 相关课程

- **L54 LangChain 基础** - Chain 组合基础
- **L54 LangGraph** - 复杂 Agent 编排
- **L54 Agent 记忆** - 长期记忆管理

### 推荐资源

- [LangChain Agents 文档](https://python.langchain.com/docs/modules/agents/)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

## 📝 练习题

### 练习 1: 天气 Agent

创建天气查询 Agent:

- 工具: 查询当前天气/未来天气
- 支持多城市查询
- 返回结构化结果

### 练习 2: 数学助手 Agent

实现数学工具集:

- 基础计算 (+-\*/)
- 高级函数 (sin/cos/log)
- 方程求解

### 练习 3: 搜索摘要 Agent

组合搜索和总结:

- 搜索关键词
- 提取 Top 3 结果
- 生成综合摘要

---

**练习答案**: 参见 `solutions/` 目录

## 🔗 下一步

完成本课后继续学习：

- [L55: MCP 协议](../L55-mcp-protocol/README.md)

> 📖 **学习路径提示**：L55 将学习 Model Context Protocol 协议。
