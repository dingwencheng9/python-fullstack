# L16: 并发编程入门

> **课程编号**: L16
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 6 小时
> **前置课程**: L13 Python 高级特性, L11 迭代器与生成器
> **核心内容**: `async`/`await`、任务调度、超时控制、异步队列、生产者-消费者

---

## 🎯 课程定位

本课从 `asyncio` 入门并发编程，重点理解协程如何让 I/O 密集型任务在单线程中高效协作。它承接 L12 的上下文管理器与 L13 的协议思想，并为后续 Web 服务、异步爬虫、消息队列和后台任务打基础。

完成本课后，你将能够：

- 编写 `async def` 协程并用 `await` 挂起等待。
- 使用 `asyncio.gather()` 并发执行多个协程。
- 使用 `asyncio.create_task()` 管理任务生命周期。
- 使用 `asyncio.wait_for()` 为异步操作添加超时保护。
- 使用 `asyncio.Queue` 实现生产者-消费者模式。
- 理解异步上下文管理器、异步迭代器和基础限流思路。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L16-concurrency-intro

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_async_basics.py
python examples/02_async_advanced.py

# 3) 完成练习并自检
python exercises/01_async_basics.py
python exercises/02_async_queues.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 协程与事件循环基础 | `lesson.md`、`examples/01_async_basics.py` | `async def`、`await`、顺序 vs 并发 |
| 2 | 任务与异常处理 | `examples/01_async_basics.py` | `gather()`、`create_task()`、异常收集 |
| 3 | 异步高级语法 | `examples/02_async_advanced.py` | 异步上下文管理器、异步生成器、限流 |
| 4 | 基础练习 | `exercises/01_async_basics.py` | 并发、顺序执行、超时处理 |
| 5 | 队列练习 | `exercises/02_async_queues.py` | `Queue.put()`、`Queue.get()`、`task_done()` |
| 6 | 自动化验证 | `tests/` | 10 个测试用例覆盖 solutions 行为 |

---

## 📁 目录结构

| 路径 | 用途 |
| ---- | ---- |
| [lesson.md](lesson.md) | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的示例代码 |
| [exercises/](exercises/) | 学员练习与脚本自检 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | pytest 单元测试 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解协程、任务、事件循环和异步队列的关系。
- [ ] 运行 2 个示例文件，观察顺序执行与并发执行的耗时差异。
- [ ] 完成 2 个练习文件，并通过脚本自检。
- [ ] 能解释 `asyncio.gather()`、`asyncio.create_task()`、`asyncio.wait_for()` 的适用场景。
- [ ] 通过 `uv run pytest tests -q`。

---

## 🧪 检查命令

```bash
# Python 语法/导入检查
python3 -m py_compile examples/*.py exercises/*.py solutions/*.py tests/*.py

# 示例运行
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done

# 练习自检
for f in exercises/*.py; do
  echo "== $f =="
  python "$f"
done

# 单元测试
uv run pytest tests -q
```

---

## 🔗 下一步

完成本课后继续学习：

- [L15: 函数式编程](../L15-functional/README.md)
- L15 会切换到函数式工具链，补齐 `map`、`filter`、`reduce`、高阶函数与不可变思维。
