"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L17: 函数式编程 - 数据转换测试
"""

import pytest


def test_apply_10_percent():
    """测试 10% 折扣"""
    result = data_transformation.apply_10_percent(100)
    assert result == 90.0


def test_apply_20_percent():
    """测试 20% 折扣"""
    result = data_transformation.apply_20_percent(100)
    assert result == 80.0


def test_with_sales_tax():
    """测试销售税"""
    result = data_transformation.with_sales_tax(100)
    assert result == 108.0


def test_with_vat():
    """测试增值税"""
    result = data_transformation.with_vat(100)
    assert result == 120.0


def test_calculate_final_price():
    """测试最终价格计算"""
    # 100 * (1 - 0.10) * (1 + 0.08) = 100 * 0.9 * 1.08 = 97.2
    result = data_transformation.calculate_final_price(100, 0.10, 0.08)
    assert result == pytest.approx(97.2)


def test_calculate_final_price_no_discount():
    """测试无折扣最终价格"""
    # 100 * (1 - 0) * (1 + 0.08) = 108
    result = data_transformation.calculate_final_price(100, 0, 0.08)
    assert result == pytest.approx(108.0)


def test_calculate_final_price_no_tax():
    """测试无税最终价格"""
    # 100 * (1 - 0.20) * (1 + 0) = 80
    result = data_transformation.calculate_final_price(100, 0.20, 0)
    assert result == pytest.approx(80.0)


def test_round_price():
    """测试价格四舍五入"""
    result = data_transformation.round_price(1.234, 2)
    assert result == 1.23

    result = data_transformation.round_price(1.235, 2)
    assert result == 1.24
