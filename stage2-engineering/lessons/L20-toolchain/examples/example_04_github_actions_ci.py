"""

from __future__ import annotations

L18 示例 4: GitHub Actions CI/CD 配置

展示如何为 Python 3.13 项目配置 GitHub Actions 自动化测试、代码质量检查和部署。
"""

from pathlib import Path


def generate_basic_ci_workflow() -> str:
    """生成基础 CI 工作流配置

    线程安全（Python 3.14）：
    - ✅ 纯函数，返回不可变字符串，线程安全
    """
    return """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.13']

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 安装 uv
      uses: astral-sh/setup-uv@v3
      with:
        enable-cache: true

    - name: 设置 Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}

    - name: 创建虚拟环境
      run: uv venv --python ${{ matrix.python-version }}

    - name: 同步依赖
      run: uv sync --frozen

    - name: 运行测试
      run: uv run pytest tests/ -v --cov=src --cov-report=xml

    - name: 上传覆盖率报告
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
"""


def generate_quality_check_workflow() -> str:
    """生成代码质量检查工作流

    包含：
    - Ruff 代码格式化和 Linting
    - MyPy 类型检查
    - 安全性扫描（bandit）
    """
    return """name: Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 安装 uv
      uses: astral-sh/setup-uv@v3

    - name: 设置 Python 3.13
      run: uv python install 3.13

    - name: 同步依赖
      run: uv sync --group dev

    - name: Ruff - 代码格式检查
      run: uv run ruff check . --target-version=py313

    - name: Ruff - 格式化检查
      run: uv run ruff format --check .

    - name: MyPy - 类型检查
      run: uv run mypy src/ --python-version=3.13

    - name: Bandit - 安全性扫描
      run: uv run bandit -r src/ -f json -o bandit-report.json
      continue-on-error: true

    - name: 上传安全报告
      uses: actions/upload-artifact@v4
      with:
        name: bandit-report
        path: bandit-report.json
"""


def generate_multi_os_workflow() -> str:
    """生成多操作系统测试工作流

    测试矩阵：
    - 操作系统：Ubuntu, macOS, Windows
    - Python 版本：3.13
    """
    return """name: Multi-OS Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-matrix:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.13']

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 安装 uv
      uses: astral-sh/setup-uv@v3
      with:
        enable-cache: true

    - name: 设置 Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}

    - name: 同步依赖
      run: uv sync --frozen

    - name: 运行测试
      run: uv run pytest tests/ -v -m "not slow"

    - name: 生成测试报告
      if: always()
      run: uv run pytest tests/ --junit-xml=test-results.xml

    - name: 上传测试报告
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-results-${{ matrix.os }}-py${{ matrix.python-version }}
        path: test-results.xml
"""


def generate_dependency_update_workflow() -> str:
    """生成自动依赖更新工作流

    功能：
    - 每周检查依赖更新
    - 自动创建 PR
    - 运行测试确保兼容性
    """
    return """name: Dependency Update

on:
  schedule:
    - cron: '0 0 * * 1'  # 每周一 UTC 00:00
  workflow_dispatch:  # 手动触发

jobs:
  update-dependencies:
    runs-on: ubuntu-latest

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 安装 uv
      uses: astral-sh/setup-uv@v3

    - name: 设置 Python 3.13
      run: uv python install 3.13

    - name: 更新依赖
      run: uv lock --upgrade

    - name: 同步依赖
      run: uv sync

    - name: 运行测试
      run: uv run pytest tests/ -v

    - name: 创建 Pull Request
      uses: peter-evans/create-pull-request@v6
      with:
        commit-message: 'chore: 更新依赖到最新版本'
        title: '🔄 自动依赖更新'
        body: |
          ## 自动依赖更新

          此 PR 由 GitHub Actions 自动创建。

          ### 更新内容
          - 更新所有依赖到最新兼容版本
          - 已通过所有测试

          ### 检查清单
          - [ ] 检查 uv.lock 变更
          - [ ] 查看 CHANGELOG（如有重大变更）
          - [ ] 本地运行测试套件

          ---
          🤖 自动生成于 ${{ github.run_id }}
        branch: auto-dependency-update
        delete-branch: true
"""


def generate_release_workflow() -> str:
    """生成自动发布工作流

    功能：
    - 基于 git tag 触发
    - 构建 wheel 包
    - 发布到 PyPI
    - 创建 GitHub Release
    """
    return """name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 安装 uv
      uses: astral-sh/setup-uv@v3

    - name: 设置 Python 3.13
      run: uv python install 3.13

    - name: 构建包
      run: uv build

    - name: 发布到 PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: uv run twine upload dist/*

    - name: 创建 GitHub Release
      uses: softprops/action-gh-release@v2
      with:
        files: dist/*
        generate_release_notes: true
        body: |
          ## 🎉 新版本发布

          查看完整的 [更新日志](CHANGELOG.md)

          ### 安装
          ```bash
          uv pip install my-package==${{ github.ref_name }}
          ```
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""


def generate_docker_build_workflow() -> str:
    """生成 Docker 镜像构建工作流

    功能：
    - 构建 Docker 镜像
    - 推送到 GitHub Container Registry
    - 支持多平台（amd64, arm64）
    """
    return """name: Docker Build

on:
  push:
    branches: [ main ]
    tags:
      - 'v*.*.*'
  pull_request:
    branches: [ main ]

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
    - name: 检出代码
      uses: actions/checkout@v4

    - name: 设置 Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: 登录 GitHub Container Registry
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: 提取元数据
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ghcr.io/${{ github.repository }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: 构建并推送
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
"""


def explain_workflow_structure() -> None:
    """解释 GitHub Actions 工作流结构"""
    print("=" * 80)
    print("📚 GitHub Actions 工作流结构解析")
    print("=" * 80)
    print()

    sections = [
        ("name", "工作流名称（显示在 Actions 页面）"),
        ("on", "触发条件（push, pull_request, schedule, workflow_dispatch）"),
        ("jobs", "作业定义（可以有多个作业并行或串行执行）"),
        ("runs-on", "运行环境（ubuntu-latest, macos-latest, windows-latest）"),
        ("strategy.matrix", "矩阵策略（并行测试多个版本/环境）"),
        ("steps", "步骤列表（按顺序执行）"),
        ("uses", "使用预定义 Action（如 actions/checkout@v4）"),
        ("run", "运行 shell 命令"),
    ]

    for key, desc in sections:
        print(f"  • {key:20} {desc}")

    print()


def show_uv_in_ci_best_practices() -> None:
    """展示 uv 在 CI 中的最佳实践"""
    print("=" * 80)
    print("🎯 uv 在 CI 中的最佳实践")
    print("=" * 80)
    print()

    practices: list[tuple[str, str, str]] = [
        ("1. 使用 uv sync --frozen", "确保依赖版本精确匹配 uv.lock", "✅ 推荐"),
        ("2. 启用缓存", "使用 enable-cache: true 加速构建", "✅ 推荐"),
        ("3. 多平台测试", "测试多个操作系统（Ubuntu/macOS/Windows）", "✅ 推荐"),
        ("4. 分离 job", "质量检查和测试分离，并行执行", "✅ 推荐"),
        ("5. 使用 uv run", "uv run pytest 而非激活虚拟环境", "✅ 推荐"),
        ("6. 锁定 Action 版本", "使用 @v4 而非 @latest", "✅ 推荐"),
    ]

    for title, desc, status in practices:
        print(f"{status} {title}")
        print(f"   {desc}")
        print()


def generate_all_workflows() -> dict[str, str]:
    """生成所有工作流配置

    返回：工作流文件名 → 配置内容的映射

    线程安全（Python 3.14）：
    - ✅ 返回新字典，无共享状态，线程安全
    """
    workflows: dict[str, str] = {
        "ci.yml": generate_basic_ci_workflow(),
        "quality.yml": generate_quality_check_workflow(),
        "multi-os.yml": generate_multi_os_workflow(),
        "dependency-update.yml": generate_dependency_update_workflow(),
        "release.yml": generate_release_workflow(),
        "docker.yml": generate_docker_build_workflow(),
    }

    return workflows


def save_workflows_to_disk(output_dir: Path) -> None:
    """保存所有工作流配置到磁盘"""
    workflows = generate_all_workflows()

    # 创建 .github/workflows 目录
    workflows_dir = output_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("💾 保存 GitHub Actions 工作流配置")
    print("=" * 80)
    print()

    for filename, content in workflows.items():
        file_path = workflows_dir / filename
        file_path.write_text(content)
        print(f"✅ 已保存: .github/workflows/{filename}")

    print()
    print(f"📁 工作流配置目录: {workflows_dir}")
    print(f"   共 {len(workflows)} 个工作流文件")


def show_workflow_summary() -> None:
    """显示工作流总览"""
    print()
    print("=" * 80)
    print("📋 GitHub Actions 工作流总览")
    print("=" * 80)
    print()

    workflows_info: list[tuple[str, str, str]] = [
        ("ci.yml", "基础 CI 测试", "每次 push/PR 触发"),
        ("quality.yml", "代码质量检查", "Ruff + MyPy + Bandit"),
        ("multi-os.yml", "多平台测试", "Ubuntu/macOS/Windows"),
        ("dependency-update.yml", "自动依赖更新", "每周一执行"),
        ("release.yml", "自动发布", "git tag 触发"),
        ("docker.yml", "Docker 镜像构建", "推送到 GHCR"),
    ]

    for filename, desc, trigger in workflows_info:
        print(f"  📄 {filename:25} {desc:20} → {trigger}")

    print()


def main() -> None:
    """主函数"""
    print("🤖 GitHub Actions CI/CD 配置生成器")
    print("=" * 80)
    print()

    # 解释工作流结构
    explain_workflow_structure()

    # 最佳实践
    show_uv_in_ci_best_practices()

    # 生成并保存工作流
    output_dir = Path("demo-github-actions")
    save_workflows_to_disk(output_dir)

    # 显示总览
    show_workflow_summary()

    # 后续步骤
    print("=" * 80)
    print("🚀 后续步骤")
    print("=" * 80)
    print()
    print("1. 复制工作流配置到你的项目：")
    print(f"   cp -r {output_dir}/.github .github/")
    print()
    print("2. 配置必要的 Secrets（Settings → Secrets and variables → Actions）：")
    print("   • PYPI_API_TOKEN - PyPI 发布令牌")
    print("   • CODECOV_TOKEN - Codecov 覆盖率上传令牌（可选）")
    print()
    print("3. 提交到 GitHub：")
    print("   git add .github/workflows/")
    print("   git commit -m 'ci: 添加 GitHub Actions 工作流'")
    print("   git push")
    print()
    print("4. 查看执行结果：")
    print("   https://github.com/<your-username>/<your-repo>/actions")
    print()

    print("✨ 配置生成完成！")


if __name__ == "__main__":
    main()
