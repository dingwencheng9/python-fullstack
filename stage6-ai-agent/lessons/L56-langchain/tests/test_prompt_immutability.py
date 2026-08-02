"""测试 PromptTemplate 状态不变性修复。"""

from __future__ import annotations

from typing import Any

import pytest





def test_format_does_not_mutate_template() -> None:
    """测试 format 方法不会修改实例的 template 属性（修复状态污染）。"""
    PromptTemplate = prompt_solution.PromptTemplate  # noqa: F821

    original_template = "Hello {name}, you are {age} years old"
    template = PromptTemplate(original_template)

    # 第一次格式化
    result1 = template.format(name="Alice", age=30)
    assert result1 == "Hello Alice, you are 30 years old"

    # 验证原始模板未被修改
    assert template.template == original_template, "Template was mutated after first format!"

    # 第二次格式化（使用不同参数）
    result2 = template.format(name="Bob", age=25)
    assert result2 == "Hello Bob, you are 25 years old"

    # 再次验证原始模板未被修改
    assert template.template == original_template, "Template was mutated after second format!"


def test_format_returns_new_string_each_time() -> None:
    """测试 format 方法每次返回新字符串。"""
    PromptTemplate = prompt_solution.PromptTemplate  # noqa: F821

    template = PromptTemplate("Value: {value}")

    result1 = template.format(value="A")
    result2 = template.format(value="B")
    result3 = template.format(value="A")

    assert result1 == "Value: A"
    assert result2 == "Value: B"
    assert result3 == "Value: A"

    # 确保每次调用都返回独立的结果
    assert result1 != result2
    assert result1 == result3


def test_format_handles_multiple_placeholders() -> None:
    """测试多个占位符的格式化。"""
    PromptTemplate = prompt_solution.PromptTemplate  # noqa: F821

    template = PromptTemplate("Name: {name}, Age: {age}, City: {city}")
    result = template.format(name="Alice", age=30, city="NYC")

    assert result == "Name: Alice, Age: 30, City: NYC"
    assert template.template == "Name: {name}, Age: {age}, City: {city}"
