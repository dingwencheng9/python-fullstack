"""L22 练习 3: 流式日志处理管道测试"""

from __future__ import annotations

import pytest

aggregate_logs = None  # type: ignore[assignment]
create_log_stream = None  # type: ignore[assignment]
merge_log_streams = None  # type: ignore[assignment]
parse_log_line = None  # type: ignore[assignment]
process_log_stream = None  # type: ignore[assignment]


@pytest.fixture(scope="module", autouse=True)
def _inject_module(solutions, request) -> None:
    """从 solutions fixture 动态获取子模块并注入模块命名空间."""
    try:
        pipeline = solutions.solution_03_streaming_pipeline
        request.module.aggregate_logs = pipeline.aggregate_logs
        request.module.create_log_stream = pipeline.create_log_stream
        request.module.merge_log_streams = pipeline.merge_log_streams
        request.module.parse_log_line = pipeline.parse_log_line
        request.module.process_log_stream = pipeline.process_log_stream
    except (AttributeError, ImportError) as e:
        pytest.fail(f"无法注入模块: {str(e)}")


class TestParseLogLine:
    """测试 parse_log_line 函数"""

    def test_parse_valid_line(self) -> None:
        """测试解析有效日志行"""
        line = "2024-01-15 10:23:45 [INFO] [AppServer] Server started"
        result = parse_log_line(line)

        assert result is not None
        assert result["timestamp"] == "2024-01-15 10:23:45"
        assert result["level"] == "INFO"
        assert result["module"] == "AppServer"
        assert result["message"] == "Server started"

    def test_parse_all_levels(self) -> None:
        """测试所有日志级别"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in levels:
            line = f"2024-01-15 10:23:45 [{level}] [Test] Test message"
            result = parse_log_line(line)
            assert result is not None
            assert result["level"] == level

    def test_parse_invalid_line(self) -> None:
        """测试解析无效行"""
        assert parse_log_line("invalid log format") is None
        assert parse_log_line("") is None


class TestCreateLogStream:
    """测试 create_log_stream 辅助函数"""

    @pytest.mark.asyncio
    async def test_stream_output(self) -> None:
        """测试流输出"""
        content = "line1\nline2\nline3"
        stream = create_log_stream("test", content, delay=0)

        lines = [line async for line in stream]
        assert len(lines) == 3
        assert lines[0] == "line1"
        assert lines[1] == "line2"
        assert lines[2] == "line3"

    @pytest.mark.asyncio
    async def test_stream_empty_lines(self) -> None:
        """测试空行过滤"""
        content = "line1\n\nline2\n   \nline3"
        stream = create_log_stream("test", content, delay=0)

        lines = [line async for line in stream]
        assert len(lines) == 3


class TestProcessLogStream:
    """测试 process_log_stream 函数"""

    @pytest.mark.asyncio
    async def test_process_valid_logs(self) -> None:
        """测试处理有效日志"""
        log_content = """
2024-01-15 10:23:45 [INFO] [App] Message 1
2024-01-15 10:23:46 [ERROR] [App] Message 2
"""
        stream = create_log_stream("test", log_content, delay=0)

        entries = await process_log_stream(stream, "test")
        assert len(entries) >= 2
        assert any(e["level"] == "INFO" for e in entries)
        assert any(e["level"] == "ERROR" for e in entries)

    @pytest.mark.asyncio
    async def test_process_mixed_logs(self) -> None:
        """测试处理混合日志（有效+无效）"""
        log_content = """
2024-01-15 10:23:45 [INFO] [App] Valid message
invalid line here
2024-01-15 10:23:46 [ERROR] [App] Another valid
"""
        stream = create_log_stream("test", log_content, delay=0)

        entries = await process_log_stream(stream, "test")
        # 应该包含有效日志和错误标记
        valid_count = sum(1 for e in entries if e["level"] != "ERROR" or not e["message"].startswith("[ParseError]"))
        assert valid_count >= 2


class TestMergeLogStreams:
    """测试 merge_log_streams 函数"""

    @pytest.mark.asyncio
    async def test_merge_sorted_output(self) -> None:
        """测试合并后按时间戳排序"""
        stream1 = create_log_stream("s1", """
2024-01-15 10:23:45 [INFO] [S1] First
2024-01-15 10:23:47 [INFO] [S1] Third
""", 0.001)

        stream2 = create_log_stream("s2", """
2024-01-15 10:23:46 [INFO] [S2] Second
2024-01-15 10:23:48 [INFO] [S2] Fourth
""", 0.001)

        results = [
            entry async for _, entry in merge_log_streams(("s1", stream1), ("s2", stream2))
        ]

        assert len(results) == 4
        timestamps = [e["timestamp"] for e in results]
        assert timestamps == sorted(timestamps)


class TestAggregateLogs:
    """测试 aggregate_logs 函数"""

    @pytest.mark.asyncio
    async def test_aggregate_basic(self) -> None:
        """测试基本聚合"""
        stream1 = create_log_stream("app", """
2024-01-15 10:23:45 [INFO] [App] Message 1
2024-01-15 10:23:46 [INFO] [App] Message 2
""", 0.001)

        stream2 = create_log_stream("db", """
2024-01-15 10:23:45 [DEBUG] [DB] Debug
2024-01-15 10:23:46 [ERROR] [DB] Error
""", 0.001)

        stats = await aggregate_logs([("app", stream1), ("db", stream2)])
        assert "INFO" in stats
        assert "DEBUG" in stats
        assert "ERROR" in stats
        assert stats["INFO"] == 2

    @pytest.mark.asyncio
    async def test_error_threshold(self) -> None:
        """测试错误阈值触发"""
        stream = create_log_stream("bad", """
2024-01-15 10:23:45 [INFO] [App] Message
invalid line 1
invalid line 2
invalid line 3
""", 0.001)

        # 高阈值不应抛出异常
        stats = await aggregate_logs([("bad", stream)], error_threshold=10)
        assert stats is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
