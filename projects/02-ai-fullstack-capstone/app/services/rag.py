"""RAG 检索服务（支持线程安全的 Embedding 和优雅关闭）。"""

from __future__ import annotations

from app.models import Chunk, Document
from app.services.vector_store import InMemoryVectorStore


class RAGService:
    """检索增强生成服务的检索部分。

    支持上下文管理器协议，可自动释放资源。
    集成线程安全的 Embedding 服务，支持优雅关闭。
    """

    def __init__(self, store: InMemoryVectorStore | None = None) -> None:
        self.store = store or InMemoryVectorStore()
        self._closed = False

    async def ingest(self, title: str, content: str, source: str = "manual") -> list[Chunk]:
        """导入文档。

        Args:
            title: 文档标题
            content: 文档内容
            source: 文档来源

        Returns:
            生成的文本块列表

        Raises:
            RuntimeError: 服务已关闭
        """
        if self._closed:
            raise RuntimeError("RAGService 已关闭，无法导入文档")

        document = Document.create(title=title, content=content, source=source)
        return await self.store.add_document(document)

    async def retrieve(self, query: str, top_k: int = 3) -> list[Chunk]:
        """检索相关片段。

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            相关文本块列表

        Raises:
            RuntimeError: 服务已关闭
        """
        if self._closed:
            raise RuntimeError("RAGService 已关闭，无法检索")

        return await self.store.search(query, top_k=top_k)

    def corpus_size(self) -> int:
        """返回语料库大小（文档数量）。"""
        return self.store.count()

    def close(self) -> None:
        """释放资源，清空所有缓存的文档和向量。

        幂等操作，可以安全地多次调用。

        ✅ 优雅关闭：
        1. 清空文档和向量缓存
        2. 关闭 embedder 的 ThreadPoolExecutor（如果是 SentenceTransformerEmbedder）
        """
        if not self._closed:
            # 清空向量存储
            self.store.chunks.clear()
            self.store.documents.clear()
            self.store.chunk_embeddings.clear()

            # 优雅关闭 embedder 的线程池
            if hasattr(self.store.embedder, "_executor"):
                # SentenceTransformerEmbedder 有 ThreadPoolExecutor
                self.store.embedder._executor.shutdown(wait=True)
                print("✅ Embedder ThreadPoolExecutor 已优雅关闭")

            self._closed = True

    def __enter__(self) -> RAGService:
        """上下文管理器入口。"""
        return self

    def __exit__(self, *args: object) -> None:
        """上下文管理器退出，自动释放资源。"""
        self.close()
