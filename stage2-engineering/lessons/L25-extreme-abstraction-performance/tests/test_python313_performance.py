"""
测试 L23 Python 3.13 性能优化特性

验证性能优化示例的正确性
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"


def _bind_examples_package() -> None:
    """绑定本课 examples 包，避免被其它 lesson 的 examples 包遮蔽。

    不使用 sys.modules.pop（CI 门禁规则禁止）。
    """
    # 复用已存在的 examples 包（如果存在），或创建新的
    examples_pkg = sys.modules.get("examples")
    if examples_pkg is None:
        examples_pkg = types.ModuleType("examples")
        sys.modules["examples"] = examples_pkg

    # 更新 __path__ 以包含本课 examples 目录
    if not hasattr(examples_pkg, "__path__"):
        examples_pkg.__path__ = []
    if isinstance(examples_pkg.__path__, list):
        # 添加本课路径（去重）
        lesson_path = str(EXAMPLES_DIR)
        if lesson_path not in examples_pkg.__path__:
            examples_pkg.__path__.append(lesson_path)


_bind_examples_package()


@pytest.fixture(autouse=True)
def _ensure_l28_examples_package() -> None:
    """每个测试前重新绑定，覆盖根 conftest 的跨课程清理。"""
    _bind_examples_package()
