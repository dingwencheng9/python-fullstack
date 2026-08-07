"""L09 日志解析器 - 测试用例

测试 solutions/01_solution.py 中的 parse_log 和 find_errors 函数。
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# 直接计算路径，不依赖 conftest
LESSON_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = LESSON_ROOT / "solutions"
_LOG_PARSER_PATH = SOLUTIONS_DIR / "01_solution.py"


def _load_module(name: str, file_path: Path):
    """按物理路径加载模块。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 加载 log_parser 解决方案
if _LOG_PARSER_PATH.exists():
    _log_parser = _load_module("_test_log_parser", _LOG_PARSER_PATH)
else:
    _log_parser = None


def _create_temp_log(content: str) -> Path:
    """创建临时日志文件并返回路径。"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


# ============================================================
# parse_log 测试
# ============================================================


@pytest.mark.skipif(_log_parser is None, reason="log_parser 未实现")
class TestParseLog:
    """parse_log 函数测试。"""

    def test_parse_log_counts_all_levels(self):
        """测试解析包含所有日志级别的文件。"""
        log_content = (
            "2024-01-01 10:00:00 INFO Server started\n"
            "2024-01-01 10:01:00 WARNING Memory usage high\n"
            "2024-01-01 10:02:00 ERROR Connection failed\n"
            "2024-01-01 10:03:00 INFO Request received\n"
            "2024-01-01 10:04:00 ERROR Timeout\n"
        )
        path = _create_temp_log(log_content)
        try:
            result = _log_parser.parse_log(path)
            assert result == {"INFO": 2, "ERROR": 2, "WARNING": 1}
        finally:
            path.unlink(missing_ok=True)

    def test_parse_log_empty_file(self):
        """测试解析空文件。"""
        path = _create_temp_log("")
        try:
            result = _log_parser.parse_log(path)
            assert result == {"INFO": 0, "ERROR": 0, "WARNING": 0}
        finally:
            path.unlink(missing_ok=True)

    def test_parse_log_no_matches(self):
        """测试文件中没有匹配的日志级别。"""
        log_content = "2024-01-01 10:00:00 DEBUG Starting application\n"
        path = _create_temp_log(log_content)
        try:
            result = _log_parser.parse_log(path)
            assert result == {"INFO": 0, "ERROR": 0, "WARNING": 0}
        finally:
            path.unlink(missing_ok=True)

    def test_parse_log_file_not_found(self):
        """测试文件不存在时返回空统计。"""
        result = _log_parser.parse_log("/nonexistent/path/xyz.log")
        assert result == {"INFO": 0, "ERROR": 0, "WARNING": 0}

    def test_parse_log_unicode_content(self):
        """测试解析包含中文的日志文件。"""
        log_content = (
            "2024-01-01 10:00:00 INFO 服务器启动成功\n2024-01-01 10:01:00 ERROR 数据库连接失败\n2024-01-01 10:02:00 WARNING 内存使用率过高\n"
        )
        path = _create_temp_log(log_content)
        try:
            result = _log_parser.parse_log(path)
            assert result == {"INFO": 1, "ERROR": 1, "WARNING": 1}
        finally:
            path.unlink(missing_ok=True)

    def test_parse_log_multiline_content(self):
        """测试解析多行内容的日志。"""
        log_content = "2024-01-01 10:00:00 INFO Starting...\nMultiple lines of debug info\n2024-01-01 10:01:00 ERROR Failed\n"
        path = _create_temp_log(log_content)
        try:
            result = _log_parser.parse_log(path)
            # 第二行不包含日志级别关键字
            assert result["INFO"] == 1
            assert result["ERROR"] == 1
        finally:
            path.unlink(missing_ok=True)


# ============================================================
# find_errors 测试
# ============================================================


@pytest.mark.skipif(_log_parser is None, reason="log_parser 未实现")
class TestFindErrors:
    """find_errors 函数测试。"""

    def test_find_errors_returns_tuples(self):
        """测试 find_errors 返回 (行号, 内容) 元组列表。"""
        log_content = (
            "2024-01-01 10:00:00 INFO Normal message\n"
            "2024-01-01 10:01:00 ERROR Something went wrong\n"
            "2024-01-01 10:02:00 INFO Another message\n"
            "2024-01-01 10:03:00 ERROR Another error\n"
        )
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            # 验证返回类型
            assert isinstance(errors, list)
            assert len(errors) == 2

            # 验证每个元素是 (int, str) 元组
            for error in errors:
                assert isinstance(error, tuple)
                assert len(error) == 2
                assert isinstance(error[0], int)  # 行号
                assert isinstance(error[1], str)  # 内容

        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_correct_line_numbers(self):
        """测试返回的行号正确。"""
        log_content = "Line 1: INFO message\nLine 2: INFO message\nLine 3: ERROR at line 3\nLine 4: INFO message\nLine 5: ERROR at line 5\n"
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            line_numbers = [e[0] for e in errors]
            assert line_numbers == [3, 5]
        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_stripped_content(self):
        """测试返回的内容已去除首尾空白。"""
        log_content = "   2024-01-01 10:00:00 ERROR Error with spaces   \n\t2024-01-01 10:01:00 ERROR Another error\t\n"
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            for _, content in errors:
                # 验证内容已去除空白
                assert content == content.strip()
                assert not content.startswith(" ")
                assert not content.endswith(" ")
        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_empty_file(self):
        """测试空文件返回空列表。"""
        path = _create_temp_log("")
        try:
            errors = _log_parser.find_errors(path)
            assert errors == []
        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_no_errors(self):
        """测试没有 ERROR 的文件返回空列表。"""
        log_content = "2024-01-01 10:00:00 INFO Message\n2024-01-01 10:01:00 WARNING Warning\n2024-01-01 10:02:00 DEBUG Debug\n"
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            assert errors == []
        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_file_not_found(self):
        """测试文件不存在时返回空列表。"""
        errors = _log_parser.find_errors("/nonexistent/path/xyz.log")
        assert errors == []

    def test_find_errors_unicode_content(self):
        """测试解析包含中文的日志文件。"""
        log_content = "2024-01-01 10:00:00 INFO 正常消息\n2024-01-01 10:01:00 ERROR 发生错误\n"
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            assert len(errors) == 1
            assert errors[0][0] == 2  # 第二行
            assert "ERROR" in errors[0][1]
        finally:
            path.unlink(missing_ok=True)

    def test_find_errors_preserves_error_keyword(self):
        """测试返回的内容保留 ERROR 关键字。"""
        log_content = "2024-01-01 10:00:00 ERROR Database connection failed\n"
        path = _create_temp_log(log_content)
        try:
            errors = _log_parser.find_errors(path)
            assert len(errors) == 1
            assert "ERROR" in errors[0][1]
        finally:
            path.unlink(missing_ok=True)
