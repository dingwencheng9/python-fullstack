# examples/ - L17 示例代码

这些示例用于演示 lambda、高阶函数、函数组合、偏函数、柯里化、生成器管道和 `itertools`。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L17-functional
python examples/01_lambda_basics.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_lambda_basics.py` | lambda 表达式基础 | 排序 key、短小回调、何时不用 lambda |
| `02_map_filter_reduce.py` | `map`、`filter`、`reduce` | 与列表推导式的可读性取舍 |
| `03_composition.py` | 函数组合 | `compose()` 从右到左，`pipe()` 从左到右 |
| `04_partial_functions.py` | 偏函数 | 固定部分参数、构造专用函数 |
| `05_currying.py` | 柯里化 | 多阶段传参、自动柯里化的边界 |
| `06_generator_functional.py` | 生成器与函数式 | 惰性求值、管道、内存效率 |
| `07_itertools_functional.py` | `itertools` 高级用法 | 组合、分组、窗口、分块和穷举 |

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
