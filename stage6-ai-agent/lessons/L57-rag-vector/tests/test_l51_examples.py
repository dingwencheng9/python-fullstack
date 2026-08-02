"""L47 RAG 向量基础示例测试。"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

pytest.importorskip("numpy", reason="numpy 未安装")

import numpy as np

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def _load_vector_example() -> ModuleType:
    """动态加载向量嵌入基础示例模块。"""
    module_path = EXAMPLES_DIR / "01_vector_embedding_basics.py"
    spec = importlib.util.spec_from_file_location("l43_vector_embedding_basics", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


veb = _load_vector_example()


@pytest.mark.parametrize("dimension", [16, 64, 128])
def test_simple_text_vectorizer_returns_normalized_vectors(dimension: int) -> None:
    """参数化验证文本向量维度与归一化。"""
    vectorizer = veb.SimpleTextVectorizer(dimension=dimension)

    vector = vectorizer.encode("python rag vector")

    assert vector.shape == (dimension,)
    assert np.linalg.norm(vector) == pytest.approx(1.0)


def test_empty_query_returns_zero_vector_boundary() -> None:
    """空查询边界应返回零向量。"""
    vectorizer = veb.SimpleTextVectorizer(dimension=32)

    vector = vectorizer.encode("")

    np.testing.assert_array_equal(vector, np.zeros(32))


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (np.array([1.0, 0.0]), np.array([1.0, 0.0]), 1.0),
        (np.array([1.0, 0.0]), np.array([0.0, 1.0]), 0.0),
        (np.array([1.0, 0.0]), np.array([-1.0, 0.0]), 0.0),
    ],
)
def test_cosine_similarity_clips_vector_distance_cases(
    left: np.ndarray,
    right: np.ndarray,
    expected: float,
) -> None:
    """参数化验证相同、正交和反向向量距离场景。"""
    assert veb.cosine_similarity(left, right) == pytest.approx(expected)


def test_batch_cosine_similarity_rejects_dimension_mismatch() -> None:
    """批量相似度遇到维度不匹配时应抛出 ValueError。"""
    query = np.array([1.0, 0.0, 0.0])
    docs = np.array([[1.0, 0.0]])

    with pytest.raises(ValueError, match="shapes"):
        veb.batch_cosine_similarity(query, docs)


def test_semantic_search_returns_top_k_sorted_results() -> None:
    """Top-K 检索应按分数降序返回指定数量结果。"""
    search_engine = veb.SimpleSemanticSearch(dimension=32)
    documents = ["python rag", "vector database", "time series"]
    search_engine.index(documents)

    results = search_engine.search("python", top_k=2)

    assert len(results) == 2
    assert results[0][1] >= results[1][1]
    assert all(document in documents for document, _ in results)


def test_semantic_search_rejects_query_before_indexing() -> None:
    """未索引文档时查询应抛出明确异常。"""
    search_engine = veb.SimpleSemanticSearch(dimension=16)

    with pytest.raises(ValueError, match="请先调用 index"):
        search_engine.search("python", top_k=1)


def test_semantic_search_empty_index_boundary() -> None:
    """空文档库边界下 Top-K 检索返回空列表。"""
    search_engine = veb.SimpleSemanticSearch(dimension=16)
    search_engine.index([])

    results = search_engine.search("anything", top_k=3)

    assert results == []
