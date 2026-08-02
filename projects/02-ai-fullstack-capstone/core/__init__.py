"""Core 模块 - embedding 服务占位符。

本模块是 stub 占位符，详见 embedding_service_threadsafe.py
"""

from __future__ import annotations

from core.embedding_service_threadsafe import (
    BaseEmbedder,
    EmbeddingBackend,
    batch_cosine_similarity,
    cosine_similarity,
    get_embedder,
)

__all__ = [
    "BaseEmbedder",
    "EmbeddingBackend",
    "batch_cosine_similarity",
    "cosine_similarity",
    "get_embedder",
]
