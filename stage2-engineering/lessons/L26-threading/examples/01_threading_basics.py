"""示例 1：Thread / start / join 基础。"""

from __future__ import annotations

import threading
import time


def download_task(name: str, delay: float) -> str:
    """模拟一个 I/O 型任务。"""
    print(f"[{threading.current_thread().name}] 开始 {name}")
    time.sleep(delay)
    result = f"{name} done"
    print(f"[{threading.current_thread().name}] 完成 {result}")
    return result


def run_with_plain_threads() -> None:
    """手动创建线程并等待完成。"""
    threads = [
        threading.Thread(
            target=download_task,
            args=(f"task-{index}", 0.2),
            name=f"worker-{index}",
        )
        for index in range(3)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("所有普通线程已完成")


def run_with_daemon_thread() -> None:
    """演示 daemon 线程只适合后台辅助任务。"""
    stop_event = threading.Event()

    def heartbeat() -> None:
        while not stop_event.is_set():
            print(f"[{threading.current_thread().name}] heartbeat")
            stop_event.wait(0.1)

    thread = threading.Thread(target=heartbeat, name="heartbeat", daemon=True)
    thread.start()
    time.sleep(0.25)
    stop_event.set()
    thread.join(timeout=1)
    print("后台心跳线程已停止")


def main() -> None:
    """运行线程基础示例。"""
    print("=== Thread / start / join ===")
    run_with_plain_threads()
    print("\n=== daemon 线程 ===")
    run_with_daemon_thread()


if __name__ == "__main__":
    main()
