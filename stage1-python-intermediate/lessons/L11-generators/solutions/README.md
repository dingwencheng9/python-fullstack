# solutions/ - L11 参考答案

> ⚠️ 建议先独立完成 `exercises/`，再查看本目录。参考答案兼顾教学可读性与 pytest 覆盖的边界行为。

## 文件清单

| 文件 | 内容 |
| ---- | ---- |
| `solution_01_iterator_protocol.py` | `FibonacciIterator`、`Range`、`Counter` 三类自定义迭代器 |
| `solution_02_generator_exercises.py` | 斐波那契生成器、递归展平、分块、素数、相邻元素对和滑动窗口 |
| `solution_03_itertools_exercises.py` | `islice`、`accumulate`、`groupby`、组合、排列和交替合并 |
| `__init__.py` | 标识 solutions 包，供测试按物理路径加载 |

## 设计说明

- 迭代器类需要让 `__iter__()` 返回自身，并在 `__next__()` 中负责状态推进与结束条件。
- 生成器函数天然实现迭代器协议，更适合表达线性数据流。
- `itertools` 函数通常返回迭代器；参考答案在需要断言比较时转换为 `list`。
- `zip_longest()` + sentinel 可用于安全交替合并不等长可迭代对象。

## 验证

```bash
uv run pytest stage1-python-intermediate/lessons/L11-generators/tests -q
```
