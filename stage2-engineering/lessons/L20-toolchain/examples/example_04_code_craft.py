"""L18 示例 4: Python 工匠 — 可维护性重构示例"""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    """订单行。"""

    sku: str
    price: float
    quantity: int


def parse_order_lines(text: str) -> list[OrderLine]:
    """从 JSON 文本解析订单行。"""
    try:
        raw_items = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("订单 JSON 格式无效") from exc

    return [
        OrderLine(
            sku=str(item["sku"]),
            price=float(item["price"]),
            quantity=int(item["quantity"]),
        )
        for item in raw_items
    ]


def calculate_subtotal(lines: list[OrderLine]) -> float:
    """计算未折扣小计。"""
    return sum(line.price * line.quantity for line in lines)


def apply_discount(subtotal: float, discount_rate: float) -> float:
    """应用折扣。"""
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate 必须在 0~1 之间")
    return subtotal * (1 - discount_rate)


def calculate_order_total(text: str, discount_rate: float = 0.0) -> float:
    """端到端计算订单总价。"""
    lines = parse_order_lines(text)
    subtotal = calculate_subtotal(lines)
    return round(apply_discount(subtotal, discount_rate), 2)


if __name__ == "__main__":
    sample = '[{"sku":"A","price":10,"quantity":2}]'
    print(calculate_order_total(sample, discount_rate=0.1))
