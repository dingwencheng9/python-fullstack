#!/usr/bin/env python3
"""L24 课程自检脚本：结构、编译与关键线程行为验证。"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
import threading
from pathlib import Path
from types import ModuleType
from typing import Any

LESSON_ROOT = Path(__file__).resolve().parent

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
    "examples/01_threading_basics.py",
    "examples/02_lock_synchronization.py",
    "examples/02_multiprocessing_basics.py",
    "examples/03_threadpool.py",
    "exercises/exercise_01_producer_consumer.py",
    "exercises/exercise_02_parallel_download.py",
    "exercises/exercise_03_threading_example.py",
    "solutions/__init__.py",
    "solutions/solution_01_producer_consumer.py",
    "solutions/solution_02_parallel_download.py",
    "solutions/solution_03_threading_example.py",
    "tests/conftest.py",
    "tests/test_threading.py",
]


def _ok(message: str) -> None:
    print(f"✅ {message}")


def _fail(message: str) -> None:
    raise AssertionError(message)


def check_structure() -> None:
    """检查课程必需目录与文件。"""
    for directory in REQUIRED_DIRS:
        path = LESSON_ROOT / directory
        if not path.is_dir():
            _fail(f"缺少目录: {path.relative_to(LESSON_ROOT)}")

    for file_name in REQUIRED_FILES:
        path = LESSON_ROOT / file_name
        if not path.is_file():
            _fail(f"缺少文件: {file_name}")

    _ok("目录与文件结构完整")


def iter_python_files() -> list[Path]:
    """返回本课需要编译检查的 Python 文件。"""
    files = [LESSON_ROOT / "verify.py"]
    for directory in ("examples", "exercises", "solutions", "tests"):
        files.extend(sorted((LESSON_ROOT / directory).glob("*.py")))
    return files


def check_compile() -> None:
    """编译所有课程 Python 文件。"""
    files = iter_python_files()
    for path in files:
        py_compile.compile(str(path), doraise=True)
    _ok(f"Python 编译检查通过（{len(files)} 个文件）")


def load_module(relative_path: str, module_name: str) -> ModuleType:
    """按物理路径加载模块，并在执行前注册到 sys.modules。"""
    path = LESSON_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {relative_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def check_producer_consumer() -> None:
    """验证生产者消费者参考答案的线程安全核心行为。"""
    module = load_module("solutions/solution_01_producer_consumer.py", "_l24_solution_01_producer_consumer")

    pc = module.ProducerConsumer(max_items=10)
    pc.produce(4)
    assert pc.consume_all() == [0, 1, 2, 3]
    assert pc.consume_all() == []

    pc.reset()
    threads = [threading.Thread(target=pc.produce, args=(5,)) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=2)
        assert not thread.is_alive()

    items = pc.consume_all()
    assert len(items) == 10
    assert items == list(range(10))

    _ok("ProducerConsumer 线程安全核心行为通过")


def check_parallel_download() -> None:
    """验证线程池下载器的成功、失败与边界行为。"""
    module = load_module("solutions/solution_02_parallel_download.py", "_l24_solution_02_parallel_download")

    def fake_fetch(url: str) -> str:
        if url.endswith("bad"):
            raise ValueError("boom")
        return f"data:{url}"

    original_fetch = module.fetch_url
    original_logger_disabled = module.logger.disabled
    module.fetch_url = fake_fetch
    module.logger.disabled = True
    try:
        results = module.parallel_download(["http://a", "http://bad", "http://c"], max_workers=2)
        assert results == {"http://a": "data:http://a", "http://c": "data:http://c"}
        assert module.parallel_download([], max_workers=2) == {}
        try:
            module.parallel_download(["http://a"], max_workers=0)
        except ValueError:
            pass
        else:
            _fail("max_workers=0 应抛出 ValueError")
    finally:
        module.fetch_url = original_fetch
        module.logger.disabled = original_logger_disabled

    _ok("parallel_download 成功/失败/边界行为通过")


def check_examples_lightweight() -> None:
    """验证示例模块的轻量对象行为，避免运行重/易抖动演示。"""
    lock_module = load_module("examples/02_lock_synchronization.py", "_l24_example_lock_synchronization")
    counter = lock_module.SafeCounter()
    threads = [threading.Thread(target=counter.increment) for _ in range(20)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=2)
        assert not thread.is_alive()
    assert counter.value == 20

    pool_module = load_module("examples/03_threadpool.py", "_l24_example_threadpool")
    assert pool_module.fetch_resource("http://ok") == "content:http://ok"
    try:
        pool_module.fetch_resource("http://bad")
    except ValueError:
        pass
    else:
        _fail("bad URL 应抛出 ValueError")

    _ok("线程同步与线程池示例轻量行为通过")


def check_text_metadata() -> None:
    """检查明显旧路径/旧编号残留。"""
    targets = [LESSON_ROOT / "README.md", LESSON_ROOT / "lesson.md"]
    for directory in ("examples", "exercises", "solutions", "tests"):
        targets.extend(sorted((LESSON_ROOT / directory).glob("*.py")))

    bad_tokens = (
        "stage2-" + "foundation",
        "L" + "30-threading",
        "L" + "29 线程",
        "l" + "28_",
        "L" + "28-extreme",
        "bench" + "marks/01_free_threading_benchmark.py",
        "exercises/" + "01_",
        "exercises/" + "02_",
        "solutions/" + "01_",
        "solutions/" + "02_",
    )
    offenders: list[str] = []
    for path in targets:
        text = path.read_text()
        for token in bad_tokens:
            if token in text:
                offenders.append(f"{path.relative_to(LESSON_ROOT)}: {token}")

    if offenders:
        _fail("发现旧编号/旧路径残留: " + "; ".join(offenders))

    _ok("旧编号与路径元数据检查通过")


def main() -> int:
    print("🔍 L24 线程与并发 - 课程自检")
    print(f"课程目录: {LESSON_ROOT}")
    print()

    checks: list[tuple[str, Any]] = [
        ("结构检查", check_structure),
        ("编译检查", check_compile),
        ("生产者消费者行为检查", check_producer_consumer),
        ("并发下载器行为检查", check_parallel_download),
        ("示例轻量行为检查", check_examples_lightweight),
        ("文本元数据检查", check_text_metadata),
    ]

    for title, check in checks:
        print()
        print(f"▶ {title}")
        check()

    print()
    print("🎉 L24 自检全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
