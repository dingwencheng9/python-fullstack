"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L13: 高级特性 - 装饰器测试
"""

import pytest


def test_timer_decorator(capsys):
    """测试计时装饰器"""

    @decorators.timer
    def slow_function():
        import time

        time.sleep(0.01)
        return 42

    result = slow_function()
    assert result == 42
    captured = capsys.readouterr()
    assert "slow_function" in captured.out
    assert "耗时" in captured.out


def test_retry_success():
    """测试重试装饰器成功情况"""

    @decorators.retry(max_attempts=3)
    def succeed():
        return "成功"

    result = succeed()
    assert result == "成功"


def test_retry_eventually_succeeds():
    """测试重试装饰器最终成功"""
    attempts = 0

    @decorators.retry(max_attempts=3)
    def flaky():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("临时错误")
        return "成功"

    result = flaky()
    assert result == "成功"
    assert attempts == 3


def test_retry_exhausted():
    """测试重试装饰器耗尽"""

    @decorators.retry(max_attempts=2)
    def always_fails():
        raise ValueError("总是失败")

    with pytest.raises(ValueError, match="总是失败"):
        always_fails()


def test_validate_args_valid():
    """测试参数验证通过"""

    @decorators.validate_args(x=lambda x: x > 0)
    def positive(x: int) -> int:
        return x

    result = positive(5)
    assert result == 5


def test_validate_args_invalid():
    """测试参数验证失败"""

    @decorators.validate_args(x=lambda x: x > 0)
    def positive(x: int) -> int:
        return x

    with pytest.raises(ValueError, match="x 验证失败"):
        positive(-5)


def test_memoize():
    """测试缓存装饰器"""
    call_count = 0

    @decorators.memoize
    def expensive(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive(5) == 10
    assert expensive(5) == 10  # 应该使用缓存
    assert expensive(6) == 12  # 新的参数
    assert call_count == 2


def test_count_calls():
    """测试调用计数装饰器"""

    @decorators.count_calls
    def counter():
        return 42

    assert counter.call_count == 0
    counter()
    assert counter.call_count == 1
    counter()
    assert counter.call_count == 2
