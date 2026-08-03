# L01: Python 核心语法

> **课程编号**: L01<br>
> **所属阶段**: Stage 0 - Python 编程基础<br>
> **定位**: Python 全栈课程入口课，建立运行程序、变量、类型、输入输出和 f-string 的基础认知。

---

## 📋 前置要求

无（入门课程）

---

## 🎯 学习目标

完成本课后，你应该能够：

- 在终端中运行 Python 文件，并使用 REPL 做快速实验
- 理解变量是“名字绑定到对象”，而不是“盒子里装值”
- 区分 `int`、`float`、`str`、`bool`、`None` 等基础类型
- 使用 `print()`、`input()`、类型转换和 f-string 完成基础交互程序
- 使用 `is None` 判断空值，并理解类型注解的入门作用
- 运行示例、完成练习，并用 pytest 验证学习结果

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L01-python-core
```

运行示例：

```bash
uv run python examples/01_hello_world.py
uv run python examples/05_basic_types.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

如果你当前环境没有使用 `uv`，也可以临时使用：

```bash
python examples/01_hello_world.py
python -m pytest tests/ -q
```

---

## 📚 学习路径

```text
1. 阅读 lesson.md，理解核心概念
2. 运行 examples/*.py，观察输出
3. 完成 exercises/*.py，补全练习代码
4. 对照 solutions/*.py，检查自己的实现
5. 运行 pytest tests/，验证理解
```

建议顺序：

```text
Hello World → REPL → 输入输出 → 变量引用 → 基础类型 → 类型注解 → f-string → 类型转换 → uv 工具入门
```

---

## 📁 目录结构

| 目录 | 用途 |
|------|------|
| [lesson.md](lesson.md) | 完整教程 |
| [examples/](examples/) | 示例代码，可直接运行 |
| [exercises/](exercises/) | 练习题，建议先独立完成 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | 单元测试，用于验证理解 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解变量、类型、输入输出和 f-string
- [ ] 至少运行 5 个示例文件
- [ ] 完成 `exercises/` 中的核心练习
- [ ] 能解释 `input()` 为什么返回字符串
- [ ] 能解释为什么推荐使用 `is None`
- [ ] 能通过 `uv run pytest tests/ -q`

---

## 🔗 下一步

完成本课后继续学习：

- [L02: 运算符与控制流](../L02-operators-control/README.md)
