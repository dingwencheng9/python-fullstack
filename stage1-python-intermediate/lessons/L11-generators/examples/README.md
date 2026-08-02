# examples/ - L11 示例代码

这些示例用于演示生成器、惰性求值和 `itertools` 的典型用法。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L11-generators
python examples/01_generator_basics.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_generator_basics.py` | 生成器函数、生成器表达式、`yield from`、双向通信、关闭生成器 | 生成器何时执行、何时暂停、何时释放资源 |
| `02_itertools.py` | `count` / `cycle` / `repeat` / `chain` / `islice` / 排列组合等 | 无限迭代器必须配合截断条件使用 |
| `03_file_stream.py` | 大文件流式读取、批量处理、过滤管道、内存对比 | 生成器在 I/O 密集型场景的实际应用 |

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
