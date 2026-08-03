"""L09 文件操作与上下文管理 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
"""

import importlib.util
from pathlib import Path
import tempfile

import pytest


EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def log_parser_module():
    """加载 exercises/01_log_parser.py"""
    return _load_exercise_module("_test_log_parser", EXERCISES_DIR / "01_log_parser.py")


@pytest.fixture(scope="module")
def csv_writer_module():
    """加载 exercises/02_csv_writer.py"""
    return _load_exercise_module("_test_csv_writer", EXERCISES_DIR / "02_csv_writer.py")


@pytest.fixture(scope="module")
def file_search_module():
    """加载 exercises/03_file_search.py"""
    return _load_exercise_module("_test_file_search", EXERCISES_DIR / "03_file_search.py")


# ============================================================
# 01_log_parser.py 测试
# ============================================================


class TestLogParser:
    """测试日志解析器"""

    def test_parse_log_counts(self, log_parser_module) -> None:
        """测试日志统计"""
        func = getattr(log_parser_module, "parse_log", None)
        assert func is not None, "请定义 parse_log 函数"

        # 创建临时日志文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write("2024-01-01 INFO: Server started\n")
            f.write("2024-01-02 ERROR: Connection failed\n")
            f.write("2024-01-03 WARNING: Low memory\n")
            f.write("2024-01-04 INFO: Request processed\n")
            f.write("2024-01-05 ERROR: Timeout\n")
            temp_path = f.name

        try:
            stats = func(temp_path)
            assert stats["INFO"] == 2
            assert stats["ERROR"] == 2
            assert stats["WARNING"] == 1
        finally:
            Path(temp_path).unlink()

    def test_find_errors(self, log_parser_module) -> None:
        """测试错误查找"""
        func = getattr(log_parser_module, "find_errors", None)
        assert func is not None, "请定义 find_errors 函数"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
            f.write("Line 1: INFO message\n")
            f.write("Line 2: ERROR: Something went wrong\n")
            f.write("Line 3: DEBUG message\n")
            f.write("Line 4: ERROR: Another error\n")
            temp_path = f.name

        try:
            errors = func(temp_path)
            assert len(errors) == 2
            assert errors[0][0] == 2  # Line number
            assert "ERROR" in errors[0][1]
        finally:
            Path(temp_path).unlink()

    def test_parse_log_file_not_found(self, log_parser_module) -> None:
        """测试文件不存在时的处理"""
        func = getattr(log_parser_module, "parse_log", None)
        # 应该返回空统计而不是崩溃
        stats = func("nonexistent_file.log")
        assert isinstance(stats, dict)
        assert stats.get("INFO", 0) >= 0


# ============================================================
# 03_file_search.py 测试
# ============================================================


class TestFileSearch:
    """测试文件搜索"""

    def test_find_by_extension(self, file_search_module) -> None:
        """测试按扩展名搜索"""
        func = getattr(file_search_module, "find_by_extension", None)
        assert func is not None, "请定义 find_by_extension 函数"

        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试文件
            Path(tmpdir, "test.py").write_text("python code")
            Path(tmpdir, "readme.md").write_text("markdown")
            Path(tmpdir, "subdir").mkdir()
            Path(tmpdir, "subdir/data.py").write_text("python code")

            # 搜索 .py 文件
            results = func(tmpdir, [".py"])
            assert len(results) >= 2  # 至少包含两个 .py 文件

    def test_find_large_files(self, file_search_module) -> None:
        """测试大文件搜索"""
        func = getattr(file_search_module, "find_large_files", None)
        assert func is not None, "请定义 find_large_files 函数"

        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建不同大小的文件
            Path(tmpdir, "small.txt").write_text("x" * 100)
            Path(tmpdir, "large.txt").write_text("x" * 2000)

            results = func(tmpdir, 500)
            assert len(results) >= 1
            # 结果应该按大小降序排列
            if len(results) > 1:
                assert results[0][1] >= results[1][1]

    def test_find_recent_files(self, file_search_module) -> None:
        """测试最近文件搜索"""
        func = getattr(file_search_module, "find_recent_files", None)
        assert func is not None, "请定义 find_recent_files 函数"

        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "recent.txt").write_text("new content")
            Path(tmpdir, "old.txt").write_text("old content")

            # 搜索最近 1 天的文件
            results = func(tmpdir, days=1)
            assert len(results) >= 1

    def test_find_in_directories(self, file_search_module) -> None:
        """测试多目录搜索"""
        func = getattr(file_search_module, "find_in_directories", None)
        assert func is not None, "请定义 find_in_directories 函数"

        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                Path(tmpdir1, "file1.py").write_text("code")
                Path(tmpdir2, "file2.py").write_text("code")

                results = func([tmpdir1, tmpdir2], "*.py")
                assert isinstance(results, dict)
                assert len(results) == 2
