"""DuckDB 分析模块（带连接池管理）。"""

from __future__ import annotations

from typing import TYPE_CHECKING

import duckdb

if TYPE_CHECKING:
    import pandas as pd


def source_summary(df: pd.DataFrame) -> pd.DataFrame:
    """按来源聚合统计（使用上下文管理器自动关闭连接）。"""
    with duckdb.connect() as conn:
        conn.register("pages", df)
        return conn.execute("""
            SELECT
                source,
                COUNT(*) AS pages,
                ROUND(AVG(word_count), 1) AS avg_words,
                SUM(CASE WHEN has_python THEN 1 ELSE 0 END) AS python_pages,
                SUM(CASE WHEN has_ai THEN 1 ELSE 0 END) AS ai_pages
            FROM pages
            GROUP BY source
            ORDER BY pages DESC, avg_words DESC
        """).df()


def top_pages(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """按词数排序返回 Top 页面（使用上下文管理器自动关闭连接）。"""
    with duckdb.connect() as conn:
        conn.register("pages", df)
        return conn.execute(
            """
            SELECT url, title, source, word_count
            FROM pages
            ORDER BY word_count DESC
            LIMIT ?
            """,
            (n,),
        ).df()
