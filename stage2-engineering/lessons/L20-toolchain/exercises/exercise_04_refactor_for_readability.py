"""练习 4: 可读性重构

from __future__ import annotations

下面的函数把 I/O、解析、计算、异常处理混在一起。
请在不改变行为的前提下重构它：

1. 拆出 parse_lines(text)
2. 拆出 calculate_total(rows)
3. 保留 load_and_calculate(path) 作为边界函数
4. 为纯函数添加类型注解
"""

from __future__ import annotations


def load_and_calculate(path: str) -> float:
    """读取 CSV 文本并计算第二列总和。"""
    text = open(path).read()
    total = 0.0
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(",")
        total += float(parts[1])
    return total
