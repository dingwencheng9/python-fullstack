"""练习 4 参考答案: 可读性重构。"""

from __future__ import annotations

from pathlib import Path


def parse_lines(text: str) -> list[list[str]]:
    """解析 CSV 文本为行列表。"""
    return [line.split(",") for line in text.splitlines() if line.strip()]


def calculate_total(rows: list[list[str]]) -> float:
    """计算第二列总和。"""
    return sum(float(row[1]) for row in rows)


def load_and_calculate(path: str) -> float:
    """读取文件并计算第二列总和。"""
    text = Path(path).read_text()
    rows = parse_lines(text)
    return calculate_total(rows)
