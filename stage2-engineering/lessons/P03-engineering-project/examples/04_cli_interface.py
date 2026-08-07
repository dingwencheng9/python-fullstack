"""CLI 接口示例 - 展示 argparse 高级用法

此模块作为独立模块运行，不依赖同一包内的其他模块。
CLI 逻辑使用字典数据格式，测试时可以与 Task 模型混合使用。
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import io
import json
import sys
from datetime import datetime
from pathlib import Path

# 注意：为了可测试性，此模块不直接依赖 Task/TaskStorage
# 测试时可以从其他模块导入并混合使用


def parse_iso_datetime(value: str) -> datetime:
    """解析 ISO 格式日期时间字符串，供 argparse 使用。"""
    return datetime.fromisoformat(value)


def create_parser() -> argparse.ArgumentParser:
    """创建 CLI 参数解析器"""
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - 任务追踪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--storage",
        type=Path,
        default=Path.home() / ".task-tracker" / "tasks.json",
        help="存储文件路径",
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 添加任务
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("-t", "--title", required=True, help="任务标题")
    add_parser.add_argument("-d", "--description", help="任务描述")
    add_parser.add_argument(
        "-p",
        "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="优先级",
    )
    add_parser.add_argument("--tags", nargs="+", help="任务标签")
    add_parser.add_argument("--due", type=parse_iso_datetime, help="截止日期 (ISO格式)")

    # 列表任务
    list_parser = subparsers.add_parser("list", help="列出任务")
    list_parser.add_argument("-s", "--status", choices=["todo", "in_progress", "done"], help="按状态筛选")
    list_parser.add_argument("--tag", help="按标签筛选")
    list_parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    # 更新任务
    update_parser = subparsers.add_parser("update", help="更新任务")
    update_parser.add_argument("id", help="任务 ID")
    update_parser.add_argument("--status", choices=["todo", "in_progress", "done"], help="新状态")
    update_parser.add_argument("--title", help="新标题")

    # 删除任务
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", help="任务 ID")

    # 导出任务
    export_parser = subparsers.add_parser("export", help="导出任务")
    export_parser.add_argument("-f", "--format", choices=["json", "csv"], default="json", help="导出格式")
    export_parser.add_argument("-o", "--output", type=Path, help="输出文件路径")

    return parser


class TaskStorage:
    """任务存储层 - 管理任务列表的持久化（独立实现）"""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    async def save(self, tasks_data: list[dict]) -> None:
        """保存任务列表（接收字典列表）"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {"tasks": tasks_data}
        content = json.dumps(data, indent=2, default=str)
        await asyncio.to_thread(self.storage_path.write_text, content)

    async def load(self) -> list[dict]:
        """加载任务列表（返回字典列表）"""
        if not self.storage_path.exists():
            return []
        content = await asyncio.to_thread(self.storage_path.read_text)
        data = json.loads(content)
        return data.get("tasks", [])


def task_to_dict(task_data: dict) -> dict:
    """将任务数据转为字典"""
    return task_data


async def handle_add(storage: TaskStorage, args: argparse.Namespace) -> int:
    """处理 add 命令"""
    task_data = {
        "id": str(datetime.now().timestamp()),
        "title": args.title,
        "description": args.description or "",
        "status": "todo",
        "priority": args.priority,
        "tags": args.tags or [],
        "due_date": args.due.isoformat() if args.due else None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    tasks = await storage.load()
    tasks.append(task_data)
    await storage.save(tasks)
    print(f"✓ 任务已添加: {task_data['title']}")
    return 0


async def handle_list(storage: TaskStorage, args: argparse.Namespace) -> int:
    """处理 list 命令"""
    tasks = await storage.load()

    if args.status:
        tasks = [t for t in tasks if t.get("status") == args.status]
    if args.tag:
        tasks = [t for t in tasks if args.tag in t.get("tags", [])]

    if args.json:
        print(json.dumps(tasks, indent=2))
    else:
        if not tasks:
            print("没有找到任务")
        for task in tasks:
            status_icon = {"todo": "○", "in_progress": "◐", "done": "●"}.get(task.get("status", "todo"), "○")
            priority = task.get("priority", "medium")
            print(f"  {status_icon} [{task.get('id', '?')}] {task.get('title', '')} ({priority})")

    return 0


async def handle_update(storage: TaskStorage, args: argparse.Namespace) -> int:
    """处理 update 命令"""
    tasks = await storage.load()
    task = next((t for t in tasks if t.get("id") == args.id), None)

    if task is None:
        print(f"✗ 找不到任务: {args.id}", file=sys.stderr)
        return 1

    if args.status:
        task["status"] = args.status
    if args.title:
        task["title"] = args.title

    task["updated_at"] = datetime.now().isoformat()
    await storage.save(tasks)
    print(f"✓ 任务已更新: {task.get('title', '')}")
    return 0


async def handle_delete(storage: TaskStorage, args: argparse.Namespace) -> int:
    """处理 delete 命令"""
    tasks = await storage.load()
    original_len = len(tasks)
    tasks = [t for t in tasks if t.get("id") != args.id]

    if len(tasks) == original_len:
        print(f"✗ 找不到任务: {args.id}", file=sys.stderr)
        return 1

    await storage.save(tasks)
    print("✓ 任务已删除")
    return 0


async def handle_export(storage: TaskStorage, args: argparse.Namespace) -> int:
    """处理 export 命令"""
    tasks = await storage.load()

    if args.format == "json":
        output = json.dumps(tasks, indent=2, default=str)
    else:
        # CSV 格式
        output_buffer = io.StringIO()
        if tasks:
            writer = csv.DictWriter(output_buffer, fieldnames=tasks[0].keys())
            writer.writeheader()
            for task in tasks:
                writer.writerow(task)
        output = output_buffer.getvalue()

    if args.output:
        args.output.write_text(output)
        print(f"✓ 已导出到: {args.output}")
    else:
        print(output)

    return 0


async def main() -> int:
    """主入口"""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    storage = TaskStorage(args.storage)

    handlers = {
        "add": handle_add,
        "list": handle_list,
        "update": handle_update,
        "delete": handle_delete,
        "export": handle_export,
    }

    handler = handlers.get(args.command)
    if handler:
        return await handler(storage, args)

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
