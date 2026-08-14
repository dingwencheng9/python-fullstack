# L24: 高阶流控与异步协同

> **课程编号**: L24
> **所属阶段**: Stage 2 - 现代工程
> **预计时长**: 13 小时
> **难度**: ⭐⭐⭐⭐☆（中高级）
> **前置课程**: L19, L21, L23
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

>
> 1. 掌握异步生成器与流式数据处理
> 2. 理解 Generator/AsyncGenerator 完整类型语义
> 3. 使用 TaskGroup + Semaphore 实现结构化并发
> 4. 掌握 except\* ExceptionGroup 精细化异常处理
> 5. 能构建类型安全的流式 ETL 和生产级异步管道

## 📚 前置知识

```mermaid
flowchart TB
    subgraph Generators["异步生成器"]
        A[async generator]
        B[异步迭代]
        C[异常传播]
    end
    
    subgraph Context["异步上下文管理器"]
        D[@asynccontextmanager]
        E[资源管理]
        F[错误处理]
    end
    
    subgraph Error["错误处理模式"]
        G[重试机制]
        H[超时控制]
        I[优雅关闭]
    end
    
    A --> G
    D --> H
    G --> I
    
    style Generators fill:#e3f2fd
    style Context fill:#c8e6c9
    style Error fill:#fff3e0
```

**学习本课程前，你应该掌握：**

- **L19**: 异步编程核心（async/await、TaskGroup、异常处理）
- **L21**: Python 3.13 新体验（PEP 695 泛型、改进的错误消息）
- **L12**: 上下文管理器深入（`__enter__`/`__exit__`）

**如果你还没有学习以上课程，建议先完成前置课程。**

> ⚠️ **跃升预警**: 本课程是 Stage 2 中难度最高的课程之一（4★），也是从"基础异步"到"生产级工程"的关键跃升点。
> 建议按下方「学习路径建议」分 3 周渐进完成，不要试图一次啃完 13 小时。

---

## 🗓️ 学习路径建议（3 周渐进式）

> **为什么需要分周学习？**
>
> 本课程涉及异步生成器、TaskGroup、ExceptionGroup、PEP 695 类型系统等多个独立且高密度的主题。
> 分周学习可以：
>
> - 🧠 让每个概念有"消化期"
> - 🏗️ 每周末有可运行的项目输出（成就感）
> - 🔄 前一周的知识在下一周自然复用（螺旋上升）

### 📅 第 1 周：异步生成器基础（4h）

**目标**: 能从同步生成器写出异步生成器，理解完整类型语义

| 章节 | 内容                             | 预计时间 |
| ---- | -------------------------------- | -------- |
| 1.1  | 从同步 yield 到异步 yield        | 45min    |
| 1.2  | Generator[Y, S, R] 完整类型语义  | 45min    |
| 1.3  | AsyncGenerator[Y, S] 异步版本    | 45min    |
| 1.4  | **实战**: LLM Token 流处理模拟器 | 1h       |

**验证点**: 完成练习 1（同步生成器→异步生成器改写），运行 `pytest tests/test_solutions.py -v -k exercise_01`

---

### 📅 第 2 周：资源管理与并发控制（4h）

**目标**: 能用 async with 管理异步资源，理解 TaskGroup vs gather

| 章节 | 内容                              | 预计时间 |
| ---- | --------------------------------- | -------- |
| 2.1  | @contextmanager 装饰器深度解析    | 45min    |
| 2.2  | @asynccontextmanager 异步资源管理 | 45min    |
| 2.3  | 异步生成器作为上下文管理器        | 30min    |
| 2.4  | **实战**: 异步数据库流式查询器    | 1h       |
| 3.1  | TaskGroup + Semaphore 限流控制    | 1h       |

**验证点**: 完成练习 2（异步文件流读取器），运行 `pytest tests/test_solutions.py -v -k exercise_02`

---

### 📅 第 3 周：高级模式与生产实战（5h）

**目标**: 能构建类型安全的流式 ETL + 生产级日志处理系统

| 章节    | 内容                                           | 预计时间 |
| ------- | ---------------------------------------------- | -------- |
| 3.2-3.4 | 流式 HTTP + except\* ExceptionGroup + 爬虫管道 | 1.5h     |
| 4.1-4.4 | PEP 695 泛型 + collections.abc + mypy strict   | 1.5h     |
| 5.1-5.5 | 结构化并发 + ExitStack + 流式日志处理          | 2h       |

**验证点**: 完成 `examples/crawler_pipeline.py` 中的爬虫管道项目模板，运行 `pytest tests/test_examples.py -v`

**附加练习**: 完成练习 3（流式日志处理管道），运行 `pytest tests/test_solution_03.py -v`

---

### 🎯 跃升检查清单

进入下一周前确认：

**第 1 周 → 第 2 周**:

- [ ] 能写出类型正确的 `AsyncGenerator[Y, None]`
- [ ] 理解 Generator 三个类型参数的含义
- [ ] LLM Token 模拟器能正确流式输出

**第 2 周 → 第 3 周**:

- [ ] 能用 `@asynccontextmanager` 写异步上下文管理器
- [ ] 理解 TaskGroup vs asyncio.gather 的差异
- [ ] 能用 Semaphore 控制并发数

**全部完成**:

- [ ] 能解释 `except* ExceptionGroup` 与 `except` 的区别
- [ ] 能写出 PEP 695 风格的泛型函数
- [ ] 爬虫管道项目通过所有测试

---

## 第一部分：旧模式 vs 现代模式对比表

### 1. 生成器类型注解

| 场景           | ❌ 旧模式 (Python ≤3.8)     | ✅ 现代模式 (Python 3.13)    |
| -------------- | --------------------------- | ---------------------------- |
| 同步生成器     | `Iterator[int]`             | `Generator[int, None, None]` |
| 可发送生成器   | `Generator[int, Any, None]` | `Generator[int, str, None]`  |
| 带返回值生成器 | 无类型支持                  | `Generator[int, None, str]`  |
| 异步生成器     | `AsyncIterator[int]`        | `AsyncGenerator[int, None]`  |

### 2. 上下文管理器

| 场景       | ❌ 旧模式                   | ✅ 现代模式                      |
| ---------- | --------------------------- | -------------------------------- |
| 同步上下文 | 手写 `__enter__/__exit__`   | `@contextmanager` + `yield`      |
| 异步上下文 | 手写 `__aenter__/__aexit__` | `@asynccontextmanager` + `yield` |
| 资源清理   | `try/finally`               | `with` 语句自动清理              |
| 动态资源   | 手动管理列表                | `ExitStack` 自动栈管理           |

### 3. 异步并发控制

| 场景     | ❌ 旧模式                | ✅ 现代模式                     |
| -------- | ------------------------ | ------------------------------- |
| 并发执行 | `asyncio.gather(*tasks)` | `async with TaskGroup() as tg`  |
| 异常处理 | 单一异常捕获             | `except* ExceptionGroup` 多异常 |
| 取消任务 | 手动 `task.cancel()`     | TaskGroup 自动级联取消          |
| 限流控制 | 手动计数器               | `Semaphore(max_concurrent)`     |

### 4. 类型系统

| 场景     | ❌ 旧模式                     | ✅ 现代模式                       |
| -------- | ----------------------------- | --------------------------------- |
| 泛型函数 | `def func(x: T) -> T:`        | `def func[T](x: T) -> T:`         |
| 泛型类   | `class Box(Generic[T])`       | `class Box[T]:`                   |
| 类型别名 | `Alias = list[int]`           | `type Alias = list[int]`          |
| 协议类型 | `from typing import Protocol` | `from collections.abc import ...` |

### 5. 流式数据处理

| 场景     | ❌ 旧模式                  | ✅ 现代模式                       |
| -------- | -------------------------- | --------------------------------- |
| 同步流   | 返回 `list` 全部加载       | `yield` 逐条生成                  |
| 异步流   | `await` 等待全部完成       | `async for` 流式消费              |
| HTTP 流  | `response.text()` 全部读取 | `response.content.iter_chunked()` |
| 数据库流 | `fetchall()` 全部加载      | `cursor.fetchmany()` 批量流式     |

### 6. 错误处理

| 场景       | ❌ 旧模式                        | ✅ 现代模式                    |
| ---------- | -------------------------------- | ------------------------------ |
| 单一异常   | `except ValueError:`             | 保持不变                       |
| 多类型异常 | `except (ValueError, KeyError):` | 保持不变                       |
| 并发异常   | 只捕获第一个                     | `except* ValueError:` 捕获所有 |
| 异常组     | 无标准支持                       | `ExceptionGroup` 内置类型      |

---

## 第二部分：完整教学大纲

### 第 1 章：流式数据处理基础（3 小时）

#### 1.1 从同步 yield 到异步 yield

**核心概念**：

- `yield` 暂停函数执行，保存状态
- `async def` + `yield` = 异步生成器
- `async for` 消费异步生成器

**示例代码**：

```python
from collections.abc import Generator, AsyncGenerator
import asyncio

# 同步生成器
def sync_range(n: int) -> Generator[int, None, None]:
    """同步生成 0 到 n-1"""
    for i in range(n):
        yield i

# 异步生成器
async def async_range(n: int) -> AsyncGenerator[int, None]:
    """异步生成 0 到 n-1，模拟 I/O 延迟"""
    for i in range(n):
        await asyncio.sleep(0.1)  # 模拟异步 I/O
        yield i

# 消费异步生成器
async def main() -> None:
    async for num in async_range(5):
        print(f"接收到: {num}")
```

#### 1.2 Generator[YieldType, SendType, ReturnType] 完整语义

**类型参数解析**：

- `YieldType`：每次 `yield` 产生的值类型
- `SendType`：通过 `.send()` 发送给生成器的值类型
- `ReturnType`：生成器返回值类型（`return` 语句）

**示例代码**：

```python
from collections.abc import Generator

def echo_generator() -> Generator[str, str, int]:
    """
    YieldType: str (yield 产生字符串)
    SendType: str (接收字符串)
    ReturnType: int (返回整数)
    """
    count = 0
    while True:
        try:
            received = yield f"Echo {count}"
            if received:
                print(f"收到: {received}")
                count += 1
        except GeneratorExit:
            return count  # 返回处理总数

# 使用示例
gen = echo_generator()
print(next(gen))           # "Echo 0"
print(gen.send("Hello"))   # "Echo 1"
print(gen.send("World"))   # "Echo 2"
result = gen.close()       # 返回 2
```

#### 1.3 AsyncGenerator[YieldType, SendType] 异步版本

**注意**：异步生成器没有 `ReturnType`（Python 限制）

```python
from collections.abc import AsyncGenerator
import asyncio

async def async_echo() -> AsyncGenerator[str, str]:
    """异步回显生成器"""
    count = 0
    while True:
        received = yield f"Async Echo {count}"
        if received:
            await asyncio.sleep(0.1)  # 模拟异步处理
            print(f"处理: {received}")
            count += 1

async def main() -> None:
    gen = async_echo()
    print(await gen.asend(None))      # "Async Echo 0"
    print(await gen.asend("Task1"))   # "Async Echo 1"
    print(await gen.asend("Task2"))   # "Async Echo 2"
    await gen.aclose()
```

#### 1.4 实战：LLM Token 流处理模拟器

**需求**：模拟大语言模型流式输出，支持限流和取消

```python
from collections.abc import AsyncGenerator
from dataclasses import dataclass
import asyncio
import time

@dataclass(frozen=True)
class TokenChunk:
    """Token 块"""
    text: str
    timestamp: float
    sequence: int

async def llm_stream(
    prompt: str,
    max_tokens: int = 100,
    tokens_per_second: float = 20.0,
) -> AsyncGenerator[TokenChunk, None]:
    """模拟 LLM 流式输出"""
    words = prompt.split()
    interval = 1.0 / tokens_per_second

    for i, word in enumerate(words[:max_tokens]):
        await asyncio.sleep(interval)
        yield TokenChunk(
            text=word,
            timestamp=time.time(),
            sequence=i,
        )

async def consume_stream(prompt: str) -> None:
    """消费流式输出"""
    print(f"提示词: {prompt}\n输出: ", end="")

    async for chunk in llm_stream(prompt, tokens_per_second=10):
        print(chunk.text, end=" ", flush=True)

    print("\n完成!")

# 运行示例
# asyncio.run(consume_stream("Python 是一门优秀的编程语言"))
```

---

### 第 2 章：资源管理与流式协同（2.5 小时）

#### 2.1 @contextmanager 装饰器深度解析

**核心思想**：用生成器替代手写类

**❌ 旧模式（手写类）**：

```python
class FileManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = None

    def __enter__(self) -> TextIO:
        self.file = open(self.filename, 'r')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.file:
            self.file.close()
```

**✅ 现代模式（装饰器）**：

```python
from contextlib import contextmanager
from collections.abc import Generator
from typing import TextIO

@contextmanager
def file_manager(filename: str) -> Generator[TextIO, None, None]:
    """文件管理上下文"""
    file = open(filename, 'r')
    try:
        yield file  # 进入 with 块
    finally:
        file.close()  # 退出时自动执行

# 使用
with file_manager("data.txt") as f:
    content = f.read()
```

#### 2.2 @asynccontextmanager 异步资源管理

**异步版本示例**：

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import aiohttp

@asynccontextmanager
async def http_client() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """异步 HTTP 客户端上下文"""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()

# 使用
async def fetch_data(url: str) -> str:
    async with http_client() as session:
        async with session.get(url) as response:
            return await response.text()
```

#### 2.3 异步生成器作为上下文管理器

**结合生成器和上下文管理器**：

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import asyncio

@asynccontextmanager
async def monitored_task(
    name: str
) -> AsyncGenerator[asyncio.Queue[str], None]:
    """监控的任务队列"""
    queue: asyncio.Queue[str] = asyncio.Queue()

    async def worker() -> None:
        while True:
            item = await queue.get()
            if item is None:
                break
            print(f"[{name}] 处理: {item}")
            await asyncio.sleep(0.1)
            queue.task_done()

    task = asyncio.create_task(worker())

    try:
        yield queue  # 进入上下文
    finally:
        await queue.put(None)  # 发送停止信号
        await task  # 等待工作线程结束
        print(f"[{name}] 已清理")

# 使用示例
async def main() -> None:
    async with monitored_task("Worker") as queue:
        await queue.put("Task 1")
        await queue.put("Task 2")
        await queue.join()
```

#### 2.4 实战：异步数据库流式查询器

**需求**：从数据库流式读取大量数据，自动管理连接

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import TypedDict
import asyncpg

class UserRow(TypedDict):
    """用户行类型"""
    id: int
    name: str
    email: str

@dataclass(frozen=True)
class DBConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    user: str = "postgres"
    password: str = "secret"

@asynccontextmanager
async def db_connection(
    config: DBConfig
) -> AsyncGenerator[asyncpg.Connection, None]:
    """数据库连接上下文"""
    conn = await asyncpg.connect(
        host=config.host,
        port=config.port,
        database=config.database,
        user=config.user,
        password=config.password,
    )
    try:
        yield conn
    finally:
        await conn.close()

async def stream_users(
    config: DBConfig,
    batch_size: int = 100,
) -> AsyncGenerator[list[UserRow], None]:
    """流式查询用户"""
    async with db_connection(config) as conn:
        async with conn.transaction():
            cursor = await conn.cursor("SELECT id, name, email FROM users")

            while True:
                rows = await cursor.fetch(batch_size)
                if not rows:
                    break

                yield [
                    UserRow(
                        id=row["id"],
                        name=row["name"],
                        email=row["email"],
                    )
                    for row in rows
                ]

# 使用示例
async def process_users() -> None:
    config = DBConfig()
    total = 0

    async for batch in stream_users(config):
        total += len(batch)
        print(f"处理 {len(batch)} 个用户，累计 {total}")
```

---

### 第 3 章：生产级异步数据管道（3 小时）

#### 3.1 TaskGroup + Semaphore 限流控制

**核心概念**：

- `TaskGroup` 结构化并发，自动管理任务生命周期
- `Semaphore` 限制并发数量，防止资源耗尽

**示例代码**：

```python
import asyncio
from collections.abc import AsyncGenerator

async def fetch_url(url: str, semaphore: asyncio.Semaphore) -> str:
    """限流的 URL 请求"""
    async with semaphore:
        print(f"开始请求: {url}")
        await asyncio.sleep(1)  # 模拟网络请求
        return f"Response from {url}"

async def concurrent_fetch(
    urls: list[str],
    max_concurrent: int = 3,
) -> list[str]:
    """并发请求，限制并发数"""
    semaphore = asyncio.Semaphore(max_concurrent)
    results: list[str] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_url(url, semaphore))
            for url in urls
        ]

    # TaskGroup 退出时，所有任务已完成
    return [task.result() for task in tasks]

# 运行示例
# urls = [f"http://example.com/{i}" for i in range(10)]
# results = asyncio.run(concurrent_fetch(urls, max_concurrent=3))
```

#### 3.2 流式 HTTP 请求与响应

**使用 aiohttp 流式处理**：

```python
import aiohttp
from collections.abc import AsyncGenerator

async def stream_download(
    url: str,
    chunk_size: int = 8192,
) -> AsyncGenerator[bytes, None]:
    """流式下载文件"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()

            async for chunk in response.content.iter_chunked(chunk_size):
                yield chunk

async def download_to_file(url: str, filepath: str) -> int:
    """流式下载到文件"""
    total_bytes = 0

    async with aiofiles.open(filepath, 'wb') as f:
        async for chunk in stream_download(url):
            await f.write(chunk)
            total_bytes += len(chunk)
            print(f"已下载: {total_bytes / 1024:.2f} KB", end="\r")

    print(f"\n完成! 总计: {total_bytes / 1024:.2f} KB")
    return total_bytes
```

#### 3.3 except\* ExceptionGroup 精细化异常处理

**传统异常处理的问题**：

```python
# ❌ 只能捕获第一个异常
async def old_way() -> None:
    try:
        await asyncio.gather(
            task_that_raises_value_error(),
            task_that_raises_type_error(),
        )
    except ValueError:
        print("捕获 ValueError")  # 只捕获第一个
```

**✅ 现代方式（except\*）**：

```python
async def new_way() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_that_raises_value_error())
            tg.create_task(task_that_raises_type_error())
    except* ValueError as eg:
        print(f"捕获 {len(eg.exceptions)} 个 ValueError")
        for exc in eg.exceptions:
            print(f"  - {exc}")
    except* TypeError as eg:
        print(f"捕获 {len(eg.exceptions)} 个 TypeError")
        for exc in eg.exceptions:
            print(f"  - {exc}")
```

**完整示例**：

```python
from dataclasses import dataclass
import asyncio

@dataclass(frozen=True)
class TaskResult:
    """任务结果"""
    task_id: int
    success: bool
    data: str | None = None
    error: str | None = None

async def risky_task(task_id: int) -> str:
    """可能失败的任务"""
    await asyncio.sleep(0.1)
    if task_id % 3 == 0:
        raise ValueError(f"Task {task_id} failed with ValueError")
    if task_id % 5 == 0:
        raise TypeError(f"Task {task_id} failed with TypeError")
    return f"Result {task_id}"

async def process_tasks(n: int) -> list[TaskResult]:
    """处理多个任务，捕获所有异常"""
    results: list[TaskResult] = []

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(risky_task(i))
                for i in range(n)
            ]

        # 所有任务成功
        results = [
            TaskResult(i, True, task.result())
            for i, task in enumerate(tasks)
        ]

    except* ValueError as eg:
        for exc in eg.exceptions:
            task_id = int(str(exc).split()[1])
            results.append(TaskResult(task_id, False, error=str(exc)))

    except* TypeError as eg:
        for exc in eg.exceptions:
            task_id = int(str(exc).split()[1])
            results.append(TaskResult(task_id, False, error=str(exc)))

    return results
```

#### 3.4 实战：分布式爬虫流式数据管道

**完整代码**（200+ 行）：

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TypedDict
import asyncio
import aiohttp
from datetime import datetime

@dataclass(frozen=True)
class CrawlerConfig:
    """爬虫配置"""
    max_concurrent: int = 5
    timeout: float = 30.0
    retry_attempts: int = 3
    backoff_factor: float = 2.0

class PageResult(TypedDict):
    """页面结果"""
    url: str
    title: str
    status: int
    content_length: int
    crawled_at: str

@dataclass
class CrawlerStats:
    """爬虫统计"""
    total: int = 0
    success: int = 0
    failed: int = 0
    start_time: datetime = field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        return (self.success / self.total * 100) if self.total > 0 else 0.0

    @property
    def elapsed_seconds(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()

@asynccontextmanager
async def http_session(
    config: CrawlerConfig
) -> AsyncGenerator[aiohttp.ClientSession, None]:
    """HTTP 会话上下文"""
    timeout = aiohttp.ClientTimeout(total=config.timeout)
    connector = aiohttp.TCPConnector(limit=config.max_concurrent)

    session = aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
    )

    try:
        yield session
    finally:
        await session.close()

async def crawl_page(
    url: str,
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    config: CrawlerConfig,
) -> PageResult:
    """爬取单个页面"""
    async with semaphore:
        for attempt in range(config.retry_attempts):
            try:
                async with session.get(url) as response:
                    html = await response.text()

                    # 简单提取标题（生产环境用 BeautifulSoup）
                    title = "Untitled"
                    if "<title>" in html:
                        start = html.find("<title>") + 7
                        end = html.find("</title>", start)
                        title = html[start:end]

                    return PageResult(
                        url=url,
                        title=title,
                        status=response.status,
                        content_length=len(html),
                        crawled_at=datetime.now().isoformat(),
                    )

            except Exception as e:
                if attempt == config.retry_attempts - 1:
                    raise

                wait_time = config.backoff_factor ** attempt
                await asyncio.sleep(wait_time)

async def crawler_pipeline(
    urls: list[str],
    config: CrawlerConfig,
) -> AsyncGenerator[PageResult, None]:
    """爬虫流式管道"""
    stats = CrawlerStats(total=len(urls))
    semaphore = asyncio.Semaphore(config.max_concurrent)

    async with http_session(config) as session:
        try:
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(
                        crawl_page(url, session, semaphore, config)
                    )
                    for url in urls
                ]

            # 所有任务成功
            for task in tasks:
                result = task.result()
                stats.success += 1
                yield result

        except* aiohttp.ClientError as eg:
            stats.failed += len(eg.exceptions)
            print(f"网络错误: {len(eg.exceptions)} 个")

        except* asyncio.TimeoutError as eg:
            stats.failed += len(eg.exceptions)
            print(f"超时错误: {len(eg.exceptions)} 个")

        finally:
            print(f"\n爬取完成!")
            print(f"成功: {stats.success}/{stats.total}")
            print(f"失败: {stats.failed}/{stats.total}")
            print(f"成功率: {stats.success_rate:.2f}%")
            print(f"耗时: {stats.elapsed_seconds:.2f}s")

# 使用示例
async def main() -> None:
    urls = [f"https://example.com/page{i}" for i in range(20)]
    config = CrawlerConfig(max_concurrent=5)

    async for result in crawler_pipeline(urls, config):
        print(f"✓ {result['title']} ({result['status']})")

# asyncio.run(main())
```

---

### 第 4 章：现代类型系统与强约束（2 小时）

#### 4.1 PEP 695 泛型语法（def func[T](...)）

**❌ 旧语法**：

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

def first[T](items: list[T]) -> T | None:
    return items[0] if items else None
```

**✅ 新语法（Python 3.13）**：

```python
class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# 类型别名也简化了
type JSONValue = str | int | float | bool | None | list[JSONValue] | dict[str, JSONValue]
```

#### 4.2 collections.abc vs typing

**优先使用 collections.abc**（性能更好，是标准协议）：

```python
# ✅ 推荐
from collections.abc import (
    Generator,
    AsyncGenerator,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)

# ❌ 不推荐（typing 模块是旧的）
from typing import (
    Generator,  # 使用 collections.abc.Generator
    AsyncGenerator,
    Iterable,
    Iterator,
)
```

**实际应用**：

```python
from collections.abc import AsyncGenerator, Mapping
from typing import TypedDict

class Config(TypedDict):
    """配置字典"""
    host: str
    port: int
    timeout: float

async def stream_data(
    config: Mapping[str, object]  # 接受任意映射
) -> AsyncGenerator[bytes, None]:
    """流式数据生成器"""
    # 实现...
    yield b"data"
```

#### 4.3 mypy --strict 配置与验证

**pyproject.toml 配置**：

```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
```

**常见错误修复**：

```python
# ❌ 错误：缺少返回类型
async def fetch_data(url):
    return await get(url)

# ✅ 正确：完整类型注解
async def fetch_data(url: str) -> dict[str, object]:
    return await get(url)

# ❌ 错误：Any 泛型
def process(items: list) -> None:
    pass

# ✅ 正确：明确类型参数
def process(items: list[str]) -> None:
    pass
```

#### 4.4 实战：类型安全的流式 ETL 框架

**完整代码**：

```python
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import TypedDict, Protocol
import asyncio

# 输入数据类型
class RawData(TypedDict):
    """原始数据"""
    id: int
    name: str
    value: float

# 输出数据类型
class ProcessedData(TypedDict):
    """处理后数据"""
    id: int
    name_upper: str
    value_doubled: float
    category: str

# 转换函数协议
class Transformer[T, U](Protocol):
    """转换器协议"""
    async def __call__(self, item: T) -> U: ...

# 具体转换器
async def transform_data(raw: RawData) -> ProcessedData:
    """转换原始数据"""
    await asyncio.sleep(0.01)  # 模拟异步处理

    return ProcessedData(
        id=raw["id"],
        name_upper=raw["name"].upper(),
        value_doubled=raw["value"] * 2,
        category="A" if raw["value"] > 50 else "B",
    )

# ETL 管道
async def etl_pipeline[T, U](
    source: AsyncGenerator[T, None],
    transformer: Transformer[T, U],
    batch_size: int = 100,
) -> AsyncGenerator[list[U], None]:
    """流式 ETL 管道"""
    batch: list[U] = []

    async for item in source:
        transformed = await transformer(item)
        batch.append(transformed)

        if len(batch) >= batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

# 数据源
async def data_source() -> AsyncGenerator[RawData, None]:
    """模拟数据源"""
    for i in range(1000):
        await asyncio.sleep(0.001)
        yield RawData(
            id=i,
            name=f"Item{i}",
            value=float(i % 100),
        )

# 使用示例
async def main() -> None:
    total = 0

    async for batch in etl_pipeline(
        data_source(),
        transform_data,
        batch_size=50,
    ):
        total += len(batch)
        print(f"处理批次: {len(batch)} 条，累计: {total}")

        # 这里可以批量写入数据库
        # await db.insert_many(batch)

# asyncio.run(main())
```

---

### 第 5 章：高级模式与最佳实践（2.5 小时）

#### 5.1 异步生成器 + TaskGroup 结构化并发

**模式：生成器内部管理任务组**：

```python
from collections.abc import AsyncGenerator
import asyncio

async def parallel_stream[T](
    items: list[T],
    processor: Callable[[T], Awaitable[U]],
    max_concurrent: int = 5,
) -> AsyncGenerator[U, None]:
    """并行处理流"""
    queue: asyncio.Queue[U | None] = asyncio.Queue(maxsize=max_concurrent * 2)

    async def worker(item: T) -> None:
        result = await processor(item)
        await queue.put(result)

    async def producer() -> None:
        async with asyncio.TaskGroup() as tg:
            for item in items:
                tg.create_task(worker(item))
        await queue.put(None)  # 标记结束

    producer_task = asyncio.create_task(producer())

    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        await producer_task
```

#### 5.2 ExitStack 动态上下文管理

**场景：动态数量的资源需要管理**：

```python
from contextlib import ExitStack, asynccontextmanager
from collections.abc import AsyncGenerator
import asyncio

async def managed_resource(name: str) -> AsyncGenerator[str, None]:
    """需要管理的异步资源"""
    print(f"打开 {name}")
    try:
        yield name
    finally:
        print(f"关闭 {name}")
        await asyncio.sleep(0.1)

async def dynamic_resources(count: int) -> None:
    """动态管理多个资源"""
    async with ExitStack() as stack:
        resources = []

        for i in range(count):
            resource = await stack.enter_async_context(
                managed_resource(f"Resource-{i}")
            )
            resources.append(resource)

        print(f"所有 {len(resources)} 个资源已打开")
        await asyncio.sleep(1)

        # ExitStack 自动按相反顺序关闭所有资源
```

#### 5.3 异常处理与资源清理保证

**关键原则**：

1. 使用 `try/finally` 保证清理
2. 使用 `except*` 处理并发异常
3. 使用上下文管理器自动化清理

**完整示例**：

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def safe_pipeline() -> AsyncGenerator[asyncio.Queue[str], None]:
    """安全的数据管道"""
    queue: asyncio.Queue[str] = asyncio.Queue()
    workers: list[asyncio.Task[None]] = []

    try:
        # 启动工作线程
        for i in range(3):
            task = asyncio.create_task(worker(queue, f"Worker-{i}"))
            workers.append(task)

        yield queue

    finally:
        # 发送停止信号
        for _ in workers:
            await queue.put("STOP")

        # 等待所有工作线程
        try:
            await asyncio.gather(*workers)
        except Exception as e:
            print(f"清理时发生错误: {e}")

async def worker(queue: asyncio.Queue[str], name: str) -> None:
    """工作线程"""
    while True:
        item = await queue.get()
        if item == "STOP":
            break
        print(f"[{name}] 处理: {item}")
        await asyncio.sleep(0.1)
```

#### 5.4 性能优化与监控

**关键指标**：

- 吞吐量（每秒处理数）
- 延迟（P50, P95, P99）
- 错误率
- 资源使用（内存、连接数）

**监控代码**：

```python
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime
import asyncio
import time

@dataclass
class PerformanceMetrics:
    """性能指标"""
    total_processed: int = 0
    total_errors: int = 0
    start_time: float = field(default_factory=time.time)
    latencies: deque[float] = field(default_factory=lambda: deque(maxlen=1000))

    @property
    def throughput(self) -> float:
        """每秒处理数"""
        elapsed = time.time() - self.start_time
        return self.total_processed / elapsed if elapsed > 0 else 0.0

    @property
    def error_rate(self) -> float:
        """错误率"""
        total = self.total_processed + self.total_errors
        return self.total_errors / total * 100 if total > 0 else 0.0

    @property
    def p95_latency(self) -> float:
        """P95 延迟"""
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[index]

async def monitored_task(
    task_id: int,
    metrics: PerformanceMetrics,
) -> None:
    """带监控的任务"""
    start = time.time()

    try:
        await asyncio.sleep(0.1)  # 模拟工作

        latency = time.time() - start
        metrics.latencies.append(latency)
        metrics.total_processed += 1

    except Exception:
        metrics.total_errors += 1
        raise

async def run_with_monitoring() -> None:
    """运行并监控"""
    metrics = PerformanceMetrics()

    async with asyncio.TaskGroup() as tg:
        for i in range(100):
            tg.create_task(monitored_task(i, metrics))

    print(f"吞吐量: {metrics.throughput:.2f} tasks/s")
    print(f"错误率: {metrics.error_rate:.2f}%")
    print(f"P95 延迟: {metrics.p95_latency*1000:.2f}ms")
```

#### 5.5 实战：生产级流式日志处理系统

**需求**：

- 从多个来源收集日志
- 流式解析和过滤
- 批量写入存储
- 支持限流和背压
- 完整监控和错误处理

**完整代码**（见 examples/log_processor.py）

---

## 第三部分：练习题

### 练习 1：同步生成器改写为异步生成器

**任务**：将以下同步生成器改写为异步版本

```python
def read_lines(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# TODO: 改写为异步版本
# async def async_read_lines(filename: str) -> AsyncGenerator[str, None]:
#     ...
```

### 练习 2：实现异步文件流读取器

**任务**：实现一个异步文件读取器，支持：

- 按块读取（避免内存溢出）
- 自动资源管理（使用 @asynccontextmanager）
- 完整类型注解

---

## 📖 总结

### 核心知识点

- 本课程涵盖了课程的核心概念和工具
- 重点掌握了关键API的使用方法
- 通过实践案例加深了理解

### 学习收获

完成本课程后，你已经：

- 掌握了本课程的核心概念和工具
- 能够运用所学知识解决实际问题
- 为后续学习打下了坚实基础

### 学习检查清单

完成本课程后，确认你已经：

- [ ] 理解了本课程的核心概念
- [ ] 掌握了主要工具和API的使用
- [ ] 能够独立完成课程练习
- [ ] 可选：通过本课测试 `uv run pytest tests -q`

## 🔗 下一步

完成本课后继续学习：

- [L25: 极限抽象与性能优化](../L25-extreme-abstraction-performance/README.md)

> 📖 **学习路径提示**：L25 将学习抽象层次和性能优化策略。
