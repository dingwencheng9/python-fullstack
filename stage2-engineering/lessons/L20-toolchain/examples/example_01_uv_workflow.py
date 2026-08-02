"""

from __future__ import annotations

L18 示例 1: uv 包管理器工作流演示

展示 uv 的核心功能和最佳实践。
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> None:
    """运行命令并显示结果"""
    print(f"\n{'=' * 60}")
    print(f"📌 {description}")
    print(f"{'=' * 60}")
    print(f"$ {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout)
    if result.returncode != 0 and result.stderr:
        print(f"❌ Error: {result.stderr}", file=sys.stderr)


def main() -> None:
    """演示 uv 工作流"""

    print("🚀 uv 包管理器工作流演示")
    print("=" * 60)

    # 1. 检查 uv 版本
    run_command("uv --version", "检查 uv 版本")

    # 2. 创建项目目录
    project_dir = Path("demo-project")
    if not project_dir.exists():
        project_dir.mkdir()
        print(f"✅ 创建项目目录: {project_dir}")

    # 3. 初始化项目
    run_command(f"cd {project_dir} && uv init", "初始化 uv 项目")

    # 4. 创建虚拟环境
    run_command(f"cd {project_dir} && uv venv --python 3.13", "创建虚拟环境（Python 3.13）")

    # 5. 添加依赖
    run_command(f"cd {project_dir} && uv add fastapi", "添加 fastapi 依赖")

    # 6. 添加开发依赖
    run_command(f"cd {project_dir} && uv add --dev pytest ruff mypy", "添加开发依赖")

    # 7. 查看依赖列表
    run_command(f"cd {project_dir} && uv pip list", "查看已安装的包")

    # 8. 显示 pyproject.toml
    pyproject_path = project_dir / "pyproject.toml"
    if pyproject_path.exists():
        print(f"\n{'=' * 60}")
        print("📄 pyproject.toml 内容")
        print(f"{'=' * 60}\n")
        print(pyproject_path.read_text())

    print("\n✨ 工作流演示完成！")
    print("\n💡 关键要点：")
    print("  1. uv init - 初始化项目")
    print("  2. uv venv - 创建虚拟环境")
    print("  3. uv add - 添加依赖（比 pip 快 10-20 倍）")
    print("  4. uv add --dev - 添加开发依赖")
    print("  5. 所有配置自动写入 pyproject.toml")


if __name__ == "__main__":
    main()
