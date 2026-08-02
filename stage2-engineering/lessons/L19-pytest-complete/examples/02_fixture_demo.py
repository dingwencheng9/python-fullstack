"""L17 示例 2: fixture 使用"""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_data():
    """提供测试数据。"""
    return {"name": "Alice", "age": 30, "scores": [85, 90, 78]}


def test_average(sample_data):
    scores = sample_data["scores"]
    assert sum(scores) / len(scores) == pytest.approx(84.33, rel=1e-2)


@pytest.fixture(scope="module")
def module_data():
    """模块级别的 fixture，只创建一次。"""
    return {"counter": 0}


def test_first(module_data):
    module_data["counter"] += 1
    assert module_data["counter"] == 1


def test_second(module_data):
    module_data["counter"] += 1
    assert module_data["counter"] == 2
