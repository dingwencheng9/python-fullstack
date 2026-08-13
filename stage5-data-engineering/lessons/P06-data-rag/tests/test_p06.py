"""P06 测试文件"""

from __future__ import annotations

import pytest
import pandas as pd
import numpy as np


class TestDataPipeline:
    """测试数据管道"""

    def setup_method(self):
        """每个测试前执行"""
        self.df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'B', 'C'],
            'amount': [100.0, 200.0, 150.0, 300.0, 250.0],
            'quantity': [1, 2, 1, 3, 2]
        })

    def test_data_types(self):
        """测试数据类型"""
        assert self.df['amount'].dtype == np.float64
        # pandas 3.0+ 使用 StringDtype，兼容旧版本
        is_str = pd.api.types.is_string_dtype(self.df['category']) or self.df['category'].dtype == object
        assert is_str

    def test_aggregation(self):
        """测试聚合"""
        result = self.df.groupby('category')['amount'].sum()
        assert result['A'] == 250.0
        assert result['B'] == 500.0


class TestEmbedding:
    """测试 Embedding 实现"""

    def test_simple_embedding(self):
        """测试简单 Embedding"""
        import numpy as np

        def simple_embedding(text: str, dim: int = 64) -> np.ndarray:
            words = set(text.lower().split())
            vec = np.zeros(dim)
            keywords = ["data", "analysis", "report", "sales", "revenue"]
            for i, kw in enumerate(keywords):
                if kw in words:
                    vec[i] = 1.0
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            return vec

        vec = simple_embedding("sales data")
        assert vec.shape == (64,)
        assert abs(np.linalg.norm(vec) - 1.0) < 0.01

    def test_cosine_similarity(self):
        """测试余弦相似度"""
        a = np.array([1.0, 0.0])
        b = np.array([1.0, 0.0])  # noqa: F841
        c = np.array([0.0, 1.0])

        # 相同向量
        sim_aa = np.dot(a, a) / (np.linalg.norm(a) * np.linalg.norm(a))
        assert abs(sim_aa - 1.0) < 0.01

        # 正交向量
        sim_ac = np.dot(a, c) / (np.linalg.norm(a) * np.linalg.norm(c))
        assert abs(sim_ac) < 0.01


class TestDuckDB:
    """测试 DuckDB 查询"""

    def setup_method(self):
        """每个测试前执行"""
        try:
            import duckdb
            self.has_duckdb = True
            self.con = duckdb.connect(":memory:")
        except ImportError:
            self.has_duckdb = False

    def test_duckdb_basic(self):
        """测试 DuckDB 基本功能"""
        if not self.has_duckdb:
            pytest.skip("DuckDB not installed")

        self.con.execute("CREATE TABLE test AS SELECT i AS id FROM range(10) t(i)")
        result = self.con.execute("SELECT COUNT(*) FROM test").fetchone()
        assert result[0] == 10


class TestVisualization:
    """测试可视化"""

    def test_matplotlib_available(self):
        """测试 Matplotlib 可用性"""
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 2, 3])
            plt.close(fig)
            assert True
        except ImportError:
            pytest.skip("Matplotlib not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
