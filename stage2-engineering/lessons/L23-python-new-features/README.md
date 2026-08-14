# L23: Python 新特性与版本迁移

> **课程编号**: L23
> **课程名称**: Python 新特性与版本迁移
> **所属阶段**: Stage 2 - 现代化基础内功
> **预计时长**: 4 小时
> **难度**: ⭐⭐☆☆☆ (初级)
> **前置课程**: L19 Pytest 完整实战, L20 工具链

> **核心版本**: Python 3.13+（动态更新）/ 3.14.x（Part 4 试验性补充；free-threading 实测需 `python3.14t` 独立构建）

---

## 📋 课程概述

Python 3.13 于 **2024 年 10 月 7 日**正式发布。本课程以 3.13 为基线，体验四大主题：

1. **彩色错误提示** - 让调试更直观
2. **改进的 REPL** - 增强交互式开发体验
3. **性能对比** - JIT 编译器带来的速度提升
4. **Python 3.14 新特性预览**（试验性补充） - PEP 649 / PEP 750 / PEP 779

---

## 🎯 学习目标

完成本课程后，你将能够：

- ✅ 使用彩色错误提示快速定位问题
- ✅ 掌握新 REPL 的高级功能
- ✅ 了解 Python 3.13 的性能改进
- ✅ 评估是否需要升级到 Python 3.13
- ✅ 理解 PEP 649（延迟注解）解决了什么真实痛点
- ✅ 用 PEP 750 t-string 安全处理 SQL/HTML/shell 拼接
- ✅ 区分 Python 3.13t（试验）与 3.14t（PEP 779 官方支持）

---

## 📚 课程内容

### Part 1: 彩色错误提示 (1h)

Python 3.13 引入了默认彩色化的错误堆栈追踪，使错误信息更易于阅读和理解。

### Part 2: 改进的 REPL (1h)

交互式解释器经过重大改进，基于 PyPy 的设计实现。

### Part 3: 性能对比 (1h)

体验 Python 3.13 的性能提升，包括实验性 JIT 编译器。

### Part 4: Python 3.14 新特性预览（试验性补充，1h）

> ⚠️ Part 4 内部按特性分两类环境：
>
> - **PEP 649 / PEP 750**：使用标准 `python3.14`，可 `uv python install 3.14` 安装。
> - **PEP 779（free-threading 实测）**：必须使用独立构建 `python3.14t`，可 `uv python install 3.14t` 或 `brew install python-freethreaded@3.14`。标准 `python3.14` 仍带 GIL，不能通过 `-X gil=0` 启用 free-threading。

**核心特性**：

- **PEP 649** — 延迟注解评估，解决运行时类型工具痛点
- **PEP 750** — t-string 模板字符串，f-string 的安全替代品（SQL/HTML/shell 注入防御）
- **PEP 779** — Free-threading 从试验性升级为官方支持（详见 [`docs/FREE_THREADING_TRUTH.md`](../../../docs/technical/FREE_THREADING_TRUTH.md)）
- **JIT 编译器** — 性能进一步优化

---

## 🛠️ 环境准备

> ⚠️ **重要**: 课程基线需要 Python 3.13。Part 4 额外需要 Python 3.14。

```bash
# 课程基线
uv python install 3.13

# Part 4 试验性补充（可选）
uv python install 3.14

# Free-threading 实测（可选，演示 PEP 779）
uv python install 3.13t
uv python install 3.14t
```

---

## 📁 课程文件清单

### examples/（演示代码）

| 文件                              | 主题                             | 需要版本               |
| --------------------------------- | -------------------------------- | ---------------------- |
| `example_01_colorful_errors.py`   | 彩色错误提示                     | 3.13                   |
| `example_02_repl_improvements.py` | REPL 改进                        | 3.13                   |
| `example_03_pep695_generics.py`   | PEP 695 泛型                     | 3.12+（课程基线 3.13） |
| `example_04_match_case.py`        | match/case 语句                  | 3.10+（课程基线 3.13） |
| `example_05_python314_pep649.py`  | PEP 649 注解 + annotationlib     | **3.14**               |
| `example_06_python314_tstring.py` | PEP 750 t-string + 安全 SQL/HTML | **3.14**               |

### exercises/（练习题）+ solutions/（参考答案）

| 文件                       | 任务                     | 需要版本 |
| -------------------------- | ------------------------ | -------- |
| `exercise_01_error_handling.py`     | 调试彩色化代码           | 3.13     |
| `exercise_02_interactive_debug.py`  | REPL 探索                | 3.13     |
| `exercise_03_benchmark.py`          | 性能基准测试             | 3.13     |
| `exercise_04_pep695_generics.py`    | 泛型应用                 | 3.13     |
| `exercise_05_pep649_annotations.py` | 自引用类 + annotationlib | **3.14** |
| `exercise_06_tstring_shell_safe.py` | 安全 shell argv 构造器   | **3.14** |

### tests/（单元测试）

- `test_features.py` / `test_new_features.py` — 3.13 基础特性测试
- `test_python314_features.py` — PEP 649 / PEP 750 测试，**3.14 上跑过 12 用例 / 3.13 上自动 skip 10 个**

---

## 🚀 快速开始

```bash
# 1. 跑 Part 1-3（3.13 基线）
python3.13 examples/example_01_colorful_errors.py
python3.13 examples/example_02_repl_improvements.py

# 2. 跑 Part 4（3.14 试验性补充）
python3.14 examples/example_05_python314_pep649.py
python3.14 examples/example_06_python314_tstring.py

# 3. 完整测试
.venv/bin/python -m pytest tests/ -v          # 3.13 基线（10 个 3.14 测试自动 skip）
.venv-py314/bin/python -m pytest tests/ -v    # 3.14 完整跑（12 个全过）
```

---

## ✅ 完成标准

### 基线（必做）

- [ ] 阅读完 `lesson.md` Part 1-3
- [ ] 在 Python 3.13 上运行所有 3.13 测试通过
- [ ] 完成 exercises/01-04（4 个基线练习）
- [ ] 体验彩色错误提示与改进 REPL

### 试验性补充（推荐）

- [ ] 阅读 `lesson.md` Part 4（PEP 649 / PEP 750 / PEP 779）
- [ ] 在 Python 3.14 上运行 example_05 / example_06
- [ ] 完成 exercises/05-06（2 个 3.14 练习）
- [ ] 阅读 [`docs/FREE_THREADING_TRUTH.md`](../../../docs/technical/FREE_THREADING_TRUTH.md) 理解 free-threading 真相

---

## 📖 相关文档

- **lesson.md** — Python 3.13 + 3.14 完整教程
- **../../../docs/technical/FREE_THREADING_TRUTH.md** — Free-threading 唯一权威源
- **../../../docs/PYTHON_VERSION.md** — Python 版本兼容性指南
- **../../../artifacts/python314-vs-313t-analysis.md** — 3.13t → 3.14t 演进分析

---

## 📁 文件导航

| 目录       | 说明                            |
| ---------- | ------------------------------- |
| examples/  | 示例代码（含 PEP 649/750 演示） |
| exercises/ | 练习题（基线 + 3.14 补充）      |
| solutions/ | 参考答案                        |
| tests/     | 单元测试（含跨版本兼容）        |

---

## ⚙️ 环境差异说明

### 彩色输出与 NO_COLOR 环境变量

Python 3.13 的彩色错误提示依赖终端的 ANSI 转义序列支持。如果彩色输出没有生效，可能是因为：

**原因 1：终端不支持彩色**

- 某些老旧终端或 IDE 内置终端不支持 ANSI 颜色代码
- 解决方案：使用支持彩色的现代终端（如 iTerm2、Windows Terminal、VS Code 集成终端）

**原因 2：NO_COLOR 环境变量被设置**

[`NO_COLOR`](https://no-color.org/) 是一个行业标准环境变量，当被设置时，程序应禁用所有彩色输出：

```bash
# 检查是否设置了 NO_COLOR
echo $NO_COLOR  # 如果输出为空则未设置

# 如果想强制禁用彩色（某些 CI 环境需要）
export NO_COLOR=1

# 如果想强制启用彩色（即使设置了 NO_COLOR）
unset NO_COLOR
```

**原因 3：PYTHON_COLORS 环境变量**

Python 3.13 还支持 `PYTHON_COLORS` 环境变量：

```bash
# 强制启用彩色
export PYTHON_COLORS=1

# 强制禁用彩色
export PYTHON_COLORS=0
```

**常见场景**：

| 环境 | 彩色状态 | 说明 |
|------|----------|------|
| macOS Terminal / iTerm2 | ✅ 默认启用 | 支持 ANSI 颜色 |
| VS Code 集成终端 | ✅ 默认启用 | 通常支持彩色 |
| SSH 远程连接 | ⚠️ 可能禁用 | 取决于终端配置 |
| CI/CD 环境 | ⚠️ 通常禁用 | 常见 `NO_COLOR=1` |
| Docker 容器 | ⚠️ 可能禁用 | 需要 `-t` 分配伪终端 |

> ⚠️ **重要**：彩色输出是否显示**不影响课程内容的正确性**。如果彩色未显示但代码运行正常，说明 Python 3.13 已正确安装，只是终端配置不支持彩色而已。

---

## 🔗 参考资源

### 官方文档

- [Python 3.13 What's New](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Python 3.14 What's New](https://docs.python.org/3.14/whatsnew/3.14.html)
- [PEP 649 — Deferred Evaluation Of Annotations](https://peps.python.org/pep-0649/)
- [PEP 750 — Template Strings](https://peps.python.org/pep-0750/)
- [PEP 779 — Free-threaded CPython is Officially Supported](https://peps.python.org/pep-0779/)

### 社区资源

- [Real Python: Python 3.13 Features](https://realpython.com/python313-new-features/)

---

## 🔗 下一步

完成本课后继续学习：

- [L24: 高阶流控与异步协同](../L24-advanced-flow-async/README.md)
