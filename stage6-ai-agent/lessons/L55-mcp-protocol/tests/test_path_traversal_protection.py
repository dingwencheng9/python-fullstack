"""测试 FileSearchServer 的路径穿越防护。"""

from __future__ import annotations

import importlib.util
from pathlib import Path


LESSON_DIR = Path(__file__).parent.parent


def load_file_search_module():
    """加载 FileSearchServer 模块。"""
    spec = importlib.util.spec_from_file_location(
        "file_search",
        LESSON_DIR / "solutions" / "01_file_search_tool.py",
    )
    if spec is None or spec.loader is None:
        raise ImportError("无法加载模块")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_file_search_blocks_path_traversal(tmp_path: Path) -> None:
    """测试 FileSearchServer 阻止路径穿越攻击。"""
    mod = load_file_search_module()

    # 创建受保护的根目录
    safe_root = tmp_path / "safe"
    safe_root.mkdir()
    (safe_root / "allowed.py").write_text("safe content")

    # 创建根目录外的敏感文件
    sensitive_dir = tmp_path / "sensitive"
    sensitive_dir.mkdir()
    (sensitive_dir / "secret.py").write_text("secret content")

    # 创建 FileSearchServer，只允许访问 safe_root
    server = mod.FileSearchServer(safe_root)

    # 正常情况：应该能找到 safe_root 内的文件
    result = server.search_files("safe")
    assert "allowed.py" in result

    # 攻击场景：不应该能访问到 safe_root 外的文件
    result = server.search_files("secret")
    assert "secret.py" not in result


def test_file_search_only_within_root(tmp_path: Path) -> None:
    """测试 FileSearchServer 只搜索根目录内的文件。"""
    mod = load_file_search_module()

    # 创建嵌套目录结构
    root = tmp_path / "root"
    root.mkdir()
    (root / "file1.py").write_text("content1")

    subdir = root / "subdir"
    subdir.mkdir()
    (subdir / "file2.py").write_text("content2")

    # 根目录外的文件
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "file3.py").write_text("content3")

    # 实例化 server
    server = mod.FileSearchServer(root)

    # 应该能找到根目录及子目录内的文件
    result1 = server.search_files("content1")
    assert "file1.py" in result1

    result2 = server.search_files("content2")
    assert "file2.py" in result2

    # 不应该能找到根目录外的文件
    result3 = server.search_files("content3")
    assert "file3.py" not in result3
    assert result3 == "no matches"
