"""练习 1: 创建项目环境（基础）- 参考答案

from __future__ import annotations

本文件提供练习 1 的完整实现，供学习参考。

【解题思路】
1. check_uv_installed(): 使用 subprocess.run() 执行 `uv --version`，捕获异常判断是否安装
2. create_project():
   - 使用 Path.cwd() / project_name 构建路径
   - mkdir(exist_ok=True) 创建目录（允许已存在）
   - subprocess.run(["uv", "init"], cwd=...) 在项目目录初始化
3. create_venv():
   - subprocess.run(["uv", "venv", "--python", version], cwd=...)
   - 使用 try-except 捕获失败并返回 False
4. add_dependencies():
   - 第一次调用 uv add 添加生产依赖（fastapi, uvicorn）
   - 第二次调用 uv add --dev 添加开发依赖（pytest, ruff, mypy）
   - 任何步骤失败都返回 False
5. verify_environment():
   - 检查文件/目录存在性：.venv/, pyproject.toml
   - 执行 uv pip list 并检查输出中是否包含关键依赖（fastapi, pytest）
   - 返回字典记录各项检查结果

【关键知识点】
- subprocess.run() 的 cwd 参数指定工作目录
- capture_output=True 捕获 stdout/stderr
- check=True 在失败时抛出 CalledProcessError
- Path 对象的 exists() 和 mkdir() 方法
- 字符串的 in 操作符用于检查子串（转小写实现不区分大小写）
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
    """创建新项目"""
    # 创建项目目录
    project_path = Path.cwd() / project_name
    project_path.mkdir(exist_ok=True)

    # 切换到项目目录并初始化
    subprocess.run(["uv", "init"], cwd=project_path, check=True, capture_output=True)

    return project_path


def create_venv(project_path: Path, python_version: str = "3.13") -> bool:
    """创建虚拟环境"""
    try:
        subprocess.run(
            ["uv", "venv", "--python", python_version],
            cwd=project_path,
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def add_dependencies(project_path: Path) -> bool:
    """添加项目依赖"""
    try:
        # 添加生产依赖
        subprocess.run(
            ["uv", "add", "fastapi", "uvicorn"],
            cwd=project_path,
            check=True,
            capture_output=True,
        )

        # 添加开发依赖
        subprocess.run(
            ["uv", "add", "--dev", "pytest", "ruff", "mypy"],
            cwd=project_path,
            check=True,
            capture_output=True,
        )

        return True
    except subprocess.CalledProcessError:
        return False


def verify_environment(project_path: Path) -> dict[str, bool]:
    """验证环境配置"""
    results = {
        "venv": (project_path / ".venv").exists(),
        "pyproject": (project_path / "pyproject.toml").exists(),
        "dependencies": False,
    }

    # 检查依赖是否安装
    if results["venv"] and results["pyproject"]:
        try:
            result = subprocess.run(
                ["uv", "pip", "list"],
                cwd=project_path,
                capture_output=True,
                text=True,
                check=True,
            )
            # 检查关键依赖是否存在
            output = result.stdout.lower()
            has_fastapi = "fastapi" in output
            has_pytest = "pytest" in output
            results["dependencies"] = has_fastapi and has_pytest
        except subprocess.CalledProcessError:
            results["dependencies"] = False

    return results


def main():
    """主函数"""
    print("=" * 60)
    print("练习 1: 创建项目环境 - 参考答案")
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
    project_path = create_project(project_name)
    print(f"✅ 项目创建成功: {project_path}")
    print()

    # 步骤 3: 创建虚拟环境
    print("步骤 3: 创建虚拟环境")
    if create_venv(project_path):
        print("✅ 虚拟环境创建成功")
    else:
        print("❌ 虚拟环境创建失败")
        return
    print()

    # 步骤 4: 添加依赖
    print("步骤 4: 添加依赖")
    if add_dependencies(project_path):
        print("✅ 依赖添加成功")
    else:
        print("❌ 依赖添加失败")
        return
    print()

    # 步骤 5: 验证环境
    print("步骤 5: 验证环境")
    results = verify_environment(project_path)
    print(f"  .venv 目录: {'✅' if results['venv'] else '❌'}")
    print(f"  pyproject.toml: {'✅' if results['pyproject'] else '❌'}")
    print(f"  依赖安装: {'✅' if results['dependencies'] else '❌'}")

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


if __name__ == "__main__":
    main()
