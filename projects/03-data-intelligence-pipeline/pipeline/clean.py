"""数据清洗模块。"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    import pandas as pd


def normalize_text(text: str) -> str:
    """规范化文本：空白压缩、去首尾空格。"""
    return re.sub(r"\s+", " ", str(text)).strip()


def extract_domain(url: str) -> str:
    """从 URL 提取域名。"""
    return urlparse(str(url)).netloc or "unknown"


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """清洗爬虫数据。"""
    required = {"url", "title", "text"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"缺少必要字段: {', '.join(sorted(missing))}")

    cleaned = df.copy()
    cleaned["url"] = cleaned["url"].astype(str).str.strip()
    cleaned["title"] = cleaned["title"].fillna("").map(normalize_text)
    cleaned["text"] = cleaned["text"].fillna("").map(normalize_text)
    cleaned["source"] = cleaned.get("source", cleaned["url"].map(extract_domain))
    cleaned["source"] = cleaned["source"].fillna(cleaned["url"].map(extract_domain))
    cleaned = cleaned.drop_duplicates(subset=["url"])
    cleaned = cleaned[cleaned["text"].str.len() > 0]
    return cleaned.reset_index(drop=True)
