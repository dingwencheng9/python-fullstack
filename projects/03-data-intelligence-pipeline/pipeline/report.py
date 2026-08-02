"""报告生成模块。"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from pipeline.analyze import source_summary, top_pages
from pipeline.clean import clean_dataframe
from pipeline.features import add_text_features
from pipeline.ingest import load_data


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """不依赖 tabulate 的简易 Markdown 表格渲染。"""
    if df.empty:
        return "_(无数据)_"
    columns = list(df.columns)
    header = "| " + " | ".join(map(str, columns)) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    rows = ["| " + " | ".join(str(row[col]) for col in columns) + " |" for _, row in df.iterrows()]
    return "\n".join([header, sep, *rows])


def generate_markdown_report(input_path: str | Path, output_path: str | Path) -> Path:
    """生成 Markdown 报告。"""
    df = add_text_features(clean_dataframe(load_data(input_path)))
    summary = source_summary(df)
    top = top_pages(df, n=5)

    lines = [
        "# 数据智能流水线报告",
        "",
        f"总页面数: {len(df)}",
        f"总词数: {int(df['word_count'].sum())}",
        "",
        "## 来源统计",
        dataframe_to_markdown(summary),
        "",
        "## Top 页面",
        dataframe_to_markdown(top),
        "",
    ]

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("用法: python -m pipeline.report input.json output.md")
    generate_markdown_report(sys.argv[1], sys.argv[2])
