from __future__ import annotations

import pytest

LogEntry = None  # type: ignore[assignment]
parse_log_line = None  # type: ignore[assignment]
filter_by_level = None  # type: ignore[assignment]
count_by_level = None  # type: ignore[assignment]
parse_logs = None  # type: ignore[assignment]


@pytest.fixture(scope="module", autouse=True)
def _inject_module(solutions, request) -> None:
    """从 solutions fixture 动态获取子模块并注入模块命名空间."""
    try:
        log_parser = solutions.solution_03_log_parser
        request.module.LogEntry = log_parser.LogEntry
        request.module.parse_log_line = log_parser.parse_log_line
        request.module.filter_by_level = log_parser.filter_by_level
        request.module.count_by_level = log_parser.count_by_level
        request.module.parse_logs = log_parser.parse_logs
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

    def test_parse_error_level(self) -> None:
        """测试解析 ERROR 级别"""
        line = "2024-01-15 10:23:48 [ERROR] [Database] Query timeout"
        result = parse_log_line(line)

        assert result is not None
        assert result["level"] == "ERROR"
        assert result["module"] == "Database"

    def test_parse_invalid_line(self) -> None:
        """测试解析无效行"""
        assert parse_log_line("invalid log format") is None
        assert parse_log_line("") is None

    def test_parse_all_levels(self) -> None:
        """测试所有日志级别"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        for level in levels:
            line = f"2024-01-15 10:23:45 [{level}] [Test] Test message"
            result = parse_log_line(line)
            assert result is not None
            assert result["level"] == level


class TestFilterByLevel:
    """测试 filter_by_level 函数"""

    @pytest.fixture
    def sample_logs(self) -> list[LogEntry]:
        """示例日志数据"""
        return [
            {"timestamp": "2024-01-15 10:23:45", "level": "INFO", "module": "App", "message": "msg1"},
            {"timestamp": "2024-01-15 10:23:46", "level": "DEBUG", "module": "DB", "message": "msg2"},
            {"timestamp": "2024-01-15 10:23:47", "level": "ERROR", "module": "API", "message": "msg3"},
            {"timestamp": "2024-01-15 10:23:48", "level": "INFO", "module": "App", "message": "msg4"},
        ]

    def test_filter_errors(self, sample_logs: list[LogEntry]) -> None:
        """测试过滤 ERROR 级别"""
        errors = filter_by_level(sample_logs, "ERROR")
        assert len(errors) == 1
        assert errors[0]["level"] == "ERROR"

    def test_filter_info(self, sample_logs: list[LogEntry]) -> None:
        """测试过滤 INFO 级别"""
        infos = filter_by_level(sample_logs, "INFO")
        assert len(infos) == 2

    def test_filter_no_match(self, sample_logs: list[LogEntry]) -> None:
        """测试无匹配结果"""
        result = filter_by_level(sample_logs, "CRITICAL")
        assert len(result) == 0


class TestCountByLevel:
    """测试 count_by_level 函数"""

    def test_count_levels(self) -> None:
        """测试统计各级别数量"""
        logs: list[LogEntry] = [
            {"timestamp": "t1", "level": "INFO", "module": "M1", "message": "m1"},
            {"timestamp": "t2", "level": "ERROR", "module": "M2", "message": "m2"},
            {"timestamp": "t3", "level": "INFO", "module": "M3", "message": "m3"},
            {"timestamp": "t4", "level": "DEBUG", "module": "M4", "message": "m4"},
            {"timestamp": "t5", "level": "ERROR", "module": "M5", "message": "m5"},
        ]

        counts = count_by_level(logs)
        assert counts["INFO"] == 2
        assert counts["ERROR"] == 2
        assert counts["DEBUG"] == 1

    def test_count_empty(self) -> None:
        """测试空列表"""
        counts = count_by_level([])
        assert counts == {}

    def test_count_single_level(self) -> None:
        """测试只有一种级别"""
        logs: list[LogEntry] = [
            {"timestamp": "t1", "level": "INFO", "module": "M1", "message": "m1"},
        ]
        counts = count_by_level(logs)
        assert counts == {"INFO": 1}


class TestParseLogs:
    """测试 parse_logs 函数"""

    def test_parse_multiple_lines(self) -> None:
        """测试解析多行日志"""
        content = """
2024-01-15 10:23:45 [INFO] [App] Message 1
2024-01-15 10:23:46 [ERROR] [API] Message 2
2024-01-15 10:23:47 [INFO] [DB] Message 3
"""
        logs = parse_logs(content)
        assert len(logs) == 3
        assert logs[0]["level"] == "INFO"
        assert logs[1]["level"] == "ERROR"
        assert logs[2]["level"] == "INFO"

    def test_parse_with_invalid_lines(self) -> None:
        """测试包含无效行"""
        content = """
2024-01-15 10:23:45 [INFO] [App] Valid message
invalid line
2024-01-15 10:23:46 [ERROR] [API] Another valid
"""
        logs = parse_logs(content)
        assert len(logs) == 2

    def test_parse_empty_content(self) -> None:
        """测试空内容"""
        assert parse_logs("") == []
        assert parse_logs("\n\n") == []
