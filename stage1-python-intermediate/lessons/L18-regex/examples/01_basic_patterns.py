"""L16 示例 1：字符类、量词与锚点。"""

from __future__ import annotations

import re


def demo_character_classes() -> None:
    """演示常用字符类。"""
    text = "订单 A100 金额 299 元，订单 B205 金额 88 元"
    print("=== 字符类 ===")
    print(re.findall(r"[A-Z]\d{3}", text))
    print(re.findall(r"\d+", text))
    print(re.findall(r"[^，]+", text))


def demo_quantifiers() -> None:
    """演示常用量词。"""
    text = "go gogle google gooogle color colour v1 v12 v123 v1234"
    print("\n=== 量词 ===")
    print(re.findall(r"go*gle", text))
    print(re.findall(r"go+gle", text))
    print(re.findall(r"colou?r", text))
    print(re.findall(r"v\d{1,3}\b", text))


def demo_anchors() -> None:
    """演示开头、结尾和单词边界。"""
    lines = "INFO start\nWARN slow\nERROR failed"
    print("\n=== 锚点 ===")
    print(re.findall(r"^\w+", lines, re.MULTILINE))
    print(bool(re.fullmatch(r"ERROR:\s+.+", "ERROR: disk full")))
    print(re.findall(r"\bcat\b", "cat scatter catalog cat"))


def main() -> None:
    """运行全部基础示例。"""
    demo_character_classes()
    demo_quantifiers()
    demo_anchors()


if __name__ == "__main__":
    main()
