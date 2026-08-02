"""

from __future__ import annotations

练习 3: Checkpoint 断点续传系统

任务：
实现支持断点续传的对话系统，可以保存和恢复对话状态。

学习目标：
- 实现对话状态持久化
- 支持多轮对话上下文
- 实现断点保存和恢复
- 处理并发访问和状态同步

预计时间: 60 分钟
难度: ⭐⭐⭐⭐⭐
"""

import asyncio
from pathlib import Path

# ============================================================================
# TODO 1: 定义消息和对话状态
# ============================================================================

# TODO: 创建消息模型
# @dataclass
# class Message:
#     role: str  # "user" or "assistant"
#     content: str
#     timestamp: float
#     metadata: dict = field(default_factory=dict)


# TODO: 创建对话状态模型
# @dataclass
# class ConversationState:
#     conversation_id: str
#     messages: List[Message] = field(default_factory=list)
#     context: dict = field(default_factory=dict)
#     created_at: float = field(default_factory=lambda: datetime.now().timestamp())
#     updated_at: float = field(default_factory=lambda: datetime.now().timestamp())


# ============================================================================
# TODO 2: 实现 Checkpoint 存储
# ============================================================================


class CheckpointStorage:
    """Checkpoint 存储"""

    def __init__(self, storage_dir: str = "./checkpoints"):
        # TODO: 初始化存储目录
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def _get_file_path(self, conversation_id: str) -> Path:
        """获取存储文件路径"""
        # TODO: 返回文件路径

    def save(self, state: ConversationState) -> None:
        """保存 checkpoint"""
        # TODO:
        # 1. 更新 updated_at
        # 2. 序列化为 JSON
        # 3. 写入文件

    def load(self, conversation_id: str) -> ConversationState | None:
        """加载 checkpoint"""
        # TODO:
        # 1. 读取文件
        # 2. 解析 JSON
        # 3. 返回 ConversationState
        # 4. 文件不存在返回 None

    def delete(self, conversation_id: str) -> bool:
        """删除 checkpoint"""
        # TODO:
        # 1. 删除文件
        # 2. 返回是否成功

    def list_conversations(self) -> list[str]:
        """列出所有对话ID"""
        # TODO:
        # 1. 扫描存储目录
        # 2. 返回所有对话ID列表


# ============================================================================
# TODO 3: 实现对话管理器
# ============================================================================


class ConversationManager:
    """对话管理器"""

    def __init__(self, storage: CheckpointStorage):
        # TODO: 初始化
        self.storage = storage
        self.active_conversations: dict[str, ConversationState] = {}
        self.locks: dict[str, asyncio.Lock] = {}

    async def get_or_create(self, conversation_id: str) -> ConversationState:
        """获取或创建对话"""
        # TODO:
        # 1. 检查内存中是否存在
        # 2. 尝试从存储加载
        # 3. 创建新对话
        # 4. 返回对话状态

    async def add_message(self, conversation_id: str, role: str, content: str, metadata: dict | None = None) -> None:
        """添加消息"""
        # TODO:
        # 1. 获取对话
        # 2. 创建消息
        # 3. 添加到对话
        # 4. 保存 checkpoint

    async def get_context(self, conversation_id: str, max_messages: int = 10) -> list[Message]:
        """获取对话上下文"""
        # TODO:
        # 1. 获取对话
        # 2. 返回最近的 N 条消息

    async def save_checkpoint(self, conversation_id: str) -> None:
        """保存 checkpoint"""
        # TODO:
        # 1. 获取对话
        # 2. 调用存储保存

    async def restore_checkpoint(self, conversation_id: str) -> ConversationState | None:
        """恢复 checkpoint"""
        # TODO:
        # 1. 从存储加载
        # 2. 加载到内存
        # 3. 返回对话状态

    def get_statistics(self) -> dict:
        """获取统计信息"""
        # TODO:
        # 1. 活跃对话数
        # 2. 总对话数
        # 3. 总消息数


# ============================================================================
# TODO 4: 实现自动保存策略
# ============================================================================


class AutoSavePolicy:
    """自动保存策略"""

    def __init__(
        self,
        save_interval: int = 5,  # 每N条消息保存一次
        time_interval: float = 60.0,  # 每N秒保存一次
    ):
        # TODO: 初始化配置
        self.save_interval = save_interval
        self.time_interval = time_interval
        self.message_count: dict[str, int] = {}
        self.last_save: dict[str, float] = {}

    def should_save(self, conversation_id: str) -> bool:
        """判断是否应该保存"""
        # TODO:
        # 1. 检查消息数
        # 2. 检查时间间隔
        # 3. 返回是否应该保存

    def record_message(self, conversation_id: str) -> None:
        """记录消息"""
        # TODO: 增加消息计数

    def record_save(self, conversation_id: str) -> None:
        """记录保存"""
        # TODO:
        # 1. 重置消息计数
        # 2. 更新保存时间


# ============================================================================
# TODO 5: 创建 FastAPI 应用
# ============================================================================

from fastapi import FastAPI

app = FastAPI(title="Checkpoint 断点续传练习")

# TODO: 创建全局组件
# storage = CheckpointStorage()
# manager = ConversationManager(storage)
# auto_save = AutoSavePolicy()


@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "Checkpoint 断点续传系统",
        "endpoints": {
            "/conversations": "对话列表",
            "/conversation/{id}/messages": "获取消息",
            "/conversation/{id}/send": "发送消息",
            "/conversation/{id}/checkpoint": "保存/恢复",
        },
    }


@app.get("/conversations")
async def list_conversations():
    """列出所有对话"""
    # TODO:
    # 1. 获取对话列表
    # 2. 返回对话ID和统计


@app.get("/conversation/{conversation_id}/messages")
async def get_messages(conversation_id: str, limit: int = 10):
    """获取对话消息"""
    # TODO:
    # 1. 获取对话上下文
    # 2. 返回消息列表


@app.post("/conversation/{conversation_id}/send")
async def send_message(conversation_id: str, content: str):
    """发送消息"""
    # TODO:
    # 1. 添加用户消息
    # 2. 生成助手回复
    # 3. 检查自动保存
    # 4. 返回回复


@app.post("/conversation/{conversation_id}/checkpoint/save")
async def save_checkpoint(conversation_id: str):
    """手动保存 checkpoint"""
    # TODO:
    # 1. 保存 checkpoint
    # 2. 返回结果


@app.post("/conversation/{conversation_id}/checkpoint/restore")
async def restore_checkpoint(conversation_id: str):
    """恢复 checkpoint"""
    # TODO:
    # 1. 恢复 checkpoint
    # 2. 返回对话状态


@app.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """删除对话"""
    # TODO:
    # 1. 从内存删除
    # 2. 从存储删除
    # 3. 返回结果


@app.get("/stats")
async def get_stats():
    """获取统计信息"""
    # TODO: 返回管理器统计


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 3: Checkpoint 断点续传系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 定义消息和对话状态")
    print("  2. 实现 Checkpoint 存储")
    print("  3. 创建对话管理器")
    print("  4. 实现自动保存策略")
    print("  5. 创建 API 端点")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.03_checkpoint:app --reload")
    print("  2. 发送消息:")
    print("     curl -X POST http://localhost:8000/conversation/test1/send?content='Hello'")
    print("  3. 获取消息:")
    print("     curl http://localhost:8000/conversation/test1/messages")
    print("  4. 保存checkpoint:")
    print("     curl -X POST http://localhost:8000/conversation/test1/checkpoint/save")
    print("\n核心概念：")
    print("  - State Persistence: 状态持久化")
    print("  - Auto-save: 自动保存")
    print("  - Context Management: 上下文管理")
    print("  - Concurrency Control: 并发控制")
    print()
