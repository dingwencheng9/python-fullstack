"""L20 练习 5: 装饰器进阶.

学习目标：装饰器链、条件装饰和装饰器组合。
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
import sys


def bold(func: Callable) -> Callable:
    """在函数结果外包裹 <b>...</b>。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper


def italic(func: Callable) -> Callable:
    """在函数结果外包裹 <i>...</i>。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"

    return wrapper


def underline(func: Callable) -> Callable:
    """在函数结果外包裹 <u>...</u>。"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"

    return wrapper


def conditional_decorator(condition: bool):
    """condition 为真时打印调用信息，否则返回原函数。"""

    def decorator(func: Callable) -> Callable:
        if not condition:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def compose(*decorators):
    """把多个装饰器组合成一个装饰器。"""

    def decorator(func: Callable) -> Callable:
        wrapped = func
        for deco in reversed(decorators):
            wrapped = deco(wrapped)
        return wrapped

    return decorator


def test_decorator_chain() -> None:
    print("\n测试 1: 装饰器链")

    @bold
    @italic
    @underline
    def greet(name):
        return f"Hello, {name}!"

    assert greet("Alice") == "<b><i><u>Hello, Alice!</u></i></b>"
    print("✅ 装饰器链测试通过")


def test_conditional_decorator() -> None:
    print("\n测试 2: 条件装饰器")

    @conditional_decorator(True)
    def func1():
        return "result1"

    @conditional_decorator(False)
    def func2():
        return "result2"

    assert func1() == "result1"
    assert func2() == "result2"
    print("✅ 条件装饰器测试通过")


def test_compose() -> None:
    print("\n测试 3: 装饰器组合器")

    @compose(bold, italic)
    def greet(name):
        return f"Hello, {name}!"

    assert greet("Bob") == "<b><i>Hello, Bob!</i></b>"
    print("✅ 装饰器组合器测试通过")


def main() -> bool:
    print("\n" + "=" * 50)
    print("L20 练习 5: 装饰器进阶")
    print("=" * 50)
    try:
        test_decorator_chain()
        test_conditional_decorator()
        test_compose()
    except AssertionError as exc:
        print(f"\n❌ 测试失败: {exc}")
        return False
    except Exception as exc:
        print(f"\n❌ 发生错误: {type(exc).__name__}: {exc}")
        return False

    print("\n🎉 所有测试通过！")
    print("💡 下一步：尝试 exercise_06_practical_decorators.py")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
