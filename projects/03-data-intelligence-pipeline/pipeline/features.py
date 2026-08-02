"""特征工程模块。"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def count_words(text: str) -> int:
    """中英文混合粗略词数。"""
    tokens = re.findall(r"[A-Za-z0-9_]+|[一-鿿]", text)
    return len(tokens)


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """添加文本特征。"""
    result = df.copy()
    result["title_len"] = result["title"].str.len()
    result["text_len"] = result["text"].str.len()
    result["word_count"] = result["text"].map(count_words)
    result["has_python"] = result["text"].str.contains("Python", case=False, na=False)
    result["has_ai"] = result["text"].str.contains("AI|Agent|LLM", case=False, na=False, regex=True)
    return result
