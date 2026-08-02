"""

from __future__ import annotations

【骨架代码】数据读取 — 读取爬虫导出数据

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_json(input_path: str | Path) -> pd.DataFrame:
    """读取爬虫导出的 JSON 文件

    JSON 格式示例：
    [
      {
        "url": "...",
        "title": "...",
        "text": "...",
        "status_code": 200,
        "fetch_time": 1234567890
      },
      ...
    ]

    返回 DataFrame
    """
    # TODO: 读取 JSON 文件，转换为 DataFrame
    # ← 你的代码写在这里


def read_csv(input_path: str | Path) -> pd.DataFrame:
    """读取 CSV 文件"""
    # TODO: 用 pandas 读取 CSV
    # ← 你的代码写在这里


def read_from_project1(input_path: str | Path) -> pd.DataFrame:
    """适配项目 1 导出格式，读取并标准化"""
    # TODO: 读取后检查必要列是否存在
    # 必要列: url, title, text, status_code, fetch_time
    # ← 你的代码写在这里
