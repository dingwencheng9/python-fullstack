"""CLI 接口测试"""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime
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


class TestCLI:
    """CLI 测试类 - 核心功能测试"""

    @pytest.mark.asyncio
    async def test_cli_add_command(self, tmp_path: Path):
        """测试添加任务功能"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage
        create_parser = cli_module.create_parser

        storage_path = tmp_path / "tasks.json"
        storage = TaskStorage(storage_path)

        # 测试参数解析
        parser = create_parser()
        args = parser.parse_args(["add", "-t", "Test Task", "-p", "high"])
        assert args.command == "add"
        assert args.title == "Test Task"
        assert args.priority == "high"

        # 测试存储
        task_data = {
            "id": str(datetime.now().timestamp()),
            "title": args.title,
            "status": "todo",
            "priority": args.priority,
            "tags": [],
        }
        tasks = await storage.load()
        tasks.append(task_data)
        await storage.save(tasks)

        loaded = await storage.load()
        assert len(loaded) == 1
        assert loaded[0]["title"] == "Test Task"

    @pytest.mark.asyncio
    async def test_cli_list_command(self, tmp_path: Path):
        """测试列表功能"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage

        storage_path = tmp_path / "tasks.json"
        storage = TaskStorage(storage_path)

        # 创建多个任务
        tasks_data = [
            {"id": "1", "title": "Todo Task", "status": "todo"},
            {"id": "2", "title": "Done Task", "status": "done"},
            {"id": "3", "title": "Another Todo", "status": "todo"},
        ]
        await storage.save(tasks_data)

        # 验证加载
        loaded = await storage.load()
        assert len(loaded) == 3

        # 筛选待办
        todos = [t for t in loaded if t["status"] == "todo"]
        assert len(todos) == 2

    @pytest.mark.asyncio
    async def test_cli_update_command(self, tmp_path: Path):
        """测试更新功能"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage

        storage_path = tmp_path / "tasks.json"
        storage = TaskStorage(storage_path)

        # 创建任务
        tasks = [{"id": "1", "title": "Original", "status": "todo"}]
        await storage.save(tasks)

        # 更新任务
        loaded = await storage.load()
        loaded[0]["title"] = "Updated"
        loaded[0]["status"] = "in_progress"
        await storage.save(loaded)

        # 验证更新
        updated = await storage.load()
        assert updated[0]["title"] == "Updated"
        assert updated[0]["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_cli_delete_command(self, tmp_path: Path):
        """测试删除功能"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage

        storage_path = tmp_path / "tasks.json"
        storage = TaskStorage(storage_path)

        # 创建任务
        tasks = [
            {"id": "1", "title": "Keep"},
            {"id": "2", "title": "Delete"},
        ]
        await storage.save(tasks)

        # 删除任务
        loaded = await storage.load()
        loaded = [t for t in loaded if t["id"] != "2"]
        await storage.save(loaded)

        # 验证删除
        remaining = await storage.load()
        assert len(remaining) == 1
        assert remaining[0]["id"] == "1"


class TestCLIWithRealStorage:
    """使用真实存储的 CLI 测试"""

    @pytest.mark.asyncio
    async def test_workflow_add_list(self, tmp_path: Path):
        """测试添加后列表的工作流"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage

        storage_path = tmp_path / "workflow.json"
        storage = TaskStorage(storage_path)

        # 添加任务
        task_data = {"id": "1", "title": "Workflow Test"}
        tasks = await storage.load()
        tasks.append(task_data)
        await storage.save(tasks)

        # 列出任务
        listed = await storage.load()
        assert len(listed) == 1
        assert listed[0]["title"] == "Workflow Test"

    @pytest.mark.asyncio
    async def test_workflow_full_crud(self, tmp_path: Path):
        """测试完整的 CRUD 工作流"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        TaskStorage = cli_module.TaskStorage

        storage_path = tmp_path / "crud.json"
        storage = TaskStorage(storage_path)

        # Create
        tasks = [{"id": "1", "title": "Create Test", "status": "todo"}]
        await storage.save(tasks)

        # Read
        loaded = await storage.load()
        assert len(loaded) == 1

        # Update
        loaded[0]["title"] = "Updated Test"
        loaded[0]["status"] = "done"
        await storage.save(loaded)

        # Verify Update
        updated = await storage.load()
        assert updated[0]["title"] == "Updated Test"
        assert updated[0]["status"] == "done"

        # Delete
        await storage.save([])

        # Verify Delete
        empty = await storage.load()
        assert len(empty) == 0


class TestCLIParser:
    """CLI 参数解析器测试"""

    def test_create_parser(self):
        """测试创建解析器"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        assert parser is not None
        assert parser.description == "Task Tracker CLI - 任务追踪工具"

    def test_parser_add_subcommand(self):
        """测试 add 子命令"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        args = parser.parse_args(["add", "-t", "Test Task", "-p", "high"])

        assert args.command == "add"
        assert args.title == "Test Task"
        assert args.priority == "high"

    def test_parser_list_subcommand(self):
        """测试 list 子命令"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        args = parser.parse_args(["list", "-s", "todo", "--json"])

        assert args.command == "list"
        assert args.status == "todo"
        assert args.json is True

    def test_parser_update_subcommand(self):
        """测试 update 子命令"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        args = parser.parse_args(["update", "123", "--status", "done"])

        assert args.command == "update"
        assert args.id == "123"
        assert args.status == "done"

    def test_parser_delete_subcommand(self):
        """测试 delete 子命令"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        args = parser.parse_args(["delete", "456"])

        assert args.command == "delete"
        assert args.id == "456"

    def test_parser_export_subcommand(self):
        """测试 export 子命令"""
        cli_module = _load_module("cli_interface", LESSON_ROOT / "examples" / "04_cli_interface.py")
        create_parser = cli_module.create_parser

        parser = create_parser()
        args = parser.parse_args(["export", "-f", "csv", "-o", "output.csv"])

        assert args.command == "export"
        assert args.format == "csv"
        assert args.output == Path("output.csv")
