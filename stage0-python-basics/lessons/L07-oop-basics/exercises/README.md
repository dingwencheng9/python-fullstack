# exercises/ - 练习题

**用途**：把类定义、封装、继承和特殊方法连成一个完整练习。

运行方式：

```bash
cd stage0-python-basics/lessons/L07-oop-basics
python3 exercises/01_oop_basics.py
```

## 文件清单

| 文件 | 任务 |
|------|------|
| `01_oop_basics.py` | 实现/理解 `Person`、`BankAccount`、`Rectangle`、`Animal/Dog/Cat`、`Vector` |

## 建议完成顺序

1. `Person`：先熟悉 `__init__`、实例属性和实例方法。
2. `BankAccount`：练习封装、只读属性、输入校验。
3. `Rectangle`：练习构造参数验证和计算方法。
4. `Animal/Dog/Cat`：练习继承和方法重写。
5. `Vector`：练习 `__add__`、`__eq__`、`__repr__` 等特殊方法。

## 验证方式

完成后对照 `solutions/`，再运行：

```bash
uv run pytest tests/ -q
```

> 说明：当前练习文件保留了可运行实现，适合作为“边读边改”的课堂练习模板；如果用于作业发布，可将方法体替换为 `pass` 或 `raise NotImplementedError`。
