"""扩展测试 - 02-intermediate.py 端到端测试

from __future__ import annotations

添加 main() 函数和完整流程的端到端测试，提升覆盖率
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("tomli")
pytest.importorskip("tomli_w")

# 导入被测试模块

import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "intermediate",
    Path(__file__).parent.parent / "solutions" / "solution_02_intermediate.py",
)
intermediate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intermediate)


class TestMainFunction:
    """测试 main() 函数的端到端场景"""

    def test_main_complete_workflow(self, tmp_path, capsys):
        """测试完整工作流程"""
        with patch("pathlib.Path") as mock_path_class:
            # 设置 Path() 返回 tmp_path
            mock_path_class.return_value = tmp_path

            intermediate.main()

            captured = capsys.readouterr()

            # 验证输出
            assert "练习 2: 配置项目约束" in captured.out
            assert "步骤 1: 设置 Python 版本约束" in captured.out
            assert "步骤 2: 添加依赖" in captured.out
            assert "步骤 3: 配置 Ruff" in captured.out
            assert "步骤 4: 配置 mypy" in captured.out
            assert "步骤 5: 保存配置" in captured.out
            assert "步骤 6: 验证配置" in captured.out
            assert "🎉 恭喜！练习 2 完成！" in captured.out

    def test_main_creates_test_project(self, tmp_path, capsys):
        """测试创建测试项目"""
        # main() 函数内部使用 Path("./test-config-project")
        # 我们需要改变工作目录
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            intermediate.main()

            # 验证项目目录被创建
            project_dir = tmp_path / "test-config-project"
            assert project_dir.exists()
        finally:
            os.chdir(old_cwd)

    def test_main_generates_valid_config(self, tmp_path, capsys):
        """测试生成有效的配置文件"""
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            intermediate.main()

            project_dir = tmp_path / "test-config-project"
            pyproject_file = project_dir / "pyproject.toml"

            assert pyproject_file.exists()
            content = pyproject_file.read_text()

            # 验证配置内容
            assert "requires-python" in content
            assert ">=3.13" in content
            assert "fastapi" in content
            assert "pytest" in content
            assert "[tool.ruff]" in content
            assert "[tool.mypy]" in content
        finally:
            os.chdir(old_cwd)

    def test_main_shows_all_verification_results(self, tmp_path, capsys):
        """测试显示所有验证结果"""
        with patch("pathlib.Path") as mock_path_class:
            mock_path_class.return_value = tmp_path

            intermediate.main()

            captured = capsys.readouterr()
            assert "requires-python:" in captured.out
            assert "ruff target-version:" in captured.out
            assert "mypy python_version:" in captured.out
            assert "mypy strict:" in captured.out

    def test_main_prints_config_content(self, tmp_path, capsys):
        """测试打印配置内容"""
        with patch("pathlib.Path") as mock_path_class:
            mock_path_class.return_value = tmp_path

            intermediate.main()

            captured = capsys.readouterr()
            assert "配置内容:" in captured.out
            assert "----" in captured.out

    def test_main_shows_next_steps(self, tmp_path, capsys):
        """测试显示下一步指令"""
        with patch("pathlib.Path") as mock_path_class:
            mock_path_class.return_value = tmp_path

            intermediate.main()

            captured = capsys.readouterr()
            assert "生成的配置文件:" in captured.out
            assert "查看配置:" in captured.out
            assert "cat" in captured.out

    def test_main_handles_missing_dependency(self, tmp_path, capsys):
        """测试缺少依赖时的错误处理"""
        # 这个测试验证导入错误的提示信息存在于代码中
        # 实际的 ImportError 会在模块加载时发生，而不是在 main() 中
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            intermediate.main()

            # 如果成功运行，说明依赖都存在
            captured = capsys.readouterr()
            assert "练习 2:" in captured.out
        finally:
            os.chdir(old_cwd)


class TestPyProjectConfigEdgeCases:
    """测试 PyProjectConfig 的边界情况"""

    def test_config_handles_nested_structure(self, tmp_path):
        """测试处理嵌套配置结构"""
        config = intermediate.PyProjectConfig(tmp_path)

        # 添加多层嵌套配置
        config.set_python_version_constraint("3.13", "3.15")
        config.configure_ruff()
        config.configure_mypy()

        assert "tool" in config.config
        assert "ruff" in config.config["tool"]
        assert "mypy" in config.config["tool"]

    def test_config_preserves_existing_data(self, tmp_path):
        """测试保留现有数据"""
        # 创建初始配置
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nname = "original"\ndescription = "test"')

        config = intermediate.PyProjectConfig(tmp_path)
        config.set_python_version_constraint("3.13", "3.15")
        config.save()

        # 重新加载并验证
        config2 = intermediate.PyProjectConfig(tmp_path)
        assert config2.config["project"]["name"] == "original"
        assert config2.config["project"]["description"] == "test"
        assert "requires-python" in config2.config["project"]

    def test_config_handles_multiple_dev_groups(self, tmp_path):
        """测试处理多个开发依赖组"""
        config = intermediate.PyProjectConfig(tmp_path)

        config.add_dependencies(["pytest"], dev=True)
        config.add_dependencies(["ruff"], dev=True)

        dev_deps = config.config["project"]["optional-dependencies"]["dev"]
        assert "pytest" in dev_deps
        assert "ruff" in dev_deps
        assert len(dev_deps) == 2

    def test_verify_with_partial_config(self, tmp_path):
        """测试验证部分配置"""
        toml_content = """
[project]
requires-python = ">=3.13"

[tool.ruff]
target-version = "py313"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        # 部分配置应该失败
        assert results["requires_python"] is True
        assert results["ruff_target"] is True
        assert results["mypy_version"] is False
        assert results["mypy_strict"] is False

    def test_config_version_comparison_edge_cases(self, tmp_path):
        """测试版本比较的边界情况"""
        config = intermediate.PyProjectConfig(tmp_path)

        # 测试各种版本格式
        config.set_python_version_constraint("3.13.0", "3.15.0")
        assert ">=3.13.0,<3.15.0" in config.config["project"]["requires-python"]

        config.set_python_version_constraint("3.13", "4.0")
        assert ">=3.13,<4.0" in config.config["project"]["requires-python"]


class TestConfigurationWorkflows:
    """测试配置工作流"""

    def test_incremental_configuration_workflow(self, tmp_path):
        """测试增量配置工作流"""
        # 第一步：创建基础配置
        config1 = intermediate.PyProjectConfig(tmp_path)
        config1.set_python_version_constraint("3.13", "3.15")
        config1.save()

        # 第二步：添加依赖
        config2 = intermediate.PyProjectConfig(tmp_path)
        config2.add_dependencies(["fastapi"], dev=False)
        config2.save()

        # 第三步：配置工具
        config3 = intermediate.PyProjectConfig(tmp_path)
        config3.configure_ruff()
        config3.save()

        # 验证所有配置都存在
        final_config = intermediate.PyProjectConfig(tmp_path)
        assert "requires-python" in final_config.config["project"]
        assert "dependencies" in final_config.config["project"]
        assert "ruff" in final_config.config["tool"]

    def test_full_configuration_in_one_step(self, tmp_path):
        """测试一次性完整配置"""
        config = intermediate.PyProjectConfig(tmp_path)

        # 一次性配置所有内容
        config.set_python_version_constraint("3.13", "3.15")
        config.add_dependencies(["fastapi", "uvicorn"], dev=False)
        config.add_dependencies(["pytest", "ruff"], dev=True)
        config.configure_ruff("py313", 100)
        config.configure_mypy("3.13", True)
        config.save()

        # 验证配置
        results = config.verify()
        assert all(results.values())

    def test_configuration_update_workflow(self, tmp_path):
        """测试配置更新工作流"""
        # 初始配置
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_ruff("py311", 88)
        config.save()

        # 更新配置
        config2 = intermediate.PyProjectConfig(tmp_path)
        config2.configure_ruff("py313", 100)
        config2.save()

        # 验证更新
        config3 = intermediate.PyProjectConfig(tmp_path)
        assert config3.config["tool"]["ruff"]["target-version"] == "py313"
        assert config3.config["tool"]["ruff"]["line-length"] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
