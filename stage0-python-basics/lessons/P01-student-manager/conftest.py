"""P01 学员管理系统 — pytest 配置（隔离重载方案）"""
from __future__ import annotations

import sys
from importlib.util import spec_from_file_location
from pathlib import Path
from types import ModuleType

import pytest


def _create_p01_pkg() -> ModuleType:
    """从 P01/solutions/ 创建隔离的 fake package，模拟 __init__.py 导出行为。"""
    solutions_dir = Path(__file__).parent.resolve() / "solutions"
    pkg = ModuleType("p01_solutions")
    pkg.__path__ = [str(solutions_dir)]
    pkg.__package__ = "p01_solutions"

    for py_file in solutions_dir.glob("*.py"):
        name = py_file.name
        if name.startswith("_"):
            continue
        mod_name = name[:-3]
        full_name = f"p01_solutions.{mod_name}"
        spec = spec_from_file_location(full_name, py_file)
        if spec and spec.loader:
            mod = ModuleType(full_name)
            mod.__file__ = str(py_file)
            mod.__package__ = "p01_solutions"
            sys.modules[full_name] = mod
            spec.loader.exec_module(mod)
            # 模拟 __init__.py 的显式导出：Student / StudentManager
            setattr(pkg, mod_name, mod)
            if mod_name == "student_manager":
                pkg.Student = mod.Student
                pkg.StudentManager = mod.StudentManager

    pkg.__all__ = ["Student", "StudentManager", "student_manager"]
    sys.modules["p01_solutions"] = pkg
    return pkg


# 模块加载时（collection 阶段）创建一次 P01 pkg
_p01_pkg = _create_p01_pkg()


@pytest.fixture(scope="module", autouse=True)
def _inject_p01_solutions() -> None:
    """覆盖 sys.modules["solutions"] 为 P01 包，在本 lesson 所有测试前执行。"""
    sys.modules["solutions"] = _p01_pkg


@pytest.fixture(scope="module")
def solutions() -> ModuleType:
    """返回 P01 的 solutions 包。"""
    return _p01_pkg
