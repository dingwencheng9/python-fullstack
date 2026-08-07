# tests/ - L16 单元测试

本目录用于自动验证 L16 参考答案。

```bash
cd stage1-python-intermediate/lessons/L16-concurrency-intro
uv run pytest tests -q
```

## 测试覆盖

| 测试文件 | 用例数 | 验证内容 |
| -------- | ------ | -------- |
| `test_async_basics.py` | 5 | 并发 gather、顺序结果、超时处理、并发任务、任务创建 |
| `test_async_queues.py` | 5 | 生产者/消费者、有界队列、异步生成器、超时消费 |

## 加载策略

`conftest.py` 使用 `importlib.util.spec_from_file_location()` 按物理路径加载 `solutions/`，避免不同课程中同名 `solutions` 包互相污染。

## 维护提示

- 异步测试统一使用 `pytest.mark.asyncio`。
- 新增长耗时测试时应控制 sleep 时长，避免课程级测试变慢。
- 修改超时时间或异常处理语义时，请同步更新练习自检和测试断言。
