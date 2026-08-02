"""
L12: 高级特性 - 上下文管理器练习解答

实现上下文管理器。
"""

from contextlib import contextmanager
from typing import Any
from collections.abc import Generator


class FileManager:
    """文件管理器"""

    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self) -> Any:
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.file:
            self.file.close()
        return False  # 不抑制异常


class Transaction:
    """事务管理器"""

    def __init__(self):
        self.operations: list = []
        self.committed = False

    def __enter__(self) -> "Transaction":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            print(f"事务失败，回滚 {len(self.operations)} 个操作")
            self.operations.clear()
            return False  # 不抑制异常，让它继续传播
        if not self.committed:
            print(f"提交 {len(self.operations)} 个操作")
            self.committed = True
        return False


class Timer:
    """计时器"""

    def __init__(self, name: str = "操作"):
        self.name = name
        self.start = 0.0
        self.elapsed = 0.0

    def __enter__(self) -> "Timer":
        from time import perf_counter

        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        from time import perf_counter

        self.elapsed = perf_counter() - self.start
        print(f"{self.name} 耗时: {self.elapsed:.4f}秒")
        return False


@contextmanager
def managed_resource(name: str) -> Generator[None]:
    """资源管理器"""
    print(f"获取资源: {name}")
    try:
        yield
    finally:
        print(f"释放资源: {name}")


@contextmanager
def redirect_stdout(filename: str) -> Generator[None]:
    """重定向标准输出"""
    import sys

    old_stdout = sys.stdout
    sys.stdout = open(filename, "w")
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = old_stdout


@contextmanager
def transaction_context(operations: list) -> Generator[None]:
    """事务上下文"""
    try:
        yield operations
        print(f"提交 {len(operations)} 个操作")
    except Exception:
        print("事务回滚")
        operations.clear()
        raise
