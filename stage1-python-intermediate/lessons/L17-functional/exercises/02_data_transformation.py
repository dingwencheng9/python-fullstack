"""
L17: 函数式编程 - 数据转换练习

使用函数式编程实现数据转换。
"""

from functools import partial


def apply_discount(price: float, discount: float) -> float:
    """应用折扣"""
    return price * (1 - discount)


def with_tax(price: float, tax_rate: float) -> float:
    """添加税费"""
    return price * (1 + tax_rate)


def round_price(price: float, decimals: int = 2) -> float:
    """四舍五入价格"""
    multiplier = 10**decimals
    return round(price * multiplier) / multiplier


# 偏函数版本
apply_10_percent = partial(apply_discount, discount=0.10)
apply_20_percent = partial(apply_discount, discount=0.20)
with_sales_tax = partial(with_tax, tax_rate=0.08)
with_vat = partial(with_tax, tax_rate=0.20)


def calculate_final_price(price: float, discount: float, tax: float) -> float:
    """计算最终价格。

    先应用折扣，再计算税费，最后保留两位小数。
    """
    apply_discount_rate = partial(apply_discount, discount=discount)
    apply_tax_rate = partial(with_tax, tax_rate=tax)
    return round_price(apply_tax_rate(apply_discount_rate(price)))


# === 验证 ===

if __name__ == "__main__":
    # 测试折扣
    assert apply_10_percent(100) == 90.0
    assert apply_20_percent(100) == 80.0

    # 测试税费
    assert with_sales_tax(100) == 108.0
    assert with_vat(100) == 120.0

    # 测试最终价格
    final = calculate_final_price(100, 0.10, 0.08)
    assert final == 97.2  # 100 * 0.9 * 1.08

    print("✅ 所有测试通过！")
