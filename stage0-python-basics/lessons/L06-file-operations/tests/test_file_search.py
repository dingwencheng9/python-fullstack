"""L05 目录文件搜索 - 测试用例"""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import pytest

# 直接计算路径，不依赖 conftest
LESSON_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = LESSON_ROOT / "solutions"
_FILE_SEARCH_PATH = SOLUTIONS_DIR / "03_file_search_solution.py"


def _load_module(name: str, file_path: Path):
    """按物理路径加载模块。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 加载 file_search 解决方案
if _FILE_SEARCH_PATH.exists():
    _file_search = _load_module("_test_file_search", _FILE_SEARCH_PATH)
else:
    _file_search = None


def _create_test_tree() -> Path:
    """创建测试目录树并返回根路径。"""
    root = Path(tempfile.mkdtemp())

    (root / "script.py").write_text("print('hello')")
    (root / "data.txt").write_text("some data")
    (root / "README.md").write_text("# Readme")
    (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (root / "subdir").mkdir()
    (root / "subdir" / "nested.py").write_text("x = 1")
    (root / "subdir" / "deep").mkdir()
    (root / "subdir" / "deep" / "utils.py").write_text("def foo(): pass")

    # 创建大文件 (> 500 字节)
    big = root / "big_file.txt"
    big.write_text("x" * 1000)

    return root


@pytest.mark.skipif(_file_search is None, reason="file_search 未实现")
class TestFindByExtension:
    """find_by_extension 测试。"""

    def test_find_py_files(self):
        """测试搜索 .py 文件。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_by_extension(str(root), [".py"])
            paths = [Path(p).name for p in result]
            assert "script.py" in paths
            assert "nested.py" in paths
            assert "utils.py" in paths
            assert "data.txt" not in paths
        finally:
            import shutil

            shutil.rmtree(root)

    def test_find_multiple_extensions(self):
        """测试搜索多种扩展名。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_by_extension(str(root), [".py", ".md"])
            paths = [Path(p).name for p in result]
            assert "script.py" in paths
            assert "README.md" in paths
            assert "data.txt" not in paths
        finally:
            import shutil

            shutil.rmtree(root)

    def test_case_insensitive(self):
        """测试扩展名不区分大小写。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_by_extension(str(root), [".PY", ".Md"])
            assert len(result) >= 3
        finally:
            import shutil

            shutil.rmtree(root)

    def test_empty_result(self):
        """测试没有匹配文件时返回空列表。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_by_extension(str(root), [".xyz"])
            assert result == []
        finally:
            import shutil

            shutil.rmtree(root)

    def test_nonexistent_dir(self):
        """测试目录不存在时返回空列表。"""
        result = _file_search.find_by_extension("/nonexistent/path/xyz", [".py"])
        assert result == []


@pytest.mark.skipif(_file_search is None, reason="file_search 未实现")
class TestFindLargeFiles:
    """find_large_files 测试。"""

    def test_find_large_files(self):
        """测试搜索超过阈值的文件。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_large_files(str(root), 500)
            paths = [Path(p).name for p, _ in result]
            assert "big_file.txt" in paths
            # 小文件不应出现
            for name, _ in result:
                assert Path(name).stat().st_size >= 500
        finally:
            import shutil

            shutil.rmtree(root)

    def test_sorted_by_size(self):
        """测试结果按大小降序排列。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_large_files(str(root), 100)
            sizes = [size for _, size in result]
            assert sizes == sorted(sizes, reverse=True)
        finally:
            import shutil

            shutil.rmtree(root)


@pytest.mark.skipif(_file_search is None, reason="file_search 未实现")
class TestFindRecentFiles:
    """find_recent_files 测试。"""

    def test_find_recent_files(self):
        """测试搜索最近修改的文件。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_recent_files(str(root), days=7)
            assert len(result) >= 5
        finally:
            import shutil

            shutil.rmtree(root)

    def test_sorted_by_mtime(self):
        """测试结果按修改时间降序排列。"""
        root = _create_test_tree()
        try:
            result = _file_search.find_recent_files(str(root), days=7)
            mtimes = [mtime for _, mtime in result]
            assert mtimes == sorted(mtimes, reverse=True)
        finally:
            import shutil

            shutil.rmtree(root)


@pytest.mark.skipif(_file_search is None, reason="file_search 未实现")
class TestFindInDirectories:
    """find_in_directories 测试。"""

    def test_find_in_multiple_dirs(self):
        """测试在多个目录中搜索。"""
        root1 = _create_test_tree()
        root2 = Path(tempfile.mkdtemp())
        (root2 / "extra.py").write_text("y = 2")
        try:
            result = _file_search.find_in_directories([str(root1), str(root2)], "*.py")
            assert len(result[str(root1)]) >= 3
            assert len(result[str(root2)]) >= 1
        finally:
            import shutil

            shutil.rmtree(root1)
            shutil.rmtree(root2)

    def test_missing_dir_returns_empty_list(self):
        """测试不存在的目录返回空列表。"""
        result = _file_search.find_in_directories(["/nonexistent"], "*.py")
        assert result["/nonexistent"] == []
