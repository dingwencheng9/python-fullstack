"""P06: OLAP 查询模块"""

import duckdb
from pandas import DataFrame


class OLAPQuery:
    """OLAP 查询引擎"""

    def __init__(self, config=None):
        self.config = config
        self.conn = duckdb.connect(config.duckdb_path if config else ":memory:")

    def aggregate(self, df: DataFrame, group_by: list[str], agg_col: str, agg_func: str = "sum") -> DataFrame:
        """聚合查询"""
        self.conn.execute("CREATE TABLE IF NOT EXISTS data AS SELECT * FROM df")
        result = self.conn.execute(
            f"SELECT {', '.join(group_by)}, {agg_func}({agg_col}) as result FROM data GROUP BY {', '.join(group_by)}"
        ).fetchdf()
        return result

    def close(self):
        """关闭连接"""
        self.conn.close()
