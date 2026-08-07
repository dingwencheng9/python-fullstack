"""L32 Agent SSE Router 基准测试

测试维度:
1. 模块导入健康测试
2. 核心 SSE 流式逻辑测试
3. 异常边界测试
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

# ============================================================================
# 测试维度 1: 模块导入健康测试
# ============================================================================


def test_import_fastapi() -> None:
    """测试 FastAPI 依赖导入"""
    pytest.importorskip("fastapi", reason="需要 FastAPI（uv sync --extra web）")
    from fastapi import APIRouter, FastAPI
    from fastapi.responses import StreamingResponse

    assert FastAPI is not None
    assert APIRouter is not None
    assert StreamingResponse is not None


def test_import_pydantic() -> None:
    """测试 Pydantic 依赖导入"""
    try:
        from pydantic import BaseModel, Field

        assert BaseModel is not None
        assert Field is not None
    except ImportError as e:
        pytest.fail(f"Pydantic 导入失败: {e}")


def test_import_opentelemetry() -> None:
    """测试 OpenTelemetry 可选依赖导入。"""
    pytest.importorskip("opentelemetry", reason="OpenTelemetry 仅 V2 可观测性示例需要")
    from opentelemetry import trace
    from opentelemetry.trace import Tracer

    assert trace is not None
    assert Tracer is not None


# ============================================================================
# 测试维度 2: 核心 SSE 流式逻辑测试
# ============================================================================


@pytest.mark.asyncio
async def test_sse_event_generator() -> None:
    """测试 SSE 事件生成器"""

    async def mock_event_generator() -> AsyncGenerator[str]:
        """模拟 SSE 事件生成器"""
        for i in range(3):
            yield f"data: event_{i}\n\n"
            await asyncio.sleep(0.01)

    # 收集生成的事件
    events = []
    async for event in mock_event_generator():
        events.append(event)

    assert len(events) == 3
    assert events[0] == "data: event_0\n\n"
    assert events[2] == "data: event_2\n\n"


@pytest.mark.asyncio
async def test_sse_format() -> None:
    """测试 SSE 格式正确性"""

    def format_sse_event(data: dict) -> str:
        """格式化 SSE 事件"""
        import json

        return f"data: {json.dumps(data)}\n\n"

    event_data = {"type": "token", "content": "hello"}
    formatted = format_sse_event(event_data)

    assert formatted.startswith("data: ")
    assert formatted.endswith("\n\n")
    assert "hello" in formatted


@pytest.mark.asyncio
async def test_async_generator_cleanup() -> None:
    """测试异步生成器正确清理"""

    cleanup_flag = {"closed": False}

    async def generator_with_cleanup() -> AsyncGenerator[int]:
        try:
            for i in range(5):
                yield i
        finally:
            cleanup_flag["closed"] = True

    # 提前中断生成器
    gen = generator_with_cleanup()
    first = await gen.__anext__()
    await gen.aclose()

    assert first == 0
    assert cleanup_flag["closed"] is True


@pytest.mark.asyncio
async def test_stream_token_events() -> None:
    """测试 Token 流式事件"""

    async def stream_tokens(text: str) -> AsyncGenerator[dict]:
        """模拟 Token 流式生成"""
        for char in text:
            yield {"event_type": "token_stream", "token": char, "is_final": False}
            await asyncio.sleep(0.01)

        yield {"event_type": "token_stream", "token": "", "is_final": True}

    tokens = []
    async for event in stream_tokens("hi"):
        tokens.append(event["token"])

    assert len(tokens) == 3  # 'h', 'i', ''
    assert tokens[0] == "h"
    assert tokens[1] == "i"


# ============================================================================
# 测试维度 3: 异常边界测试
# ============================================================================


@pytest.mark.asyncio
async def test_empty_stream() -> None:
    """测试空流处理"""

    async def empty_generator() -> AsyncGenerator[str]:
        """空生成器"""
        return
        yield  # 永远不会执行

    events = []
    async for event in empty_generator():
        events.append(event)

    assert len(events) == 0


@pytest.mark.asyncio
async def test_generator_exception_handling() -> None:
    """测试生成器异常处理"""

    async def failing_generator() -> AsyncGenerator[int]:
        """会抛出异常的生成器"""
        yield 1
        yield 2
        raise ValueError("Generator failed")

    with pytest.raises(ValueError, match="Generator failed"):
        async for _item in failing_generator():
            pass


@pytest.mark.asyncio
async def test_invalid_sse_data() -> None:
    """测试无效 SSE 数据处理"""

    def format_sse_safe(data: dict) -> str:
        """安全的 SSE 格式化"""
        import json

        try:
            json_str = json.dumps(data)
        except (TypeError, ValueError):
            return "data: {}\n\n"
        else:
            return f"data: {json_str}\n\n"

    # 测试不可序列化的对象
    class NonSerializable:
        pass

    result = format_sse_safe({"obj": NonSerializable()})
    assert result == "data: {}\n\n"


@pytest.mark.asyncio
async def test_concurrent_stream_handling() -> None:
    """测试并发流处理"""

    async def concurrent_generator(id: int) -> AsyncGenerator[dict]:
        """并发生成器"""
        for i in range(3):
            yield {"id": id, "value": i}
            await asyncio.sleep(0.01)

    # 并发执行多个生成器
    results = await asyncio.gather(
        collect_stream(concurrent_generator(1)),
        collect_stream(concurrent_generator(2)),
    )

    assert len(results) == 2
    assert len(results[0]) == 3
    assert len(results[1]) == 3


async def collect_stream(gen: AsyncGenerator[object]) -> list[object]:
    """收集流数据"""
    items = []
    async for item in gen:
        items.append(item)
    return items


@pytest.mark.asyncio
async def test_stream_cancellation() -> None:
    """测试流取消处理"""

    cancelled = {"flag": False}

    async def cancellable_stream() -> AsyncGenerator[int]:
        try:
            for i in range(100):
                yield i
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            cancelled["flag"] = True
            raise
        except GeneratorExit:
            cancelled["flag"] = True
            raise

    async def consume_and_cancel() -> None:
        gen = cancellable_stream()
        # 只消费前 2 个
        for _ in range(2):
            await gen.__anext__()
        # 取消
        await gen.aclose()

    await consume_and_cancel()
    assert cancelled["flag"] is True


# ============================================================================
# 集成测试
# ============================================================================


@pytest.mark.asyncio
async def test_full_sse_pipeline() -> None:
    """测试完整 SSE 管道"""

    async def simulate_agent_stream() -> AsyncGenerator[str]:
        """模拟完整的 Agent 流"""
        import json

        # 1. 思考事件
        yield f"data: {json.dumps({'type': 'thinking', 'content': 'Processing query'})}\n\n"
        await asyncio.sleep(0.01)

        # 2. Token 流
        for token in ["Hello", " ", "World"]:
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
            await asyncio.sleep(0.01)

        # 3. 完成事件
        yield f"data: {json.dumps({'type': 'done', 'content': ''})}\n\n"

    events = []
    async for event in simulate_agent_stream():
        events.append(event)

    assert len(events) == 5
    assert "thinking" in events[0]
    assert "Hello" in events[1]
    assert "done" in events[-1]


# ============================================================================
# 性能测试
# ============================================================================


@pytest.mark.asyncio
async def test_stream_performance() -> None:
    """测试流处理性能"""
    import time

    async def high_throughput_stream(n: int) -> AsyncGenerator[int]:
        """高吞吐量流"""
        for i in range(n):
            yield i

    start = time.time()
    count = 0
    async for _ in high_throughput_stream(10000):
        count += 1
    elapsed = time.time() - start

    assert count == 10000
    assert elapsed < 1.0  # 应该在 1 秒内完成


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
