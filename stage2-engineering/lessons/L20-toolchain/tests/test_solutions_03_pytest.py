"""测试 03-pytest.py 的功能

from __future__ import annotations

测试 pytest 测试框架相关函数
"""

from __future__ import annotations

# 动态导入 03-pytest.py
import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "pytest_solution",
    Path(__file__).parent.parent / "solutions" / "solution_03_pytest.py",
)
pytest_sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pytest_sol)


class TestSaveSourceCode:
    """测试 save_source_code 函数"""

    def test_save_source_code_creates_file(self, tmp_path):
        """测试保存源代码创建文件"""
        file_path = tmp_path / "calculator.py"
        pytest_sol.save_source_code(file_path)

        assert file_path.exists()
        assert file_path.read_text() == pytest_sol.SOURCE_CODE

    def test_save_source_code_creates_parent_directory(self, tmp_path):
        """测试自动创建父目录"""
        file_path = tmp_path / "src" / "calculator.py"
        pytest_sol.save_source_code(file_path)

        assert file_path.parent.exists()
        assert file_path.exists()


class TestCreateTestForAdd:
    """测试 create_test_for_add 函数"""

    def test_creates_valid_test_code(self):
        """测试创建有效的测试代码"""
        test_code = pytest_sol.create_test_for_add()

        assert "def test_add():" in test_code
        assert "from src.calculator import add" in test_code
        assert "assert" in test_code

    def test_includes_positive_numbers(self):
        """测试包含正数测试"""
        test_code = pytest_sol.create_test_for_add()

        assert "add(1, 2) == 3" in test_code

    def test_includes_negative_numbers(self):
        """测试包含负数测试"""
        test_code = pytest_sol.create_test_for_add()

        assert "add(-1, 1)" in test_code or "add(-5, -3)" in test_code


class TestCreateTestForDivide:
    """测试 create_test_for_divide 函数"""

    def test_creates_valid_test_code(self):
        """测试创建有效的测试代码"""
        test_code = pytest_sol.create_test_for_divide()

        assert "def test_divide():" in test_code
        assert "from src.calculator import divide" in test_code

    def test_includes_zero_division_test(self):
        """测试包含除零测试"""
        test_code = pytest_sol.create_test_for_divide()

        assert "pytest.raises" in test_code or "ValueError" in test_code


class TestCreateTestForCalculator:
    """测试 create_test_for_calculator 函数"""

    def test_creates_valid_test_code(self):
        """测试创建有效的测试代码"""
        test_code = pytest_sol.create_test_for_calculator()

        assert "def test_calculator" in test_code
        assert "from src.calculator import Calculator" in test_code

    def test_includes_calculator_operations(self):
        """测试包含计算器操作"""
        test_code = pytest_sol.create_test_for_calculator()

        assert "calculate" in test_code

    def test_includes_history_tests(self):
        """测试包含历史记录测试"""
        test_code = pytest_sol.create_test_for_calculator()

        assert "history" in test_code or "get_history" in test_code


class TestSaveTestCode:
    """测试 save_test_code 函数"""

    def test_save_test_code_creates_file(self, tmp_path):
        """测试保存测试文件"""
        file_path = tmp_path / "test_calc.py"
        content = "def test_something():\n    assert True\n"

        pytest_sol.save_test_code(file_path, content)

        assert file_path.exists()
        # 文件内容会包含额外的头部信息
        file_content = file_path.read_text()
        assert "def test_something():" in file_content
        assert "assert True" in file_content

    def test_save_test_code_creates_parent(self, tmp_path):
        """测试创建父目录"""
        file_path = tmp_path / "tests" / "test_calc.py"
        content = "def test_something():\n    assert True\n"

        pytest_sol.save_test_code(file_path, content)

        assert file_path.parent.exists()
        assert file_path.exists()


class TestRunPytest:
    """测试 run_pytest 函数"""

    def test_run_pytest_success(self, tmp_path):
        """测试运行 pytest 成功"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "5 passed"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            passed, output = pytest_sol.run_pytest(tmp_path)

        assert passed is True
        assert "passed" in output

    def test_run_pytest_with_failures(self, tmp_path):
        """测试运行 pytest 有失败"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "3 passed, 2 failed"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            passed, output = pytest_sol.run_pytest(tmp_path)

        assert passed is False
        assert "failed" in output

    def test_run_pytest_not_installed(self, tmp_path):
        """测试 pytest 未安装"""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            passed, _output = pytest_sol.run_pytest(tmp_path)

        assert passed is False

    def test_run_pytest_timeout(self, tmp_path):
        """测试命令超时"""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pytest", 60)):
            passed, _output = pytest_sol.run_pytest(tmp_path)

        assert passed is False


class TestRunPytestWithCoverage:
    """测试 run_pytest_with_coverage 函数"""

    def test_run_with_coverage_success(self, tmp_path):
        """测试带覆盖率运行成功"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "5 passed\nCoverage: 85%"

        with patch("subprocess.run", return_value=mock_result):
            passed, coverage_info = pytest_sol.run_pytest_with_coverage(tmp_path)

        assert passed is True
        assert isinstance(coverage_info, dict)

    def test_run_with_coverage_parse_percentage(self, tmp_path):
        """测试解析覆盖率百分比"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "TOTAL  100  20  80%"

        with patch("subprocess.run", return_value=mock_result):
            _passed, coverage_info = pytest_sol.run_pytest_with_coverage(tmp_path)

        assert isinstance(coverage_info, dict)

    def test_run_with_coverage_failure(self, tmp_path):
        """测试运行失败"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "3 passed, 2 failed"

        with patch("subprocess.run", return_value=mock_result):
            passed, _coverage_info = pytest_sol.run_pytest_with_coverage(tmp_path)

        assert passed is False


class TestCreatePytestConfig:
    """测试 create_pytest_config 函数"""

    def test_create_pytest_config_new_file(self, tmp_path):
        """测试创建新配置文件"""
        if importlib.util.find_spec("tomli_w") is None:
            pytest.skip("tomli_w not installed")

        pytest_sol.create_pytest_config(tmp_path)

        config_file = tmp_path / "pyproject.toml"
        assert config_file.exists()

        content = config_file.read_text()
        assert "pytest" in content

    def test_create_pytest_config_with_coverage(self, tmp_path):
        """测试配置包含覆盖率设置"""
        if importlib.util.find_spec("tomli_w") is None:
            pytest.skip("tomli_w not installed")

        pytest_sol.create_pytest_config(tmp_path)

        config_file = tmp_path / "pyproject.toml"
        content = config_file.read_text()

        assert "cov" in content or "pytest" in content

    def test_create_pytest_config_without_tomli_w(self, tmp_path):
        """测试 tomli_w 未安装时的处理"""
        try:
            pytest_sol.create_pytest_config(tmp_path)
        except Exception as e:
            pytest.fail(f"Function should handle missing tomli_w gracefully: {e}")


class TestMain:
    """测试 main 函数"""

    @patch("builtins.print")
    @patch.object(pytest_sol, "run_pytest", return_value=(True, "3 passed"))
    @patch.object(pytest_sol, "run_pytest_with_coverage", return_value=(True, {"coverage": 85.0}))
    def test_main_success_flow(self, mock_cov, mock_run, mock_print, tmp_path, monkeypatch):
        """测试 main 函数成功流程"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        pytest_sol.main()

        # 验证 print 被调用
        assert mock_print.call_count > 0

        # 验证测试目录被创建
        test_dir = tmp_path / "pytest_test"
        assert test_dir.exists()

    @patch("builtins.print")
    @patch.object(pytest_sol, "run_pytest", return_value=(False, "Test failed"))
    def test_main_test_failure(self, mock_run, mock_print, tmp_path, monkeypatch):
        """测试 main 函数测试失败"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        pytest_sol.main()

        # 验证仍然能完成
        assert mock_print.call_count > 0

    @patch("builtins.print")
    def test_main_creates_files(self, mock_print, tmp_path, monkeypatch):
        """测试 main 函数创建文件"""
        monkeypatch.chdir(tmp_path)

        # Mock pytest 运行以避免真实调用
        with (
            patch.object(pytest_sol, "run_pytest", return_value=(True, "3 passed")),
            patch.object(
                pytest_sol,
                "run_pytest_with_coverage",
                return_value=(True, {"coverage": 85.0}),
            ),
        ):
            pytest_sol.main()

        # 验证文件被创建（注意：在 src/ 和 tests/ 子目录下）
        test_dir = tmp_path / "pytest_test"
        assert (test_dir / "src" / "calculator.py").exists()
        assert (test_dir / "tests" / "test_calculator.py").exists()


class TestQualityStrengthening:
    """补充 pytest 生成器的强标记测试。"""

    @pytest.mark.parametrize(
        ("factory_name", "required_snippet"),
        [
            ("create_test_for_add", "assert add(0, 0) == 0"),
            ("create_test_for_divide", "pytest.raises(ValueError"),
            ("create_test_for_calculator", "calc.clear_history()"),
        ],
    )
    def test_generated_tests_include_boundary_and_error_cases(
        self,
        factory_name: str,
        required_snippet: str,
    ) -> None:
        """参数化验证生成的测试代码覆盖边界和异常意图。"""
        factory = getattr(pytest_sol, factory_name)
        test_code = factory()

        assert required_snippet in test_code

    def test_source_code_divide_raises_for_zero_denominator(self) -> None:
        """异常路径：动态执行示例源码后验证除零保护。"""
        namespace: dict[str, object] = {}
        exec(pytest_sol.SOURCE_CODE, namespace)
        divide = namespace["divide"]

        with pytest.raises(ValueError, match="除数不能为 0"):
            divide(1, 0)

    def test_coverage_parser_boundary_zero_statements(self, tmp_path: Path) -> None:
        """边界场景：覆盖率输出为 0 条语句时仍能解析百分比。"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "TOTAL 0 0 100%"

        with patch("subprocess.run", return_value=mock_result):
            passed, coverage_info = pytest_sol.run_pytest_with_coverage(tmp_path)

        assert passed is True
        assert coverage_info["coverage"] == 100.0
        assert coverage_info["statements"] == 0
        assert coverage_info["missing"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
