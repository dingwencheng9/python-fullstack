"""

from __future__ import annotations

L20 练习 5 参考答案

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
import logging
from threading import Lock
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== 任务 1: 性能监控装饰器 ====================


class PerformanceMonitor:
    """
    性能监控装饰器类

    统计函数的调用次数、执行时间等性能指标
    """

    def __init__(self):
        self.stats: dict[str, dict[str, int | float | list]] = {}
        self.lock = Lock()

    def timer(self, func: Callable) -> Callable:
        """
        计时装饰器方法

        记录函数的性能统计信息
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start

                # 线程安全地更新统计信息
                with self.lock:
                    func_name = func.__name__
                    if func_name not in self.stats:
                        self.stats[func_name] = {
                            "calls": 0,
                            "total_time": 0.0,
                            "min_time": float("inf"),
                            "max_time": 0.0,
                            "times": [],
                        }

                    stats = self.stats[func_name]
                    stats["calls"] += 1
                    stats["total_time"] += elapsed
                    stats["min_time"] = min(stats["min_time"], elapsed)
                    stats["max_time"] = max(stats["max_time"], elapsed)
                    stats["times"].append(elapsed)

        return wrapper

    def report(self):
        """生成性能报告"""
        print("\n" + "=" * 70)
        print(" 性能监控报告")
        print("=" * 70)

        if not self.stats:
            print("暂无性能数据")
            return

        for func_name, stats in sorted(self.stats.items()):
            avg_time = stats["total_time"] / stats["calls"]

            print(f"\n函数: {func_name}")
            print(f"  调用次数:   {stats['calls']}")
            print(f"  总时间:     {stats['total_time']:.6f}s")
            print(f"  平均时间:   {avg_time:.6f}s")
            print(f"  最小时间:   {stats['min_time']:.6f}s")
            print(f"  最大时间:   {stats['max_time']:.6f}s")

        print("=" * 70)

    def reset(self):
        """重置统计数据"""
        with self.lock:
            self.stats.clear()
            logger.info("性能监控数据已重置")


# ==================== 任务 2: 事务管理装饰器 ====================


class Transaction:
    """模拟事务管理器"""

    def __init__(self):
        self.in_transaction = False
        self.operations = []

    def begin(self):
        self.in_transaction = True
        self.operations = []
        logger.info("BEGIN TRANSACTION")

    def commit(self):
        self.in_transaction = False
        logger.info(f"COMMIT: {len(self.operations)} operations")

    def rollback(self):
        self.in_transaction = False
        logger.warning(f"ROLLBACK: {len(self.operations)} operations")

    def add_operation(self, op: str):
        self.operations.append(op)


transaction = Transaction()


def transactional(func: Callable) -> Callable:
    """
    事务装饰器

    自动管理事务的生命周期：
    - 函数执行前开启事务
    - 函数成功执行后提交事务
    - 函数抛出异常时回滚事务
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 开启事务
        transaction.begin()

        try:
            # 执行函数
            result = func(*args, **kwargs)
            # 成功则提交
            transaction.commit()
            return result
        except Exception:
            # 失败则回滚
            transaction.rollback()
            # 继续向上抛出异常
            raise

    return wrapper


# ==================== 任务 3: API 限流装饰器 ====================


class TokenBucket:
    """
    令牌桶算法限流装饰器

    使用令牌桶算法控制请求速率
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: 桶的容量（最多存储多少令牌）
            refill_rate: 令牌生成速率（每秒生成多少令牌）
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity  # 初始令牌数
        self.last_refill = time.time()
        self.lock = Lock()

    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_refill

        # 计算应该生成的令牌数
        tokens_to_add = elapsed * self.refill_rate

        # 更新令牌数（不超过容量）
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def _consume(self, tokens: int = 1) -> bool:
        """
        尝试消耗令牌

        Returns:
            是否成功消耗令牌
        """
        with self.lock:
            self._refill()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def __call__(self, func: Callable) -> Callable:
        """装饰器逻辑"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 尝试获取令牌
            if self._consume():
                # 获取到令牌，执行函数
                return func(*args, **kwargs)

            # 没有令牌，拒绝请求
            raise RuntimeError(f"Rate limit exceeded: {self.capacity} calls per second")

        return wrapper


# ==================== 补充：更多实用装饰器 ====================


def singleton(cls):
    """
    单例模式装饰器

    确保一个类只有一个实例
    """
    instances = {}
    lock = Lock()

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                # 双重检查锁定
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def memoize_with_expiry(expiry_seconds: int):
    """
    带过期时间的缓存装饰器

    Args:
        expiry_seconds: 缓存过期时间（秒）
    """

    def decorator(func: Callable) -> Callable:
        cache = {}
        lock = Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            with lock:
                if key in cache:
                    result, timestamp = cache[key]
                    if now - timestamp < expiry_seconds:
                        return result

                # 缓存过期或不存在，重新计算
                result = func(*args, **kwargs)
                cache[key] = (result, now)
                return result

        wrapper.cache_clear = cache.clear
        return wrapper

    return decorator


def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    异步重试装饰器

    Args:
        max_attempts: 最大重试次数
        delay: 重试延迟（秒）
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed: {e}")

                    if attempt < max_attempts:
                        time.sleep(delay * attempt)  # 指数退避

            # 所有重试都失败
            logger.error(f"All {max_attempts} attempts failed")
            raise last_exception

        return wrapper

    return decorator


# ==================== 示例使用 ====================

if __name__ == "__main__":
    print("实战装饰器示例:\n")

    # 示例 1: 性能监控
    monitor = PerformanceMonitor()

    @monitor.timer
    def task1():
        time.sleep(0.01)
        return "task1 done"

    @monitor.timer
    def task2():
        time.sleep(0.02)
        return "task2 done"

    print("1. 性能监控:")
    for _ in range(3):
        task1()
    for _ in range(2):
        task2()

    monitor.report()

    # 示例 2: 事务管理
    print("\n2. 事务管理:")

    @transactional
    def transfer_money(from_acc, to_acc, amount):
        transaction.add_operation(f"Debit {from_acc}: {amount}")
        transaction.add_operation(f"Credit {to_acc}: {amount}")

        if amount > 10000:
            raise ValueError("Amount too large")

        return True

    # 成功场景
    transfer_money("Alice", "Bob", 100)

    # 失败场景
    try:
        transfer_money("Alice", "Bob", 20000)
    except ValueError:
        print("事务已回滚")

    # 示例 3: 令牌桶限流
    print("\n3. API 限流:")

    @TokenBucket(capacity=3, refill_rate=10.0)
    def api_call(endpoint):
        return f"Response from {endpoint}"

    for i in range(3):
        result = api_call(f"/api/{i}")
        print(f"  {result}")

    print("\n✅ 所有示例运行完成")
