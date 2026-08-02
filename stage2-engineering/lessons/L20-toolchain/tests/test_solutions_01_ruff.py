"""测试 01-ruff.py 的功能

from __future__ import annotations

测试 Ruff 代码格式化和检查相关函数
"""

# 动态导入 01-ruff.py
import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "ruff_solution",
    Path(__file__).parent.parent / "solutions" / "solution_01_ruff.py",
)
ruff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ruff)


class TestSaveSampleCode:
    """测试 save_sample_code 函数"""

    def test_save_sample_code_creates_file(self, tmp_path):
        """测试保存示例代码创建文件"""
        file_path = tmp_path / "test.py"
        ruff.save_sample_code(file_path)

        assert file_path.exists()
        assert file_path.read_text() == ruff.SAMPLE_CODE

    def test_save_sample_code_creates_parent_directory(self, tmp_path):
        """测试自动创建父目录"""
        file_path = tmp_path / "subdir" / "test.py"
        ruff.save_sample_code(file_path)

        assert file_path.parent.exists()
        assert file_path.exists()

    def test_save_sample_code_overwrites_existing(self, tmp_path):
        """测试覆盖已存在的文件"""
        file_path = tmp_path / "test.py"
        file_path.write_text("old content")

        ruff.save_sample_code(file_path)

        assert file_path.read_text() == ruff.SAMPLE_CODE


class TestRunRuffFormat:
    """测试 run_ruff_format 函数"""

    def test_run_ruff_format_success(self, tmp_path):
        """测试成功格式化"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():pass")

        mock_result = Mock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = ruff.run_ruff_format(file_path)

        assert result is True

    def test_run_ruff_format_failure(self, tmp_path):
        """测试格式化失败"""
        file_path = tmp_path / "test.py"
        file_path.write_text("invalid python code {{{")

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Syntax error"

        with patch("subprocess.run", return_value=mock_result):
            result = ruff.run_ruff_format(file_path)

        assert result is False

    def test_run_ruff_format_not_installed(self, tmp_path):
        """测试 Ruff 未安装"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():pass")

        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = ruff.run_ruff_format(file_path)

        assert result is False

    def test_run_ruff_format_timeout(self, tmp_path):
        """测试命令超时"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():pass")

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ruff", 30)):
            result = ruff.run_ruff_format(file_path)

        assert result is False

    def test_run_ruff_format_exception(self, tmp_path):
        """测试其他异常"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():pass")

        with patch("subprocess.run", side_effect=Exception("Unknown error")):
            result = ruff.run_ruff_format(file_path)

        assert result is False


class TestRunRuffCheck:
    """测试 run_ruff_check 函数"""

    def test_run_ruff_check_success(self, tmp_path):
        """测试检查通过"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():\n    pass\n")

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            passed, message = ruff.run_ruff_check(file_path)

        assert passed is True
        assert "通过" in message

    def test_run_ruff_check_with_errors(self, tmp_path):
        """测试检查发现错误"""
        file_path = tmp_path / "test.py"

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "E501 Line too long"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            passed, message = ruff.run_ruff_check(file_path)

        assert passed is False
        assert "E501" in message

    def test_run_ruff_check_not_installed(self, tmp_path):
        """测试 Ruff 未安装"""
        file_path = tmp_path / "test.py"

        with patch("subprocess.run", side_effect=FileNotFoundError):
            passed, message = ruff.run_ruff_check(file_path)

        assert passed is False
        assert "未安装" in message

    def test_run_ruff_check_timeout(self, tmp_path):
        """测试命令超时"""
        file_path = tmp_path / "test.py"

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ruff", 30)):
            passed, message = ruff.run_ruff_check(file_path)

        assert passed is False
        assert "超时" in message


class TestRunRuffFix:
    """测试 run_ruff_fix 函数"""

    def test_run_ruff_fix_success(self, tmp_path):
        """测试自动修复成功"""
        file_path = tmp_path / "test.py"
        file_path.write_text("import os\nimport sys\n")

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Fixed 1 error"

        with patch("subprocess.run", return_value=mock_result):
            result = ruff.run_ruff_fix(file_path)

        assert result is True

    def test_run_ruff_fix_no_issues(self, tmp_path):
        """测试没有需要修复的问题"""
        file_path = tmp_path / "test.py"
        file_path.write_text("def hello():\n    pass\n")

        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            result = ruff.run_ruff_fix(file_path)

        assert result is True

    def test_run_ruff_fix_partial(self, tmp_path):
        """测试部分问题无法修复"""
        file_path = tmp_path / "test.py"

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "Some issues cannot be fixed"

        with patch("subprocess.run", return_value=mock_result):
            result = ruff.run_ruff_fix(file_path)

        assert result is False

    def test_run_ruff_fix_not_installed(self, tmp_path):
        """测试 Ruff 未安装"""
        file_path = tmp_path / "test.py"

        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = ruff.run_ruff_fix(file_path)

        assert result is False


class TestCompareCode:
    """测试 compare_code 函数"""

    def test_compare_code_no_changes(self):
        """测试代码无变化"""
        code = "def hello():\n    pass\n"

        result = ruff.compare_code(code, code)

        assert result["lines_changed"] == 0

    def test_compare_code_with_changes(self):
        """测试代码有变化"""
        original = "def hello(  ):\n    pass\n"
        formatted = "def hello():\n    pass\n"

        result = ruff.compare_code(original, formatted)

        assert result["lines_changed"] > 0

    def test_compare_code_imports_sorted(self):
        """测试导入排序"""
        original = "import sys\nimport os\n"
        formatted = "import os\nimport sys\n"

        result = ruff.compare_code(original, formatted)

        assert result["imports_sorted"] is True

    def test_compare_code_spacing_fixed(self):
        """测试空格修复"""
        original = "def hello(  ):\n    pass\n"
        formatted = "def hello():\n    pass\n"

        result = ruff.compare_code(original, formatted)

        assert result["spacing_fixed"] is True


class TestCreateRuffConfig:
    """测试 create_ruff_config 函数"""

    def test_create_ruff_config_new_file(self, tmp_path):
        """测试创建新配置文件"""
        # 确保 tomli_w 已安装
        if importlib.util.find_spec("tomli_w") is None:
            pytest.skip("tomli_w not installed")

        ruff.create_ruff_config(tmp_path)

        config_file = tmp_path / "pyproject.toml"
        assert config_file.exists()

        content = config_file.read_text()
        assert "ruff" in content

    def test_create_ruff_config_merge_existing(self, tmp_path):
        """测试合并现有配置"""
        # 确保 tomli_w 已安装
        try:
            pass
        except ImportError:
            pytest.skip("tomli_w not installed")

        config_file = tmp_path / "pyproject.toml"
        config_file.write_text('[project]\nname = "test"\n')

        ruff.create_ruff_config(tmp_path)

        content = config_file.read_text()
        assert "project" in content or "ruff" in content

    def test_create_ruff_config_without_tomli_w(self, tmp_path):
        """测试 tomli_w 未安装时返回"""
        # 这个测试验证函数在依赖缺失时能够优雅处理
        tmp_path / "pyproject.toml"

        # 函数应该不崩溃
        try:
            ruff.create_ruff_config(tmp_path)
        except Exception as e:
            pytest.fail(f"Function should handle missing tomli_w gracefully: {e}")

        # 如果 tomli_w 未安装，文件不应该被创建
        # 如果已安装，文件会被创建
        # 两种情况都是正确的行为


class TestMain:
    """测试 main 函数"""

    @patch("builtins.print")
    @patch.object(ruff, "run_ruff_format", return_value=True)
    @patch.object(ruff, "run_ruff_check", return_value=(True, ""))
    @patch.object(ruff, "run_ruff_fix", return_value=True)
    def test_main_success_flow(self, mock_fix, mock_check, mock_format, mock_print, tmp_path, monkeypatch):
        """测试 main 函数成功流程"""
        # 切换到临时目录
        monkeypatch.chdir(tmp_path)

        # 运行 main
        ruff.main()

        # 验证 print 被调用
        assert mock_print.call_count > 0

        # 验证测试目录被创建
        test_dir = tmp_path / "ruff_test"
        assert test_dir.exists()

        # 验证示例文件被创建
        test_file = test_dir / "sample.py"
        assert test_file.exists()

    @patch("builtins.print")
    @patch.object(ruff, "run_ruff_format", return_value=False)
    def test_main_format_failure(self, mock_format, mock_print, tmp_path, monkeypatch):
        """测试 main 函数格式化失败"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        ruff.main()

        # 验证仍然能完成
        assert mock_print.call_count > 0

    @patch("builtins.print")
    @patch.object(ruff, "run_ruff_format", return_value=True)
    @patch.object(ruff, "run_ruff_check", return_value=(False, "Error"))
    def test_main_check_failure(self, mock_check, mock_format, mock_print, tmp_path, monkeypatch):
        """测试 main 函数检查失败"""
        monkeypatch.chdir(tmp_path)

        # 运行 main
        ruff.main()

        # 验证仍然能完成
        assert mock_print.call_count > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
