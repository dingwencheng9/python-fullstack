"""测试 solutions/03-advanced.py - 验证环境配置（高级）

from __future__ import annotations

测试覆盖:
- get_python_version()
- get_tool_version()
- validate_pyproject_config()
- generate_validation_report()
- print_validation_report()
- fix_common_issues()
"""

# 导入被测试模块
# 动态导入 03-advanced.py (因为文件名包含连字符)
import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "advanced",
    Path(__file__).parent.parent / "solutions" / "solution_03_advanced.py",
)
advanced = importlib.util.module_from_spec(spec)
spec.loader.exec_module(advanced)


class TestGetPythonVersion:
    """测试 get_python_version()"""

    def test_get_python_version_returns_correct_info(self):
        """测试返回正确的 Python 版本信息"""
        result = advanced.get_python_version()

        assert result["installed"] is True
        assert isinstance(result["version"], str)
        assert result["meets_requirement"] == (sys.version_info >= (3, 12))

    def test_get_python_version_format(self):
        """测试版本号格式"""
        result = advanced.get_python_version()

        version_parts = result["version"].split(".")
        assert len(version_parts) == 3
        assert all(part.isdigit() for part in version_parts)

    def test_get_python_version_requirement_check(self):
        """测试版本要求检查逻辑"""
        result = advanced.get_python_version()

        major = sys.version_info.major
        minor = sys.version_info.minor

        if major > 3 or (major == 3 and minor >= 12):
            assert result["meets_requirement"] is True
        else:
            assert result["meets_requirement"] is False


class TestGetToolVersion:
    """测试 get_tool_version()"""

    def test_get_tool_version_installed(self):
        """测试工具已安装的情况"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0 (abc123)\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("uv")

        assert result["installed"] is True
        assert result["version"] == "0.5.0"
        assert result["meets_requirement"] is True

    def test_get_tool_version_not_installed(self):
        """测试工具未安装"""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = advanced.get_tool_version("nonexistent-tool")

        assert result["installed"] is False
        assert result["version"] == "not installed"
        assert result["meets_requirement"] is False

    def test_get_tool_version_subprocess_error(self):
        """测试命令执行失败"""
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "tool")):
            result = advanced.get_tool_version("tool")

        assert result["installed"] is False

    def test_get_tool_version_with_min_version_pass(self):
        """测试版本满足最低要求"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.5.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", min_version="1.3.0")

        assert result["meets_requirement"] is True

    def test_get_tool_version_with_min_version_fail(self):
        """测试版本不满足最低要求"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.2.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", min_version="1.3.0")

        assert result["meets_requirement"] is False

    def test_get_tool_version_no_version_pattern(self):
        """测试输出中无版本号"""
        mock_result = Mock()
        mock_result.stdout = "tool version unknown\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool")

        assert result["installed"] is True
        assert result["version"] == "unknown"
        assert result["meets_requirement"] is False

    def test_get_tool_version_complex_output(self):
        """测试复杂的版本输出格式"""
        mock_result = Mock()
        mock_result.stdout = "ruff 0.8.1 (build 2024-01-01)\nPython 3.12.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("ruff")

        # 应该提取第一个匹配的版本号
        assert result["version"] == "0.8.1"


class TestValidatePyprojectConfig:
    """测试 validate_pyproject_config()"""

    def test_validate_config_all_pass(self, tmp_path):
        """测试所有配置验证通过"""
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.13"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        result = advanced.validate_pyproject_config(tmp_path)

        assert result is True

    def test_validate_config_missing_file(self, tmp_path):
        """测试 pyproject.toml 不存在"""
        result = advanced.validate_pyproject_config(tmp_path)

        assert result is False

    def test_validate_config_missing_requires_python(self, tmp_path):
        """测试缺少 requires-python"""
        toml_content = """
[project]
name = "test"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.13"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        result = advanced.validate_pyproject_config(tmp_path)

        assert result is False

    def test_validate_config_wrong_ruff_target(self, tmp_path):
        """测试 ruff target-version 错误"""
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py311"

[tool.mypy]
python_version = "3.13"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        result = advanced.validate_pyproject_config(tmp_path)

        assert result is False

    def test_validate_config_wrong_mypy_version(self, tmp_path):
        """测试 mypy python_version 错误"""
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.11"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        result = advanced.validate_pyproject_config(tmp_path)

        assert result is False

    def test_validate_config_invalid_toml(self, tmp_path):
        """测试无效的 TOML 文件"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text("invalid toml content [[[")

        result = advanced.validate_pyproject_config(tmp_path)

        assert result is False


class TestGenerateValidationReport:
    """测试 generate_validation_report()"""

    def test_generate_report_all_tools_installed(self, tmp_path):
        """测试所有工具都已安装"""
        # 创建完整配置
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.13"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        mock_result = Mock()
        mock_result.stdout = "tool 1.0.0\n"

        with patch("subprocess.run", return_value=mock_result):
            report = advanced.generate_validation_report(tmp_path)

        assert "python" in report
        assert "uv" in report
        assert "ruff" in report
        assert "mypy" in report
        assert "pytest" in report
        assert "config_valid" in report
        assert "overall_pass" in report

    def test_generate_report_python_info(self, tmp_path):
        """测试报告包含正确的 Python 信息"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text("")

        with patch("subprocess.run", side_effect=FileNotFoundError):
            report = advanced.generate_validation_report(tmp_path)

        python_info = report["python"]
        assert python_info["installed"] is True
        assert isinstance(python_info["version"], str)

    def test_generate_report_overall_pass_logic(self, tmp_path):
        """测试 overall_pass 逻辑"""
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.13"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        # 模拟所有工具都满足要求
        mock_result = Mock()
        mock_result.stdout = "tool 9.0.0\n"

        with patch("subprocess.run", return_value=mock_result):
            report = advanced.generate_validation_report(tmp_path)

        # 如果 Python >= 3.13，overall_pass 应该为 True
        assert report["overall_pass"] is True

    def test_generate_report_config_invalid(self, tmp_path):
        """测试配置无效时的报告"""
        # 不创建 pyproject.toml

        with patch("subprocess.run", side_effect=FileNotFoundError):
            report = advanced.generate_validation_report(tmp_path)

        assert report["config_valid"] is False
        assert report["overall_pass"] is False


class TestPrintValidationReport:
    """测试 print_validation_report()"""

    def test_print_report_structure(self, capsys):
        """测试打印报告的结构"""
        report = {
            "python": {
                "installed": True,
                "version": "3.12.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.8.0", "meets_requirement": True},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": True,
            "overall_pass": True,
        }

        advanced.print_validation_report(report)
        captured = capsys.readouterr()

        assert "环境验证报告" in captured.out
        assert "Python 版本:" in captured.out
        assert "工具链:" in captured.out
        assert "配置验证:" in captured.out
        assert "总体结果:" in captured.out

    def test_print_report_pass_status(self, capsys):
        """测试通过状态的打印"""
        report = {
            "python": {
                "installed": True,
                "version": "3.12.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.8.0", "meets_requirement": True},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": True,
            "overall_pass": True,
        }

        advanced.print_validation_report(report)
        captured = capsys.readouterr()

        assert "✅ 通过" in captured.out

    def test_print_report_fail_status(self, capsys):
        """测试失败状态的打印"""
        report = {
            "python": {
                "installed": True,
                "version": "3.11.0",
                "meets_requirement": False,
            },
            "uv": {
                "installed": False,
                "version": "not installed",
                "meets_requirement": False,
            },
            "ruff": {
                "installed": False,
                "version": "not installed",
                "meets_requirement": False,
            },
            "mypy": {
                "installed": False,
                "version": "not installed",
                "meets_requirement": False,
            },
            "pytest": {
                "installed": False,
                "version": "not installed",
                "meets_requirement": False,
            },
            "config_valid": False,
            "overall_pass": False,
        }

        advanced.print_validation_report(report)
        captured = capsys.readouterr()

        assert "❌" in captured.out
        assert "未通过" in captured.out


class TestFixCommonIssues:
    """测试 fix_common_issues()"""

    def test_fix_issues_python_version(self, tmp_path, capsys):
        """测试 Python 版本过低的修复建议"""
        report = {
            "python": {
                "installed": True,
                "version": "3.11.0",
                "meets_requirement": False,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.8.0", "meets_requirement": True},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": True,
            "overall_pass": False,
        }

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "Python 版本过低" in captured.out
        assert "3.13" in captured.out

    def test_fix_issues_missing_uv(self, tmp_path, capsys):
        """测试 uv 未安装的修复建议"""
        report = {
            "python": {
                "installed": True,
                "version": "3.12.0",
                "meets_requirement": True,
            },
            "uv": {
                "installed": False,
                "version": "not installed",
                "meets_requirement": False,
            },
            "ruff": {"installed": True, "version": "0.8.0", "meets_requirement": True},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": True,
            "overall_pass": False,
        }

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "uv 未安装" in captured.out
        assert "install.sh" in captured.out

    def test_fix_issues_outdated_ruff(self, tmp_path, capsys):
        """测试 ruff 版本过低的修复建议"""
        report = {
            "python": {
                "installed": True,
                "version": "3.12.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.5.0", "meets_requirement": False},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": True,
            "overall_pass": False,
        }

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "ruff 版本过低" in captured.out
        assert "--upgrade" in captured.out

    def test_fix_issues_config_invalid(self, tmp_path, capsys):
        """测试配置无效的修复建议"""
        report = {
            "python": {
                "installed": True,
                "version": "3.12.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.8.0", "meets_requirement": True},
            "mypy": {"installed": True, "version": "1.13.0", "meets_requirement": True},
            "pytest": {
                "installed": True,
                "version": "8.0.0",
                "meets_requirement": True,
            },
            "config_valid": False,
            "overall_pass": False,
        }

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "pyproject.toml 配置不正确" in captured.out
        assert "requires-python" in captured.out


# 集成测试
class TestIntegration:
    """集成测试"""

    def test_complete_validation_workflow(self, tmp_path):
        """测试完整的验证流程"""
        # 创建完整的配置文件
        toml_content = """
[project]
name = "test-project"
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.mypy]
python_version = "3.13"
strict = true
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        # 模拟所有工具都已安装
        mock_result = Mock()
        mock_result.stdout = "tool 9.0.0\n"

        with patch("subprocess.run", return_value=mock_result):
            # 生成报告
            report = advanced.generate_validation_report(tmp_path)

        # 验证报告结构
        assert "python" in report
        assert "config_valid" in report
        assert report["config_valid"] is True

        # 验证配置
        config_valid = advanced.validate_pyproject_config(tmp_path)
        assert config_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
