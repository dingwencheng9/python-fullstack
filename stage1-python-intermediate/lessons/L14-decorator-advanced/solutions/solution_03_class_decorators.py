"""L14 练习 3 参考答案: 类装饰器

参考实现:
1. CallCounter - 调用计数器
2. singleton - 单例模式
3. validate - 参数验证
4. Memoized - 记忆化类方法
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
    def __init__(self, func: F) -> None:
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.count += 1
        return self.func(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<CallCounter({self.func.__name__}): count={self.count}>"


# ============================================================
# 练习 3.2: 单例模式装饰器
# ============================================================

def singleton(cls: type[F]) -> type[F]:
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
    instances: dict[type, F] = {}

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> F:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore[return-value]


# ============================================================
# 练习 3.3: 参数验证装饰器
# ============================================================

def validate(**validators: dict[str, Callable[[Any], Any]]) -> Callable[[F], F]:
    """参数验证装饰器工厂

    验证函数参数的类型和范围。

    使用方式:
        @validate(age=lambda x: 0 <= x <= 150, name=isinstance_arg(str))
        def create_person(name, age):
            return Person(name, age)
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 获取函数参数名
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # 验证每个参数
            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    try:
                        validator(value)
                    except Exception as e:
                        # 保留原始异常信息
                        raise type(e)(f"参数 '{param_name}' 验证失败: {e}") from e

            return func(*args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator


def isinstance_arg(cls: type) -> Callable[[Any], Any]:
    """创建类型检查验证器"""
    def validator(value: Any) -> Any:
        if not isinstance(value, cls):
            raise TypeError(f"Expected {cls.__name__}, got {type(value).__name__}")
        return value
    return validator


# ============================================================
# 练习 3.4: 记忆化类装饰器
# ============================================================

class Memoized:
    """类方法记忆化装饰器（使用描述符协议）

    为类的方法添加缓存功能。

    使用方式:
        class Math:
            @Memoized
            def fibonacci(self, n):
                if n < 2:
                    return n
                return self.fibonacci(n - 1) + self.fibonacci(n - 2)
    """
    def __init__(self, func: Callable) -> None:
        wraps(func)(self)
        self.func = func
        self._instance_caches: dict = {}  # instance id -> cache dict

    def __get__(self, instance: Any, owner: type) -> Callable:
        """描述符协议：返回绑定方法"""
        if instance is None:
            # 通过类访问，返回自身
            return self

        # 通过实例访问，返回绑定的包装器
        instance_id = id(instance)
        if instance_id not in self._instance_caches:
            self._instance_caches[instance_id] = {}

        def bound_method(*args: Any, **kwargs: Any) -> Any:
            # 创建缓存键
            key = (args, tuple(sorted(kwargs.items())))
            cache = self._instance_caches[instance_id]

            # 检查缓存
            if key in cache:
                return cache[key]

            # 计算并缓存
            result = self.func(instance, *args, **kwargs)
            cache[key] = result
            return result

        # 复制函数元信息
        bound_method.__wrapped__ = self.func
        bound_method.__doc__ = self.func.__doc__
        bound_method.cache_clear = lambda: self._instance_caches[instance_id].clear()
        return bound_method


# ============================================================
# 测试验证
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

    print("\n所有测试通过!")
