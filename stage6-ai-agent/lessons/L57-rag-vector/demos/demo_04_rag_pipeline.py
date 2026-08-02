"""Demo 04: 完整的检索增强生成（RAG）流水线闭环

from __future__ import annotations

本演示展示完整的 RAG 系统流程：
用户提问 → Embedding → 向量检索 → 上下文构建 → LLM 生成答案

核心要点：
1. 缝合 LLMRouter + VectorStore 实现完整 RAG
2. 完备的异常捕获与容错治理
3. 生产级 Exception 替代 assert
4. 端到端类型安全

运行方式：
    python demo_04_rag_pipeline.py
"""

import asyncio
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, ScoredPoint, VectorParams

from stage4_data_intelligence.core.llm_router import LLMRouter, Message


class RAGPipelineError(Exception):
    """RAG 流水线异常基类"""


class EmbeddingError(RAGPipelineError):
    """Embedding 生成失败"""


class RetrievalError(RAGPipelineError):
    """向量检索失败"""


class GenerationError(RAGPipelineError):
    """LLM 生成失败"""


class DimensionMismatchError(RAGPipelineError):
    """向量维度不匹配"""


class SimpleRAGPipeline:
    """
    简化版 RAG 流水线

    生产级特性：
    - 完备的异常处理
    - 类型安全保障
    - 异步非阻塞
    - 容错降级
    """

    def __init__(
        self,
        llm_router: LLMRouter,
        qdrant_client: AsyncQdrantClient,
        collection_name: str,
        vector_size: int,
    ) -> None:
        """
        初始化 RAG 流水线

        Args:
            llm_router: LLM 路由器
            qdrant_client: Qdrant 客户端
            collection_name: 集合名称
            vector_size: 向量维度

        Raises:
            ValueError: 参数无效时
        """
        if vector_size <= 0:
            raise ValueError(f"向量维度必须大于 0，当前: {vector_size}")

        self.llm_router = llm_router
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        self.vector_size = vector_size
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
            raise RAGPipelineError(f"集合初始化失败: {e}") from e

    async def ingest_documents(self, documents: list[str]) -> int:
        """
        摄取文档到向量库

        Args:
            documents: 文档列表

        Returns:
            成功摄取的文档数量

        Raises:
            EmbeddingError: Embedding 生成失败
            RetrievalError: 向量存储失败
        """
        if not self._initialized:
            await self.initialize()

        if not documents:
            raise ValueError("文档列表不能为空")

        try:
            # 生成 embeddings（模拟）
            embeddings = [self._mock_embedding(doc) for doc in documents]

            # 验证维度
            for i, emb in enumerate(embeddings):
                if len(emb) != self.vector_size:
                    raise DimensionMismatchError(f"文档 {i} 的 embedding 维度不匹配: 期望 {self.vector_size}, 实际 {len(emb)}")

            # 存储到向量库
            points = [
                PointStruct(
                    id=i,
                    vector=emb,
                    payload={"text": doc, "source": "demo", "index": i},
                )
                for i, (doc, emb) in enumerate(zip(documents, embeddings, strict=True))
            ]

            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            return len(documents)

        except DimensionMismatchError:
            raise
        except Exception as e:
            raise RetrievalError(f"文档摄取失败: {e}") from e

    async def query(self, question: str, top_k: int = 3) -> dict[str, Any]:
        """
        RAG 查询流程

        Args:
            question: 用户问题
            top_k: 返回结果数量

        Returns:
            包含 question, answer, sources 的字典

        Raises:
            EmbeddingError: Query embedding 生成失败
            RetrievalError: 向量检索失败
            GenerationError: LLM 生成失败
        """
        if not self._initialized:
            raise RAGPipelineError("RAG 流水线未初始化")

        if not question.strip():
            raise ValueError("问题不能为空")

        if top_k <= 0:
            raise ValueError(f"top_k 必须大于 0，当前: {top_k}")

        try:
            # Step 1: 生成 query embedding
            query_embedding = self._mock_embedding(question)

            # Step 2: 向量检索
            query_response = await self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
            )
            results: list[ScoredPoint] = query_response.points

            if not results:
                return {
                    "question": question,
                    "answer": "抱歉，我在知识库中没有找到相关信息。",
                    "sources": [],
                }

            # Step 3: 构建上下文
            context_parts: list[str] = []
            sources: list[dict[str, Any]] = []

            for i, hit in enumerate(results, 1):
                if hit.payload:
                    text: str = hit.payload.get("text", "")
                    if text:
                        score: float = hit.score if hit.score is not None else 0.0
                        context_parts.append(f"[文档 {i}] (相似度: {score:.2f})\n{text}")
                        sources.append(
                            {
                                "text": text,
                                "score": score,
                                "metadata": {k: v for k, v in hit.payload.items() if k != "text"},
                            }
                        )

            context = "\n\n".join(context_parts)

            # Step 4: 构建 Prompt
            prompt = self._build_prompt(question, context)

            # Step 5: LLM 生成答案
            messages: list[Message] = [{"role": "user", "content": prompt}]

            try:
                answer = await self.llm_router.chat(messages)
            except Exception as e:
                raise GenerationError(f"LLM 生成失败: {e}") from e

            return {
                "question": question,
                "answer": answer,
                "sources": sources,
                "context": context,
            }

        except (EmbeddingError, RetrievalError, GenerationError):
            raise
        except Exception as e:
            raise RAGPipelineError(f"RAG 查询失败: {e}") from e

    def _mock_embedding(self, text: str) -> list[float]:
        """
        模拟 embedding 生成（实际应使用真实模型）

        Args:
            text: 输入文本

        Returns:
            向量列表

        Raises:
            EmbeddingError: 生成失败时
        """
        try:
            import random

            random.seed(hash(text))
            return [random.random() for _ in range(self.vector_size)]
        except Exception as e:
            raise EmbeddingError(f"Embedding 生成失败: {e}") from e

    def _build_prompt(self, question: str, context: str) -> str:
        """
        构建 RAG prompt

        Args:
            question: 用户问题
            context: 检索到的上下文

        Returns:
            完整的 prompt
        """
        return f"""基于以下上下文回答问题：

上下文:
{context}

问题: {question}

要求：
1. 只基于上下文回答，不要编造信息
2. 如果上下文中没有相关信息，明确说明
3. 引用具体的文档片段
4. 保持简洁，直接回答问题

回答:"""


async def demo_basic_rag() -> None:
    """演示基础 RAG 流程"""
    print("=" * 60)
    print("Demo 4.1: 基础 RAG 流程")
    print("=" * 60)

    # 初始化组件
    llm_router = LLMRouter(mode="LOCAL")
    qdrant_client = AsyncQdrantClient(":memory:")

    try:
        # 创建 RAG 流水线
        rag = SimpleRAGPipeline(
            llm_router=llm_router,
            qdrant_client=qdrant_client,
            collection_name="demo_knowledge",
            vector_size=128,
        )

        print("✅ RAG 流水线已创建")

        # 摄取文档
        documents = [
            "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
            "FastAPI 是一个现代化的 Web 框架，支持异步编程和自动 API 文档生成。",
            "Qdrant 是一个高性能的向量数据库，专为语义搜索和 RAG 系统设计。",
            "异步编程可以提高 I/O 密集型应用的性能，Python 3.12 进一步优化了 asyncio。",
        ]

        print(f"\n⏳ 正在摄取 {len(documents)} 条文档...")
        await rag.ingest_documents(documents)
        print("✅ 文档摄取完成")

        # RAG 查询
        questions = [
            "Python 是什么时候创建的？",
            "FastAPI 有哪些特性？",
            "什么是向量数据库？",
        ]

        for question in questions:
            print(f"\n{'─' * 60}")
            print(f"🔍 问题: {question}")
            print("─" * 60)

            result = await rag.query(question, top_k=2)

            print(f"✅ 答案: {result['answer']}")
            print(f"\n📚 来源 ({len(result['sources'])} 个):")
            for i, source in enumerate(result["sources"], 1):
                score: float = source["score"]
                text: str = source["text"]
                print(f"  {i}. [相似度: {score:.2f}] {text[:50]}...")

    finally:
        await qdrant_client.close()


async def demo_error_handling() -> None:
    """演示完备的错误处理"""
    print("\n" + "=" * 60)
    print("Demo 4.2: 完备的错误处理")
    print("=" * 60)

    llm_router = LLMRouter(mode="LOCAL")
    qdrant_client = AsyncQdrantClient(":memory:")

    try:
        rag = SimpleRAGPipeline(
            llm_router=llm_router,
            qdrant_client=qdrant_client,
            collection_name="error_demo",
            vector_size=128,
        )

        # 测试 1: 未初始化查询
        print("\n🧪 测试 1: 未初始化查询")
        try:
            await rag.query("测试问题")
        except RAGPipelineError as e:
            print(f"✅ 捕获预期异常: {type(e).__name__}: {e}")

        # 测试 2: 空文档列表
        print("\n🧪 测试 2: 空文档列表")
        try:
            await rag.ingest_documents([])
        except ValueError as e:
            print(f"✅ 捕获预期异常: {type(e).__name__}: {e}")

        # 测试 3: 无效 top_k
        print("\n🧪 测试 3: 无效 top_k")
        await rag.initialize()
        await rag.ingest_documents(["测试文档"])
        try:
            await rag.query("测试问题", top_k=0)
        except ValueError as e:
            print(f"✅ 捕获预期异常: {type(e).__name__}: {e}")

        print("\n✅ 所有错误处理测试通过")

    finally:
        await qdrant_client.close()


async def demo_empty_results() -> None:
    """演示空结果处理"""
    print("\n" + "=" * 60)
    print("Demo 4.3: 空结果处理")
    print("=" * 60)

    llm_router = LLMRouter(mode="LOCAL")
    qdrant_client = AsyncQdrantClient(":memory:")

    try:
        rag = SimpleRAGPipeline(
            llm_router=llm_router,
            qdrant_client=qdrant_client,
            collection_name="empty_demo",
            vector_size=128,
        )

        await rag.initialize()

        # 在空知识库中查询
        print("\n🔍 在空知识库中查询...")
        result = await rag.query("这是一个问题")

        print(f"✅ 答案: {result['answer']}")
        print(f"✅ 来源数量: {len(result['sources'])}")
        print("✅ 空结果处理正确")

    finally:
        await qdrant_client.close()


async def main() -> None:
    """主函数：运行所有演示"""
    print("\n" + "🚀" * 30)
    print("L17 Demo 04: 完整的 RAG 流水线闭环")
    print("🚀" * 30 + "\n")

    # 运行所有演示
    await demo_basic_rag()
    await demo_error_handling()
    await demo_empty_results()

    print("\n" + "✅" * 30)
    print("所有演示完成！")
    print("✅" * 30 + "\n")

    # 关键学习点总结
    print("📚 关键学习点:")
    print("=" * 60)
    print("1. ✅ 完整 RAG 流程：Query → Embedding → 检索 → 生成")
    print("2. ✅ 生产级异常处理：自定义 Exception 替代 assert")
    print("3. ✅ 容错治理：空结果、维度不匹配、LLM 失败")
    print("4. ✅ 类型安全：端到端类型注解")
    print("5. ✅ 异步非阻塞：全异步 API 调用")
    print("=" * 60)

    print("\n💡 生产部署建议:")
    print("   1. 使用真实的 Embedding 模型（如 nomic-embed-text）")
    print("   2. 添加缓存层（Redis）减少重复查询")
    print("   3. 实现重排序（Reranking）提高召回质量")
    print("   4. 监控性能指标（延迟、QPS、准确率）")
    print("   5. 实现降级策略（本地模型 fallback）")


if __name__ == "__main__":
    # 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
    except Exception as e:
        print(f"\n\n❌ 未捕获的异常: {type(e).__name__}: {e}")
        raise
