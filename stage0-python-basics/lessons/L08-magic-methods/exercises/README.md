# exercises/ - 练习题

**用途**：通过三个小类练习最常用的魔术方法。

运行方式：

```bash
cd stage0-python-basics/lessons/L08-magic-methods
python3 exercises/01_fraction.py
```

## 文件清单

| 文件 | 任务 | 对应答案 |
|------|------|----------|
| `01_fraction.py` | 分数类：`__repr__`、`__str__`、`__eq__`、`__add__` | `solutions/fraction.py` |
| `02_set_class.py` | 简化集合：`__len__`、`__contains__`、`__iter__` | `solutions/set_class.py` |
| `03_callable.py` | 可调用乘法器：`__call__`、`__repr__` | `solutions/callable.py` |

## 建议完成顺序

1. `Multiplier`：最短路径理解 `__call__`。
2. `Set`：练习容器协议，理解 `len(s)`、`x in s`、`for x in s`。
3. `Fraction`：综合练习表示、比较、归一化和加法。

## 验证方式

完成后运行：

```bash
uv run pytest tests/ -q
```

> 提醒：`Fraction.__eq__` 比较前应先约分；如果实现了 `__eq__` 且对象不可变，建议同时实现与相等逻辑一致的 `__hash__`。
