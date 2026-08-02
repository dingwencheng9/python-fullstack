"""练习 1: 异步生成器 - 参考答案

===============================================================================
解题思路
===============================================================================

将同步生成器改写为异步生成器的核心要点：

1. 生成器类型注解：AsyncGenerator[YieldType, SendType]
2. 使用 aiofiles 替代标准 open()
3. async def + yield 定义异步生成器
4. async with 管理异步资源
5. async for 消费异步生成器

===============================================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path


async def read_lines_async(filename: str) -> AsyncGenerator[str]:
    """
    异步读取文件行

    关键实现：
    - async with aiofiles.open() 异步打开文件
    - async for 异步迭代文件对象
    - yield 产出每一行
    """
    import aiofiles  # 延迟导入，避免 collection 阶段失败

    async with aiofiles.open(filename, encoding="utf-8") as f:
        async for line in f:
            yield line.strip()


async def read_lines_with_line_numbers(
    filename: str,
) -> AsyncGenerator[tuple[int, str]]:
    """带行号的异步读取"""
    import aiofiles  # 延迟导入，避免 collection 阶段失败

    line_number = 0
    async with aiofiles.open(filename, encoding="utf-8") as f:
        async for line in f:
            line_number += 1
            yield (line_number, line.strip())


# ============================================================================
# 测试代码
# ============================================================================


async def test_read_lines_async() -> None:
    """测试基本异步读取"""
    test_file = Path("/tmp/test_async_read.txt")
    test_file.write_text("Line 1\nLine 2\nLine 3\n", encoding="utf-8")

    print("测试: 异步读取文件")
    lines: list[str] = []
    async for line in read_lines_async(str(test_file)):
        print(f"  {line}")
        lines.append(line)

    assert lines == ["Line 1", "Line 2", "Line 3"]
    print("✓ 测试通过\n")
    test_file.unlink(missing_ok=True)


async def main() -> None:
    """主测试函数"""
    print("=" * 60)
    print("L22 练习 1: 异步生成器 - 参考答案")
    print("=" * 60)
    print()

    await test_read_lines_async()

    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
