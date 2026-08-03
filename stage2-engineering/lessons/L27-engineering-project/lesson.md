# L27: 工程化综合项目

> **课程编号**: L27
> **所属阶段**: Stage 2 - 现代工程
> **预计时长**: 5-8 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L19 (pytest), L20 (工具链), L21 (异步), L22 (装饰器), L23 (新特性), L24 (高级异步), L25 (性能), L26 (线程)
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 📚 项目概述

### 项目：任务追踪 CLI 工具（Task Tracker CLI）

一个完整的命令行任务管理工具，综合运用 Stage 2 工程化内容：

- **pytest 完整实战**：单元测试、Mock、Fixture、参数化测试
- **现代化工具链**：uv + Ruff + mypy + 类型注解
- **异步编程**：使用 asyncio.TaskGroup 并发处理任务
- **装饰器**：日志、缓存、权限检查装饰器
- **CI/CD**：GitHub Actions 自动化流水线
- **类型安全**：mypy strict 模式

### 功能需求

1. **任务管理**：CRUD 操作（创建、读取、更新、删除）
2. **任务状态**：待办、进行中、已完成
3. **优先级**：高、中、低
4. **截止日期**：日期时间管理
5. **标签系统**：多标签分类
6. **搜索过滤**：按状态、标签、日期搜索
7. **数据持久化**：JSON 文件存储
8. **导出功能**：CSV/JSON 格式导出

---

## 🏗️ 项目结构

### 目录组织

```
L25-engineering-project/
├── examples/                  # 示例代码
│   ├── 01_task_model.py       # 任务数据模型
│   ├── 02_task_storage.py     # 异步存储层
│   ├── 03_decorators.py       # 自定义装饰器
│   └── 04_cli_interface.py    # CLI 接口
├── exercises/                 # 练习题
│   └── exercise_01_task_model.py
├── solutions/                 # 参考答案
│   ├── __init__.py
│   └── solution_01_task_model.py
├── tests/                     # 测试用例
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_decorators.py
│   └── test_cli.py
├── pyproject.toml             # 项目配置
├── verify.py                  # 课程自检脚本
├── README.md
└── lesson.md
```

---

## 📚 学习内容

### Part 1: 项目架构设计 (1h)

#### 1.1 领域模型

```python
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

#### 1.2 存储层设计

```python
from pathlib import Path
import asyncio
import json

class TaskStorage:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._lock = asyncio.Lock()

    async def save(self, tasks: list[Task]) -> None:
        async with self._lock:
            data = [self._serialize(t) for t in tasks]
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            await asyncio.to_thread(self.storage_path.write_text, json.dumps(data, indent=2))

    async def load(self) -> list[Task]:
        if not self.storage_path.exists():
            return []
        async with self._lock:
            content = await asyncio.to_thread(self.storage_path.read_text)
            data = json.loads(content)
            return [self._deserialize(d) for d in data]
```

---

### Part 2: 装饰器实战 (1.5h)

#### 2.1 日志装饰器

```python
import functools
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=Callable)

def logged(func: T) -> T:
    """记录函数调用的日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"调用 {func.__name__} (args={args}, kwargs={kwargs})")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} 返回 {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} 异常: {e}")
            raise
    return wrapper  # type: ignore

def async_logged(func: T) -> T:
    """异步函数的日志装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.debug(f"调用 {func.__name__}")
        result = await func(*args, **kwargs)
        logger.debug(f"{func.__name__} 完成")
        return result
    return wrapper  # type: ignore
```

#### 2.2 缓存装饰器

```python
from functools import lru_cache

def memoized(maxsize: int = 128):
    """带配置的最大结果缓存装饰器"""
    def decorator(func: T) -> T:
        cached_func = lru_cache(maxsize=maxsize)(func)
        return cached_func  # type: ignore
    return decorator

# 使用示例
@memoized(maxsize=256)
def expensive_computation(task_id: str) -> dict:
    """耗时的计算操作"""
    # 模拟耗时操作
    import time
    time.sleep(0.1)
    return {"task_id": task_id, "result": "computed"}
```

#### 2.3 重试装饰器

```python
import asyncio

def retry(max_attempts: int = 3, delay: float = 1.0):
    """失败自动重试的装饰器"""
    def decorator(func: T) -> T:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay)
            raise last_exception

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper  # type: ignore
    return decorator
```

---

### Part 3: 异步编程实战 (1.5h)

#### 3.1 TaskGroup 并发处理

```python
async def process_multiple_tasks(task_ids: list[str]) -> list[dict]:
    """并发处理多个任务"""
    results = []

    async with asyncio.TaskGroup() as tg:
        async def fetch_and_process(task_id: str) -> dict:
            # 并发获取任务详情
            task_data = await fetch_task(task_id)
            # 并发计算任务统计
            stats = await compute_stats(task_data)
            return {"id": task_id, "data": task_data, "stats": stats}

        for task_id in task_ids:
            results.append(tg.create_task(fetch_and_process(task_id)))

    return [r.result() for r in results]
```

#### 3.2 信号处理

```python
import signal

async def graceful_shutdown():
    """优雅关闭：处理中断信号"""
    shutdown_event = asyncio.Event()

    def signal_handler():
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    await shutdown_event.wait()
    # 执行清理逻辑
    await cleanup()
```

---

### Part 4: CLI 接口设计 (1h)

#### 4.1 argparse 高级用法

```python
import argparse
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - 任务追踪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 添加任务
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("-t", "--title", required=True, help="任务标题")
    add_parser.add_argument("-d", "--description", help="任务描述")
    add_parser.add_argument("-p", "--priority", choices=["high", "medium", "low"], default="medium")
    add_parser.add_argument("--tags", nargs="+", help="任务标签")
    add_parser.add_argument("--due", type=lambda s: datetime.fromisoformat(s), help="截止日期 (ISO格式)")

    # 列表任务
    list_parser = subparsers.add_parser("list", help="列出任务")
    list_parser.add_argument("-s", "--status", choices=["todo", "in_progress", "done"])
    list_parser.add_argument("--tag", help="按标签筛选")

    # 更新任务
    update_parser = subparsers.add_parser("update", help="更新任务")
    update_parser.add_argument("id", help="任务 ID")
    update_parser.add_argument("--status", choices=["todo", "in_progress", "done"])
    update_parser.add_argument("--title", help="新标题")

    return parser
```

---

### Part 5: pytest 测试实战 (1.5h)

#### 5.1 完整测试用例

```python
# tests/test_models.py
import pytest
from datetime import datetime, timedelta
from task_tracker import Task, TaskStatus, Priority

class TestTask:
    def test_task_creation_with_defaults(self):
        """测试默认值的任务创建"""
        task = Task(id="1", title="Test Task")
        assert task.status == TaskStatus.TODO
        assert task.priority == Priority.MEDIUM
        assert task.tags == []
        assert task.created_at is not None

    def test_task_status_transition(self):
        """测试状态转换"""
        task = Task(id="1", title="Test")
        task.status = TaskStatus.IN_PROGRESS
        assert task.status == TaskStatus.IN_PROGRESS
        task.status = TaskStatus.DONE
        assert task.status == TaskStatus.DONE

    def test_task_with_due_date(self):
        """测试带截止日期的任务"""
        due = datetime.now() + timedelta(days=7)
        task = Task(id="1", title="Deadline Task", due_date=due)
        assert task.due_date == due
        assert task.due_date > datetime.now()

    @pytest.mark.parametrize("priority", list(Priority))
    def test_task_priorities(self, priority: Priority):
        """参数化测试所有优先级"""
        task = Task(id="1", title="Priority Test", priority=priority)
        assert task.priority == priority
```

#### 5.2 Mock 和 Patch

```python
# tests/test_storage.py
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from task_tracker import TaskStorage, Task, TaskStatus

@pytest.fixture
def storage(tmp_path):
    return TaskStorage(tmp_path / "tasks.json")

@pytest.fixture
def sample_tasks():
    return [
        Task(id="1", title="Task 1", status=TaskStatus.TODO),
        Task(id="2", title="Task 2", status=TaskStatus.DONE),
    ]

class TestTaskStorage:
    @pytest.mark.asyncio
    async def test_save_and_load(self, storage, sample_tasks):
        """测试保存和加载"""
        await storage.save(sample_tasks)
        loaded = await storage.load()

        assert len(loaded) == 2
        assert loaded[0].id == "1"
        assert loaded[1].title == "Task 2"

    @pytest.mark.asyncio
    async def test_load_empty_storage(self, storage):
        """测试加载空存储"""
        tasks = await storage.load()
        assert tasks == []

    @pytest.mark.asyncio
    async def test_concurrent_save(self, storage, sample_tasks):
        """测试并发保存（TaskGroup）"""
        async with asyncio.TaskGroup() as tg:
            for task in sample_tasks:
                tg.create_task(storage.save([task]))

        loaded = await storage.load()
        assert len(loaded) >= 1
```

---

## 🧪 练习题

### 练习 1: 完善任务模型 (⭐)

实现 `Task` 类的以下方法：

```python
# exercises/exercise_01_task_model.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def is_overdue(self) -> bool:
        """检查任务是否已过期"""
        # TODO: 实现过期检查
        pass

    def days_until_due(self) -> int | None:
        """计算距离截止日期的天数"""
        # TODO: 实现天数计算
        pass

    def to_dict(self) -> dict:
        """序列化为字典"""
        # TODO: 实现序列化
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典反序列化"""
        # TODO: 实现反序列化
        pass
```

**验收标准**：
- [ ] `is_overdue()` 正确判断过期任务
- [ ] `days_until_due()` 正确计算剩余天数（负数表示已过期）
- [ ] `to_dict()` / `from_dict()` 正确序列化/反序列化

---

### 练习 2: 异步存储层 (⭐⭐)

实现异步存储层：

```python
# examples/02_task_storage.py
from pathlib import Path
import asyncio
import json
class AsyncStorage:
    def __init__(self, path: Path):
        self.path = path
        self._lock = asyncio.Lock()

    async def read(self) -> dict | None:
        """异步读取文件"""
        # TODO: 使用 asyncio.to_thread 避免阻塞
        pass

    async def write(self, data: dict) -> None:
        """异步写入文件"""
        # TODO: 使用 asyncio.to_thread 避免阻塞
        pass
```

---

### 练习 3: CLI 装饰器 (⭐⭐⭐)

实现一个权限检查装饰器：

```python
# examples/03_decorators.py
import functools
from typing import Callable, TypeVar

T = TypeVar("T")

def require_admin(func: Callable[..., T]) -> Callable[..., T]:
    """要求管理员权限的装饰器"""
    # TODO: 检查环境变量或配置
    # 如果不是管理员，抛出 PermissionError
    pass

def rate_limit(calls: int, period: float):
    """限流装饰器"""
    # TODO: 限制函数调用频率
    # 超过限制时抛出 RateLimitError
    pass
```

---

### 练习 4: 完整 CLI 工具 (⭐⭐⭐⭐)

整合所有组件，实现完整的 CLI 工具：

```python
# examples/04_cli_interface.py
import asyncio
import argparse
from pathlib import Path
from task_tracker import TaskManager, TaskStorage

async def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # 实现子命令: add, list, update, delete, export
    # ...

    args = parser.parse_args()

    storage = TaskStorage(Path.home() / ".task-tracker" / "tasks.json")
    manager = TaskManager(storage)

    if args.command == "add":
        await manager.add_task(
            title=args.title,
            description=args.description or "",
            priority=args.priority or "medium",
        )
    elif args.command == "list":
        tasks = await manager.list_tasks(status=args.status)
        for task in tasks:
            print(f"[{task.status.value}] {task.title}")
    # ... 其他命令

if __name__ == "__main__":
    asyncio.run(main())
```

**验收标准**：
- [ ] 实现 `add`、`list`、`update`、`delete`、`export` 命令
- [ ] 支持 `--json` 输出格式
- [ ] 集成所有装饰器（日志、缓存、重试）
- [ ] 通过 pytest 测试

---

## 📊 测试覆盖率目标

| 模块 | 覆盖率目标 | 说明 |
|------|-----------|------|
| models | 90%+ | Task 模型所有方法 |
| storage | 85%+ | 异步 I/O 边界测试 |
| decorators | 80%+ | 装饰器行为验证 |
| cli | 75%+ | CLI 命令覆盖 |

---

## 🔧 GitHub Actions CI/CD 配置

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 安装 uv
        uses: astral-sh/setup-uv@v4

      - name: 安装依赖
        run: uv sync --dev

      - name: 代码检查
        run: uv run ruff check .

      - name: 类型检查
        run: uv run mypy .

      - name: 测试
        run: uv run pytest --cov=src --cov-report=xml
```

---

## 📚 扩展阅读

- [PEP 695 - 类型参数语法](https://peps.python.org/pep-0695/)
- [pytest 文档](https://docs.pytest.org/)
- [asyncio TaskGroup](https://docs.python.org/3/library/asyncio-task.html#taskgroup)
- [uv 工具链](https://github.com/astral-sh/uv)

---

## 🧪 本课验证命令

在仓库根目录运行：

```bash
python3 -m py_compile \
  stage2-engineering/lessons/L25-engineering-project/examples/*.py \
  stage2-engineering/lessons/L25-engineering-project/exercises/*.py \
  stage2-engineering/lessons/L25-engineering-project/solutions/*.py \
  stage2-engineering/lessons/L25-engineering-project/tests/*.py \
  stage2-engineering/lessons/L25-engineering-project/*.py

uv run pytest stage2-engineering/lessons/L25-engineering-project/tests -q
uv run python stage2-engineering/lessons/L25-engineering-project/verify.py
uv run ruff check stage2-engineering/lessons/L25-engineering-project
```

## ✅ 完成标准

- [ ] 理解工程化项目架构
- [ ] 掌握装饰器设计模式
- [ ] 熟练使用 pytest + Mock
- [ ] 实现完整的 CLI 工具
- [ ] 配置 CI/CD 流水线
- [ ] 测试覆盖率 ≥ 80%


---

## 🔗 下一步

- [Stage 3: Web 开发基础](../../../stage3-web-basics/) — 进入 Web 开发世界
- [L26: HTTP 协议与抓包](../../../stage3-web-basics/lessons/L26-http/) — 互联网通信基础

---
