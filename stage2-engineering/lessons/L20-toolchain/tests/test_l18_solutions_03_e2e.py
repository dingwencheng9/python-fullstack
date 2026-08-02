"""扩展测试 - 03-advanced.py 端到端测试

from __future__ import annotations

添加 main() 函数和完整流程的端到端测试，提升覆盖率
"""

# 导入被测试模块
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "advanced",
    Path(__file__).parent.parent / "solutions" / "solution_03_advanced.py",
)
advanced = importlib.util.module_from_spec(spec)
spec.loader.exec_module(advanced)


class TestMainFunction:
    """测试 main() 函数的端到端场景"""

    def test_main_complete_success_workflow(self, tmp_path, capsys):
        """测试完整成功流程"""
        # 创建完整的配置文件
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
        mock_result.stdout = "tool 9.0.0\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            advanced.main()

            captured = capsys.readouterr()
            assert "练习 3: 验证环境配置" in captured.out
            assert "步骤 1: 检查 Python 版本" in captured.out
            assert "步骤 2: 检查工具链" in captured.out
            assert "步骤 3: 验证配置" in captured.out
            assert "步骤 4: 生成完整报告" in captured.out

    def test_main_all_tools_installed(self, tmp_path, capsys):
        """测试所有工具都已安装"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nrequires-python = ">=3.13"')

        mock_result = Mock()
        mock_result.stdout = "tool 9.0.0\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            advanced.main()

            captured = capsys.readouterr()
            assert "✅ uv:" in captured.out
            assert "✅ ruff:" in captured.out
            assert "✅ mypy:" in captured.out
            assert "✅ pytest:" in captured.out

    def test_main_pyproject_not_exists(self, tmp_path, capsys):
        """测试 pyproject.toml 不存在"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.0.0\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            advanced.main()

            captured = capsys.readouterr()
            assert "⚠️  pyproject.toml 不存在" in captured.out

    def test_main_shows_fix_suggestions(self, tmp_path, capsys):
        """测试显示修复建议"""
        # 创建不完整的配置
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text("[project]\nname = 'test'")

        with (
            patch("subprocess.run", side_effect=FileNotFoundError),
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            advanced.main()

            captured = capsys.readouterr()
            assert "步骤 5: 修复建议" in captured.out
            assert "修复建议:" in captured.out

    def test_main_success_message(self, tmp_path, capsys):
        """测试成功消息"""
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
        mock_result.stdout = "tool 9.0.0\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            advanced.main()

            captured = capsys.readouterr()

            assert "🎉 恭喜！环境配置完全符合 v4.1 标准！" in captured.out
            assert "下一步: 进入 L19 学习异步编程核心" in captured.out

    def test_main_keyboard_interrupt(self, tmp_path):
        """测试直接调用 main 时键盘中断会向上传播。

        CLI 入口的 ``if __name__ == "__main__"`` 块负责将该异常转换为
        用户友好的退出消息；单元测试直接调用 ``main()`` 时应验证传播行为。
        """
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch.object(advanced, "get_python_version", side_effect=KeyboardInterrupt),
            pytest.raises(KeyboardInterrupt),
        ):
            advanced.main()

    def test_main_import_error(self, tmp_path):
        """测试直接调用 main 时 ImportError 会向上传播。

        CLI 入口的 ``if __name__ == "__main__"`` 块负责将该异常转换为
        用户友好的依赖安装提示；单元测试直接调用 ``main()`` 时验证传播行为。
        """
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch.object(advanced, "get_python_version", side_effect=ImportError("tomli")),
            pytest.raises(ImportError, match="tomli"),
        ):
            advanced.main()


class TestPrintValidationReportDetailed:
    """测试 print_validation_report 的详细输出"""

    def test_print_report_python_pass(self, capsys):
        """测试 Python 版本通过的输出"""
        report = {
            "python": {
                "installed": True,
                "version": "3.13.0",
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

        assert "Python 版本:" in captured.out
        assert "Python 3.13.0" in captured.out
        assert "✅ 满足要求 (>= 3.13)" in captured.out

    def test_print_report_python_fail(self, capsys):
        """测试 Python 版本不满足的输出"""
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

        assert "❌ 不满足要求 (需要 >= 3.13)" in captured.out

    def test_print_report_tool_not_installed(self, capsys):
        """测试工具未安装的输出"""
        report = {
            "python": {
                "installed": True,
                "version": "3.13.0",
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

        advanced.print_validation_report(report)
        captured = capsys.readouterr()

        assert "❌ uv: 未安装" in captured.out

    def test_print_report_tool_version_warning(self, capsys):
        """测试工具版本警告"""
        report = {
            "python": {
                "installed": True,
                "version": "3.13.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.3.0", "meets_requirement": False},
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

        advanced.print_validation_report(report)
        captured = capsys.readouterr()

        assert "⚠️ uv: 0.3.0" in captured.out


class TestFixCommonIssuesDetailed:
    """测试 fix_common_issues 的详细输出"""

    def test_fix_issues_missing_all_tools(self, tmp_path, capsys):
        """测试所有工具都缺失"""
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

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "❌ Python 版本过低" in captured.out
        assert "❌ uv 未安装" in captured.out
        assert "❌ ruff 未安装" in captured.out
        assert "❌ mypy 未安装" in captured.out
        assert "❌ pytest 未安装" in captured.out
        assert "❌ pyproject.toml 配置不正确" in captured.out

    def test_fix_issues_outdated_tools(self, tmp_path, capsys):
        """测试工具版本过低"""
        report = {
            "python": {
                "installed": True,
                "version": "3.13.0",
                "meets_requirement": True,
            },
            "uv": {"installed": True, "version": "0.5.0", "meets_requirement": True},
            "ruff": {"installed": True, "version": "0.5.0", "meets_requirement": False},
            "mypy": {"installed": True, "version": "1.0.0", "meets_requirement": False},
            "pytest": {
                "installed": True,
                "version": "7.0.0",
                "meets_requirement": False,
            },
            "config_valid": True,
            "overall_pass": False,
        }

        advanced.fix_common_issues(tmp_path, report)
        captured = capsys.readouterr()

        assert "⚠️  ruff 版本过低" in captured.out
        assert "⚠️  mypy 版本过低" in captured.out
        assert "⚠️  pytest 版本过低" in captured.out
        assert "uv add --dev ruff --upgrade" in captured.out
        assert "uv add --dev mypy --upgrade" in captured.out
        assert "uv add --dev pytest --upgrade" in captured.out

    def test_fix_issues_shows_reference(self, tmp_path, capsys):
        """测试显示参考信息"""
        report = {
            "python": {
                "installed": True,
                "version": "3.13.0",
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

        assert "请检查:" in captured.out
        assert "requires-python >= 3.13" in captured.out
        assert "tool.ruff.target-version = 'py313'" in captured.out
        assert "tool.mypy.python_version = '3.13'" in captured.out
        assert "参考练习 2 的配置示例" in captured.out


class TestVersionComparison:
    """测试版本比较逻辑"""

    def test_version_comparison_equal(self):
        """测试相等版本"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.0.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", "1.0.0")

        assert result["meets_requirement"] is True

    def test_version_comparison_greater(self):
        """测试更高版本"""
        mock_result = Mock()
        mock_result.stdout = "tool 2.0.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", "1.0.0")

        assert result["meets_requirement"] is True

    def test_version_comparison_minor_greater(self):
        """测试次版本号更高"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.5.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", "1.3.0")

        assert result["meets_requirement"] is True

    def test_version_comparison_patch_greater(self):
        """测试补丁版本号更高"""
        mock_result = Mock()
        mock_result.stdout = "tool 1.0.5\n"

        with patch("subprocess.run", return_value=mock_result):
            result = advanced.get_tool_version("tool", "1.0.3")

        assert result["meets_requirement"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
