# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】向量存储服务

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

import numpy as np

# TODO: 导入 SearchResult 模型
# from ...models import SearchResult


class InMemoryVectorStore:
    """内存向量存储，支持余弦相似度检索"""

    def __init__(self, dimension: int = 1536):
        # TODO: 初始化：
        # 1. self.dimension = dimension
        # 2. self.vectors: np.ndarray = np.array([], shape=(0, dimension))
        # 3. self.doc_ids: list[str] = []
        # 4. self.contents: list[str] = []
        # ← 你的代码写在这里
        pass

    def add(
        self, doc_id: str, chunks: list[str], embedding_fn: callable[[str], np.ndarray]
    ) -> None:  # noqa: E501
        """添加文档分块

        步骤：
        1. 对每个 chunk 计算 embedding
        2. 将向量追加到 self.vectors
        3. 记录 doc_id 和 chunk 内容
        """
        # TODO: 实现添加
        # ← 你的代码写在这里

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[SearchResult]:
        """相似性搜索

        步骤：
        1. 计算查询向量和所有存储向量的余弦相似度
        2. 按相似度降序排序
        3. 返回 top_k 个结果
        """
        # TODO: 实现搜索
        # 提示：余弦相似度 = (a · b) / (||a|| * ||b||)
        # ← 你的代码写在这里


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算两个向量的余弦相似度"""
    # TODO: 实现余弦相似度计算
    # ← 你的代码写在这里
