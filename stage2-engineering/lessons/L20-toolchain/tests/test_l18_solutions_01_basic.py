"""测试 solutions/01-basic.py - 创建项目环境（基础）

from __future__ import annotations

测试覆盖:
- check_uv_installed()
- create_project()
- create_venv()
- add_dependencies()
- verify_environment()
"""

from __future__ import annotations

# 导入被测试模块
# 动态导入 01-basic.py (因为文件名包含连字符)
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


class TestCheckUvInstalled:
    """测试 check_uv_installed() 函数"""

    def test_uv_installed_successfully(self, capsys):
        """测试 uv 已安装的情况"""
        mock_result = Mock()
        mock_result.stdout = "uv 0.5.0\n"

        with patch("subprocess.run", return_value=mock_result):
            result = basic.check_uv_installed()

        assert result is True
        captured = capsys.readouterr()
        assert "✅ uv 已安装" in captured.out
        assert "0.5.0" in captured.out

    def test_uv_not_installed_file_not_found(self, capsys):
        """测试 uv 未安装（FileNotFoundError）"""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = basic.check_uv_installed()

        assert result is False
        captured = capsys.readouterr()
        assert "❌ uv 未安装" in captured.out

    def test_uv_not_installed_process_error(self, capsys):
        """测试 uv 命令执行失败"""
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "uv")):
            result = basic.check_uv_installed()

        assert result is False
        captured = capsys.readouterr()
        assert "❌ uv 未安装" in captured.out

    def test_uv_version_output_format(self, capsys):
        """测试不同版本输出格式"""
        mock_result = Mock()
        mock_result.stdout = "uv version 0.6.1 (abc123)\n"

        with patch("subprocess.run", return_value=mock_result):
            result = basic.check_uv_installed()

        assert result is True


class TestCreateProject:
    """测试 create_project() 函数"""

    def test_create_project_successfully(self, tmp_path):
        """测试成功创建项目"""
        project_name = "test-project"

        with (
            patch("subprocess.run") as mock_run,
            patch("pathlib.Path.cwd", return_value=tmp_path),
        ):
            result = basic.create_project(project_name)

        expected_path = tmp_path / project_name
        assert result == expected_path
        assert expected_path.exists()

        # 验证调用了 uv init
        mock_run.assert_called_once()
        args = mock_run.call_args
        assert args[0][0] == ["uv", "init"]

    def test_create_project_existing_directory(self, tmp_path):
        """测试项目目录已存在的情况"""
        project_name = "existing-project"
        existing_dir = tmp_path / project_name
        existing_dir.mkdir()

        with patch("subprocess.run"), patch("pathlib.Path.cwd", return_value=tmp_path):
            result = basic.create_project(project_name)

        assert result == existing_dir
        assert existing_dir.exists()

    def test_create_project_subprocess_error(self, tmp_path):
        """测试 uv init 失败"""
        project_name = "test-project"

        with (
            patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "uv")),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            pytest.raises(subprocess.CalledProcessError),
        ):
            basic.create_project(project_name)

    def test_create_project_returns_path_object(self, tmp_path):
        """测试返回值类型为 Path"""
        with patch("subprocess.run"), patch("pathlib.Path.cwd", return_value=tmp_path):
            result = basic.create_project("test")

        assert isinstance(result, Path)


class TestCreateVenv:
    """测试 create_venv() 函数"""

    def test_create_venv_default_version(self, tmp_path):
        """测试使用默认 Python 版本创建虚拟环境"""
        with patch("subprocess.run") as mock_run:
            result = basic.create_venv(tmp_path)

        assert result is True
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args == ["uv", "venv", "--python", "3.13"]

    def test_create_venv_custom_version(self, tmp_path):
        """测试使用自定义 Python 版本"""
        with patch("subprocess.run") as mock_run:
            result = basic.create_venv(tmp_path, python_version="3.12")

        assert result is True
        args = mock_run.call_args[0][0]
        assert args == ["uv", "venv", "--python", "3.12"]

    def test_create_venv_failure(self, tmp_path):
        """测试创建虚拟环境失败"""
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "uv")):
            result = basic.create_venv(tmp_path)

        assert result is False

    def test_create_venv_passes_project_path(self, tmp_path):
        """测试正确传递项目路径"""
        with patch("subprocess.run") as mock_run:
            basic.create_venv(tmp_path)

        assert mock_run.call_args.kwargs["cwd"] == tmp_path


class TestAddDependencies:
    """测试 add_dependencies() 函数"""

    def test_add_dependencies_successfully(self, tmp_path):
        """测试成功添加依赖"""
        with patch("subprocess.run") as mock_run:
            result = basic.add_dependencies(tmp_path)

        assert result is True
        assert mock_run.call_count == 2  # 生产依赖 + 开发依赖

    def test_add_production_dependencies(self, tmp_path):
        """测试添加生产依赖"""
        with patch("subprocess.run") as mock_run:
            basic.add_dependencies(tmp_path)

        # 第一次调用应该是添加生产依赖
        first_call = mock_run.call_args_list[0]
        args = first_call[0][0]
        assert "fastapi" in args
        assert "uvicorn" in args
        assert "--dev" not in args

    def test_add_dev_dependencies(self, tmp_path):
        """测试添加开发依赖"""
        with patch("subprocess.run") as mock_run:
            basic.add_dependencies(tmp_path)

        # 第二次调用应该是添加开发依赖
        second_call = mock_run.call_args_list[1]
        args = second_call[0][0]
        assert "--dev" in args
        assert "pytest" in args
        assert "ruff" in args
        assert "mypy" in args

    def test_add_dependencies_failure_production(self, tmp_path):
        """测试添加生产依赖失败"""
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "uv")):
            result = basic.add_dependencies(tmp_path)

        assert result is False

    def test_add_dependencies_failure_dev(self, tmp_path):
        """测试添加开发依赖失败"""
        with patch("subprocess.run") as mock_run:
            # 第一次成功，第二次失败
            mock_run.side_effect = [Mock(), subprocess.CalledProcessError(1, "uv")]
            result = basic.add_dependencies(tmp_path)

        assert result is False


class TestVerifyEnvironment:
    """测试 verify_environment() 函数"""

    def test_verify_all_pass(self, tmp_path):
        """测试所有检查通过"""
        # 创建必要的文件和目录
        (tmp_path / ".venv").mkdir()
        (tmp_path / "pyproject.toml").write_text("")

        mock_result = Mock()
        mock_result.stdout = "fastapi\npytest\n"

        with patch("subprocess.run", return_value=mock_result):
            result = basic.verify_environment(tmp_path)

        assert result["venv"] is True
        assert result["pyproject"] is True
        assert result["dependencies"] is True

    def test_verify_missing_venv(self, tmp_path):
        """测试缺少虚拟环境"""
        (tmp_path / "pyproject.toml").write_text("")

        result = basic.verify_environment(tmp_path)

        assert result["venv"] is False

    def test_verify_missing_pyproject(self, tmp_path):
        """测试缺少 pyproject.toml"""
        (tmp_path / ".venv").mkdir()

        result = basic.verify_environment(tmp_path)

        assert result["pyproject"] is False

    def test_verify_missing_dependencies(self, tmp_path):
        """测试缺少依赖"""
        (tmp_path / ".venv").mkdir()
        (tmp_path / "pyproject.toml").write_text("")

        mock_result = Mock()
        mock_result.stdout = "some-other-package\n"

        with patch("subprocess.run", return_value=mock_result):
            result = basic.verify_environment(tmp_path)

        assert result["dependencies"] is False

    def test_verify_subprocess_error(self, tmp_path):
        """测试 subprocess 错误"""
        (tmp_path / ".venv").mkdir()
        (tmp_path / "pyproject.toml").write_text("")

        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "uv")):
            result = basic.verify_environment(tmp_path)

        assert result["dependencies"] is False

    def test_verify_case_insensitive_check(self, tmp_path):
        """测试依赖检查不区分大小写"""
        (tmp_path / ".venv").mkdir()
        (tmp_path / "pyproject.toml").write_text("")

        mock_result = Mock()
        mock_result.stdout = "FastAPI\nPyTest\n"

        with patch("subprocess.run", return_value=mock_result):
            result = basic.verify_environment(tmp_path)

        assert result["dependencies"] is True


# 集成测试
class TestIntegration:
    """集成测试"""

    def test_complete_workflow(self, tmp_path, capsys):
        """测试完整工作流程"""
        with (
            patch("subprocess.run") as mock_run,
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch.object(basic, "check_uv_installed", return_value=True),
        ):
            # 设置 mock 返回值
            mock_result = Mock()
            mock_result.stdout = "fastapi\npytest\n"
            mock_run.return_value = mock_result

            # 执行完整流程
            project_path = basic.create_project("test-project")
            venv_created = basic.create_venv(project_path)
            deps_added = basic.add_dependencies(project_path)

            # 创建验证所需的文件
            (project_path / ".venv").mkdir()
            (project_path / "pyproject.toml").write_text("")

            verification = basic.verify_environment(project_path)

        # 验证结果
        assert venv_created is True
        assert deps_added is True
        assert all(verification.values())


class TestQualityStrengthening:
    """补充参数化、异常路径和边界场景。"""

    @pytest.mark.parametrize(
        ("python_version", "expected_args"),
        [
            ("3.13", ["uv", "venv", "--python", "3.13"]),
            ("3.13t", ["uv", "venv", "--python", "3.13t"]),
            ("3.12", ["uv", "venv", "--python", "3.12"]),
        ],
    )
    def test_create_venv_uses_requested_python_version(
        self,
        tmp_path: Path,
        python_version: str,
        expected_args: list[str],
    ) -> None:
        """参数化验证虚拟环境命令保留目标 Python 版本。"""
        with patch("subprocess.run") as mock_run:
            assert basic.create_venv(tmp_path, python_version=python_version) is True

        assert mock_run.call_args.args[0] == expected_args
        assert mock_run.call_args.kwargs["cwd"] == tmp_path

    def test_create_project_raises_when_uv_init_fails(self, tmp_path: Path) -> None:
        """异常路径：uv init 失败时向调用方传播错误。"""
        with (
            patch(
                "subprocess.run",
                side_effect=subprocess.CalledProcessError(2, "uv init"),
            ),
            patch("pathlib.Path.cwd", return_value=tmp_path),
            pytest.raises(subprocess.CalledProcessError),
        ):
            basic.create_project("broken-project")

    def test_verify_environment_boundary_empty_project(self, tmp_path: Path) -> None:
        """边界场景：空项目目录不会尝试检查依赖且全部验证失败。"""
        with patch("subprocess.run") as mock_run:
            result = basic.verify_environment(tmp_path)

        assert result == {"venv": False, "pyproject": False, "dependencies": False}
        mock_run.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
