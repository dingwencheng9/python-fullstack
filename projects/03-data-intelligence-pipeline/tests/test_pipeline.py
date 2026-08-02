"""数据智能流水线项目测试。"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from pipeline.analyze import source_summary, top_pages
from pipeline.clean import clean_dataframe, extract_domain, normalize_text
from pipeline.features import add_text_features, count_words
from pipeline.ingest import load_data, load_json
from pipeline.report import generate_markdown_report

ROOT = Path(__file__).parent.parent
SAMPLE = ROOT / "data" / "sample.json"


def test_load_json():
    df = load_json(SAMPLE)
    assert len(df) == 3
    assert {"url", "title", "text"}.issubset(df.columns)


def test_load_data_dispatch():
    df = load_data(SAMPLE)
    assert len(df) == 3


def test_load_data_invalid_suffix(tmp_path):
    f = tmp_path / "bad.txt"
    f.write_text("x")
    with pytest.raises(ValueError, match="不支持的文件类型"):
        load_data(f)


def test_normalize_text():
    assert normalize_text(" hello   world \n ") == "hello world"


def test_extract_domain():
    assert extract_domain("https://docs.python.org/3/") == "docs.python.org"
    assert extract_domain("not-a-url") == "unknown"


def test_clean_dataframe():
    df = pd.DataFrame(
        {
            "url": ["https://a.com", "https://a.com", "https://b.com"],
            "title": [" A ", " A ", "B"],
            "text": ["hello", "hello", ""],
        }
    )
    cleaned = clean_dataframe(df)
    assert len(cleaned) == 1
    assert cleaned["title"].iloc[0] == "A"


def test_clean_dataframe_missing_required():
    with pytest.raises(ValueError, match="缺少必要字段"):
        clean_dataframe(pd.DataFrame({"url": ["x"]}))


def test_count_words():
    assert count_words("Python 全栈 AI") >= 4


def test_add_text_features():
    df = clean_dataframe(load_json(SAMPLE))
    enriched = add_text_features(df)
    for col in ("title_len", "text_len", "word_count", "has_python", "has_ai"):
        assert col in enriched.columns


def test_source_summary():
    df = add_text_features(clean_dataframe(load_json(SAMPLE)))
    summary = source_summary(df)
    assert "source" in summary.columns
    assert "pages" in summary.columns
    assert summary["pages"].sum() == len(df)


def test_top_pages():
    df = add_text_features(clean_dataframe(load_json(SAMPLE)))
    top = top_pages(df, n=2)
    assert len(top) == 2
    assert top["word_count"].iloc[0] >= top["word_count"].iloc[1]


def test_generate_markdown_report(tmp_path):
    out = tmp_path / "report.md"
    result = generate_markdown_report(SAMPLE, out)
    assert result.exists()
    content = result.read_text()
    assert "数据智能流水线报告" in content
    assert "来源统计" in content
    assert "Top 页面" in content


@pytest.mark.parametrize(
    ("text", "expected_min"),
    [
        ("FastAPI 是 Python Web 框架", 4),
        ("DuckDB OLAP database", 3),
        ("", 0),
    ],
)
def test_count_words_parametrized(text, expected_min):
    assert count_words(text) >= expected_min
