# L17: Pytest 完整实战 — 从单元测试到 CI/CD

> **课程代码**: L17-pytest-complete
> **课程时长**: 5-6 小时
> **难度**: ⭐⭐⭐⭐☆（中高级）
> **前置课程**: L01-L16（Python 基础与进阶）

## 📚 课程概述

本课程把 **pytest 测试工程** 与 **CI/CD 自动化** 放在同一条工程链路中学习：先掌握测试用例、fixture、parametrize、mock、conftest 等核心能力，再理解如何把这些检查放进 GitHub Actions 质量门。

完成本课后，你将能够：

- 使用 pytest 编写清晰、可维护的单元测试与边界测试。
- 使用 fixture 管理测试依赖、临时资源和清理逻辑。
- 使用 parametrize 将重复测试改写为数据驱动测试。
- 使用 mock/monkeypatch 隔离网络、环境变量等外部依赖。
- 读懂并验证基础 GitHub Actions CI 工作流。
- 将 lint、format、typecheck、pytest 组织成最小质量门。

## 📂 当前目录结构

本课文件已按当前仓库结构展平到各目录根部：

```text
L17-pytest-complete/
├── README.md
├── lesson.md
├── pyproject.toml
├── EXECUTION_LOG.md
├── examples/
│   ├── README.md
│   ├── 01_basic_test.py
│   ├── 02_fixture_demo.py
│   ├── 03_parametrize_demo.py
│   ├── 04_mock_demo.py
│   ├── 01_validate_ci.py
│   ├── 02_matrix_report.py
│   ├── ci_basic.yml
│   └── ci_matrix.yml
├── exercises/
│   ├── README.md
│   ├── exercise_01_write_fixture.py
│   ├── exercise_02_parametrize_calc.py
│   ├── exercise_03_mock_api.py
│   ├── exercise_01_customize_ci.py
│   └── exercise_02_add_cache.py
├── solutions/
│   ├── README.md
│   ├── __init__.py
│   ├── exercises.md
│   ├── solution_01_write_fixture.py
│   ├── solution_02_parametrize_calc.py
│   ├── solution_03_mock_api.py
│   ├── solution_01_customize_ci.py
│   └── solution_02_add_cache.py
└── tests/
    ├── conftest.py
    ├── test_pytest_concepts.py
    └── test_cicd.py
```

> 说明：早期合并日志中可能还能看到 `pytest/`、`cicd/` 子目录说法；当前可交付结构以上方展平结构为准。

## 🧭 推荐学习路径

1. 阅读 `lesson.md` 的第一部分，理解测试工程的基本动机。
2. 运行 `examples/01_basic_test.py`、`02_fixture_demo.py`、`03_parametrize_demo.py`、`04_mock_demo.py`。
3. 完成并运行 `exercises/` 中的 pytest 练习。
4. 阅读 CI/CD 章节，运行 `examples/01_validate_ci.py` 与 `02_matrix_report.py`。
5. 对比 `solutions/` 中的参考答案。
6. 最后运行 `tests/`，确认课程基线通过。

## ⚡ 快速开始

从仓库根目录运行：

```bash
# 课程基线测试
uv run pytest stage2-engineering/lessons/L17-pytest-complete/tests -q

# pytest 示例
uv run pytest \
  stage2-engineering/lessons/L17-pytest-complete/examples/01_basic_test.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/02_fixture_demo.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/03_parametrize_demo.py \
  stage2-engineering/lessons/L17-pytest-complete/examples/04_mock_demo.py \
  -q

# CI/CD 示例脚本
uv run python stage2-engineering/lessons/L17-pytest-complete/examples/01_validate_ci.py
uv run python stage2-engineering/lessons/L17-pytest-complete/examples/02_matrix_report.py

# 练习自检
uv run pytest \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_01_write_fixture.py \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_02_parametrize_calc.py \
  stage2-engineering/lessons/L17-pytest-complete/exercises/exercise_03_mock_api.py \
  -q

# 参考答案自检
uv run pytest stage2-engineering/lessons/L17-pytest-complete/solutions/*.py -q
```

## 🎯 课程内容

### 第一部分：Pytest 测试工程基础

- AAA 测试结构
- `pytest.raises` 异常断言
- `pytest.approx` 浮点比较
- fixture 创建、注入、作用域与清理
- `@pytest.mark.parametrize` 数据驱动测试
- `unittest.mock.patch` 与 `monkeypatch`
- `conftest.py` 共享测试资源

### 第二部分：CI/CD 自动化集成

- GitHub Actions 工作流结构
- push / pull_request 触发条件
- Python 版本矩阵与质量门
- uv 依赖安装与锁定
- ruff / mypy / pytest 的流水线组织
- CI 缓存与运行报告

## ✅ 完成标准

- [ ] 能解释 pytest 的 AAA、fixture、parametrize、mock 四个核心概念。
- [ ] 能独立编写至少 3 类测试：正常路径、边界条件、异常路径。
- [ ] 能使用 mock 隔离 HTTP 请求。
- [ ] 能读懂 `.github/workflows/ci.yml` 的触发、矩阵、质量门和依赖安装步骤。
- [ ] 课程测试通过：`uv run pytest stage2-engineering/lessons/L17-pytest-complete/tests -q`。
- [ ] 示例、练习、答案自检通过。

## 🔗 前后衔接

- 上一阶段：[Stage 1: Python 进阶](../../../stage1-python-intermediate/README.md)
- 下一课：[L18: 现代化工具链](../L18-toolchain/README.md)
