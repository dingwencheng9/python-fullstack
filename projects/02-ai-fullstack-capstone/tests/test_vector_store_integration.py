"""Projects/02 向量存储集成测试（线程安全版本）

from __future__ import annotations

验证 InMemoryVectorStore 与线程安全 Embedding 的集成功能。

✅ 测试覆盖：
- Embedding 生成（确定性、归一化）
- 向量存储和检索
- 相似度计算的正确性
- 批量优化（batch_cosine_similarity）

⚠️ 注意：本测试使用本地 stub embedder，它提供确定性的伪随机向量，
用于测试基础设施的正确性，而非语义搜索能力。
"""

import pytest

from app.models import Document
from app.services.vector_store import InMemoryVectorStore
from core.embedding_service_threadsafe import (
    EmbeddingBackend,
    batch_cosine_similarity,
    get_embedder,
)


@pytest.fixture
def embedder():
    """创建本地 stub Embedder"""
    return get_embedder(EmbeddingBackend.LOCAL)


@pytest.fixture
def vector_store(embedder):
    """创建向量存储实例（使用 stub embedder）"""
    return InMemoryVectorStore(embedder=embedder)


@pytest.fixture
def sample_documents():
    """测试文档"""
    return [
        Document(
            id="doc1",
            title="Python 编程",
            content="Python 是一门强大的编程语言，广泛应用于 Web 开发、数据科学和机器学习。",
        ),
        Document(
            id="doc2",
            title="机器学习",
            content="机器学习是人工智能的核心技术，使用 Python 可以轻松实现各种算法。",
        ),
        Document(
            id="doc3",
            title="FastAPI 框架",
            content="FastAPI 是一个现代化的 Web 框架，基于 Python 3.6+ 类型提示构建。",
        ),
        Document(
            id="doc4",
            title="Docker 容器",
            content="Docker 容器技术简化了应用部署，是现代 DevOps 的重要工具。",
        ),
    ]


@pytest.mark.asyncio
class TestInMemoryVectorStoreIntegration:
    """测试 InMemoryVectorStore 的完整功能"""

    async def test_add_document_generates_embeddings(self, vector_store, sample_documents):
        """测试添加文档时生成 embedding"""
        doc = sample_documents[0]
        chunks = await vector_store.add_document(doc)

        # 验证生成了 chunks
        assert len(chunks) > 0

        # 验证每个 chunk 都有对应的 embedding
        for chunk in chunks:
            assert chunk.id in vector_store.chunk_embeddings
            embedding = vector_store.chunk_embeddings[chunk.id]

            # 验证 embedding 的形状和归一化
            import numpy as np

            assert embedding.shape == (vector_store.embedding_dim,)
            norm = np.linalg.norm(embedding)
            assert abs(norm - 1.0) < 1e-5, "Embedding 应该是归一化的"

    async def test_search_returns_results(self, vector_store, sample_documents):
        """测试搜索返回结果"""
        # 添加所有文档
        for doc in sample_documents:
            await vector_store.add_document(doc)

        # 搜索
        query = "Python 编程语言"
        results = await vector_store.search(query, top_k=3)

        # 验证返回了结果
        assert len(results) > 0
        assert len(results) <= 3

        # 验证所有结果都有相似度分数
        for chunk in results:
            assert chunk.score is not None
            # stub embedder 的相似度在 [-1, 1] 范围内
            assert -1 <= chunk.score <= 1, f"相似度分数应该在 [-1, 1]，实际: {chunk.score}"

    async def test_identical_query_consistent_results(self, vector_store, sample_documents):
        """测试相同查询返回一致的结果（stub embedder 的确定性）"""
        doc = sample_documents[0]
        await vector_store.add_document(doc)

        # 相同查询应该返回相同结果
        query = "Python 是一门强大的编程语言"
        results1 = await vector_store.search(query, top_k=1)
        results2 = await vector_store.search(query, top_k=1)

        assert len(results1) == len(results2)
        assert results1[0].id == results2[0].id
        assert abs(results1[0].score - results2[0].score) < 1e-6

    async def test_deterministic_embeddings(self, embedder):
        """测试 stub embedder 的确定性"""
        text = "Python 编程语言"

        embedding1 = embedder.embed(text)
        embedding2 = embedder.embed(text)

        import numpy as np

        # 相同文本应该产生完全相同的 embedding
        assert np.allclose(embedding1, embedding2)

    async def test_semantic_search_ranking(self, vector_store, sample_documents):
        """测试语义搜索的正确排序（验证结果按分数降序）"""
        # 添加所有文档
        for doc in sample_documents:
            await vector_store.add_document(doc)

        # 搜索
        query = "Python 编程"
        results = await vector_store.search(query, top_k=3)

        # 验证返回了结果
        assert len(results) > 0

        # 验证结果按相似度降序排列
        scores = [chunk.score for chunk in results]
        assert scores == sorted(scores, reverse=True), "结果应该按相似度降序排列"

    async def test_empty_query_returns_empty(self, vector_store, sample_documents):
        """测试空查询返回空结果"""
        await vector_store.add_document(sample_documents[0])

        results = await vector_store.search("", top_k=5)
        assert len(results) == 0, "空查询应该返回空结果"

        results = await vector_store.search("   ", top_k=5)
        assert len(results) == 0, "空白查询应该返回空结果"

    async def test_top_k_limit(self, vector_store, sample_documents):
        """测试 top_k 限制"""
        # 添加多个文档
        for doc in sample_documents:
            await vector_store.add_document(doc)

        # 请求 top_k=2
        results = await vector_store.search("Python", top_k=2)
        assert len(results) <= 2, "返回结果不应超过 top_k"

    async def test_multiple_documents(self, vector_store, sample_documents):
        """测试添加多个文档"""
        for doc in sample_documents:
            await vector_store.add_document(doc)

        assert vector_store.count() == len(sample_documents)
        assert len(vector_store.chunks) > 0


@pytest.mark.asyncio
class TestBatchCosineSimilarity:
    """测试 batch_cosine_similarity 函数"""

    async def test_batch_cosine_similarity_basic(self):
        """测试基本的批量余弦相似度计算"""
        import numpy as np

        # 查询向量
        query = np.array([1.0, 0.0, 0.0], dtype=np.float32)

        # 嵌入向量
        embeddings = [
            np.array([1.0, 0.0, 0.0], dtype=np.float32),  # 相同方向
            np.array([0.0, 1.0, 0.0], dtype=np.float32),  # 正交
            np.array([-1.0, 0.0, 0.0], dtype=np.float32),  # 相反方向
        ]

        similarities = batch_cosine_similarity(query, embeddings)

        # 验证相似度
        assert len(similarities) == 3
        assert abs(similarities[0] - 1.0) < 1e-5  # 相同方向 = 1.0
        assert abs(similarities[1] - 0.0) < 1e-5  # 正交 = 0.0
        assert abs(similarities[2] - (-1.0)) < 1e-5  # 相反方向 = -1.0

    async def test_batch_cosine_similarity_normalized(self):
        """测试归一化向量的批量相似度"""
        import numpy as np

        query = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        embeddings = [np.array([0.707, 0.707, 0.0], dtype=np.float32)]

        similarities = batch_cosine_similarity(query, embeddings)

        # 验证相似度在 [-1, 1] 范围内
        assert -1 <= similarities[0] <= 1

    async def test_batch_cosine_similarity_empty(self):
        """测试空列表"""
        import numpy as np

        query = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        similarities = batch_cosine_similarity(query, [])

        assert len(similarities) == 0


@pytest.mark.asyncio
class TestEmbeddingBackendSelection:
    """测试 Embedding 后端选择"""

    async def test_local_backend(self):
        """测试本地后端"""
        embedder = get_embedder(EmbeddingBackend.LOCAL)
        assert embedder.dimension == 384

    async def test_embedder_produces_normalized_vectors(self, embedder):
        """测试 embedder 产生归一化向量"""
        import numpy as np

        embedding = await embedder.embed_text("test text")
        norm = np.linalg.norm(embedding)

        assert abs(norm - 1.0) < 1e-5, "Embedding 应该是归一化的"

    async def test_batch_embeddings(self, embedder):
        """测试批量 embedding"""
        import numpy as np

        texts = ["text1", "text2", "text3"]
        embeddings = await embedder.embed_batch(texts)

        assert embeddings.shape == (3, embedder.dimension)

        # 验证所有向量都归一化
        for i, text in enumerate(texts):
            norm = np.linalg.norm(embeddings[i])
            assert abs(norm - 1.0) < 1e-5
