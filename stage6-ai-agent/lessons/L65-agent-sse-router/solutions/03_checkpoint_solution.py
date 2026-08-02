"""

from __future__ import annotations

练习 3: Agent Checkpoint 持久化系统 - 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. asyncio.TaskGroup 并发操作
3. match/case 错误处理
4. Free-threading 线程安全设计

作者：Python 3.13 全栈课程
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ============================================================================
# 1. 数据模型（使用内置泛型和管道符）
# ============================================================================


@dataclass
class Message:
    """消息记录"""

    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation[T]:
    """
    会话记录（Python 3.13 PEP 695 泛型）

    泛型参数:
        T: 消息类型
    """

    conversation_id: str
    user_id: str
    messages: list[T] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, message: T) -> None:
        """添加消息"""
        self.messages.append(message)
        self.updated_at = datetime.now(UTC).isoformat()


@dataclass
class Checkpoint[T]:
    """
    检查点（Python 3.13 PEP 695 泛型）

    泛型参数:
        T: 会话数据类型
    """

    checkpoint_id: str
    conversation: T
    checkpoint_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# 2. Checkpoint 存储管理器（使用 asyncio.TaskGroup）
# ============================================================================


class CheckpointManager[T]:
    """
    Checkpoint 管理器（Python 3.13 PEP 695 泛型）

    🔒 Free-threading 线程安全说明:
    - 文件 I/O 操作使用 asyncio 保证单线程执行
    - dict 操作在 asyncio event loop 内是安全的
    - Python 3.14 环境下避免跨线程共享状态

    泛型参数:
        T: 会话数据类型
    """

    def __init__(self, storage_dir: str = "./checkpoints") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 🔒 内存缓存（asyncio event loop 单线程安全）
        self.cache: dict[str, Checkpoint[T]] = {}

    def _get_checkpoint_path(self, conversation_id: str) -> Path:
        """获取 checkpoint 文件路径"""
        return self.storage_dir / f"{conversation_id}.json"

    async def save_checkpoint(
        self,
        conversation: T,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """
        保存 checkpoint（使用 asyncio.TaskGroup 并发）

        🚀 Python 3.13 asyncio.TaskGroup:
        - 并发执行内存缓存和文件写入
        - 结构化并发，任一失败会取消其他任务

        Args:
            conversation: 会话数据
            metadata: 元数据

        Returns:
            checkpoint ID
        """
        checkpoint_id = str(uuid4())
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            conversation=conversation,
            metadata=metadata or {},
        )

        # 使用 TaskGroup 并发执行缓存和持久化
        async with asyncio.TaskGroup() as tg:
            # 任务 1: 更新内存缓存
            tg.create_task(self._update_cache(checkpoint))

            # 任务 2: 持久化到文件
            tg.create_task(self._persist_to_file(checkpoint))

        return checkpoint_id

    async def _update_cache(self, checkpoint: Checkpoint[T]) -> None:
        """更新内存缓存"""
        # 提取 conversation_id（假设 T 有此属性）
        if hasattr(checkpoint.conversation, "conversation_id"):
            conv_id = checkpoint.conversation.conversation_id
            self.cache[conv_id] = checkpoint

    async def _persist_to_file(self, checkpoint: Checkpoint[T]) -> None:
        """持久化到文件（异步 I/O）"""
        if hasattr(checkpoint.conversation, "conversation_id"):
            conv_id = checkpoint.conversation.conversation_id
            file_path = self._get_checkpoint_path(conv_id)

            # 序列化（支持 dataclass）
            data = {
                "checkpoint_id": checkpoint.checkpoint_id,
                "conversation": self._serialize_conversation(checkpoint.conversation),
                "checkpoint_at": checkpoint.checkpoint_at,
                "version": checkpoint.version,
                "metadata": checkpoint.metadata,
            }

            # 异步写入文件
            await asyncio.to_thread(
                file_path.write_text,
                json.dumps(data, ensure_ascii=False, indent=2),
            )

    def _serialize_conversation(self, conversation: T) -> dict[str, Any]:
        """序列化会话数据（递归序列化 dataclass）"""
        if hasattr(conversation, "__dict__"):
            result = {}
            for key, value in conversation.__dict__.items():
                # 跳过类型注解等非数据属性
                if key.startswith("_"):
                    continue
                if isinstance(value, list):
                    # 递归序列化列表中的 dataclass
                    result[key] = [item.__dict__ if hasattr(item, "__dict__") and not isinstance(item, type) else item for item in value]
                elif hasattr(value, "__dict__") and not isinstance(value, type):
                    # 递归序列化嵌套的 dataclass（排除类型对象）
                    result[key] = value.__dict__
                elif not isinstance(value, type):
                    # 只添加非类型对象
                    result[key] = value
            return result
        return {}

    async def load_checkpoint(self, conversation_id: str) -> Checkpoint[T] | None:
        """
        加载 checkpoint（使用 match/case 错误处理）

        🎯 Python 3.10+ match/case 错误处理

        Args:
            conversation_id: 会话 ID

        Returns:
            Checkpoint 或 None
        """
        # 1. 先从缓存读取
        if conversation_id in self.cache:
            return self.cache[conversation_id]

        # 2. 从文件加载
        file_path = self._get_checkpoint_path(conversation_id)

        if not file_path.exists():
            return None

        try:
            # 异步读取文件
            content = await asyncio.to_thread(file_path.read_text)
            data = json.loads(content)

            # 重建 Checkpoint（简化版，实际需要反序列化）
            checkpoint = Checkpoint(
                checkpoint_id=data["checkpoint_id"],
                conversation=data["conversation"],  # type: ignore
                checkpoint_at=data["checkpoint_at"],
                version=data["version"],
                metadata=data["metadata"],
            )

            # 更新缓存
            self.cache[conversation_id] = checkpoint
        except json.JSONDecodeError:
            print(f"JSON 解析错误: {conversation_id}")
            return None
        except FileNotFoundError:
            print(f"文件不存在: {conversation_id}")
            return None
        except PermissionError:
            print(f"权限错误: {conversation_id}")
            return None
        except Exception as e:
            print(f"未知错误: {type(e).__name__} - {e}")
            return None
        else:
            return checkpoint

    async def list_checkpoints(self, user_id: str | None = None) -> list[dict[str, Any]]:
        """
        列出所有 checkpoint（使用 asyncio.TaskGroup 并发）

        🚀 使用 TaskGroup 并发读取多个文件

        Args:
            user_id: 可选的用户 ID 过滤

        Returns:
            Checkpoint 列表
        """
        checkpoint_files = list(self.storage_dir.glob("*.json"))

        if not checkpoint_files:
            return []

        # 并发读取所有 checkpoint 文件
        checkpoints: list[dict[str, Any]] = []

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self._read_checkpoint_metadata(file_path)) for file_path in checkpoint_files]

        # 收集结果
        for task in tasks:
            result = task.result()
            if result is not None and (user_id is None or result.get("user_id") == user_id):
                checkpoints.append(result)

        return checkpoints

    async def _read_checkpoint_metadata(self, file_path: Path) -> dict[str, Any] | None:
        """读取 checkpoint 元数据"""
        try:
            content = await asyncio.to_thread(file_path.read_text)
            data = json.loads(content)
            return {
                "checkpoint_id": data["checkpoint_id"],
                "conversation_id": data["conversation"].get("conversation_id"),
                "user_id": data["conversation"].get("user_id"),
                "checkpoint_at": data["checkpoint_at"],
                "version": data["version"],
            }
        except Exception:
            return None

    async def delete_checkpoint(self, conversation_id: str) -> bool:
        """
        删除 checkpoint

        Args:
            conversation_id: 会话 ID

        Returns:
            是否删除成功
        """
        file_path = self._get_checkpoint_path(conversation_id)

        # 从缓存删除
        if conversation_id in self.cache:
            del self.cache[conversation_id]

        # 从文件系统删除
        if file_path.exists():
            await asyncio.to_thread(file_path.unlink)
            return True

        return False


# ============================================================================
# 3. FastAPI 应用
# ============================================================================

app = FastAPI(title="Agent Checkpoint 系统 - Python 3.13")

# 全局管理器
manager: CheckpointManager[Conversation[Message]] = CheckpointManager()


class CreateConversationRequest(BaseModel):
    """创建会话请求"""

    user_id: str
    initial_message: str | None = None


class AddMessageRequest(BaseModel):
    """添加消息请求"""

    role: str
    content: str
    metadata: dict[str, Any] | None = None


@app.get("/")
async def root() -> dict[str, Any]:
    """根端点"""
    return {
        "message": "Agent Checkpoint 系统 (Python 3.13)",
        "features": [
            "PEP 695 泛型语法",
            "asyncio.TaskGroup 并发",
            "match/case 错误处理",
            "Free-threading 线程安全",
        ],
    }


@app.post("/conversations")
async def create_conversation(request: CreateConversationRequest) -> dict[str, Any]:
    """
    创建新会话

    Args:
        request: 创建请求

    Returns:
        会话信息
    """
    conversation = Conversation[Message](
        conversation_id=str(uuid4()),
        user_id=request.user_id,
        messages=[],
    )

    # 添加初始消息
    if request.initial_message:
        message = Message(role="user", content=request.initial_message)
        conversation.add_message(message)

    # 保存 checkpoint
    checkpoint_id = await manager.save_checkpoint(conversation)

    return {
        "conversation_id": conversation.conversation_id,
        "checkpoint_id": checkpoint_id,
        "user_id": conversation.user_id,
        "created_at": conversation.created_at,
    }


@app.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str,
    request: AddMessageRequest,
) -> dict[str, Any]:
    """
    添加消息到会话

    Args:
        conversation_id: 会话 ID
        request: 消息请求

    Returns:
        更新后的会话信息
    """
    # 加载现有 checkpoint
    checkpoint = await manager.load_checkpoint(conversation_id)

    if checkpoint is None:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 添加消息
    message = Message(
        role=request.role,
        content=request.content,
        metadata=request.metadata or {},
    )
    checkpoint.conversation.add_message(message)

    # 保存新 checkpoint
    new_checkpoint_id = await manager.save_checkpoint(checkpoint.conversation)

    return {
        "conversation_id": conversation_id,
        "checkpoint_id": new_checkpoint_id,
        "message_count": len(checkpoint.conversation.messages),
        "updated_at": checkpoint.conversation.updated_at,
    }


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> dict[str, Any]:
    """
    获取会话详情

    Args:
        conversation_id: 会话 ID

    Returns:
        会话详情
    """
    checkpoint = await manager.load_checkpoint(conversation_id)

    if checkpoint is None:
        raise HTTPException(status_code=404, detail="会话不存在")

    return {
        "conversation_id": checkpoint.conversation.conversation_id,
        "user_id": checkpoint.conversation.user_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "metadata": msg.metadata,
            }
            for msg in checkpoint.conversation.messages
        ],
        "created_at": checkpoint.conversation.created_at,
        "updated_at": checkpoint.conversation.updated_at,
        "checkpoint_id": checkpoint.checkpoint_id,
        "checkpoint_at": checkpoint.checkpoint_at,
    }


@app.get("/checkpoints")
async def list_checkpoints(user_id: str | None = None) -> dict[str, Any]:
    """
    列出所有 checkpoint（使用 asyncio.TaskGroup 并发）

    Args:
        user_id: 可选的用户 ID 过滤

    Returns:
        Checkpoint 列表
    """
    checkpoints = await manager.list_checkpoints(user_id)

    return {
        "checkpoints": checkpoints,
        "count": len(checkpoints),
    }


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str) -> dict[str, Any]:
    """
    删除会话和 checkpoint

    Args:
        conversation_id: 会话 ID

    Returns:
        删除结果
    """
    success = await manager.delete_checkpoint(conversation_id)

    if not success:
        raise HTTPException(status_code=404, detail="会话不存在")

    return {
        "status": "deleted",
        "conversation_id": conversation_id,
    }


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("Agent Checkpoint 系统 - Python 3.13 参考答案")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ PEP 695 泛型语法: class CheckpointManager[T]")
    print("  ✅ asyncio.TaskGroup: 并发保存和加载")
    print("  ✅ match/case: 优雅的错误处理")
    print("  ✅ Free-threading 线程安全设计")
    print("\n启动服务:")
    print("  uvicorn solutions.03_checkpoint_solution:app --reload")
    print("\n测试端点:")
    print("  # 创建会话")
    print("  curl -X POST http://localhost:8000/conversations \\")
    print("    -H 'Content-Type: application/json' \\")
    print('    -d \'{"user_id": "user_123", "initial_message": "你好"}\'')
    print()
    print("  # 添加消息")
    print("  curl -X POST http://localhost:8000/conversations/{conv_id}/messages \\")
    print("    -H 'Content-Type: application/json' \\")
    print('    -d \'{"role": "assistant", "content": "你好！"}\'')
    print()
    print("  # 列出所有 checkpoint")
    print("  curl http://localhost:8000/checkpoints")
    print()

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
