"""装饰器示例 - 展示日志、缓存、重试等装饰器"""

from __future__ import annotations

import asyncio
import functools
import logging
import time
from collections.abc import Callable

logger = logging.getLogger(__name__)


def logged(func: Callable[..., object]) -> Callable[..., object]:
    """记录函数调用的日志装饰器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"调用 {func.__name__} (args={args}, kwargs={kwargs})")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} 返回 {result}")
            return result
        except Exception:
            logger.exception(f"{func.__name__} 异常")
            raise

    return wrapper


def async_logged(func: Callable[..., object]) -> Callable[..., object]:
    """异步函数的日志装饰器"""

    @functools.wraps(func)
    async def wrapper(*args: object, **kwargs: object) -> object:
        logger.debug(f"调用 {func.__name__}")
        result = await func(*args, **kwargs)
        logger.debug(f"{func.__name__} 完成")
        return result

    return wrapper  # type: ignore


def memoized(maxsize: int = 128) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """带配置的最大结果缓存装饰器"""

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        cached_func = functools.lru_cache(maxsize=maxsize)(func)
        return cached_func

    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """失败自动重试的装饰器"""

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
            raise last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


# 使用示例
@memoized(maxsize=256)
def expensive_computation(task_id: str) -> dict:
    """耗时的计算操作"""
    time.sleep(0.1)
    return {"task_id": task_id, "result": "computed"}


@retry(max_attempts=3, delay=0.5)
async def fetch_data(url: str) -> dict:
    """模拟网络请求"""
    await asyncio.sleep(0.1)
    if "error" in url:
        raise ConnectionError("Network error")
    return {"url": url, "status": 200}


# 运行示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # 测试缓存
    print("Testing memoized decorator...")
    start = time.time()
    result1 = expensive_computation("task-1")
    print(f"First call: {result1} ({time.time() - start:.3f}s)")

    start = time.time()
    result2 = expensive_computation("task-1")
    print(f"Second call (cached): {result2} ({time.time() - start:.3f}s)")

    # 测试重试
    print("\nTesting retry decorator...")
    asyncio.run(fetch_data("https://example.com"))
    print("Success!")
