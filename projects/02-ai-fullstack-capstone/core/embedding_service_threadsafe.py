"""线程安全 Embedding 服务。

本模块提供：
1. BaseEmbedder 抽象基类
2. 线程安全的 Embedding 服务
3. 本地 stub 实现

真实实现请参考：
- stage6-ai-agent/lessons/L57-rag-vector/solutions/01_embedding_pipeline.py

使用说明：
1. 在生产环境中，使用 LangChain Embeddings
2. 参考 L57 课程学习完整的 embedding 管道
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import StrEnum

import numpy as np


class EmbeddingBackend(StrEnum):
    """Embedding 后端类型"""

    OPENAI = "openai"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    LOCAL = "local"


class BaseEmbedder(ABC):
    """Embedding 基础抽象类"""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """返回 embedding 向量的维度"""
        ...

    @abstractmethod
    async def embed_text(self, text: str) -> np.ndarray:
        """异步生成单个文本的 embedding 向量"""
        ...

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> np.ndarray:
        """异步批量生成文本的 embedding 向量"""
        ...

    def embed(self, text: str) -> np.ndarray:
        """同步生成单个文本的 embedding（stub 实现）"""
        raise NotImplementedError("子类应实现此方法或使用异步版本")

    def embed_batch_sync(self, texts: list[str]) -> np.ndarray:
        """同步批量生成 embedding（stub 实现）"""
        raise NotImplementedError("子类应实现此方法或使用异步版本")


class _LocalStubEmbedder(BaseEmbedder):
    """本地 stub 实现，返回基于文本的确定性归一化向量"""

    def __init__(self, dim: int = 384):
        self._dim = dim
        self._cache: dict[str, np.ndarray] = {}

    @property
    def dimension(self) -> int:
        return self._dim

    def _text_to_seed(self, text: str) -> int:
        """将文本转换为随机种子"""
        return sum(ord(c) for c in text)

    def embed(self, text: str) -> np.ndarray:
        """同步生成单个文本的 embedding（归一化向量）"""
        if text in self._cache:
            return self._cache[text]

        seed = self._text_to_seed(text)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(self._dim).astype(np.float32)

        # ✅ 归一化向量，确保余弦相似度在 [-1, 1] 范围内
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        self._cache[text] = vec
        return vec

    def embed_batch_sync(self, texts: list[str]) -> np.ndarray:
        """同步批量生成 embedding（每个向量单独归一化）"""
        embeddings = [self.embed(text) for text in texts]
        return np.array(embeddings)

    async def embed_text(self, text: str) -> np.ndarray:
        """异步生成单个文本的 embedding"""
        return self.embed(text)

    async def embed_batch(self, texts: list[str]) -> np.ndarray:
        """异步批量生成 embedding"""
        return self.embed_batch_sync(texts)


def get_embedder(backend: EmbeddingBackend = EmbeddingBackend.LOCAL) -> BaseEmbedder:
    """获取 embedding 后端实例

    Args:
        backend: Embedding 后端类型

    Returns:
        BaseEmbedder 实例
    """
    # 所有后端都使用本地 stub（用于测试）
    # 生产环境请替换为 LangChain Embeddings
    return _LocalStubEmbedder()


def batch_cosine_similarity(
    query_embedding: np.ndarray, embeddings: list[np.ndarray]
) -> np.ndarray:
    """计算查询向量与多个嵌入向量的余弦相似度。

    Args:
        query_embedding: 查询向量 (dim,)
        embeddings: 嵌入向量列表 [(dim,), ...]

    Returns:
        相似度数组 (n,)，每个元素是对应嵌入与查询的余弦相似度
    """
    if not embeddings:
        return np.array([])

    embeddings_matrix = np.array(embeddings)

    query_norm = np.linalg.norm(query_embedding)
    if query_norm == 0:
        return np.zeros(len(embeddings))

    embeddings_norms = np.linalg.norm(embeddings_matrix, axis=1)
    embeddings_norms = np.where(embeddings_norms == 0, 1, embeddings_norms)

    dot_products = np.dot(embeddings_matrix, query_embedding)
    similarities = dot_products / (embeddings_norms * query_norm)

    return similarities


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """计算两个向量的余弦相似度"""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))
