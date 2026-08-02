# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】RAG 检索服务

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

import numpy as np

# TODO: 导入
# from ...models import SearchResult
# from .vector_store import InMemoryVectorStore
# from .storage import DocumentStorage


class RAGService:
    """RAG 检索服务"""

    def __init__(
        self,
        vector_store: InMemoryVectorStore,
        document_store: DocumentStorage,
        embedding_fn: callable[[str], np.ndarray],
    ):
        # TODO: 保存依赖
        # self.vector_store = vector_store
        # self.document_store = document_store
        # self.embedding_fn = embedding_fn
        # ← 你的代码写在这里
        pass

    def add_document(self, doc_id: str, chunks: list[str]) -> None:
        """添加文档到向量存储"""
        # TODO: 调用 vector_store.add
        # ← 你的代码写在这里

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """搜索相关文档片段

        步骤：
        1. 对查询计算 embedding
        2. 向量存储检索 top_k
        3. 返回检索结果
        """
        # TODO: 实现搜索
        # ← 你的代码写在这里
