"""P06: RAG 向量存储模块"""

import numpy as np


class VectorStore:
    """向量存储与检索"""

    def __init__(self, config=None):
        self.config = config
        self.vectors: list[np.ndarray] = []
        self.documents: list[str] = []
        self.dimensions = config.embedding_dim if config else 384

    async def add_documents(self, documents: list[str]) -> None:
        """添加文档"""
        for doc in documents:
            # 简化的 embedding（实际应使用模型）
            vector = np.random.randn(self.dimensions)
            vector = vector / np.linalg.norm(vector)
            self.vectors.append(vector)
            self.documents.append(doc)

    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        """向量检索"""
        # 简化的 query embedding
        query_vector = np.random.randn(self.dimensions)
        query_vector = query_vector / np.linalg.norm(query_vector)

        # 计算相似度
        scores = []
        for vec in self.vectors:
            score = np.dot(query_vector, vec)
            scores.append(score)

        # 返回 top_k 结果
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = []
        for idx in top_indices:
            results.append({"doc": self.documents[idx], "score": float(scores[idx])})
        return results

    def count(self) -> int:
        """文档数量"""
        return len(self.documents)
