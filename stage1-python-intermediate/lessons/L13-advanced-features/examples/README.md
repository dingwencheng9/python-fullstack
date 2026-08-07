# examples/ - L13 示例代码

这些示例用于演示闭包、装饰器和上下文管理器的典型用法。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L13-advanced-features
python examples/01_closures_decorators.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_closures_decorators.py` | 闭包、函数工厂、装饰器、装饰器工厂、类装饰器 | `wraps` 为什么重要、闭包状态何时变化 |
| `02_context_managers.py` | 类上下文管理器、`contextmanager`、`suppress`、`ExitStack`、`nullcontext` | `__exit__` 返回值与资源清理时机 |

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
