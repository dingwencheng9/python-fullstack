# R01: Python 3.14t 完全体

> **课程编号**: R01
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 4-6 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: M01-M08 或 L54-L65
> **版本**: v5.0
> **最后更新**: 2026-07-22
> **核心版本**: Python 3.14t (free-threading)

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解 Python 3.14t free-threading 架构**：掌握无 GIL 的设计原理与限制
2. **迁移现有代码到 free-threading**：将 asyncio + 线程池代码适配新模式
3. **诊断线程安全问题**：使用 GIL 诊断工具识别竞态条件
4. **评估库兼容性**：判断主流库对 free-threading 的支持状态
5. **编写线程安全代码**：掌握无 GIL 环境下的最佳实践

---

## 📖 课程导读

### 为什么学习 Python 3.14t？

Python 3.13 引入的 free-threading 是 Python 历史上最重要的变化之一。**GIL（全局解释器锁）的移除**意味着：

- 多线程终于可以真正并行执行 CPU 密集型任务
- asyncio 不再是唯一的并发方案
- 但现有的线程安全假设可能需要重新审视

### 本课定位

本课程是 Stage R（前沿探索实验室）的第一课，为你准备：
- Python 3.14 正式发布后的生产环境迁移
- 对 free-threading 局限性的清醒认知
- 面向未来的 Python 并发编程范式

### 前置知识

- L14 并发编程入门（async/await 基础）
- L19 异步编程核心（asyncio 进阶）
- L24 线程与并发（GIL 原理）

---

## Part 1: Free-Threading 架构解析

### 1.1 GIL 移除的背景

Python 的 GIL 一直是性能瓶颈的根源：

```python
# GIL 存在时：多线程只能并发执行，无法并行
import threading
import time

def cpu_bound_task(n: int) -> int:
    """模拟 CPU 密集型任务"""
    result = 0
    for i in range(n * 10_000_000):
        result += i % 3
    return result

# 4 个线程同时运行，但 GIL 让它们串行化
threads = [threading.Thread(target=cpu_bound_task, args=(1,)) for _ in range(4)]
start = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"4 线程耗时: {time.perf_counter() - start:.2f}s")  # 约等于 4x 单线程
```

**Free-threading 通过移除 GIL，让多线程真正并行**：

```python
# Python 3.14t（free-threading）：多线程可以真正并行
# 使用 python3.14t 运行此代码
import threading
import time

# 同样 4 个线程，现在可以并行执行
threads = [threading.Thread(target=cpu_bound_task, args=(1,)) for _ in range(4)]
start = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"4 线程耗时: {time.perf_counter() - start:.2f}s")  # 约等于 1x 单线程
```

### 1.2 Free-Threading 的实现机制

Python 3.13t 通过以下方式实现 free-threading：

| 组件 | GIL 模式 | Free-Threading 模式 |
|-------|----------|---------------------|
| **锁粒度** | 全局单一锁 | 对象级细粒度锁 |
| **引用计数** | 非原子操作 + GIL 保护 | 原子操作（原子引用计数） |
| **内存分配** | pymalloc（GIL 保护） | 线程安全的 pymalloc_free_threading |
| **解释器状态** | 单一全局状态 | 每线程独立状态 |

```python
# 检查当前 Python 是否支持 free-threading
import sys
import threading

def check_free_threading() -> dict:
    """检测 Python free-threading 支持状态"""
    info = {
        "version": sys.version,
        "gil_available": hasattr(sys, '吉尔可用'),  # 旧版本检测方式
        "thread_count": threading.active_count(),
        "free_threading_build": "_吉尔" in sys.version or "free threading" in sys.version.lower(),
    }
    return info

# 运行检测
result = check_free_threading()
print(f"Python 版本: {result['version']}")
print(f"Free-threading 构建: {result['free_threading_build']}")
```

### 1.3 关键 API 变化

#### 3.13 → 3.14t 的 API 迁移

```python
# Python 3.13（GIL 模式）
import threading
import asyncio

# asyncio.Lock 在 GIL 模式下是轻量级的
lock = asyncio.Lock()

# Python 3.14t（free-threading 模式）
# asyncio.Lock 保持不变，但内部实现变为线程安全
# 新增 threading.Lock 比 3.13 略有开销（无 GIL 保护）
native_lock = threading.Lock()  # 现在是真正的互斥锁

# 跨线程的 asyncio 需要显式同步
async def cross_thread_async():
    """跨线程异步操作的正确方式"""
    # 3.14t 中 asyncio 和线程的边界更清晰
    loop = asyncio.get_running_loop()

    # 如果需要在另一个线程运行异步代码
    # 3.13: 可能工作但不稳定
    # 3.14t: 需要显式传递事件循环
    await asyncio.sleep(0)  # 安全的 yield 点
```

---

## Part 2: 代码迁移实战

### 2.1 线程安全检查清单

在迁移到 free-threading 前，评估你的代码：

```python
"""
线程安全自检清单：
□ 是否依赖 GIL 做隐式同步？
□ 是否使用锁/队列等显式同步？
□ 是否访问共享的可变状态？
□ 是否有非线程安全的数据结构（list、dict）？
□ 是否有非原子操作（a += 1）？
"""

# 示例：需要修改的代码
class Counter:
    """非线程安全的计数器"""
    def __init__(self):
        self.count = 0

    def increment(self):
        # ⚠️ 在 free-threading 下可能导致计数丢失
        self.count += 1

# 迁移后：线程安全的计数器
from threading import Lock

class ThreadSafeCounter:
    """线程安全的计数器"""
    def __init__(self):
        self._lock = Lock()
        self._count = 0

    def increment(self):
        with self._lock:
            self._count += 1

    @property
    def count(self):
        with self._lock:
            return self._count
```

### 2.2 asyncio + 线程混合模式

```python
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, TypeVar

T = TypeVar("T")

class AsyncThreadBridge:
    """asyncio 和线程池的桥接"""

    def __init__(self, max_workers: int = 4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    async def run_sync_in_thread(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """在线程池中运行同步代码"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor,
            lambda: func(*args, **kwargs)
        )

    def shutdown(self):
        """关闭线程池"""
        self._executor.shutdown(wait=True)

# 使用示例
async def example():
    bridge = AsyncThreadBridge()

    # CPU 密集型任务在线程池运行
    result = await bridge.run_sync_in_thread(cpu_bound_task, 10)
    print(f"结果: {result}")

    bridge.shutdown()

# 在 python3.14t 中，ThreadPoolExecutor 性能更好
# 因为没有 GIL 阻塞
```

### 2.3 数据结构迁移

```python
from threading import Lock
from collections import defaultdict
from typing import Any

# 迁移前：依赖 GIL 的非线程安全代码
class Cache:
    """非线程安全缓存（依赖 GIL 保护）"""
    def __init__(self):
        self._data: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def set(self, key: str, value: Any):
        # ⚠️ 在 free-threading 可能丢失更新
        self._data[key] = value

# 迁移后：显式线程安全
class ThreadSafeCache:
    """线程安全缓存"""
    def __init__(self):
        self._lock = Lock()
        self._data: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        with self._lock:
            return self._data.get(key)

    def set(self, key: str, value: Any):
        with self._lock:
            self._data[key] = value

    def get_or_compute(self, key: str, factory: Callable[[], Any]) -> Any:
        """线程安全的 get-or-create 模式"""
        with self._lock:
            if key in self._data:
                return self._data[key]
            value = factory()
            self._data[key] = value
            return value
```

---

## Part 3: 性能调优与诊断

### 3.1 线程安全诊断工具

```python
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ThreadDiagnostics:
    """线程诊断工具"""
    operations: int = 0
    conflicts: int = 0
    start_time: float = field(default_factory=time.perf_counter)

    def record_operation(self, wait_time: float):
        self.operations += 1
        if wait_time > 0.001:  # 超过 1ms 视为冲突
            self.conflicts += 1

    @property
    def conflict_rate(self) -> float:
        if self.operations == 0:
            return 0.0
        return self.conflicts / self.operations

    def report(self) -> str:
        elapsed = time.perf_counter() - self.start_time
        return (
            f"线程诊断报告:\n"
            f"  操作总数: {self.operations}\n"
            f"  冲突次数: {self.conflicts}\n"
            f"  冲突率: {self.conflict_rate:.2%}\n"
            f"  耗时: {elapsed:.2f}s"
        )

def monitor_threads(func):
    """线程监控装饰器"""
    diagnostics = ThreadDiagnostics()

    def wrapper(*args, **kwargs):
        lock = Lock()
        wait_times = []

        def monitored(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            wait = time.perf_counter() - start
            wait_times.append(wait)
            return result

        # 并发执行
        threads = [threading.Thread(target=monitored) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return diagnostics.report()

    return wrapper
```

### 3.2 性能对比基准

```python
import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

def benchmark(name: str, func, iterations: int = 100) -> float:
    """基准测试工具"""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.3f}s ({iterations} iterations)")
    return elapsed

def cpu_task(n: int) -> int:
    """CPU 密集型任务"""
    return sum(i * i for i in range(n * 100_000))

# 基准测试
print("=== CPU 密集型任务基准测试 ===")

# 单线程
benchmark("单线程", lambda: cpu_task(1))

# 多线程（GIL 模式：约等于单线程）
threads = [threading.Thread(target=cpu_task, args=(1,)) for _ in range(4)]
benchmark("4 线程（传统）", lambda: [t.start() or t.join() for t in threads])

# 多进程（绕过 GIL）
from concurrent.futures import ProcessPoolExecutor
benchmark("4 进程", lambda: list(
    ProcessPoolExecutor(max_workers=4).map(cpu_task, [1]*4)
))

# python3.14t 多线程（真正并行）
# benchmark("4 线程（free-threading）", ...)
```

---

## Part 4: 库兼容性指南

### 4.1 主流库支持状态

| 库 | 3.13 | 3.14t 支持 | 备注 |
|-----|-------|-------------|------|
| **numpy** | ✅ | ✅ | 已支持，需要重新编译 |
| **pandas** | ✅ | ✅ | 已支持 |
| **CPython 内置** | ✅ | ✅ | 完全兼容 |
| **asyncio** | ✅ | ✅ | 完全兼容 |
| **threading** | ✅ | ✅ | 需要显式锁 |
| **multiprocessing** | ✅ | ✅ | 完全兼容 |
| **C 扩展** | ✅ | ⚠️ | 需确认线程安全 |

### 4.2 C 扩展兼容性检查

```python
"""
检查 C 扩展的线程安全性
"""
import importlib.util
import sys

def check_extension_safety(module_name: str) -> dict:
    """检查 C 扩展的线程安全性"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return {"error": f"模块 {module_name} 未找到"}

        module = importlib.import_module(module_name)

        # 检查是否有 _thread 模块
        has_thread_local = hasattr(module, '_thread_local')

        return {
            "module": module_name,
            "version": getattr(module, '__version__', 'unknown'),
            "has_thread_local": has_thread_local,
            "thread_safe": True,  # 需要实际测试
        }
    except ImportError as e:
        return {"error": str(e)}

# 检查常用库
for lib in ['numpy', 'pandas', 'requests', 'sqlalchemy']:
    result = check_extension_safety(lib)
    print(f"{lib}: {result}")
```

---

## 💡 常见陷阱与最佳实践

### 陷阱 1: 依赖 GIL 做隐式同步

```python
# ❌ 错误：依赖 GIL 保护共享状态
class GILDependent:
    def __init__(self):
        self.counter = 0  # GIL 保护，但 free-threading 下会出错

    def increment(self):
        self.counter += 1  # 非原子操作！

# ✅ 正确：显式同步
class ThreadSafe:
    def __init__(self):
        self._lock = Lock()
        self._counter = 0

    def increment(self):
        with self._lock:
            self._counter += 1
```

### 陷阱 2: asyncio.Lock 跨线程使用

```python
# ❌ 错误：跨线程传递 asyncio.Lock
async def bad_example():
    lock = asyncio.Lock()

    async def worker():
        async with lock:  # 在不同线程执行会出问题
            await do_work()

    # 错误：创建新线程运行异步代码
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as pool:
        loop = asyncio.new_event_loop()
        await loop.run_in_executor(pool, worker)

# ✅ 正确：显式管理事件循环
async def good_example():
    lock = asyncio.Lock()

    async def worker(loop):
        asyncio.set_event_loop(loop)
        async with lock:
            await do_work()

    # 正确：传递事件循环
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as pool:
        loop = asyncio.new_event_loop()
        await loop.run_in_executor(pool, worker, loop)
```

### 最佳实践 1: 优先使用 asyncio

```python
# ✅ 推荐：asyncio 是跨版本最安全的并发方式
# asyncio.Lock 在 GIL 和 free-threading 下都工作

async def async_safe_operation():
    lock = asyncio.Lock()
    async with lock:
        # 安全的异步临界区
        await do_work()
```

### 最佳实践 2: 使用线程安全数据结构

```python
# ✅ 推荐：queue.Queue 是线程安全的
from queue import Queue, Empty

def producer(q: Queue):
    for i in range(10):
        q.put(i)  # 线程安全

def consumer(q: Queue):
    while True:
        try:
            item = q.get(timeout=1)
            print(item)
        except Empty:
            break

# ✅ 推荐：使用 dataclass + Lock 组合
from dataclasses import dataclass
from threading import Lock

@dataclass
class ThreadSafeData:
    value: int = 0
    _lock: Lock = None

    def __post_init__(self):
        self._lock = Lock()

    def update(self, delta: int):
        with self._lock:
            self.value += delta
```

---

## 🚀 实战案例：迁移生产代码

### 案例：Web 服务并发处理

```python
"""
场景：FastAPI 服务，处理 CPU 密集型请求
迁移策略：从 asyncio + 线程池 → 原生多线程（python3.14t）
"""

# 迁移前（3.13）
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

@app.get("/process")
async def process_endpoint(data: str):
    # asyncio 包装线程池执行 CPU 密集型任务
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        executor,
        cpu_intensive_task,
        data
    )
    return {"result": result}

# 迁移后（3.14t）
import threading
from fastapi import FastAPI

app = FastAPI()

# 真正的多线程处理
thread_pool = ThreadPoolExecutor(max_workers=4)

@app.get("/process")
async def process_endpoint_v2(data: str):
    loop = asyncio.get_running_loop()

    # 3.14t 中线程池执行效率更高
    # 因为没有 GIL 阻塞
    result = await loop.run_in_executor(
        thread_pool,
        cpu_intensive_task,
        data
    )
    return {"result": result}

def cpu_intensive_task(data: str) -> str:
    """CPU 密集型任务"""
    # 模拟复杂计算
    result = sum(ord(c) * i for i, c in enumerate(data * 1000))
    return f"processed: {result}"
```

---

## 📚 延伸阅读

### 官方资源
- [PEP 703 - Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [Python 3.13 Free-Threading 文档](https://docs.python.org/3.13/whatsnew/3.13.html#free-threading)
- [threading — Thread-based parallelism](https://docs.python.org/3/library/threading.html)

### 深度文章
- [Understanding Python's Free-Threading Model](https://realpython.com/python-free-threading/)
- [Migrating to Thread-Safe Python](https://pythonspeed.com/articles/gil-free-threading/)

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 解释 GIL 移除如何影响 Python 并发模型
- [ ] 使用 `threading.Lock` 保护共享状态
- [ ] 识别代码中依赖 GIL 的隐式同步
- [ ] 将 asyncio + 线程池代码迁移到 free-threading
- [ ] 使用诊断工具检测线程竞争
- [ ] 评估第三方库对 free-threading 的兼容性
- [ ] 在 python3.14t 环境中编写线程安全代码

---

## 🔗 下一步

完成本课程后，继续学习：

- [R02: GIL Free Fallback 策略](../R02-gil-fallback-avoid/lesson.md) — 学习在混合环境中优雅降级
- [R03: PEP 649/810 延迟注解](../R03-pep-649-810-lazy/lesson.md) — Python 3.14 类型系统演进

在下一课中，我们将学习：
- 多版本 Python 的兼容策略
- 渐进式迁移路径
- 回退机制设计

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0（核心版本: Python 3.14t）
