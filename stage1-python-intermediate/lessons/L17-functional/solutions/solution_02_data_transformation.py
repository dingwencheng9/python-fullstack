"""
L15: 函数式编程 - 数据转换练习解答

使用偏函数组合实现数据转换。
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
    """计算最终价格"""
    discounted = partial(apply_discount, discount=discount)
    taxed = partial(with_tax, tax_rate=tax)
    return taxed(discounted(price))
