"""

from __future__ import annotations

练习 2: 向量检索系统 - 标准答案

【解题思路】

1. 相似度计算向量化：
   - 余弦相似度：np.dot(doc_vecs, query_vec) / (norm(doc_vecs) * norm(query_vec))
   - 如果向量已归一化，直接np.dot即可
   - 避免for循环，使用矩阵乘法（快100倍）

2. Top-K检索算法：
   - 计算所有相似度（向量化）
   - 使用np.argsort获取排序索引
   - [::-1]反转为降序
   - [:top_k]取前K个

3. 过滤和重排序：
   - 分数阈值过滤：score >= threshold
   - 元数据过滤：自定义filter_func
   - 重排序：使用更精确的模型（交叉编码器）

4. 混合检索：
   - 向量检索：语义相似度
   - 关键词检索：词频匹配（简化BM25）
   - 分数融合：final = alpha * vec + (1-alpha) * keyword

【关键知识点】

- 余弦相似度计算公式
- NumPy向量化操作
- Top-K算法（argsort + 切片）
- 混合检索提升召回率
- 重排序提升精确度

【生产级考量】

- 使用FAISS/Qdrant等专业向量数据库
- 实现ANN（近似最近邻）加速大规模检索
- 添加过滤条件（时间范围、分类等）
- 实现分页
- 监控检索性能
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import numpy as np

# ============================================================================
# 1. 定义检索配置
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
# 2. 实现相似度计算（向量化）
# ============================================================================


class SimilarityCalculator:
    """相似度计算器（向量化实现）"""

    @staticmethod
    def cosine_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算余弦相似度（向量化）

        关键优化：
        - 假设向量已归一化（norm=1）
        - 此时 cosine = dot_product
        - 避免重复计算norm
        """
        # 计算点积（向量化）
        # 等价于：[np.dot(query_vec, doc_vec) for doc_vec in doc_vecs]
        # 但快100倍！
        similarities = np.dot(doc_vecs, query_vec)

        # 限制范围 [0, 1]
        return np.clip(similarities, 0.0, 1.0)

    @staticmethod
    def euclidean_distance(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算欧氏距离（向量化）

        公式：d = ||query_vec - doc_vec||
        """
        # 利用广播机制计算所有距离
        # query_vec: (d,) -> (1, d)
        # doc_vecs: (n, d)
        # diff: (n, d)
        diff = doc_vecs - query_vec

        # 计算L2范数（每行）
        distances = np.linalg.norm(diff, axis=1)

        return distances

    @staticmethod
    def dot_product(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算点积（向量化）"""
        return np.dot(doc_vecs, query_vec)


# ============================================================================
# 3. 实现Top-K检索
# ============================================================================


class TopKRetriever:
    """Top-K检索器"""

    def __init__(self, config: SearchConfig):
        self.config = config
        self.calculator = SimilarityCalculator()

    def search(self, query_vec: np.ndarray, doc_vecs: np.ndarray, doc_ids: list[str] | None = None) -> list[tuple[str, float]]:
        """执行Top-K检索"""
        # 1. 计算相似度
        scores = self._calculate_scores(query_vec, doc_vecs)

        # 2. 应用阈值过滤
        valid_indices = np.where(scores >= self.config.score_threshold)[0]

        if len(valid_indices) == 0:
            return []

        # 3. 获取Top-K（在有效结果中）
        valid_scores = scores[valid_indices]
        top_k = min(self.config.top_k, len(valid_indices))

        # argsort返回从小到大的索引，[::-1]反转为从大到小
        top_indices_in_valid = np.argsort(valid_scores)[::-1][:top_k]

        # 映射回原始索引
        top_indices = valid_indices[top_indices_in_valid]

        # 4. 构建结果
        if doc_ids is None:
            doc_ids = [f"doc_{i}" for i in range(len(doc_vecs))]

        results = [(doc_ids[idx], float(scores[idx])) for idx in top_indices]

        return results

    def _calculate_scores(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """计算相似度分数"""
        if self.config.metric == SimilarityMetric.COSINE:
            return self.calculator.cosine_similarity(query_vec, doc_vecs)
        if self.config.metric == SimilarityMetric.EUCLIDEAN:
            # 欧氏距离转相似度：1 / (1 + distance)
            distances = self.calculator.euclidean_distance(query_vec, doc_vecs)
            return 1.0 / (1.0 + distances)
        if self.config.metric == SimilarityMetric.DOT_PRODUCT:
            return self.calculator.dot_product(query_vec, doc_vecs)
        raise ValueError(f"不支持的度量: {self.config.metric}")


# ============================================================================
# 4. 实现过滤和重排序
# ============================================================================


class SearchFilter:
    """检索过滤器"""

    @staticmethod
    def filter_by_metadata(
        results: list[tuple[str, float]],
        metadata: dict[str, Any],
        filter_func: Callable[[Any], bool],
    ) -> list[tuple[str, float]]:
        """根据元数据过滤结果"""
        filtered = []
        for doc_id, score in results:
            if doc_id in metadata:
                if filter_func(metadata[doc_id]):
                    filtered.append((doc_id, score))
        return filtered

    @staticmethod
    def filter_by_score(results: list[tuple[str, float]], min_score: float) -> list[tuple[str, float]]:
        """根据分数过滤"""
        return [(doc_id, score) for doc_id, score in results if score >= min_score]


class Reranker:
    """重排序器"""

    def rerank(self, results: list[tuple[str, float]], query: str, documents: dict[str, str]) -> list[tuple[str, float]]:
        """重排序检索结果

        策略：
        - 初排：向量检索（快但粗糙）
        - 精排：交叉编码器（慢但精确）

        这里简化：基于文本长度匹配度
        """
        reranked = []

        for doc_id, vec_score in results:
            if doc_id not in documents:
                reranked.append((doc_id, vec_score))
                continue

            doc_text = documents[doc_id]

            # 简化的重排序分数：结合向量分数和文本特征
            # 真实场景使用交叉编码器模型
            text_score = self._calculate_text_score(query, doc_text)

            # 融合分数（70%向量 + 30%文本）
            final_score = 0.7 * vec_score + 0.3 * text_score

            reranked.append((doc_id, final_score))

        # 重新排序
        reranked.sort(key=lambda x: x[1], reverse=True)

        return reranked

    def _calculate_text_score(self, query: str, doc: str) -> float:
        """计算文本匹配分数（简化版）"""
        query_words = set(query.lower().split())
        doc_words = set(doc.lower().split())

        if not query_words:
            return 0.0

        # Jaccard相似度
        intersection = query_words & doc_words
        union = query_words | doc_words

        return len(intersection) / len(union) if union else 0.0


# ============================================================================
# 5. 实现混合检索
# ============================================================================


class HybridRetriever:
    """混合检索器（向量 + 关键词）"""

    def __init__(self, config: SearchConfig):
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
        """混合检索（向量 + 关键词）"""
        doc_ids = list(documents.keys())

        # 1. 向量检索
        vector_results = self.vector_retriever.search(query_vec, doc_vecs, doc_ids)

        # 2. 关键词检索
        keyword_results = self._keyword_search(query_text, documents, self.config.top_k)

        # 3. 融合分数
        merged_results = self._merge_scores(vector_results, keyword_results, alpha)

        return merged_results

    def _keyword_search(self, query_text: str, documents: dict[str, str], top_k: int) -> list[tuple[str, float]]:
        """关键词检索（简化版BM25）"""
        query_words = set(query_text.lower().split())
        scores = []

        for doc_id, doc_text in documents.items():
            doc_words = doc_text.lower().split()

            # 计算词频匹配分数
            match_count = sum(1 for word in doc_words if word in query_words)
            score = match_count / len(doc_words) if doc_words else 0.0

            scores.append((doc_id, score))

        # 排序并返回Top-K
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def _merge_scores(
        self,
        vector_results: list[tuple[str, float]],
        keyword_results: list[tuple[str, float]],
        alpha: float,
    ) -> list[tuple[str, float]]:
        """融合向量和关键词检索分数"""
        # 构建分数字典
        vec_scores = dict(vector_results)
        kw_scores = dict(keyword_results)

        # 合并所有文档ID
        all_doc_ids = set(vec_scores.keys()) | set(kw_scores.keys())

        # 计算融合分数
        merged = []
        for doc_id in all_doc_ids:
            vec_score = vec_scores.get(doc_id, 0.0)
            kw_score = kw_scores.get(doc_id, 0.0)

            # 加权融合
            final_score = alpha * vec_score + (1 - alpha) * kw_score

            merged.append((doc_id, final_score))

        # 排序
        merged.sort(key=lambda x: x[1], reverse=True)

        return merged[: self.config.top_k]


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2: 向量检索系统 - 标准答案")
    print("=" * 70)

    # 准备测试数据
    np.random.seed(42)

    # 模拟文档向量（5个文档，128维）
    doc_vecs = np.random.randn(5, 128)
    doc_vecs = doc_vecs / np.linalg.norm(doc_vecs, axis=1, keepdims=True)  # 归一化

    # 模拟查询向量
    query_vec = np.random.randn(128)
    query_vec = query_vec / np.linalg.norm(query_vec)  # 归一化

    # 文档内容
    documents = {
        "doc_0": "Python是一种高级编程语言",
        "doc_1": "机器学习需要大量的数据",
        "doc_2": "深度学习是机器学习的一个分支",
        "doc_3": "自然语言处理用于理解人类语言",
        "doc_4": "向量检索是RAG系统的核心",
    }

    # 测试1: Top-K检索
    print("\n测试1: Top-K检索")
    config = SearchConfig(top_k=3, score_threshold=0.0)
    retriever = TopKRetriever(config)

    results = retriever.search(query_vec, doc_vecs, list(documents.keys()))

    print("Top-3结果：")
    for i, (doc_id, score) in enumerate(results, 1):
        print(f"  {i}. {doc_id}: {score:.4f} - {documents[doc_id]}")

    # 测试2: 混合检索
    print("\n测试2: 混合检索")
    hybrid = HybridRetriever(config)

    hybrid_results = hybrid.hybrid_search(
        query_text="机器学习和深度学习",
        query_vec=query_vec,
        doc_vecs=doc_vecs,
        documents=documents,
        alpha=0.7,
    )

    print("混合检索Top-3结果：")
    for i, (doc_id, score) in enumerate(hybrid_results, 1):
        print(f"  {i}. {doc_id}: {score:.4f} - {documents[doc_id]}")

    print("\n✅ 测试完成！")
