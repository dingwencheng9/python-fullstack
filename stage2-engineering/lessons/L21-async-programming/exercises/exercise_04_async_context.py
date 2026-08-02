"""练习 4: 优雅关闭 + 熔断器.

学习目标：
- 实现 SIGTERM/SIGINT 信号触发的优雅关闭
- 使用 asyncio.Event 协调工作协程停止
- 实现熔断器模式防止级联失败
"""

from __future__ import annotations

import asyncio


# ============================================================
# 优雅关闭
# ============================================================


class GracefulShutdown:
    """优雅关闭管理器。"""

    def __init__(self, max_wait: float = 5.0) -> None:
        self.shutdown_event = asyncio.Event()
        self.tasks: set[asyncio.Task] = set()
        self.max_wait = max_wait

    def trigger(self) -> None:
        """触发关闭。"""
        if not self.shutdown_event.is_set():
            print("  关闭信号触发")
            self.shutdown_event.set()

    async def register(self, coro) -> asyncio.Task:
        """注册工作协程。"""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task

    async def wait_for_shutdown(self) -> None:
        """等待关闭信号。"""
        await self.shutdown_event.wait()


async def worker(worker_id: int, shutdown: GracefulShutdown) -> None:
    """工作协程。"""
    try:
        while not shutdown.shutdown_event.is_set():
            print(f"  Worker-{worker_id} 运行中")
            await asyncio.sleep(0.5)
        print(f"  Worker-{worker_id} 收到停止信号")
    except asyncio.CancelledError:
        print(f"  Worker-{worker_id} 被取消")
        raise


async def test_graceful_shutdown() -> None:
    """测试优雅关闭。"""
    print("=" * 60)
    print("练习 4: 优雅关闭 + 熔断器")
    print("=" * 60)
    print()

    shutdown = GracefulShutdown()

    # 模拟 1.5 秒后触发关闭
    async def trigger_later():
        await asyncio.sleep(1.5)
        shutdown.trigger()

    # 注册工作协程
    await shutdown.register(worker(1, shutdown))
    await shutdown.register(worker(2, shutdown))

    # 并发运行关闭管理器和工作协程
    await asyncio.gather(
        shutdown.wait_for_shutdown(),
        trigger_later(),
    )

    print()
    print("✅ 优雅关闭测试通过")


# ============================================================
# 熔断器
# ============================================================


class CircuitBreaker:
    """熔断器。"""

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 5.0,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = "closed"
        self.lock = asyncio.Lock()

    async def call(self, func) -> str:
        """通过熔断器调用函数（func 应为协程）。"""
        async with self.lock:
            if self.state == "open":
                raise RuntimeError("Circuit OPEN")

        try:
            result = await func()
            async with self.lock:
                if self.state == "half-open":
                    self.state = "closed"
                self.failure_count = 0
            return result
        except Exception:
            async with self.lock:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
            raise


async def test_circuit_breaker() -> None:
    """测试熔断器。"""
    breaker = CircuitBreaker(failure_threshold=3)
    open_count = 0
    fail_count = 0

    async def fail_op() -> None:
        raise ValueError("失败")

    # 触发熔断：3 次失败后电路打开
    for i in range(3):
        try:
            await breaker.call(fail_op)
        except ValueError:
            fail_count += 1

    assert fail_count == 3, f"期望 3 次失败，得到 {fail_count}"
    assert breaker.state == "open", f"期望 open，得到 {breaker.state}"

    # 电路打开后，调用被拒绝
    try:
        await breaker.call(fail_op)
    except RuntimeError:
        open_count += 1

    assert open_count == 1, "电路打开后应拒绝调用"
    print()
    print(f"  失败次数: {fail_count}，熔断拒绝: {open_count} 次")
    print("✅ 熔断器测试通过")


# ============================================================
# 自检入口
# ============================================================


async def main() -> None:
    try:
        await test_graceful_shutdown()
        await test_circuit_breaker()
    except Exception as exc:
        print(f"❌ 错误: {exc}")
        raise SystemExit(1) from exc

    print()
    print("🎉 练习 4 完成！")
    print("下一步: exercise_05_retry_backoff.py")


if __name__ == "__main__":
    asyncio.run(main())
