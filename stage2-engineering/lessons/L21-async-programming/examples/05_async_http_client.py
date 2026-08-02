"""

from __future__ import annotations

异步HTTP客户端示例（模拟版）

演示异步HTTP请求的基本模式。
这是一个简化的模拟版本，展示异步HTTP的核心概念。

真实项目请使用 aiohttp 库（见 05_async_http_real.py）

作者: Python 3.13 全栈课程
日期: 2026-06-04
Python版本: 3.12+
"""

import asyncio
import time


async def fetch_url(url: str) -> dict[str, str | int]:
    """
    模拟异步HTTP请求

    在真实项目中，应该使用 aiohttp.ClientSession.get()

    Args:
        url: 请求URL

    Returns:
        响应数据字典，包含 url, status, data 字段
    """
    print(f"→ 请求: {url}")

    # 模拟网络延迟（0.3-0.7秒随机）
    import random

    delay = random.uniform(0.3, 0.7)
    await asyncio.sleep(delay)

    print(f"← 响应: {url} (耗时 {delay:.2f}s)")

    return {
        "url": url,
        "status": 200,
        "data": f"数据来自 {url}",
    }


async def demonstrate_single_request() -> None:
    """演示单个异步请求"""
    print("=" * 60)
    print("1. 单个异步请求")
    print("=" * 60)

    start = time.time()
    response = await fetch_url("https://api.example.com/users/1")
    elapsed = time.time() - start

    print(f"\n结果: {response}")
    print(f"总耗时: {elapsed:.2f}秒\n")


async def demonstrate_sequential_requests() -> None:
    """演示顺序请求（不推荐）"""
    print("=" * 60)
    print("2. 顺序请求（慢）")
    print("=" * 60)

    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
    ]

    start = time.time()

    # 一个接一个地请求（慢！）
    results = []
    for url in urls:
        response = await fetch_url(url)
        results.append(response)

    elapsed = time.time() - start

    print(f"\n完成 {len(results)} 个请求")
    print(f"总耗时: {elapsed:.2f}秒")
    print("⚠️  顺序执行很慢，应该使用并发！\n")


async def demonstrate_concurrent_requests() -> None:
    """演示并发请求（推荐）"""
    print("=" * 60)
    print("3. 并发请求（快）")
    print("=" * 60)

    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
        "https://api.example.com/users/3",
    ]

    start = time.time()

    # 并发请求（快！）
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"\n完成 {len(results)} 个请求")
    print(f"总耗时: {elapsed:.2f}秒")
    print(f"✅ 并发执行，速度提升 {len(urls)}倍！\n")


async def demonstrate_error_handling() -> None:
    """演示错误处理"""
    print("=" * 60)
    print("4. 错误处理")
    print("=" * 60)

    async def fetch_with_error(url: str) -> dict[str, str | int] | None:
        """可能失败的请求"""
        try:
            # 模拟某些请求失败
            if "error" in url:
                raise Exception(f"请求失败: {url}")
            return await fetch_url(url)
        except Exception as e:
            print(f"✗ 错误: {e}")
            return None

    urls = [
        "https://api.example.com/users/1",
        "https://api.example.com/error/404",  # 会失败
        "https://api.example.com/users/2",
    ]

    tasks = [fetch_with_error(url) for url in urls]
    results = await asyncio.gather(*tasks)

    # 过滤掉失败的请求
    success_results = [r for r in results if r is not None]
    print(f"\n成功: {len(success_results)}/{len(urls)} 个请求\n")


async def main() -> None:
    """主函数"""
    print("\n" + "=" * 60)
    print("异步HTTP客户端示例（模拟版）")
    print("=" * 60 + "\n")

    await demonstrate_single_request()
    await demonstrate_sequential_requests()
    await demonstrate_concurrent_requests()
    await demonstrate_error_handling()

    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    print()
    print("💡 要点总结：")
    print("1. 使用 asyncio.gather() 实现并发请求")
    print("2. 并发比顺序快 N 倍（N = 请求数）")
    print("3. 需要妥善处理错误，避免一个失败导致全部失败")
    print("4. 真实项目使用 aiohttp（见 05_async_http_real.py）")


if __name__ == "__main__":
    asyncio.run(main())
