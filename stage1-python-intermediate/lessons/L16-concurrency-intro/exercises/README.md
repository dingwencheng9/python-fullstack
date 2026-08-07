# exercises/ - L16 练习题

本目录包含 `asyncio` 协程基础练习。每个练习文件都可直接运行，并通过内置断言完成基础自检。

```bash
cd stage1-python-intermediate/lessons/L16-concurrency-intro
python exercises/01_async_basics.py
```

## 文件清单

| 文件 | 练习内容 | 对应参考答案 |
| ---- | -------- | ------------ |
| `01_async_basics.py` | 使用 `gather()` 并发执行、顺序 await、`wait_for()` 超时 | `solutions/solution_01_async_basics.py` |

## 学习建议

1. 先实现顺序版本，确认 `await` 会等待单个协程完成。
2. 再实现 `gather_results()`，观察结果顺序与完成顺序的区别。
3. 注意 `wait_for` 的超时处理逻辑。

> **进阶学习**: 异步队列、信号量、异步生成器等高级特性请参考 L19 异步编程核心。
