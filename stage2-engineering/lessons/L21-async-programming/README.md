# L21: 异步核心进阶

> **课程编号**: L21
> **所属阶段**: Stage 2 - 工程化进阶
> **预计时长**: 4 小时
> **难度**: ⭐⭐⭐☆☆（高级）
> **前置课程**: L16 并发基础（async/await、gather、create_task、async with）
> **Python 版本**: 3.13+

---

## 前置说明

**本课程不重复 L16 已讲内容**（async/await、asyncio.run、gather、create_task、async with、Semaphore）。如果你对以下概念不熟悉，请先完成 L16。

---

## 学习目标

完成本课程后，你将能够：

1. **掌握 asyncio 进阶同步原语**：Queue、Event、Condition、Lock 超时。
2. **使用 as_completed / wait**：按完成顺序处理结果、等待任务子集。
3. **使用 TaskGroup 实现结构化并发**：自动管理任务生命周期、ExceptionGroup 异常收集。
4. **实现优雅关闭**：SIGTERM/SIGINT 信号处理、任务取消协调。
5. **掌握生产级模式**：熔断器、指数退避重试、令牌桶限流。

---

## 课程模块

| 模块 | 主题 | 重点 |
| --- | --- | --- |
| 1 | 同步原语进阶 | Queue 生产者/消费者、Event 信号、Condition 条件变量、Lock 超时 |
| 2 | as_completed / wait | 按完成顺序处理、超时等待子集 |
| 3 | TaskGroup 结构化并发 | 自动取消、ExceptionGroup、asyncio.timeout |
| 4 | 生产级模式 | 优雅关闭、熔断器、指数退避重试 |

---

## 常用命令

从仓库根目录运行：

```bash
# 检查课程结构
ls stage2-engineering/lessons/L21-async-programming/

# 运行单元测试
uv run pytest stage2-engineering/lessons/L21-async-programming/tests -q

# 运行核心演示
uv run python stage2-engineering/lessons/L21-async-programming/examples/demo_async.py
uv run python stage2-engineering/lessons/L21-async-programming/examples/06_producer_consumer.py
uv run python stage2-engineering/lessons/L21-async-programming/examples/08_modern_taskgroup.py
uv run python stage2-engineering/lessons/L21-async-programming/examples/ex09_pep695_async_generics.py

# 运行练习自检
uv run python stage2-engineering/lessons/L21-async-programming/exercises/exercise_01_asyncio_basics.py
uv run python stage2-engineering/lessons/L21-async-programming/exercises/exercise_02_async_await.py
uv run python stage2-engineering/lessons/L21-async-programming/exercises/exercise_03_concurrency_control.py
uv run python stage2-engineering/lessons/L21-async-programming/exercises/exercise_04_async_context.py
uv run python stage2-engineering/lessons/L21-async-programming/exercises/exercise_05_async_patterns.py
```

> `examples/07_async_http_real.py` 是真实 HTTP 示例，依赖网络与 `aiohttp`，按需单独运行。

---

## 完成标准

- [ ] 阅读 `lesson.md`，理解 Queue/Event/Condition/TaskGroup/as_completed 用法。
- [ ] 确认课程目录结构完整（README.md, lesson.md, examples/, exercises/, solutions/, tests/）。
- [ ] 完成 5 个练习脚本自检。
- [ ] 通过 `tests/` 下全部测试。

---

## 📖 参考资源

- [asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)
- [PEP 492 - Coroutines with async and await](https://peps.python.org/pep-0492/)
- [PEP 525 - Asynchronous Generators](https://peps.python.org/pep-0525/)
- [PEP 530 - Asynchronous Comprehensions](https://peps.python.org/pep-0530/)
- [PEP 654 - Exception Groups](https://peps.python.org/pep-0654/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)

---

## 🔗 下一步

完成本课后继续学习：

- [L22: 装饰器深度探索](../L22-decorators/README.md)

> 📖 **学习路径提示**：L22 将深入学习装饰器的设计模式和高级用法。

## 🎓 延伸阅读

- [Message Queue](../../../extensions/) — 异步任务队列与事件驱动
- [IoT/MQTT](../../../extensions/) — 物联网异步通信
