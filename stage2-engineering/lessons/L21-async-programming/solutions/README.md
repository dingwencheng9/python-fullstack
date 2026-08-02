# L19 异步编程核心 - 参考答案

本目录提供 5 个练习的参考实现，文件名与 `../exercises/` 一一对应。

| 练习 | 参考答案 | 覆盖主题 |
| --- | --- | --- |
| 练习 1 | `solution_01_asyncio_basics.py` | 协程、`gather`、`create_task`、异步性能对比 |
| 练习 2 | `solution_02_async_await.py` | 异步迭代器、异步生成器、异步上下文管理器 |
| 练习 3 | `solution_03_concurrency_control.py` | 并发下载、限流、锁与共享状态 |
| 练习 4 | `solution_04_async_context.py` | 异步数据库/文件上下文管理器 |
| 练习 5 | `solution_05_async_patterns.py` | 生产者-消费者、重试、异步迭代模式 |

## 运行方式

从仓库根目录运行：

```bash
uv run python stage2-engineering/lessons/L19-async-programming/solutions/solution_01_asyncio_basics.py
uv run python stage2-engineering/lessons/L19-async-programming/solutions/solution_02_async_await.py
uv run python stage2-engineering/lessons/L19-async-programming/solutions/solution_03_concurrency_control.py
uv run python stage2-engineering/lessons/L19-async-programming/solutions/solution_04_async_context.py
uv run python stage2-engineering/lessons/L19-async-programming/solutions/solution_05_async_patterns.py
```

测试：

```bash
uv run pytest stage2-engineering/lessons/L19-async-programming/tests -q
```

## 学习建议

1. 先独立完成 `../exercises/` 中对应练习。
2. 再阅读参考答案，对比资源清理、并发控制和异常处理方式。
3. 对网络相关示例，区分本地模拟客户端与 `examples/07_async_http_real.py` 的真实网络依赖。

## 代码质量关注点

- 使用 Python 3.13+ 语法和内置泛型类型标注。
- 优先保证异步资源在 `__aexit__`、`finally` 或 `TaskGroup` 中被清理。
- 对共享状态使用 `asyncio.Lock`，对外部资源使用 `Semaphore` 或连接池限制并发。
