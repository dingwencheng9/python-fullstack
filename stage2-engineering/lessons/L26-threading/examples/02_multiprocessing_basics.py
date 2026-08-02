"""兼容旧文件名：本课重点是 threading，进程内容仅作对比。"""

from __future__ import annotations

import os
import time
from multiprocessing import Process


def process_worker(name: str) -> None:
    """模拟一个独立进程任务。"""
    print(f"进程 {name} 启动，pid={os.getpid()}")
    time.sleep(0.05)
    print(f"进程 {name} 完成")


def main() -> None:
    """运行最小多进程对比示例。"""
    process = Process(target=process_worker, args=("demo",))
    process.start()
    process.join()


if __name__ == "__main__":
    main()
