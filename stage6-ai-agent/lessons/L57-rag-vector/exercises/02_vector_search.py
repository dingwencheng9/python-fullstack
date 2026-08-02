"""

from __future__ import annotations

练习 2: 向量检索系统

任务：
实现高效的向量相似度检索系统，支持Top-K检索和混合检索。

学习目标：
- 实现余弦相似度计算（向量化）
- 实现Top-K检索算法
- 支持过滤和重排序
- 优化检索性能

预计时间: 60 分钟
难度: ⭐⭐⭐⭐⭐
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import numpy as np

# ============================================================================
# TODO 1: 定义检索配置
# ============================================================================


class SimilarityMetric(StrEnum):
    """相似度度量"""

    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"


@dataclass
class SearchConfig:
    """检索配置"""

    metric: SimilarityMetric = SimilarityMetric.COSINE
    top_k: int = 10
    score_threshold: float = 0.0
    use_reranking: bool = False


# ============================================================================
# TODO 2: 实现相似度计算（向量化）
# ============================================================================


class SimilarityCalculator:
    """相似度计算器（向量化实现）"""

    @staticmethod
    def cosine_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算余弦相似度（向量化）

        使用向量化操作，避免循环，性能提升100倍。

        公式: cos(θ) = (A·B) / (||A|| * ||B||)

        Args:
            query_vec: 查询向量 (d,)
            doc_vecs: 文档向量矩阵 (n, d)

        Returns:
            相似度数组 (n,)

        Example:
            >>> query = np.array([1, 0, 0])
            >>> docs = np.array([[1, 0, 0], [0, 1, 0]])
            >>> sim = SimilarityCalculator.cosine_similarity(query, docs)
            >>> print(sim)  # [1.0, 0.0]
        """
        # TODO: 实现向量化余弦相似度
        # 提示:
        # 1. 使用 np.dot 计算点积
        # 2. 使用 np.linalg.norm 计算模长
        # 3. 避免使用 for 循环

    @staticmethod
    def euclidean_distance(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算欧氏距离（向量化）

        Args:
            query_vec: 查询向量 (d,)
            doc_vecs: 文档向量矩阵 (n, d)

        Returns:
            距离数组 (n,)
        """
        # TODO: 实现向量化欧氏距离
        # 提示: 使用 np.linalg.norm 和广播

    @staticmethod
    def dot_product(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算点积（向量化）

        Args:
            query_vec: 查询向量 (d,)
            doc_vecs: 文档向量矩阵 (n, d)

        Returns:
            点积数组 (n,)
        """
        # TODO: 实现向量化点积
        # 提示: 使用 np.dot


# ============================================================================
# TODO 3: 实现Top-K检索
# ============================================================================


class TopKRetriever:
    """Top-K检索器"""

    def __init__(self, config: SearchConfig):
        # TODO: 初始化
        self.config = config
        self.calculator = SimilarityCalculator()

    def search(self, query_vec: np.ndarray, doc_vecs: np.ndarray, doc_ids: list[str] | None = None) -> list[tuple[str, float]]:
        """执行Top-K检索

        Args:
            query_vec: 查询向量
            doc_vecs: 文档向量矩阵
            doc_ids: 文档ID列表

        Returns:
            (doc_id, score) 列表，按分数降序排列
        """
        # TODO: 实现Top-K检索
        # 1. 计算相似度
        # 2. 应用阈值过滤
        # 3. 获取Top-K
        # 4. 返回结果

    def _calculate_scores(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算相似度分数"""
        # TODO: 根据配置选择相似度度量


# ============================================================================
# TODO 4: 实现过滤和重排序
# ============================================================================


class SearchFilter:
    """检索过滤器"""

    @staticmethod
    def filter_by_metadata(results: list[tuple[str, float]], metadata: dict[str, Any], filter_func: Callable) -> list[tuple[str, float]]:
        """根据元数据过滤结果

        Args:
            results: 原始检索结果
            metadata: 文档元数据
            filter_func: 过滤函数

        Returns:
            过滤后的结果
        """
        # TODO: 实现元数据过滤

    @staticmethod
    def filter_by_score(results: list[tuple[str, float]], min_score: float) -> list[tuple[str, float]]:
        """根据分数过滤"""
        # TODO: 过滤低分结果


class Reranker:
    """重排序器"""

    def rerank(self, results: list[tuple[str, float]], query: str, documents: dict[str, str]) -> list[tuple[str, float]]:
        """重排序检索结果

        使用更精确的相似度计算重新排序

        Args:
            results: 初始检索结果
            query: 查询文本
            documents: 文档内容字典

        Returns:
            重排序后的结果
        """
        # TODO: 实现重排序逻辑


# ============================================================================
# TODO 5: 实现混合检索
# ============================================================================


class HybridRetriever:
    """混合检索器（向量 + 关键词）"""

    def __init__(self, config: SearchConfig):
        # TODO: 初始化
        self.config = config
        self.vector_retriever = TopKRetriever(config)

    def hybrid_search(
        self,
        query_text: str,
        query_vec: np.ndarray,
        doc_vecs: np.ndarray,
        documents: dict[str, str],
        alpha: float = 0.7,
    ) -> list[tuple[str, float]]:
        """混合检索（向量 + 关键词）

        Args:
            query_text: 查询文本
            query_vec: 查询向量
            doc_vecs: 文档向量矩阵
            documents: 文档内容字典
            alpha: 向量检索权重（0-1）

        Returns:
            融合后的检索结果
        """
        # TODO: 实现混合检索
        # 1. 向量检索
        # 2. 关键词检索（BM25简化版）
        # 3. 分数融合
        # 4. 重排序

    def _keyword_search(self, query_text: str, documents: dict[str, str], top_k: int) -> list[tuple[str, float]]:
        """关键词检索（简化版BM25）

        Args:
            query_text: 查询文本
            documents: 文档内容
            top_k: 返回数量

        Returns:
            检索结果
        """
        # TODO: 实现简化的关键词检索
        # 计算词频匹配分数

    def _merge_scores(
        self,
        vector_results: list[tuple[str, float]],
        keyword_results: list[tuple[str, float]],
        alpha: float,
    ) -> list[tuple[str, float]]:
        """融合向量和关键词检索分数

        Args:
            vector_results: 向量检索结果
            keyword_results: 关键词检索结果
            alpha: 向量权重

        Returns:
            融合后的结果
        """
        # TODO: 实现分数融合
        # final_score = alpha * vector_score + (1-alpha) * keyword_score


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2: 向量检索系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现相似度计算（向量化）")
    print("  2. 实现Top-K检索")
    print("  3. 实现过滤和重排序")
    print("  4. 实现混合检索")
    print("\n核心优化：")
    print("  - 向量化操作: 避免循环，提升100倍性能")
    print("  - Top-K算法: 使用堆或排序优化")
    print("  - 混合检索: 向量+关键词互补")
    print("\n提示：")
    print("  - 使用 np.dot 和 np.linalg.norm")
    print("  - 使用 np.argsort 获取Top-K")
    print("  - 余弦相似度范围 [-1, 1]")
    print()
