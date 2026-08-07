# L26: 线程与并发

> **课程编号**: L26
> **所属阶段**: Stage 2 - 现代化基础内功
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐ (中高级)

---

## 📚 课程概览

- **位置**: Stage 2 / 第 8 课
- **学习时长**: 4-5 小时
- **难度**: ⭐⭐⭐⭐
- **前置课程**: L21-L25（异步/装饰器/性能优化）
- **后续课程**: Stage 3 Web APIs

线程是 Python 后端工程中处理 I/O 并发的基础工具。
本课从 `threading.Thread` 的生命周期讲起，逐步覆盖同步原语、队列、线程池、GIL、Python 3.13 free-threading 以及常见并发陷阱。
完成本课后，你应该能写出线程安全的生产者消费者容器，也能用 `ThreadPoolExecutor` 实现可测试的并发下载器。

---

## 🎯 学习目标

1. ✅ 创建、启动、命名并等待线程。
2. ✅ 解释 daemon 线程的适用边界。
3. ✅ 用 Lock 保护共享可变状态。
4. ✅ 区分 Lock、RLock、Condition、Event、Semaphore。
5. ✅ 用 queue.Queue 组织生产者消费者模型。
6. ✅ 正确使用 task_done 与 join。
7. ✅ 用 ThreadPoolExecutor 管理任务并收集 Future。
8. ✅ 用 as_completed 处理先完成的任务。
9. ✅ 隔离并发任务中的异常，避免单任务失败拖垮整批任务。
10. ✅ 解释 GIL 对 I/O 密集和 CPU 密集任务的不同影响。
11. ✅ 了解 Python 3.13 free-threading 与 PEP 703 的现实边界。
12. ✅ 识别竞态、死锁、线程泄漏、无界并发等陷阱。
13. ✅ 为并发代码编写稳定测试。

---

## 📋 前置知识

- Python 函数、类和类型注解
- 异常处理与上下文管理器
- 列表、字典、队列等基础容器
- pytest 基本运行方式
- 网络请求和文件 I/O 的基本概念

如果你还不熟悉 `with` 语句，建议先复习上下文管理器。锁、线程池和资源释放都大量依赖这一模式。

---

## 🗂️ 文件导航

| 文件                                  | 用途                                       |
| ------------------------------------- | ------------------------------------------ |
| `lesson.md`                           | 详细教程（约 650 行）                      |
| `examples/01_threading_basics.py`     | Thread / start / join / daemon             |
| `examples/02_lock_synchronization.py` | Lock / RLock / Condition                   |
| `examples/03_threadpool.py`           | ThreadPoolExecutor / Future / as_completed |
| `exercises/exercise_01_producer_consumer.py`   | 生产者消费者练习骨架                       |
| `exercises/exercise_02_parallel_download.py`   | 并发下载练习骨架                           |
| `solutions/solution_01_producer_consumer.py`   | 线程安全容器参考答案                       |
| `solutions/solution_02_parallel_download.py`   | 可注入 fetch_url 的下载器参考答案          |
| `tests/test_threading.py`             | 线程与下载器测试                           |
| `tests/conftest.py`                   | 测试路径配置                               |

建议学习顺序：先读 `lesson.md`，再运行 `examples/`，然后完成 `exercises/`，最后用测试验证。

---

## 💡 核心知识点摘要

### 第一章：课程定位

线程用于让 I/O 等待期间的其他任务继续推进，是后端工程的基础能力。

### 第二章：学习目标

本课强调可验证目标：能启动线程、保护共享状态、处理 Future 异常并写稳定测试。

### 第三章：线程基础

`Thread` 对象创建后需要 `start()`，主线程用 `join()` 等待，daemon 线程不能承载关键写入。

### 第四章：同步原语

Lock 保护临界区，RLock 处理重入，Condition 等待条件，Event 广播信号，Semaphore 限制并发。

### 第五章：队列与生产者消费者

`queue.Queue` 是线程安全通道，`task_done()` 和 `join()` 能表达任务完成关系。

### 第六章：线程池

`ThreadPoolExecutor` 用固定工作线程执行任务，Future 负责承载结果和异常。

### 第七章：GIL 与 Python 3.13 Free-threading

GIL 限制 CPU 密集型 Python 字节码并行，但 I/O 线程仍有价值；free-threading 需要生态逐步适配。

### 第八章：实战与陷阱

并发下载器要隔离真实网络、集中收集结果，并规避竞态、死锁、遗漏异常和无界并发。

---

## 🚀 快速开始

进入项目根目录：

```bash
cd <项目根目录>
```

运行线程基础示例：

```bash
python stage2-engineering/lessons/L26-threading/examples/01_threading_basics.py
```

运行同步原语示例：

```bash
python stage2-engineering/lessons/L26-threading/examples/02_lock_synchronization.py
```

运行线程池示例：

```bash
python stage2-engineering/lessons/L26-threading/examples/03_threadpool.py
```

运行课程测试：

```bash
python -m pytest stage2-engineering/lessons/L26-threading/tests/ -o addopts="" -v
```

## 🛠️ 练习要求

### 练习 1：生产者消费者

- 实现 `ProducerConsumer` 类。
- 构造函数接收 `max_items`。
- `produce(count)` 生产递增整数。
- 多个线程同时调用时不能超过容量。
- `consume_all()` 返回当前全部数据并清空内部列表。
- `reset()` 清空状态并把下一个值重置为 0。
- 必须使用 Lock 保护共享状态。

### 练习 2：并发下载

- 实现 `parallel_download(urls, max_workers=5)`。
- 必须使用 `ThreadPoolExecutor`。
- 必须使用模块级 `fetch_url(url)`，便于测试替换。
- 不能访问真实网络。
- 单个 URL 失败时跳过该 URL。
- 返回值使用 `dict[str, str]`，键为 URL，值为下载内容。

---

## ✅ 完成标准

- [ ] 能解释 Thread、start、join、daemon 和线程命名。
- [ ] 能解释每种同步原语适合的场景。
- [ ] 能用 Queue 或 Lock 安全传递/保护数据。
- [ ] 能用 ThreadPoolExecutor 实现并发任务。
- [ ] 能处理 Future 异常。
- [ ] 能解释 GIL 对不同任务类型的影响。
- [ ] 能通过本课 ruff 与 pytest 验证。

---

## 🔗 下一步

[P03: 工程化综合项目](../P03-engineering-project/README.md)
