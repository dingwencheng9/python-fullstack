# R02: GIL Free Fallback 策略

> **课程编号**: R02
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 4-6 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: R01
> **版本**: v5.0
> **最后更新**: 2026-07-22
> **核心版本**: Python 3.13 / 3.14t

---

## 📌 学习目标

完成本课程后，你将能够：

1. **实现版本检测机制**：在运行时判断 Python 是否支持 free-threading
2. **设计优雅降级策略**：在不支持的环境中自动切换到兼容模式
3. **编写渐进式迁移代码**：让代码同时支持 GIL 和 free-threading 模式
4. **构建多版本测试矩阵**：确保代码在所有目标版本中正常工作
5. **优化锁竞争性能**：减少 free-threading 模式下的锁开销

---

## 📖 课程导读

### 为什么需要 Fallback 策略？

Python 3.13t（free-threading）和 3.13（GIL）将长期共存：

- **生产环境**：可能运行在 GIL 模式（更好的库兼容性）
- **开发环境**：可能运行在 free-threading 模式（更好的并发性能）
- **用户环境**：不可控的 Python 版本和构建

**渐进式迁移**是最佳策略：让你的代码同时支持两种模式。

### 本课定位

本课程承接 R01，学习如何在混合环境中优雅地处理 free-threading：
- 运行时检测 Python 版本
- 条件化启用/禁用特性
- 性能对比与选择策略

### 前置知识

- R01 Python 3.14t 完全体（free-threading 基础）
- L24 线程与并发（线程安全基础）

---

## Part 1: 版本检测机制

### 1.1 运行时版本检测

```python
import sys
import platform
from dataclasses import dataclass

@dataclass
class PythonEnvironment:
    """Python 运行环境信息"""
    version: str
    version_info: tuple[int, int, int]
    implementation: str
    is_free_threading: bool
    platform: str

    @classmethod
    def detect(cls) -> "PythonEnvironment":
        """检测当前 Python 运行环境"""
        version_info = sys.version_info

        # 检测 free-threading 的方法
        is_free_threading = (
            # 方法1: 检查版本字符串
            "free threading" in sys.version.lower()
            # 方法2: 检查 _thread 模块的特殊属性
            or getattr(sys, '_free_threading', False)
        )

        return cls(
            version=sys.version,
            version_info=(version_info.major, version_info.minor, version_info.micro),
            implementation=platform.python_implementation(),
            is_free_threading=is_free_threading,
            platform=sys.platform,
        )

# 使用示例
env = PythonEnvironment.detect()
print(f"检测到: {env}")
# 输出: Python 3.13 (free-threading) on darwin
```

### 1.2 特性检测而非版本检测

```python
from typing import Callable, TypeVar
import functools

T = TypeVar("T")

def supports_free_threading() -> bool:
    """检测是否支持 free-threading"""
    return (
        "free threading" in sys.version.lower()
        or getattr(sys, '_free_threading', False)
    )

class FeatureGate:
    """
    特性开关：根据环境启用/禁用特性

    优于版本检测：特性可能出现在任意版本
    """

    def __init__(self):
        self._features: dict[str, bool] = {
            "free_threading": supports_free_threading(),
            "pep695_type_params": sys.version_info >= (3, 12),
        }

    def is_enabled(self, feature: str) -> bool:
        """检查特性是否启用"""
        return self._features.get(feature, False)

    def enable(self, feature: str):
        """启用特性（用于测试）"""
        self._features[feature] = True

    def disable(self, feature: str):
        """禁用特性（用于测试）"""
        self._features[feature] = False

# 全局实例
features = FeatureGate()

def require_free_threading(func: Callable[..., T]) -> Callable[..., T]:
    """必须在 free-threading 环境运行的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not features.is_enabled("free_threading"):
            raise RuntimeError(
                f"{func.__name__} requires free-threading Python. "
                f"Current: {sys.version}"
            )
        return func(*args, **kwargs)
    return wrapper
```

### 1.3 多版本兼容性层

```python
"""
跨版本兼容性层
为 GIL 和 free-threading 提供统一 API
"""
from typing import Protocol, Any
from abc import ABC, abstractmethod

class ThreadLock(Protocol):
    """线程锁抽象接口"""
    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool: ...
    def release(self) -> None: ...

class SynchronizationFactory:
    """同步原语工厂"""

    @staticmethod
    def create_lock() -> ThreadLock:
        """创建线程锁"""
        if supports_free_threading():
            return FineGrainedLock()  # free-threading 优化的锁
        return StandardLock()  # GIL 模式的标准锁

class StandardLock:
    """GIL 模式的标准锁"""
    def __init__(self):
        import threading
        self._lock = threading.Lock()

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        return self._lock.acquire(blocking, timeout)

    def release(self):
        self._lock.release()

class FineGrainedLock:
    """free-threading 优化的细粒度锁"""
    def __init__(self):
        import threading
        self._lock = threading.Lock()

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        return self._lock.acquire(blocking, timeout)

    def release(self):
        self._lock.release()
```

---

## Part 2: 优雅降级策略

### 2.1 条件化代码路径

```python
from typing import Callable, Optional
from enum import Enum
import asyncio
import sys

class ThreadingMode(Enum):
    """线程模式"""
    GIL = "gil"
    FREE_THREADING = "free_threading"
    AUTO = "auto"

class AsyncThreadBridge:
    """
    异步与线程的桥接器
    根据环境自动选择最优实现
    """

    def __init__(
        self,
        mode: ThreadingMode = ThreadingMode.AUTO,
        max_workers: Optional[int] = None
    ):
        self.mode = mode
        self.max_workers = max_workers or (4 if supports_free_threading() else 8)
        self._executor = None

    def _get_mode(self) -> ThreadingMode:
        """确定实际运行模式"""
        if self.mode == ThreadingMode.AUTO:
            return (
                ThreadingMode.FREE_THREADING
                if supports_free_threading()
                else ThreadingMode.GIL
            )
        return self.mode

    async def run_cpu_bound(
        self,
        func: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """运行 CPU 密集型任务"""
        actual_mode = self._get_mode()

        if actual_mode == ThreadingMode.FREE_THREADING:
            # free-threading 模式：多线程更高效
            return await self._run_in_thread_pool(func, *args, **kwargs)
        else:
            # GIL 模式：多进程绕过 GIL
            return await self._run_in_process_pool(func, *args, **kwargs)

    async def _run_in_thread_pool(self, func, *args, **kwargs):
        """线程池执行（free-threading 优化）"""
        from concurrent.futures import ThreadPoolExecutor

        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor,
            lambda: func(*args, **kwargs)
        )

    async def _run_in_process_pool(self, func, *args, **kwargs):
        """进程池执行（GIL 模式）"""
        from concurrent.futures import ProcessPoolExecutor

        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            return await loop.run_in_executor(
                executor,
                lambda: func(*args, **kwargs)
            )

    def shutdown(self):
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
```

### 2.2 回退装饰器

```python
import functools
from typing import Callable, TypeVar, Optional

T = TypeVar("T")

def fallback(
    primary: Callable[..., T],
    fallback_fn: Optional[Callable[..., T]] = None,
) -> Callable[..., T]:
    """
    回退装饰器：主函数失败时使用回退函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except (NotImplementedError, RuntimeError) as e:
                if "free-threading" in str(e) and fallback_fn:
                    return fallback_fn(*args, **kwargs)
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except (NotImplementedError, RuntimeError) as e:
                if "free-threading" in str(e) and fallback_fn:
                    if asyncio.iscoroutinefunction(fallback_fn):
                        return await fallback_fn(*args, **kwargs)
                    return fallback_fn(*args, **kwargs)
                raise

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

# 示例：带回退的线程安全计数器
class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = None

    def _ensure_lock(self):
        if self._lock is None:
            import threading
            self._lock = threading.Lock()

    def increment(self):
        if supports_free_threading():
            self._ensure_lock()
            with self._lock:
                self._count += 1
        else:
            # GIL 模式下不需要额外锁
            self._count += 1
```

### 2.3 性能自适应

```python
import time
import asyncio
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")

@dataclass
class PerformanceMetrics:
    """性能指标"""
    executions: int = 0
    total_time: float = 0
    min_time: float = float('inf')

    def record(self, elapsed: float):
        self.executions += 1
        self.total_time += elapsed
        self.min_time = min(self.min_time, elapsed)

    @property
    def avg_time(self) -> float:
        if self.executions == 0:
            return 0
        return self.total_time / self.executions

class AdaptiveStrategy:
    """自适应策略：根据实际性能选择最优实现"""

    def __init__(self):
        self._strategies: dict[str, PerformanceMetrics] = {}

    def register_strategy(self, name: str):
        if name not in self._strategies:
            self._strategies[name] = PerformanceMetrics()

    async def execute(
        self,
        strategy_name: str,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        start = time.perf_counter()
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start
        self._strategies[strategy_name].record(elapsed)
        return result

    def get_best_strategy(self) -> Optional[str]:
        if not self._strategies:
            return None
        return min(
            self._strategies.items(),
            key=lambda x: x[1].avg_time
        )[0]
```

---

## Part 3: 多版本测试矩阵

### 3.1 测试配置

```python
# conftest.py - 多版本测试配置
import pytest
import sys

def pytest_configure(config):
    """配置测试标记"""
    config.addinivalue_line(
        "markers",
        "requires_free_threading: 仅在 free-threading 模式下运行"
    )

def pytest_collection_modifyitems(items):
    """根据环境修改测试"""
    is_ft = "free threading" in sys.version.lower()

    for item in items:
        if item.get_closest_marker("requires_free_threading") and not is_ft:
            item.add_marker(pytest.mark.skip(
                reason="需要 free-threading Python"
            ))
```

### 3.2 版本条件测试

```python
import pytest
import sys

def is_free_threading() -> bool:
    return "free threading" in sys.version.lower()

class TestThreadSafety:
    """线程安全测试"""

    def test_lock_acquire_release(self):
        """锁的获取和释放"""
        from threading import Lock
        lock = Lock()

        assert lock.acquire(blocking=False)
        assert not lock.acquire(blocking=False)
        lock.release()
        assert lock.acquire(blocking=False)

    @pytest.mark.requires_free_threading
    def test_true_parallelism(self):
        """测试真正的并行执行（仅 free-threading）"""
        import threading
        import time

        results = []

        def cpu_task():
            total = 0
            for _ in range(10_000_000):
                total += 1
            results.append(total)

        threads = [threading.Thread(target=cpu_task) for _ in range(4)]

        start = time.perf_counter()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        elapsed = time.perf_counter() - start

        assert len(results) == 4
        assert all(r == 10_000_000 for r in results)
```

### 3.3 持续集成矩阵

```yaml
# .github/workflows/multiversion-test.yml
name: Multi-Version Tests

on: [push, pull_request]

jobs:
  test-gil:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install uv
      - run: uv sync
      - run: uv run pytest tests/ -v

  test-free-threading:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python 3.14t
        run: |
          # 编译 Python 3.14t free-threading 构建
      - run: pip install uv
      - run: uv sync
      - run: uv run pytest tests/ -v
```

---

## Part 4: 锁竞争优化

### 4.1 读写锁优化

```python
from threading import Lock
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ReadWriteLock:
    """
    读写锁：读多写少场景优化
    """

    def __init__(self):
        import threading
        self._readers = 0
        self._writer = False
        self._readers_lock = threading.Lock()
        self._write_lock = threading.Lock()

    def acquire_read(self):
        """获取读锁"""
        while True:
            with self._readers_lock:
                if not self._writer:
                    self._readers += 1
                    return True
            import time
            time.sleep(0.001)

    def release_read(self):
        with self._readers_lock:
            self._readers -= 1

    def acquire_write(self):
        """获取写锁"""
        with self._write_lock:
            self._writer = True
            while True:
                with self._readers_lock:
                    if self._readers == 0:
                        return True
                import time
                time.sleep(0.001)

    def release_write(self):
        with self._readers_lock:
            self._writer = False

class ReadOptimizedCache(Generic[T]):
    """读优化的缓存"""

    def __init__(self):
        self._data: dict[str, T] = {}
        self._lock = ReadWriteLock()

    def get(self, key: str) -> Optional[T]:
        """读取（多线程安全，读锁优化）"""
        self._lock.acquire_read()
        try:
            return self._data.get(key)
        finally:
            self._lock.release_read()

    def set(self, key: str, value: T):
        """写入（独占写锁）"""
        self._lock.acquire_write()
        try:
            self._data[key] = value
        finally:
            self._lock.release_write()
```

---

## 💡 常见陷阱与最佳实践

### 陷阱 1: 错误假设版本特性

```python
# ❌ 错误：假设版本号决定特性
if sys.version_info >= (3, 14):
    use_optimized_code()

# ✅ 正确：直接检测特性
if supports_free_threading():
    use_optimized_code()
```

### 陷阱 2: 混用同步和异步锁

```python
# ❌ 错误：跨线程使用 asyncio.Lock
async def bad_example():
    lock = asyncio.Lock()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(lock.acquire())  # 可能死锁

# ✅ 正确：使用标准 threading.Lock 跨线程
from threading import Lock

def good_example():
    lock = Lock()
    with lock:
        do_work()
```

### 最佳实践 1: 渐进式迁移

```python
# ✅ 推荐：从兼容代码开始，逐步引入特性

def process_concurrently(items: list):
    """渐进式并发处理"""
    if supports_free_threading():
        return _process_threaded(items)
    else:
        return _process_multiprocess(items)
```

---

## 🚀 实战案例：跨版本兼容库

```python
"""
跨版本兼容的事件总线
"""
import asyncio
from typing import Callable, Any
from dataclasses import dataclass, field

class EventBus:
    """线程安全事件总线"""

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}
        self._lock = None if supports_free_threading() else asyncio.Lock()
        self._thread_lock = None if not supports_free_threading() else __import__('threading').Lock()

    def subscribe(self, event: str, handler: Callable[..., Any]):
        """订阅事件"""
        if self._thread_lock:
            with self._thread_lock:
                if event not in self._subscribers:
                    self._subscribers[event] = []
                self._subscribers[event].append(handler)
        else:
            if event not in self._subscribers:
                self._subscribers[event] = []
            self._subscribers[event].append(handler)

    async def publish(self, event: str, *args, **kwargs):
        """发布事件"""
        handlers = self._subscribers.get(event, [])
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(*args, **kwargs)
            else:
                handler(*args, **kwargs)
```

---

## 📚 延伸阅读

- [PEP 703 - Making the GIL Optional](https://peps.python.org/pep-0703/)
- [Python 3.13 What's New](https://docs.python.org/3/whatsnew/3.13.html)
- [Free Threading in Python 3.13](https://pythonspeed.com/articles/free-threaded-python-313/)

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 实现运行时 free-threading 检测
- [ ] 编写条件化代码路径（自动降级）
- [ ] 设计带回退的线程安全函数
- [ ] 构建多版本测试矩阵
- [ ] 优化锁竞争（读写锁、细粒度锁）
- [ ] 编写跨版本兼容库

---

## 🔗 下一步

- [R03: PEP 649/810 延迟注解](../R03-pep-649-810-lazy/lesson.md)
- [R04: t-string 与格式化新纪元](../R04-tstring-fstring/lesson.md)

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0
