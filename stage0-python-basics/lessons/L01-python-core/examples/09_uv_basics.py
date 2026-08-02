"""L01 示例9: uv 现代化包管理入门。

学习目标:
- 了解 uv 包管理器的基本用途
- 掌握 uv 常用命令
- 理解虚拟环境、pyproject.toml 与 uv.lock 的关系
- 为后续 Python 工程化课程打下工具链基础
"""

# ============================================================
# 1. 什么是 uv？
# ============================================================
print("=" * 60)
print("🚀 uv 现代化包管理器")
print("=" * 60)
print()
print("uv 是用 Rust 编写的 Python 包管理工具")
print("速度比 pip 快 10-100 倍")
print("由 Astral 公司开发（同 Ruff 团队）")
print()
print("核心优势:")
print("  ⚡ 极速安装（并行下载 + 缓存）")
print("  🔒 自动锁文件（uv.lock）")
print("  📦 统一 pyproject.toml")
print("  🐍 内置虚拟环境管理")
print()

# ============================================================
# 2. 安装 uv
# ============================================================
print("=" * 60)
print("📥 安装 uv")
print("=" * 60)
print()
print("# macOS / Linux")
print("curl -LsSf https://astral.sh/uv/install.sh | sh")
print()
print("# 或使用 Homebrew (macOS)")
print("brew install uv")
print()
print("# 或使用 pip（备用方案）")
# ❌ 反模式演示：pip install uv 已被 uv init 替代，仅作历史对比
print("pip install uv  # ❌ 反模式")
print()
print("# 验证安装")
print("uv --version")
print()

# ============================================================
# 3. 创建项目（pyproject.toml）
# ============================================================
print("=" * 60)
print("📋 创建 Python 项目")
print("=" * 60)
print()
print("# 1. 创建项目目录")
print("uv init myproject")
print("cd myproject")
print()
print("# 这会生成:")
print("myproject/")
print("├── pyproject.toml   ← 项目配置文件")
print("├── README.md")
print("└── hello.py         ← 示例文件")
print()
print("# 2. 指定 Python 版本")
print("uv python pin 3.13")
print()

# ============================================================
# 4. 虚拟环境管理
# ============================================================
print("=" * 60)
print("🐍 虚拟环境管理")
print("=" * 60)
print()
print("# uv 自动管理虚拟环境，无需手动创建!")
print()
print("# 创建并激活虚拟环境（一条命令）")
print("uv venv")
print("source .venv/bin/activate   # macOS/Linux")
print(".venv\\Scripts\\activate      # Windows")
print()
print("# 退出虚拟环境")
print("deactivate")
print()

# ============================================================
# 5. 安装和管理依赖
# ============================================================
print("=" * 60)
print("📦 依赖管理")
print("=" * 60)
print()
print("# 安装包（自动更新 pyproject.toml + uv.lock）")
print("uv add requests")
print()
print("# 安装开发依赖")
print("uv add --dev pytest ruff")
print()
print("# 安装所有依赖")
print("uv sync")
print()
print("# 移除包")
print("uv remove requests")
print()
print("# 查看已安装的包")
print("uv pip list")
print()

# ============================================================
# 6. 运行代码
# ============================================================
print("=" * 60)
print("▶️  运行 Python 代码")
print("=" * 60)
print()
print("# 使用 uv 运行（自动使用项目虚拟环境）")
print("uv run python hello.py")
print()
print("# 运行脚本")
print("uv run hello.py")
print()
print("# 运行测试")
print("uv run pytest")
print()

# ============================================================
# 7. pyproject.toml 简介
# ============================================================
print("=" * 60)
print("📋 pyproject.toml — 项目配置文件")
print("=" * 60)
print()
print("pyproject.toml 是 Python 项目的标准配置文件")
print("替代了传统的 setup.py / requirements.txt")
print()
print("一个典型的 pyproject.toml:")
print()
print("[project]")
print('name = "myproject"')
print('version = "0.1.0"')
print('requires-python = ">=3.13"')
print()
print("dependencies = [")
print('    "requests>=2.31.0",')
print("]")
print()
print("[dependency-groups]")
print("dev = [")
print('    "pytest>=8.0",')
print('    "ruff>=0.5",')
print("]")
print()

# ============================================================
# 8. uv.lock — 锁定依赖版本
# ============================================================
print("=" * 60)
print("🔒 uv.lock — 依赖版本锁定")
print("=" * 60)
print()
print("uv.lock 记录每个依赖包的精确版本和哈希值")
print()
print("重要性:")
print("  ✅ 确保所有开发者使用完全相同的依赖版本")
print("  ✅ 确保开发环境与生产环境 100% 一致")
print("  ✅ 防止 '在我电脑上能跑' 问题")
print()
print("uv.lock 由 uv add / uv sync 自动生成")
print("应提交到 Git 仓库中")
print()

# ============================================================
# 9. Python 版本要求
# ============================================================
print("=" * 60)
print("🐍 Python 版本")
print("=" * 60)
print()
print("本课程使用: Python 3.13")
print()
print("检查版本:")
print("  python3 --version")
print("  uv python list")
print()
print("⚠️  必须使用 Python 3.13+")
print()

# ============================================================
# 10. 进阶学习
# ============================================================
print("=" * 60)
print("🎓 进阶学习")
print("=" * 60)
print()
print("在后续课程中，你将深入学习:")
print("  L19 - 现代化开发环境（uv 深度使用）")
print("  L21 - 工具链生态（Ruff + mypy + pytest）")
print()
print("✅ 现在掌握 uv 的基本使用已经足够！")
