"""L18 Python 工匠专题测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

LESSON_DIR = Path(__file__).parent.parent

# 修复后的路径（展平后）
EXAMPLE_CODE_CRAFT = LESSON_DIR / "examples" / "example_04_code_craft.py"
SOLUTION_REFACTOR = LESSON_DIR / "solutions" / "solution_04_refactor_for_readability.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_example_calculate_order_total():
    mod = load_module(EXAMPLE_CODE_CRAFT, "code_craft")
    text = '[{"sku":"A","price":10,"quantity":2}]'
    assert mod.calculate_order_total(text, discount_rate=0.1) == 18.0


def test_example_invalid_discount():
    mod = load_module(EXAMPLE_CODE_CRAFT, "code_craft")
    with pytest.raises(ValueError):
        mod.apply_discount(100, 1.5)


def test_solution_parse_lines():
    mod = load_module(SOLUTION_REFACTOR, "craft_solution")
    assert mod.parse_lines("a,1\n\nb,2") == [["a", "1"], ["b", "2"]]


def test_solution_calculate_total():
    mod = load_module(SOLUTION_REFACTOR, "craft_solution")
    assert mod.calculate_total([["a", "1"], ["b", "2.5"]]) == 3.5


@pytest.mark.parametrize(
    "content,expected",
    [
        ("a,1\nb,2", 3.0),
        ("x,10\n\ny,5", 15.0),
    ],
)
def test_solution_load_and_calculate(tmp_path, content: str, expected: float):
    mod = load_module(SOLUTION_REFACTOR, "craft_solution")
    file_path = tmp_path / "data.csv"
    file_path.write_text(content)
    assert mod.load_and_calculate(str(file_path)) == expected
