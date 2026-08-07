"""练习 3 参考答案：分析响应状态码。"""

from __future__ import annotations

import re


def summarize_status(lines: list[str]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for line in lines:
        match = re.search(r"HTTP/\d\.\d\s+(\d{3})", line)
        if match:
            code = int(match.group(1))
            counts[code] = counts.get(code, 0) + 1
    return counts
