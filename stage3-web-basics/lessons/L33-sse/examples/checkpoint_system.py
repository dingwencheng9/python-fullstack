"""

from __future__ import annotations

L32 SSE 服务器推送事件 - 持久化检查点系统
======================================

本模块实现 Agent 会话的持久化存储。

核心能力：
1. PostgreSQL AsyncPG 持久化
2. Redis 缓存层
3. LangGraph Checkpointer 集成
4. 会话状态管理
5. Token 统计与控制

作者：Python 3.13 全栈课程
"""

import asyncio
from collections.abc import AsyncIterator
from datetime import datetime, UTC
import json
from typing import Any

import asyncpg
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from pydantic import BaseModel, Field
from redis.asyncio import Redis

# ============================================================
# 1. 数据模型
# ============================================================


class ConversationMetadata(BaseModel):
    """会话元数据"""

    thread_id: str = Field(description="会话 ID")
    user_id: str = Field(description="用户 ID")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    total_messages: int = Field(default=0, description="消息总数")
    total_tokens: int = Field(default=0, description="Token 总数")
    status: str = Field(default="active", description="会话状态")


class MessageRecord(BaseModel):
    """消息记录"""

    message_id: str
    thread_id: str
    role: str  # user, assistant, system
    content: str
    tokens: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class CheckpointRecord(BaseModel):
    """检查点记录"""

    thread_id: str
    checkpoint_id: str
    state: dict[str, Any]
    metadata: dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


# ============================================================
# 2. PostgreSQL 持久化层
# ============================================================


class PostgreSQLCheckpointSaver(BaseCheckpointSaver):
    """
    PostgreSQL 检查点存储器

    **表结构**:
    - conversations: 会话元数据
    - messages: 消息记录
    - checkpoints: 检查点快照
    """

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: asyncpg.Pool | None = None

    async def setup(self):
        """初始化数据库连接池和表结构"""
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=5,
            max_size=20,
        )

        # 创建表结构
        async with self.pool.acquire() as conn:
            # 会话表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    thread_id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    total_messages INTEGER DEFAULT 0,
                    total_tokens INTEGER DEFAULT 0,
                    status VARCHAR(50) DEFAULT 'active',
                    metadata JSONB DEFAULT '{}'
                )
            """)

            # 消息表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id VARCHAR(255) PRIMARY KEY,
                    thread_id VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    tokens INTEGER NOT NULL,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    metadata JSONB DEFAULT '{}',
                    FOREIGN KEY (thread_id) REFERENCES conversations(thread_id)
                )
            """)

            # 创建索引
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_thread_id
                ON messages(thread_id)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp
                ON messages(timestamp)
            """)

            # 检查点表
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id VARCHAR(255) PRIMARY KEY,
                    thread_id VARCHAR(255) NOT NULL,
                    state JSONB NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    FOREIGN KEY (thread_id) REFERENCES conversations(thread_id)
                )
            """)

            # 摘要表（压缩的历史记忆）
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    summary_id VARCHAR(255) PRIMARY KEY,
                    thread_id VARCHAR(255) NOT NULL,
                    summary TEXT NOT NULL,
                    message_range_start TIMESTAMP NOT NULL,
                    message_range_end TIMESTAMP NOT NULL,
                    original_tokens INTEGER NOT NULL,
                    compressed_tokens INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    FOREIGN KEY (thread_id) REFERENCES conversations(thread_id)
                )
            """)

    async def cleanup(self):
        """清理连接池"""
        if self.pool:
            await self.pool.close()

    # ========== 会话管理 ==========

    async def create_conversation(
        self,
        thread_id: str,
        user_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationMetadata:
        """创建新会话"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO conversations (thread_id, user_id, metadata)
                VALUES ($1, $2, $3)
                ON CONFLICT (thread_id) DO NOTHING
                """,
                thread_id,
                user_id,
                json.dumps(metadata or {}),
            )

        return ConversationMetadata(
            thread_id=thread_id,
            user_id=user_id,
            total_messages=0,
            total_tokens=0,
        )

    async def get_conversation(self, thread_id: str) -> ConversationMetadata | None:
        """获取会话元数据"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM conversations WHERE thread_id = $1
                """,
                thread_id,
            )

        if not row:
            return None

        return ConversationMetadata(
            thread_id=row["thread_id"],
            user_id=row["user_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            total_messages=row["total_messages"],
            total_tokens=row["total_tokens"],
            status=row["status"],
        )

    async def list_conversations(
        self,
        user_id: str,
        limit: int = 20,
    ) -> list[ConversationMetadata]:
        """列出用户的会话"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM conversations
                WHERE user_id = $1
                ORDER BY updated_at DESC
                LIMIT $2
                """,
                user_id,
                limit,
            )

        return [
            ConversationMetadata(
                thread_id=row["thread_id"],
                user_id=row["user_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                total_messages=row["total_messages"],
                total_tokens=row["total_tokens"],
                status=row["status"],
            )
            for row in rows
        ]

    # ========== 消息管理 ==========

    async def add_message(
        self,
        thread_id: str,
        message: MessageRecord,
    ):
        """添加消息"""
        async with self.pool.acquire() as conn:
            # 插入消息
            await conn.execute(
                """
                INSERT INTO messages (message_id, thread_id, role, content, tokens, metadata)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                message.message_id,
                thread_id,
                message.role,
                message.content,
                message.tokens,
                json.dumps(message.metadata),
            )

            # 更新会话统计
            await conn.execute(
                """
                UPDATE conversations
                SET
                    total_messages = total_messages + 1,
                    total_tokens = total_tokens + $2,
                    updated_at = NOW()
                WHERE thread_id = $1
                """,
                thread_id,
                message.tokens,
            )

    async def get_messages(
        self,
        thread_id: str,
        limit: int = 50,
    ) -> list[MessageRecord]:
        """获取会话消息"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM messages
                WHERE thread_id = $1
                ORDER BY timestamp ASC
                LIMIT $2
                """,
                thread_id,
                limit,
            )

        return [
            MessageRecord(
                message_id=row["message_id"],
                thread_id=row["thread_id"],
                role=row["role"],
                content=row["content"],
                tokens=row["tokens"],
                timestamp=row["timestamp"],
                metadata=json.loads(row["metadata"]) if row["metadata"] else {},
            )
            for row in rows
        ]

    async def get_token_count(self, thread_id: str) -> int:
        """获取会话的 Token 总数"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT total_tokens FROM conversations WHERE thread_id = $1
                """,
                thread_id,
            )

        return row["total_tokens"] if row else 0

    # ========== 检查点管理 ==========

    async def put(
        self,
        config: RunnableConfig,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
    ) -> RunnableConfig:
        """保存检查点"""
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO checkpoints (checkpoint_id, thread_id, state, metadata)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (checkpoint_id)
                DO UPDATE SET state = $3, metadata = $4
                """,
                checkpoint_id,
                thread_id,
                json.dumps(checkpoint),
                json.dumps(metadata),
            )

        return config

    async def get(
        self,
        config: RunnableConfig,
    ) -> Checkpoint | None:
        """加载检查点"""
        thread_id = config["configurable"]["thread_id"]

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT state FROM checkpoints
                WHERE thread_id = $1
                ORDER BY created_at DESC
                LIMIT 1
                """,
                thread_id,
            )

        if not row:
            return None

        return json.loads(row["state"])

    async def list(
        self,
        config: RunnableConfig,
    ) -> AsyncIterator[Checkpoint]:
        """列出检查点"""
        thread_id = config["configurable"]["thread_id"]

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT state FROM checkpoints
                WHERE thread_id = $1
                ORDER BY created_at DESC
                """,
                thread_id,
            )

        for row in rows:
            yield json.loads(row["state"])


# ============================================================
# 3. Redis 缓存层
# ============================================================


class RedisCacheLayer:
    """
    Redis 缓存层

    **用途**:
    - 缓存会话元数据
    - 缓存最近消息
    - 减少数据库查询
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Redis | None = None

    async def setup(self):
        """初始化 Redis 连接"""
        self.redis = await Redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def cleanup(self):
        """清理连接"""
        if self.redis:
            await self.redis.close()

    async def cache_conversation(
        self,
        thread_id: str,
        metadata: ConversationMetadata,
        ttl: int = 3600,
    ):
        """缓存会话元数据"""
        key = f"conversation:{thread_id}"
        await self.redis.setex(
            key,
            ttl,
            metadata.model_dump_json(),
        )

    async def get_cached_conversation(
        self,
        thread_id: str,
    ) -> ConversationMetadata | None:
        """获取缓存的会话元数据"""
        key = f"conversation:{thread_id}"
        data = await self.redis.get(key)

        if not data:
            return None

        return ConversationMetadata.model_validate_json(data)

    async def cache_messages(
        self,
        thread_id: str,
        messages: list[MessageRecord],
        ttl: int = 3600,
    ):
        """缓存消息列表"""
        key = f"messages:{thread_id}"
        await self.redis.setex(
            key,
            ttl,
            json.dumps([msg.model_dump(mode="json") for msg in messages]),
        )

    async def get_cached_messages(
        self,
        thread_id: str,
    ) -> list[MessageRecord] | None:
        """获取缓存的消息"""
        key = f"messages:{thread_id}"
        data = await self.redis.get(key)

        if not data:
            return None

        return [MessageRecord(**msg) for msg in json.loads(data)]


# ============================================================
# 4. 示例用法
# ============================================================


async def main():
    """示例：持久化检查点系统"""
    print("=" * 80)
    print("L32 SSE 服务器推送事件 - 持久化检查点系统")
    print("=" * 80 + "\n")

    # 初始化 PostgreSQL
    print("1. 初始化 PostgreSQL...")
    pg_saver = PostgreSQLCheckpointSaver("postgresql://user:pass@localhost:5432/agent_db")
    await pg_saver.setup()
    print("   ✅ PostgreSQL 已初始化\n")

    # 初始化 Redis
    print("2. 初始化 Redis...")
    redis_cache = RedisCacheLayer("redis://localhost:6379")
    await redis_cache.setup()
    print("   ✅ Redis 已初始化\n")

    # 创建会话
    print("3. 创建会话...")
    thread_id = "thread_123"
    user_id = "user_456"

    conv = await pg_saver.create_conversation(thread_id, user_id)
    print(f"   ✅ 会话已创建: {conv.thread_id}\n")

    # 添加消息
    print("4. 添加消息...")
    message = MessageRecord(
        message_id="msg_001",
        thread_id=thread_id,
        role="user",
        content="搜索 Python 异步编程",
        tokens=20,
    )
    await pg_saver.add_message(thread_id, message)
    print(f"   ✅ 消息已添加: {message.message_id}\n")

    # 获取消息
    print("5. 获取消息...")
    messages = await pg_saver.get_messages(thread_id)
    print(f"   ✅ 获取到 {len(messages)} 条消息\n")

    # 获取 Token 统计
    print("6. Token 统计...")
    token_count = await pg_saver.get_token_count(thread_id)
    print(f"   ✅ 总 Token 数: {token_count}\n")

    # 列出会话
    print("7. 列出会话...")
    conversations = await pg_saver.list_conversations(user_id)
    print(f"   ✅ 用户有 {len(conversations)} 个会话\n")

    # 清理
    print("8. 清理连接...")
    await pg_saver.cleanup()
    await redis_cache.cleanup()
    print("   ✅ 清理完成\n")

    print("=" * 80)
    print("演示完成")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
