"""L24 线程并发测试。"""

from __future__ import annotations

import importlib.util
import sys
import threading
from pathlib import Path

import pytest


def load_solution(module_name: str, filename: str) -> object:
    """按文件路径加载参考答案，避免跨课程 solutions 包名冲突。"""
    module_path = Path(__file__).resolve().parents[1] / "solutions" / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        msg = f"无法加载模块: {module_path}"
        raise ImportError(msg)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


pc_module = load_solution("l24_producer_consumer", "solution_01_producer_consumer.py")
dl_module = load_solution("l24_parallel_download", "solution_02_parallel_download.py")


def test_producer_consumer_basic() -> None:
    pc = pc_module.ProducerConsumer(max_items=10)
    pc.produce(5)
    assert pc.consume_all() == [0, 1, 2, 3, 4]


def test_producer_consumer_thread_safe() -> None:
    """多线程生产线程安全。"""
    pc = pc_module.ProducerConsumer(max_items=100)
    threads = [threading.Thread(target=pc.produce, args=(20,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(pc.consume_all()) == 100


@pytest.mark.parametrize(
    ("workers", "urls", "expected_count"),
    [
        (1, ["http://x", "http://y"], 2),
        (3, ["http://a", "http://b", "http://c"], 3),
        (5, [], 0),
    ],
)
def test_parallel_download_counts(
    workers: int,
    urls: list[str],
    expected_count: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """参数化：不同 worker 数与 URL 数。"""
    monkeypatch.setattr(dl_module, "fetch_url", lambda u: f"data:{u}")
    results = dl_module.parallel_download(urls, max_workers=workers)
    assert len(results) == expected_count


def test_parallel_download_handles_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """异常路径：单 URL 失败不影响其他。"""

    def fake_fetch(url: str) -> str:
        if url == "http://error":
            raise ValueError("fetch failed")
        return f"data:{url}"

    monkeypatch.setattr(dl_module, "fetch_url", fake_fetch)
    results = dl_module.parallel_download(
        ["http://ok", "http://error", "http://ok2"],
        max_workers=2,
    )
    assert len(results) == 2  # 失败被跳过


def test_producer_consumer_empty_consume() -> None:
    """边界：未生产时 consume_all 返回空。"""
    pc = pc_module.ProducerConsumer(max_items=10)
    assert pc.consume_all() == []
