"""L14 示例 2: 装饰器链与执行顺序

演示多个装饰器的叠加规则和执行顺序。

运行方式: python examples/02_decorator_chaining.py
"""

from functools import wraps


# ============================================================
# 2.1 基本装饰器
# ============================================================

def bold(func):
    """加粗装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italic(func):
    """斜体装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


def uppercase(func):
    """大写装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


# ============================================================
# 2.2 带参数的可组合装饰器
# ============================================================

def log(level: str = "INFO"):
    """日志装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] 调用 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def timer(unit: str = "s"):
    """计时装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            unit_factor = 1000 if unit == "ms" else 1
            print(f"[计时] {func.__name__}: {elapsed * unit_factor:.4f}{unit}")
            return result
        return wrapper
    return decorator


# ============================================================
# 2.3 HTML 包装器（演示顺序影响）
# ============================================================

def add_header(func):
    """添加 HTML 头部"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return "<header>" + func(*args, **kwargs)
    return wrapper


def add_footer(func):
    """添加 HTML 尾部"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "</footer>"
    return wrapper


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("=== 装饰器链基础 ===")

    @bold
    @italic
    def greet(name):
        return f"Hello, {name}!"

    # 等价于: greet = bold(italic(greet))
    # 执行顺序: italic -> bold
    # 返回顺序: bold -> italic
    print(f"greet('Alice') = {greet('Alice')}")

    print("\n=== 执行顺序图示 ===")
    print("""
    @bold
    @italic
    def greet(): pass

    等价于: greet = bold(italic(greet))

    调用 greet() 时的执行顺序:
    1. 先进入 bold 的 wrapper
    2. 再进入 italic 的 wrapper
    3. 最后执行原始的 greet 函数
    4. 返回值依次穿过 italic wrapper、bold wrapper
    """)

    print("=== 三装饰器链 ===")

    @bold
    @italic
    @uppercase
    def message():
        return "hello world"

    print(f"message() = {message()}")
    # 结果: <b><i>HELLO WORLD</i></b>

    print("\n=== 可组合带参装饰器 ===")

    @log("INFO")
    @timer(unit="ms")
    def process_data(data):
        import time
        time.sleep(0.05)
        return f"处理完成: {data}"

    result = process_data([1, 2, 3])
    print(f"结果: {result}")

    print("\n=== 顺序重要性 ===")

    @add_header
    @add_footer
    def page():
        return "Content"

    print(f"正确顺序: {page()}")
    # <header>Content</footer>

    # 如果顺序错误
    def page_wrong():
        return "Content"

    page_wrong = add_footer(add_header(page_wrong))
    print(f"错误顺序: {page_wrong()}")
    # <header></footer>Content (错误!)

    print("\n=== 装饰器执行顺序总结 ===")
    print("""
    ┌─────────────────────────────────────────┐
    │ 规律: 从下往上装饰，从外到内执行         │
    ├─────────────────────────────────────────┤
    │                                         │
    │  @g1          greet = g1(g2(g3(func)))  │
    │  @g2          执行顺序: g3 -> g2 -> g1   │
    │  @g3          返回顺序: g1 -> g2 -> g3   │
    │  def greet(): pass                      │
    │                                         │
    │  装饰顺序: g3(最近) -> g2 -> g1(最远)    │
    │  执行顺序: g1(最外) -> g2 -> g3(最内)    │
    └─────────────────────────────────────────┘
    """)
