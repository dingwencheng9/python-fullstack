"""

from __future__ import annotations

L20 练习 2: 带参数的装饰器

学习目标：
- 实现装饰器工厂函数
- 掌握三层嵌套结构
- 实现可选参数装饰器

难度：★★★☆☆
预计时间：45-60 分钟
"""

from collections.abc import Callable
from functools import wraps
import sys
import time

# ==================== 任务 1: 重试装饰器 ====================


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """函数失败时按退避策略重试。"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    print(f"Attempt {attempt}/{max_attempts} failed: {exc}")
                    if attempt == max_attempts:
                        raise
                    print(f"Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


# ==================== 任务 2: 超时装饰器 ====================


def timeout(seconds: float):
    """函数执行完成后检查耗时，超过限制则抛出 TimeoutError。"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed > seconds:
                print(f"{func.__name__} timed out after {elapsed:.2f}s")
                raise TimeoutError(
                    f"Function took {elapsed:.2f}s, limit was {seconds}s"
                )
            return result

        return wrapper

    return decorator


# ==================== 任务 3: 限流装饰器 ====================


def rate_limit(max_calls: int, period: float):
    """滑动窗口限流；达到上限时等待到窗口可用。"""
    if max_calls <= 0:
        raise ValueError("max_calls must be > 0")
    if period <= 0:
        raise ValueError("period must be > 0")

    call_times: list[float] = []

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_times
            now = time.time()
            call_times = [ts for ts in call_times if now - ts < period]
            if len(call_times) >= max_calls:
                wait_time = period - (now - call_times[0])
                if wait_time > 0:
                    print(f"Rate limit reached, waiting {wait_time:.2f}s")
                    time.sleep(wait_time)
                now = time.time()
                call_times = [ts for ts in call_times if now - ts < period]
            call_times.append(time.time())
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ==================== 任务 4: 缓存装饰器（带过期时间）====================


def cache_with_ttl(ttl: float = 60.0):
    """带 TTL 的结果缓存装饰器。"""

    def decorator(func: Callable) -> Callable:
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache:
                result, expire_time = cache[key]
                if now < expire_time:
                    return result
                del cache[key]
            result = func(*args, **kwargs)
            cache[key] = (result, now + ttl)
            return result

        return wrapper

    return decorator


# ==================== 任务 5: 权限装饰器 ====================


def require_permission(*permissions: str):
    """要求用户拥有任一指定权限。"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user is None:
                raise PermissionError("Not authenticated")
            if not any(permission in user.permissions for permission in permissions):
                raise PermissionError(f"Required permissions: {permissions}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


# ==================== 任务 6: 可选参数装饰器 ====================


def debug(func: Callable | None = None, *, prefix: str = "DEBUG"):
    """支持 @debug 和 @debug(prefix=...) 两种形式的调试装饰器。"""

    def decorator(inner_func: Callable) -> Callable:
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            print(f"[{prefix}] Calling {inner_func.__name__}")
            result = inner_func(*args, **kwargs)
            print(f"[{prefix}] {inner_func.__name__} returned {result!r}")
            return result

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


# ==================== 测试代码 ====================


def test_retry():
    """测试重试装饰器"""
    print("\n测试 1: 重试装饰器")
    print("=" * 50)

    attempt_count = 0

    @retry(max_attempts=3, delay=0.01, backoff=2)
    def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError(f"Attempt {attempt_count} failed")
        return "Success"

    result = flaky_function()
    assert result == "Success", "函数应该最终成功"
    assert attempt_count == 3, f"应该尝试 3 次，实际 {attempt_count} 次"

    # 测试最终失败的情况
    @retry(max_attempts=2, delay=0.01, backoff=1)
    def always_fail():
        raise RuntimeError("Always fails")

    try:
        always_fail()
        raise AssertionError("应该抛出异常")
    except RuntimeError as e:
        assert str(e) == "Always fails", "应该抛出原始异常"

    print("✅ 重试装饰器测试通过")


def test_timeout():
    """测试超时装饰器"""
    print("\n测试 2: 超时装饰器")
    print("=" * 50)

    @timeout(0.2)
    def fast_function():
        time.sleep(0.05)
        return "Done"

    result = fast_function()
    assert result == "Done", "快速函数应该正常执行"

    @timeout(0.1)
    def slow_function():
        time.sleep(0.3)
        return "Should not reach here"

    try:
        slow_function()
        raise AssertionError("应该抛出 TimeoutError")
    except TimeoutError:
        pass  # 预期的异常

    print("✅ 超时装饰器测试通过")


def test_rate_limit():
    """测试限流装饰器"""
    print("\n测试 3: 限流装饰器")
    print("=" * 50)

    call_times = []

    @rate_limit(max_calls=3, period=0.5)
    def api_call():
        call_times.append(time.time())
        return "OK"

    # 快速调用 5 次
    for _ in range(5):
        api_call()

    # 前 3 次应该很快，第 4 次会有延迟
    assert len(call_times) == 5, "应该调用 5 次"

    # 检查前 3 次的时间间隔很小
    for i in range(2):
        interval = call_times[i + 1] - call_times[i]
        assert interval < 0.1, f"前 3 次调用应该很快，实际间隔 {interval}s"

    # 第 4 次应该有明显延迟
    delay_before_4th = call_times[3] - call_times[2]
    assert delay_before_4th > 0.4, (
        f"第 4 次调用应该有延迟，实际延迟 {delay_before_4th}s"
    )

    print("✅ 限流装饰器测试通过")


def test_cache_with_ttl():
    """测试带过期时间的缓存装饰器"""
    print("\n测试 4: 带过期时间的缓存装饰器")
    print("=" * 50)

    call_count = 0

    @cache_with_ttl(ttl=0.2)
    def get_data(key):
        nonlocal call_count
        call_count += 1
        return f"data_{key}_{call_count}"

    # 第一次调用
    result1 = get_data("a")
    assert call_count == 1, "第一次应该调用函数"

    # 缓存有效期内
    result2 = get_data("a")
    assert call_count == 1, "缓存有效期内不应该调用函数"
    assert result1 == result2, "应该返回相同的缓存结果"

    # 等待缓存过期
    time.sleep(0.3)

    # 缓存过期后
    result3 = get_data("a")
    assert call_count == 2, "缓存过期后应该重新调用函数"
    assert result1 != result3, "过期后应该返回新结果"

    print("✅ 带过期时间的缓存装饰器测试通过")


def test_require_permission():
    """测试权限装饰器"""
    print("\n测试 5: 权限装饰器")
    print("=" * 50)

    class User:
        def __init__(self, permissions):
            self.permissions = set(permissions)

    @require_permission("admin", "moderator")
    def delete_post(post_id, user=None):
        return f"Deleted {post_id}"

    # 管理员权限
    admin = User(["admin", "read", "write"])
    result = delete_post(123, user=admin)
    assert result == "Deleted 123", "管理员应该可以删除"

    # 版主权限
    moderator = User(["moderator"])
    result = delete_post(456, user=moderator)
    assert result == "Deleted 456", "版主应该可以删除"

    # 普通用户
    guest = User(["read"])
    try:
        delete_post(789, user=guest)
        raise AssertionError("普通用户不应该有权限")
    except PermissionError:
        pass  # 预期的异常

    # 未登录
    try:
        delete_post(999, user=None)
        raise AssertionError("未登录不应该有权限")
    except PermissionError:
        pass  # 预期的异常

    print("✅ 权限装饰器测试通过")


def test_debug():
    """测试可选参数装饰器"""
    print("\n测试 6: 可选参数装饰器")
    print("=" * 50)

    @debug
    def add(a, b):
        return a + b

    @debug(prefix="INFO")
    def multiply(a, b):
        return a * b

    result1 = add(3, 5)
    assert result1 == 8, "函数返回值错误"

    result2 = multiply(3, 5)
    assert result2 == 15, "函数返回值错误"

    print("✅ 可选参数装饰器测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("L20 练习 2: 带参数的装饰器")
    print("=" * 50)

    try:
        test_retry()
        test_timeout()
        test_rate_limit()
        test_cache_with_ttl()
        test_require_permission()
        test_debug()

        print("\n" + "=" * 50)
        print("🎉 所有测试通过！")
        print("=" * 50)
        print("\n✅ 完成情况:")
        print("  ✅ 任务 1: 重试装饰器")
        print("  ✅ 任务 2: 超时装饰器")
        print("  ✅ 任务 3: 限流装饰器")
        print("  ✅ 任务 4: 带过期时间的缓存装饰器")
        print("  ✅ 任务 5: 权限装饰器")
        print("  ✅ 任务 6: 可选参数装饰器")
        print("\n🎓 恭喜！你已经掌握了带参数的装饰器。")
        print("💡 下一步：尝试 exercise_03_class_decorators.py")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        print("💡 提示: 请检查你的实现，确保符合所有要求")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        print("💡 提示: 请检查你的代码是否有语法错误或逻辑错误")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
