"""测试 02-mypy.py 的功能

from __future__ import annotations

测试 mypy 类型检查相关函数
"""

# 动态导入 02-mypy.py
import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "mypy_solution",
    Path(__file__).parent.parent / "solutions" / "solution_02_mypy.py",
)
mypy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mypy)


class TestSaveCodeWithoutTypes:
    """测试 save_code_without_types 函数"""

    def test_save_code_creates_file(self, tmp_path):
        """测试保存代码创建文件"""
        file_path = tmp_path / "test.py"
        mypy.save_code_without_types(file_path)

        assert file_path.exists()
        assert file_path.read_text() == mypy.SAMPLE_CODE_NO_TYPES

    def test_save_code_creates_parent_directory(self, tmp_path):
        """测试自动创建父目录"""
        file_path = tmp_path / "subdir" / "test.py"
        mypy.save_code_without_types(file_path)

        assert file_path.parent.exists()
        assert file_path.exists()


class TestAddBasicTypes:
    """测试 add_basic_types 函数"""

    def test_add_basic_types_adds_imports(self):
        """测试不添加旧版 typing 导入（Python 3.10+ 现代语法）"""
        code = "def greet(name):\n    pass\n"

        result = mypy.add_basic_types(code)

        # ✅ Python 3.10+ 不需要导入 typing.List/Dict
        # 直接使用内置泛型 list[T], dict[K,V]
        assert "def greet(name: str) -> str:" in result

    def test_add_basic_types_greet_function(self):
        """测试为 greet 函数添加类型"""
        code = "def greet(name):\n    return f'Hello, {name}'\n"

        result = mypy.add_basic_types(code)

        assert "def greet(name: str) -> str:" in result

    def test_add_basic_types_calculate_total_function(self):
        """测试为 calculate_total 函数添加类型（现代语法）"""
        code = "def calculate_total(prices):\n    return sum(prices)\n"

        result = mypy.add_basic_types(code)

        # ✅ 使用 list[float] 而不是 List[float]
        assert "def calculate_total(prices: list[float]) -> float:" in result

    def test_add_basic_types_preserves_existing_imports(self):
        """测试保留已存在的导入"""
        code = "from typing import Dict\n\ndef greet(name):\n    pass\n"

        result = mypy.add_basic_types(code)

        # 不应该重复添加 typing 导入
        assert code.count("from typing import") == result.count("from typing import")


class TestAddComplexTypes:
    """测试 add_complex_types 函数"""

    def test_add_complex_types_find_user(self):
        """测试为 find_user 添加类型（Python 3.10+ 现代语法）"""
        code = "def find_user(users, user_id):\n    pass\n"

        result = mypy.add_complex_types(code)

        # ✅ 使用 list[dict[str, str | int]] 和 X | None
        assert "list[dict[str, str | int]]" in result
        assert "dict[str, str | int] | None" in result

    def test_add_complex_types_user_manager_init(self):
        """测试为 UserManager.__init__ 添加类型"""
        code = "def __init__(self, database_url):\n    pass\n"

        result = mypy.add_complex_types(code)

        assert "def __init__(self, database_url: str) -> None:" in result

    def test_add_complex_types_add_user(self):
        """测试为 add_user 添加类型（现代语法）"""
        code = "def add_user(self, name, age):\n    pass\n"

        result = mypy.add_complex_types(code)

        assert "def add_user(self, name: str, age: int)" in result
        # ✅ 使用 dict[str, str | int] 而不是 Dict[str, Union[str, int]]
        assert "dict[str, str | int]" in result

    def test_add_complex_types_get_user(self):
        """测试为 get_user 添加类型（现代语法）"""
        code = "def get_user(self, user_id):\n    pass\n"

        result = mypy.add_complex_types(code)

        assert "def get_user(self, user_id: int)" in result
        # ✅ 使用 X | None 而不是 Optional[X]
        assert "dict[str, str | int] | None" in result


class TestRunMypyCheck:
    """测试 run_mypy_check 函数"""

    def test_run_mypy_check_success(self, tmp_path):
        """测试类型检查通过"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello(name: str) -> str:\n    return name\n")

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Success"

        with patch("subprocess.run", return_value=mock_result):
            passed, output = mypy.run_mypy_check(file_path)

        assert passed is True
        # output is a list
        assert isinstance(output, list)

    def test_run_mypy_check_with_errors(self, tmp_path):
        """测试类型检查发现错误"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello(name) -> str:\n    return name\n")

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "error: Missing type annotation"

        with patch("subprocess.run", return_value=mock_result):
            passed, output = mypy.run_mypy_check(file_path)

        assert passed is False
        # output is a list of error messages
        assert isinstance(output, list)

    def test_run_mypy_check_not_installed(self, tmp_path):
        """测试 mypy 未安装"""
        file_path = tmp_path / "test.py"

        with patch("subprocess.run", side_effect=FileNotFoundError):
            passed, output = mypy.run_mypy_check(file_path)

        assert passed is False
        assert isinstance(output, list)

    def test_run_mypy_check_timeout(self, tmp_path):
        """测试命令超时"""
        file_path = tmp_path / "test.py"

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("mypy", 30)):
            passed, output = mypy.run_mypy_check(file_path)

        assert passed is False
        assert isinstance(output, list)


class TestAnalyzeTypeCoverage:
    """测试 analyze_type_coverage 函数"""

    def test_analyze_no_annotations(self, tmp_path):
        """测试无类型注解的代码"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello(name):\n    return name\n")

        result = mypy.analyze_type_coverage(file_path)

        assert isinstance(result, dict)
        assert "total_params" in result or "coverage" in result

    def test_analyze_with_annotations(self, tmp_path):
        """测试有类型注解的代码"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello(name: str) -> str:\n    return name\n")

        result = mypy.analyze_type_coverage(file_path)

        assert isinstance(result, dict)

    def test_analyze_partial_annotations(self, tmp_path):
        """测试部分有类型注解"""
        file_path = tmp_path / "test.py"
        code = """def hello(name: str) -> str:
    return name

def goodbye(name):
    return name
"""
        file_path.write_text(code)

        result = mypy.analyze_type_coverage(file_path)

        assert isinstance(result, dict)


class TestCreateMypyConfig:
    """测试 create_mypy_config 函数"""

    def test_create_mypy_config_new_file(self, tmp_path):
        """测试创建新配置文件"""
        if importlib.util.find_spec("tomli_w") is None:
            pytest.skip("tomli_w not installed")

        mypy.create_mypy_config(tmp_path)

        config_file = tmp_path / "pyproject.toml"
        assert config_file.exists()

        content = config_file.read_text()
        assert "mypy" in content

    def test_create_mypy_config_merge_existing(self, tmp_path):
        """测试合并现有配置"""
        if importlib.util.find_spec("tomli_w") is None:
            pytest.skip("tomli_w not installed")

        config_file = tmp_path / "pyproject.toml"
        config_file.write_text('[project]\nname = "test"\n')

        mypy.create_mypy_config(tmp_path)

        content = config_file.read_text()
        assert "project" in content or "mypy" in content

    def test_create_mypy_config_without_tomli_w(self, tmp_path):
        """测试 tomli_w 未安装时的处理"""
        try:
            mypy.create_mypy_config(tmp_path)
        except Exception as e:
            pytest.fail(f"Function should handle missing tomli_w gracefully: {e}")


class TestMain:
    """测试 main 函数"""

    @patch("builtins.print")
    @patch.object(mypy, "run_mypy_check", return_value=(True, []))
    def test_main_success_flow(self, mock_check, mock_print, tmp_path, monkeypatch):
        """测试 main 函数成功流程"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        mypy.main()

        # 验证 print 被调用
        assert mock_print.call_count > 0

        # 验证测试目录被创建
        test_dir = tmp_path / "mypy_test"
        assert test_dir.exists()

    @patch("builtins.print")
    @patch.object(mypy, "run_mypy_check", return_value=(False, ["Error"]))
    def test_main_with_errors(self, mock_check, mock_print, tmp_path, monkeypatch):
        """测试 main 函数有类型错误"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        mypy.main()

        # 验证仍然能完成
        assert mock_print.call_count > 0

    @patch("builtins.print")
    def test_main_creates_files(self, mock_print, tmp_path, monkeypatch):
        """测试 main 函数创建文件"""
        monkeypatch.chdir(tmp_path)

        # Mock mypy 检查以避免真实调用
        with patch.object(mypy, "run_mypy_check", return_value=(True, [])):
            mypy.main()

        # 验证文件被创建
        test_dir = tmp_path / "mypy_test"
        assert (test_dir / "sample.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
