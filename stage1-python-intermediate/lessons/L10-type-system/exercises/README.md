# exercises/ - L10 练习题

练习用于巩固类型系统的三个核心动作：**收窄类型、定义结构化接口、约束泛型参数**。

```bash
cd stage1-python-intermediate/lessons/L10-type-system
python exercises/01_type_narrowing.py
```

## 文件清单

| 文件 | 练习目标 | 对应参考答案/测试 |
| ---- | -------- | ----------------- |
| `01_type_narrowing.py` | 编写 `TypeGuard`，过滤和拆分混合类型列表 | `solutions/solution_01_type_narrowing.py` / `tests/test_type_narrowing.py` |
| `02_protocol.py` | 使用 `Protocol` 描述可求长度对象与可比较对象 | `solutions/solution_02_protocol.py` / `tests/test_protocol.py` |
| `03_generic_constraints.py` | 使用 PEP 695 泛型约束限制数字类型 | `solutions/solution_03_generic_constraints.py` / `tests/test_generic_constraints.py` |

## 建议流程

1. 先阅读文件顶部说明和函数签名。
2. 只改动练习文件中需要实现或实验的部分。
3. 运行当前练习脚本做快速自检。
4. 再运行 pytest，观察参考答案覆盖的完整行为。

```bash
uv run pytest tests -q
```

> 练习脚本中的断言偏向“快速反馈”；pytest 覆盖的是参考答案 API 与边界行为。
