"""

from __future__ import annotations

L32 SSE 服务器推送事件 - Token 控制与自动摘要
========================================

本模块实现智能 Token 管理和历史记忆压缩。

核心能力：
1. Token 统计与监控
2. 自动摘要触发
3. 历史压缩策略
4. 滑动窗口管理

作者：Python 3.13 全栈课程
"""

import asyncio
from typing import Any

from checkpoint_system import (
    MessageRecord,
    PostgreSQLCheckpointSaver,
)
from opentelemetry import trace
from pydantic import BaseModel, Field

tracer = trace.get_tracer(__name__)


# ============================================================
# 1. Token 控制策略
# ============================================================


class TokenControlConfig(BaseModel):
    """Token 控制配置"""

    # Token 阈值
    max_context_tokens: int = Field(default=8000, description="最大上下文 Token 数（触发摘要）")
    target_context_tokens: int = Field(default=4000, description="目标上下文 Token 数（摘要后）")
    min_messages_for_summary: int = Field(default=10, description="触发摘要的最小消息数")

    # 摘要策略
    summary_window_size: int = Field(default=20, description="摘要窗口大小（消息数）")
    keep_recent_messages: int = Field(default=5, description="保留最近的 N 条消息（不摘要）")


class TokenStatistics(BaseModel):
    """Token 统计"""

    total_tokens: int = Field(default=0, description="总 Token 数")
    message_count: int = Field(default=0, description="消息数")
    avg_tokens_per_message: float = Field(default=0.0, description="平均 Token/消息")
    needs_summary: bool = Field(default=False, description="是否需要摘要")


# ============================================================
# 2. Token 统计器
# ============================================================


class TokenCounter:
    """
    Token 统计器

    **职责**:
    - 统计消息 Token 数
    - 判断是否超过阈值
    - 计算压缩比例
    """

    def __init__(self, config: TokenControlConfig):
        self.config = config

    def count_tokens(self, text: str) -> int:
        """
        统计 Token 数

        **简化实现**: 1 Token ≈ 4 字符（中文 1:1, 英文 1:4）
        **生产环境**: 使用 tiktoken 库
        """
        # 简单估算
        # 中文字符
        chinese_chars = sum(1 for c in text if "一" <= c <= "鿿")
        # 其他字符
        other_chars = len(text) - chinese_chars

        # 中文 1:1, 英文 1:4
        return chinese_chars + (other_chars // 4)

    def analyze_conversation(
        self,
        messages: list[MessageRecord],
    ) -> TokenStatistics:
        """分析会话的 Token 统计"""
        total_tokens = sum(msg.tokens for msg in messages)
        message_count = len(messages)
        avg_tokens = total_tokens / message_count if message_count > 0 else 0

        needs_summary = total_tokens > self.config.max_context_tokens and message_count >= self.config.min_messages_for_summary

        return TokenStatistics(
            total_tokens=total_tokens,
            message_count=message_count,
            avg_tokens_per_message=avg_tokens,
            needs_summary=needs_summary,
        )

    def select_messages_for_summary(
        self,
        messages: list[MessageRecord],
    ) -> tuple[list[MessageRecord], list[MessageRecord]]:
        """
        选择需要摘要的消息

        **返回**: (需要摘要的消息, 保留的最近消息)
        """
        if len(messages) <= self.config.keep_recent_messages:
            return [], messages

        # 保留最近的 N 条消息
        recent_messages = messages[-self.config.keep_recent_messages :]

        # 其余消息需要摘要
        messages_to_summarize = messages[: -self.config.keep_recent_messages]

        # 限制摘要窗口大小
        if len(messages_to_summarize) > self.config.summary_window_size:
            messages_to_summarize = messages_to_summarize[-self.config.summary_window_size :]

        return messages_to_summarize, recent_messages


# ============================================================
# 3. 自动摘要器
# ============================================================


class AutoSummarizer:
    """
    自动摘要器

    **职责**:
    - 生成对话摘要
    - 压缩历史记忆
    - 保留关键信息
    """

    def __init__(self, saver: PostgreSQLCheckpointSaver):
        self.saver = saver

    async def summarize_messages(
        self,
        messages: list[MessageRecord],
    ) -> str:
        """
        摘要消息列表

        **策略**:
        - 提取关键信息
        - 去除重复内容
        - 保留时间顺序

        **生产环境**: 调用 LLM 生成摘要
        """
        # 简化实现：拼接关键信息
        summary_parts = []

        for msg in messages:
            if msg.role == "user":
                summary_parts.append(f"用户询问: {msg.content[:100]}")
            elif msg.role == "assistant":
                summary_parts.append(f"助手回复: {msg.content[:100]}")

        summary = "\n".join(summary_parts[:10])  # 最多 10 条

        # 生产环境示例：
        # summary = await llm.summarize({
        #     "messages": [msg.model_dump() for msg in messages],
        #     "instruction": "请用 200 字以内总结对话要点",
        # })

        return f"[历史对话摘要]\n{summary}"

    async def compress_conversation(
        self,
        thread_id: str,
        messages_to_summarize: list[MessageRecord],
    ) -> dict[str, Any]:
        """
        压缩会话历史

        **流程**:
        1. 生成摘要
        2. 保存到 summaries 表
        3. 删除旧消息（可选）
        4. 返回压缩统计
        """
        with tracer.start_as_current_span("compress_conversation") as span:
            span.set_attribute("thread_id", thread_id)
            span.set_attribute("messages_count", len(messages_to_summarize))

            # 生成摘要
            summary = await self.summarize_messages(messages_to_summarize)

            # 计算 Token
            original_tokens = sum(msg.tokens for msg in messages_to_summarize)
            compressed_tokens = len(summary) // 4  # 简化估算

            # 保存摘要
            import uuid

            summary_id = f"summary_{uuid.uuid4().hex[:8]}"

            async with self.saver.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO summaries (
                        summary_id, thread_id, summary,
                        message_range_start, message_range_end,
                        original_tokens, compressed_tokens
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    summary_id,
                    thread_id,
                    summary,
                    messages_to_summarize[0].timestamp,
                    messages_to_summarize[-1].timestamp,
                    original_tokens,
                    compressed_tokens,
                )

            compression_ratio = (original_tokens - compressed_tokens) / original_tokens * 100 if original_tokens > 0 else 0

            span.set_attribute("compression_ratio", compression_ratio)

            return {
                "summary_id": summary_id,
                "original_tokens": original_tokens,
                "compressed_tokens": compressed_tokens,
                "compression_ratio": compression_ratio,
                "summary": summary,
            }

    async def get_conversation_context(
        self,
        thread_id: str,
        max_tokens: int = 4000,
    ) -> tuple[str, list[MessageRecord]]:
        """
        获取会话上下文（包含摘要和最近消息）

        **返回**: (摘要文本, 最近消息列表)
        """
        # 获取最新摘要
        summary_text = ""

        async with self.saver.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT summary FROM summaries
                WHERE thread_id = $1
                ORDER BY created_at DESC
                LIMIT 1
                """,
                thread_id,
            )

        if row:
            summary_text = row["summary"]

        # 获取最近消息
        recent_messages = await self.saver.get_messages(thread_id, limit=20)

        # 计算 Token
        summary_tokens = len(summary_text) // 4
        messages_tokens = sum(msg.tokens for msg in recent_messages)

        # 如果超过限制，裁剪消息
        if summary_tokens + messages_tokens > max_tokens:
            # 保留最近的消息
            total_tokens = summary_tokens
            kept_messages = []

            for msg in reversed(recent_messages):
                if total_tokens + msg.tokens > max_tokens:
                    break
                kept_messages.insert(0, msg)
                total_tokens += msg.tokens

            recent_messages = kept_messages

        return summary_text, recent_messages


# ============================================================
# 4. Token 控制节点
# ============================================================


class TokenControlNode:
    """
    Token 控制节点

    **职责**:
    - 在每次对话前检查 Token
    - 自动触发摘要
    - 返回可用上下文
    """

    def __init__(
        self,
        saver: PostgreSQLCheckpointSaver,
        config: TokenControlConfig | None = None,
    ):
        self.saver = saver
        self.config = config or TokenControlConfig()
        self.counter = TokenCounter(self.config)
        self.summarizer = AutoSummarizer(saver)

    async def check_and_compress(
        self,
        thread_id: str,
    ) -> dict[str, Any]:
        """
        检查并压缩会话

        **返回**:
        - needs_compression: 是否需要压缩
        - compression_result: 压缩结果（如果执行了）
        - context: 可用上下文
        """
        with tracer.start_as_current_span("token_control") as span:
            span.set_attribute("thread_id", thread_id)

            # 获取会话消息
            messages = await self.saver.get_messages(thread_id, limit=100)

            # 分析 Token 统计
            stats = self.counter.analyze_conversation(messages)

            span.set_attribute("total_tokens", stats.total_tokens)
            span.set_attribute("needs_summary", stats.needs_summary)

            result = {
                "needs_compression": stats.needs_summary,
                "statistics": stats.model_dump(),
                "compression_result": None,
                "context": None,
            }

            # 如果需要摘要
            if stats.needs_summary:
                # 选择需要摘要的消息
                messages_to_summarize, recent_messages = self.counter.select_messages_for_summary(messages)

                # 执行压缩
                compression_result = await self.summarizer.compress_conversation(
                    thread_id,
                    messages_to_summarize,
                )

                result["compression_result"] = compression_result

                span.add_event(
                    "conversation_compressed",
                    {
                        "original_tokens": compression_result["original_tokens"],
                        "compressed_tokens": compression_result["compressed_tokens"],
                    },
                )

            # 获取可用上下文
            summary, recent_messages = await self.summarizer.get_conversation_context(
                thread_id,
                max_tokens=self.config.target_context_tokens,
            )

            result["context"] = {
                "summary": summary,
                "recent_messages": [msg.model_dump(mode="json") for msg in recent_messages],
            }

            return result


# ============================================================
# 5. 示例用法
# ============================================================


async def main():
    """示例：Token 控制与自动摘要"""
    print("=" * 80)
    print("L32 SSE 服务器推送事件 - Token 控制与自动摘要")
    print("=" * 80 + "\n")

    # 初始化
    saver = PostgreSQLCheckpointSaver("postgresql://user:pass@localhost:5432/agent_db")
    await saver.setup()

    config = TokenControlConfig(
        max_context_tokens=1000,  # 测试用小阈值
        target_context_tokens=500,
        min_messages_for_summary=5,
    )

    node = TokenControlNode(saver, config)

    # 模拟会话
    thread_id = "thread_test"
    user_id = "user_test"

    print("1. 创建会话...")
    await saver.create_conversation(thread_id, user_id)
    print("   ✅ 会话已创建\n")

    # 添加多条消息
    print("2. 添加消息...")
    for i in range(15):
        message = MessageRecord(
            message_id=f"msg_{i:03d}",
            thread_id=thread_id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"这是第 {i} 条消息，内容较长" * 10,
            tokens=200,
        )
        await saver.add_message(thread_id, message)

    print("   ✅ 已添加 15 条消息\n")

    # 检查 Token
    print("3. 检查 Token...")
    result = await node.check_and_compress(thread_id)

    print(f"   总 Token 数: {result['statistics']['total_tokens']}")
    print(f"   需要压缩: {result['needs_compression']}")

    if result["compression_result"]:
        print("\n4. 压缩结果:")
        print(f"   原始 Token: {result['compression_result']['original_tokens']}")
        print(f"   压缩后 Token: {result['compression_result']['compressed_tokens']}")
        print(f"   压缩率: {result['compression_result']['compression_ratio']:.1f}%")

    print("\n5. 可用上下文:")
    print(f"   摘要长度: {len(result['context']['summary'])} 字符")
    print(f"   最近消息: {len(result['context']['recent_messages'])} 条")

    # 清理
    await saver.cleanup()

    print("\n" + "=" * 80)
    print("演示完成")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
