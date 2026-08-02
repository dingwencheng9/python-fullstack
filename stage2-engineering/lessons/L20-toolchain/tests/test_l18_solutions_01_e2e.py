"""扩展测试 - 01-basic.py 端到端测试

from __future__ import annotations

添加 main() 函数和完整流程的端到端测试，提升覆盖率
"""

# 导入被测试模块
import importlib.util
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "basic",
    Path(__file__).parent.parent / "solutions" / "solution_01_basic.py",
)
basic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(basic)


class TestMainFunction:
    """测试 main() 函数的端到端场景"""

    def test_main_complete_success_workflow(self, tmp_path, capsys, monkeypatch):
        """测试完整成功流程"""
        # 模拟成功的命令执行
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\nfastapi\npytest\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit") as mock_exit,
        ):
            # 创建必要的目录结构
            project_dir = tmp_path / "my-first-project"
            project_dir.mkdir()
            (project_dir / ".venv").mkdir()
            (project_dir / "pyproject.toml").write_text("")

            # 运行 main
            basic.main()

            captured = capsys.readouterr()

            # 验证输出
            assert "练习 1: 创建项目环境" in captured.out
            assert "步骤 1: 检查 uv 安装" in captured.out
            assert "✅ uv 已安装" in captured.out
            assert "步骤 2: 创建项目" in captured.out
            assert "步骤 3: 创建虚拟环境" in captured.out
            assert "步骤 4: 添加依赖" in captured.out
            assert "步骤 5: 验证环境" in captured.out
            assert "🎉 恭喜！练习 1 完成！" in captured.out

            # 验证没有调用 sys.exit(1)
            mock_exit.assert_not_called()

    def test_main_uv_not_installed(self, capsys, monkeypatch):
        """测试 uv 未安装的场景"""
        with (
            patch("subprocess.run", side_effect=FileNotFoundError),
            pytest.raises(SystemExit) as exc_info,
        ):
            basic.main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "❌ uv 未安装" in captured.out

    def test_main_venv_creation_fails(self, tmp_path, capsys):
        """测试虚拟环境创建失败"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\n"

        call_count = [0]

        def mock_run(*args, **kwargs):
            call_count[0] += 1
            # 第一次调用 (uv --version) 成功
            if call_count[0] == 1 or call_count[0] == 2:
                return mock_result
            # 第三次调用 (uv venv) 失败
            raise subprocess.CalledProcessError(1, "uv")

        with (
            patch("subprocess.run", side_effect=mock_run),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            basic.main()

            captured = capsys.readouterr()
            assert "❌ 虚拟环境创建失败" in captured.out

    def test_main_dependency_installation_fails(self, tmp_path, capsys):
        """测试依赖安装失败"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\n"

        call_count = [0]

        def mock_run(*args, **kwargs):
            call_count[0] += 1
            # 前三次成功 (uv --version, uv init, uv venv)
            if call_count[0] <= 3:
                return mock_result
            # 第四次失败 (uv add)
            raise subprocess.CalledProcessError(1, "uv")

        with (
            patch("subprocess.run", side_effect=mock_run),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            basic.main()

            captured = capsys.readouterr()
            assert "❌ 依赖添加失败" in captured.out

    def test_main_partial_verification_failure(self, tmp_path, capsys):
        """测试部分验证失败"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            # 创建不完整的项目结构（缺少依赖）
            project_dir = tmp_path / "my-first-project"
            project_dir.mkdir()
            (project_dir / ".venv").mkdir()
            (project_dir / "pyproject.toml").write_text("")

            basic.main()

            captured = capsys.readouterr()
            assert "⚠️  部分验证未通过" in captured.out

    def test_main_prints_next_steps(self, tmp_path, capsys):
        """测试成功后打印下一步指令"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\nfastapi\npytest\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            project_dir = tmp_path / "my-first-project"
            project_dir.mkdir()
            (project_dir / ".venv").mkdir()
            (project_dir / "pyproject.toml").write_text("")

            basic.main()

            captured = capsys.readouterr()
            assert "下一步:" in captured.out
            assert "cd" in captured.out
            assert "source .venv/bin/activate" in captured.out
            assert "python --version" in captured.out

    def test_main_creates_project_with_correct_name(self, tmp_path, capsys):
        """测试项目名称正确"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\nfastapi\npytest\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            project_dir = tmp_path / "my-first-project"
            project_dir.mkdir()
            (project_dir / ".venv").mkdir()
            (project_dir / "pyproject.toml").write_text("")

            basic.main()

            captured = capsys.readouterr()
            assert "my-first-project" in captured.out

    def test_main_verification_shows_all_checks(self, tmp_path, capsys):
        """测试验证环节显示所有检查项"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\nfastapi\npytest\n"

        with (
            patch("subprocess.run", return_value=mock_result),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("sys.exit"),
        ):
            project_dir = tmp_path / "my-first-project"
            project_dir.mkdir()
            (project_dir / ".venv").mkdir()
            (project_dir / "pyproject.toml").write_text("")

            basic.main()

            captured = capsys.readouterr()
            assert ".venv 目录:" in captured.out
            assert "pyproject.toml:" in captured.out
            assert "依赖安装:" in captured.out


class TestErrorHandling:
    """测试错误处理和边界情况"""

    def test_create_project_handles_permission_error(self, tmp_path):
        """测试处理权限错误"""
        with (
            patch("pathlib.Path.mkdir", side_effect=PermissionError),
            pytest.raises(PermissionError),
        ):
            basic.create_project("test-project")

    def test_verify_environment_empty_pip_list(self, tmp_path):
        """测试 pip list 为空的情况"""
        (tmp_path / ".venv").mkdir()
        (tmp_path / "pyproject.toml").write_text("")

        mock_result = Mock()
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            result = basic.verify_environment(tmp_path)

        assert result["dependencies"] is False

    def test_add_dependencies_with_network_error(self, tmp_path):
        """测试网络错误情况"""
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "uv", stderr="Network error"),
        ):
            result = basic.add_dependencies(tmp_path)

        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
