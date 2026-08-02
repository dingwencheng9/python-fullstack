"""

from __future__ import annotations

示例 2: RAG完整管道 - 检索增强生成系统

教学目标：
1. 理解RAG（Retrieval-Augmented Generation）架构
2. 掌握向量数据库的使用
3. 实现完整的RAG工作流
4. 理解上下文窗口和重排序

核心技术：
- 向量索引和检索
- Top-K检索
- 重排序（Reranking）
- 上下文构建
- LLM提示词工程

RAG工作流程：
1. 文档分块（Chunking）
2. 向量化（Embedding）
3. 存储到向量数据库
4. 查询向量化
5. 相似度检索（Top-K）
6. 重排序（可选）
7. 构建上下文
8. 调用LLM生成答案

运行方式：
    python examples/02_rag_pipeline.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import numpy as np

# ============================================================================
# 第一部分：理解RAG架构
# ============================================================================


def explain_rag_architecture():
    """解释RAG架构的核心概念

    什么是RAG？
    - Retrieval-Augmented Generation（检索增强生成）
    - 结合检索系统和生成模型的优点
    - 让LLM基于实时的、特定领域的知识回答问题

    为什么需要RAG？
    1. LLM训练数据有时效性（知识截止日期）
    2. LLM无法记住所有细节（幻觉问题）
    3. 企业内部数据无法训练进模型
    4. 微调成本高，RAG更灵活

    RAG vs 微调：
    - RAG: 低成本，实时更新，适合动态知识
    - 微调: 高成本，固化知识，适合特定风格
    """
    print("=" * 70)
    print("RAG架构详解")
    print("=" * 70)

    print("\nRAG工作流程：")
    print("""
    用户问题
        ↓
    [1. 向量化查询]
        ↓
    [2. 向量检索] → 从向量数据库获取Top-K相关文档
        ↓
    [3. 重排序] → 精细化排序（可选）
        ↓
    [4. 构建上下文] → 将检索到的文档拼接
        ↓
    [5. LLM生成] → 基于上下文回答问题
        ↓
    答案返回给用户
    """)

    print("\n关键优化点：")
    print("  1. 文档分块：chunk_size=512-1024, overlap=50-100")
    print("  2. Top-K选择：k=3-10（权衡精度和成本）")
    print("  3. 重排序：使用交叉编码器提升精度")
    print("  4. 上下文窗口：不超过LLM最大token数的70%")


# ============================================================================
# 第二部分：文档分块器
# ============================================================================


@dataclass
class DocumentChunk:
    """文档块

    为什么需要分块？
    - 长文档超过向量模型最大输入长度（512-8192 tokens）
    - 更小的块提供更精确的检索
    - 减少无关信息干扰
    """

    content: str
    chunk_id: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: np.ndarray | None = None


class DocumentChunker:
    """文档分块器

    策略：
    - 固定大小分块（简单）
    - 句子边界分块（更好）
    - 语义分块（最好但复杂）
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """初始化分块器

        Args:
            chunk_size: 每块的字符数（大约）
            overlap: 块之间的重叠字符数（保持上下文连贯性）
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, source: str = "unknown") -> list[DocumentChunk]:
        """将文本分块

        Args:
            text: 输入文本
            source: 文档来源

        Returns:
            文档块列表
        """
        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(text):
            # 确定块结束位置
            end = start + self.chunk_size

            # 如果不是最后一块，尝试在句号处切分（更自然）
            if end < len(text):
                # 在窗口内查找最后一个句号
                last_period = text.rfind("。", start, end)
                if last_period != -1 and last_period > start:
                    end = last_period + 1

            # 提取块内容
            chunk_content = text[start:end].strip()

            if chunk_content:
                chunk = DocumentChunk(
                    content=chunk_content,
                    chunk_id=f"{source}_chunk_{chunk_idx}",
                    source=source,
                    metadata={
                        "start_pos": start,
                        "end_pos": end,
                        "chunk_index": chunk_idx,
                    },
                )
                chunks.append(chunk)
                chunk_idx += 1

            # 移动到下一块（考虑重叠）
            start = end - self.overlap

        return chunks


# ============================================================================
# 第三部分：向量数据库（简化版）
# ============================================================================


class SimpleVectorDB:
    """简单的向量数据库

    真实场景使用：
    - Qdrant（推荐）
    - Pinecone
    - Weaviate
    - Milvus
    - Chroma

    这里实现教学版本
    """

    def __init__(self, dimension: int = 128):
        """初始化向量数据库"""
        self.dimension = dimension
        self.chunks: list[DocumentChunk] = []
        self.vectors: np.ndarray | None = None

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """添加文档块到数据库

        Args:
            chunks: 已向量化的文档块列表
        """
        # 验证所有块都有向量
        for chunk in chunks:
            if chunk.vector is None:
                raise ValueError(f"块 {chunk.chunk_id} 缺少向量")

        # 添加到存储
        self.chunks.extend(chunks)

        # 构建向量矩阵（用于高效检索）
        all_vectors = [chunk.vector for chunk in self.chunks]
        self.vectors = np.array(all_vectors)

        print(f"✅ 向量数据库：已添加 {len(chunks)} 个块")
        print(f"   总块数: {len(self.chunks)}")
        print(f"   向量维度: {self.dimension}")
        print(f"   存储大小: {self.vectors.nbytes / 1024:.2f} KB")

    def search(self, query_vector: np.ndarray, top_k: int = 5, score_threshold: float = 0.3) -> list[tuple[DocumentChunk, float]]:
        """搜索相关文档块

        Args:
            query_vector: 查询向量
            top_k: 返回Top-K个结果
            score_threshold: 相似度阈值（过滤低分结果）

        Returns:
            [(文档块, 相似度分数), ...]
        """
        if self.vectors is None or len(self.chunks) == 0:
            return []

        # 计算相似度（向量化操作）
        similarities = np.dot(self.vectors, query_vector)
        similarities = np.clip(similarities, 0.0, 1.0)

        # 应用阈值过滤
        valid_indices = np.where(similarities >= score_threshold)[0]

        if len(valid_indices) == 0:
            return []

        # 获取Top-K
        filtered_similarities = similarities[valid_indices]
        top_k_in_filtered = min(top_k, len(valid_indices))
        top_indices_in_filtered = np.argsort(filtered_similarities)[::-1][:top_k_in_filtered]

        # 映射回原始索引
        top_indices = valid_indices[top_indices_in_filtered]

        # 构建结果
        results = [(self.chunks[idx], float(similarities[idx])) for idx in top_indices]

        return results


# ============================================================================
# 第四部分：RAG管道
# ============================================================================


class RAGPipeline:
    """完整的RAG管道

    组件：
    1. Chunker: 文档分块
    2. Embedder: 向量化（这里使用简化版本）
    3. VectorDB: 向量存储和检索
    4. LLM: 生成答案（这里模拟）
    """

    def __init__(self, chunk_size: int = 512, vector_dim: int = 128):
        """初始化RAG管道"""
        self.chunker = DocumentChunker(chunk_size=chunk_size)
        self.vector_db = SimpleVectorDB(dimension=vector_dim)
        self.vector_dim = vector_dim

    def _mock_embed(self, text: str) -> np.ndarray:
        """模拟向量化（教学用）

        真实场景使用：
        - OpenAI text-embedding-ada-002
        - HuggingFace sentence-transformers
        """
        # 使用文本哈希生成一致的随机向量
        seed = hash(text) % (2**32)
        np.random.seed(seed)
        vec = np.random.randn(self.vector_dim)
        return vec / np.linalg.norm(vec)

    def index_documents(self, documents: list[tuple[str, str]]) -> None:
        """索引文档

        Args:
            documents: [(文本, 来源), ...]
        """
        print("\n" + "=" * 70)
        print("步骤 1: 文档索引")
        print("=" * 70)

        all_chunks = []

        for text, source in documents:
            # 1. 分块
            chunks = self.chunker.chunk(text, source)
            print(f"  {source}: {len(chunks)} 个块")

            # 2. 向量化
            for chunk in chunks:
                chunk.vector = self._mock_embed(chunk.content)

            all_chunks.extend(chunks)

        # 3. 存储到向量数据库
        self.vector_db.add_chunks(all_chunks)

    def query(self, question: str, top_k: int = 3, verbose: bool = True) -> dict[str, Any]:
        """执行RAG查询

        Args:
            question: 用户问题
            top_k: 检索Top-K个文档块
            verbose: 是否打印详细信息

        Returns:
            包含检索结果和生成答案的字典
        """
        if verbose:
            print("\n" + "=" * 70)
            print(f"步骤 2: RAG查询 - '{question}'")
            print("=" * 70)

        # 1. 向量化查询
        query_vector = self._mock_embed(question)

        # 2. 检索相关文档
        retrieved = self.vector_db.search(query_vector, top_k=top_k)

        if verbose:
            print(f"\n检索到 {len(retrieved)} 个相关文档块：")
            for i, (chunk, score) in enumerate(retrieved, 1):
                print(f"  {i}. [{score:.4f}] {chunk.content[:60]}...")

        # 3. 构建上下文
        context = self._build_context(retrieved)

        # 4. 生成答案（这里模拟）
        answer = self._mock_generate(question, context)

        if verbose:
            print("\n生成的答案：")
            print(f"  {answer}")

        return {
            "question": question,
            "retrieved_chunks": retrieved,
            "context": context,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
        }

    def _build_context(self, retrieved: list[tuple[DocumentChunk, float]]) -> str:
        """构建上下文

        策略：
        - 将检索到的块拼接
        - 添加来源标注
        - 控制总长度
        """
        context_parts = []

        for i, (chunk, score) in enumerate(retrieved, 1):
            context_parts.append(f"[文档 {i} - 来源: {chunk.source} - 相关度: {score:.2f}]\n{chunk.content}\n")

        return "\n".join(context_parts)

    def _mock_generate(self, question: str, context: str) -> str:
        """模拟LLM生成（教学用）

        真实场景使用：
        - OpenAI GPT-4
        - Claude
        - 本地Llama

        提示词模板：
            基于以下上下文回答问题：
            {context}

            问题：{question}

            请基于上述上下文回答，如果上下文中没有相关信息，请说"根据提供的信息无法回答"。
        """
        # 这里返回一个说明性的模拟回复
        return (
            f"基于检索到的 {len(context.split('[文档')) - 1} 个文档块，"
            f"这是对问题 '{question}' 的回答。"
            f"（注：这是模拟回复，真实场景会调用LLM生成详细答案）"
        )


# ============================================================================
# 第五部分：完整演示
# ============================================================================


def main():
    """主演示函数"""

    # Part 1: 解释RAG架构
    explain_rag_architecture()

    # Part 2: 准备知识库文档
    print("\n" + "=" * 70)
    print("准备知识库")
    print("=" * 70)

    documents = [
        (
            "Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。"
            "Python设计哲学强调代码的可读性和简洁的语法。"
            "Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。"
            "Python拥有丰富的标准库和第三方库生态系统。",
            "python_intro.txt",
        ),
        (
            "机器学习是人工智能的一个分支，专注于构建能够从数据中学习的系统。"
            "机器学习算法可以分为监督学习、无监督学习和强化学习三大类。"
            "常见的机器学习应用包括图像识别、自然语言处理、推荐系统等。"
            "深度学习是机器学习的一个子领域，使用神经网络进行学习。",
            "ml_basics.txt",
        ),
        (
            "自然语言处理（NLP）是人工智能的一个重要分支，处理人类语言。"
            "NLP的核心任务包括文本分类、情感分析、命名实体识别、机器翻译等。"
            "现代NLP广泛使用Transformer模型，如BERT、GPT等。"
            "向量嵌入（Embedding）是NLP中的关键技术，用于表示文本的语义。",
            "nlp_intro.txt",
        ),
    ]

    # Part 3: 创建RAG管道并索引
    rag = RAGPipeline(chunk_size=200, vector_dim=128)
    rag.index_documents(documents)

    # Part 4: 执行多个查询
    queries = [
        "Python是什么时候发布的？",
        "什么是机器学习？",
        "NLP中使用哪些模型？",
    ]

    for query in queries:
        rag.query(query, top_k=3, verbose=True)

    # Part 5: 总结关键点
    print("\n" + "=" * 70)
    print("RAG系统关键要点总结")
    print("=" * 70)

    print("""
1. 文档分块（Chunking）：
   - chunk_size: 512-1024字符
   - overlap: 50-100字符（保持连贯性）
   - 在句子边界切分（更自然）

2. 向量化（Embedding）：
   - 使用预训练模型（OpenAI, HuggingFace）
   - 维度通常是768或1536
   - 同一模型用于索引和查询

3. 向量检索（Retrieval）：
   - Top-K: 通常3-10个
   - 阈值过滤: score >= 0.3-0.5
   - 考虑性能和成本

4. 上下文构建（Context）：
   - 拼接检索到的块
   - 添加来源标注
   - 控制总长度（不超过LLM上下文窗口的70%）

5. LLM生成（Generation）：
   - 使用结构化提示词
   - 明确告诉LLM基于上下文回答
   - 处理无法回答的情况

6. 优化技巧：
   - 重排序（Reranking）提升精度
   - 混合检索（向量+关键词）
   - 缓存常见查询
   - 异步处理提升吞吐
    """)


if __name__ == "__main__":
    main()
