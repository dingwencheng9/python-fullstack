"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L17: 函数式编程 - 组合装饰器测试
"""


def test_add_logging(capsys):
    """测试日志装饰器"""

    @compose_decorator.add_logging
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    result = greet("World")
    assert result == "Hello, World!"

    captured = capsys.readouterr()
    assert "调用函数: greet" in captured.out
    assert "greet 返回: Hello, World!" in captured.out


def test_add_retry_success():
    """测试重试装饰器成功"""

    @compose_decorator.add_retry(max_attempts=3)
    def succeed() -> str:
        return "成功"

    result = succeed()
    assert result == "成功"


def test_add_retry_eventually_succeeds():
    """测试重试装饰器最终成功"""
    attempts = 0

    @compose_decorator.add_retry(max_attempts=3)
    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("临时错误")
        return "成功"

    result = flaky()
    assert result == "成功"
    assert attempts == 3


def test_memoize():
    """测试缓存装饰器"""
    call_count = 0

    @compose_decorator.memoize
    def expensive(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive(5) == 10
    assert expensive(5) == 10  # 使用缓存
    assert expensive(6) == 12  # 新参数
    assert call_count == 2


def test_compose_decorators():
    """测试装饰器组合"""
    logs = []

    def log1(func):
        def wrapper(*args, **kwargs):
            logs.append("log1_before")
            result = func(*args, **kwargs)
            logs.append("log1_after")
            return result

        return wrapper

    def log2(func):
        def wrapper(*args, **kwargs):
            logs.append("log2_before")
            result = func(*args, **kwargs)
            logs.append("log2_after")
            return result

        return wrapper

    @compose_decorator.compose_decorators(log1, log2)
    def target():
        logs.append("target")
        return "done"

    logs.clear()
    result = target()
    assert result == "done"
    # compose 从右到左应用，所以 log2 先，log1 后
    assert logs == ["log1_before", "log2_before", "target", "log2_after", "log1_after"]


def test_pipe_decorators():
    """测试管道装饰器组合"""
    logs = []

    def log1(func):
        def wrapper(*args, **kwargs):
            logs.append("log1_before")
            result = func(*args, **kwargs)
            logs.append("log1_after")
            return result

        return wrapper

    def log2(func):
        def wrapper(*args, **kwargs):
            logs.append("log2_before")
            result = func(*args, **kwargs)
            logs.append("log2_after")
            return result

        return wrapper

    @compose_decorator.pipe_decorators(log1, log2)
    def target():
        logs.append("target")
        return "done"

    logs.clear()
    result = target()
    assert result == "done"
    # pipe 从左到右应用
    assert logs == ["log2_before", "log1_before", "target", "log1_after", "log2_after"]
