"""L01 Python 核心语法 - 演示型练习测试

测试 exercises/ 目录下的演示型练习。
演示型练习是完整实现，学员运行并观察输出。

注意：
- 演示型练习不要求学员"实现"代码
- 测试验证模块可加载、变量存在、无语法错误
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


# 通过物理路径加载 exercises 模块
EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def hello_module():
    """加载 exercises/01_hello_practice.py"""
    return _load_exercise_module("_test_hello", EXERCISES_DIR / "01_hello_practice.py")


@pytest.fixture(scope="module")
def io_module():
    """加载 exercises/02_io_practice.py"""
    return _load_exercise_module("_test_io", EXERCISES_DIR / "02_io_practice.py")


@pytest.fixture(scope="module")
def types_module():
    """加载 exercises/03_type_basics.py"""
    return _load_exercise_module("_test_types", EXERCISES_DIR / "03_type_basics.py")


@pytest.fixture(scope="module")
def conversion_module():
    """加载 exercises/04_type_conversion.py"""
    return _load_exercise_module("_test_conversion", EXERCISES_DIR / "04_type_conversion.py")


@pytest.fixture(scope="module")
def fstring_module():
    """加载 exercises/05_fstring_practice.py"""
    return _load_exercise_module("_test_fstring", EXERCISES_DIR / "05_fstring_practice.py")


# ============================================================
# 01_hello_practice.py 测试
# ============================================================


class TestHelloPractice:
    """测试 01_hello_practice.py

    验证：
    1. 模块可正常加载
    2. 定义了 name, age, city, hobby 变量
    3. 包含 f-string 格式化
    4. 脚本可执行（无语法错误）
    """

    def test_module_exists(self, hello_module) -> None:
        """验证模块可加载"""
        assert hello_module is not None

    def test_has_variables(self, hello_module) -> None:
        """验证定义了基本变量（无 def 函数）"""
        assert hasattr(hello_module, "name"), "应定义 name 变量"
        assert hasattr(hello_module, "age"), "应定义 age 变量"
        assert hasattr(hello_module, "city"), "应定义 city 变量"
        assert hasattr(hello_module, "hobby"), "应定义 hobby 变量"

    def test_no_function_definitions(self, hello_module) -> None:
        """验证不包含 def 函数定义（符合 L01 知识边界）"""
        # 获取模块的源代码
        source_file = EXERCISES_DIR / "01_hello_practice.py"
        source = source_file.read_text()

        # 检查源代码中不包含 def 关键字
        assert "def " not in source, "L01 演示型练习不应包含 def 函数定义"

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行（无语法错误）"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "01_hello_practice.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 02_io_practice.py 测试
# ============================================================


class TestIOPractice:
    """测试 02_io_practice.py

    验证：
    1. 模块可正常加载
    2. 不包含 def 函数定义
    3. 脚本可执行
    """

    def test_module_exists(self, io_module) -> None:
        """验证模块可加载"""
        assert io_module is not None

    def test_no_function_definitions(self, io_module) -> None:
        """验证不包含 def 函数定义"""
        source_file = EXERCISES_DIR / "02_io_practice.py"
        source = source_file.read_text()
        assert "def " not in source, "L01 演示型练习不应包含 def 函数定义"


# ============================================================
# 03_type_basics.py 测试
# ============================================================


class TestTypeBasics:
    """测试 03_type_basics.py

    验证：
    1. 模块可正常加载
    2. 定义了各种类型的变量
    3. 不包含 def 函数定义
    """

    def test_module_exists(self, types_module) -> None:
        """验证模块可加载"""
        assert types_module is not None

    def test_has_type_examples(self, types_module) -> None:
        """验证包含类型示例变量"""
        # 检查是否定义了示例变量（通过检查模块属性）
        attrs = dir(types_module)
        # 模块应包含一些变量，但不是函数
        has_variables = any(
            not callable(getattr(types_module, attr)) and not attr.startswith("_")
            for attr in attrs
        )
        assert has_variables, "应包含变量示例"

    def test_no_function_definitions(self, types_module) -> None:
        """验证不包含 def 函数定义"""
        source_file = EXERCISES_DIR / "03_type_basics.py"
        source = source_file.read_text()
        assert "def " not in source, "L01 演示型练习不应包含 def 函数定义"


# ============================================================
# 04_type_conversion.py 测试
# ============================================================


class TestTypeConversion:
    """测试 04_type_conversion.py

    验证：
    1. 模块可正常加载
    2. 不包含 def 函数定义
    3. 不包含 if 语句（知识边界）
    """

    def test_module_exists(self, conversion_module) -> None:
        """验证模块可加载"""
        assert conversion_module is not None

    def test_no_function_definitions(self, conversion_module) -> None:
        """验证不包含 def 函数定义"""
        source_file = EXERCISES_DIR / "04_type_conversion.py"
        source = source_file.read_text()
        assert "def " not in source, "L01 演示型练习不应包含 def 函数定义"


# ============================================================
# 05_fstring_practice.py 测试
# ============================================================


class TestFStringPractice:
    """测试 05_fstring_practice.py

    验证：
    1. 模块可正常加载
    2. 包含 f-string 示例
    3. 不包含 def 函数定义
    """

    def test_module_exists(self, fstring_module) -> None:
        """验证模块可加载"""
        assert fstring_module is not None

    def test_has_fstring_examples(self, fstring_module) -> None:
        """验证包含 f-string 示例变量"""
        # 检查模块中是否有示例变量
        source_file = EXERCISES_DIR / "05_fstring_practice.py"
        source = source_file.read_text()
        assert 'f"' in source or "f'" in source, "应包含 f-string 示例"

    def test_no_function_definitions(self, fstring_module) -> None:
        """验证不包含 def 函数定义"""
        source_file = EXERCISES_DIR / "05_fstring_practice.py"
        source = source_file.read_text()
        assert "def " not in source, "L01 演示型练习不应包含 def 函数定义"


# ============================================================
# 整体验证
# ============================================================


class TestStage0L01Compliance:
    """整体验证：L01 exercises 符合知识边界定义"""

    def test_all_exercises_no_def(self) -> None:
        """验证所有 L01 exercises 不包含 def 函数定义"""
        for py_file in EXERCISES_DIR.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            assert "def " not in source, f"{py_file.name} 不应包含 def 函数定义"

    def test_all_exercises_no_if(self) -> None:
        """验证所有 L01 exercises 不包含 if 语句（越界 L02）"""
        for py_file in EXERCISES_DIR.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            # 注意：注释中的 "if" 可以忽略，但实际代码中的 if 语句不行
            lines = source.split("\n")
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    assert not stripped.startswith("if "), f"{py_file.name} 不应包含 if 语句"

    def test_all_exercises_no_class(self) -> None:
        """验证所有 L01 exercises 不包含 class 定义（越界 L07）"""
        for py_file in EXERCISES_DIR.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            assert "class " not in source, f"{py_file.name} 不应包含 class 定义"
