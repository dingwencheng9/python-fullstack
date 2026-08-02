"""测试 examples/example_01_uv_workflow_advanced.py - uv 高级工作流

from __future__ import annotations

测试覆盖:
- run_command()
- demo_uv_lock_workflow()
- demo_uv_sync_workflow()
- demo_dependency_groups()
- demo_uv_pip_compile()
- demo_workspace_management()
- generate_all_workflows()
"""

# 导入被测试模块
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

spec = importlib.util.spec_from_file_location(
    "uv_advanced",
    Path(__file__).parent.parent / "examples" / "example_01_uv_workflow_advanced.py",
)
uv_advanced = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uv_advanced)


class TestRunCommand:
    """测试 run_command() 函数"""

    def test_successful_command(self, capsys):
        """测试命令执行成功"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Success output"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            success, output = uv_advanced.run_command("echo test", "测试命令")

        assert success is True
        assert output == "Success output"
        captured = capsys.readouterr()
        assert "测试命令" in captured.out
        assert "echo test" in captured.out

    def test_failed_command(self, capsys):
        """测试命令执行失败"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "Error message"
            mock_run.return_value = mock_result

            success, output = uv_advanced.run_command("false", "失败命令")

        assert success is False
        assert output == ""

    def test_command_with_output(self, capsys):
        """测试命令输出显示"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Line 1\nLine 2\n"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.run_command("ls", "列出文件")

        captured = capsys.readouterr()
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out


class TestDemoUvLockWorkflow:
    """测试 demo_uv_lock_workflow() 函数"""

    def test_generates_lock_file(self, tmp_path, capsys):
        """测试生成 uv.lock 文件"""
        # 创建模拟的 uv.lock 文件
        lock_file = tmp_path / "uv.lock"
        lock_content = "\n".join([f"line {i}" for i in range(30)])
        lock_file.write_text(lock_content)

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Lock file generated"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_lock_workflow(tmp_path)

        captured = capsys.readouterr()
        assert "uv lock" in captured.out
        assert "已生成 uv.lock 文件" in captured.out

    def test_lock_file_content_display(self, tmp_path, capsys):
        """测试显示 lock 文件内容"""
        lock_file = tmp_path / "uv.lock"
        lock_file.write_text("version = 1\npackage = fastapi\n")

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_lock_workflow(tmp_path)

        captured = capsys.readouterr()
        assert "version = 1" in captured.out


class TestDemoUvSyncWorkflow:
    """测试 demo_uv_sync_workflow() 函数"""

    def test_sync_success(self, tmp_path, capsys):
        """测试依赖同步成功"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "Synced successfully"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_sync_workflow(tmp_path)

        captured = capsys.readouterr()
        assert "uv sync" in captured.out
        assert "依赖同步成功" in captured.out

    def test_sync_failure(self, tmp_path, capsys):
        """测试依赖同步失败"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "Sync failed"
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_sync_workflow(tmp_path)

        captured = capsys.readouterr()
        assert "uv sync" in captured.out


class TestDemoDependencyGroups:
    """测试 demo_dependency_groups() 函数"""

    def test_adds_test_group(self, tmp_path, capsys):
        """测试添加测试依赖组"""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[dependency-groups]\ntest = ['pytest']\n")

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_dependency_groups(tmp_path)

        captured = capsys.readouterr()
        assert "test" in captured.out

    def test_adds_docs_group(self, tmp_path, capsys):
        """测试添加文档依赖组"""
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[dependency-groups]\ndocs = ['mkdocs']\n")

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_dependency_groups(tmp_path)

        captured = capsys.readouterr()
        assert "依赖组" in captured.out


class TestDemoUvPipCompile:
    """测试 demo_uv_pip_compile() 函数"""

    def test_generates_requirements_txt(self, tmp_path, capsys):
        """测试生成 requirements.txt"""
        req_file = tmp_path / "requirements.txt"
        req_content = "\n".join([f"package{i}==1.0.{i}" for i in range(20)])
        req_file.write_text(req_content)

        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_pip_compile(tmp_path)

        captured = capsys.readouterr()
        assert "requirements.txt" in captured.out

    def test_generates_dev_requirements(self, tmp_path, capsys):
        """测试生成开发依赖文件"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            uv_advanced.demo_uv_pip_compile(tmp_path)

        captured = capsys.readouterr()
        assert "requirements-dev.txt" in captured.out


class TestDemoWorkspaceManagement:
    """测试 demo_workspace_management() 函数"""

    def test_creates_workspace_structure(self, tmp_path, capsys):
        """测试创建 workspace 结构"""
        uv_advanced.demo_workspace_management(tmp_path)

        workspace_dir = tmp_path / "demo-workspace"
        assert workspace_dir.exists()

        workspace_toml = workspace_dir / "pyproject.toml"
        assert workspace_toml.exists()

        content = workspace_toml.read_text()
        assert "tool.uv.workspace" in content
        assert "members" in content

    def test_creates_subprojects(self, tmp_path, capsys):
        """测试创建子项目"""
        uv_advanced.demo_workspace_management(tmp_path)

        backend_dir = tmp_path / "demo-workspace" / "packages" / "backend"
        frontend_dir = tmp_path / "demo-workspace" / "packages" / "frontend"

        assert backend_dir.exists()
        assert frontend_dir.exists()

        backend_toml = backend_dir / "pyproject.toml"
        frontend_toml = frontend_dir / "pyproject.toml"

        assert backend_toml.exists()
        assert frontend_toml.exists()

        backend_content = backend_toml.read_text()
        assert "fastapi" in backend_content

        frontend_content = frontend_toml.read_text()
        assert "jinja2" in frontend_content


class TestShowBestPractices:
    """测试 show_best_practices() 函数"""

    def test_displays_best_practices(self, capsys):
        """测试显示最佳实践"""
        uv_advanced.show_best_practices()

        captured = capsys.readouterr()
        assert "最佳实践" in captured.out
        assert "uv lock" in captured.out
        assert "uv sync" in captured.out
        assert "Workspace" in captured.out


class TestThreadSafety:
    """测试线程安全性（Python 3.14 兼容）"""

    def test_run_command_is_thread_safe(self):
        """测试 run_command 返回不可变数据"""
        with patch("subprocess.run") as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "output"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            result = uv_advanced.run_command("test", "test")

        # 验证返回 tuple（不可变）
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)


class TestIntegration:
    """集成测试"""

    def test_main_function_runs(self, tmp_path, capsys):
        """测试 main() 函数执行"""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            patch("subprocess.run") as mock_run,
        ):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = ""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            # 注意：main() 会创建实际的目录和文件
            # 这里我们只测试它不会崩溃
            try:
                uv_advanced.main()
            except Exception as e:
                pytest.fail(f"main() raised {type(e).__name__}: {e}")

        captured = capsys.readouterr()
        assert "高级工作流演示" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
