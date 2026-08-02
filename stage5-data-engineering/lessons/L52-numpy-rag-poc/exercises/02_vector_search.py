"""练习 2: 实现向量检索系统

本练习要求实现一个简单的向量检索系统，支持：
- 添加文档
- 向量检索
- 返回 Top-K 结果
"""

import numpy as np


class VectorSearch:
    """简单向量检索器"""

    def __init__(self, dim: int):
        """
        初始化检索器

        Args:
            dim: 向量维度
        """
        self.dim = dim
        self.documents: list[str] = []
        self.vectors: list[np.ndarray] = []

    def add(self, text: str, vector: np.ndarray) -> None:
        """
        添加文档

        Args:
            text: 文档文本
            vector: 文档向量，形状必须与 dim 一致
        """
        assert vector.shape == (self.dim,), f"向量维度必须为 {self.dim}"
        self.documents.append(text)
        self.vectors.append(vector)

    def search(self, query: np.ndarray, top_k: int = 5) -> list[tuple[str, float]]:
        """
        搜索最相似的文档

        Args:
            query: 查询向量
            top_k: 返回结果数量

        Returns:
            [(文档文本, 相似度), ...] 按相似度降序排列
        """
        assert query.shape == (self.dim,), f"查询向量维度必须为 {self.dim}"

        # TODO: 实现搜索逻辑
        # 1. 计算 query 与所有文档的余弦相似度
        # 2. 排序
        # 3. 返回 top_k
        raise NotImplementedError("请实现搜索功能")


# 测试代码
if __name__ == "__main__":
    # 创建检索器
    searcher = VectorSearch(dim=4)

    # 添加文档
    documents = [
        ("Python 编程语言", np.array([1.0, 0.8, 0.2, 0.1])),
        ("JavaScript 前端", np.array([0.2, 0.1, 0.9, 0.3])),
        ("机器学习 AI", np.array([0.3, 0.7, 0.4, 0.9])),
        ("Web 开发", np.array([0.1, 0.2, 0.8, 0.2])),
    ]

    for text, vec in documents:
        searcher.add(text, vec)

    # 搜索
    query = np.array([0.9, 0.7, 0.3, 0.2])  # Python 相关
    results = searcher.search(query, top_k=2)

    print("搜索结果:")
    for text, score in results:
        print(f"  [{score:.3f}] {text}")
