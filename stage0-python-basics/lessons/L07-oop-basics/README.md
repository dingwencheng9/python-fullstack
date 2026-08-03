# L07: 面向对象基础

> **课程编号**: L07
>
> **所属阶段**: Stage 0 - Python 编程基础
>
> **建议学习时间**: 4-6 小时
>
> **前置课程**: L06 文件操作
>
> **后续课程**: L08 魔术方法

---

## 🎯 课程定位

本课是 Stage 0 从“函数式脚本”进入“对象建模”的关键转折点。

你会把前几课学过的变量、函数、模块和数据结构组织到类中，理解：

- 如何用 `class` 定义对象模板；
- 如何用 `__init__` 初始化实例状态；
- 如何通过封装保护对象内部数据；
- 如何用继承和多态复用行为；
- 为什么 `__str__`、`__repr__`、`__eq__` 等特殊方法是后续 L07 的基础。

---

## ✅ 学习目标

完成本课后，你应该能够：

1. 定义类、创建对象，并区分类属性与实例属性。
2. 正确理解 `self`、实例方法、类方法和静态方法。
3. 使用单下划线、双下划线和 `@property` 表达封装意图。
4. 使用继承、方法重写和 `super()` 组织代码。
5. 用鸭子类型/统一接口理解 Python 多态。
6. 为对象实现基础特殊方法，例如 `__str__`、`__repr__`、`__eq__`。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage0-python-basics/lessons/L07-oop-basics
python3 examples/01_class_basics.py
python3 examples/02_encapsulation.py
uv run pytest tests/ -q
```

如果不使用 `uv`，也可以在已安装 pytest 的环境中运行：

```bash
python3 -m pytest tests/ -q
```

---

## 📚 推荐学习路径

1. 阅读 `lesson.md` 的 Part 1-2，先掌握类、对象、`self`、实例属性。
2. 运行 `examples/01_class_basics.py` 和 `examples/02_encapsulation.py`，观察对象状态如何变化。
3. 阅读 Part 3-4，再运行继承与多态示例。
4. 阅读 Part 5-6，理解本课只做特殊方法入门，深入内容留到 L07。
5. 完成 `exercises/01_oop_basics.py` 中的 5 个小任务。
6. 对照 `solutions/`，再运行 `uv run pytest tests/ -q` 验证行为。

---

## 📁 目录结构

| 目录/文件 | 用途 |
|-----------|------|
| `lesson.md` | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的课堂示例 |
| [exercises/](exercises/) | 练习题，建议先独立完成 |
| [solutions/](solutions/) | 拆分后的参考答案模块 |
| [tests/](tests/) | 验证参考答案行为的 pytest 测试 |

---

## ✅ 完成标准

- [ ] 能独立解释类与对象、类属性与实例属性的区别。
- [ ] 能运行并读懂 `examples/*.py` 的输出。
- [ ] 能实现 `Person`、`BankAccount`、`Rectangle`、`Animal/Dog/Cat`、`Vector`。
- [ ] 能说明 `@property` 与直接暴露属性的差异。
- [ ] 能说明继承和多态分别解决什么问题。
- [ ] `uv run pytest tests/ -q` 全部通过。

---

## 🔗 下一步

[L08: 魔术方法](../L08-magic-methods/README.md)

下一课会系统展开特殊方法、运算符重载、容器协议和可调用对象。
