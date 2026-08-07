"""L14 练习 1 测试: 带参装饰器

测试速率限制、废弃警告、记忆化缓存装饰器。
"""

import pytest
import time
import warnings


class TestRateLimit:
    """速率限制装饰器测试"""

    def test_rate_limit_allows_calls_within_limit(self):
        """在限制内的调用应该成功"""
        from solutions import rate_limit

        call_count = 0

        @rate_limit(calls=3, period=1)
        def limited_func():
            nonlocal call_count
            call_count += 1
            return "success"

        # 连续 3 次调用应该成功
        for i in range(3):
            result = limited_func()
            assert result == "success"

        assert call_count == 3

    def test_rate_limit_blocks_excess_calls(self):
        """超过限制的调用应该抛出异常"""
        from solutions import rate_limit

        @rate_limit(calls=2, period=1)
        def limited_func():
            return "success"

        # 前 2 次成功
        limited_func()
        limited_func()

        # 第 3 次应该失败
        with pytest.raises(RuntimeError, match="速率限制"):
            limited_func()

    def test_rate_limit_resets_after_period(self):
        """超过时间周期后应该重置"""
        from solutions import rate_limit

        @rate_limit(calls=1, period=0.2)
        def limited_func():
            return "success"

        # 第一次成功
        limited_func()

        # 等待周期结束
        time.sleep(0.3)

        # 应该可以再次调用
        result = limited_func()
        assert result == "success"


class TestDeprecated:
    """废弃警告装饰器测试"""

    def test_deprecated_warns(self):
        """调用废弃函数应该发出警告"""
        from solutions import deprecated

        @deprecated(reason="Use new_func instead")
        def old_func():
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_func()

            assert result == "old"
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "已废弃" in str(w[0].message)
            assert "Use new_func instead" in str(w[0].message)


class TestMemoize:
    """记忆化缓存装饰器测试"""

    def test_memoize_caches_result(self):
        """相同参数应该使用缓存"""
        from solutions import memoize

        call_count = 0

        @memoize(ttl=60)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # 第一次调用
        result1 = expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # 第二次相同参数调用（使用缓存）
        result2 = expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # 没有增加

    def test_memoize_different_args(self):
        """不同参数应该重新计算"""
        from solutions import memoize

        call_count = 0

        @memoize(ttl=60)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        expensive_func(5)
        expensive_func(10)

        assert call_count == 2

    def test_memoize_expires_after_ttl(self):
        """缓存应该在 TTL 后过期"""
        from solutions import memoize

        call_count = 0

        @memoize(ttl=1)
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        expensive_func(5)
        assert call_count == 1

        time.sleep(1.1)

        expensive_func(5)
        assert call_count == 2  # 重新计算

    def test_memoize_cache_clear(self):
        """应该可以通过 cache_clear 清除缓存"""
        from solutions import memoize

        @memoize(ttl=60)
        def expensive_func(x):
            return x * 2

        expensive_func(5)
        expensive_func(5)  # 缓存

        expensive_func.cache_clear()

        # 缓存信息应该显示为空
        info = expensive_func.cache_info()
        assert info["size"] == 0


class TestDecoratorSignature:
    """装饰器签名测试"""

    def test_rate_limit_preserves_function_name(self):
        """装饰器应该保留原函数名"""
        from solutions import rate_limit

        @rate_limit(calls=10)
        def my_function():
            return "test"

        assert my_function.__name__ == "my_function"

    def test_memoize_preserves_function_docstring(self):
        """装饰器应该保留原函数文档字符串"""
        from solutions import memoize

        @memoize(ttl=60)
        def my_function():
            """This is my docstring"""
            return "test"

        assert my_function.__doc__ == "This is my docstring"
