"""练习 1 答案: 同步生成器改写为异步生成器

【解题思路】
1. 理解异步生成器的核心概念：
   - 使用 async def 定义异步生成器函数
   - 使用 yield 产出值（与同步生成器相同）
   - 使用 async for 消费异步生成器
   - 返回类型注解为 AsyncGenerator[YieldType, SendType]

2. 改写策略：
   - 将 def 改为 async def
   - 使用 aiofiles.open() 替代内置 open()
   - 使用 async with 管理异步上下文
   - 使用 async for 异步迭代文件行
   - yield 语句保持不变（异步生成器也使用 yield）

3. 类型注解：
   - AsyncGenerator[str, None] 表示产出 str，不接收 send 值
   - 导入自 collections.abc（Python 3.9+）

4. 测试要点：
   - 使用 async for 消费生成器
   - 验证每行正确去除首尾空白
   - 清理测试文件

【关键知识点】
- AsyncGenerator vs Generator：异步版本支持 await 表达式
- aiofiles 库：异步文件 I/O（函数内延迟导入）
- async with：异步上下文管理器
- async for：异步迭代器协议
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path


async def read_lines_async(filename: str) -> AsyncGenerator[str]:
    """
    异步读取文件行

    参数:
        filename: 文件路径

    产出:
        文件的每一行（去除首尾空白）
    """
    import aiofiles  # 延迟导入，避免 collection 阶段失败

    async with aiofiles.open(filename, encoding="utf-8") as f:
        async for line in f:
            yield line.strip()


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

    lines: list[str] = []
    async for line in read_lines_async(str(test_file)):
        print(f"  读取: {line!r}")
        lines.append(line)

    # 验证结果
    assert lines == ["Line 1", "Line 2", "Line 3", "Line 4 with spaces", "Line 5"]
    print("\n✓ 测试通过")

    # 清理测试文件
    test_file.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(test_read_lines_async())
