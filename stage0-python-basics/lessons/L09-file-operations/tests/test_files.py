"""L05 文件操作 - 测试用例"""

import json
import os
from pathlib import Path
import tempfile

import pytest

# ============================================================
# 基础文件读写
# ============================================================


def test_read_file():
    """测试文本文件读取"""
    path = Path("test_read.txt")
    path.write_text("test content")
    try:
        assert path.read_text() == "test content"
    finally:
        path.unlink(missing_ok=True)


def test_write_file():
    """测试文本文件写入"""
    path = Path("test_write.txt")
    path.write_text("hello")
    try:
        assert path.exists()
    finally:
        path.unlink(missing_ok=True)


# ============================================================
# 参数化：文件操作
# ============================================================


@pytest.mark.parametrize(
    "content,encoding",
    [
        ("Hello World", "utf-8"),
        ("你好世界", "utf-8"),
        ("café", "utf-8"),
        ("Line1\nLine2\nLine3", "utf-8"),
    ],
)
def test_write_read_encodings(content, encoding):
    """参数化：不同内容编码的写入读取"""
    path = Path("test_enc.txt")
    path.write_text(content, encoding=encoding)
    try:
        assert path.read_text(encoding=encoding) == content
    finally:
        path.unlink(missing_ok=True)


# ============================================================
# 二进制文件操作
# ============================================================


def test_binary_write_read():
    """测试二进制文件写入读取"""
    data = b"\x00\x01\x02\xff\xfe"
    path = Path("test_bin.bin")
    path.write_bytes(data)
    try:
        assert path.read_bytes() == data
    finally:
        path.unlink(missing_ok=True)


def test_file_not_found():
    """测试读取不存在文件抛出异常"""
    with pytest.raises(FileNotFoundError):
        Path("nonexistent_file_xyz.txt").read_text()


# ============================================================
# Context Manager
# ============================================================


def test_context_manager_write():
    """测试 with 语句写入文件"""
    path = Path("test_cm.txt")
    try:
        with open(path, "w") as f:
            f.write("context manager test")
        assert path.read_text() == "context manager test"
    finally:
        path.unlink(missing_ok=True)


def test_context_manager_read():
    """测试 with 语句读取文件"""
    path = Path("test_cm_read.txt")
    path.write_text("read me")
    try:
        with open(path) as f:
            content = f.read()
        assert content == "read me"
    finally:
        path.unlink(missing_ok=True)


# ============================================================
# JSON 文件操作
# ============================================================


def test_json_write_read():
    """测试 JSON 序列化和反序列化"""
    data = {"name": "Alice", "age": 25, "scores": [90, 85, 88]}
    path = Path("test.json")
    path.write_text(json.dumps(data))
    try:
        loaded = json.loads(path.read_text())
        assert loaded == data
    finally:
        path.unlink(missing_ok=True)


def test_json_invalid():
    """测试无效 JSON 抛出异常"""
    with pytest.raises(json.JSONDecodeError):
        json.loads("not valid json {{{")


# ============================================================
# 文件模式与权限
# ============================================================


def test_append_mode():
    """测试追加模式写入"""
    path = Path("test_append.txt")
    try:
        path.write_text("line1\n")
        with open(path, "a") as f:
            f.write("line2\n")
        lines = path.read_text().strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "line1"
        assert lines[1] == "line2"
    finally:
        path.unlink(missing_ok=True)


def test_file_exists_check():
    """测试文件存在性检查"""
    path = Path("test_exists.txt")
    path.write_text("data")
    try:
        assert path.exists()
        assert path.is_file()
        assert not path.is_dir()
    finally:
        path.unlink(missing_ok=True)


# ============================================================
# 临时文件
# ============================================================


def test_tempfile_usage():
    """测试临时文件创建与清理"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("temp data")
        temp_path = f.name

    try:
        assert os.path.exists(temp_path)
        assert Path(temp_path).read_text() == "temp data"
    finally:
        os.unlink(temp_path)
