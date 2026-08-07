"""
L16: 并发编程 - async/await 练习

实现异步函数和并发任务。
"""

import asyncio


async def delay(seconds: float, value: str) -> str:
    """模拟异步延迟"""
    await asyncio.sleep(seconds)
    return value


async def gather_results() -> list[str]:
    """并发获取多个结果。

    ``gather`` 会同时调度多个协程，并按传入顺序返回结果。
    """
    results = await asyncio.gather(
        delay(0.3, "A"),
        delay(0.2, "B"),
        delay(0.1, "C"),
    )
    return list(results)


async def sequential_results() -> list[str]:
    """顺序获取多个结果。"""
    results = []
    for value in ["A", "B", "C"]:
        results.append(await delay(0.1, value))
    return results


async def with_timeout_coro() -> str:
    """超时处理练习。"""
    try:
        return await asyncio.wait_for(delay(5.0, "完成"), timeout=0.1)
    except TimeoutError:
        return "超时"


# === 验证 ===

if __name__ == "__main__":

    async def main():
        # 测试并发
        results = await gather_results()
        assert results == ["A", "B", "C"]

        # 测试顺序
        results = await sequential_results()
        assert results == ["A", "B", "C"]

        # 测试超时
        result = await with_timeout_coro()
        assert result == "超时"
        print("超时正确触发")

    asyncio.run(main())

    print("✅ 所有测试通过！")
