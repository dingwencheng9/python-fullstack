"""

from __future__ import annotations

【骨架代码】特征工程 — 提取特征

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

import pandas as pd


def add_word_count(df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
    """添加词数特征 word_count

    按空格分词，计算词数
    """
    # TODO: 新增 word_count 列
    # ← 你的代码写在这里


def add_title_length(df: pd.DataFrame, title_column: str = "title") -> pd.DataFrame:
    """添加标题长度特征 title_length"""
    # TODO: 新增 title_length 列（字符数）
    # ← 你的代码写在这里


def add_domain(df: pd.DataFrame, url_column: str = "url") -> pd.DataFrame:
    """提取域名特征 domain"""
    # TODO: 使用 urlparse 提取 netloc 作为 domain
    # ← 你的代码写在这里


def add_fetch_date(df: pd.DataFrame, time_column: str = "fetch_time") -> pd.DataFrame:
    """添加抓取日期特征 fetch_date

    从 timestamp 转换为 YYYY-MM-DD 格式字符串
    """
    # TODO: 新增 fetch_date 列
    # ← 你的代码写在这里


def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """添加所有特征"""
    # TODO: 依次调用以上函数，返回添加特征后的 DataFrame
    # ← 你的代码写在这里
