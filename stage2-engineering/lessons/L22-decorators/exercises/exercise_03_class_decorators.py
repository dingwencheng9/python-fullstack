"""L20 练习 3: 类装饰器.

学习目标：
- 使用类实现装饰器
- 理解 __call__ 方法
- 使用装饰器修改类
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import sys


class CallCounter:
    """使用类实现的调用计数装饰器。"""

    def __init__(self, func: Callable) -> None:
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)


def singleton(cls):
    """确保被装饰类只创建一个实例。"""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class Memoize:
    """使用类实现的缓存装饰器。"""

    def __init__(self, func: Callable) -> None:
        wraps(func)(self)
        self.func = func
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in self.cache:
            self.hits += 1
            print(f"Cache hit: {self.func.__name__}{args}")
            return self.cache[key]
        self.misses += 1
        print(f"Cache miss: {self.func.__name__}{args}")
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result

    def cache_info(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache)}

    def cache_clear(self) -> None:
        self.cache.clear()
        self.hits = 0
        self.misses = 0


def add_methods(**methods):
    """为类添加一组方法。"""

    def decorator(cls):
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls

    return decorator


def test_call_counter() -> None:
    print("\n测试 1: 类装饰器 CallCounter")

    @CallCounter
    def greet(name):
        return f"Hello, {name}!"

    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
    assert greet.count == 2
    assert greet.__name__ == "greet"
    print("✅ CallCounter 测试通过")


def test_singleton() -> None:
    print("\n测试 2: 单例装饰器")

    @singleton
    class Database:
        def __init__(self, name):
            self.name = name

    db1 = Database("main")
    db2 = Database("backup")
    assert db1 is db2
    assert db1.name == "main"
    print("✅ singleton 测试通过")


def test_memoize() -> None:
    print("\n测试 3: 类缓存装饰器")

    @Memoize
    def square(n):
        return n * n

    assert square(4) == 16
    assert square(4) == 16
    info = square.cache_info()
    assert info["hits"] == 1
    assert info["misses"] == 1
    square.cache_clear()
    assert square.cache_info()["size"] == 0
    print("✅ Memoize 测试通过")


def test_add_methods() -> None:
    print("\n测试 4: 属性注入装饰器")

    def greet(self):
        return f"Hello, {self.name}!"

    @add_methods(greet=greet)
    class Person:
        def __init__(self, name):
            self.name = name

    person = Person("Alice")
    assert person.greet() == "Hello, Alice!"
    print("✅ add_methods 测试通过")


def main() -> bool:
    print("\n" + "=" * 50)
    print("L20 练习 3: 类装饰器")
    print("=" * 50)
    try:
        test_call_counter()
        test_singleton()
        test_memoize()
        test_add_methods()
    except AssertionError as exc:
        print(f"\n❌ 测试失败: {exc}")
        return False
    except Exception as exc:
        print(f"\n❌ 发生错误: {type(exc).__name__}: {exc}")
        return False

    print("\n🎉 所有测试通过！")
    print("💡 下一步：尝试 exercise_05_advanced_decorators.py")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
