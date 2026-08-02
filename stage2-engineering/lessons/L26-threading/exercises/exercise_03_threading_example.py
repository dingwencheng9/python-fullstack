"""兼容旧练习文件：请优先完成 01_producer_consumer.py。"""

from __future__ import annotations

import threading
import time


def worker(name: str) -> None:
    """待实现：模拟一个工作线程。"""
    raise NotImplementedError(f"请实现 {name} 的工作逻辑")


def worker_solution(name: str) -> None:
    """参考实现：打印开始和结束信息。"""
    print(f"{name} 开始工作")
    time.sleep(0.01)
    print(f"{name} 完成")


def run_solution() -> None:
    """运行参考线程。"""
    thread = threading.Thread(target=worker_solution, args=("Worker1",))
    thread.start()
    thread.join()


if __name__ == "__main__":
    run_solution()
