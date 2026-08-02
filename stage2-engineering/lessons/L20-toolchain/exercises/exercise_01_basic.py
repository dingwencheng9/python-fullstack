"""练习 1: 创建项目环境（基础）

from __future__ import annotations

任务：
创建一个新的 Python 项目，配置开发环境，验证安装成功。

学习目标：
- 使用 uv 创建项目
- 创建虚拟环境
- 安装依赖
- 验证环境配置

预计时间: 30 分钟
难度: ⭐☆☆☆☆
"""

import subprocess
import sys
from pathlib import Path


def check_uv_installed() -> bool:
    """检查 uv 是否已安装"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ uv 已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv 未安装")
        print("请运行: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def create_project(project_name: str) -> Path:
    """创建新项目

    TODO: 实现以下功能
    1. 创建项目目录
    2. 初始化项目 (uv init)
    3. 返回项目路径

    提示: 使用 subprocess.run() 执行命令
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_project 函数")


def create_venv(project_path: Path, python_version: str = "3.13") -> bool:
    """创建虚拟环境

    TODO: 实现以下功能
    1. 在项目目录下创建虚拟环境
    2. 使用指定的 Python 版本
    3. 返回是否成功

    提示: 运行 uv venv --python {python_version}
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_venv 函数")


def add_dependencies(project_path: Path) -> bool:
    """添加项目依赖

    TODO: 实现以下功能
    1. 添加生产依赖: fastapi, uvicorn
    2. 添加开发依赖: pytest, ruff, mypy
    3. 返回是否成功

    提示: 使用 uv add 和 uv add --dev
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 add_dependencies 函数")


def verify_environment(project_path: Path) -> dict[str, bool]:
    """验证环境配置

    TODO: 实现以下功能
    1. 检查 .venv 目录是否存在
    2. 检查 pyproject.toml 是否存在
    3. 检查依赖是否安装成功
    4. 返回验证结果字典

    返回格式: {"venv": True, "pyproject": True, "dependencies": True}
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 verify_environment 函数")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 1: 创建项目环境")
    print("=" * 60)
    print()

    # 步骤 1: 检查 uv
    print("步骤 1: 检查 uv 安装")
    if not check_uv_installed():
        sys.exit(1)
    print()

    # 步骤 2: 创建项目
    print("步骤 2: 创建项目")
    project_name = "my-first-project"
    try:
        project_path = create_project(project_name)
        print(f"✅ 项目创建成功: {project_path}")
    except NotImplementedError:
        print("❌ 请实现 create_project 函数")
        return
    print()

    # 步骤 3: 创建虚拟环境
    print("步骤 3: 创建虚拟环境")
    try:
        if create_venv(project_path):
            print("✅ 虚拟环境创建成功")
        else:
            print("❌ 虚拟环境创建失败")
            return
    except NotImplementedError:
        print("❌ 请实现 create_venv 函数")
        return
    print()

    # 步骤 4: 添加依赖
    print("步骤 4: 添加依赖")
    try:
        if add_dependencies(project_path):
            print("✅ 依赖添加成功")
        else:
            print("❌ 依赖添加失败")
            return
    except NotImplementedError:
        print("❌ 请实现 add_dependencies 函数")
        return
    print()

    # 步骤 5: 验证环境
    print("步骤 5: 验证环境")
    try:
        results = verify_environment(project_path)
        print(f"  .venv 目录: {'✅' if results.get('venv') else '❌'}")
        print(f"  pyproject.toml: {'✅' if results.get('pyproject') else '❌'}")
        print(f"  依赖安装: {'✅' if results.get('dependencies') else '❌'}")

        if all(results.values()):
            print()
            print("🎉 恭喜！练习 1 完成！")
            print()
            print("下一步:")
            print(f"  cd {project_path}")
            print("  source .venv/bin/activate")
            print("  python --version")
        else:
            print()
            print("⚠️  部分验证未通过，请检查实现")
    except NotImplementedError:
        print("❌ 请实现 verify_environment 函数")
        return


if __name__ == "__main__":
    main()
