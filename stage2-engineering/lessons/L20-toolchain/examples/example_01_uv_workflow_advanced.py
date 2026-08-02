"""

from __future__ import annotations

L18 示例 1+: uv 包管理器高级工作流演示

展示 uv 的高级功能：sync, lock, 依赖组管理等。
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> tuple[bool, str]:
    """运行命令并显示结果

    线程安全（Python 3.14）：
    - ✅ subprocess.run() 本身是线程安全的
    - ✅ 返回不可变的 tuple，无共享状态
    """
    print(f"\n{'=' * 60}")
    print(f"📌 {description}")
    print(f"{'=' * 60}")
    print(f"$ {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout)

    success = result.returncode == 0
    if not success and result.stderr:
        print(f"❌ Error: {result.stderr}", file=sys.stderr)

    return success, result.stdout


def demo_uv_lock_workflow(project_dir: Path) -> None:
    """演示 uv lock 锁定依赖版本

    uv.lock 的作用：
    - 锁定所有依赖的精确版本（包括传递依赖）
    - 确保团队成员使用相同的依赖版本
    - 类似 npm 的 package-lock.json 或 poetry 的 poetry.lock
    """
    print("\n" + "=" * 80)
    print("🔒 演示 1: uv lock - 锁定依赖版本")
    print("=" * 80)

    # 1. 生成 uv.lock 文件
    run_command(f"cd {project_dir} && uv lock", "生成 uv.lock 锁定文件")

    # 2. 检查锁文件
    lock_file = project_dir / "uv.lock"
    if lock_file.exists():
        print("\n✅ 已生成 uv.lock 文件")
        print(f"   大小: {lock_file.stat().st_size} 字节")

        # 读取前 20 行
        lines = lock_file.read_text().splitlines()[:20]
        print("\n📄 uv.lock 文件内容（前 20 行）:")
        print("-" * 60)
        for line in lines:
            print(f"  {line}")
        print("  ...")

    print("\n💡 关键点:")
    print("  1. uv.lock 记录所有依赖的精确版本（包括传递依赖）")
    print("  2. 提交到 git，确保团队使用相同版本")
    print("  3. CI/CD 使用 uv sync 安装精确版本")


def demo_uv_sync_workflow(project_dir: Path) -> None:
    """演示 uv sync 同步依赖

    uv sync vs uv add:
    - uv add: 添加新依赖到 pyproject.toml
    - uv sync: 根据 uv.lock 安装精确版本的依赖
    """
    print("\n" + "=" * 80)
    print("🔄 演示 2: uv sync - 同步依赖")
    print("=" * 80)

    # 1. 同步依赖
    success, output = run_command(f"cd {project_dir} && uv sync", "同步依赖（根据 uv.lock）")

    if success:
        print("\n✅ 依赖同步成功")
        print("\n💡 使用场景:")
        print("  • 新成员 clone 项目后：uv sync")
        print("  • CI/CD 构建：uv sync --frozen（禁止修改 lock）")
        print("  • 更新依赖后：uv lock && uv sync")


def demo_dependency_groups(project_dir: Path) -> None:
    """演示依赖组管理

    依赖组（Dependency Groups）：
    - 比 optional-dependencies 更灵活
    - 可以定义多个环境：dev, test, docs, lint
    - 使用 uv sync --group <name> 安装特定组
    """
    print("\n" + "=" * 80)
    print("📦 演示 3: 依赖组管理")
    print("=" * 80)

    # 1. 添加测试依赖组
    run_command(
        f"cd {project_dir} && uv add --group test pytest-cov pytest-asyncio",
        "添加测试依赖组",
    )

    # 2. 添加文档依赖组
    run_command(
        f"cd {project_dir} && uv add --group docs mkdocs mkdocs-material",
        "添加文档依赖组",
    )

    # 3. 查看 pyproject.toml
    pyproject_path = project_dir / "pyproject.toml"
    if pyproject_path.exists():
        content = pyproject_path.read_text()

        print("\n📄 pyproject.toml 中的依赖组:")
        print("-" * 60)

        # 提取 dependency-groups 部分
        lines = content.splitlines()
        in_dep_groups = False
        for line in lines:
            if "[dependency-groups]" in line:
                in_dep_groups = True
            if in_dep_groups:
                print(f"  {line}")
                if line.strip() and not line.startswith(" ") and "[dependency-groups]" not in line:
                    break

    print("\n💡 依赖组的优势:")
    print("  1. 分离不同环境的依赖（dev/test/docs/lint）")
    print("  2. 按需安装：uv sync --group test")
    print("  3. 比 optional-dependencies 更语义化")


def demo_uv_pip_compile(project_dir: Path) -> None:
    """演示 uv pip compile 生成 requirements.txt

    用途：
    - 兼容传统 pip 工具链
    - 生成精确版本的 requirements.txt
    - 适合不支持 uv 的部署环境
    """
    print("\n" + "=" * 80)
    print("📋 演示 4: 生成 requirements.txt")
    print("=" * 80)

    # 1. 生成 requirements.txt
    run_command(
        f"cd {project_dir} && uv pip compile pyproject.toml -o requirements.txt",
        "从 pyproject.toml 生成 requirements.txt",
    )

    # 2. 生成开发依赖的 requirements
    run_command(
        f"cd {project_dir} && uv pip compile pyproject.toml --extra dev -o requirements-dev.txt",
        "生成开发依赖的 requirements-dev.txt",
    )

    # 3. 查看生成的文件
    req_file = project_dir / "requirements.txt"
    if req_file.exists():
        lines = req_file.read_text().splitlines()[:15]
        print("\n📄 requirements.txt 内容（前 15 行）:")
        print("-" * 60)
        for line in lines:
            print(f"  {line}")
        print("  ...")

    print("\n💡 使用场景:")
    print("  • 部署到不支持 uv 的环境（如旧版 Docker）")
    print("  • 与 pip-tools 工具链集成")
    print("  • 生成精确版本的依赖清单供审计")


def demo_workspace_management(base_dir: Path) -> None:
    """演示 workspace 多项目管理

    Workspace（工作空间）：
    - 管理多个相关的 Python 项目
    - 共享依赖和虚拟环境
    - 类似 npm workspaces 或 cargo workspace
    """
    print("\n" + "=" * 80)
    print("🏢 演示 5: Workspace 多项目管理")
    print("=" * 80)

    workspace_dir = base_dir / "demo-workspace"
    workspace_dir.mkdir(exist_ok=True)

    # 1. 创建 workspace 配置
    workspace_toml = workspace_dir / "pyproject.toml"
    workspace_content = """[tool.uv.workspace]
members = ["packages/*"]

[project]
name = "demo-workspace"
version = "0.1.0"
requires-python = ">=3.13"
"""
    workspace_toml.write_text(workspace_content)
    print("✅ 创建 workspace 配置")

    # 2. 创建子项目 1
    pkg1_dir = workspace_dir / "packages" / "backend"
    pkg1_dir.mkdir(parents=True, exist_ok=True)

    pkg1_toml = pkg1_dir / "pyproject.toml"
    pkg1_content = """[project]
name = "backend"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["fastapi>=0.110.0", "uvicorn>=0.30.0"]
"""
    pkg1_toml.write_text(pkg1_content)
    print("✅ 创建子项目: packages/backend")

    # 3. 创建子项目 2
    pkg2_dir = workspace_dir / "packages" / "frontend"
    pkg2_dir.mkdir(parents=True, exist_ok=True)

    pkg2_toml = pkg2_dir / "pyproject.toml"
    pkg2_content = """[project]
name = "frontend"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["jinja2>=3.1.0"]
"""
    pkg2_toml.write_text(pkg2_content)
    print("✅ 创建子项目: packages/frontend")

    # 4. 显示目录结构
    print("\n📁 Workspace 结构:")
    print("-" * 60)
    print("  demo-workspace/")
    print("  ├── pyproject.toml          # workspace 配置")
    print("  └── packages/")
    print("      ├── backend/")
    print("      │   └── pyproject.toml  # 子项目 1")
    print("      └── frontend/")
    print("          └── pyproject.toml  # 子项目 2")

    print("\n💡 Workspace 的优势:")
    print("  • 多个项目共享一个虚拟环境")
    print("  • 统一管理依赖版本")
    print("  • 适合 monorepo 架构")
    print("  • 使用: cd demo-workspace && uv sync")


def show_best_practices() -> None:
    """展示 uv 最佳实践总结"""
    print("\n" + "=" * 80)
    print("📋 uv 高级工作流最佳实践")
    print("=" * 80)

    practices = [
        ("1. 使用 uv lock 锁定依赖", "uv lock → 提交 uv.lock 到 git"),
        ("2. CI/CD 使用 uv sync", "uv sync --frozen 确保精确版本"),
        ("3. 使用依赖组分离环境", "uv add --group test/docs/lint"),
        ("4. 生成 requirements.txt", "uv pip compile 兼容传统工具链"),
        ("5. Workspace 管理多项目", "适合 monorepo 架构"),
        ("6. 定期更新依赖", "uv lock --upgrade → uv sync"),
    ]

    for title, desc in practices:
        print(f"\n✅ {title}")
        print(f"   {desc}")

    print("\n" + "=" * 80)
    print("🔗 参考资源")
    print("=" * 80)
    print("  • uv 官方文档: https://docs.astral.sh/uv/")
    print("  • uv GitHub: https://github.com/astral-sh/uv")
    print("  • PEP 621: https://peps.python.org/pep-0621/")


def main() -> None:
    """主函数"""
    print("🚀 uv 包管理器高级工作流演示")
    print("=" * 80)

    # 创建演示项目
    base_dir = Path.cwd()
    project_dir = base_dir / "demo-project-advanced"

    if not project_dir.exists():
        project_dir.mkdir()
        print(f"✅ 创建项目目录: {project_dir}")

        # 初始化项目
        run_command(f"cd {project_dir} && uv init", "初始化 uv 项目")
        run_command(f"cd {project_dir} && uv venv --python 3.13", "创建虚拟环境")
        run_command(f"cd {project_dir} && uv add fastapi uvicorn", "添加基础依赖")
    else:
        print(f"⚠️  项目已存在: {project_dir}")

    # 演示各个高级功能
    demo_uv_lock_workflow(project_dir)
    demo_uv_sync_workflow(project_dir)
    demo_dependency_groups(project_dir)
    demo_uv_pip_compile(project_dir)
    demo_workspace_management(base_dir)

    # 最佳实践总结
    show_best_practices()

    print("\n✨ 高级工作流演示完成！")
    print("\n🎯 下一步:")
    print(f"  1. cd {project_dir}")
    print("  2. 查看生成的 uv.lock 和 requirements.txt")
    print("  3. 尝试 uv sync 和依赖组管理")


if __name__ == "__main__":
    main()
