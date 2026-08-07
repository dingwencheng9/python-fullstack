# examples/ - L16 示例代码

这些示例用于演示 `asyncio` 协程基础，包括 async/await、并发执行、任务创建和错误处理。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L16-concurrency-intro
python examples/01_async_basics.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_async_basics.py` | `async`/`await`、顺序 vs 并发、任务创建、gather、wait_for、异常处理 | 协程如何并发执行、事件循环调度机制 |

> **进阶学习**: 异步上下文管理器、异步生成器、asyncio.Queue、Semaphore 等高级特性请参考 L19 异步编程核心。

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
