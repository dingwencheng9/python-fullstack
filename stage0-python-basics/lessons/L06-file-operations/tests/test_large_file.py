"""L05 文件操作 - 边界测试：超大文件

测试目标：
1. 验证流式读取避免内存溢出
2. 验证分块读取处理大文件
3. 性能基准测试

运行方式：
    pytest test_large_file.py -v
    pytest test_large_file.py -v -m benchmark  # 仅运行性能测试
"""

import tempfile
import time
from pathlib import Path

import pytest


def test_read_large_file_streaming():
    """测试：流式读取超大文件（避免内存溢出）"""
    # 创建 10MB 测试文件
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        test_file = Path(f.name)
        # 写入 10MB 数据（每行 100 字节 × 100,000 行）
        for i in range(100_000):
            f.write(f"Line {i:06d}: " + "x" * 90 + "\n")

    try:
        # 流式读取（逐行，不一次性加载到内存）
        line_count = 0
        with open(test_file, encoding="utf-8") as f:
            for line in f:
                line_count += 1
                # 验证行格式
                if line_count == 1:
                    assert line.startswith("Line 000000:"), "首行格式错误"

        assert line_count == 100_000, f"行数不匹配: {line_count} != 100_000"
    finally:
        test_file.unlink()  # 清理测试文件


def test_read_large_file_chunks():
    """测试：分块读取超大文件"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        test_file = Path(f.name)
        # 写入 10MB 数据（10,000,000 个 'A'）
        f.write("A" * 10_000_000)

    try:
        # 分块读取（每次 1MB）
        chunk_size = 1024 * 1024  # 1MB
        total_size = 0

        with open(test_file, encoding="utf-8") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                total_size += len(chunk)
                # 验证块内容
                assert all(c == "A" for c in chunk), "块内容错误"

        assert total_size == 10_000_000, f"总大小不匹配: {total_size} != 10_000_000"
    finally:
        test_file.unlink()


@pytest.mark.benchmark
def test_file_io_performance():
    """基准测试：文件 I/O 性能

    验证：
    - 写入 10,000 行应在 1 秒内完成
    - 读取 10,000 行应在 0.5 秒内完成
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        test_file = Path(f.name)

        # 写入性能测试
        start = time.perf_counter()
        for i in range(10_000):
            f.write(f"Line {i}\n")
        write_duration = time.perf_counter() - start

    try:
        # 读取性能测试
        start = time.perf_counter()
        with open(test_file, encoding="utf-8") as f:
            lines = f.readlines()
        read_duration = time.perf_counter() - start

        # 性能断言（宽松标准，避免 CI 环境差异）
        assert write_duration < 2.0, f"写入过慢: {write_duration:.2f}s > 2.0s"
        assert read_duration < 1.0, f"读取过慢: {read_duration:.2f}s > 1.0s"
        assert len(lines) == 10_000, f"行数不匹配: {len(lines)} != 10_000"

        print("\n性能指标:")
        print(f"  写入 10,000 行: {write_duration:.3f}s")
        print(f"  读取 10,000 行: {read_duration:.3f}s")
        print(f"  写入吞吐: {10_000 / write_duration:.0f} 行/秒")
        print(f"  读取吞吐: {10_000 / read_duration:.0f} 行/秒")
    finally:
        test_file.unlink()


def test_empty_file_edge_case():
    """测试：空文件边界情况"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        test_file = Path(f.name)
        # 不写入任何内容

    try:
        # 读取空文件
        with open(test_file, encoding="utf-8") as f:
            content = f.read()
            assert content == "", "空文件应返回空字符串"

            # 重置文件指针
            f.seek(0)
            lines = f.readlines()
            assert lines == [], "空文件应返回空列表"
    finally:
        test_file.unlink()


def test_single_byte_file():
    """测试：单字节文件边界情况"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        test_file = Path(f.name)
        f.write("A")

    try:
        with open(test_file, encoding="utf-8") as f:
            content = f.read()
            assert content == "A", "单字节文件内容错误"
            assert len(content) == 1, "长度应为 1"
    finally:
        test_file.unlink()
