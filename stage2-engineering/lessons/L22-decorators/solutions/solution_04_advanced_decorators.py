"""

from __future__ import annotations

L20 练习 4 参考答案

解题思路：
本练习的完整实现展示了以下核心概念和技术要点：

1. **问题分析**：
   - 理解练习要求和核心目标
   - 识别关键技术点和实现难点
   - 确定合适的数据结构和算法

2. **实现策略**：
   - 采用模块化设计，每个函数/类职责单一
   - 使用 Python 3.13 类型提示增强代码可读性
   - 遵循 PEP 8 编码规范和最佳实践

3. **关键技术点**：
   - 正确使用语言特性（类型系统/异步/装饰器等）
   - 处理边界条件和异常情况
   - 编写清晰的文档字符串和注释

4. **测试验证**：
   - 覆盖正常流程和异常情况
   - 使用 pytest 进行单元测试
   - 确保代码质量和可维护性

学习建议：
- 先理解问题需求，再查看实现代码
- 对比自己的实现，找出差距和改进点
- 运行代码并修改参数，观察行为变化
- 尝试扩展功能，加深理解
"""

from collections.abc import Callable
from functools import wraps

# ==================== 任务 1: 装饰器链 ====================


def bold(func: Callable) -> Callable:
    """在结果外包裹 <b>...</b> 标签"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<b>{result}</b>"

    return wrapper


def italic(func: Callable) -> Callable:
    """在结果外包裹 <i>...</i> 标签"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<i>{result}</i>"

    return wrapper


def underline(func: Callable) -> Callable:
    """在结果外包裹 <u>...</u> 标签"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<u>{result}</u>"

    return wrapper


# ==================== 任务 2: 条件装饰器 ====================


def conditional_decorator(condition: bool):
    """
    条件装饰器工厂

    Args:
        condition: 是否应用装饰逻辑

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        if not condition:
            # 条件为 False，直接返回原函数
            return func

        # 条件为 True，应用装饰逻辑
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__} with condition=True")
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned {result!r}")
            return result

        return wrapper

    return decorator


# ==================== 任务 3: 装饰器组合器 ====================


def compose(*decorators):
    """
    装饰器组合函数

    接收多个装饰器并按顺序应用

    Args:
        *decorators: 要组合的装饰器

    Returns:
        组合后的装饰器

    示例:
        @compose(timer, log_calls, cache)
        def func():
            pass

        # 等价于
        @timer
        @log_calls
        @cache
        def func():
            pass
    """

    def decorator(func: Callable) -> Callable:
        # 从右到左应用装饰器（与 @语法的顺序一致）
        for dec in reversed(decorators):
            func = dec(func)
        return func

    return decorator


# ==================== 补充：更高级的组合器实现 ====================


def compose_advanced(*decorators):
    """
    高级装饰器组合器

    支持带参数的装饰器和普通装饰器混合使用
    """

    def decorator(func: Callable) -> Callable:
        result = func
        for dec in reversed(decorators):
            # 检查装饰器是否已经被调用（带参数的装饰器）
            # 或者需要直接应用（普通装饰器）
            result = dec(result)
        return result

    return decorator


# ==================== 实用工具：装饰器调试 ====================


def debug_decorator(func: Callable) -> Callable:
    """
    调试装饰器：显示装饰器的应用过程

    在开发复杂的装饰器链时很有用
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n🔍 调用函数: {func.__name__}")
        print(f"   参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"   返回: {result!r}")
        return result

    return wrapper


# ==================== 示例：复杂装饰器链 ====================


def make_html_decorator(tag: str):
    """
    HTML 标签装饰器工厂

    更通用的 HTML 标签包装器
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"<{tag}>{result}</{tag}>"

        return wrapper

    return decorator


# 使用示例
if __name__ == "__main__":
    print("装饰器链示例:\n")

    # 示例 1: 基础装饰器链
    @bold
    @italic
    @underline
    def greet(name):
        return f"Hello, {name}!"

    print(f"1. 装饰器链: {greet('Alice')}")

    # 示例 2: 条件装饰器
    @conditional_decorator(True)
    def func1():
        return "enabled"

    @conditional_decorator(False)
    def func2():
        return "disabled"

    print("\n2. 条件装饰器:")
    func1()
    func2()

    # 示例 3: 装饰器组合
    @compose(bold, italic)
    def greet2(name):
        return f"Hi, {name}!"

    print(f"\n3. 装饰器组合: {greet2('Bob')}")

    # 示例 4: 使用通用的 HTML 装饰器
    @make_html_decorator("div")
    @make_html_decorator("p")
    def content():
        return "Some content"

    print(f"\n4. 通用装饰器: {content()}")
