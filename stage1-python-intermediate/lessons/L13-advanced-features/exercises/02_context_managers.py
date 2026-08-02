"""
L12: 进阶特性 - 上下文管理器练习

实现上下文管理器。
"""

from contextlib import contextmanager
from time import perf_counter
import io
import sys


class Transaction:
    """事务上下文管理器"""

    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def __enter__(self) -> "Transaction":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is None:
            self.committed = True
        else:
            self.rolled_back = True
        return False


class TimerState:
    """计时状态。"""

    def __init__(self, start: float) -> None:
        self.start = start
        self.end: float | None = None

    @property
    def elapsed(self) -> float:
        stop = perf_counter() if self.end is None else self.end
        return stop - self.start


@contextmanager
def timer():
    """计时上下文管理器。"""
    state = TimerState(perf_counter())
    try:
        yield state
    finally:
        state.end = perf_counter()


@contextmanager
def redirect_stdout():
    """重定向标准输出到 StringIO。"""
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        yield buffer
    finally:
        sys.stdout = old_stdout


class LazyResource:
    """延迟加载资源。"""

    def __init__(self, factory=object) -> None:
        self.factory = factory
        self._resource = None

    def __enter__(self) -> object:
        if self._resource is None:
            self._resource = self.factory()
        return self._resource

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        close = getattr(self._resource, "close", None)
        if callable(close):
            close()
        self._resource = None
        return False


# === 验证 ===

if __name__ == "__main__":
    # 测试事务
    with Transaction() as t:
        assert not t.committed

    # 测试计时
    import time

    with timer() as t:
        time.sleep(0.01)
        assert t.elapsed > 0

    # 测试 LazyResource
    initialized = [False]

    class MockResource:
        def __init__(self):
            initialized[0] = True

    resource = LazyResource(MockResource)
    assert not initialized[0]
    with resource as r:
        assert isinstance(r, MockResource)
    assert initialized[0]

    # 测试输出重定向
    with redirect_stdout() as output:
        print("captured")
    assert output.getvalue().strip() == "captured"

    print("✅ 所有测试通过！")
