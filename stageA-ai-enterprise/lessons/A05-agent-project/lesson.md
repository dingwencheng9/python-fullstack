# A05: Agent 项目实战

> **课程编号**: A05
> **所属阶段**: Stage A - AI Agent 企业级 (Specialization)
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐⭐ (高级)
> **前置课程**: A01, A02, A03, A04
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

完成本课程后，你将能够：

1. **项目架构**：设计完整的 Agent 系统架构
2. **功能实现**：实现端到端的 Agent 功能
3. **测试策略**：编写 Agent 系统的测试
4. **部署运维**：将 Agent 系统部署到生产环境

---

## 📚 课程内容

### 第一部分：项目架构

#### 1.1 系统架构设计

```python
from dataclasses import dataclass, field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    DONE = "done"

@dataclass
class Message:
    """消息"""
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

@dataclass
class AgentState:
    """Agent 状态"""
    messages: list[Message] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    context: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

class AgentSystem:
    """Agent 系统主类"""

    def __init__(
        self,
        name: str,
        system_prompt: str,
        model: str = "gpt-4o-mini"
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.state = AgentState()
        self.plugins: list[dict] = []
        self.middlewares: list[dict] = []

    def add_plugin(self, name: str, handler: callable) -> None:
        """添加插件"""
        self.plugins.append({"name": name, "handler": handler})

    def add_middleware(self, name: str, middleware: callable) -> None:
        """添加中间件"""
        self.middlewares.append({"name": name, "middleware": middleware})

    async def process(self, user_input: str) -> str:
        """处理用户输入"""
        # 1. 输入验证
        if not self._validate_input(user_input):
            raise ValueError("Invalid input")

        # 2. 应用中间件
        processed_input = self._apply_middlewares_input(user_input)

        # 3. 更新状态
        self.state.status = AgentStatus.PROCESSING
        self.state.messages.append(Message("user", processed_input))

        # 4. 执行插件
        plugin_results = await self._execute_plugins(processed_input)

        # 5. 生成响应（实际应调用 LLM API）
        response = await self._generate_response(plugin_results)

        # 6. 应用输出中间件
        response = self._apply_middlewares_output(response)

        # 7. 更新状态
        self.state.messages.append(Message("assistant", response))
        self.state.status = AgentStatus.DONE

        return response

    def _validate_input(self, input: str) -> bool:
        """验证输入"""
        # 基本验证
        if not input or len(input) > 10000:
            return False
        return True

    def _apply_middlewares_input(self, input: str) -> str:
        """应用输入中间件"""
        result = input
        for mw in self.middlewares:
            result = mw["middleware"](result)
        return result

    def _apply_middlewares_output(self, output: str) -> str:
        """应用输出中间件"""
        result = output
        for mw in reversed(self.middlewares):
            if "output_handler" in mw:
                result = mw["output_handler"](result)
        return result

    async def _execute_plugins(self, input: str) -> dict:
        """执行插件"""
        results = {}
        for plugin in self.plugins:
            try:
                results[plugin["name"]] = await plugin["handler"](input)
            except Exception as e:
                results[plugin["name"]] = {"error": str(e)}
        return results

    async def _generate_response(self, context: dict) -> str:
        """生成响应"""
        # 简化实现
        return f"Processed with {len(context)} plugin results"
```

#### 1.2 插件系统

```python
from typing import Protocol, Awaitable

class Plugin(Protocol):
    """插件协议"""
    name: str

    async def execute(self, input: str) -> dict:
        """执行插件"""
        ...

class SearchPlugin:
    """搜索插件"""
    name = "search"

    async def execute(self, input: str) -> dict:
        """执行搜索"""
        # 实际应调用搜索 API
        return {
            "results": [
                {"title": "Result 1", "url": "https://example.com/1"},
                {"title": "Result 2", "url": "https://example.com/2"},
            ]
        }

class CalculatorPlugin:
    """计算器插件"""
    name = "calculator"

    async def execute(self, input: str) -> dict:
        """执行计算"""
        # 简单计算逻辑
        return {"result": 42, "expression": input}
```

---

### 第二部分：功能实现

#### 2.1 工具集成

```python
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: dict
    handler: Callable[..., Awaitable[Any]]

class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """注册工具"""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(name)

    def list_tools(self) -> list[dict]:
        """列出所有工具"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools.values()
        ]

# 使用示例
registry = ToolRegistry()

@registry.register
@ dataclass
class MyTool(Tool):
    pass

async def search_handler(query: str) -> dict:
    return {"results": []}

registry.register(Tool(
    name="search",
    description="Search the web",
    parameters={"query": {"type": "string", "required": True}},
    handler=search_handler
))
```

#### 2.2 记忆系统

```python
from datetime import datetime
from typing import Optional
import json

class Memory:
    """Agent 记忆系统"""

    def __init__(self, max_items: int = 100):
        self.short_term: list[dict] = []
        self.long_term: dict[str, list[dict]] = {}
        self.max_items = max_items

    def add(self, content: str, memory_type: str = "short") -> None:
        """添加记忆"""
        item = {
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        if memory_type == "short":
            self.short_term.append(item)
            # 限制短期记忆长度
            if len(self.short_term) > self.max_items:
                self.short_term.pop(0)
        else:
            key = self._extract_key(content)
            if key not in self.long_term:
                self.long_term[key] = []
            self.long_term[key].append(item)

    def retrieve(self, query: str, limit: int = 5) -> list[dict]:
        """检索记忆"""
        results = []

        # 搜索短期记忆
        for item in self.short_term:
            if query.lower() in item["content"].lower():
                results.append(item)

        # 搜索长期记忆
        for key, items in self.long_term.items():
            if query.lower() in key.lower():
                results.extend(items)

        return results[:limit]

    def _extract_key(self, content: str) -> str:
        """提取键"""
        # 简单实现：取前 50 个字符
        return content[:50]

    def clear(self, memory_type: str = "short") -> None:
        """清除记忆"""
        if memory_type == "short":
            self.short_term.clear()
        else:
            self.long_term.clear()

    def export(self) -> str:
        """导出记忆"""
        return json.dumps({
            "short_term": self.short_term,
            "long_term": self.long_term,
            "exported_at": datetime.now().isoformat()
        })
```

---

### 第三部分：测试策略

#### 3.1 单元测试

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def agent():
    """创建测试 Agent"""
    from your_module import AgentSystem
    return AgentSystem(
        name="test_agent",
        system_prompt="You are a helpful assistant"
    )

@pytest.mark.asyncio
async def test_agent_process(agent):
    """测试 Agent 处理"""
    with patch("your_module.openai"):
        response = await agent.process("Hello")
    assert response is not None
    assert isinstance(response, str)

@pytest.mark.asyncio
async def test_agent_input_validation(agent):
    """测试输入验证"""
    # 空输入
    with pytest.raises(ValueError):
        await agent.process("")

    # 超长输入
    long_input = "a" * 20000
    with pytest.raises(ValueError):
        await agent.process(long_input)

def test_memory():
    """测试记忆系统"""
    from your_module import Memory

    memory = Memory()

    # 添加记忆
    memory.add("Test content")
    assert len(memory.short_term) == 1

    # 检索
    results = memory.retrieve("Test")
    assert len(results) == 1
    assert results[0]["content"] == "Test content"
```

#### 3.2 集成测试

```python
@pytest.mark.asyncio
async def test_agent_with_plugins():
    """测试 Agent 与插件集成"""
    from your_module import AgentSystem, Plugin

    agent = AgentSystem(name="test", system_prompt="Test")

    # 添加插件
    async def mock_plugin(input: str) -> dict:
        return {"result": "plugin output"}

    agent.add_plugin("mock", mock_plugin)

    # 处理
    response = await agent.process("test input")
    assert "plugin" in response.lower() or "processed" in response.lower()

@pytest.mark.asyncio
async def test_agent_with_middleware():
    """测试 Agent 与中间件集成"""
    from your_module import AgentSystem

    agent = AgentSystem(name="test", system_prompt="Test")

    # 添加中间件
    def uppercase_middleware(input: str) -> str:
        return input.upper()

    agent.add_middleware("uppercase", uppercase_middleware)

    # 验证中间件生效
    assert agent._apply_middlewares_input("hello") == "HELLO"
```

---

### 第四部分：部署运维

#### 4.1 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

# 复制代码
COPY . .

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# 启动命令
CMD ["uv", "run", "python", "-m", "your_module.main"]
```

#### 4.2 健康检查

```python
from fastapi import FastAPI

app = FastAPI()

# 健康检查端点
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# 就绪检查端点
@app.get("/ready")
async def ready():
    # 检查依赖
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "llm": check_llm_service()
    }

    all_ready = all(checks.values())
    return {
        "ready": all_ready,
        "checks": checks
    }
```

#### 4.3 监控端点

```python
from fastapi import APIRouter

router = APIRouter(prefix="/metrics")

@router.get("/")
async def metrics():
    """Prometheus 指标端点"""
    collector = MetricsCollector()
    snapshot = collector.get_snapshot()

    # 格式化 Prometheus
    lines = []
    for name, value in snapshot["counters"].items():
        lines.append(f"agent_requests_total{{name=\"{name}\"}} {value}")

    for name, data in snapshot["histograms"].items():
        lines.append(f"agent_request_duration_seconds{{name=\"{name}\"}} {data['avg']}")

    return "\n".join(lines)
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 设计完整的 Agent 系统架构
- [ ] 实现插件系统和中间件
- [ ] 实现记忆系统
- [ ] 编写 Agent 系统的测试
- [ ] 部署 Agent 系统到生产环境

---

## 🔗 相关资源

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

## 🔗 下一步

完成 Stage 6 后，进入：

- Stage A: AI Agent 企业级应用
- Stage K: DevOps 与平台工程

---

**最后更新**: 2026-07-18
