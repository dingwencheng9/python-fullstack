"""

from __future__ import annotations

【骨架代码】报告生成 — 生成 Markdown/HTML 报告

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def generate_markdown_report(
    stats: pd.DataFrame,
    domain_dist: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """生成 Markdown 分析报告

    报告包含：
    1. 标题
    2. 汇总统计表格
    3. 域名分布表格
    4. （可选）图表链接
    """
    # TODO:
    # 1. 读取统计数据
    # 2. 格式化表格
    # 3. 写入 Markdown 文件
    # ← 你的代码写在这里


def generate_html_report(
    stats: pd.DataFrame,
    domain_dist: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """生成 HTML 报告（可选进阶）"""
    # TODO: 转换 Markdown 为 HTML 或者用模板生成
    # ← 你的代码写在这里
