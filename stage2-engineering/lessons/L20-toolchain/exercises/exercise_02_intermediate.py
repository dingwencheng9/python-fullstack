"""练习 2: 配置项目约束（中级）。

任务：编辑 pyproject.toml，实现 Python 3.13 现代化环境配置。

学习目标：
- 理解 pyproject.toml 结构
- 配置 Python 版本约束
- 配置工具链（Ruff、mypy）
- 验证配置正确性
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tomli
import tomli_w


class PyProjectConfig:
    """pyproject.toml 配置管理器。"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.toml_path = project_path / "pyproject.toml"
        self.config: dict[str, Any] = {}

        if self.toml_path.exists():
            with self.toml_path.open("rb") as f:
                self.config = tomli.load(f)

    def set_python_version_constraint(self, min_version: str, max_version: str) -> None:
        """设置 project.requires-python，例如 >=3.13,<3.15。"""
        project = self.config.setdefault("project", {})
        project["requires-python"] = f">={min_version},<{max_version}"

    def add_dependencies(self, deps: list[str], dev: bool = False) -> None:
        """添加运行依赖或 dev 可选依赖。"""
        project = self.config.setdefault("project", {})
        if dev:
            optional = project.setdefault("optional-dependencies", {})
            optional.setdefault("dev", [])
            optional["dev"].extend(deps)
        else:
            project.setdefault("dependencies", [])
            project["dependencies"].extend(deps)

    def configure_ruff(self, target_version: str = "py313", line_length: int = 100) -> None:
        """配置 Ruff 的目标版本、行宽和基础规则。"""
        tool = self.config.setdefault("tool", {})
        ruff = tool.setdefault("ruff", {})
        ruff["target-version"] = target_version
        ruff["line-length"] = line_length
        ruff["select"] = ["E", "F", "I", "N", "W"]

    def configure_mypy(self, python_version: str = "3.13", strict: bool = True) -> None:
        """配置 mypy 的 Python 版本与严格模式。"""
        tool = self.config.setdefault("tool", {})
        mypy = tool.setdefault("mypy", {})
        mypy["python_version"] = python_version
        mypy["strict"] = strict
        mypy["warn_unused_ignores"] = True

    def save(self) -> None:
        """保存配置到文件。"""
        with self.toml_path.open("wb") as f:
            tomli_w.dump(self.config, f)

    def verify(self) -> dict[str, bool]:
        """验证关键配置是否正确。"""
        project = self.config.get("project", {})
        tool = self.config.get("tool", {})
        ruff = tool.get("ruff", {})
        mypy = tool.get("mypy", {})
        requires_python = project.get("requires-python", "")

        return {
            "requires_python": ">=3.13" in requires_python,
            "ruff_target": ruff.get("target-version") == "py313",
            "mypy_version": mypy.get("python_version") == "3.13",
            "mypy_strict": mypy.get("strict") is True,
        }


def main() -> None:
    """运行练习自检。"""
    print("=" * 60)
    print("练习 2: 配置项目约束")
    print("=" * 60)
    print()

    project_path = Path("./test-config-project")
    project_path.mkdir(exist_ok=True)

    pyproject_file = project_path / "pyproject.toml"
    pyproject_file.write_text(
        """[project]
name = "test-project"
version = "0.1.0"
""",
        encoding="utf-8",
    )

    print("步骤 1: 设置 Python 版本约束")
    config = PyProjectConfig(project_path)
    config.set_python_version_constraint("3.13", "3.15")
    print("✅ Python 版本约束设置成功")
    print()

    print("步骤 2: 添加依赖")
    config.add_dependencies(["fastapi>=0.136.0", "uvicorn[standard]>=0.30.0"], dev=False)
    config.add_dependencies(["pytest>=8.0.0", "ruff>=0.8.0", "mypy>=1.13.0"], dev=True)
    print("✅ 依赖添加成功")
    print()

    print("步骤 3: 配置 Ruff")
    config.configure_ruff("py313", 100)
    print("✅ Ruff 配置成功")
    print()

    print("步骤 4: 配置 mypy")
    config.configure_mypy("3.13", True)
    print("✅ mypy 配置成功")
    print()

    print("步骤 5: 保存配置")
    config.save()
    print("✅ 配置已保存到 pyproject.toml")
    print()

    print("步骤 6: 验证配置")
    results = config.verify()
    print(f"  requires-python: {'✅' if results['requires_python'] else '❌'}")
    print(f"  ruff target-version: {'✅' if results['ruff_target'] else '❌'}")
    print(f"  mypy python_version: {'✅' if results['mypy_version'] else '❌'}")
    print(f"  mypy strict: {'✅' if results['mypy_strict'] else '❌'}")

    if not all(results.values()):
        raise SystemExit("部分验证未通过，请检查实现")

    print()
    print("🎉 恭喜！练习 2 完成！")


if __name__ == "__main__":
    main()
