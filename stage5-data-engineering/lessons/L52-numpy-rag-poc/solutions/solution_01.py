"""练习 1: 实现余弦相似度计算

本练习要求实现一个纯 NumPy 的余弦相似度计算函数，
这是向量检索的基础算法。

学习目标：
- 掌握 NumPy 向量操作
- 理解余弦相似度原理
- 避免除零错误
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    计算两个向量的余弦相似度

    Args:
        a: 向量 A
        b: 向量 B

    Returns:
        余弦相似度，范围 [-1, 1]
        1 表示完全相同，0 表示正交，-1 表示完全相反

    示例:
        >>> a = np.array([1, 0])
        >>> b = np.array([1, 0])
        >>> cosine_similarity(a, b)
        1.0
    """
    # TODO: 实现此函数
    raise NotImplementedError("请实现余弦相似度计算")


def batch_cosine_similarity(query: np.ndarray, docs: np.ndarray) -> np.ndarray:
    """
    批量计算查询向量与文档向量的余弦相似度

    Args:
        query: 查询向量，形状 (embedding_dim,)
        docs: 文档向量矩阵，形状 (n_docs, embedding_dim)

    Returns:
        相似度数组，形状 (n_docs,)

    示例:
        >>> query = np.array([1, 0, 0])
        >>> docs = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> batch_cosine_similarity(query, docs)
        array([1., 0., 0.])
    """
    # TODO: 使用矩阵运算实现批量计算（避免循环）
    raise NotImplementedError("请实现批量余弦相似度计算")
