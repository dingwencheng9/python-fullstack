"""练习 1: 同步生成器改写为异步生成器

任务：
将以下同步生成器改写为异步版本，并添加完整类型注解

要求：
1. 使用 AsyncGenerator 类型注解
2. 使用 aiofiles 读取文件
3. 保持原有功能不变
4. 通过 mypy --strict 检查
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

try:
    import aiofiles  # noqa: F401
except ImportError:
    print("请安装 aiofiles: uv add aiofiles")
    raise


# ============================================================================
# 原始同步版本
# ============================================================================


def read_lines_sync(filename: str) -> Generator[str]:
    """同步读取文件行"""
    with open(filename, encoding="utf-8") as f:
        for line in f:
            yield line.strip()


# ============================================================================
# TODO: 学生需要实现的部分
# ============================================================================


async def read_lines_async(filename: str) -> AsyncGenerator[str]:
    """
    异步读取文件行

    TODO: 实现以下功能
    1. 使用 aiofiles.open() 打开文件
    2. 使用 async for 读取每一行
    3. 使用 yield 产生每一行（去除首尾空白）
    4. 确保文件正确关闭（使用 async with）

    参数:
        filename: 文件路径

    产出:
        文件的每一行（去除首尾空白）

    示例:
        async for line in read_lines_async("test.txt"):
            print(line)
    """
    # TODO: 实现
    raise NotImplementedError("请实现 read_lines_async")
    yield  # 使其成为生成器（移除此行并实现真正的 yield）


# ============================================================================
# 测试代码
# ============================================================================


async def test_read_lines_async() -> None:
    """测试异步读取"""
    # 创建测试文件
    test_file = Path("/tmp/test_async_read.txt")
    test_file.write_text(
        "Line 1\nLine 2\nLine 3\n  Line 4 with spaces  \nLine 5\n",
        encoding="utf-8",
    )

    print("测试异步读取文件:\n")

    try:
        async for line in read_lines_async(str(test_file)):
            print(f"  读取: {line!r}")

        print("\n✓ 测试通过")

    except NotImplementedError:
        print("✗ 请先实现 read_lines_async 函数")

    finally:
        # 清理测试文件
        test_file.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(test_read_lines_async())
