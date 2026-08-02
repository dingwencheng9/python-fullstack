#!/usr/bin/env python3
"""示例 1: NumPy 向量基础操作

演示 NumPy 的基本向量操作，包括：
- 向量创建
- 基本运算
- 范数计算
"""

import numpy as np


def main():
    # 创建向量
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([5, 4, 3, 2, 1])

    print("=" * 50)
    print("NumPy 向量基础")
    print("=" * 50)

    # 基本运算
    print(f"\n向量 a = {a}")
    print(f"向量 b = {b}")
    print(f"a + b = {a + b}")
    print(f"a * 2 = {a * 2}")
    print(f"a · b = {np.dot(a, b)}")  # 点积

    # 范数
    print(f"\n||a|| = {np.linalg.norm(a)}")  # L2 范数
    print(f"||b|| = {np.linalg.norm(b)}")

    # 余弦相似度
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    print(f"\ncos(a, b) = {cos_sim:.4f}")

    # 矩阵操作
    print("\n" + "=" * 50)
    print("矩阵操作")
    print("=" * 50)

    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\n矩阵:\n{matrix}")
    print(f"转置:\n{matrix.T}")
    print(f"求和: {matrix.sum()}")
    print(f"按行求和: {matrix.sum(axis=1)}")


if __name__ == "__main__":
    main()
