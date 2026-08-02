"""装饰器测试"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import pytest

LESSON_ROOT = Path(__file__).resolve().parent.parent


def _load_module(name: str, file_path: Path) -> object:
    """按物理路径加载模块，注册到 sys.modules（不清理）。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 创建模块 spec")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class TestDecorators:
    """装饰器测试类"""

    def test_memoized_caches_result(self):
        """测试 memoized 装饰器缓存结果"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        expensive_computation = decorators_module.expensive_computation

        # 第一次调用
        start1 = time.time()
        result1 = expensive_computation("task-1")
        _ = time.time() - start1

        # 第二次调用（应该使用缓存）
        start2 = time.time()
        result2 = expensive_computation("task-1")
        _ = time.time() - start2

        assert result1 == result2
        assert result1["task_id"] == "task-1"

    def test_memoized_different_args(self):
        """测试 memoized 对不同参数返回不同结果"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        expensive_computation = decorators_module.expensive_computation

        result1 = expensive_computation("task-1")
        result2 = expensive_computation("task-2")

        assert result1 != result2
        assert result1["task_id"] == "task-1"
        assert result2["task_id"] == "task-2"

    @pytest.mark.asyncio
    async def test_async_logged(self):
        """测试异步日志装饰器"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        async_logged = decorators_module.async_logged

        call_count = 0

        @async_logged
        async def test_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result = await test_func(5)
        assert result == 10
        assert call_count == 1

    def test_logged_decorator(self):
        """测试同步日志装饰器"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        logged = decorators_module.logged

        call_count = 0

        @logged
        def test_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result = test_func(5)
        assert result == 10
        assert call_count == 1


class TestRetryDecorator:
    """重试装饰器测试"""

    @pytest.mark.asyncio
    async def test_retry_succeeds_on_first_try(self):
        """测试首次成功"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        retry = decorators_module.retry

        call_count = 0

        @retry(max_attempts=3)
        async def succeed_once():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await succeed_once()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retry_eventually_succeeds(self):
        """测试最终成功"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        retry = decorators_module.retry

        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        async def fail_twice_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"

        result = await fail_twice_then_succeed()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_fails_after_max_attempts(self):
        """测试达到最大重试次数后失败"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        retry = decorators_module.retry

        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        async def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError, match="Always fails"):
            await always_fail()

        assert call_count == 3

    def test_retry_sync_function(self):
        """测试同步函数重试"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        retry = decorators_module.retry

        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def sync_fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Sync failure")
            return "sync success"

        result = sync_fail_twice()
        assert result == "sync success"
        assert call_count == 3


class TestDecoratorComposition:
    """装饰器组合测试"""

    @pytest.mark.asyncio
    async def test_combined_decorators(self):
        """测试装饰器组合"""
        decorators_module = _load_module("decorators", LESSON_ROOT / "examples" / "03_decorators.py")
        async_logged = decorators_module.async_logged
        retry = decorators_module.retry

        call_count = 0

        @async_logged
        @retry(max_attempts=2, delay=0.01)
        async def combined_func():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First attempt fails")
            return "combined success"

        result = await combined_func()
        assert result == "combined success"
        assert call_count == 2
