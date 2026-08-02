"""Task 模型测试"""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta
from pathlib import Path

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


class TestTaskModel:
    """Task 模型测试类"""

    def test_task_creation_with_defaults(self):
        """测试默认值的任务创建"""
        module = _load_module("task_model", LESSON_ROOT / "examples" / "01_task_model.py")

        task = module.Task(id="1", title="Test Task")
        assert task.status == module.TaskStatus.TODO
        assert task.priority == module.Priority.MEDIUM
        assert task.tags == []
        assert task.created_at is not None

    def test_task_creation_with_all_fields(self):
        """测试带所有字段的任务创建"""
        module = _load_module("task_model", LESSON_ROOT / "examples" / "01_task_model.py")

        due = datetime.now() + timedelta(days=7)
        task = module.Task(
            id="1",
            title="Full Task",
            description="Description",
            status=module.TaskStatus.IN_PROGRESS,
            priority=module.Priority.HIGH,
            due_date=due,
            tags=["work", "urgent"],
        )

        assert task.id == "1"
        assert task.title == "Full Task"
        assert task.description == "Description"
        assert task.status == module.TaskStatus.IN_PROGRESS
        assert task.priority == module.Priority.HIGH
        assert task.due_date == due
        assert task.tags == ["work", "urgent"]
        assert task.created_at is not None

    def test_task_status_transitions(self):
        """测试任务状态转换（不可变方式）"""
        module = _load_module("task_model", LESSON_ROOT / "examples" / "01_task_model.py")

        task = module.Task(id="1", title="Test Task")
        assert task.status == module.TaskStatus.TODO

        # 不可变对象通过创建新实例实现状态转换
        updated_task = module.Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=module.TaskStatus.IN_PROGRESS,
            priority=task.priority,
            tags=task.tags,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=datetime.now(),
        )
        assert updated_task.status == module.TaskStatus.IN_PROGRESS

        # 原始任务保持不变
        assert task.status == module.TaskStatus.TODO

    def test_task_priority_comparison(self):
        """测试优先级比较"""
        module = _load_module("task_model", LESSON_ROOT / "examples" / "01_task_model.py")

        low = module.Task(id="1", title="Low", priority=module.Priority.LOW)
        high = module.Task(id="2", title="High", priority=module.Priority.HIGH)

        assert module.Priority.HIGH > module.Priority.LOW
        assert high.priority == module.Priority.HIGH
        assert low.priority == module.Priority.LOW

    def test_task_immutability(self):
        """测试任务的不可变特性"""
        module = _load_module("task_model", LESSON_ROOT / "examples" / "01_task_model.py")

        task = module.Task(id="1", title="Original")
        original_title = task.title

        # 标题不应被修改
        assert task.title == original_title

        # 尝试修改应无效（如果是 dataclass(frozen=True)）
        try:
            task.title = "Modified"
        except (AttributeError, TypeError):
            pass  # 如果是不可变 dataclass，这会抛出异常

        assert task.title == original_title
