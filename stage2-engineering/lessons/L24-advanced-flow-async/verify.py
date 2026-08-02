#!/usr/bin/env python3
"""L22: 高阶流控与异步协同 - 课程验证脚本。

验证课程目录结构、Python 版本、源码语法、关键模块导入与核心异步行为。
依赖网络/数据库的综合爬虫只做导入和离线 mock 级抽检，完整生产环境验证由
测试套件和学习者本地环境完成。
"""

from __future__ import annotations

import asyncio
import importlib.util
import py_compile
import sys
import tempfile
import traceback
from pathlib import Path
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock

COURSE_ID = "L22"
COURSE_NAME = "高阶流控与异步协同"
LESSON_ROOT = Path(__file__).resolve().parent
MIN_PYTHON_VERSION = (3, 13)

REQUIRED_DIRS = [
    "examples",
    "exercises",
    "solutions",
    "tests",
]

REQUIRED_FILES = [
    "README.md",
    "lesson.md",
    "pyproject.toml",
    "verify.py",
    "examples/example_01_async_generators.py",
    "examples/example_02_context_managers.py",
    "examples/example_03_taskgroup_exceptions.py",
    "examples/example_04_pep695_generics.py",
    "examples/crawler_pipeline.py",
    "exercises/exercise_01_async_flow_patterns.py",
    "exercises/exercise_02_advanced_async_patterns.py",
    "solutions/solution_00_exercise.py",
    "solutions/solution_01_async_contextvar.py",
    "solutions/solution_02_semaphore.py",
    "solutions/solution_03_crawler_pipeline.py",
    "tests/conftest.py",
    "tests/test_examples.py",
    "tests/test_solutions.py",
    "tests/test_crawler.py",
]

IMPORT_TARGETS = [
    "examples/example_01_async_generators.py",
    "examples/example_02_context_managers.py",
    "examples/example_03_taskgroup_exceptions.py",
    "examples/example_04_pep695_generics.py",
    "examples/crawler_pipeline.py",
    "exercises/exercise_01_async_flow_patterns.py",
    "exercises/exercise_02_advanced_async_patterns.py",
    "solutions/solution_00_exercise.py",
    "solutions/solution_01_async_contextvar.py",
    "solutions/solution_02_semaphore.py",
    "solutions/solution_03_crawler_pipeline.py",
]


def print_header(title: str) -> None:
    """打印分节标题。"""
    print(f"\n{title}")
    print("-" * 70)


def check_python_version() -> bool:
    """检查 Python 版本。"""
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if version >= MIN_PYTHON_VERSION:
        print(f"  ✅ Python 版本: {version_text}")
        return True
    print(f"  ❌ Python 版本: {version_text}")
    print(f"     本课基线需要 Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+")
    return False


def check_structure() -> bool:
    """检查目录与关键文件是否存在。"""
    ok = True
    for rel_dir in REQUIRED_DIRS:
        path = LESSON_ROOT / rel_dir
        if path.is_dir():
            print(f"  ✅ 目录存在: {rel_dir}/")
        else:
            print(f"  ❌ 目录缺失: {rel_dir}/")
            ok = False

    for rel_file in REQUIRED_FILES:
        path = LESSON_ROOT / rel_file
        if path.is_file():
            print(f"  ✅ 文件存在: {rel_file}")
        else:
            print(f"  ❌ 文件缺失: {rel_file}")
            ok = False
    return ok


def iter_python_files() -> list[Path]:
    """列出本课需要语法检查的 Python 文件。"""
    excluded_parts = {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
    return sorted(path for path in LESSON_ROOT.rglob("*.py") if not excluded_parts.intersection(path.parts))


def check_compile() -> bool:
    """检查所有 Python 文件可编译。"""
    ok = True
    for path in iter_python_files():
        rel = path.relative_to(LESSON_ROOT)
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"  ✅ 语法通过: {rel}")
        except py_compile.PyCompileError as exc:
            print(f"  ❌ 语法失败: {rel}")
            print(f"     {exc.msg}")
            ok = False
    return ok


def load_module(rel_path: str) -> ModuleType:
    """按物理路径加载模块，避免依赖当前工作目录。"""
    file_path = LESSON_ROOT / rel_path
    module_name = "_l22_verify_" + rel_path.replace("/", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {rel_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        # 加载失败时清理已注册的模块（避免 CI 门禁熔断）
        del sys.modules[module_name]
        raise
    return module


def check_imports() -> bool:
    """检查关键示例、练习与参考答案可导入。"""
    ok = True
    for rel_path in IMPORT_TARGETS:
        try:
            load_module(rel_path)
            print(f"  ✅ 可导入: {rel_path}")
        except ModuleNotFoundError as exc:
            print(f"  ⚠️  跳过导入: {rel_path}（缺少依赖: {exc.name}）")
        except Exception as exc:  # pragma: no cover - verify 输出诊断信息
            print(f"  ❌ 导入失败: {rel_path}")
            print(f"     {type(exc).__name__}: {exc}")
            traceback.print_exc(limit=1)
            ok = False
    return ok


async def _check_async_behavior() -> bool:
    """异步核心行为抽检。"""
    ok = True

    try:
        generators = load_module("examples/example_01_async_generators.py")
        assert list(generators.sync_range(3)) == [0, 1, 2]
        async_values = [value async for value in generators.async_range(3)]
        assert async_values == [0, 1, 2]
        transformed = [item async for item in generators.transform_stream(generators.data_source())]
        assert transformed[:2] == ["Item-000", "Item-001"]
        assert len(transformed) == 10
        print("  ✅ 异步生成器与流式转换行为正常")
    except Exception as exc:
        print(f"  ❌ 异步生成器行为验证失败: {exc}")
        ok = False

    try:
        solution_01 = load_module("solutions/solution_01_async_contextvar.py")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            tmp.write("Alpha\nBeta\n")
            tmp_path = Path(tmp.name)
        try:
            lines = [line async for line in solution_01.read_lines_async(str(tmp_path))]
        finally:
            tmp_path.unlink(missing_ok=True)
        assert lines == ["Alpha", "Beta"]
        print("  ✅ 异步文件流参考答案行为正常")
    except ModuleNotFoundError as exc:
        print(f"  ⚠️  跳过异步文件流抽检（缺少依赖: {exc.name}）")
    except Exception as exc:
        print(f"  ❌ 异步文件流行为验证失败: {exc}")
        ok = False

    try:
        semaphore_solution = load_module("solutions/solution_02_semaphore.py")
        pool = semaphore_solution.ConnectionPool(size=1)
        await pool.initialize()
        async with semaphore_solution.get_connection(pool) as conn:
            assert conn.in_use is True
            result = await conn.execute("SELECT 1")
            assert result[0]["id"] == 1
        assert pool.connections[0].in_use is False
        assert semaphore_solution.create_pool([1, 2, 3]) == [1, 2, 3]
        await pool.close()
        print("  ✅ 异步连接池与 PEP 695 泛型参考答案行为正常")
    except Exception as exc:
        print(f"  ❌ 异步连接池行为验证失败: {exc}")
        ok = False

    try:
        crawler = load_module("solutions/solution_03_crawler_pipeline.py")
        config = crawler.CrawlerConfig(retry_attempts=1, backoff_factor=0.01)
        semaphore = asyncio.Semaphore(1)
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="<html><head><title>Verify</title></head></html>")
        mock_session = AsyncMock()
        mock_session.get = MagicMock()
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
        result = await crawler.crawl_page("https://example.com", mock_session, semaphore, config)
        assert result["title"] == "Verify"
        assert result["status"] == 200
        print("  ✅ 爬虫管道核心 crawl_page 行为正常")
    except ModuleNotFoundError as exc:
        print(f"  ⚠️  跳过爬虫管道抽检（缺少依赖: {exc.name}）")
    except Exception as exc:
        print(f"  ❌ 爬虫管道行为验证失败: {exc}")
        ok = False

    return ok


def check_core_behavior() -> bool:
    """运行异步核心行为抽检。"""
    return asyncio.run(_check_async_behavior())


def main() -> int:
    """执行课程验证。"""
    print("=" * 70)
    print(f"{COURSE_ID}: {COURSE_NAME} - 课程验证")
    print("=" * 70)
    print(f"课程目录: {LESSON_ROOT}")

    checks = [
        ("测试 1: Python 环境", check_python_version),
        ("测试 2: 文件结构", check_structure),
        ("测试 3: Python 语法", check_compile),
        ("测试 4: 关键模块导入", check_imports),
        ("测试 5: 核心异步行为抽检", check_core_behavior),
    ]

    results: list[tuple[str, bool]] = []
    for title, check in checks:
        print_header(title)
        results.append((title, check()))

    print("\n" + "=" * 70)
    print("验证结果汇总")
    print("=" * 70)
    for title, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{title:<24}: {status}")

    if all(passed for _, passed in results):
        print("\n🎉 L22 课程验证通过！")
        print("\n建议继续执行:")
        print("1. uv run pytest stage2-engineering/lessons/L22-advanced-flow-async/tests -q")
        print("2. uv run python stage2-engineering/lessons/L22-advanced-flow-async/examples/example_01_async_generators.py")
        print("3. uv run python stage2-engineering/lessons/L22-advanced-flow-async/solutions/solution_02_semaphore.py")
        return 0

    print("\n❌ L22 课程验证失败，请根据上方诊断修复。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
