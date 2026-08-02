"""

from __future__ import annotations

练习 4: 异步上下文管理器 - 参考答案

===============================================================================
解题思路: 实现 __aenter__ 和 __aexit__ 管理异步资源
===============================================================================

Python 版本要求: 3.11+ (Self 类型标注)
"""

import asyncio
from typing import Self  # Python 3.11+: Self 用于标注返回自身实例的方法


class AsyncDatabase:
    """异步数据库连接"""

    def __init__(self, host: str):
        self.host = host
        self.connected = False

    async def __aenter__(self) -> Self:
        """建立连接"""
        print(f"连接到 {self.host}")
        await asyncio.sleep(0.3)
        self.connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """关闭连接"""
        print("关闭连接")
        await asyncio.sleep(0.2)
        self.connected = False
        return False

    async def query(self, sql: str) -> list[dict]:
        """执行查询"""
        if not self.connected:
            raise RuntimeError("数据库未连接")
        print(f"执行: {sql}")
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Alice"}]


class AsyncFileWriter:
    """异步文件写入器"""

    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    async def __aenter__(self) -> Self:
        """打开文件"""
        print(f"打开文件: {self.filename}")
        await asyncio.sleep(0.1)
        # 模拟异步文件打开
        self.file = open(self.filename, "w")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """关闭文件"""
        if self.file:
            print(f"关闭文件: {self.filename}")
            self.file.close()
            await asyncio.sleep(0.1)
        return False

    async def write(self, data: str):
        """写入数据"""
        if not self.file:
            raise RuntimeError("文件未打开")
        print(f"写入: {data}")
        self.file.write(data + "\n")
        await asyncio.sleep(0.05)


async def test_database():
    """测试数据库上下文管理器"""
    print("测试 1: AsyncDatabase")

    async with AsyncDatabase("localhost:5432") as db:
        results = await db.query("SELECT * FROM users")
        print(f"查询结果: {results}")

    print("✅ 数据库测试通过\n")


async def test_file_writer():
    """测试文件写入器"""
    print("测试 2: AsyncFileWriter")

    async with AsyncFileWriter("/tmp/test_async.txt") as writer:
        await writer.write("Line 1")
        await writer.write("Line 2")

    print("✅ 文件写入测试通过\n")


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("练习 4: 异步上下文管理器")
    print("=" * 60)
    print()

    await test_database()
    await test_file_writer()

    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
