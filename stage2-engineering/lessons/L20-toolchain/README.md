# L20: 现代化工具链 - 从环境到生态

> 本课承接 L19 Pytest 完整实战，聚焦 Python 3.13 工程化开发环境、依赖管理、代码质量、类型检查、CI/CD 与容器化基础。

## 📖 课程概述

本课程将”能运行的脚本”推进到”可维护、可测试、可协作的工程”。你会用一组现代化工具建立稳定开发闭环：

- `uv`：虚拟环境、依赖解析、锁文件与命令运行；
- `pyproject.toml`：统一项目元数据与工具配置；
- `Ruff`：格式化、Lint 与导入排序；
- `mypy`：静态类型检查；
- `pytest`：测试组织与质量反馈；
- `GitHub Actions` / `Docker`：自动化验证与环境交付。

**课程时长**: 6-8 小时
**难度**: ⭐⭐⭐☆☆（中级）
**前置课程**: L04 模块与包、L10 类型注解、L19 Pytest 完整实战

## 🎯 学习目标

完成本课程后，你将能够：

1. 区分脚本、模块、包与工程项目的边界；
2. 使用 uv 创建环境、管理依赖并运行命令；
3. 编写和维护 `pyproject.toml` 工具链配置；
4. 配置 Ruff、mypy、pytest，形成本地质量门禁；
5. 读写 GitHub Actions CI 工作流；
6. 理解 Docker 化 Python 3.13 项目的基本做法。

## 📚 课程结构

| 模块 | 主题 | 重点 |
| --- | --- | --- |
| Part A | 从脚本到工程 | 项目结构、src-layout/flat-layout、工程边界 |
| Part B | Git 工作流 | 分支、约定式提交、Code Review、pre-commit |
| Part C | uv 包管理器 | venv、sync、lock、依赖组、命令运行 |
| Part D | Ruff | 格式化、Lint、规则配置、自动修复 |
| Part E | mypy | 类型注解、严格模式、错误定位 |
| Part F | pytest | 测试组织、fixtures、覆盖率与插件 |
| Part G | CI/CD | GitHub Actions、矩阵测试、缓存 |
| Part H | Docker | Dockerfile、Compose、多阶段构建 |

## 📁 当前目录结构

本课程目录已扁平化：示例、练习、答案和测试文件直接放在对应目录下，不再使用 `environment/`、`toolchain/` 二级目录。

```text
L18-toolchain/
├── lesson.md
├── README.md
├── pyproject.toml
├── verify.py
├── report.py
├── examples/
│   ├── README.md
│   ├── example_01_uv_workflow.py
│   ├── example_01_uv_workflow_advanced.py
│   ├── example_01_ruff_usage.py
│   ├── example_02_pyproject_config.py
│   ├── example_02_mypy_types.py
│   ├── example_03_python313_features.py
│   ├── example_03_pytest_basic.py
│   ├── example_04_code_craft.py
│   ├── example_04_github_actions_ci.py
│   └── example_05_docker_environment.py
├── exercises/
│   ├── exercise_00_quickstart.py
│   ├── exercise_01_basic.py
│   ├── exercise_01_ruff.py
│   ├── exercise_02_intermediate.py
│   ├── exercise_02_mypy.py
│   ├── exercise_03_advanced.py
│   ├── exercise_03_pytest.py
│   └── exercise_04_refactor_for_readability.py
├── solutions/
│   ├── solution_00_quickstart.py
│   ├── solution_01_basic.py
│   ├── solution_01_ruff.py
│   ├── solution_02_intermediate.py
│   ├── solution_02_mypy.py
│   ├── solution_03_advanced.py
│   ├── solution_03_pytest.py
│   ├── solution_04_refactor_for_readability.py
│   ├── solution_05_combined.py
│   └── solution_05_pyproject.py
└── tests/
    └── test_*.py
```

## 🚀 快速开始

```bash
# 在仓库根目录运行
uv sync

# 验证课程目录和依赖状态
uv run python stage2-engineering/lessons/L18-toolchain/verify.py

# 运行一个配置示例
uv run python stage2-engineering/lessons/L18-toolchain/examples/example_02_pyproject_config.py

# 运行一个练习自检
uv run python stage2-engineering/lessons/L18-toolchain/exercises/exercise_02_intermediate.py

# 运行 L18 测试
uv run pytest stage2-engineering/lessons/L18-toolchain/tests -q
```

如果你已经 `cd stage2-engineering/lessons/L18-toolchain`，命令可简化为：

```bash
uv run python verify.py
uv run python examples/example_02_pyproject_config.py
uv run python exercises/exercise_02_intermediate.py
uv run pytest tests -q
```

## 🧪 推荐练习顺序

1. `exercise_00_quickstart.py`：快速认识 uv 与工具链输出；
2. `exercise_01_basic.py` / `exercise_01_ruff.py`：环境和 Ruff 基础；
3. `exercise_02_intermediate.py` / `exercise_02_mypy.py`：pyproject 与类型检查；
4. `exercise_03_advanced.py` / `exercise_03_pytest.py`：环境验证与测试组织；
5. `exercise_04_refactor_for_readability.py`：代码工匠式重构。

## ✅ 完成检查清单

- [ ] 能解释 `pyproject.toml` 中 project、tool.ruff、tool.mypy、tool.pytest 的职责；
- [ ] 能使用 uv 创建虚拟环境、同步依赖和运行命令；
- [ ] 能根据项目需要配置 Ruff 规则和行宽；
- [ ] 能开启 mypy 严格模式并理解常见报错；
- [ ] 能为工具链脚本编写 pytest 测试；
- [ ] 能读懂 GitHub Actions 中的 Python 版本矩阵、缓存与质量检查步骤；
- [ ] 能描述 Dockerfile 多阶段构建的基本收益。

## 🔗 相关资源

- [uv 文档](https://docs.astral.sh/uv/)
- [Ruff 文档](https://docs.astral.sh/ruff/)
- [mypy 文档](https://mypy.readthedocs.io/)
- [pytest 文档](https://docs.pytest.org/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Docker 文档](https://docs.docker.com/)

## 🔗 下一步

完成本课后继续学习：

- [L21: 异步核心进阶](../L21-async-programming/README.md)
