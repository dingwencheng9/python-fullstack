# examples/ - 示例代码

**用途**：通过可运行脚本观察 Python 语法如何触发魔术方法。

运行方式：

```bash
cd stage0-python-basics/lessons/L08-magic-methods
python3 examples/01_basic_magic_methods.py
```

也可以批量运行：

```bash
for f in examples/*.py; do python3 "$f"; done
```

## 文件清单

| 文件 | 重点 |
|------|------|
| `01_basic_magic_methods.py` | `__init__`、`__repr__`、`__str__` |
| `02_arithmetic_operators.py` | `__add__`、`__sub__`、`__mul__`、`__rmul__` |
| `03_comparison_operators.py` | `__eq__`、`__lt__`、排序与比较 |
| `04_container_iterators.py` | `__len__`、`__contains__`、`__iter__`、`__next__` |
| `05_callable_objects.py` | `__call__` 与带状态的可调用对象 |
| `06_property_access.py` | `__getattr__`、`__setattr__`、属性访问拦截 |

## 学习建议

- 运行示例时重点观察“哪种语法触发了哪个方法”。
- 不建议在业务代码中过度使用属性访问拦截；先掌握常用的表示、比较、运算和容器协议。
- `__repr__` 优先面向调试，`__str__` 优先面向用户展示。
