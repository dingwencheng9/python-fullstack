# L22: 装饰器深度探索 - 详细教学内容

> **课程编号**: L22
> **所属阶段**: Stage 2 - 现代工程
> **预计时长**: 6.5 小时（含前置检查）
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L13（L14 推荐）
> **版本**: v2.0
> **最后更新**: 2026-08-01
> **核心版本**: Python 3.13


## 📚 前置知识

```mermaid
flowchart TB
    A[原始函数] --> B[装饰器函数]
    B --> C[返回包装函数]
    C --> D[增强后的函数]
    
    subgraph Levels["装饰器层次"]
        E[基础装饰器<br/>一层嵌套]
        F[带参装饰器<br/>两层嵌套]
        G[装饰器工厂<br/>三层嵌套]
    end
    
    subgraph Types["装饰器类型"]
        H[函数装饰器]
        I[类装饰器]
        J[@property]
    end
    
    C --> E
    C --> F
    C --> G
    E --> H
    F --> H
    G --> I
    G --> J
    
    style Levels fill:#e3f2fd
    style Types fill:#c8e6c9
```

**学习本课程前，你应该掌握：**

- **L13 Python 高级特性（入门）** - 闭包、装饰器基础、上下文管理器
- **L14 装饰器进阶**（推荐）- 带参装饰器、装饰器链、类装饰器

> ⚠️ **重要提示**：本课程基于 L13/L14 的基础知识构建。如果你是初学者，建议先完成前置课程。本课程提供了前置知识检查点，帮助你评估是否需要复习。

---

## 🔍 前置知识检查（30 分钟）

### 检查点测试

在开始本课程之前，请回答以下问题来评估你的基础：

**检查 1: 闭包概念**
```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))  # 输出是什么？
print(triple(5))  # 输出是什么？
```
- A: 10, 15
- B: 10, 10
- C: 15, 15
- D: 报错

<details>
<summary>答案与解析</summary>

**答案: A (10, 15)**

**解析**: `make_multiplier(2)` 返回的 `multiply` 函数记住了 `factor=2`，所以 `double(5)=5*2=10`。同理 `triple(5)=5*3=15`。这就是闭包的"记忆"能力。

</details>

---

**检查 2: 装饰器基础**
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```
执行上述代码，输出顺序是什么？

- A: Before → Hello! → After
- B: Hello! → Before → After
- C: Before → After → Hello!
- D: After → Before → Hello!

<details>
<summary>答案与解析</summary>

**答案: A**

**解析**: `@my_decorator` 将 `say_hello` 替换为 `wrapper`，调用 `say_hello()` 实际调用 `wrapper()`，而 `wrapper` 先执行 `print("Before")`，再调用原函数 `func()`（即 `say_hello`），最后执行 `print("After")`。

</details>

---

**检查 3: @wraps 的作用**

`@wraps(func)` 在装饰器中的主要作用是什么？

- A: 加快函数执行速度
- B: 保留原函数的 `__name__` 和 `__doc__`
- C: 添加异常处理
- D: 改变函数的返回值

<details>
<summary>答案与解析</summary>

**答案: B**

**解析**: `@wraps(func)` 来自 `functools`，它将原函数的 `__name__`、`__doc__`、`__module__` 等属性复制到包装器函数上，保持元信息不变，便于调试和文档生成。

</details>

---

**检查 4: 带参装饰器**

以下装饰器的执行顺序是什么？
```python
def repeat(times=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet():
    return "Hi"
```

- A: 先执行 `repeat(times=3)` → 再执行 `decorator(greet)` → 最后调用 `wrapper()`
- B: 直接执行 `decorator(greet)` → 调用 `wrapper()`
- C: 先执行 `decorator(greet)` → 再执行 `repeat(times=3)` → 最后调用 `wrapper()`
- D: 按顺序从上到下执行

<details>
<summary>答案与解析</summary>

**答案: A**

**解析**: `@repeat(times=3)` 是装饰器工厂，先调用 `repeat(times=3)` 返回 `decorator` 函数，再将 `greet` 传给 `decorator` 返回 `wrapper`。三层嵌套结构的执行顺序是：**参数层 → 函数层 → 调用层**。

</details>

---

**检查 5: 类装饰器**

以下类装饰器的输出是什么？
```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self):
        self.count += 1
        print(f"Called {self.count} times")
        return self.func()

@CountCalls
def foo():
    return "Done"

foo()
foo()
```

- A: Called 1 times → Done → Called 2 times → Done
- B: Done → Called 1 times → Done → Called 2 times
- C: Called 2 times → Done
- D: 报错

<details>
<summary>答案与解析</summary>

**答案: A**

**解析**: `@CountCalls` 将 `foo` 替换为 `CountCalls` 实例，调用 `foo()` 实际调用实例的 `__call__` 方法。在 `__call__` 中，先 `count += 1`，打印计数，然后调用并返回 `self.func()`。

</details>

---

### 📊 检查结果评估

| 正确数 | 评估 | 建议 |
|:------:|------|------|
| 5/5 | ✅ 优秀 | 可以跳过模块 1-2，直接进入模块 3 |
| 4/5 | ✅ 良好 | 快速浏览模块 1-2 的代码示例即可 |
| 3/5 | ⚠️ 一般 | 建议完成模块 1-2 的学习 |
| ≤2/5 | ❌ 薄弱 | 请先完成 L13/L14 前置课程 |

---

## 模块 1: 基础回顾（可选）(30 分钟)

### 1.1 前置知识：闭包回顾

在理解装饰器之前，我们需要先复习闭包的概念。

```python
def outer(x):
    """外部函数"""
    def inner(y):
        """内部函数 - 可以访问外部函数的变量"""
        return x + y
    return inner

# 使用闭包
add_5 = outer(5)
print(add_5(3))  # 输出: 8
print(add_5(10))  # 输出: 15
```

**闭包的关键特征**：

1. 嵌套函数
2. 内部函数引用外部函数的变量
3. 外部函数返回内部函数

### 1.2 高阶函数回顾

高阶函数是接收函数作为参数，或返回函数的函数。

```python
def apply_twice(func, value):
    """高阶函数：接收函数作为参数"""
    return func(func(value))

def add_one(x):
    return x + 1

result = apply_twice(add_one, 5)
print(result)  # 输出: 7 (5 + 1 + 1)
```

### 1.3 装饰器的本质

装饰器是一个返回函数的函数。它的基本模式是：

```python
def decorator(func):
    """装饰器函数"""
    def wrapper():
        """包装器函数"""
        print("Before function call")
        result = func()
        print("After function call")
        return result
    return wrapper

# 手动装饰
def say_hello():
    print("Hello!")

say_hello = decorator(say_hello)
say_hello()
# 输出:
# Before function call
# Hello!
# After function call
```

### 1.4 @ 语法糖

Python 提供了 `@` 语法来简化装饰器的使用：

```python
@decorator
def say_hello():
    print("Hello!")

# 完全等价于
def say_hello():
    print("Hello!")
say_hello = decorator(say_hello)
```

### 1.5 处理函数参数

大多数函数都有参数，装饰器需要正确处理：

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        """使用 *args, **kwargs 接收任意参数"""
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@decorator
def add(a, b):
    return a + b

result = add(3, 5)
# 输出:
# Calling add
# add returned: 8
```

### 1.6 functools.wraps 的重要性

装饰器会覆盖原函数的元信息（`__name__`, `__doc__` 等），使用 `@wraps` 可以保留：

```python
from functools import wraps

def decorator_without_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def decorator_with_wraps(func):
    @wraps(func)  # ← 保留原函数的元信息
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator_without_wraps
def func1():
    """This is func1"""
    pass

@decorator_with_wraps
def func2():
    """This is func2"""
    pass

print(func1.__name__)  # 输出: wrapper
print(func2.__name__)  # 输出: func2

print(func1.__doc__)   # 输出: None
print(func2.__doc__)   # 输出: This is func2
```

**最佳实践：始终使用 @wraps**

### 1.7 实战示例：计时装饰器

```python
import time
from functools import wraps

def timer(func):
    """测量函数执行时间的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

result = slow_function()
# 输出: slow_function took 1.0001s
```

---

## 模块 2: 装饰器基础回顾（快速版）(30 分钟)

### 2.1 装饰器工厂函数

有时我们需要为装饰器传递参数，这需要额外一层嵌套：

```python
from functools import wraps

def repeat(times):
    """装饰器工厂：返回装饰器"""
    def decorator(func):
        """实际的装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """包装器函数"""
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)
# 输出: ['Hello, Alice!', 'Hello, Alice!', 'Hello, Alice!']
```

**三层嵌套结构**：

1. 最外层：接收装饰器参数
2. 中间层：接收被装饰的函数
3. 最内层：接收函数调用的参数

### 2.2 可选参数的装饰器

实现既可以带参数也可以不带参数的装饰器：

```python
from functools import wraps

def optional_debug(func=None, *, prefix="DEBUG"):
    """可选参数的装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"{prefix}: Calling {f.__name__}")
            return f(*args, **kwargs)
        return wrapper

    if func is None:
        # 带参数调用: @optional_debug(prefix="INFO")
        return decorator
    else:
        # 不带参数调用: @optional_debug
        return decorator(func)

# 不带参数使用
@optional_debug
def func1():
    return "Result 1"

# 带参数使用
@optional_debug(prefix="INFO")
def func2():
    return "Result 2"

func1()  # 输出: DEBUG: Calling func1
func2()  # 输出: INFO: Calling func2
```

### 2.3 实战：重试装饰器

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2):
    """重试装饰器

    Args:
        max_attempts: 最大重试次数
        delay: 初始延迟秒数
        backoff: 延迟的倍数因子
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")

                    if attempt < max_attempts:
                        print(f"Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, backoff=2)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success"

# 使用
try:
    result = unreliable_function()
    print(result)
except ValueError as e:
    print(f"Final failure: {e}")
```

### 2.4 实战：缓存装饰器

```python
from functools import wraps
import time

def cache(max_size=128):
    """简单的缓存装饰器"""
    def decorator(func):
        cached_results = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 创建缓存键（只支持可哈希的参数）
            cache_key = (args, tuple(sorted(kwargs.items())))

            if cache_key in cached_results:
                print(f"Cache hit for {func.__name__}{args}")
                return cached_results[cache_key]

            # 限制缓存大小
            if len(cached_results) >= max_size:
                # 简单策略：清空缓存
                cached_results.clear()

            print(f"Cache miss for {func.__name__}{args}")
            result = func(*args, **kwargs)
            cached_results[cache_key] = result
            return result

        # 提供清除缓存的方法
        wrapper.cache_clear = lambda: cached_results.clear()
        wrapper.cache_info = lambda: {
            "size": len(cached_results),
            "max_size": max_size
        }

        return wrapper
    return decorator

@cache(max_size=10)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))  # 第一次调用
print(fibonacci(10))  # 缓存命中
print(fibonacci.cache_info())  # 查看缓存信息
```

**注意：Python 标准库已提供 `functools.lru_cache`**

---

## 模块 3: 类装饰器 (2h)

### 3.1 使用类实现装饰器

类可以通过实现 `__call__` 方法来作为装饰器：

```python
from functools import wraps

class CallCounter:
    """统计函数调用次数的装饰器类"""

    def __init__(self, func):
        wraps(func)(self)  # 保留原函数的元信息
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        """使实例可调用"""
        self.count += 1
        print(f"{self.func.__name__} has been called {self.count} times")
        return self.func(*args, **kwargs)

@CallCounter
def greet(name):
    return f"Hello, {name}!"

greet("Alice")  # 输出: greet has been called 1 times
greet("Bob")    # 输出: greet has been called 2 times
print(greet.count)  # 输出: 2
```

### 3.2 带参数的类装饰器

```python
from functools import wraps

class Retry:
    """重试装饰器（类版本）"""

    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, self.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_attempts:
                        raise
                    print(f"Attempt {attempt} failed, retrying...")
        return wrapper

@Retry(max_attempts=3)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Failed")
    return "Success"
```

### 3.3 装饰类的装饰器

装饰器不仅可以装饰函数，还可以装饰类：

```python
def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Database:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        print(f"Connecting to {host}:{port}")

# 只创建一个实例
db1 = Database("localhost", 5432)
db2 = Database("localhost", 5432)
print(db1 is db2)  # 输出: True
```

### 3.4 为类添加方法的装饰器

```python
def add_repr(cls):
    """为类添加 __repr__ 方法的装饰器"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"

    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(10, 20)
print(p)  # 输出: Point(x=10, y=20)
```

### 3.5 数据类装饰器（dataclasses）

Python 3.7+ 提供了 `@dataclass` 装饰器：

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str = ""

    def greet(self):
        return f"Hello, I'm {self.name}, {self.age} years old"

# 自动生成 __init__, __repr__, __eq__ 等方法
p = Person("Alice", 30, "alice@example.com")
print(p)  # 输出: Person(name='Alice', age=30, email='alice@example.com')
```

### 3.6 frozen=True — 不可变数据类

`frozen=True` 将数据类变为不可变对象，修改属性会抛出 `FrozenInstanceError`：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int
    timeout: float = 30.0

config = Config("localhost", 8080)
print(config)  # Config(host='localhost', port=8080, timeout=30.0)

# 尝试修改会抛出 FrozenInstanceError
config.port = 9000  # dataclasses.FrozenInstanceError: cannot assign to field 'port'
```

**常见应用场景**：
- 配置对象（启动后不可修改）
- 函数式编程中的不可变数据
- 充当字典的键（需配合 `eq=True`）

### 3.7 @singledispatch — 函数重载

`functools.singledispatch` 允许根据第一个参数的类型分派到不同实现：

```python
from functools import singledispatch

@singledispatch
def process(data):
    """默认实现"""
    raise TypeError(f"Unsupported type: {type(data)}")

@process.register(int)
def _(data: int) -> str:
    return f"整数: {data * 2}"

@process.register(str)
def _(data: str) -> str:
    return f"字符串: {data.upper()}"

@process.register(list)
def _(data: list) -> str:
    return f"列表: 包含 {len(data)} 个元素"

print(process(42))       # 整数: 84
print(process("hello"))  # 字符串: HELLO
print(process([1, 2]))   # 列表: 包含 2 个元素
print(process(3.14))     # TypeError: Unsupported type: <class 'float'>
```

### 3.8 __init_subclass__ — 子类注册钩子

`__init_subclass__` 是一种隐式类装饰器机制，在子类被创建时自动调用：

```python
class PluginRegistry:
    """插件注册表"""
    _plugins: dict = {}

    def __init_subclass__(cls, name: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        if name:
            cls._plugins[name] = cls
            cls.plugin_name = name

class AuthPlugin(PluginRegistry, name="auth"):
    def authenticate(self):
        return "Authenticating..."

class CachePlugin(PluginRegistry, name="cache"):
    def get(self, key):
        return f"Value for {key}"

# 自动注册
print(PluginRegistry._plugins)
# {'auth': <class 'AuthPlugin'>, 'cache': <class 'CachePlugin'>}

# 通过名称获取插件
plugin = PluginRegistry._plugins["auth"]()
print(plugin.authenticate())  # Authenticating...
```

**应用场景**：
- 自动插件/组件注册系统
- 枚举类型的值约束
- 自动继承参数配置

---

## 模块 4: 装饰器进阶 (2h)

### 4.1 装饰器链（多个装饰器）

多个装饰器从下往上应用：

```python
def bold(func):
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
# 输出: <b><i>Hello, Alice!</i></b>

# 等价于
def greet(name):
    return f"Hello, {name}!"
greet = bold(italic(greet))
```

**执行顺序**：

1. `italic` 先装饰 `greet`
2. `bold` 再装饰 `italic(greet)`
3. 调用时从外到内：bold → italic → greet

### 4.2 保留函数签名

使用 `functools.wraps` 可以保留 `__name__` 和 `__doc__`，但不能保留签名。如需保留完整签名，可使用 `inspect` 模块或第三方库 `decorator`：

```python
import inspect
from functools import wraps

def preserve_signature(func):
    """尝试保留函数签名"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    # 复制签名
    wrapper.__signature__ = inspect.signature(func)
    return wrapper

@preserve_signature
def add(a: int, b: int) -> int:
    """Add two integers"""
    return a + b

# 查看签名
print(inspect.signature(add))  # 输出: (a: int, b: int) -> int
print(add.__doc__)             # 输出: Add two integers
```

### 4.3 条件装饰

根据条件决定是否应用装饰器：

```python
def conditional_decorator(condition):
    """条件装饰器工厂"""
    def decorator(func):
        if condition:
            # 应用装饰逻辑
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"Calling {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        else:
            # 不应用装饰，直接返回原函数
            return func
    return decorator

# 根据环境变量决定是否启用调试
import os
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

@conditional_decorator(DEBUG)
def process_data(data):
    return data.upper()

# 当 DEBUG=true 时会打印日志，否则不打印
```

### 4.4 装饰器的性能考量

装饰器会增加函数调用的开销：

```python
import time

def expensive_decorator(func):
    """性能开销较大的装饰器"""
    def wrapper(*args, **kwargs):
        # 每次调用都做昂贵的操作
        time.sleep(0.1)  # 模拟开销
        return func(*args, **kwargs)
    return wrapper

@expensive_decorator
def fast_function():
    return 42

# 性能影响
start = time.time()
for _ in range(10):
    fast_function()
print(f"Time: {time.time() - start:.2f}s")  # 约 1 秒
```

**性能优化建议**：

1. 装饰器逻辑尽量轻量
2. 避免在热路径使用复杂装饰器
3. 考虑使用条件装饰
4. 必要时可以在生产环境禁用某些装饰器

### 4.5 装饰器与类型注解

装饰器会影响类型检查，需要正确标注：

```python
from typing import TypeVar, Callable, Any
from functools import wraps

F = TypeVar('F', bound=Callable[..., Any])

def typed_decorator(func: F) -> F:
    """类型安全的装饰器"""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper  # type: ignore

@typed_decorator
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 类型检查器能正确推断类型
result: str = greet("Alice")
```

---

## 模块 5: 实战应用 (2h)

### 5.1 日志装饰器

```python
import logging
from functools import wraps
from typing import Any, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_calls(level: str = "INFO"):
    """记录函数调用的装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 记录调用信息
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            logger.log(
                getattr(logging, level.upper()),
                f"Calling {func.__name__}({signature})"
            )

            try:
                result = func(*args, **kwargs)
                logger.log(
                    getattr(logging, level.upper()),
                    f"{func.__name__} returned {result!r}"
                )
                return result
            except Exception as e:
                logger.exception(
                    f"{func.__name__} raised {type(e).__name__}: {e}"
                )
                raise

        return wrapper
    return decorator

@log_calls(level="INFO")
def divide(a: float, b: float) -> float:
    """除法运算"""
    return a / b

# 使用
divide(10, 2)   # 正常情况
divide(10, 0)   # 异常情况
```

### 5.2 权限验证装饰器

```python
from functools import wraps
from typing import Callable, Set

class PermissionError(Exception):
    """权限错误"""
    pass

class User:
    """用户类"""
    def __init__(self, username: str, roles: Set[str]):
        self.username = username
        self.roles = roles

# 全局当前用户（实际应用中应从请求上下文获取）
current_user: User | None = None

def require_role(*roles: str):
    """要求特定角色的装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user is None:
                raise PermissionError("Not authenticated")

            if not any(role in current_user.roles for role in roles):
                raise PermissionError(
                    f"User {current_user.username} lacks required role: {roles}"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_role("admin", "moderator")
def delete_user(user_id: int):
    """删除用户（需要管理员或版主权限）"""
    print(f"Deleting user {user_id}")

# 测试
current_user = User("alice", {"user"})
try:
    delete_user(123)  # 抛出 PermissionError
except PermissionError as e:
    print(f"Error: {e}")

current_user = User("bob", {"admin"})
delete_user(123)  # 成功
```

### 5.3 性能计时装饰器（增强版）

```python
import time
import functools
from typing import Callable, Dict, List

class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.stats: Dict[str, List[float]] = {}

    def timer(self, func: Callable) -> Callable:
        """计时装饰器"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start

            # 记录统计
            if func.__name__ not in self.stats:
                self.stats[func.__name__] = []
            self.stats[func.__name__].append(elapsed)

            return result
        return wrapper

    def report(self):
        """生成性能报告"""
        print("\n=== Performance Report ===")
        for func_name, times in self.stats.items():
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            print(f"{func_name}:")
            print(f"  Calls: {len(times)}")
            print(f"  Avg: {avg_time*1000:.2f}ms")
            print(f"  Min: {min_time*1000:.2f}ms")
            print(f"  Max: {max_time*1000:.2f}ms")

# 使用
monitor = PerformanceMonitor()

@monitor.timer
def process_data(n: int):
    time.sleep(0.01 * n)
    return n * 2

# 执行多次
for i in range(1, 6):
    process_data(i)

# 生成报告
monitor.report()
```

### 5.4 限流装饰器

```python
import time
from functools import wraps
from typing import Callable

class RateLimiter:
    """限流器"""

    def __init__(self, max_calls: int, period: float):
        """
        Args:
            max_calls: 时间段内最大调用次数
            period: 时间段（秒）
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # 清理过期的调用记录
            self.calls = [t for t in self.calls if now - t < self.period]

            # 检查是否超过限制
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                if sleep_time > 0:
                    print(f"Rate limit reached, sleeping {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                    self.calls.clear()

            # 记录此次调用
            self.calls.append(time.time())
            return func(*args, **kwargs)

        return wrapper

@RateLimiter(max_calls=3, period=1.0)
def api_call(endpoint: str):
    """API 调用（限制每秒 3 次）"""
    print(f"Calling {endpoint}")
    return f"Response from {endpoint}"

# 快速调用 5 次
for i in range(5):
    api_call(f"/api/endpoint-{i}")
    print(f"Call {i+1} completed")
```

### 5.5 事务管理装饰器

```python
from functools import wraps
from typing import Callable, Any
import contextlib

class DatabaseConnection:
    """模拟数据库连接"""

    def __init__(self):
        self.in_transaction = False

    def begin(self):
        print("BEGIN TRANSACTION")
        self.in_transaction = True

    def commit(self):
        print("COMMIT")
        self.in_transaction = False

    def rollback(self):
        print("ROLLBACK")
        self.in_transaction = False

# 全局数据库连接
db = DatabaseConnection()

def transaction(func: Callable) -> Callable:
    """事务装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        db.begin()
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise
    return wrapper

@transaction
def transfer_money(from_account: str, to_account: str, amount: float):
    """转账操作"""
    print(f"Debit {amount} from {from_account}")
    print(f"Credit {amount} to {to_account}")

    # 模拟失败场景
    if amount > 10000:
        raise ValueError("Amount too large")

    return True

# 成功场景
transfer_money("Alice", "Bob", 100)

# 失败场景（会回滚）
try:
    transfer_money("Alice", "Bob", 20000)
except ValueError as e:
    print(f"Transfer failed: {e}")
```

### 5.6 缓存装饰器（使用 functools.lru_cache）

Python 标准库提供了强大的缓存装饰器：

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """斐波那契数列（带缓存）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 性能对比
start = time.time()
result = fibonacci(35)
elapsed = time.time() - start
print(f"Result: {result}, Time: {elapsed:.4f}s")

# 查看缓存信息
print(fibonacci.cache_info())
# 输出: CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)

# 清除缓存
fibonacci.cache_clear()
```

---

## 常见问题与陷阱

### Q1: 装饰类方法时遇到问题

**问题**：

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper

class MyClass:
    @my_decorator
    def method(self):  # self 参数丢失？
        print("Method called")
```

**解决**：使用 `*args, **kwargs` 可以自动处理 `self`：

```python
obj = MyClass()
obj.method()  # 正常工作
```

### Q2: 装饰器丢失函数元信息

**问题**：

```python
def decorator(func):
    def wrapper():
        return func()
    return wrapper

@decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)  # 输出: wrapper
print(my_func.__doc__)   # 输出: None
```

**解决**：使用 `@wraps`

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper():
        return func()
    return wrapper
```

### Q3: 装饰器参数和函数参数混淆

**问题**：

```python
# 这是装饰器还是装饰器工厂？
@my_decorator
def func():
    pass

@my_decorator()
def func():
    pass
```

**解决**：明确区分

```python
# 装饰器（直接接收函数）
def simple_decorator(func):
    return func

# 装饰器工厂（返回装饰器）
def decorator_factory(param):
    def decorator(func):
        return func
    return decorator

@simple_decorator
def func1():
    pass

@decorator_factory(param="value")
def func2():
    pass
```

### Q4: 装饰器顺序的影响

**问题**：

```python
@decorator_a
@decorator_b
def func():
    pass

# 执行顺序是什么？
```

**答案**：

```python
# 等价于
func = decorator_a(decorator_b(func))

# 从下往上装饰，从外到内执行
```

### Q5: 装饰器与 staticmethod/classmethod

**问题**：

```python
class MyClass:
    @my_decorator
    @staticmethod
    def method():
        pass
```

**解决**：`@staticmethod` 应该在最外层

```python
class MyClass:
    @staticmethod
    @my_decorator
    def method():
        pass
```

---

## 最佳实践

### 1. 始终使用 @wraps

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # ← 必须
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 2. 使用 \*args, \*\*kwargs 传递参数

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # ← 接收任意参数
        return func(*args, **kwargs)
    return wrapper
```

### 3. 装饰器命名清晰

```python
# ✅ 好的命名
@timer
@cache
@retry
@require_auth

# ❌ 不好的命名
@decorator1
@my_func
@process
```

### 4. 提供装饰器的文档

```python
def timer(func):
    """
    测量函数执行时间的装饰器

    Usage:
        @timer
        def my_function():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper
```

### 5. 考虑装饰器的可组合性

```python
# 确保装饰器可以组合使用
@cache
@timer
@log_calls
def expensive_function():
    pass
```

### 6. 避免过度使用

不要为了装饰器而装饰器，保持简单。

### 7. 测试装饰器

```python
def test_timer_decorator():
    @timer
    def slow_func():
        time.sleep(0.1)

    slow_func()  # 应该打印执行时间
```

---

## 练习指南

### 练习 1: 基础装饰器 (exercise_01_basic_decorators.py)

**学习目标**：

- 实现简单的函数装饰器
- 理解 @wraps 的作用
- 处理函数参数

**任务**：

1. 实现计时装饰器
2. 实现日志装饰器
3. 实现参数验证装饰器

### 练习 2: 带参数的装饰器 (exercise_02_parameterized_decorators.py)

**学习目标**：

- 实现装饰器工厂
- 掌握三层嵌套结构
- 实现可选参数装饰器

**任务**：

1. 实现重试装饰器
2. 实现缓存装饰器
3. 实现重复执行装饰器

### 练习 3: 类装饰器 (exercise_03_class_decorators.py)

**学习目标**：

- 使用类实现装饰器
- 装饰类
- 单例模式

**任务**：

1. 实现调用计数器
2. 实现单例装饰器
3. 实现属性注入装饰器

### 练习 4: 装饰器进阶 (exercise_05_advanced_decorators.py)

**学习目标**：

- 装饰器链
- 条件装饰
- 保留签名

**任务**：

1. 实现装饰器组合
2. 实现条件装饰器
3. 实现签名保留

### 练习 5: 实战应用 (exercise_06_practical_decorators.py)

**学习目标**：

- 构建实用装饰器库
- 解决实际问题
- 综合应用

**任务**：

1. 权限验证装饰器
2. 限流装饰器
3. 事务管理装饰器
4. 性能监控装饰器

---

## 实战项目建议

### 项目 1: 装饰器工具库

构建一个可复用的装饰器库：

- 缓存装饰器（多种策略）
- 重试装饰器（指数退避）
- 限流装饰器（令牌桶算法）
- 日志装饰器（可配置级别）

### 项目 2: Web 框架路由装饰器

模仿 Flask/FastAPI 的路由系统：

```python
app = App()

@app.route("/users")
@require_auth
def get_users():
    return {"users": [...]}
```

### 项目 3: 性能分析工具

构建性能分析装饰器：

- 自动计时
- 内存使用跟踪
- 调用次数统计
- 生成性能报告

---

## 延伸阅读

### 1. 高级话题

- **描述符协议** - 装饰器的底层机制
- **元类** - 更底层的元编程
- **上下文管理器** - 类似的资源管理模式
- **类型注解** - 装饰器的类型标注

### 2. 标准库装饰器

- `@functools.lru_cache` - LRU 缓存
- `@functools.singledispatch` - 单分派泛函数
- `@property` - 属性装饰器
- `@staticmethod` / `@classmethod` - 方法装饰器
- `@dataclass` - 数据类装饰器
- `@contextmanager` - 上下文管理器

### 3. 第三方库

- **decorator** - 保留签名的装饰器
- **wrapt** - 高级装饰器工具
- **functools32** - functools 的向后移植

### 4. 设计模式

装饰器体现了以下设计模式：

- **装饰器模式** - 动态添加职责
- **代理模式** - 控制对象访问
- **策略模式** - 可互换的算法

---

## 总结

### 核心要点

1. **装饰器本质** - 接收函数并返回函数的函数
2. **@ 语法糖** - 简化装饰器应用
3. **@wraps 必须** - 保留函数元信息
4. **参数处理** - 使用 \*args, \*\*kwargs
5. **装饰器工厂** - 三层嵌套结构
6. **类装饰器** - **call** 方法
7. **装饰器链** - 从下往上应用
8. **实战应用** - 日志、缓存、权限、限流等

### 学习检查清单

- [ ] 理解闭包和高阶函数
- [ ] 能实现简单装饰器
- [ ] 掌握 @wraps 的使用
- [ ] 能实现带参数的装饰器
- [ ] 理解三层嵌套结构
- [ ] 会使用类实现装饰器
- [ ] 理解装饰器链的执行顺序
- [ ] 能解决实际问题

### 下一步

完成本课程后，建议：

1. 实现一个完整的装饰器库
2. 学习 L06: 元类与描述符
3. 研究标准库装饰器的实现
4. 在实际项目中应用装饰器

---

## 参考答案说明

练习文件位于 `exercises/` 目录，参考答案位于 `solutions/` 目录。

**学习建议**：

1. 先自己尝试实现
2. 运行测试检查正确性
3. 对比参考答案
4. 理解不同实现方式

**验证方法**：

```bash
# 运行练习测试
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_01_basic_decorators.py

# 查看参考答案
cat stage2-engineering/lessons/L20-decorators/solutions/solution_01_basic_decorators.py

# 运行完整验证
python verify.py
```

---

## 🔄 螺旋上升学习路径

### 阶段 1 学习重点（现在）

在本课程中，你已经掌握：

- ✅ 函数装饰器的基础语法
- ✅ 装饰器的执行顺序
- ✅ functools.wraps 的重要性
- ✅ 类装饰器的基础用法
- ✅ 编写简单的装饰器

### 阶段 2 深化场景（即将到来）

在学习 FastAPI 时，你会遇到装饰器的高级应用并深入学习：

**场景 1: FastAPI 路由装饰器**

```python
@app.get("/tasks")
async def get_tasks():
    return tasks
```

**触发问题**: "这些 @ 是什么？FastAPI 如何通过装饰器实现路由？"

**场景 2: 权限控制装饰器**

```python
@require_auth(roles=["admin"])
@app.post("/users")
async def create_user(user: User):
    return user
```

**触发问题**: "如何编写带参数的装饰器？如何叠加使用多个装饰器？"

**场景 3: 依赖注入装饰器**

```python
@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

**触发问题**: "Depends 是如何工作的？装饰器如何实现依赖注入？"

### 阶段 2 学习内容（JIT - Just In Time）

当你在 FastAPI/LangChain 实战中遇到上述场景时，会深入学习：

- 🔄 **参数化装饰器**（带参数的装饰器）
- 🔄 **装饰器叠加**（多个装饰器的执行顺序）
- 🔄 **类方法装饰器**（@staticmethod, @classmethod, @property）
- 🔄 **装饰器与依赖注入**（FastAPI Depends）
- 🔄 **装饰器与中间件**（请求拦截）
- 🔄 **框架特定装饰器**（FastAPI `@app.get`、LangChain `@tool`）

### 框架装饰器：返回可调用对象的装饰器

标准库的 `@property`、`@staticmethod` 返回的是**属性或方法**，但 LangChain 的 `@tool` 返回的是**另一个可调用对象**——这是"装饰器返回装饰器"的模式：

```python
from langchain_core.tools import tool

# @tool 接收一个函数，返回 StructuredTool 对象
# StructuredTool 实现了 __call__，所以仍然可以像函数一样调用
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# 效果上看起来像函数调用
result = multiply(a=3, b=4)  # → 12

# 但实际上是 StructuredTool 对象
print(type(multiply))  # <class 'langchain_core.tools.StructuredTool'>
print(multiply.name)   # 'multiply'
print(multiply.args_schema)  # Pydantic 模型（自动从函数签名生成）
```

**装饰器的三层境界**：

| 层次 | 示例 | 返回值 |
|------|------|--------|
| 1. 简单包装 | `@lru_cache` | 包装后的原函数 |
| 2. 属性/方法 | `@property` | 属性描述符 |
| 3. 返回新对象 | `@tool` | 完全不同类型的对象 |

**为什么这样做**：LangChain 需要在 `StructuredTool` 对象上附加元数据（名称、描述、参数模式），而不仅仅是包装函数。

**预告**：L54 Agent 基础课会深入使用 `@tool` 装饰器（L20 的装饰器知识是前置基础）。

**为什么采用螺旋上升？**

**现在学基础**：建立装饰器思维，理解核心机制
**稍后深入**：在 FastAPI / LangChain 项目中遇到实际问题时，学习更有针对性

---

**课程结束 - 祝你掌握 Python 装饰器！** 🎉

---



---

## 📝 本章总结

### 核心知识点

| 模块 | 核心内容 | 关键工具 |
|------|----------|----------|
| **本课程** | 装饰器深度探索 | pytest |

### 关键要点

1. 理解本课程的核心概念
2. 掌握主要工具和 API 的使用
3. 能够独立完成课程练习

### 学习收获

完成本课程后，你已经：
- ✅ 掌握了本课程的核心概念
- ✅ 能够运用所学知识解决实际问题
- ✅ 为后续学习打下坚实基础


## 🔗 下一步

[L23: Python 新特性与版本迁移](../L23-python-new-features/README.md)
