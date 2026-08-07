"""L14 示例 3: 类装饰器

使用类实现装饰器，包括带参数的类装饰器和装饰类。

运行方式: python examples/03_class_decorators.py
"""

from functools import wraps


# ============================================================
# 3.1 使用类实现装饰器
# ============================================================

class CallCounter:
    """统计函数调用次数的类装饰器"""
    def __init__(self, func):
        # 使用 wraps 保留原函数元信息
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"调用次数: {self.count}")
        return self.func(*args, **kwargs)


# ============================================================
# 3.2 带参数的类装饰器
# ============================================================

class Repeat:
    """重复执行装饰器"""
    def __init__(self, times: int = 1):
        self.times = times

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(self.times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper


# ============================================================
# 3.3 装饰类的装饰器 - 单例模式
# ============================================================

def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


# ============================================================
# 3.4 装饰类的装饰器 - 自动添加方法
# ============================================================

def add_repr(cls):
    """为类自动添加 __repr__"""
    def repr_func(self):
        attrs = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )
        return f"{cls.__name__}({attrs})"

    cls.__repr__ = repr_func
    return cls


def add_eq(cls):
    """为类添加基于属性的相等比较"""
    original_eq = cls.__eq__

    def new_eq(self, other):
        if not isinstance(other, cls):
            return NotImplemented
        return original_eq(self, other) if original_eq is not object.__eq__ else (
            self.__dict__ == other.__dict__
        )
    cls.__eq__ = new_eq

    return cls


# ============================================================
# 3.5 类装饰器的状态管理
# ============================================================

class StateMachine:
    """状态机装饰器"""
    def __init__(self, initial: str = "idle"):
        self.state = initial
        self.transitions: dict = {}
        self.listeners: list = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_state = self.state
            result = func(*args, **kwargs)
            new_state = getattr(result, 'state', self.state)
            if old_state != new_state:
                print(f"状态变化: {old_state} -> {new_state}")
                self.state = new_state
                self._notify_listeners(old_state, new_state)
            return result
        return wrapper

    def add_transition(self, from_state: str, to_state: str, event: str):
        """添加状态转换规则"""
        self.transitions[(from_state, event)] = to_state

    def trigger(self, event: str):
        """触发状态转换"""
        next_state = self.transitions.get((self.state, event))
        if next_state:
            self.state = next_state
            return self.state
        return None

    def on_state_change(self, callback):
        """注册状态变化监听器"""
        self.listeners.append(callback)

    def _notify_listeners(self, old_state, new_state):
        for listener in self.listeners:
            listener(old_state, new_state)


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("=== 类装饰器基础 ===")

    @CallCounter
    def greet(name):
        return f"Hello, {name}!"

    print(greet("Alice"))  # 调用次数: 1
    print(greet("Bob"))    # 调用次数: 2
    print(f"总调用次数: {greet.count}")

    print("\n=== 带参数的类装饰器 ===")

    @Repeat(times=3)
    def fetch_data():
        return {"data": "value"}

    results = fetch_data()
    print(f"重复执行 {len(results)} 次: {results}")

    print("\n=== 单例模式装饰器 ===")

    @singleton
    class Database:
        def __init__(self, host: str):
            self.host = host
            print(f"连接数据库: {host}")

        def query(self, sql: str):
            return f"查询: {sql}"

    db1 = Database("localhost")
    db2 = Database("localhost")
    db3 = Database("remote")

    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"db1 is db3: {db1 is db3}")  # False
    print(f"db1.host: {db1.host}")
    print(f"db3.host: {db3.host}")

    print("\n=== 为类添加方法 ===")

    @add_repr
    class Point:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    p = Point(10, 20)
    print(f"Point: {p}")

    print("\n=== 状态机装饰器 ===")

    @StateMachine(initial="idle")
    def process():
        # 模拟状态变化
        class Result:
            state = "running"
        return Result()

    def on_change(old, new):
        print(f"  -> 监听器收到: {old} -> {new}")

    process.on_state_change = on_change

    p = process()
    print(f"当前状态: {p.state}")

    print("\n=== 类装饰器 vs 函数装饰器对比 ===")
    print("""
    ┌─────────────────────────────────────────────────────────┐
    │ 类装饰器                                                │
    ├─────────────────────────────────────────────────────────┤
    │ 优点:                                                   │
    │   - 可以维护状态 (self.count, self.state)               │
    │   - 可以有多个配置参数 __init__                          │
    │   - 可以定义多个方法 (__call__, 其他方法)                │
    │                                                         │
    │ 缺点:                                                   │
    │   - 代码量稍多                                          │
    │   - 需要理解 __call__ 方法                              │
    ├─────────────────────────────────────────────────────────┤
    │ 函数装饰器                                              │
    ├─────────────────────────────────────────────────────────┤
    │ 优点:                                                   │
    │   - 简洁直观                                            │
    │   - 易于理解和编写                                      │
    │                                                         │
    │ 缺点:                                                   │
    │   - 状态需要通过闭包或全局变量维护                       │
    └─────────────────────────────────────────────────────────┘
    """)
