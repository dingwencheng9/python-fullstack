# ruff: noqa
# 骨架代码：学生填空用教学模板

"""

from __future__ import annotations

【骨架代码】数据分析 — DuckDB 聚合分析

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

import duckdb
import pandas as pd


def analyze_statistics(conn: duckdb.DuckDBPyConnection, table_name: str = "pages") -> pd.DataFrame:
    """计算统计指标

    返回单行 DataFrame，包含：
    - total_pages: 总页数
    - avg_word_count: 平均词数（整数）
    - min_word_count: 最小词数
    - max_word_count: 最大词数
    - total_domains: 不同域名数量
    """
    # TODO: 写 SQL 查询，返回结果
    # 示例 SQL 框架：
    # SELECT
    #     COUNT(*) as total_pages,
    #     ROUND(AVG(word_count), 0) as avg_word_count,
    #     ...
    # FROM {table_name}
    # ← 你的代码写在这里


def domain_distribution(conn: duckdb.DuckDBPyConnection, table_name: str = "pages") -> pd.DataFrame:
    """按域名统计页数，降序排列"""
    # TODO: 统计每个域名的页数，按页数降序排列
    # 返回 domain, page_count 两列
    # ← 你的代码写在这里


def word_count_histogram(
    conn: duckdb.DuckDBPyConnection, table_name: str = "pages"
) -> pd.DataFrame:
    """词数分布直方图"""
    # TODO: 按词数区间分组统计
    # ← 你的代码写在这里
