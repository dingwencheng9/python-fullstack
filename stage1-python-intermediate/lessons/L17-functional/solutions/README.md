# solutions/ - L17 参考答案

本目录提供函数式编程练习的参考实现。建议先独立完成 `exercises/`，遇到困难再阅读。

## 文件清单

| 文件 | 说明 |
| ---- | ---- |
| `solution_01_functional_pipeline.py` | 数据管道、字符串转换、`compose()`、`pipe()` |
| `solution_02_data_transformation.py` | 折扣、税费、价格舍入与偏函数组合 |
| `solution_03_compose_decorator.py` | 日志、重试、缓存、装饰器组合与管道式组合 |
| `__init__.py` | 参考答案包入口 |

## 实现要点

- `process_data()` 使用 `filter -> map -> reduce`，并提供初始值 `0` 以支持空列表。
- `compose()` 从右到左执行函数，`pipe()` 从左到右执行函数。
- `calculate_final_price()` 先折扣、再税费，适合用 `partial()` 固定参数。
- `compose_decorators(a, b)` 等价于 `a(b(func))`；`pipe_decorators(a, b)` 先应用 `a` 再应用 `b`。
- 装饰器实现使用 `functools.wraps` 保留原函数元数据。
