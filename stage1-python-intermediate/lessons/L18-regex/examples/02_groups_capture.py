"""L16 示例 2：分组、命名分组、非捕获组与反向引用。"""

from __future__ import annotations

import re


def demo_capture_groups() -> None:
    """演示普通捕获组。"""
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", "日期: 2026-06-11")
    print("=== 普通分组 ===")
    if match:
        print(match.group(0))
        print(match.group(1), match.group(2), match.group(3))


def demo_named_groups() -> None:
    """演示命名分组和 groupdict。"""
    pattern = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})\s+" r"(?P<level>[A-Z]+)\s+" r"(?P<message>.+)")
    match = pattern.fullmatch("2026-06-11 INFO service started")
    print("\n=== 命名分组 ===")
    if match:
        print(match.group("level"))
        print(match.groupdict())


def demo_non_capture_groups() -> None:
    """演示非捕获组避免 findall 只返回组内容。"""
    text = "http://example.com https://python.org ftp://legacy.local"
    urls = re.findall(r"(?:https?)://[\w.-]+", text)
    print("\n=== 非捕获组 ===")
    print(urls)


def demo_backreferences() -> None:
    """演示数字和命名反向引用。"""
    duplicated = re.findall(r"\b(\w+)\s+\1\b", "this is is a test test")
    quote_pattern = re.compile(r"(?P<quote>['\"])(?P<value>.*?)(?P=quote)")
    values = [match.group("value") for match in quote_pattern.finditer("name='Alice' title=\"Dev\"")]
    print("\n=== 反向引用 ===")
    print(duplicated)
    print(values)


def main() -> None:
    """运行全部分组示例。"""
    demo_capture_groups()
    demo_named_groups()
    demo_non_capture_groups()
    demo_backreferences()


if __name__ == "__main__":
    main()
