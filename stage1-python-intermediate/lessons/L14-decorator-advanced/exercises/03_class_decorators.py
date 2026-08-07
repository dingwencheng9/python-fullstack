"""L14 练习 3: 类装饰器 [模板型练习]

难度: ⭐⭐⭐⭐☆（中高级）
模式: 模板型 - 根据需求描述实现完整功能

任务要求:
1. 实现带状态的类装饰器
2. 实现单例模式装饰器
3. 实现参数验证装饰器

参考示例: examples/03_class_decorators.py
"""

from functools import wraps
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


# ============================================================
# 练习 3.1: 调用计数器（类装饰器）
# ============================================================

class CallCounter:
    """统计函数调用次数的类装饰器

    使用方式:
        @CallCounter
        def my_function():
            pass

        print(my_function.count)  # 访问调用次数
    """
    # TODO: 实现 CallCounter 类装饰器
    # 提示:
    # 1. __init__ 接收被装饰的函数
    # 2. __call__ 实现计数逻辑
    # 3. 使用 wraps 保留原函数元信息
    pass


# ============================================================
# 练习 3.2: 单例模式装饰器
# ============================================================

def singleton(cls):
    """单例模式装饰器

    确保类只有一个实例。

    使用方式:
        @singleton
        class Database:
            def __init__(self, host):
                self.host = host

        db1 = Database("localhost")
        db2 = Database("localhost")
        assert db1 is db2  # True
    """
    # TODO: 实现单例装饰器
    # 提示:
    # 1. 使用字典存储实例
    # 2. 检查类是否已有实例
    # 3. 首次创建后缓存实例
    pass


# ============================================================
# 练习 3.3: 参数验证装饰器
# ============================================================

def validate(**validators):
    """参数验证装饰器工厂

    验证函数参数的类型和范围。

    使用方式:
        @validate(age=lambda x: 0 <= x <= 150, name=isinstance_arg(str))
        def create_person(name, age):
            return Person(name, age)
    """
    # TODO: 实现参数验证装饰器
    # 提示:
    # 1. 遍历 validators 检查每个参数
    # 2. validators 是 {参数名: 验证函数} 的映射
    # 3. 验证失败抛出 ValueError 或 TypeError
    pass


def isinstance_arg(cls):
    """创建类型检查验证器"""
    def validator(value):
        if not isinstance(value, cls):
            raise TypeError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value
    return validator


# ============================================================
# 练习 3.4: 记忆化类装饰器
# ============================================================

class Memoized:
    """类方法记忆化装饰器

    为类的方法添加缓存功能。

    使用方式:
        class Math:
            @Memoized
            def fibonacci(self, n):
                if n < 2:
                    return n
                return self.fibonacci(n - 1) + self.fibonacci(n - 2)
    """
    # TODO: 实现 Memoized 类装饰器
    # 提示:
    # 1. 使用字典缓存方法结果
    # 2. 缓存键应包含 self 和所有参数
    # 3. 方法应能正常访问 self 的其他属性
    pass


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("=== 调用计数器测试 ===")

    @CallCounter
    def greet(name):
        return f"Hello, {name}!"

    print(greet("Alice"))
    print(greet("Bob"))
    print(greet("Charlie"))
    print(f"总调用次数: {greet.count}")

    print("\n=== 单例模式测试 ===")

    @singleton
    class Database:
        def __init__(self, host: str):
            self.host = host
            print(f"  连接数据库: {host}")

        def query(self, sql: str):
            return f"执行: {sql}"

    print("创建第一个实例...")
    db1 = Database("localhost")
    print("创建第二个实例（应该复用）...")
    db2 = Database("localhost")
    print("创建第三个实例（不同参数）...")
    db3 = Database("remote.example.com")

    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db1 is db3: {db1 is db3}")  # False
    print(f"db1.host: {db1.host}")
    print(f"db3.host: {db3.host}")

    print("\n=== 参数验证测试 ===")

    @validate(
        name=isinstance_arg(str),
        age=lambda x: 0 <= x <= 150,
        email=isinstance_arg(str)
    )
    def register_user(name, age, email):
        return f"注册用户: {name}, {age}岁, {email}"

    try:
        result = register_user("Alice", 25, "alice@example.com")
        print(f"  成功: {result}")
    except (TypeError, ValueError) as e:
        print(f"  失败: {e}")

    # 测试类型错误
    try:
        result = register_user(123, 25, "alice@example.com")
        print(f"  成功: {result}")
    except TypeError as e:
        print(f"  类型错误: {e}")

    # 测试值范围错误
    try:
        result = register_user("Bob", -5, "bob@example.com")
        print(f"  成功: {result}")
    except ValueError as e:
        print(f"  值范围错误: {e}")

    print("\n=== 记忆化类方法测试 ===")

    class Math:
        @Memoized
        def fibonacci(self, n: int) -> int:
            """斐波那契数列"""
            print(f"    [计算] fibonacci({n})")
            if n < 2:
                return n
            return self.fibonacci(n - 1) + self.fibonacci(n - 2)

    math = Math()
    print("计算 fibonacci(10):")
    result = math.fibonacci(10)
    print(f"  结果: {result}")

    print("\n测试完成！")
