# L18 示例代码索引

本目录采用扁平结构，所有示例文件直接位于 `examples/` 下。建议在仓库根目录通过 `uv run python <文件路径>` 运行，或先进入 `stage2-engineering/lessons/L18-toolchain` 再运行相对路径。

## 示例清单

| 文件 | 主题 | 建议用途 |
| --- | --- | --- |
| `example_01_uv_workflow.py` | uv 基础工作流 | 认识初始化、依赖添加、命令运行 |
| `example_01_uv_workflow_advanced.py` | uv 进阶工作流 | sync、lock、依赖组与更完整流程 |
| `example_01_ruff_usage.py` | Ruff 代码质量 | 观察格式化、Lint 和自动修复思路 |
| `example_02_pyproject_config.py` | pyproject 配置 | 学习 project / tool 配置结构 |
| `example_02_mypy_types.py` | mypy 类型检查 | 学习基础类型、协议和泛型写法 |
| `example_03_python313_features.py` | Python 3.13 特性 | 学习现代泛型语法等 3.13 写法 |
| `example_03_pytest_basic.py` | pytest 基础 | 学习测试函数、异常断言和参数化 |
| `example_04_code_craft.py` | 可维护性重构 | 学习解析、计算和格式化职责拆分 |
| `example_04_github_actions_ci.py` | GitHub Actions | 生成并理解 CI 工作流片段 |
| `example_05_git_advanced.py` | Git 进阶操作 | 学习 rebase、cherry-pick、reflog、bisect、stash 用法 |

## 快速运行

```bash
# 仓库根目录
uv run python stage2-engineering/lessons/L18-toolchain/examples/example_02_pyproject_config.py
uv run python stage2-engineering/lessons/L18-toolchain/examples/example_03_python313_features.py

# 或进入课程目录后
cd stage2-engineering/lessons/L18-toolchain
uv run python examples/example_02_pyproject_config.py
uv run python examples/example_04_github_actions_ci.py
```

## 注意事项

- 部分示例会创建临时演示目录或打印较长配置文本；运行前先阅读文件顶部说明。
- 与外部工具相关的示例（例如 Docker、GitHub Actions）以生成配置和解释为主，不要求本机必须安装 Docker 或连接 GitHub。
- 若只想验证课程基本状态，优先运行 `../verify.py` 和课程测试：

```bash
uv run python stage2-engineering/lessons/L18-toolchain/verify.py
uv run pytest stage2-engineering/lessons/L18-toolchain/tests -q
```
