"""L25 工程化综合项目 - 课程自检脚本。

从仓库根目录运行：
    uv run python stage2-engineering/lessons/L25-engineering-project/verify.py

或从本课目录运行：
    uv run python verify.py
"""

from __future__ import annotations

import asyncio
import importlib.util
import py_compile
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType

LESSON_ROOT = Path(__file__).resolve().parent
REPO_ROOT = LESSON_ROOT.parents[2]


def load_module(name: str, path: Path) -> ModuleType:
    """按文件路径加载模块，并在执行期注册到 sys.modules。"""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {path} 创建模块 spec")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        # 加载失败时清理已注册的模块
        del sys.modules[name]
        raise
    return module


def check_structure() -> None:
    required = [
        "README.md",
        "lesson.md",
        "pyproject.toml",
        "verify.py",
        "examples/01_task_model.py",
        "examples/02_task_storage.py",
        "examples/03_decorators.py",
        "examples/04_cli_interface.py",
        "examples/README.md",
        "exercises/exercise_01_task_model.py",
        "exercises/README.md",
        "solutions/__init__.py",
        "solutions/solution_01_task_model.py",
        "solutions/README.md",
        "tests/conftest.py",
        "tests/test_models.py",
        "tests/test_storage.py",
        "tests/test_decorators.py",
        "tests/test_cli.py",
        "tests/README.md",
    ]
    missing = [item for item in required if not (LESSON_ROOT / item).exists()]
    if missing:
        raise AssertionError(f"缺少必需文件: {missing}")
    print("✅ 目录与文件结构完整")


def check_compile() -> None:
    py_files = sorted(path for path in LESSON_ROOT.rglob("*.py") if ".ruff_cache" not in path.parts and "__pycache__" not in path.parts)
    for path in py_files:
        py_compile.compile(str(path), doraise=True)
    print(f"✅ Python 编译检查通过（{len(py_files)} 个文件）")


def check_task_model() -> None:
    module = load_module("l25_task_model_verify", LESSON_ROOT / "examples" / "01_task_model.py")

    due_date = datetime.now() + timedelta(days=2)
    task = module.Task(
        id="verify-1",
        title="Verify Task",
        description="self check",
        priority=module.Priority.HIGH,
        tags=["verify"],
        due_date=due_date,
    )
    assert task.is_overdue() is False
    assert task.days_until_due() in {1, 2}

    data = task.to_dict()
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert data["tags"] == ["verify"]

    restored = module.Task.from_dict(data)
    assert restored.id == task.id
    assert restored.title == task.title
    assert restored.priority == module.Priority.HIGH
    assert restored.tags == ["verify"]

    overdue = module.Task(id="verify-2", title="Overdue", due_date=datetime.now() - timedelta(days=1))
    assert overdue.is_overdue() is True
    assert overdue.days_until_due() is not None and overdue.days_until_due() < 0
    print("✅ Task 模型核心行为通过")


async def check_storage_and_cli() -> None:
    storage_module = load_module("l25_storage_verify", LESSON_ROOT / "examples" / "02_task_storage.py")
    cli_module = load_module("l25_cli_verify", LESSON_ROOT / "examples" / "04_cli_interface.py")

    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "nested" / "tasks.json"
        storage = storage_module.TaskStorage(storage_path)
        await storage.save([{"id": "1", "title": "Task 1"}])
        loaded = await storage.load()
        assert loaded == [{"id": "1", "title": "Task 1"}]

        cli_storage = cli_module.TaskStorage(Path(tmpdir) / "cli" / "tasks.json")
        parser = cli_module.create_parser()
        args = parser.parse_args(["add", "-t", "CLI Task", "-p", "high", "--tags", "verify"])
        assert await cli_module.handle_add(cli_storage, args) == 0
        tasks = await cli_storage.load()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "CLI Task"
        assert tasks[0]["priority"] == "high"
        assert tasks[0]["tags"] == ["verify"]

    print("✅ 异步存储与 CLI 核心行为通过")


def check_decorators() -> None:
    module = load_module("l25_decorators_verify", LESSON_ROOT / "examples" / "03_decorators.py")

    first = module.expensive_computation("verify")
    second = module.expensive_computation("verify")
    assert first == second == {"task_id": "verify", "result": "computed"}

    attempts = 0

    @module.retry(max_attempts=3, delay=0.01)
    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("temporary")
        return "ok"

    assert flaky() == "ok"
    assert attempts == 2
    print("✅ 装饰器示例核心行为通过")


def check_representative_scripts() -> None:
    scripts = [
        [sys.executable, str(LESSON_ROOT / "examples" / "01_task_model.py")],
        [sys.executable, str(LESSON_ROOT / "examples" / "02_task_storage.py")],
        [sys.executable, str(LESSON_ROOT / "examples" / "03_decorators.py")],
        [sys.executable, str(LESSON_ROOT / "examples" / "04_cli_interface.py"), "--help"],
        [sys.executable, str(LESSON_ROOT / "solutions" / "solution_01_task_model.py")],
    ]
    for command in scripts:
        result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise AssertionError("脚本运行失败: " + " ".join(command) + f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    print("✅ 代表性脚本入口运行通过")


def check_stale_references() -> None:
    text_files = [
        *(LESSON_ROOT.glob("*.md")),
        *(LESSON_ROOT.glob("*.py")),
        *(LESSON_ROOT / "examples").glob("*.md"),
        *(LESSON_ROOT / "examples").glob("*.py"),
        *(LESSON_ROOT / "exercises").glob("*.md"),
        *(LESSON_ROOT / "exercises").glob("*.py"),
        *(LESSON_ROOT / "solutions").glob("*.md"),
        *(LESSON_ROOT / "solutions").glob("*.py"),
        *(LESSON_ROOT / "tests").glob("*.md"),
        *(LESSON_ROOT / "tests").glob("*.py"),
    ]
    stale_tokens = [
        "stage2" + "-foundation",
        "task" + "_tracker" + ".py",
        "exercises/" + "01_task_model.py",
        "solutions/" + "01_task_model.py",
        "exercises/" + "task" + "_tracker" + ".py",
        "solutions/" + "task" + "_tracker" + ".py",
        "L" + "30" + ": HTTP",
        "stage3" + "-web-apis",
    ]
    hits: list[str] = []
    for path in text_files:
        content = path.read_text(encoding="utf-8")
        if path.name == "verify.py":
            continue
        for token in stale_tokens:
            if token in content:
                hits.append(f"{path.relative_to(LESSON_ROOT)}: {token}")
    if hits:
        raise AssertionError("发现旧编号/旧路径残留:\n" + "\n".join(hits))
    print("✅ 旧编号与路径元数据检查通过")


async def main() -> None:
    print("🔍 L25 工程化综合项目 - 课程自检")
    check_structure()
    check_compile()
    check_task_model()
    await check_storage_and_cli()
    check_decorators()
    check_representative_scripts()
    check_stale_references()
    print("🎉 L25 自检全部通过")


if __name__ == "__main__":
    asyncio.run(main())
