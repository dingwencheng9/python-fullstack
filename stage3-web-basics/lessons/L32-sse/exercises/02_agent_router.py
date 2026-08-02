"""

from __future__ import annotations

练习 2: Agent 智能路由系统

任务：
实现基于意图识别的 Agent 路由系统，将用户请求分发到不同的专业 Agent。

学习目标：
- 实现意图识别和分类
- 构建 Agent 路由器
- 实现 Agent 响应流
- 处理 Agent 切换和上下文

预计时间: 60 分钟
难度: ⭐⭐⭐⭐⭐
"""

from collections.abc import AsyncGenerator

from fastapi import FastAPI

# ============================================================================
# TODO 1: 定义 Agent 类型和能力
# ============================================================================

# TODO: 创建 Agent 类型枚举
# class AgentType(str, Enum):
#     CODE_EXPERT = "code"  # 代码专家
#     DATA_ANALYST = "data"  # 数据分析
#     WRITER = "writer"  # 写作助手
#     GENERAL = "general"  # 通用助手


# TODO: 创建 Agent 能力定义
# @dataclass
# class AgentCapability:
#     agent_type: AgentType
#     keywords: list[str]  # 关键词
#     description: str
#     system_prompt: str


# ============================================================================
# TODO 2: 实现意图识别器
# ============================================================================


class IntentClassifier:
    """意图识别器"""

    def __init__(self):
        # TODO: 初始化 Agent 能力映射
        self.capabilities: dict[AgentType, AgentCapability] = {}

    def register_agent(self, capability: AgentCapability) -> None:
        """注册 Agent 能力"""
        # TODO: 添加到能力映射

    def classify(self, user_input: str) -> AgentType:
        """分类用户意图"""
        # TODO:
        # 1. 提取关键词
        # 2. 匹配 Agent 能力
        # 3. 返回最匹配的 Agent 类型
        # 4. 默认返回 GENERAL


# ============================================================================
# TODO 3: 实现 Agent 基类
# ============================================================================

# TODO: 创建 Agent 基类
# class BaseAgent:
#     def __init__(self, agent_type: AgentType, system_prompt: str):
#         self.agent_type = agent_type
#         self.system_prompt = system_prompt
#
#     async def process(self, user_input: str) -> AsyncGenerator[str, None]:
#         """处理用户输入，返回流式响应"""
#         pass
#
#     async def _generate_response(self, user_input: str) -> AsyncGenerator[str, None]:
#         """生成响应（子类实现）"""
#         pass


# ============================================================================
# TODO 4: 实现具体 Agent
# ============================================================================

# TODO: 实现代码专家 Agent
# class CodeExpertAgent(BaseAgent):
#     def __init__(self):
#         super().__init__(
#             AgentType.CODE_EXPERT,
#             "你是一个代码专家，擅长编程和技术问题。"
#         )
#
#     async def _generate_response(self, user_input: str) -> AsyncGenerator[str, None]:
#         """生成代码相关响应"""
#         pass


# TODO: 实现数据分析 Agent
# class DataAnalystAgent(BaseAgent):
#     pass


# TODO: 实现写作助手 Agent
# class WriterAgent(BaseAgent):
#     pass


# TODO: 实现通用助手 Agent
# class GeneralAgent(BaseAgent):
#     pass


# ============================================================================
# TODO 5: 实现 Agent 路由器
# ============================================================================


class AgentRouter:
    """Agent 路由器"""

    def __init__(self):
        # TODO: 初始化
        self.classifier = IntentClassifier()
        self.agents: dict[AgentType, BaseAgent] = {}
        self.routing_history: list[dict] = []

    def register_agent(self, agent: BaseAgent) -> None:
        """注册 Agent"""
        # TODO: 添加到 agents 字典

    async def route_and_process(self, user_input: str, context: dict | None = None) -> AsyncGenerator[dict]:
        """路由并处理请求"""
        # TODO:
        # 1. 识别意图
        # 2. 选择 Agent
        # 3. 记录路由历史
        # 4. 流式返回响应
        # 5. yield 路由信息和响应内容

    def get_routing_stats(self) -> dict:
        """获取路由统计"""
        # TODO:
        # 1. 统计各 Agent 使用次数
        # 2. 返回统计信息


# ============================================================================
# TODO 6: 创建 FastAPI 应用
# ============================================================================

app = FastAPI(title="Agent 智能路由练习")

# TODO: 创建全局路由器
# router = AgentRouter()

# TODO: 注册所有 Agent


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "Agent 智能路由系统",
        "agents": ["code", "data", "writer", "general"],
    }


@app.post("/chat")
async def chat(user_input: str):
    """聊天端点（非流式）"""
    # TODO:
    # 1. 调用路由器
    # 2. 收集所有响应
    # 3. 返回完整结果


@app.post("/chat/stream")
async def chat_stream(user_input: str):
    """聊天端点（流式）"""
    # TODO:
    # 1. 创建 SSE 流
    # 2. yield 路由信息
    # 3. yield Agent 响应
    # 4. 返回 StreamingResponse


@app.get("/stats")
async def get_stats():
    """获取路由统计"""
    # TODO: 返回路由统计信息


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2: Agent 智能路由系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 定义 Agent 类型和能力")
    print("  2. 实现意图识别器")
    print("  3. 创建 Agent 基类")
    print("  4. 实现具体 Agent")
    print("  5. 构建 Agent 路由器")
    print("  6. 创建聊天端点")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.02_agent_router:app --reload")
    print("  2. 测试路由:")
    print("     curl -X POST http://localhost:8000/chat?user_input='写一段Python代码'")
    print("     curl -X POST http://localhost:8000/chat?user_input='分析这组数据'")
    print("  3. 查看统计: curl http://localhost:8000/stats")
    print("\n核心概念：")
    print("  - Intent Classification: 意图识别")
    print("  - Agent Selection: Agent 选择")
    print("  - Context Management: 上下文管理")
    print("  - Streaming Response: 流式响应")
    print()
