"""兼容旧示例的简单线程工作函数。"""

from __future__ import annotations

import time


def worker(name: str) -> None:
    """模拟一个短任务。"""
    print(f"{name} 开始")
    time.sleep(0.01)
    print(f"{name} 完成")


def main() -> None:
    """保留旧入口，便于手动运行。"""
    worker("Thread-0")


if __name__ == "__main__":
    main()
