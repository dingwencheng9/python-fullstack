"""Solution 01: Embedding Pipeline 实现

from __future__ import annotations

完整的 Embedding Pipeline，包含文本分块、向量生成和存储。
严格遵循异步设计模式，生产级异常处理。
"""

import asyncio
import random
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class EmbeddingError(Exception):
    """Embedding 生成异常"""


class StorageError(Exception):
    """存储异常"""


class TextChunker:
    """文本分块器

    将长文本切分为固定大小的块，支持重叠。
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        """
        初始化分块器

        Args:
            chunk_size: 每个块的最大字符数
            overlap: 块之间的重叠字符数

        Raises:
            ValueError: 参数无效时
        """
        if chunk_size <= 0:
            raise ValueError(f"chunk_size 必须大于 0，当前: {chunk_size}")
        if overlap < 0:
            raise ValueError(f"overlap 必须大于等于 0，当前: {overlap}")
        if overlap >= chunk_size:
            raise ValueError(f"overlap ({overlap}) 必须小于 chunk_size ({chunk_size})")

        self.chunk_size = chunk_size
        self.overlap = overlap

    async def chunk(self, text: str) -> list[str]:
        """
        异步分块文本

        Args:
            text: 输入文本

        Returns:
            分块后的文本列表

        Raises:
            ValueError: 文本为空时
        """
        if not text.strip():
            raise ValueError("文本不能为空")

        # 模拟异步操作（实际可能涉及 I/O）
        await asyncio.sleep(0)

        chunks: list[str] = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()

            if chunk:  # 跳过空块
                chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks


class EmbeddingPipeline:
    """Embedding 流水线

    完整流程：文本 → 分块 → 生成向量 → 存储到 Qdrant
    """

    def __init__(
        self,
        qdrant_client: AsyncQdrantClient,
        collection_name: str,
        vector_size: int = 384,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        """
        初始化 Pipeline

        Args:
            qdrant_client: Qdrant 异步客户端
            collection_name: 集合名称
            vector_size: 向量维度
            chunk_size: 分块大小
            overlap: 块重叠大小

        Raises:
            ValueError: 参数无效时
        """
        if vector_size <= 0:
            raise ValueError(f"vector_size 必须大于 0，当前: {vector_size}")

        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        self._initialized = False

    async def initialize(self) -> None:
        """初始化向量集合"""
        if self._initialized:
            return

        try:
            await self.qdrant_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            self._initialized = True
        except Exception as e:
            raise StorageError(f"集合初始化失败: {e}") from e

    async def process_document(
        self,
        document: str,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """
        处理单个文档

        Args:
            document: 文档文本
            metadata: 元数据（可选）

        Returns:
            插入的向量数量

        Raises:
            ValueError: 文档为空时
            EmbeddingError: Embedding 生成失败
            StorageError: 存储失败
        """
        if not document.strip():
            raise ValueError("文档不能为空")

        # 确保集合已初始化
        if not self._initialized:
            await self.initialize()

        # Step 1: 文本分块
        try:
            chunks = await self.chunker.chunk(document)
        except Exception as e:
            raise ValueError(f"文本分块失败: {e}") from e

        if not chunks:
            raise ValueError("分块后结果为空")

        # Step 2: 生成 embeddings
        try:
            embeddings = [self._generate_embedding(chunk) for chunk in chunks]
        except Exception as e:
            raise EmbeddingError(f"Embedding 生成失败: {e}") from e

        # Step 3: 构建 Points
        base_metadata = metadata or {}
        points = [
            PointStruct(
                id=i,
                vector=emb,
                payload={
                    "text": chunk,
                    "chunk_index": i,
                    **base_metadata,
                },
            )
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings, strict=True))
        ]

        # Step 4: 批量存储
        try:
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
        except Exception as e:
            raise StorageError(f"向量存储失败: {e}") from e

        return len(points)

    def _generate_embedding(self, text: str) -> list[float]:
        """
        生成 embedding（模拟）

        实际生产环境应使用真实模型（如 nomic-embed-text）

        Args:
            text: 输入文本

        Returns:
            向量列表

        Raises:
            EmbeddingError: 生成失败时
        """
        try:
            random.seed(hash(text))
            return [random.random() for _ in range(self.vector_size)]
        except Exception as e:
            raise EmbeddingError(f"Embedding 生成失败: {e}") from e


# ============================================================================
# 测试代码
# ============================================================================


async def test_text_chunker() -> None:
    """测试文本分块器"""
    print("=" * 60)
    print("测试: TextChunker")
    print("=" * 60)

    chunker = TextChunker(chunk_size=20, overlap=5)

    # 测试正常分块
    text = "Hello World! This is a test. We need multiple chunks."
    chunks = await chunker.chunk(text)

    print(f"✅ 原始文本长度: {len(text)}")
    print(f"✅ 分块数量: {len(chunks)}")
    print("✅ 块内容:")
    for i, chunk in enumerate(chunks, 1):
        print(f"   {i}. [{len(chunk)}字符] {chunk}")

    # 测试空文本
    try:
        await chunker.chunk("")
    except ValueError as e:
        print(f"✅ 空文本异常捕获: {e}")


async def test_embedding_pipeline() -> None:
    """测试 Embedding Pipeline"""
    print("\n" + "=" * 60)
    print("测试: EmbeddingPipeline")
    print("=" * 60)

    client = AsyncQdrantClient(":memory:")

    try:
        pipeline = EmbeddingPipeline(
            qdrant_client=client,
            collection_name="test_pipeline",
            vector_size=128,
            chunk_size=50,
            overlap=10,
        )

        # 测试文档处理
        document = "这是一个测试文档。" * 10  # 创建一个足够长的文档以产生多个分块

        count = await pipeline.process_document(
            document=document,
            metadata={"source": "test", "type": "demo"},
        )

        print(f"✅ 文档长度: {len(document)}")
        print(f"✅ 插入向量数量: {count}")

        # 测试空文档
        try:
            await pipeline.process_document("")
        except ValueError as e:
            print(f"✅ 空文档异常捕获: {e}")

    finally:
        await client.close()


async def main() -> None:
    """主测试函数"""
    print("\n" + "🚀" * 30)
    print("Solution 01: Embedding Pipeline 测试")
    print("🚀" * 30 + "\n")

    await test_text_chunker()
    await test_embedding_pipeline()

    print("\n" + "✅" * 30)
    print("所有测试完成！")
    print("✅" * 30 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
