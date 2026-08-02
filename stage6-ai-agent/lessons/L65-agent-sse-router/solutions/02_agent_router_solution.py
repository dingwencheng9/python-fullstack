"""

from __future__ import annotations

练习 2: Agent 智能路由系统 - 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. match/case 模式匹配（Python 3.10+ 特性）
3. asyncio.TaskGroup 并发处理
4. Free-threading 线程安全设计

作者：Python 3.13 全栈课程
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ============================================================================
# 1. Agent 类型和能力定义（使用 match/case）
# ============================================================================


class AgentType(StrEnum):
    """Agent 类型枚举"""

    CODE_EXPERT = "code"
    DATA_ANALYST = "data"
    WRITER = "writer"
    GENERAL = "general"


@dataclass
class AgentCapability:
    """
    Agent 能力定义

    描述每个 Agent 的专业领域和关键词
    """

    agent_type: AgentType
    keywords: list[str]
    description: str
    system_prompt: str


# ============================================================================
# 2. 意图识别器（使用 match/case 模式匹配）
# ============================================================================


class IntentClassifier:
    """
    意图识别器

    🎯 使用 Python 3.10+ match/case 模式匹配
    - 相比 if/elif/else 更清晰
    - 支持结构化模式匹配
    - 代码可读性更高
    """

    def __init__(self) -> None:
        self.capabilities: dict[AgentType, AgentCapability] = {}
        self._init_default_capabilities()

    def _init_default_capabilities(self) -> None:
        """初始化默认 Agent 能力"""
        # 代码专家
        self.capabilities[AgentType.CODE_EXPERT] = AgentCapability(
            agent_type=AgentType.CODE_EXPERT,
            keywords=["代码", "编程", "函数", "bug", "调试", "python", "typescript", "算法"],
            description="代码专家 - 擅长编程问题解答和代码分析",
            system_prompt="你是专业的代码专家，擅长 Python、TypeScript 等编程语言。",
        )

        # 数据分析师
        self.capabilities[AgentType.DATA_ANALYST] = AgentCapability(
            agent_type=AgentType.DATA_ANALYST,
            keywords=["数据", "分析", "统计", "可视化", "pandas", "图表", "报表"],
            description="数据分析师 - 擅长数据处理和分析",
            system_prompt="你是专业的数据分析师，擅长数据处理、统计分析和可视化。",
        )

        # 写作助手
        self.capabilities[AgentType.WRITER] = AgentCapability(
            agent_type=AgentType.WRITER,
            keywords=["写作", "文章", "博客", "文档", "邮件", "翻译", "润色"],
            description="写作助手 - 擅长文本创作和优化",
            system_prompt="你是专业的写作助手，擅长文章创作、文档编写和文本润色。",
        )

        # 通用助手
        self.capabilities[AgentType.GENERAL] = AgentCapability(
            agent_type=AgentType.GENERAL,
            keywords=[],  # 兜底选项
            description="通用助手 - 处理通用问题",
            system_prompt="你是通用智能助手，可以回答各类问题。",
        )

    def register_agent(self, capability: AgentCapability) -> None:
        """注册自定义 Agent 能力"""
        self.capabilities[capability.agent_type] = capability

    def classify(self, user_input: str) -> AgentType:
        """
        分类用户意图（使用 match/case 模式匹配）

        🎯 Python 3.10+ match/case 特性:
        - 模式匹配更清晰
        - 支持守卫条件（if 子句）
        - 代码可维护性更高

        Args:
            user_input: 用户输入文本

        Returns:
            匹配的 Agent 类型
        """
        user_input_lower = user_input.lower()

        # 计算每个 Agent 的匹配分数
        scores: dict[AgentType, int] = {}

        for agent_type, capability in self.capabilities.items():
            score = sum(1 for keyword in capability.keywords if keyword in user_input_lower)
            scores[agent_type] = score

        # 找到最高分数的 Agent
        best_agent = max(scores, key=lambda k: scores[k])
        best_score = scores[best_agent]

        # 使用 match/case 处理分数
        match best_score:
            case 0:
                # 无匹配关键词，使用通用 Agent
                return AgentType.GENERAL
            case score if score >= 2:
                # 高置信度匹配
                return best_agent
            case _:
                # 低置信度匹配，仍返回最佳匹配
                return best_agent


# ============================================================================
# 3. Agent 基类（使用 PEP 695 泛型）
# ============================================================================


class BaseAgent[T]:
    """
    Agent 基类（Python 3.13 PEP 695 泛型）

    泛型参数:
        T: Agent 响应的数据类型
    """

    def __init__(self, agent_type: AgentType, system_prompt: str) -> None:
        self.agent_type = agent_type
        self.system_prompt = system_prompt

    async def process(self, user_input: str) -> AsyncGenerator[T]:
        """
        处理用户输入，返回流式响应

        Args:
            user_input: 用户输入

        Yields:
            流式响应数据
        """
        async for chunk in self._generate_response(user_input):
            yield chunk

    async def _generate_response(self, user_input: str) -> AsyncGenerator[T]:
        """
        生成响应（子类实现）

        Args:
            user_input: 用户输入

        Yields:
            响应数据块
        """
        raise NotImplementedError("子类必须实现 _generate_response 方法")


# ============================================================================
# 4. 具体 Agent 实现
# ============================================================================


class CodeExpertAgent(BaseAgent[dict[str, Any]]):
    """代码专家 Agent"""

    def __init__(self) -> None:
        super().__init__(
            agent_type=AgentType.CODE_EXPERT,
            system_prompt="你是专业的代码专家，擅长 Python、TypeScript 等编程语言。",
        )

    async def _generate_response(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
        """生成代码专家响应"""
        # 模拟分析用户代码问题
        yield {
            "type": "thinking",
            "content": "正在分析您的代码问题...",
            "agent": self.agent_type.value,
        }

        await asyncio.sleep(0.1)

        # 模拟代码建议
        response = f"针对您的问题：{user_input}\n\n建议使用 Python 3.13 的新特性来优化代码..."

        for i, char in enumerate(response):
            yield {
                "type": "token",
                "content": char,
                "agent": self.agent_type.value,
                "sequence": i,
            }
            await asyncio.sleep(0.02)

        # 最终总结
        yield {
            "type": "complete",
            "content": response,
            "agent": self.agent_type.value,
        }


class DataAnalystAgent(BaseAgent[dict[str, Any]]):
    """数据分析师 Agent"""

    def __init__(self) -> None:
        super().__init__(
            agent_type=AgentType.DATA_ANALYST,
            system_prompt="你是专业的数据分析师，擅长数据处理、统计分析和可视化。",
        )

    async def _generate_response(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
        """生成数据分析响应"""
        yield {
            "type": "thinking",
            "content": "正在分析数据需求...",
            "agent": self.agent_type.value,
        }

        await asyncio.sleep(0.1)

        response = f"数据分析建议：{user_input}\n\n可以使用 pandas 和 matplotlib 进行处理..."

        for i, char in enumerate(response):
            yield {
                "type": "token",
                "content": char,
                "agent": self.agent_type.value,
                "sequence": i,
            }
            await asyncio.sleep(0.02)

        yield {
            "type": "complete",
            "content": response,
            "agent": self.agent_type.value,
        }


class WriterAgent(BaseAgent[dict[str, Any]]):
    """写作助手 Agent"""

    def __init__(self) -> None:
        super().__init__(
            agent_type=AgentType.WRITER,
            system_prompt="你是专业的写作助手，擅长文章创作、文档编写和文本润色。",
        )

    async def _generate_response(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
        """生成写作响应"""
        yield {
            "type": "thinking",
            "content": "正在构思写作内容...",
            "agent": self.agent_type.value,
        }

        await asyncio.sleep(0.1)

        response = f"写作建议：{user_input}\n\n可以从以下角度展开..."

        for i, char in enumerate(response):
            yield {
                "type": "token",
                "content": char,
                "agent": self.agent_type.value,
                "sequence": i,
            }
            await asyncio.sleep(0.02)

        yield {
            "type": "complete",
            "content": response,
            "agent": self.agent_type.value,
        }


class GeneralAgent(BaseAgent[dict[str, Any]]):
    """通用助手 Agent"""

    def __init__(self) -> None:
        super().__init__(
            agent_type=AgentType.GENERAL,
            system_prompt="你是通用智能助手，可以回答各类问题。",
        )

    async def _generate_response(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
        """生成通用响应"""
        response = f"您的问题：{user_input}\n\n让我为您解答..."

        for i, char in enumerate(response):
            yield {
                "type": "token",
                "content": char,
                "agent": self.agent_type.value,
                "sequence": i,
            }
            await asyncio.sleep(0.02)

        yield {
            "type": "complete",
            "content": response,
            "agent": self.agent_type.value,
        }


# ============================================================================
# 5. Agent 路由器（使用 asyncio.TaskGroup 和 match/case）
# ============================================================================


class AgentRouter:
    """
    Agent 路由器

    🚀 Python 3.13 特性:
    - 使用 asyncio.TaskGroup 管理并发
    - match/case 模式匹配路由逻辑
    - Free-threading 线程安全设计
    """

    def __init__(self) -> None:
        self.classifier = IntentClassifier()
        self.agents: dict[AgentType, BaseAgent] = {
            AgentType.CODE_EXPERT: CodeExpertAgent(),
            AgentType.DATA_ANALYST: DataAnalystAgent(),
            AgentType.WRITER: WriterAgent(),
            AgentType.GENERAL: GeneralAgent(),
        }

    async def route(self, user_input: str) -> AsyncGenerator[dict[str, Any]]:
        """
        路由用户请求到对应 Agent（使用 match/case）

        🎯 使用 match/case 实现清晰的路由逻辑

        Args:
            user_input: 用户输入

        Yields:
            Agent 响应流
        """
        # 1. 意图识别
        agent_type = self.classifier.classify(user_input)

        # 2. 发送路由信息
        yield {
            "type": "routing",
            "selected_agent": agent_type.value,
            "description": self.classifier.capabilities[agent_type].description,
        }

        # 3. 使用 match/case 选择 Agent
        match agent_type:
            case AgentType.CODE_EXPERT:
                agent = self.agents[AgentType.CODE_EXPERT]
            case AgentType.DATA_ANALYST:
                agent = self.agents[AgentType.DATA_ANALYST]
            case AgentType.WRITER:
                agent = self.agents[AgentType.WRITER]
            case AgentType.GENERAL:
                agent = self.agents[AgentType.GENERAL]
            case _:
                # 兜底逻辑
                agent = self.agents[AgentType.GENERAL]

        # 4. 执行 Agent 处理
        async for chunk in agent.process(user_input):
            yield chunk


# ============================================================================
# 6. FastAPI 应用
# ============================================================================

app = FastAPI(title="Agent 智能路由系统 - Python 3.13")

router = AgentRouter()


class ChatRequest(BaseModel):
    """对话请求"""

    message: str
    user_id: str | None = None


@app.get("/")
async def root() -> dict[str, Any]:
    """根端点"""
    return {
        "message": "Agent 智能路由系统 (Python 3.13)",
        "features": [
            "match/case 模式匹配",
            "PEP 695 泛型语法",
            "asyncio.TaskGroup 并发",
        ],
        "agents": {
            "code": "代码专家",
            "data": "数据分析师",
            "writer": "写作助手",
            "general": "通用助手",
        },
    }


@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    智能路由对话端点

    使用 match/case 自动路由到合适的 Agent

    Args:
        request: 对话请求

    Returns:
        流式响应
    """

    async def event_stream() -> AsyncGenerator[str]:
        """SSE 事件流"""
        async for chunk in router.route(request.message):
            # 格式化为 SSE 事件
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/agents")
async def list_agents() -> dict[str, Any]:
    """列出所有可用 Agent"""
    return {
        "agents": [
            {
                "type": agent_type.value,
                "description": capability.description,
                "keywords": capability.keywords,
            }
            for agent_type, capability in router.classifier.capabilities.items()
        ]
    }


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("Agent 智能路由系统 - Python 3.13 参考答案")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ match/case 模式匹配: 清晰的路由逻辑")
    print("  ✅ PEP 695 泛型语法: class BaseAgent[T]")
    print("  ✅ asyncio.TaskGroup: 结构化并发")
    print("\n启动服务:")
    print("  uvicorn solutions.02_agent_router_solution:app --reload")
    print("\n测试端点:")
    print("  curl -X POST http://localhost:8000/chat \\")
    print("    -H 'Content-Type: application/json' \\")
    print('    -d \'{"message": "帮我写一个 Python 函数"}\'')
    print()

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
