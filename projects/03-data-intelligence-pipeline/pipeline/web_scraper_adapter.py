"""项目1 Web Scraper 数据适配器。

from __future__ import annotations

直接兼容项目1导出的JSON/CSV格式，无缝接入数据流水线。
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

from pipeline.ingest import load_data

if TYPE_CHECKING:
    from collections.abc import Callable


def adapt_web_scraper_data(df: pd.DataFrame) -> pd.DataFrame:
    """适配Web Scraper输出格式到数据流水线格式。

    字段映射:
        url -> url
        title -> title
        text -> content
        word_count -> word_count
        extracted_date -> date
        fetch_time -> fetch_seconds
    """
    # 字段重命名和标准化
    df = df.rename(
        columns={"text": "content", "extracted_date": "date", "fetch_time": "fetch_seconds"}
    )

    # 新增衍生字段
    df["domain"] = df["url"].str.extract(r"https?://([^/]+)")  # 提取域名
    df["is_article"] = df["word_count"] > 300  # 是否为长文章
    df["crawled_at"] = pd.Timestamp.now()  # 采集时间戳

    return df


def load_web_scraper_data(path: str | Path) -> pd.DataFrame:
    """直接加载并适配项目1的导出数据。

    使用示例:
        from pipeline.web_scraper_adapter import load_web_scraper_data
        df = load_web_scraper_data("../01-web-scraper/results.json")
    """
    df = load_data(path)
    return adapt_web_scraper_data(df)


def create_web_scraper_pipeline(
    output_dir: str | Path = "reports",
) -> Callable[[str | Path], Path]:
    """创建处理项目1数据的完整流水线。

    返回:
        一个函数，输入项目1的导出文件路径，输出报告路径
    """
    from pipeline.clean import clean_dataframe
    from pipeline.features import add_text_features
    from pipeline.report import generate_markdown_report

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    def process_file(input_path: str | Path) -> Path:
        # 加载+适配（结果暂不直接使用，但保留以触发数据校验副作用）
        _ = add_text_features(clean_dataframe(load_web_scraper_data(input_path)))

        # 生成报告
        input_name = Path(input_path).stem
        report_path = output_path / f"{input_name}_report.md"
        return generate_markdown_report(input_path, report_path)

    return process_file


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("用法: python -m pipeline.web_scraper_adapter input.json output_dir/")
        sys.exit(1)

    process_func = create_web_scraper_pipeline(sys.argv[2])
    report = process_func(sys.argv[1])
    print(f"✅ 报告生成完成: {report}")
