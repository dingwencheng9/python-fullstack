"""

from __future__ import annotations

实用装饰器示例（Python 3.13 现代化版）

展示装饰器在实际项目中的应用场景。
本文件是从02-core简化而来，去除Web特定概念，使其更通用。

涵盖场景：
- 日志记录
- 输入验证
- 条件检查
- 执行统计

Python 3.13 现代化要点：
- 使用内置泛型 (list, dict) 替代 typing.List, typing.Dict
- 使用管道符 | 替代 typing.Optional/Union
- 使用 time.perf_counter() 获取高精度时间

作者: Python 3.13 全栈课程
日期: 2026-06-08
Python版本: 3.13+
"""

from collections.abc import Callable
import functools
import time

# ============================================
# 1. 日志装饰器
# ============================================


def log_execution(func: Callable) -> Callable:
    """
    执行日志装饰器。

    记录函数的执行情况，包括：
    - 函数名
    - 参数
    - 返回值
    - 执行时间
    - 异常信息

    这是最常用的装饰器之一，适用于调试和监控。

    Python 3.13 优化：使用 time.perf_counter() 获取高精度时间
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录开始
        print(f"[LOG] 开始执行: {func.__name__}")
        print(f"[LOG] 参数: args={args}, kwargs={kwargs}")

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[LOG] 执行成功: {func.__name__}")
            print(f"[LOG] 耗时: {elapsed:.4f}秒")
            print(f"[LOG] 返回值: {result}")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            print(f"[LOG] 执行失败: {func.__name__}")
            print(f"[LOG] 耗时: {elapsed:.4f}秒")
            print(f"[LOG] 错误: {e}")
            raise

    return wrapper


@log_execution
def process_data(data: list[int]) -> int:
    """处理数据"""
    time.sleep(0.1)  # 模拟处理
    return sum(data)


# ============================================
# 2. 输入验证装饰器
# ============================================


def validate_input(**validators: Callable[[...], bool]) -> Callable:
    """
    输入验证装饰器。

    验证函数参数是否符合要求。
    这是一个带参数的装饰器（装饰器工厂）。

    使用方式：
        @validate_input(age=lambda x: 0 <= x <= 150, email=lambda x: "@" in x)
        def register_user(name: str, age: int, email: str):
            ...

    Args:
        **validators: 参数名 -> 验证函数的映射
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 验证每个参数
            for param_name, validator in validators.items():
                if param_name in kwargs:
                    value = kwargs[param_name]
                    if not validator(value):
                        raise ValueError(f"参数 {param_name} 验证失败: {value}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


@validate_input(age=lambda x: 0 <= x <= 150, email=lambda x: "@" in x)
def register_user(name: str, age: int, email: str) -> str:
    """注册用户"""
    return f"注册成功: {name}, {age}岁, {email}"


# ============================================
# 3. 条件检查装饰器
# ============================================


def require_condition(
    condition_func: Callable[..., bool], error_message: str
) -> Callable:
    """
    条件检查装饰器。

    检查是否满足某个条件，不满足时抛出异常。
    这是一个通用的条件装饰器，可以用于各种场景。

    使用示例：
        # 检查是否登录
        @require_condition(lambda user: user is not None, "请先登录")
        def view_profile(user=None):
            ...

        # 检查权限
        @require_condition(lambda user: user.get("role") == "admin", "需要管理员权限")
        def delete_data(user=None):
            ...

    Args:
        condition_func: 条件检查函数
        error_message: 条件不满足时的错误消息
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行条件检查
            if not condition_func(*args, **kwargs):
                raise PermissionError(error_message)

            return func(*args, **kwargs)

        return wrapper

    return decorator


# 示例：检查用户是否存在
@require_condition(lambda user=None: user is not None, "用户未登录或不存在")
def view_profile(user: dict | None = None) -> str:
    """查看个人资料"""
    return f"用户资料: {user['name']}"


# 示例：检查年龄
@require_condition(lambda age: age >= 18, "年龄必须大于等于18岁")
def purchase_alcohol(age: int) -> str:
    """购买酒类商品"""
    return f"购买成功，年龄: {age}"


# ============================================
# 4. 执行统计装饰器（使用类实现）
# ============================================


class CountCalls:
    """
    调用计数装饰器。

    使用类实现装饰器，可以维护状态。
    这个装饰器记录函数被调用的次数。

    使用方式：
        @count_calls
        def my_function():
            ...

        my_function()
        print(my_function.calls)  # 1
        my_function.reset()
    """

    def __init__(self, func: Callable) -> None:
        """
        初始化装饰器。

        Args:
            func: 被装饰的函数
        """
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        """
        调用被装饰的函数。

        每次调用时增加计数。
        """
        self.calls += 1
        return self.func(*args, **kwargs)

    def reset(self) -> None:
        """重置计数"""
        self.calls = 0


@CountCalls
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


# ============================================
# 演示函数
# ============================================


def demonstrate_logging_decorator() -> None:
    """演示日志装饰器"""
    print("=" * 50)
    print("1. 日志装饰器")
    print("=" * 50)

    process_data([1, 2, 3, 4, 5])
    print()


def demonstrate_validation_decorator() -> None:
    """演示验证装饰器"""
    print("=" * 50)
    print("2. 输入验证装饰器")
    print("=" * 50)

    # 有效输入
    result = register_user("李四", age=25, email="lisi@example.com")
    print(f"成功: {result}")

    # 无效年龄
    try:
        register_user("王五", age=200, email="wangwu@example.com")
    except ValueError as e:
        print(f"错误: {e}")

    # 无效邮箱
    try:
        register_user("赵六", age=30, email="invalid-email")
    except ValueError as e:
        print(f"错误: {e}")
    print()


def demonstrate_condition_decorator() -> None:
    """演示条件装饰器"""
    print("=" * 50)
    print("3. 条件检查装饰器")
    print("=" * 50)

    # 用户未登录
    try:
        view_profile()
    except PermissionError as e:
        print(f"错误: {e}")

    # 用户已登录
    user = {"name": "张三", "role": "user"}
    result = view_profile(user=user)
    print(f"成功: {result}")

    # 年龄检查
    try:
        purchase_alcohol(16)
    except PermissionError as e:
        print(f"错误: {e}")

    result = purchase_alcohol(20)
    print(f"成功: {result}")
    print()


def demonstrate_count_decorator() -> None:
    """演示计数装饰器"""
    print("=" * 50)
    print("4. 执行统计装饰器（类实现）")
    print("=" * 50)

    # 多次调用
    greet("Alice")
    greet("Bob")
    greet("Charlie")

    print(f"调用次数: {greet.calls}")

    # 重置计数
    greet.reset()
    print(f"重置后: {greet.calls}")
    print()


# ============================================
# 主函数
# ============================================


def main() -> None:
    """主函数"""
    demonstrate_logging_decorator()
    demonstrate_validation_decorator()
    demonstrate_condition_decorator()
    demonstrate_count_decorator()

    print("=" * 50)
    print("演示完成！")
    print("=" * 50)
    print()
    print("💡 要点总结：")
    print("1. 日志装饰器：用于调试和监控")
    print("2. 验证装饰器：确保输入合法")
    print("3. 条件装饰器：通用的条件检查")
    print("4. 类装饰器：可以维护状态")
    print()
    print("🚀 实战建议：")
    print("- 日志装饰器是最常用的，建议掌握")
    print("- 验证装饰器可以简化输入检查代码")
    print("- 条件装饰器可以替代大量的 if 语句")
    print("- 类装饰器适合需要维护状态的场景")


if __name__ == "__main__":
    main()
