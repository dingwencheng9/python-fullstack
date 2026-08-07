"""L16: 并发编程 - 异步高级语法"""

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional
import random
import time


# === Part 1: 异步上下文管理器 ===

class AsyncResource:
    """异步资源管理器"""

    async def __aenter__(self):
        print("获取资源")
        await asyncio.sleep(0.1)  # 模拟异步获取
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
        await asyncio.sleep(0.1)  # 模拟异步释放
        return False  # 不抑制异常


@asynccontextmanager
async def managed_connection(name: str):
    """使用装饰器创建异步上下文管理器"""
    print(f"[{name}] 建立连接...")
    conn = {"name": name, "data": []}
    try:
        yield conn
        print(f"[{name}] 提交数据: {conn['data']}")
    finally:
        print(f"[{name}] 关闭连接")


async def context_manager_demo():
    """异步上下文管理器示例"""
    # 使用类
    async with AsyncResource() as resource:
        print("使用资源中...")

    print()

    # 使用装饰器
    async with managed_connection("DB") as db:
        db["data"].append({"id": 1, "name": "Alice"})
        await asyncio.sleep(0.1)


asyncio.run(context_manager_demo())


# === Part 2: 异步队列与生产者-消费者 ===

@dataclass
class Task:
    id: int
    data: str
    priority: int = 0


class AsyncTaskQueue:
    """异步任务队列"""

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: asyncio.Queue[Task] = asyncio.Queue(maxsize=maxsize)

    async def put(self, task: Task) -> None:
        """添加任务"""
        await self._queue.put(task)

    async def get(self) -> Task:
        """获取任务（阻塞直到有任务）"""
        return await self._queue.get()

    async def get_with_timeout(self, timeout: float) -> Optional[Task]:
        """带超时的获取"""
        try:
            return await asyncio.wait_for(self._queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return None

    def task_done(self) -> None:
        """标记任务完成"""
        self._queue.task_done()

    async def join(self) -> None:
        """等待所有任务完成"""
        await self._queue.join()


async def producer(queue: AsyncTaskQueue, num_tasks: int):
    """生产者：生成任务"""
    for i in range(num_tasks):
        task = Task(
            id=i,
            data=f"任务数据 {i}",
            priority=random.randint(1, 3)
        )
        await queue.put(task)
        print(f"[生产者] 添加任务 #{task.id} (优先级: {task.priority})")
        await asyncio.sleep(0.2)


async def consumer(queue: AsyncTaskQueue, consumer_id: int):
    """消费者：处理任务"""
    processed = 0
    while True:
        task = await queue.get_with_timeout(timeout=1.0)
        if task is None:
            print(f"[消费者 #{consumer_id}] 无任务，退出 (处理了 {processed} 个)")
            break

        print(f"[消费者 #{consumer_id}] 处理任务 #{task.id}")
        await asyncio.sleep(random.uniform(0.1, 0.3))  # 模拟处理
        queue.task_done()
        processed += 1
        print(f"[消费者 #{consumer_id}] 完成任务 #{task.id}")


async def queue_demo():
    """异步队列示例"""
    queue = AsyncTaskQueue()

    # 启动生产者和消费者
    await asyncio.gather(
        producer(queue, 8),
        consumer(queue, 1),
        consumer(queue, 2),
    )


asyncio.run(queue_demo())


# === Part 3: 异步信号量与连接池 ===

class AsyncConnectionPool:
    """异步连接池"""

    def __init__(self, max_connections: int = 5) -> None:
        self.max_connections = max_connections
        self._semaphore = asyncio.Semaphore(max_connections)
        self._connections: list[str] = []
        self._created = 0

    async def acquire(self) -> str:
        """获取连接"""
        await self._semaphore.acquire()

        # 创建或复用连接
        if self._connections:
            conn = self._connections.pop()
        else:
            self._created += 1
            conn = f"conn-{self._created}"
            await asyncio.sleep(0.1)  # 模拟连接建立

        return conn

    async def release(self, conn: str) -> None:
        """释放连接"""
        if len(self._connections) < self.max_connections:
            self._connections.append(conn)
        self._semaphore.release()

    async def __aenter__(self) -> "AsyncConnectionPool":
        return self

    async def __aexit__(self, *args) -> None:
        pass  # 保持连接池


async def use_connection(pool: AsyncConnectionPool, task_id: int):
    """使用连接池"""
    conn = await pool.acquire()
    try:
        print(f"[任务 {task_id}] 获取 {conn}")
        await asyncio.sleep(0.5)  # 模拟使用连接
    finally:
        pool.release(conn)
        print(f"[任务 {task_id}] 释放 {conn}")


async def connection_pool_demo():
    """连接池示例"""
    async with AsyncConnectionPool(max_connections=3) as pool:
        # 模拟 10 个并发请求，但只有 3 个连接
        tasks = [use_connection(pool, i) for i in range(10)]
        await asyncio.gather(*tasks)


asyncio.run(connection_pool_demo())


# === Part 4: 异步锁与线程安全 ===

class AsyncCounter:
    """异步计数器（线程安全）"""

    def __init__(self) -> None:
        self._count = 0
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        """递增计数器"""
        async with self._lock:
            self._count += 1
            return self._count

    async def get_count(self) -> int:
        """获取计数"""
        async with self._lock:
            return self._count


async def concurrent_increment(counter: AsyncCounter, num_times: int):
    """并发递增"""
    for _ in range(num_times):
        await counter.increment()


async def lock_demo():
    """异步锁示例"""
    counter = AsyncCounter()

    # 10 个协程各递增 100 次
    tasks = [concurrent_increment(counter, 100) for _ in range(10)]
    await asyncio.gather(*tasks)

    final_count = await counter.get_count()
    print(f"最终计数: {final_count} (预期: 1000)")


asyncio.run(lock_demo())


# === Part 5: 事件循环深入理解 ===

async def event_loop_demo():
    """事件循环示例"""
    print("=== 事件循环示例 ===")

    async def task(name: str, duration: float):
        print(f"[{name}] 开始")
        await asyncio.sleep(duration)
        print(f"[{name}] 完成")
        return f"{name} 结果"

    # 1. 创建任务（不执行）
    t1 = asyncio.create_task(task("任务A", 0.5))
    t2 = asyncio.create_task(task("任务B", 0.3))

    print(f"任务创建: t1={t1.get_name()}, t2={t2.get_name()}")
    print(f"初始状态: t1.done()={t1.done()}, t2.done()={t2.done()}")

    # 2. 等待所有任务
    results = await asyncio.gather(t1, t2)

    print(f"最终状态: t1.done()={t1.done()}, t2.done()={t2.done()}")
    print(f"结果: {results}")


asyncio.run(event_loop_demo())


# === Part 6: 性能对比：串行 vs 并发 ===

async def fetch_data(name: str, delay: float) -> str:
    """模拟数据获取"""
    await asyncio.sleep(delay)
    return f"{name} 数据"


async def sequential_demo():
    """串行执行"""
    start = time.perf_counter()
    await fetch_data("A", 0.5)
    await fetch_data("B", 0.3)
    await fetch_data("C", 0.2)
    return time.perf_counter() - start


async def concurrent_demo():
    """并发执行"""
    start = time.perf_counter()
    await asyncio.gather(
        fetch_data("A", 0.5),
        fetch_data("B", 0.3),
        fetch_data("C", 0.2),
    )
    return time.perf_counter() - start


async def performance_comparison():
    """性能对比"""
    seq_time = await sequential_demo()
    print(f"串行耗时: {seq_time:.2f}秒")

    con_time = await concurrent_demo()
    print(f"并发耗时: {con_time:.2f}秒")
    print(f"加速比: {seq_time / con_time:.1f}x")


asyncio.run(performance_comparison())

print("\n=== 异步高级语法示例完成 ===")
