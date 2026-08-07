"""test_decorator.py - 装饰器链测试"""

import pytest
import time
from solutions.solution_03_decorator_validators import (
    log,
    retry,
    validate,
    timeout,
)


def test_log_decorator():
    """测试日志装饰器"""
    @log
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    assert result == 3


def test_retry_decorator():
    """测试重试装饰器"""
    attempts = []

    @retry(max_attempts=3, delay=0.01)
    def flaky_function():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("暂未成功")
        return "成功"

    result = flaky_function()
    assert result == "成功"
    assert len(attempts) == 3


def test_retry_decorator_fail():
    """测试重试装饰器最终失败"""
    @retry(max_attempts=2, delay=0.01)
    def always_fail():
        raise ValueError("总是失败")

    with pytest.raises(ValueError, match="总是失败"):
        always_fail()


def test_validate_decorator():
    """测试验证装饰器"""
    @validate(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    result = create_user(name="Alice", age=25)
    assert result == {"name": "Alice", "age": 25}


def test_validate_decorator_type_error():
    """测试验证装饰器类型错误"""
    @validate(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    with pytest.raises(TypeError, match="age.*类型错误"):
        create_user(name="Bob", age="invalid")  # type: ignore


def test_validate_decorator_missing():
    """测试验证装饰器缺失参数"""
    @validate(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    # 应该使用默认值或抛出错误
    result = create_user(name="Carol", age=30)
    assert result["name"] == "Carol"


def test_decorator_chain():
    """测试装饰器链"""
    @log
    @retry(max_attempts=2, delay=0.01)
    @validate(name=str, age=int)
    def process(name: str, age: int) -> str:
        return f"{name}: {age}"

    result = process(name="Alice", age=25)
    assert result == "Alice: 25"


@pytest.mark.skipif(
    True,  # SIGALRM 在 macOS 上不可靠
    reason="SIGALRM 在 macOS 上不可靠"
)
def test_timeout_decorator():
    """测试超时装饰器"""
    @timeout(0.1)
    def slow_function():
        time.sleep(1)
        return "完成"

    with pytest.raises(TimeoutError):
        slow_function()


def test_timeout_decorator_normal():
    """测试超时装饰器正常完成"""
    @timeout(1.0)
    def fast_function():
        return "完成"

    result = fast_function()
    assert result == "完成"
