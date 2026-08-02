"""L53 测试套件

测试 DuckDB OLAP 功能。
"""

from __future__ import annotations

import pytest


def test_duckdb_available() -> None:
    """测试 DuckDB 是否可用"""
    try:
        import duckdb

        assert duckdb is not None
    except ImportError:
        pytest.skip("DuckDB 未安装，跳过测试")


class TestDuckDBBasics:
    """测试 DuckDB 基础功能"""

    def test_connect_memory(self) -> None:
        """测试内存连接"""
        import duckdb

        con = duckdb.connect(":memory:")
        assert con is not None
        con.close()

    def test_create_table(self) -> None:
        """测试创建表"""
        import duckdb

        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")
        result = con.execute("SELECT * FROM test").fetchdf()
        assert len(result) == 0
        con.close()

    def test_insert_and_select(self) -> None:
        """测试插入和查询"""
        import duckdb

        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE test (id INTEGER, value INTEGER)")
        con.execute("INSERT INTO test VALUES (1, 100), (2, 200)")
        result = con.execute("SELECT SUM(value) FROM test").fetchone()[0]
        assert result == 300
        con.close()


class TestSQLExtensions:
    """测试 SQL 扩展"""

    def test_sample_clause(self) -> None:
        """测试 USING SAMPLE 子句"""
        import duckdb

        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE test AS SELECT i FROM generate_series(1, 1000) t(i)")
        result = con.execute("SELECT COUNT(*) FROM test USING SAMPLE 100 ROWS").fetchone()[0]
        assert result == 100
        con.close()

    def test_window_functions(self) -> None:
        """测试窗口函数"""
        import duckdb

        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE sales (product VARCHAR, amount INTEGER)")
        con.execute("INSERT INTO sales VALUES ('A', 100), ('A', 200), ('B', 150)")
        result = con.execute("""
            SELECT product, amount,
                   SUM(amount) OVER (PARTITION BY product) as total
            FROM sales
        """).fetchdf()
        assert result.loc[result["product"] == "A", "total"].iloc[0] == 300
        con.close()

    def test_lateral_join(self) -> None:
        """测试 LATERAL JOIN"""
        import duckdb

        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE t1 (id INTEGER, val INTEGER)")
        con.execute("CREATE TABLE t2 (id INTEGER, val2 INTEGER)")
        con.execute("INSERT INTO t1 VALUES (1, 10), (2, 20)")
        con.execute("INSERT INTO t2 VALUES (1, 100), (1, 200)")
        result = con.execute("""
            SELECT t1.id, t1.val, t2.val2
            FROM t1, LATERAL (SELECT val2 FROM t2 WHERE t2.id = t1.id LIMIT 1) t2
        """).fetchdf()
        # LATERAL 返回每行一条匹配记录
        assert len(result) >= 1
        assert result.loc[result["id"] == 1, "val2"].iloc[0] in [100, 200]
        con.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
