"""P06 练习 2: RAG 向量检索"""

from __future__ import annotations

import numpy as np
from typing import List, Tuple

# ============ Embedding 实现 ============

def simple_embedding(text: str, dim: int = 64) -> np.ndarray:
    """简单 Embedding 实现（基于词频）"""
    words = set(text.lower().split())
    vec = np.zeros(dim)

    # 关键词列表（简化）
    keywords = ["data", "analysis", "report", "sales", "revenue",
                "customer", "product", "order", "trend", "growth"]

    for i, kw in enumerate(keywords):
        if kw in words:
            vec[i] = 1.0

    # L2 归一化
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    return vec

def batch_embedding(texts: List[str], dim: int = 64) -> np.ndarray:
    """批量 Embedding"""
    # TODO: 使用 list comprehension 调用 simple_embedding
    # 提示: np.array([...])

    # 你的代码:
    # return np.array([...])

    return np.zeros((len(texts), dim))

# ============ 相似度计算 ============

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算两个向量的余弦相似度"""
    # TODO: 实现余弦相似度
    # 提示: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # 你的代码:
    # return ...

    return 0.0

def batch_similarity(query: np.ndarray, docs: np.ndarray) -> np.ndarray:
    """批量计算查询向量与所有文档的相似度"""
    # TODO: 批量计算（向量化）
    # 提示: 使用矩阵乘法

    # 你的代码:
    # query_norm = query / np.linalg.norm(query)
    # docs_norm = docs / np.linalg.norm(docs, axis=1, keepdims=True)
    # return np.dot(docs_norm, query_norm)

    return np.zeros(len(docs))

def top_k_retrieval(
    query: str,
    documents: List[str],
    embeddings: np.ndarray,
    k: int = 3
) -> List[Tuple[int, float]]:
    """Top-K 检索"""
    # TODO: 实现 Top-K 检索
    # 1. 生成查询向量
    # 2. 计算与所有文档的相似度
    # 3. 返回 Top-K

    # 你的代码:
    # query_vec = simple_embedding(query)
    # similarities = batch_similarity(query_vec, embeddings)
    # top_indices = np.argsort(similarities)[::-1][:k]
    # return [(idx, similarities[idx]) for idx in top_indices]

    return []

# ============ 运行测试 ============

if __name__ == "__main__":
    # 文档集合
    documents = [
        "data analysis shows sales growth",
        "customer satisfaction report",
        "product revenue trend analysis",
        "order volume increased",
        "customer acquisition report",
    ]

    # 生成文档向量
    doc_embeddings = batch_embedding(documents)
    print(f"文档向量形状: {doc_embeddings.shape}")

    # 测试检索
    query = "sales report"
    results = top_k_retrieval(query, documents, doc_embeddings, k=3)

    print(f"\n查询: {query}")
    print("Top-3 结果:")
    for idx, score in results:
        print(f"  [{score:.3f}] {documents[idx]}")
