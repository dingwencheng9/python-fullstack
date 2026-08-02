"""异步存储层 - 展示 asyncio.TaskGroup 并发处理

此模块展示异步文件存储和任务持久化。
作为独立模块运行，不依赖同一包内的其他模块。
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

# 为避免循环依赖，此处定义简化版 Task 序列化接口
# 测试时会从 01_task_model.py 加载完整 Task 类


class AsyncStorage:
    """异步文件存储"""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = asyncio.Lock()

    async def read(self) -> dict | None:
        """异步读取文件"""
        if not self.path.exists():
            return None
        async with self._lock:
            content = await asyncio.to_thread(self.path.read_text)
            return json.loads(content)

    async def write(self, data: dict) -> None:
        """异步写入文件"""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with self._lock:
            await asyncio.to_thread(self.path.write_text, json.dumps(data, indent=2))


class TaskStorage:
    """任务存储层 - 管理任务列表的持久化"""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self._async_storage = AsyncStorage(storage_path)

    async def save(self, tasks_data: list[dict]) -> None:
        """保存任务列表（接收字典列表）"""
        data = {"tasks": tasks_data}
        await self._async_storage.write(data)

    async def load(self) -> list[dict]:
        """加载任务列表（返回字典列表）"""
        data = await self._async_storage.read()
        if data is None:
            return []
        return data.get("tasks", [])

    async def save_task(self, task_data: dict) -> None:
        """保存单个任务（并发安全）"""
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.save([task_data]))

    async def load_with_retry(self, retries: int = 3) -> list[dict]:
        """带重试的加载"""
        for attempt in range(retries):
            try:
                return await self.load()
            except Exception:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(0.1 * (attempt + 1))


async def demo_concurrent_save() -> None:
    """演示并发保存"""
    import tempfile

    storage_path = Path(tempfile.gettempdir()) / "task_tracker_demo.json"
    storage = TaskStorage(storage_path)

    # 并发保存多个任务
    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            task_data = {"id": str(i), "title": f"Task {i}"}
            tg.create_task(storage.save_task(task_data))

    print(f"保存完成，文件位置: {storage_path}")
    tasks = await storage.load()
    print(f"加载了 {len(tasks)} 个任务")


if __name__ == "__main__":
    asyncio.run(demo_concurrent_save())
