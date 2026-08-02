"""练习 2: 配置项目约束（中级）- 参考答案

from __future__ import annotations

本文件提供练习 2 的完整实现，供学习参考。

【解题思路】
1. PyProjectConfig 类设计：
   - __init__: 初始化时读取已存在的 pyproject.toml（使用 tomllib）
   - 使用 dict[str, object] 存储配置树结构（Python 3.13+ 推荐）
2. set_python_version_constraint():
   - 构造版本约束字符串 ">=min,<max"
   - 确保 config["project"] 存在后写入 "requires-python"
3. add_dependencies():
   - 根据 dev 参数分别写入 dependencies 或 optional-dependencies.dev
   - 使用 extend() 追加到列表
4. configure_ruff():
   - 写入 tool.ruff.target-version, line-length, select 等配置
5. configure_mypy():
   - 写入 tool.mypy.python_version, strict, warn_unused_ignores
6. save():
   - 使用 tomli_w.dump() 以二进制模式写入文件
7. verify():
   - 检查关键配置项是否存在且值正确
   - 返回字典记录各项检查结果

【关键知识点】
- tomllib/tomli_w: Python 3.11+ 内置 tomllib（只读），需 tomli_w 写入
- 嵌套字典的安全访问：先检查父键是否存在
- TOML 文件必须以二进制模式打开（"rb"/"wb"）
- 字典的 get() 方法提供默认值避免 KeyError
- Python 3.13+ 类型注解：使用 object 而非 Any 表示任意类型
"""

import tomllib
from pathlib import Path

import tomli_w  # type: ignore[import-not-found]


class PyProjectConfig:
    """pyproject.toml 配置管理器"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.toml_path = project_path / "pyproject.toml"
        self.config: dict[str, object] = {}

        if self.toml_path.exists():
            with open(self.toml_path, "rb") as f:
                self.config = tomllib.load(f)

    def set_python_version_constraint(self, min_version: str, max_version: str) -> None:
        """设置 Python 版本约束"""
        if "project" not in self.config:
            self.config["project"] = {}

        self.config["project"]["requires-python"] = f">={min_version},<{max_version}"

    def add_dependencies(self, deps: list[str], dev: bool = False) -> None:
        """添加依赖到 pyproject.toml"""
        if "project" not in self.config:
            self.config["project"] = {}

        if not dev:
            # 添加到生产依赖
            if "dependencies" not in self.config["project"]:
                self.config["project"]["dependencies"] = []
            self.config["project"]["dependencies"].extend(deps)
        else:
            # 添加到开发依赖
            if "optional-dependencies" not in self.config["project"]:
                self.config["project"]["optional-dependencies"] = {}
            if "dev" not in self.config["project"]["optional-dependencies"]:
                self.config["project"]["optional-dependencies"]["dev"] = []
            self.config["project"]["optional-dependencies"]["dev"].extend(deps)

    def configure_ruff(self, target_version: str = "py313", line_length: int = 100) -> None:
        """配置 Ruff

        线程安全（Python 3.14）：
        - ⚠️ 修改 self.config 字典，多线程访问需加锁
        """
        if "tool" not in self.config:
            self.config["tool"] = {}
        if "ruff" not in self.config["tool"]:
            self.config["tool"]["ruff"] = {}

        self.config["tool"]["ruff"]["target-version"] = target_version
        self.config["tool"]["ruff"]["line-length"] = line_length
        self.config["tool"]["ruff"]["select"] = ["E", "F", "I", "N", "W"]

    def configure_mypy(self, python_version: str = "3.13", strict: bool = True) -> None:
        """配置 mypy

        线程安全（Python 3.14）：
        - ⚠️ 修改 self.config 字典，多线程访问需加锁
        """
        if "tool" not in self.config:
            self.config["tool"] = {}
        if "mypy" not in self.config["tool"]:
            self.config["tool"]["mypy"] = {}

        self.config["tool"]["mypy"]["python_version"] = python_version
        self.config["tool"]["mypy"]["strict"] = strict
        self.config["tool"]["mypy"]["warn_unused_ignores"] = True

    def save(self) -> None:
        """保存配置到文件"""
        with open(self.toml_path, "wb") as f:
            tomli_w.dump(self.config, f)

    def verify(self) -> dict[str, bool]:
        """验证配置是否正确"""
        results = {
            "requires_python": False,
            "ruff_target": False,
            "mypy_version": False,
            "mypy_strict": False,
        }

        # 检查 requires-python
        if "project" in self.config:
            requires_python = self.config["project"].get("requires-python", "")
            results["requires_python"] = ">=3.13" in requires_python

        # 检查 ruff
        if "tool" in self.config and "ruff" in self.config["tool"]:
            ruff_config = self.config["tool"]["ruff"]
            results["ruff_target"] = ruff_config.get("target-version") == "py313"

        # 检查 mypy
        if "tool" in self.config and "mypy" in self.config["tool"]:
            mypy_config = self.config["tool"]["mypy"]
            results["mypy_version"] = mypy_config.get("python_version") == "3.13"
            results["mypy_strict"] = mypy_config.get("strict") is True

        return results


def main():
    """主函数"""
    print("=" * 60)
    print("练习 2: 配置项目约束 - 参考答案")
    print("=" * 60)
    print()

    # 创建测试项目
    project_path = Path("./test-config-project")
    project_path.mkdir(exist_ok=True)

    # 创建基础 pyproject.toml
    pyproject_file = project_path / "pyproject.toml"
    pyproject_file.write_text("""[project]
name = "test-project"
version = "0.1.0"
""")

    # 步骤 1: 设置 Python 版本约束
    print("步骤 1: 设置 Python 版本约束")
    config = PyProjectConfig(project_path)
    config.set_python_version_constraint("3.13", "3.15")
    print("✅ Python 版本约束设置成功")
    print()

    # 步骤 2: 添加依赖
    print("步骤 2: 添加依赖")
    config.add_dependencies(["fastapi>=0.136.0", "uvicorn[standard]>=0.30.0"], dev=False)
    config.add_dependencies(["pytest>=8.0.0", "ruff>=0.8.0", "mypy>=1.13.0"], dev=True)
    print("✅ 依赖添加成功")
    print()

    # 步骤 3: 配置 Ruff
    print("步骤 3: 配置 Ruff")
    config.configure_ruff("py313", 100)
    print("✅ Ruff 配置成功")
    print()

    # 步骤 4: 配置 mypy
    print("步骤 4: 配置 mypy")
    config.configure_mypy("3.13", True)
    print("✅ mypy 配置成功")
    print()

    # 步骤 5: 保存配置
    print("步骤 5: 保存配置")
    config.save()
    print("✅ 配置已保存到 pyproject.toml")
    print()

    # 步骤 6: 验证配置
    print("步骤 6: 验证配置")
    results = config.verify()
    print(f"  requires-python: {'✅' if results['requires_python'] else '❌'}")
    print(f"  ruff target-version: {'✅' if results['ruff_target'] else '❌'}")
    print(f"  mypy python_version: {'✅' if results['mypy_version'] else '❌'}")
    print(f"  mypy strict: {'✅' if results['mypy_strict'] else '❌'}")

    if all(results.values()):
        print()
        print("🎉 恭喜！练习 2 完成！")
        print()
        print("生成的配置文件:")
        print(f"  {pyproject_file}")
        print()
        print("查看配置:")
        print(f"  cat {pyproject_file}")
        print()
        print("配置内容:")
        print("-" * 60)
        print(pyproject_file.read_text())
        print("-" * 60)
    else:
        print()
        print("⚠️  部分验证未通过，请检查实现")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: uv add tomli tomli-w")
