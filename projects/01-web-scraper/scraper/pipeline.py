"""数据管道 — 清洗 + 存储 + 分析"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import duckdb

if TYPE_CHECKING:
    from pathlib import Path

    import pandas as pd

    from scraper.collector import PageResult


def clean_text(text: str) -> str:
    """清洗文本：空白规范化 + 去除非ASCII字符"""
    return re.sub(r"\s+", " ", text).strip()


def extract_date(text: str) -> str | None:
    """从文本中提取日期（YYYY-MM-DD）"""
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    return match.group(0) if match else None


class Pipeline:
    """数据处理管道：存储 → 清洗 → 分析"""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = duckdb.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                url VARCHAR PRIMARY KEY,
                title VARCHAR,
                text VARCHAR,
                status_code INTEGER,
                fetch_time DOUBLE,
                word_count INTEGER,
                extracted_date VARCHAR
            )
        """)

    def save(self, result: PageResult) -> None:
        """存储采集结果"""
        text = clean_text(result.text)
        date = extract_date(text)
        self.conn.execute(
            """
            INSERT OR REPLACE INTO pages
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                result.url,
                result.title,
                text,
                result.status_code,
                result.fetch_time,
                len(text.split()),
                date,
            ),
        )

    def save_batch(self, results: list[PageResult]) -> None:
        """批量存储"""
        for r in results:
            self.save(r)

    def analyze(self) -> pd.DataFrame:
        """分析采集数据"""
        return self.conn.execute("""
            SELECT
                COUNT(*) AS total_pages,
                ROUND(AVG(word_count), 0) AS avg_word_count,
                ROUND(AVG(fetch_time), 3) AS avg_fetch_time,
                COUNT(DISTINCT extracted_date) AS unique_dates
            FROM pages
        """).df()

    def top_sources(self, n: int = 10) -> pd.DataFrame:
        """按域名统计采集量"""
        return self.conn.execute(
            """
            SELECT
                url,
                title,
                word_count,
                fetch_time,
                extracted_date
            FROM pages
            ORDER BY word_count DESC
            LIMIT ?
            """,
            (n,),
        ).df()

    def export_json(self, output: str | Path) -> None:
        """导出为 JSON"""
        df = self.conn.execute("SELECT * FROM pages").df()
        df.to_json(output, orient="records", force_ascii=False)

    def export_csv(self, output: str | Path) -> None:
        """导出为 CSV"""
        df = self.conn.execute("SELECT * FROM pages").df()
        df.to_csv(output, index=False)
