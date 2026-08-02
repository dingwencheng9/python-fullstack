# exercises/ - L11 练习题

练习用于把迭代器/生成器概念转成可运行代码。当前练习脚本都带有 `__main__` 自检，可直接运行获取快速反馈。

```bash
cd stage1-python-intermediate/lessons/L11-generators
python exercises/01_iterator_protocol.py
```

## 文件清单

| 文件 | 练习目标 | 对应参考答案/测试 |
| ---- | -------- | ----------------- |
| `01_iterator_protocol.py` | 手写 `Counter`、`Fibonacci`、`Range` 的迭代器协议 | `solutions/solution_01_iterator_protocol.py` / `tests/test_iterator_protocol.py` |
| `02_generator_exercises.py` | 使用 `yield` 实现计数、平方、链式迭代、分块和展平 | `solutions/solution_02_generator_exercises.py` / `tests/test_generator_exercises.py` |
| `03_itertools_exercises.py` | 使用 `itertools` 实现截断、连续获取、分组、滑动窗口和幂集 | `solutions/solution_03_itertools_exercises.py` / `tests/test_itertools_exercises.py` |

## 建议流程

1. 先运行示例，确认 `yield` 和 `itertools` 的输出顺序。
2. 完成练习脚本并运行自检。
3. 查看 `solutions/`，比较参考答案 API 和边界处理。
4. 运行 pytest 验证参考答案行为。

```bash
uv run pytest tests -q
```

> 注：练习脚本侧重概念自检；pytest 当前验证的是 `solutions/` 中更完整的参考答案实现。
