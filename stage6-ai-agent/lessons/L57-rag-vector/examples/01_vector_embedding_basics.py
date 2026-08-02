"""

from __future__ import annotations

示例 1: 向量嵌入基础 - 从文本到向量的完整流程

教学目标：
1. 理解文本向量化的原理
2. 掌握向量维度和语义相似度
3. 实现简单的语义检索
4. 理解余弦相似度计算

核心技术：
- 文本预处理和分词
- 向量嵌入（Embedding）
- 余弦相似度（Cosine Similarity）
- NumPy向量化操作

运行方式：
    python examples/01_vector_embedding_basics.py
"""

from __future__ import annotations

import numpy as np

# ============================================================================
# 第一部分：理解向量嵌入的本质
# ============================================================================


def demonstrate_vector_concept():
    """演示向量嵌入的核心概念

    什么是向量嵌入？
    - 将文本（离散符号）转换为数值向量（连续空间）
    - 语义相似的文本在向量空间中距离更近
    - 向量维度通常是128、256、512、768、1536等

    为什么需要向量嵌入？
    - 计算机无法直接理解文本
    - 需要数值表示才能进行数学运算
    - 向量可以捕捉语义信息
    """
    print("=" * 70)
    print("Part 1: 向量嵌入的核心概念")
    print("=" * 70)

    # 示例：三个简单的词向量（3维，方便可视化）
    # 在真实场景中，维度通常是768或1536
    word_vectors = {
        "国王": np.array([0.9, 0.1, 0.0]),  # 性别：男性，权力：高
        "王后": np.array([0.1, 0.9, 0.0]),  # 性别：女性，权力：高
        "男人": np.array([0.8, 0.2, 0.0]),  # 性别：男性，权力：低
        "女人": np.array([0.2, 0.8, 0.0]),  # 性别：女性，权力：低
    }

    print("\n词向量表示（3维简化版）：")
    for word, vec in word_vectors.items():
        print(f"  {word:4s}: {vec}")

    # 向量运算的语义含义
    # 经典示例：国王 - 男人 + 女人 ≈ 王后
    result = word_vectors["国王"] - word_vectors["男人"] + word_vectors["女人"]
    print("\n向量运算示例：")
    print(f"  国王 - 男人 + 女人 = {result}")
    print(f"  与'王后'的向量：{word_vectors['王后']}")
    print("  (非常接近！这就是向量嵌入的魅力)")


# ============================================================================
# 第二部分：实现简单的文本向量化器
# ============================================================================


class SimpleTextVectorizer:
    """简单的文本向量化器（教学用）

    真实场景使用：
    - OpenAI text-embedding-ada-002
    - HuggingFace sentence-transformers
    - Google BERT/T5

    这里为了教学，实现一个简化版本
    """

    def __init__(self, dimension: int = 128):
        """初始化向量化器

        Args:
            dimension: 向量维度（通常是2的幂次，如128、256、512）
        """
        self.dimension = dimension
        # 词汇表：将每个词映射到一个唯一的向量
        # 真实模型会通过神经网络训练这些向量
        self.vocab: dict[str, np.ndarray] = {}

    def _get_or_create_vector(self, word: str) -> np.ndarray:
        """获取或创建词向量

        真实场景：
        - 通过训练好的神经网络生成
        - 这里简化为随机向量（但同一个词始终返回相同向量）

        Args:
            word: 单词

        Returns:
            词向量（归一化后）
        """
        if word not in self.vocab:
            # 使用词的哈希值作为随机种子，确保相同的词得到相同的向量
            seed = hash(word) % (2**32)
            np.random.seed(seed)
            # 生成随机向量并归一化（L2范数=1）
            vec = np.random.randn(self.dimension)
            vec = vec / np.linalg.norm(vec)  # 归一化
            self.vocab[word] = vec

        return self.vocab[word]

    def encode(self, text: str) -> np.ndarray:
        """将文本编码为向量

        策略：对所有词向量求平均（Mean Pooling）
        真实场景还会使用：
        - CLS token (BERT)
        - Weighted average
        - Max pooling

        Args:
            text: 输入文本

        Returns:
            文本向量（归一化后）
        """
        # 简单分词（按空格）
        words = text.lower().split()

        if not words:
            return np.zeros(self.dimension)

        # 获取所有词向量
        word_vecs = [self._get_or_create_vector(word) for word in words]

        # 平均池化
        text_vec = np.mean(word_vecs, axis=0)

        # 归一化（重要！用于计算余弦相似度）
        norm = np.linalg.norm(text_vec)
        if norm > 0:
            text_vec = text_vec / norm

        return text_vec


# ============================================================================
# 第三部分：实现余弦相似度计算
# ============================================================================


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """计算两个向量的余弦相似度

    公式：
        cos(θ) = (A · B) / (||A|| * ||B||)

    性质：
        - 范围：[-1, 1]
        - 1: 完全相同方向
        - 0: 垂直（无关）
        - -1: 完全相反方向

    为什么使用余弦相似度？
        - 只关注方向，不关注长度
        - 归一化后，点积 = 余弦相似度
        - 计算高效

    Args:
        vec1: 向量1（已归一化）
        vec2: 向量2（已归一化）

    Returns:
        相似度分数 [0, 1]
    """
    # 如果向量已归一化，余弦相似度 = 点积
    similarity = np.dot(vec1, vec2)

    # 限制范围在 [0, 1]（有时会有浮点误差导致略微超出）
    return max(0.0, min(1.0, similarity))


def batch_cosine_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
    """批量计算余弦相似度（向量化版本）

    性能对比：
    - for循环版本：O(n) 时间，慢100倍
    - 向量化版本：O(1) 时间（利用NumPy底层优化）

    Args:
        query_vec: 查询向量 (d,)
        doc_vecs: 文档向量矩阵 (n, d)

    Returns:
        相似度数组 (n,)
    """
    # 边界：空索引时直接返回空相似度，避免 (0,) 与 (d,) 形状不齐导致 ValueError
    if doc_vecs.size == 0:
        return np.empty((0,), dtype=np.float64)

    # 向量化点积：一次性计算所有相似度
    # 等价于：[np.dot(query_vec, doc_vec) for doc_vec in doc_vecs]
    # 但快100倍！
    similarities = np.dot(doc_vecs, query_vec)

    # 限制范围
    return np.clip(similarities, 0.0, 1.0)


# ============================================================================
# 第四部分：构建简单的语义搜索引擎
# ============================================================================


class SimpleSemanticSearch:
    """简单的语义搜索引擎

    工作流程：
    1. 初始化：创建向量化器
    2. 索引：将文档转换为向量并存储
    3. 搜索：将查询转换为向量，计算相似度，返回Top-K
    """

    def __init__(self, dimension: int = 128):
        """初始化搜索引擎"""
        self.vectorizer = SimpleTextVectorizer(dimension)
        self.documents: list[str] = []
        self.doc_vectors: np.ndarray | None = None

    def index(self, documents: list[str]) -> None:
        """索引文档

        Args:
            documents: 文档列表
        """
        self.documents = documents

        # 向量化所有文档
        doc_vecs = [self.vectorizer.encode(doc) for doc in documents]
        self.doc_vectors = np.array(doc_vecs)

        print(f"✅ 已索引 {len(documents)} 个文档")
        print(f"   向量维度: {self.vectorizer.dimension}")
        print(f"   存储空间: {self.doc_vectors.nbytes / 1024:.2f} KB")

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        """搜索相关文档

        Args:
            query: 查询文本
            top_k: 返回Top-K个结果

        Returns:
            [(文档, 相似度分数), ...]
        """
        if self.doc_vectors is None:
            raise ValueError("请先调用 index() 索引文档")

        # 1. 向量化查询
        query_vec = self.vectorizer.encode(query)

        # 2. 计算相似度（向量化操作，快！）
        similarities = batch_cosine_similarity(query_vec, self.doc_vectors)

        # 3. 获取Top-K
        # argsort返回从小到大的索引，[::-1]反转为从大到小
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # 4. 构建结果
        results = [(self.documents[idx], float(similarities[idx])) for idx in top_indices]

        return results


# ============================================================================
# 第五部分：完整演示
# ============================================================================


def main():
    """主演示函数"""

    # Part 1: 理解向量的概念
    demonstrate_vector_concept()

    print("\n" + "=" * 70)
    print("Part 2: 语义搜索演示")
    print("=" * 70)

    # 准备文档库
    documents = [
        "Python是一种高级编程语言",
        "机器学习需要大量的数据",
        "深度学习是机器学习的一个分支",
        "神经网络模拟人脑的工作方式",
        "自然语言处理用于理解人类语言",
        "计算机视觉处理图像和视频",
        "强化学习通过奖励来学习",
        "数据科学结合统计学和编程",
        "人工智能正在改变世界",
        "区块链是一种分布式账本技术",
    ]

    # 创建搜索引擎
    search_engine = SimpleSemanticSearch(dimension=128)

    # 索引文档
    print("\n1. 索引文档...")
    search_engine.index(documents)

    # 执行多个搜索
    queries = [
        "什么是机器学习？",
        "编程语言有哪些？",
        "AI技术的应用",
    ]

    print("\n2. 执行语义搜索...")
    for i, query in enumerate(queries, 1):
        print(f"\n查询 {i}: '{query}'")
        print("-" * 70)

        results = search_engine.search(query, top_k=3)

        for rank, (doc, score) in enumerate(results, 1):
            print(f"  {rank}. [相似度: {score:.4f}] {doc}")

    # 演示相似度的含义
    print("\n" + "=" * 70)
    print("Part 3: 相似度分数的含义")
    print("=" * 70)

    print("\n相似度范围：")
    print("  0.9 - 1.0  : 几乎完全相同（同义词、改写）")
    print("  0.7 - 0.9  : 高度相关（同一主题）")
    print("  0.5 - 0.7  : 相关（有关联）")
    print("  0.3 - 0.5  : 弱相关（部分重叠）")
    print("  0.0 - 0.3  : 不相关")

    print("\n💡 关键要点：")
    print("  1. 向量嵌入将文本转换为数值向量")
    print("  2. 语义相似的文本在向量空间中距离更近")
    print("  3. 余弦相似度衡量向量之间的角度（方向）")
    print("  4. 向量化操作（NumPy）比循环快100倍")
    print("  5. 真实场景使用OpenAI/HuggingFace的预训练模型")


if __name__ == "__main__":
    main()
