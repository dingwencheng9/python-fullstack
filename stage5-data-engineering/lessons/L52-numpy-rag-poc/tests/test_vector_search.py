"""
L51 NumPy RAG PoC - 向量检索测试
"""

from __future__ import annotations

import numpy as np
import pytest


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算两个向量的余弦相似度"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def batch_cosine_similarity(query: np.ndarray, docs: np.ndarray) -> np.ndarray:
    """批量计算余弦相似度（向量化）"""
    query_norm = query / np.linalg.norm(query)
    doc_norms = docs / np.linalg.norm(docs, axis=1, keepdims=True)
    return np.dot(doc_norms, query_norm)


class TestCosineSimilarity:
    """测试余弦相似度计算"""

    def test_identical_vectors(self):
        """相同向量相似度为1"""
        vec = np.array([1.0, 0.0, 0.0])
        assert cosine_similarity(vec, vec) == pytest.approx(1.0)

    def test_perpendicular_vectors(self):
        """垂直向量相似度为0"""
        vec_a = np.array([1.0, 0.0])
        vec_b = np.array([0.0, 1.0])
        assert cosine_similarity(vec_a, vec_b) == pytest.approx(0.0)

    def test_opposite_vectors(self):
        """相反向量相似度为-1"""
        vec_a = np.array([1.0, 0.0])
        vec_b = np.array([-1.0, 0.0])
        assert cosine_similarity(vec_a, vec_b) == pytest.approx(-1.0)

    def test_zero_vector(self):
        """零向量相似度为0"""
        vec = np.array([1.0, 0.0])
        zero = np.array([0.0, 0.0])
        assert cosine_similarity(vec, zero) == 0.0


class TestBatchCosineSimilarity:
    """测试批量余弦相似度"""

    def test_batch_similarity(self):
        """批量计算相似度"""
        query = np.array([1.0, 0.0, 0.0])
        docs = np.array(
            [
                [1.0, 0.0, 0.0],  # 相似度 = 1
                [0.0, 1.0, 0.0],  # 相似度 = 0
                [-1.0, 0.0, 0.0],  # 相似度 = -1
            ]
        )

        similarities = batch_cosine_similarity(query, docs)

        assert similarities[0] == pytest.approx(1.0)
        assert similarities[1] == pytest.approx(0.0)
        assert similarities[2] == pytest.approx(-1.0)

    def test_top_k_selection(self):
        """Top-K 选择"""
        query = np.array([1.0, 0.0, 0.0])
        docs = np.array(
            [
                [0.5, 0.5, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        )

        similarities = batch_cosine_similarity(query, docs)
        top_indices = np.argsort(similarities)[::-1][:2]

        assert top_indices[0] == 1  # 最相似
        assert set(top_indices) == {0, 1}  # Top-2
