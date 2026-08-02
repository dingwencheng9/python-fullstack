# L07: 魔术方法（Magic Methods）

> **课程编号**: L07
>
> **所属阶段**: Stage 0 - Python 编程基础
>
> **建议学习时间**: 4-6 小时
>
> **前置课程**: L06 面向对象基础
>
> **后续课程**: L08 异常处理

---

## 🎯 课程定位

本课承接 L06 的类与对象基础，系统学习 Python 对象如何接入语言内置语法。

所谓“魔术方法”就是 `__xxx__` 形式的特殊方法。你不会直接调用它们，而是通过 Python 语法间接触发：

- `print(obj)` 触发 `__str__`；
- `repr(obj)` 触发 `__repr__`；
- `obj1 + obj2` 触发 `__add__`；
- `x in obj` 触发 `__contains__`；
- `obj()` 触发 `__call__`。

学完本课后，你写出的类会更像 Python 内置类型，也更容易进入后续异常处理、迭代器、装饰器和框架源码阅读。

---

## ✅ 学习目标

完成本课后，你应该能够：

1. 区分 `__repr__` 和 `__str__` 的用途。
2. 实现 `__eq__` 与 `__hash__`，并理解二者必须保持一致。
3. 使用 `__add__`、`__sub__`、`__mul__`、`__rmul__` 实现运算符重载。
4. 使用 `__len__`、`__contains__`、`__iter__` 实现容器协议。
5. 使用 `__call__` 创建可调用对象。
6. 初步理解 `__getattr__`、`__setattr__` 等属性访问协议的风险和场景。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage0-python-basics/lessons/L08-magic-methods
python3 examples/01_basic_magic_methods.py
python3 examples/02_arithmetic_operators.py
uv run pytest tests/ -q
```

如果不使用 `uv`，也可以在已安装 pytest 的环境中运行：

```bash
python3 -m pytest tests/ -q
```

---

## 📚 推荐学习路径

1. 先阅读 `lesson.md` Part 1，掌握 `__repr__`、`__str__`。
2. 运行 `examples/01_basic_magic_methods.py`，观察打印对象时发生了什么。
3. 学习比较与哈希，再运行 `examples/03_comparison_operators.py`。
4. 学习算术运算符重载，再运行 `examples/02_arithmetic_operators.py`。
5. 学习容器协议和可调用对象，再运行 `examples/04_container_iterators.py`、`05_callable_objects.py`。
6. 完成 `exercises/` 三个练习，并对照 `solutions/fraction.py`、`set_class.py`、`callable.py`。
7. 运行测试确认行为：`uv run pytest tests/ -q`。

---

## 📁 目录结构

| 目录/文件 | 用途 |
|-----------|------|
| `lesson.md` | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的魔术方法示例 |
| [exercises/](exercises/) | 分数、集合、可调用对象练习 |
| [solutions/](solutions/) | 练习对应答案 + 扩展示范答案 |
| [tests/](tests/) | pytest 行为验证 |

---

## ✅ 完成标准

- [ ] 能解释 `repr(obj)` 与 `str(obj)` 的差异。
- [ ] 能让自定义对象支持 `+`、`==`、`in`、`len()`、`for ... in`。
- [ ] 能说明实现 `__eq__` 后为什么通常也要考虑 `__hash__`。
- [ ] 完成 `Fraction`、`Set`、`Multiplier` 三个练习。
- [ ] `uv run pytest tests/ -q` 全部通过。

---

## 🔗 下一步

[L08: 异常处理](../L09-exceptions/README.md)

下一课会学习异常分类、`try/except`、自定义异常和异常处理最佳实践。
