# exercises/ - L17 练习题

本目录包含函数式编程练习。每个练习文件都可直接运行，并通过内置断言完成基础自检。

```bash
cd stage1-python-intermediate/lessons/L17-functional
python exercises/01_functional_pipeline.py
python exercises/02_data_transformation.py
python exercises/03_compose_decorator.py
```

## 文件清单

| 文件 | 练习内容 | 对应参考答案 | 相关测试 |
| ---- | -------- | ------------ | -------- |
| `01_functional_pipeline.py` | 用 `map`/`filter`/`reduce` 处理数据，实现 `compose()` 和 `pipe()` | `solutions/solution_01_functional_pipeline.py` | `tests/test_functional_pipeline.py` |
| `02_data_transformation.py` | 使用 `partial()` 组合折扣、税费和价格舍入 | `solutions/solution_02_data_transformation.py` | `tests/test_data_transformation.py` |
| `03_compose_decorator.py` | 实现装饰器组合和管道式装饰器组合 | `solutions/solution_03_compose_decorator.py` | `tests/test_compose_decorator.py` |

## 学习建议

1. 先确认 `compose(f, g)(x)` 等价于 `f(g(x))`，`pipe(f, g)(x)` 等价于 `g(f(x))`。
2. 价格转换练习中先应用折扣，再计算税费，最后统一舍入。
3. 装饰器组合练习中关注“应用顺序”和“调用时输出顺序”的区别。
