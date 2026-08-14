# L06: 异常处理（Exceptions）

> **课程编号**: L06
>
> **所属阶段**: Stage 0 - Python 编程基础
>
> **建议学习时间**: 3-4 小时
>
> **前置课程**: L05 调试工具
>
> **后续课程**: L07 文件操作

---

## 📋 前置要求

- 掌握 L05 调试工具（pdb、breakpoint）
- **重要**：异常处理是文件操作的前置，必须先学

---

## 🎯 课程定位

本课学习 Python 中最重要的可靠性机制：异常处理。

异常不是“把错误藏起来”，而是把失败路径显式表达出来：

- 输入不合法时，应该给出明确错误；
- 文件、网络、数据库等外部资源失败时，应该能恢复或清理；
- 业务规则失败时，应该使用可读的异常类型告诉调用方；
- 调试复杂错误时，应该保留异常链和上下文。

学完本课后，你会从“程序报错就停止”过渡到“能设计可控的失败流程”，为后续项目、Web API、数据库操作和自动化脚本打基础。

---

## ✅ 学习目标

完成本课后，你应该能够：

1. 使用 `try/except` 捕获具体异常，而不是盲目吞掉所有错误。
2. 区分 `ValueError`、`TypeError`、`IndexError`、`KeyError`、`ZeroDivisionError` 等常见异常。
3. 使用多个 `except` 子句为不同失败类型提供不同处理逻辑。
4. 理解 `else` 与 `finally` 的执行时机，能在失败后正确释放资源。
5. 使用 `raise` 主动抛出合适的内置异常。
6. 定义自定义异常类表达业务错误。
7. 理解 `raise ... from ...` 与 traceback，保留关键调试信息。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage0-python-basics/lessons/L06-exceptions
python3 examples/01_basic_try_except.py
python3 examples/05_custom_exceptions.py
uv run pytest tests/ -q
```

如果不使用 `uv`，也可以在已安装 pytest 的环境中运行：

```bash
python3 -m pytest tests/ -q
```

---

## 📚 推荐学习路径

1. 阅读 `lesson.md` 第 1-2 节，理解异常对象和 `try/except` 基础。
2. 运行 `examples/01_basic_try_except.py`、`02_multiple_except.py`，观察不同异常的捕获方式。
3. 学习 `else/finally`，运行 `examples/03_else_finally.py`，理解成功路径和清理路径。
4. 学习主动抛出异常，运行 `examples/04_raise_exception.py`。
5. 学习自定义异常，运行 `examples/05_custom_exceptions.py`。
6. 运行 `examples/06_exception_chaining.py`，观察异常链与 traceback。
7. 完成 `exercises/` 三个练习，并对照 `solutions/`。
8. 运行 `uv run pytest tests/ -q` 验证行为。

> 说明：`examples/06_exception_chaining.py` 会有意打印 traceback，用于教学异常链；看到 traceback 不代表示例失败。

---

## 📁 目录结构

| 目录/文件 | 用途 |
|-----------|------|
| `lesson.md` | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的异常处理示例 |
| [exercises/](exercises/) | 基础捕获、多异常处理、自定义异常练习 |
| [solutions/](solutions/) | 三个练习的参考答案 |
| [tests/](tests/) | pytest 行为验证 |

---

## ✅ 完成标准

- [ ] 能说明为什么应优先捕获具体异常类型。
- [ ] 能实现 `safe_divide`、`safe_parse_int`、`safe_getitem` 等安全包装函数。
- [ ] 能针对输入转换、除零、类型错误分别处理。
- [ ] 能使用自定义异常表达年龄、邮箱等业务校验失败。
- [ ] 能解释 `finally` 适合放资源清理逻辑。
- [ ] `uv run pytest tests/ -q` 全部通过。

---

## ⚠️ 常见误区

- 不要无条件写 `except Exception: pass`，这会隐藏真实错误。
- 不要把异常处理当作普通分支控制的替代品；可预期的简单判断优先用 `if`。
- 捕获异常后如果无法恢复，应重新抛出或转换为更清晰的异常。
- 自定义异常应继承合适的内置异常，例如输入值非法通常继承 `ValueError`。

---

## 🔗 下一步

完成本课后继续学习：

- [L07: 面向对象基础](../L07-oop-basics/README.md)

> 📖 **学习路径提示**：L07 将学习类、对象、继承等 OOP 核心概念，为 L08 魔术方法和后续 Stage 1 打基础。
