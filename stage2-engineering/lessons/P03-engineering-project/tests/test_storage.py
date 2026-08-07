"""异步存储层测试"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
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


class TestAsyncStorage:
    """异步存储测试类"""

    @pytest.mark.asyncio
    async def test_save_and_load(self, tmp_storage_path: Path):
        """测试保存和加载"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage = TaskStorage(tmp_storage_path)
        tasks_data = [
            {"id": "1", "title": "Task 1"},
            {"id": "2", "title": "Task 2"},
        ]

        await storage.save(tasks_data)
        loaded = await storage.load()

        assert len(loaded) == 2
        assert loaded[0]["id"] == "1"
        assert loaded[1]["title"] == "Task 2"

    @pytest.mark.asyncio
    async def test_load_empty_storage(self, tmp_storage_path: Path):
        """测试加载空存储"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage = TaskStorage(tmp_storage_path)
        tasks = await storage.load()

        assert tasks == []

    @pytest.mark.asyncio
    async def test_load_nonexistent_file(self, tmp_storage_path: Path):
        """测试加载不存在的文件"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage = TaskStorage(tmp_storage_path)
        tasks = await storage.load()

        assert tasks == []

    @pytest.mark.asyncio
    async def test_save_creates_parent_directory(self, tmp_path: Path):
        """测试保存时自动创建父目录"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage_path = tmp_path / "subdir" / "tasks.json"
        storage = TaskStorage(storage_path)

        assert not storage_path.parent.exists()

        tasks = [{"id": "1", "title": "Test"}]
        await storage.save(tasks)

        assert storage_path.parent.exists()
        assert storage_path.exists()

    @pytest.mark.asyncio
    async def test_update_task(self, tmp_storage_path: Path):
        """测试更新任务"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage = TaskStorage(tmp_storage_path)

        # 创建任务
        tasks = [{"id": "1", "title": "Original", "status": "todo"}]
        await storage.save(tasks)

        # 更新任务
        loaded = await storage.load()
        loaded[0]["title"] = "Updated"
        loaded[0]["status"] = "done"
        await storage.save(loaded)

        # 验证更新
        updated = await storage.load()
        assert updated[0]["title"] == "Updated"
        assert updated[0]["status"] == "done"

    @pytest.mark.asyncio
    async def test_delete_task(self, tmp_storage_path: Path):
        """测试删除任务"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        TaskStorage = storage_module.TaskStorage

        storage = TaskStorage(tmp_storage_path)

        # 创建任务
        tasks = [{"id": "1", "title": "Keep"}, {"id": "2", "title": "Delete"}]
        await storage.save(tasks)

        # 删除任务
        loaded = await storage.load()
        loaded = [t for t in loaded if t["id"] != "2"]
        await storage.save(loaded)

        # 验证删除
        remaining = await storage.load()
        assert len(remaining) == 1
        assert remaining[0]["id"] == "1"


class TestAsyncStorageLowLevel:
    """AsyncStorage 底层测试"""

    @pytest.mark.asyncio
    async def test_async_read_nonexistent(self, tmp_path: Path):
        """测试读取不存在的文件"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        AsyncStorage = storage_module.AsyncStorage

        storage = AsyncStorage(tmp_path / "nonexistent.json")
        result = await storage.read()

        assert result is None

    @pytest.mark.asyncio
    async def test_async_write_and_read(self, tmp_path: Path):
        """测试异步写入和读取"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        AsyncStorage = storage_module.AsyncStorage

        storage = AsyncStorage(tmp_path / "test.json")
        test_data = {"key": "value", "number": 42}

        await storage.write(test_data)
        result = await storage.read()

        assert result == test_data

    @pytest.mark.asyncio
    async def test_concurrent_write(self, tmp_path: Path):
        """测试并发写入"""
        storage_module = _load_module("task_storage", LESSON_ROOT / "examples" / "02_task_storage.py")
        AsyncStorage = storage_module.AsyncStorage

        storage = AsyncStorage(tmp_path / "concurrent.json")

        async def write_task(i: int):
            await storage.write({"index": i})

        # 并发写入
        await asyncio.gather(*[write_task(i) for i in range(5)])

        # 最终内容应该是最后一个写入的
        result = await storage.read()
        assert "index" in result
