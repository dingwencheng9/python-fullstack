# L63: Agent 评估与调试

> **课程编号**: L63
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L61 多智能体编排, L62 LangGraph 服务端
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L61**: 多智能体编排（理解 Agent 协作与状态管理）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 6 AI Agent 系统 - 质量保证与性能优化  
> **前置要求**: L52-L65 Agent 完整体系  
> **后续课程**: L64 部署与监控  
> **学习时长**: 3-4 小时

---

---

## 📚 目录

- [第一章：评估指标体系](#第一章评估指标体系)
- [第二章：调试技术](#第二章调试技术)
- [第三章：性能优化](#第三章性能优化)
- [第四章：自动化测试](#第四章自动化测试)

---

## 第一章：评估指标体系

### 1.1 任务成功率

```python
from dataclasses import dataclass
from typing import List
import time

@dataclass
class TaskResult:
    task_id: str
    success: bool
    latency: float
    tokens_used: int
    error: str | None = None

class AgentEvaluator:
    def __init__(self):
        self.results: List[TaskResult] = []

    def evaluate_task(self, task: str, expected_output: str) -> TaskResult:
        """评估单个任务"""
        start_time = time.time()

        try:
            output = agent.run(task)
            success = self.check_success(output, expected_output)
            tokens = count_tokens(output)

            result = TaskResult(
                task_id=str(uuid.uuid4()),
                success=success,
                latency=time.time() - start_time,
                tokens_used=tokens,
                error=None
            )
        except Exception as e:
            result = TaskResult(
                task_id=str(uuid.uuid4()),
                success=False,
                latency=time.time() - start_time,
                tokens_used=0,
                error=str(e)
            )

        self.results.append(result)
        return result

    def get_metrics(self) -> dict:
        """计算整体指标"""
        total = len(self.results)
        if total == 0:
            return {}

        successful = sum(1 for r in self.results if r.success)

        return {
            "success_rate": successful / total,
            "avg_latency": sum(r.latency for r in self.results) / total,
            "total_tokens": sum(r.tokens_used for r in self.results),
            "error_rate": sum(1 for r in self.results if r.error) / total
        }
```python
---

### 1.2 LLM-as-Judge 评估

```python
from langchain_openai import ChatOpenAI

class LLMJudge:
    def __init__(self):
        self.judge_llm = ChatOpenAI(model="gpt-4o")

    def evaluate_quality(self, task: str, output: str) -> dict:
        """使用 LLM 作为评判"""
        prompt = f"""
任务: {task}
Agent输出: {output}

请从以下维度评分 (0-10分):
1. 准确性 (是否正确回答问题)
2. 完整性 (是否覆盖所有要点)
3. 清晰度 (表达是否清晰)
4. 相关性 (是否紧扣主题)

输出JSON格式:
{{
    "accuracy": 0-10,
    "completeness": 0-10,
    "clarity": 0-10,
    "relevance": 0-10,
    "reasoning": "评分理由"
}}
"""

        response = self.judge_llm.invoke(prompt)
        scores = json.loads(response.content)

        # 计算总分
        scores["total"] = sum([
            scores["accuracy"],
            scores["completeness"],
            scores["clarity"],
            scores["relevance"]
        ]) / 4

        return scores
```python
---

### 1.3 成本效益分析

```python
class CostAnalyzer:
    # OpenAI 价格 (2026-06)
    PRICES = {
        "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000}
    }

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """计算单次调用成本"""
        price = self.PRICES[model]
        cost = (input_tokens * price["input"]) + (output_tokens * price["output"])
        return cost

    def analyze_agent_cost(self, results: List[TaskResult]) -> dict:
        """分析 Agent 成本"""
        total_cost = sum(
            self.calculate_cost(r.model, r.input_tokens, r.output_tokens)
            for r in results
        )

        avg_cost = total_cost / len(results) if results else 0

        return {
            "total_cost": round(total_cost, 4),
            "avg_cost_per_task": round(avg_cost, 4),
            "cost_per_success": round(
                total_cost / sum(1 for r in results if r.success), 4
            ) if any(r.success for r in results) else 0
        }
```python
---

## 第二章：调试技术

### 2.1 LangSmith 追踪

```python
import os
from langsmith import Client

# 启用 LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "agent-debugging"

# 运行 Agent (自动追踪)
result = agent.run("你的任务")

# 查看追踪: https://smith.langchain.com
```python
**LangSmith 提供**:

- 完整调用链可视化
- Token 使用统计
- 延迟分析
- 错误追踪

---

### 2.2 自定义 Callbacks

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any

class DebugCallbackHandler(BaseCallbackHandler):
    """调试回调"""

    def on_llm_start(self, serialized: dict, prompts: list[str], **kwargs):
        """LLM 开始调用"""
        print(f"🤖 LLM Start: {serialized.get('name')}")
        print(f"📝 Prompt: {prompts[0][:100]}...")

    def on_llm_end(self, response, **kwargs):
        """LLM 结束调用"""
        print(f"✅ LLM End: {response.generations[0][0].text[:100]}...")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        """工具开始调用"""
        print(f"🔧 Tool Start: {serialized.get('name')}")
        print(f"📥 Input: {input_str}")

    def on_tool_end(self, output: str, **kwargs):
        """工具结束调用"""
        print(f"✅ Tool End: {output[:100]}...")

    def on_agent_action(self, action, **kwargs):
        """Agent 采取行动"""
        print(f"🎯 Action: {action.tool} - {action.tool_input}")

    def on_agent_finish(self, finish, **kwargs):
        """Agent 完成"""
        print(f"🏁 Finish: {finish.return_values}")

# 使用
agent = create_agent(llm, tools, callbacks=[DebugCallbackHandler()])
```python
---

### 2.3 日志追踪

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"agent_{datetime.now():%Y%m%d}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AgentSystem")

class LoggingAgent:
    def run(self, task: str):
        logger.info(f"Task received: {task}")

        try:
            result = self._execute(task)
            logger.info(f"Task completed: {result[:100]}")
            return result
        except Exception as e:
            logger.error(f"Task failed: {str(e)}", exc_info=True)
            raise

    def _execute(self, task: str):
        logger.debug(f"Executing task: {task}")
        # 执行逻辑...
        return result
```python
---

## 第三章：性能优化

### 3.1 Profiling (性能分析)

```python
import cProfile
import pstats
from io import StringIO

def profile_agent(task: str):
    """性能分析"""
    profiler = cProfile.Profile()
    profiler.enable()

    # 运行 Agent
    result = agent.run(task)

    profiler.disable()

    # 输出统计
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # 前 20 个最慢函数

    print(stream.getvalue())
    return result

# 使用
profile_agent("复杂任务")
```python
---

### 3.2 Prompt 优化

```python
class PromptOptimizer:
    def __init__(self):
        self.test_cases = [
            ("任务1", "期望输出1"),
            ("任务2", "期望输出2"),
            # ...
        ]

    def compare_prompts(self, prompt_v1: str, prompt_v2: str) -> dict:
        """对比两个 Prompt 版本"""
        results = {"v1": [], "v2": []}

        for task, expected in self.test_cases:
            # 测试 v1
            output_v1 = llm.invoke(prompt_v1.format(task=task))
            score_v1 = self.evaluate(output_v1, expected)
            results["v1"].append(score_v1)

            # 测试 v2
            output_v2 = llm.invoke(prompt_v2.format(task=task))
            score_v2 = self.evaluate(output_v2, expected)
            results["v2"].append(score_v2)

        return {
            "v1_avg": sum(results["v1"]) / len(results["v1"]),
            "v2_avg": sum(results["v2"]) / len(results["v2"]),
            "improvement": (sum(results["v2"]) - sum(results["v1"])) / len(results["v1"])
        }
```python
---

### 3.3 Token 优化

```python
def optimize_context(messages: list, max_tokens: int = 4000) -> list:
    """优化上下文 Token 数"""

    # 策略 1: 删除冗余消息
    messages = remove_duplicate_messages(messages)

    # 策略 2: 摘要旧消息
    if count_tokens(messages) > max_tokens:
        old_messages = messages[:len(messages)//2]
        summary = summarize_messages(old_messages)
        messages = [summary] + messages[len(messages)//2:]

    # 策略 3: 压缩 Prompt
    messages = [compress_message(m) for m in messages]

    return messages

def compress_message(message: str) -> str:
    """压缩单条消息"""
    # 移除多余空格
    message = " ".join(message.split())

    # 移除冗余标点
    message = message.replace("...", ".")

    # 使用缩写
    replacements = {
        "你好，我是": "你好",
        "非常感谢": "谢谢",
        # ...
    }
    for old, new in replacements.items():
        message = message.replace(old, new)

    return message
```python
---

## 第四章：自动化测试

### 4.1 单元测试

```python
import pytest
from unittest.mock import Mock

def test_agent_tool_selection():
    """测试工具选择逻辑"""
    agent = create_test_agent()

    # Mock LLM 响应
    agent.llm = Mock(return_value=AIMessage(
        content="",
        tool_calls=[{"name": "search", "args": {"query": "test"}}]
    ))

    result = agent.run("搜索测试")

    assert "search" in result.tool_calls
    assert result.tool_calls[0]["args"]["query"] == "test"

def test_memory_retention():
    """测试记忆保持"""
    agent = create_agent_with_memory()

    agent.run("我叫小明")
    result = agent.run("我叫什么？")

    assert "小明" in result
```python
---

### 4.2 集成测试

```python
@pytest.fixture
def test_agent():
    """测试 Agent 固件"""
    return create_agent(
        llm=ChatOpenAI(model="gpt-4o-mini"),
        tools=[search_tool, calculator_tool]
    )

def test_multi_step_task(test_agent):
    """测试多步骤任务"""
    task = "搜索北京天气，然后计算温度华氏度"
    result = test_agent.run(task)

    # 验证
    assert "°F" in result
    assert test_agent.tool_call_count == 2  # 调用了2个工具
```python
---

### 4.3 端到端测试

```python
def test_end_to_end_workflow():
    """端到端测试"""
    # 准备环境
    db = setup_test_database()
    agent = create_production_agent()

    # 执行完整流程
    result = agent.run("创建用户并发送欢迎邮件")

    # 验证结果
    user = db.query("SELECT * FROM users WHERE name='test'")
    assert user is not None

    emails = db.query("SELECT * FROM emails WHERE user_id=?", user.id)
    assert len(emails) == 1
    assert "欢迎" in emails[0].content

    # 清理
    teardown_test_database(db)
```

---

## 🎯 最佳实践总结

### ✅ 评估检查清单

- [ ] 定义清晰的成功标准
- [ ] 准备多样化测试用例
- [ ] 使用 LLM-as-Judge 评估质量
- [ ] 追踪 Token 和成本
- [ ] 监控响应时间
- [ ] 设置性能基线
- [ ] 定期回归测试

### 评估维度权重

| 维度     | 权重 | 说明         |
| -------- | ---- | ------------ |
| 准确性   | 40%  | 最重要       |
| 效率     | 25%  | Token + 时间 |
| 鲁棒性   | 20%  | 错误处理     |
| 用户体验 | 15%  | 清晰度       |

---

## 🔗 延伸阅读

### 相关课程

- **L54 Agent 基础** - Agent 核心
- **L60 规划与推理** - 提升准确性
- **L64 部署与监控** - 生产化

### 推荐资源

- [LangSmith 文档](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Agent Evaluation Best Practices](https://arxiv.org/abs/2401.01863)

---

## 📝 练习题

### 练习 1: 评估框架

实现 Agent 评估框架:

- 成功率计算
- Token 统计
- 延迟分析

### 练习 2: LLM-as-Judge

实现质量评估:

- 多维度评分
- 理由生成
- 批量评估

### 练习 3: 性能优化

识别并优化瓶颈:

- Profiling 分析
- Prompt 优化
- Token 压缩

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L64 Agent 部署与监控](../L64-agent-deployment/lesson.md)

## 🔗 下一步


[L64: Agent 部署与监控](../L64-agent-deployment/)
