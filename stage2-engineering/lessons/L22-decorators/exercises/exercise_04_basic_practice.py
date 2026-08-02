"""

from __future__ import annotations

L20 装饰器基础补充练习

本练习作为 L20 的基础补强材料，覆盖计时、日志和参数类型验证等
常用装饰器写法，可直接运行进行自检。

练习难度：
- 练习1: ⭐（基础）
- 练习2: ⭐⭐（中级）
- 练习3: ⭐⭐（中级）

作者: Python 3.13 全栈课程
日期: 2026-06-04
Python版本: 3.13+
"""

from collections.abc import Callable
import functools
import time
from typing import Any

# ============================================
# 练习 1：简单计时装饰器 ⭐
# ============================================


def timer(func: Callable) -> Callable:
    """
    实现目标：实现一个计时装饰器

    要求：
    1. 使用 time.perf_counter() 测量执行时间
    2. 打印函数名和执行时间（保留4位小数）
    3. 使用 @wraps 保留函数元数据
    4. 返回函数的原始返回值

    提示：
        from functools import wraps
        import time

        def timer(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                print(f"{func.__name__} 执行时间: {elapsed:.4f} 秒")
                return result
            return wrapper
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 执行时间: {elapsed:.4f} 秒")
        return result

    return wrapper


# 测试练习1
@timer
def slow_function() -> str:
    """模拟耗时操作"""
    time.sleep(0.5)
    return "done"


def test_exercise_1() -> None:
    """测试练习1"""
    print("=" * 50)
    print("测试练习1: 计时装饰器")
    print("=" * 50)

    result = slow_function()
    print(f"返回值: {result}")
    print(f"函数名保留: {slow_function.__name__}")
    print(f"文档保留: {slow_function.__doc__}")
    print()


# ============================================
# 练习 2：调用计数装饰器 ⭐⭐
# ============================================


class count_calls:
    """
    TODO: 实现一个调用计数装饰器（使用类）

    要求：
    1. 使用类实现装饰器
    2. 在 __init__ 中保存被装饰的函数
    3. 在 __call__ 中增加计数并调用原函数
    4. 提供 calls 属性查看调用次数
    5. 提供 reset() 方法重置计数

    提示：
        class count_calls:
            def __init__(self, func):
                self.func = func
                self.calls = 0

            def __call__(self, *args, **kwargs):
                self.calls += 1
                return self.func(*args, **kwargs)

            def reset(self):
                self.calls = 0
    """

    def __init__(self, func: Callable) -> None:
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls += 1
        return self.func(*args, **kwargs)

    def reset(self) -> None:
        self.calls = 0


# 测试练习2
@count_calls
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


def test_exercise_2() -> None:
    """测试练习2"""
    print("=" * 50)
    print("测试练习2: 调用计数装饰器")
    print("=" * 50)

    # 多次调用
    greet("Alice")
    greet("Bob")
    greet("Charlie")

    print(f"调用次数: {greet.calls}")  # 应该是 3

    # 重置
    greet.reset()
    print(f"重置后: {greet.calls}")  # 应该是 0

    # 再次调用
    greet("David")
    print(f"再次调用后: {greet.calls}")  # 应该是 1
    print()


# ============================================
# 练习 3：参数验证装饰器 ⭐⭐
# ============================================


def validate_types(*expected_types: type) -> Callable:
    """
    实现目标：实现一个参数类型验证装饰器

    要求：
    1. 这是一个装饰器工厂（返回装饰器）
    2. 接受期望的参数类型（按顺序）
    3. 验证函数参数的类型是否匹配
    4. 类型不匹配时抛出 TypeError，包含详细错误信息
    5. 使用 @wraps 保留函数元数据

    提示：
        def validate_types(*expected_types):
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    # 验证参数类型
                    for arg, expected_type in zip(args, expected_types):
                        if not isinstance(arg, expected_type):
                            raise TypeError(
                                f"参数类型错误: 期望 {expected_type.__name__}, "
                                f"实际 {type(arg).__name__}"
                            )
                    return func(*args, **kwargs)
                return wrapper
            return decorator
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 验证参数类型
            for arg, expected_type in zip(args, expected_types, strict=False):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"参数类型错误: 期望 {expected_type.__name__}, 实际 {type(arg).__name__}"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


# 测试练习3
@validate_types(str, int)
def create_user(name: str, age: int) -> str:
    """创建用户"""
    return f"User: {name}, Age: {age}"


def test_exercise_3() -> None:
    """测试练习3"""
    print("=" * 50)
    print("测试练习3: 参数验证装饰器")
    print("=" * 50)

    # 正确的参数类型
    result1 = create_user("Alice", 25)
    print(f"成功: {result1}")

    # 错误的参数类型
    try:
        create_user("Alice", "25")  # 第二个参数应该是 int
    except TypeError as e:
        print(f"捕获错误: {e}")

    try:
        create_user(123, 25)  # 第一个参数应该是 str
    except TypeError as e:
        print(f"捕获错误: {e}")

    print()


# ============================================
# 运行所有测试
# ============================================


def main() -> None:
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("装饰器基础练习测试")
    print("=" * 50 + "\n")

    test_exercise_1()
    test_exercise_2()
    test_exercise_3()

    print("=" * 50)
    print("所有测试完成！")
    print("=" * 50)
    print()
    print("💡 如需拓展，可继续对照 exercise_01_basic_decorators.py")
    print("📝 参考答案可对照 solutions/solution_01_basic_decorators.py")


if __name__ == "__main__":
    main()
