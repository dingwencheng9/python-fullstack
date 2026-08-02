"""真实语义向量检索存储（基于余弦相似度的向量检索架构）。

from __future__ import annotations

✅ 生产级实现（线程安全版本）：
- 移除所有伪随机 embedding 生成（np.random.randn）
- 集成线程安全 Embedding 服务（SentenceTransformers / OpenAI / 智谱）
- 使用真实余弦相似度进行检索
- 支持本地和远程 Embedding 后端
- ThreadPoolExecutor 隔离执行，支持优雅关闭

架构说明：
1. 文档切片 → 生成真实 embedding 向量（线程安全）
2. 查询 → 生成查询向量（线程安全）
3. 计算所有 chunk 的余弦相似度
4. 按相似度降序排序，返回 top_k
"""
# ruff: noqa: E402
# 项目特殊结构：需要动态添加 stage4 路径后再导入

from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import numpy as np
from numpy.typing import NDArray

# 添加项目根目录到 sys.path（用于导入 settings 和 stage4）
project_root = Path(__file__).parent.parent.parent
repo_root = project_root.parent.parent
stage4_root = repo_root / "stage4-data-intelligence"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
if str(stage4_root) not in sys.path:
    sys.path.insert(0, str(stage4_root))


# 导入线程安全的 embedding service
from app.models import Chunk, Document
from core.embedding_service_threadsafe import (
    BaseEmbedder,
    EmbeddingBackend,
    batch_cosine_similarity,
    get_embedder,
)


def chunk_text(text: str, size: int = 300, overlap: int = 50) -> list[str]:
    """按字符切分文本，带重叠。

    Args:
        text: 输入文本
        size: 每个块的最大字符数
        overlap: 块之间的重叠字符数

    Returns:
        文本块列表
    """
    if len(text) <= size:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def cosine_similarity(vec_a: NDArray[np.float32], vec_b: NDArray[np.float32]) -> float:
    """计算余弦相似度（numpy 优化版本）。

    Formula: cos(θ) = (A · B) / (||A|| × ||B||)

    对于归一化向量，余弦相似度等于点积。

    Args:
        vec_a: 向量 A
        vec_b: 向量 B

    Returns:
        余弦相似度，范围 [-1, 1]，值越大表示越相似
    """
    if vec_a.shape != vec_b.shape:
        raise ValueError(f"向量维度必须相同: {vec_a.shape} vs {vec_b.shape}")

    # 对于归一化向量，余弦相似度 = 点积
    return float(np.dot(vec_a, vec_b))


class InMemoryVectorStore:
    """基于真实语义向量的内存检索器（余弦相似度排序）。

    核心架构：
    1. 文档切片 → 生成真实 embedding 向量
    2. 查询 → 生成查询向量
    3. 计算所有 chunk 的余弦相似度
    4. 按相似度降序排序，返回 top_k

    支持的 Embedding 后端：
    - SentenceTransformers: all-MiniLM-L6-v2 (384维，本地)
    - OpenAI: text-embedding-3-small (1536维，远程)
    - 智谱: embedding-3 (2048维，远程)
    """

    def __init__(
        self,
        backend: EmbeddingBackend | None = None,
        embedder: BaseEmbedder | None = None,
    ) -> None:
        """初始化向量存储。

        Args:
            backend: 指定 Embedding 后端，None 则自动选择
            embedder: 直接传入 Embedder 实例（用于测试）
        """
        self.documents: dict[str, Document] = {}
        self.chunks: list[Chunk] = []
        self.chunk_embeddings: dict[str, NDArray[np.float32]] = {}

        # 初始化 Embedder
        if embedder is not None:
            self.embedder = embedder
        else:
            self.embedder = get_embedder(backend)

        self.embedding_dim = self.embedder.dimension

    async def add_document(self, document: Document) -> list[Chunk]:
        """添加文档、切片并生成真实 embedding 向量。

        流程：
        1. 文档切片（300 字符/块，50 字符重叠）
        2. 为每个 chunk 生成真实 embedding 向量
        3. 存储 chunk 和对应的向量

        Args:
            document: 待添加的文档对象

        Returns:
            新增的 chunk 列表
        """
        self.documents[document.id] = document
        text_chunks = chunk_text(document.content)
        new_chunks = [
            Chunk(id=str(uuid4()), document_id=document.id, text=text) for text in text_chunks
        ]

        # 批量生成真实 embeddings
        chunk_texts = [chunk.text for chunk in new_chunks]
        embeddings = await self.embedder.embed_batch(chunk_texts)

        # 存储 embeddings
        for chunk, embedding in zip(new_chunks, embeddings, strict=True):
            self.chunk_embeddings[chunk.id] = embedding

        self.chunks.extend(new_chunks)
        return new_chunks

    async def search(self, query: str, top_k: int = 3) -> list[Chunk]:
        """基于真实语义向量的余弦相似度检索。

        流程：
        1. 生成查询的真实 embedding 向量
        2. 使用 batch_cosine_similarity 批量计算余弦相似度（numpy 优化）
        3. 按相似度降序排序
        4. 返回前 top_k 个最相关的 chunk

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            按相似度排序的 chunk 列表（包含相似度分数）
        """
        if not query.strip():
            return []

        # 生成查询的真实 embedding 向量
        query_embedding = await self.embedder.embed_text(query)

        # 批量计算所有 chunk 的相似度（numpy 矩阵优化）
        embeddings = [
            self.chunk_embeddings[chunk.id]
            for chunk in self.chunks
            if chunk.id in self.chunk_embeddings
        ]

        if not embeddings:
            return []

        # 使用 batch_cosine_similarity 高效计算（numpy 优化）
        similarities = batch_cosine_similarity(query_embedding, embeddings)

        # 构建带分数的结果
        scored: list[tuple[Chunk, float]] = [
            (chunk, float(sim))
            for chunk, sim in zip(self.chunks, similarities)
            if chunk.id in self.chunk_embeddings
        ]

        # 按相似度降序排序
        scored.sort(key=lambda x: x[1], reverse=True)

        # 返回 top_k 结果（带相似度分数）
        return [Chunk(c.id, c.document_id, c.text, score) for c, score in scored[:top_k]]

    def count(self) -> int:
        """返回存储的文档数量。"""
        return len(self.documents)
