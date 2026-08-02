"""Exercise 1: API Performance Analysis"""

import time
import asyncio
import functools


def timing_decorator(func):
    """Timing decorator"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__}: {elapsed:.2f}ms")
        return result

    return wrapper


@timing_decorator
def slow_function():
    time.sleep(0.01)
    return "done"


def test():
    result = slow_function()
    assert result == "done"
    print("PASS: Timing decorator works")


if __name__ == "__main__":
    test()
