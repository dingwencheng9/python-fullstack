# solutions/ - L14 参考答案

本目录提供 `asyncio` 练习的参考实现。建议先独立完成 `exercises/`，遇到困难再阅读。

## 文件清单

| 文件 | 说明 |
| ---- | ---- |
| `solution_01_async_basics.py` | 协程延迟、并发 gather、顺序 await、超时处理、任务创建 |
| `solution_02_async_queues.py` | 异步队列生产者/消费者、有界队列、异步生成器、超时消费 |
| `__init__.py` | 参考答案包入口 |

## 实现要点

- `asyncio.gather()` 会并发调度多个 awaitable，并按传入顺序返回结果。
- 顺序执行需要逐个 `await`，适合存在依赖关系的任务。
- `asyncio.wait_for()` 可以为慢操作添加超时边界。
- `asyncio.Queue` 的 `put()`/`get()` 都是协程；在有界队列中，`put()` 会在队列满时等待。
- 消费者处理完 `get()` 取得的项目后应调用 `queue.task_done()`。
