"""P02 练习 3: 装饰器链实现验证器

课程编号: P02
所属课程: Stage 1 - Python 进阶
练习编号: 03
难度: ⭐⭐⭐⭐
知识点: 装饰器工厂 + functools.wraps + 装饰器链

任务：
1. 实现 @log 装饰器，记录函数调用
2. 实现 @retry(max_attempts) 装饰器工厂
3. 实现 @validate(**schemas) 验证参数
4. 实现 @timeout(seconds) 超时装饰器
5. 组合使用多个装饰器

运行方式:
    python exercises/03_decorator_validators.py

预期行为：
    @log
    @retry(max_attempts=3)
    @validate(name=str, age=int)
    def register_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}
"""

import functools
import time
import logging
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# ============================================================
# 1. @log 装饰器
# ============================================================

# TODO: 实现 @log 装饰器
def log(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器

    功能：
    - 记录函数调用（参数和返回值）
    - 使用 functools.wraps 保留元数据

    预期行为:
        @log
        def add(a: int, b: int) -> int:
            return a + b

        add(1, 2)
        # 输出: [LOG] 调用 add, 参数: (1, 2)
        # 输出: [LOG] add 返回 3
    """
    # TODO: 使用 functools.wraps 并实现日志记录
    pass


# ============================================================
# 2. @retry 装饰器工厂
# ============================================================

# TODO: 实现 @retry 装饰器工厂
def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂

    参数:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）

    预期行为:
        @retry(max_attempts=3, delay=0.1)
        def flaky_function():
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("失败")
            return "成功"

        attempts = [0]
        result = flaky_function()
        assert result == "成功"
        assert attempts[0] == 3
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # TODO: 实现重试逻辑
            # 1. 循环最多 max_attempts 次
            # 2. 捕获异常并重试
            # 3. 最后一次仍然失败则抛出异常
            pass
        return wrapper
    return decorator


# ============================================================
# 3. @validate 装饰器工厂
# ============================================================

# TODO: 实现 @validate 装饰器工厂
def validate(**schemas):
    """参数验证装饰器工厂

    参数:
        **schemas: 参数名到期望类型的映射

    预期行为:
        @validate(name=str, age=int)
        def create_user(name: str, age: int) -> dict:
            return {"name": name, "age": age}

        # 有效调用
        result = create_user(name="Alice", age=25)
        assert result == {"name": "Alice", "age": 25}

        # 无效调用（类型错误）
        try:
            create_user(name="Bob", age="invalid")  # age 应该是 int
        except TypeError as e:
            print(f"捕获错误: {e}")
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # TODO: 实现参数验证逻辑
            # 1. 使用 functools.signature 获取函数签名
            # 2. 绑定参数并应用默认值
            # 3. 检查每个 schema 中的类型是否匹配
            # 4. 类型不匹配则抛出 TypeError
            pass
        return wrapper
    return decorator


# ============================================================
# 4. @timeout 装饰器工厂
# ============================================================

# TODO: 实现 @timeout 装饰器工厂
def timeout(seconds: float):
    """超时装饰器工厂

    参数:
        seconds: 超时时间（秒）

    预期行为:
        @timeout(0.5)
        def slow_function():
            time.sleep(2)
            return "完成"

        try:
            slow_function()
        except TimeoutError:
            print("函数执行超时")
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # TODO: 实现超时控制
            # 提示: 使用 signal.SIGALRM（Unix）或 threading（跨平台）
            # Unix 方式:
            # import signal
            # def handler(signum, frame):
            #     raise TimeoutError(f"{func.__name__} 执行超时")
            # signal.signal(signal.SIGALRM, handler)
            # signal.alarm(int(seconds))
            # try:
            #     return func(*args, **kwargs)
            # finally:
            #     signal.alarm(0)
            pass
        return wrapper
    return decorator


# ============================================================
# 5. 组合装饰器链
# ============================================================

# 使用你实现的装饰器创建一个函数
@log
@retry(max_attempts=2, delay=0.1)
@validate(name=str, age=int)
def register_user(name: str, age: int) -> dict:
    """组合多个装饰器"""
    return {"name": name, "age": age}


# ============================================================
# 测试
# ============================================================

def test_log_decorator():
    """测试日志装饰器"""
    calls = []

    def mock_log(msg):
        calls.append(msg)

    @log
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    assert result == 3
    assert len(calls) >= 2  # 至少调用和返回
    print("✓ log 装饰器测试通过")


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
    assert result == "成功", f"实际: {result}"
    assert len(attempts) == 3, f"实际: {len(attempts)}"
    print("✓ retry 装饰器测试通过")


def test_validate_decorator():
    """测试验证装饰器"""
    @validate(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    result = create_user(name="Alice", age=25)
    assert result == {"name": "Alice", "age": 25}
    print("✓ validate 装饰器测试通过")

    try:
        create_user(name="Bob", age="invalid")  # type: ignore
        assert False, "应该抛出 TypeError"
    except TypeError as e:
        print(f"  捕获预期错误: {e}")


def test_decorator_chain():
    """测试装饰器链"""
    @log
    @retry(max_attempts=2, delay=0.01)
    @validate(name=str, age=int)
    def process(name: str, age: int) -> str:
        return f"{name}: {age}"

    result = process(name="Alice", age=25)
    assert result == "Alice: 25"
    print("✓ 装饰器链测试通过")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("P02 练习 3: 装饰器链")
    print("=" * 50)

    try:
        test_log_decorator()
        test_retry_decorator()
        test_validate_decorator()
        test_decorator_chain()
        print("\n🎉 所有测试通过!")
    except (AssertionError, NotImplementedError) as e:
        print(f"\n❌ 测试失败: {e}")
        print("请实现 TODO 部分")


if __name__ == "__main__":
    main()
