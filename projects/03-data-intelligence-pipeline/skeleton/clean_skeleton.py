"""

from __future__ import annotations

【骨架代码】数据清洗 — 清洗规范化

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

import pandas as pd


def clean_text(text: str) -> str:
    """清洗文本

    步骤：
    1. 多个空白字符替换为单个空格
    2. 去掉前后空白
    3. （可选）去除非 ASCII 字符
    """
    # TODO: 实现文本清洗
    # ← 你的代码写在这里


def drop_missing(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """删除缺失必要列的行"""
    # TODO: 删除指定列中有缺失值的行
    # ← 你的代码写在这里


def drop_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """删除重复行"""
    # TODO: 删除重复行
    # ← 你的代码写在这里


def filter_status_ok(df: pd.DataFrame) -> pd.DataFrame:
    """只保留状态码为 200 的行"""
    # TODO: 过滤
    # ← 你的代码写在这里


def clean_all(df: pd.DataFrame) -> pd.DataFrame:
    """完整清洗流程

    步骤：
    1. 清洗 text 列
    2. 删除缺失值
    3. 删除重复（按 url 去重）
    4. 只保留 200 状态
    """
    # TODO: 组合以上步骤，返回清洗后的 DataFrame
    # ← 你的代码写在这里
