"""L34-htmx 测试 conftest

通过 importlib.util.spec_from_file_location 按物理路径加载 examples 模块，
不修改 sys.path，不清理 sys.modules。
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


LESSON_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = LESSON_ROOT / "examples"

_PKG_NAME = "_test_examples_L34_htmx"


def _load_module(name: str, file_path: Path) -> object:
    """按物理路径加载模块并赋予唯一名，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def examples() -> object:
    """加载 L34 examples 包及其全部子模块。"""
    examples_pkg = _load_module(_PKG_NAME, EXAMPLES_DIR / "__init__.py")
    examples_pkg.__path__ = [str(EXAMPLES_DIR)]
    for sub_file in sorted(EXAMPLES_DIR.glob("*.py")):
        if sub_file.stem in ("__init__", "conftest"):
            continue
        if not hasattr(examples_pkg, sub_file.stem):
            setattr(
                examples_pkg,
                sub_file.stem,
                _load_module(f"{_PKG_NAME}.{sub_file.stem}", sub_file),
            )
    return examples_pkg


@pytest.fixture(scope="module", autouse=True)
def _inject_examples(examples, request) -> None:
    """将 examples 子模块注入测试模块命名空间。"""
    for stem in ("01_basic_htmx", "02_crud_operations"):
        if hasattr(examples, stem):
            request.module.__dict__[stem.replace("_", "_")] = getattr(examples, stem)
