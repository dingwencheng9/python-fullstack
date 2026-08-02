"""测试 solutions/02-intermediate.py - 配置项目约束（中级）

from __future__ import annotations

测试覆盖:
- PyProjectConfig.__init__()
- PyProjectConfig.set_python_version_constraint()
- PyProjectConfig.add_dependencies()
- PyProjectConfig.configure_ruff()
- PyProjectConfig.configure_mypy()
- PyProjectConfig.save()
- PyProjectConfig.verify()
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("tomli")
pytest.importorskip("tomli_w")
# 导入被测试模块
# 动态导入 02-intermediate.py (因为文件名包含连字符)
import importlib.util  # noqa: E402

import tomli  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "intermediate",
    Path(__file__).parent.parent / "solutions" / "solution_02_intermediate.py",
)
intermediate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intermediate)


class TestPyProjectConfigInit:
    """测试 PyProjectConfig 初始化"""

    def test_init_with_existing_file(self, tmp_path):
        """测试从已存在的 pyproject.toml 初始化"""
        toml_file = tmp_path / "pyproject.toml"
        toml_content = """
[project]
name = "test-project"
version = "1.0.0"
"""
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)

        assert config.project_path == tmp_path
        assert config.toml_path == toml_file
        assert "project" in config.config
        assert config.config["project"]["name"] == "test-project"

    def test_init_without_existing_file(self, tmp_path):
        """测试没有 pyproject.toml 时初始化"""
        config = intermediate.PyProjectConfig(tmp_path)

        assert config.project_path == tmp_path
        assert config.config == {}

    def test_init_path_assignment(self, tmp_path):
        """测试路径赋值正确"""
        config = intermediate.PyProjectConfig(tmp_path)

        assert isinstance(config.project_path, Path)
        assert isinstance(config.toml_path, Path)
        assert config.toml_path.name == "pyproject.toml"


class TestSetPythonVersionConstraint:
    """测试 set_python_version_constraint()"""

    def test_set_version_constraint_new_project(self, tmp_path):
        """测试在新项目中设置 Python 版本约束"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.set_python_version_constraint("3.13", "3.15")

        assert "project" in config.config
        assert config.config["project"]["requires-python"] == ">=3.13,<3.15"

    def test_set_version_constraint_existing_project(self, tmp_path):
        """测试在已有项目中设置 Python 版本约束"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"')

        config = intermediate.PyProjectConfig(tmp_path)
        config.set_python_version_constraint("3.11", "3.13")

        assert config.config["project"]["requires-python"] == ">=3.11,<3.13"
        assert config.config["project"]["name"] == "test"

    def test_set_version_constraint_format(self, tmp_path):
        """测试版本约束格式正确"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.set_python_version_constraint("3.10", "4.0")

        requires = config.config["project"]["requires-python"]
        assert requires.startswith(">=")
        assert ",<" in requires

    def test_set_version_constraint_overwrites_existing(self, tmp_path):
        """测试覆盖已存在的版本约束"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.set_python_version_constraint("3.10", "3.13")
        config.set_python_version_constraint("3.13", "3.15")

        assert config.config["project"]["requires-python"] == ">=3.13,<3.15"


class TestAddDependencies:
    """测试 add_dependencies()"""

    def test_add_production_dependencies(self, tmp_path):
        """测试添加生产依赖"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.add_dependencies(["fastapi>=0.100.0", "uvicorn"], dev=False)

        assert "dependencies" in config.config["project"]
        assert "fastapi>=0.100.0" in config.config["project"]["dependencies"]
        assert "uvicorn" in config.config["project"]["dependencies"]

    def test_add_dev_dependencies(self, tmp_path):
        """测试添加开发依赖"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.add_dependencies(["pytest", "ruff"], dev=True)

        assert "optional-dependencies" in config.config["project"]
        assert "dev" in config.config["project"]["optional-dependencies"]
        assert "pytest" in config.config["project"]["optional-dependencies"]["dev"]

    def test_add_dependencies_multiple_times(self, tmp_path):
        """测试多次添加依赖"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.add_dependencies(["fastapi"], dev=False)
        config.add_dependencies(["uvicorn"], dev=False)

        deps = config.config["project"]["dependencies"]
        assert len(deps) == 2
        assert "fastapi" in deps
        assert "uvicorn" in deps

    def test_add_empty_dependencies(self, tmp_path):
        """测试添加空依赖列表"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.add_dependencies([], dev=False)

        assert config.config["project"]["dependencies"] == []

    def test_add_dependencies_creates_structure(self, tmp_path):
        """测试添加依赖时创建必要的结构"""
        config = intermediate.PyProjectConfig(tmp_path)
        assert config.config == {}

        config.add_dependencies(["pytest"], dev=True)

        assert "project" in config.config
        assert "optional-dependencies" in config.config["project"]
        assert "dev" in config.config["project"]["optional-dependencies"]


class TestConfigureRuff:
    """测试 configure_ruff()"""

    def test_configure_ruff_default_values(self, tmp_path):
        """测试使用默认值配置 Ruff"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_ruff()

        ruff_config = config.config["tool"]["ruff"]
        assert ruff_config["target-version"] == "py313"
        assert ruff_config["line-length"] == 100

    def test_configure_ruff_custom_values(self, tmp_path):
        """测试使用自定义值配置 Ruff"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_ruff(target_version="py311", line_length=88)

        ruff_config = config.config["tool"]["ruff"]
        assert ruff_config["target-version"] == "py311"
        assert ruff_config["line-length"] == 88

    def test_configure_ruff_select_rules(self, tmp_path):
        """测试 Ruff 规则选择"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_ruff()

        select = config.config["tool"]["ruff"]["select"]
        assert "E" in select  # pycodestyle errors
        assert "F" in select  # pyflakes
        assert "I" in select  # isort
        assert "N" in select  # pep8-naming
        assert "W" in select  # pycodestyle warnings

    def test_configure_ruff_creates_structure(self, tmp_path):
        """测试配置 Ruff 时创建必要的结构"""
        config = intermediate.PyProjectConfig(tmp_path)
        assert config.config == {}

        config.configure_ruff()

        assert "tool" in config.config
        assert "ruff" in config.config["tool"]


class TestConfigureMypy:
    """测试 configure_mypy()"""

    def test_configure_mypy_default_values(self, tmp_path):
        """测试使用默认值配置 mypy"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_mypy()

        mypy_config = config.config["tool"]["mypy"]
        assert mypy_config["python_version"] == "3.13"
        assert mypy_config["strict"] is True
        assert mypy_config["warn_unused_ignores"] is True

    def test_configure_mypy_custom_values(self, tmp_path):
        """测试使用自定义值配置 mypy"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_mypy(python_version="3.11", strict=False)

        mypy_config = config.config["tool"]["mypy"]
        assert mypy_config["python_version"] == "3.11"
        assert mypy_config["strict"] is False

    def test_configure_mypy_strict_mode(self, tmp_path):
        """测试 mypy strict 模式配置"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_mypy(strict=True)

        assert config.config["tool"]["mypy"]["strict"] is True

    def test_configure_mypy_creates_structure(self, tmp_path):
        """测试配置 mypy 时创建必要的结构"""
        config = intermediate.PyProjectConfig(tmp_path)
        assert config.config == {}

        config.configure_mypy()

        assert "tool" in config.config
        assert "mypy" in config.config["tool"]


class TestSave:
    """测试 save()"""

    def test_save_creates_file(self, tmp_path):
        """测试保存时创建文件"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.config = {"project": {"name": "test"}}
        config.save()

        toml_file = tmp_path / "pyproject.toml"
        assert toml_file.exists()

    def test_save_writes_correct_content(self, tmp_path):
        """测试保存的内容正确"""
        config = intermediate.PyProjectConfig(tmp_path)
        config.config = {"project": {"name": "test-project", "version": "1.0.0"}}
        config.save()

        toml_file = tmp_path / "pyproject.toml"
        with open(toml_file, "rb") as f:
            saved_config = tomli.load(f)

        assert saved_config["project"]["name"] == "test-project"
        assert saved_config["project"]["version"] == "1.0.0"

    def test_save_overwrites_existing(self, tmp_path):
        """测试保存时覆盖已存在的文件"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nname = "old"')

        config = intermediate.PyProjectConfig(tmp_path)
        config.config = {"project": {"name": "new"}}
        config.save()

        with open(toml_file, "rb") as f:
            saved_config = tomli.load(f)

        assert saved_config["project"]["name"] == "new"


class TestVerify:
    """测试 verify()"""

    def test_verify_all_pass(self, tmp_path):
        """测试所有验证通过"""
        toml_content = """
[project]
requires-python = ">=3.13,<3.15"

[tool.ruff]
target-version = "py313"

[tool.mypy]
python_version = "3.13"
strict = true
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert results["requires_python"] is True
        assert results["ruff_target"] is True
        assert results["mypy_version"] is True
        assert results["mypy_strict"] is True

    def test_verify_missing_requires_python(self, tmp_path):
        """测试缺少 requires-python"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"')

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert results["requires_python"] is False

    def test_verify_wrong_ruff_target(self, tmp_path):
        """测试 Ruff target-version 错误"""
        toml_content = """
[tool.ruff]
target-version = "py311"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert results["ruff_target"] is False

    def test_verify_wrong_mypy_version(self, tmp_path):
        """测试 mypy python_version 错误"""
        toml_content = """
[tool.mypy]
python_version = "3.11"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert results["mypy_version"] is False

    def test_verify_mypy_not_strict(self, tmp_path):
        """测试 mypy strict 未启用"""
        toml_content = """
[tool.mypy]
python_version = "3.13"
strict = false
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert results["mypy_strict"] is False

    def test_verify_empty_config(self, tmp_path):
        """测试空配置"""
        config = intermediate.PyProjectConfig(tmp_path)
        results = config.verify()

        assert all(value is False for value in results.values())


# 集成测试
class TestIntegration:
    """集成测试"""

    def test_complete_configuration_workflow(self, tmp_path):
        """测试完整配置流程"""
        # 创建基础文件
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\nversion = "0.1.0"')

        # 初始化配置
        config = intermediate.PyProjectConfig(tmp_path)

        # 设置 Python 版本约束
        config.set_python_version_constraint("3.13", "3.15")

        # 添加依赖
        config.add_dependencies(["fastapi>=0.136.0"], dev=False)
        config.add_dependencies(["pytest>=8.0.0", "ruff>=0.8.0"], dev=True)

        # 配置工具
        config.configure_ruff("py313", 100)
        config.configure_mypy("3.13", True)

        # 保存配置
        config.save()

        # 验证配置
        results = config.verify()

        # 断言所有配置正确
        assert all(results.values())

        # 验证文件内容
        with open(toml_file, "rb") as f:
            saved_config = tomli.load(f)

        assert saved_config["project"]["requires-python"] == ">=3.13,<3.15"
        assert "fastapi>=0.136.0" in saved_config["project"]["dependencies"]
        assert saved_config["tool"]["ruff"]["target-version"] == "py313"
        assert saved_config["tool"]["mypy"]["python_version"] == "3.13"

    def test_incremental_configuration(self, tmp_path):
        """测试增量配置"""
        config = intermediate.PyProjectConfig(tmp_path)

        # 分步配置
        config.set_python_version_constraint("3.13", "3.15")
        config.save()

        config = intermediate.PyProjectConfig(tmp_path)
        config.add_dependencies(["fastapi"], dev=False)
        config.save()

        config = intermediate.PyProjectConfig(tmp_path)
        config.configure_ruff()
        config.save()

        # 验证所有配置都保留
        config = intermediate.PyProjectConfig(tmp_path)
        assert ">=3.13" in config.config["project"]["requires-python"]
        assert "fastapi" in config.config["project"]["dependencies"]
        assert "ruff" in config.config["tool"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
