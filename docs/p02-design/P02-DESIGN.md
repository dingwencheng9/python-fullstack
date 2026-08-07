# P02: 数据处理管道系统（Stage 1 收官项目）

> **课程编号**: P02
> **所属阶段**: Stage 1 - Python 进阶
> **建议学习时间**: 8-10 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: L10-L18 全部进阶课程
> **后续课程**: Stage 2 / L19 pytest
> **核心版本**: Python 3.13

---

## 🎯 学习目标

完成本项目后，你将能够：

1. **类型安全**：使用 Protocol + TypeVar 构建类型安全的数据处理管道
2. **惰性计算**：使用生成器实现内存高效的数据流处理
3. **横切关注点**：使用装饰器链实现日志、重试、验证的分离
4. **属性验证**：使用描述符实现字段级别的数据验证
5. **并发处理**：使用 async/await 实现 I/O 密集型任务的并发处理
6. **函数式组合**：使用 map/filter/reduce 构建数据转换管道
7. **文本解析**：使用正则表达式实现复杂的数据验证和提取

---

## 📖 项目导读

### 为什么做这个项目？

Stage 0 的 P01 教你如何组织基础语法（类、函数、文件操作）。

Stage 1 的 P02 教你如何组织**进阶语法**（类型注解、生成器、装饰器、描述符、异步、函数式）。

**核心问题**：当你有 9 个独立的进阶知识点时，如何把它们组合成一个有意义的项目？

**答案**：构建一个数据处理管道——这是 Python 工程中的常见场景，也是所有进阶语法天然适合的领域。

### 项目特点

| 特点 | 说明 |
|------|------|
| **类型安全** | Protocol 定义管道接口，TypeVar 实现泛型 |
| **惰性计算** | 生成器管道避免一次性加载全部数据 |
| **可组合** | 装饰器链式叠加（日志 → 验证 → 重试） |
| **可验证** | 描述符在属性赋值时进行数据校验 |
| **可并发** | async/await 同时处理多个数据源 |
| **可追踪** | 函数式管道让数据转换透明可见 |

---

## 📚 项目概述

### 项目：批量数据处理管道（Data Pipeline Processor）

从原始数据文件（CSV/JSON）到清洗、验证、转换、分析的完整数据处理系统。

### 功能需求

1. **数据读取**：从 CSV/JSON 文件读取原始数据
2. **数据验证**：使用正则表达式验证字段格式
3. **数据清洗**：使用描述符验证数值范围
4. **数据转换**：使用生成器管道进行惰性处理
5. **数据统计**：使用函数式编程进行聚合分析
6. **并发处理**：使用 async/await 并发处理多个文件
7. **管道组合**：使用装饰器链添加日志、重试、超时

### 技术栈

```
P02 数据处理管道
├── L10: 类型系统（Protocol + TypeVar + 泛型）
├── L11-L12: 生成器（yield + yield from + send()）
├── L14: 装饰器（@retry + @log + @validate）
├── L15: 描述符（ValidatedField 数值验证）
├── L16: 异步（async/await + gather）
├── L17: 函数式（map/filter/reduce + pipeline）
└── L18: 正则（re.compile + pattern matching）
```

---

## 🏗️ 项目架构

### 核心组件

```
┌─────────────────────────────────────────────────────────────────┐
│                    P02 数据处理管道系统                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │ DataSource  │───▶│ Pipeline    │───▶│ DataSink    │          │
│  │ (CSV/JSON) │    │ (生成器链)  │    │ (JSON/CSV)  │          │
│  └─────────────┘    └─────────────┘    └─────────────┘          │
│         │                 │                                       │
│         ▼                 ▼                                       │
│  ┌─────────────┐    ┌─────────────┐                              │
│  │ AsyncLoader │    │ Decorator   │                              │
│  │ (并发读取)  │    │ Chain       │                              │
│  └─────────────┘    └─────────────┘                              │
│                           │                                       │
│                           ▼                                       │
│                    ┌─────────────┐                                │
│                    │ Validators  │                                │
│                    │ (描述符)    │                                │
│                    └─────────────┘                                │
└─────────────────────────────────────────────────────────────────┘
```

### 目录结构

```
P02-data-pipeline/
├── README.md               # 项目入口
├── lesson.md               # 详细文档
├── pyproject.toml         # 项目配置
├── data/                   # 示例数据
│   ├── users.csv
│   └── orders.json
├── examples/               # 示例代码
│   ├── 01_protocol_types.py      # Protocol + TypeVar
│   ├── 02_generator_pipeline.py  # 生成器管道
│   ├── 03_decorator_chain.py    # 装饰器链
│   ├── 04_descriptor_validators.py # 描述符验证
│   ├── 05_async_processing.py    # 异步处理
│   ├── 06_functional_pipeline.py # 函数式管道
│   └── 07_complete_pipeline.py   # 完整管道
├── exercises/              # 练习题
│   ├── 01_typed_pipeline.py      # TODO: 类型安全管道
│   ├── 02_generator_pipeline.py  # TODO: 生成器管道
│   ├── 03_decorator_validators.py # TODO: 装饰器验证器
│   └── 04_async_processor.py     # TODO: 异步处理器
├── solutions/              # 参考答案
│   ├── __init__.py
│   ├── typed_pipeline.py
│   ├── generator_pipeline.py
│   ├── decorator_validators.py
│   └── async_processor.py
└── tests/                  # 测试用例
    ├── conftest.py
    ├── test_protocol.py
    ├── test_generator.py
    ├── test_decorator.py
    ├── test_descriptor.py
    └── test_async.py
```

---

## 📝 实现步骤

### 步骤 1: 类型定义（Protocol + TypeVar）

```python
# typed_pipeline.py
from typing import TypeVar, Protocol, Iterator

T = TypeVar("T")
U = TypeVar("U")

class DataSource(Protocol[T]):
    """数据源协议"""
    def read(self) -> Iterator[T]: ...

class DataSink(Protocol[T]):
    """数据汇协议"""
    def write(self, item: T) -> None: ...

class PipelineStage(Protocol[T, U]):
    """管道阶段协议"""
    def process(self, items: Iterator[T]) -> Iterator[U]: ...
```

### 步骤 2: 生成器管道

```python
# generator_pipeline.py
from typing import Iterator, Callable, TypeVar
import re

T = TypeVar("T")

def generator_pipeline(
    source: Iterator[T],
    *stages: Callable[[Iterator[T]], Iterator[T]]
) -> Iterator[T]:
    """生成器管道组合"""
    result = source
    for stage in stages:
        result = stage(result)
    yield from result

def filter_by_pattern(
    pattern: str,
    field: str
) -> Callable[[Iterator[dict]], Iterator[dict]]:
    """返回基于正则的过滤器"""
    compiled = re.compile(pattern, re.IGNORECASE)
    def _filter(items: Iterator[dict]) -> Iterator[dict]:
        for item in items:
            if compiled.search(str(item.get(field, ""))):
                yield item
    return _filter

def transform_field(
    field: str,
    func: Callable
) -> Callable[[Iterator[dict]], Iterator[dict]]:
    """返回字段转换器"""
    def _transform(items: Iterator[dict]) -> Iterator[dict]:
        for item in items:
            item[field] = func(item.get(field, ""))
            yield item
    return _transform
```

### 步骤 3: 装饰器链

```python
# decorators.py
import functools
import logging
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger(__name__)

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.debug(f"调用 {func.__name__} 参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} 返回: {result}")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器工厂"""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"{func.__name__} 失败，重试 {attempt + 1}/{max_attempts}")
                    time.sleep(delay)
        return wrapper
    return decorator

def validate_input(pattern: str):
    """输入验证装饰器工厂"""
    compiled = re.compile(pattern)
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 验证逻辑
            for arg in args:
                if isinstance(arg, str) and not compiled.match(arg):
                    raise ValueError(f"验证失败: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 步骤 4: 描述符验证

```python
# descriptors.py
import re
from typing import Any

class ValidatedField:
    """数值验证描述符"""

    def __init__(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
        pattern: str | None = None
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.pattern = re.compile(pattern) if pattern else None
        self.name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        return obj.__dict__.get(self.name)

    def __set__(self, obj: Any, value: Any) -> None:
        if self.pattern and value:
            if not self.pattern.match(str(value)):
                raise ValueError(f"{self.name} 不匹配模式: {self.pattern.pattern}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} 低于最小值 {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} 超过最大值 {self.max_value}")
        obj.__dict__[self.name] = value

class Record:
    """带验证的数据记录"""
    id = ValidatedField(pattern=r"^\d{4}$")
    name = ValidatedField(pattern=r"^[A-Za-z一-龥]+$")
    age = ValidatedField(min_value=0, max_value=150)
    score = ValidatedField(min_value=0, max_value=100)
```

### 步骤 5: 异步处理

```python
# async_processor.py
import asyncio
import json
from pathlib import Path
from typing import AsyncIterator

async def read_json_file(filepath: Path) -> list[dict]:
    """异步读取 JSON 文件"""
    await asyncio.sleep(0)  # 模拟 I/O
    return json.loads(filepath.read_text(encoding="utf-8"))

async def process_file(filepath: Path) -> dict:
    """处理单个文件"""
    data = await read_json_file(filepath)
    return {
        "file": filepath.name,
        "count": len(data),
        "records": data
    }

async def process_multiple_files(filepaths: list[Path]) -> list[dict]:
    """并发处理多个文件"""
    tasks = [process_file(fp) for fp in filepaths]
    return await asyncio.gather(*tasks)

async def stream_process(
    filepaths: list[Path],
    batch_size: int = 100
) -> AsyncIterator[dict]:
    """流式处理文件"""
    for fp in filepaths:
        data = await read_json_file(fp)
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            yield {"batch": batch, "file": fp.name}
```

### 步骤 6: 函数式管道

```python
# functional_pipeline.py
from functools import reduce
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")
U = TypeVar("U")

def pipeline(*functions: Callable) -> Callable[[T], U]:
    """函数组合管道"""
    def composed(data: T) -> U:
        return reduce(lambda x, f: f(x), functions, data)
    return composed

def chunk(size: int) -> Callable[[Iterator[T]], Iterator[list[T]]]:
    """分块处理"""
    def _chunk(items: Iterator[T]) -> Iterator[list[T]]:
        batch = []
        for item in items:
            batch.append(item)
            if len(batch) >= size:
                yield batch
                batch = []
        if batch:
            yield batch
        return _chunk

# 使用示例
stats = pipeline(
    lambda data: data,  # 源数据
    lambda d: d.values(),  # 提取值
    lambda v: filter(lambda x: x["active"], v),  # 过滤
    lambda v: map(lambda x: x["score"], v),  # 映射
    lambda s: list(s),  # 收集
    lambda scores: {
        "count": len(scores),
        "avg": sum(scores) / len(scores) if scores else 0,
        "max": max(scores) if scores else 0,
        "min": min(scores) if scores else 0,
    }
)
```

### 步骤 7: 完整管道整合

```python
# complete_pipeline.py
from dataclasses import dataclass
from typing import Protocol, TypeVar, Iterator, AsyncIterator
import re

# 类型定义
T = TypeVar("T")

class DataProcessor(Protocol[T]):
    """数据处理器协议"""
    def process(self, data: T) -> T: ...

@dataclass
class PipelineConfig:
    """管道配置"""
    min_score: int = 0
    max_score: int = 100
    batch_size: int = 100
    enable_logging: bool = True
    max_retries: int = 3

class DataPipeline:
    """完整数据处理管道"""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self._validators: list[re.Pattern] = []
        self._processors: list[DataProcessor] = []

    def add_validator(self, pattern: str) -> "DataPipeline":
        """添加验证规则"""
        self._validators.append(re.compile(pattern))
        return self

    def add_processor(self, processor: DataProcessor) -> "DataPipeline":
        """添加处理器"""
        self._processors.append(processor)
        return self

    def process_stream(self, items: Iterator[dict]) -> Iterator[dict]:
        """处理数据流"""
        for item in items:
            # 验证
            if not self._validate(item):
                continue
            # 处理
            for processor in self._processors:
                item = processor.process(item)
            yield item

    def _validate(self, item: dict) -> bool:
        """验证数据"""
        for pattern in self._validators:
            for field, value in item.items():
                if isinstance(value, str) and not pattern.search(value):
                    return False
        return True
```

---

## 🎯 练习题设计

### Exercise 1: 类型安全管道（对应 L10）

```python
# exercises/01_typed_pipeline.py
"""P02 练习 1: 类型安全的数据处理管道

难度: ⭐⭐⭐⭐
知识点: Protocol + TypeVar + 泛型

任务：
1. 定义 ItemProcessor Protocol，支持 process(item) 方法
2. 实现 UppercaseProcessor：将字符串字段转为大写
3. 实现 LengthFilter：过滤超过指定长度的字段
4. 实现 TypedPipeline[T] 泛型类，支持链式调用

预期输出：
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    result = list(pipeline.process(["hello", "world"]))
    assert result == ["HELLO", "WORLD"]
"""

from typing import TypeVar, Protocol, Iterator

T = TypeVar("T")

# TODO: 定义 ItemProcessor Protocol
class ItemProcessor(Protocol[T]):
    """数据处理器协议"""
    ...

# TODO: 实现 UppercaseProcessor
class UppercaseProcessor:
    """字符串转大写处理器"""
    ...

# TODO: 实现 LengthFilter
class LengthFilter:
    """按长度过滤"""
    def __init__(self, max_length: int) -> None:
        self.max_length = max_length
    ...

# TODO: 实现 TypedPipeline 泛型类
class TypedPipeline:
    """类型安全的数据管道"""
    def __init__(self) -> None:
        ...

    def add_processor(self, processor: ItemProcessor) -> "TypedPipeline":
        """添加处理器"""
        ...

    def process(self, items: Iterator[T]) -> Iterator[T]:
        """处理数据流"""
        ...
```

### Exercise 2: 生成器管道（对应 L11-L12）

```python
# exercises/02_generator_pipeline.py
"""P02 练习 2: 生成器数据处理管道

难度: ⭐⭐⭐⭐
知识点: yield + yield from + send()

任务：
1. 实现 generator_pipeline 函数，组合多个生成器
2. 实现 batch_generator 分批 yield
3. 实现 yield_from_chain 链接多个迭代器
4. 使用 send() 实现进度追踪

预期行为：
    def counter():
        total = 0
        while True:
            increment = yield total
            total += increment or 1

    c = counter()
    next(c)  # 初始化
    c.send(5)  # 返回 5
    c.send(3)  # 返回 8
"""

from typing import Iterator, Callable, TypeVar, Generator

T = TypeVar("T")

# TODO: 实现 generator_pipeline
def generator_pipeline(
    source: Iterator[T],
    *transformers: Callable[[Iterator[T]], Iterator[T]]
) -> Iterator[T]:
    """组合多个转换生成器"""
    ...

# TODO: 实现 batch_generator
def batch_generator(items: Iterator[T], batch_size: int) -> Generator[list[T], None, None]:
    """分批 yield 数据"""
    ...

# TODO: 实现带 send() 的进度追踪器
def progress_tracker(total: int) -> Generator[None, int, int]:
    """追踪进度的生成器"""
    ...

# TODO: 实现 yield from 链
def flatten(nested_iterators: Iterator[Iterator[T]]) -> Iterator[T]:
    """展平嵌套迭代器"""
    ...
```

### Exercise 3: 装饰器验证器（对应 L14）

```python
# exercises/03_decorator_validators.py
"""P02 练习 3: 装饰器链实现验证器

难度: ⭐⭐⭐⭐
知识点: 装饰器工厂 + functools.wraps + 装饰器链

任务：
1. 实现 @log 装饰器，记录函数调用
2. 实现 @retry(max_attempts) 装饰器工厂
3. 实现 @validate(**schemas) 验证参数
4. 实现 @timeout(seconds) 超时装饰器
5. 组合使用多个装饰器

预期行为：
    @log
    @retry(max_attempts=3)
    @validate(name=str, age=int)
    def register_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}
"""

import functools
import time
import logging
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger(__name__)

# TODO: 实现 @log 装饰器
def log(func: Callable[P, R]) -> Callable[P, R]:
    """日志装饰器"""
    ...

# TODO: 实现 @retry 装饰器工厂
def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂"""
    ...

# TODO: 实现 @validate 装饰器工厂
def validate(**schemas):
    """参数验证装饰器工厂"""
    ...

# TODO: 实现 @timeout 装饰器工厂
def timeout(seconds: float):
    """超时装饰器工厂"""
    ...
```

### Exercise 4: 异步处理器（对应 L16）

```python
# exercises/04_async_processor.py
"""P02 练习 4: 异步数据处理

难度: ⭐⭐⭐⭐
知识点: async/await + gather + Semaphore

任务：
1. 实现 async_read_file 异步读取
2. 实现 async_process_files 并发处理
3. 实现 RateLimiter 限流器
4. 实现带超时的异步处理

预期行为：
    async def main():
        results = await async_process_files(["a.json", "b.json", "c.json"])
        assert len(results) == 3
"""

import asyncio
from pathlib import Path
from typing import AsyncIterator

# TODO: 实现异步文件读取
async def async_read_file(filepath: Path) -> dict:
    """异步读取文件"""
    ...

# TODO: 实现并发文件处理
async def async_process_files(
    filepaths: list[Path],
    max_concurrent: int = 5
) -> list[dict]:
    """并发处理多个文件"""
    ...

# TODO: 实现限流器
class RateLimiter:
    """异步限流器"""
    def __init__(self, rate: float, per: float):
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_update = None

    async def acquire(self) -> None:
        """获取令牌"""
        ...

# TODO: 实现流式处理
async def stream_process(
    filepaths: list[Path],
    batch_size: int = 100
) -> AsyncIterator[dict]:
    """流式处理数据"""
    ...
```

---

## 🧪 测试用例设计

### test_protocol.py

```python
# tests/test_protocol.py
"""Protocol + TypeVar 类型测试"""
import pytest
from solutions.typed_pipeline import (
    ItemProcessor,
    UppercaseProcessor,
    LengthFilter,
    TypedPipeline,
)

def test_processor_protocol():
    """验证 Protocol 定义正确"""
    proc: ItemProcessor = UppercaseProcessor()
    assert callable(proc.process)

def test_uppercase_processor():
    """测试大写处理器"""
    processor = UppercaseProcessor()
    assert processor.process("hello") == "HELLO"
    assert processor.process("World") == "WORLD"

def test_length_filter():
    """测试长度过滤器"""
    filter_ = LengthFilter(max_length=5)
    assert filter_.process("hi") is True
    assert filter_.process("hello world") is False

def test_typed_pipeline():
    """测试泛型管道"""
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    result = list(pipeline.process(["hello", "world"]))
    assert result == ["HELLO", "WORLD"]

def test_pipeline_chain():
    """测试管道链式调用"""
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    pipeline.add_processor(LengthFilter(max_length=10))
    result = list(pipeline.process(["hello", "world", "this is long"]))
    assert result == ["HELLO", "WORLD"]
```

### test_generator.py

```python
# tests/test_generator.py
"""生成器管道测试"""
import pytest
from solutions.generator_pipeline import (
    generator_pipeline,
    batch_generator,
    progress_tracker,
    flatten,
)

def test_batch_generator():
    """测试分批生成器"""
    items = range(10)
    batches = list(batch_generator(items, batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert len(batches) == 4

def test_progress_tracker():
    """测试进度追踪器"""
    tracker = progress_tracker(100)
    next(tracker)  # 初始化
    assert tracker.send(10) == 10
    assert tracker.send(20) == 30
    assert tracker.send(5) == 35

def test_flatten():
    """测试嵌套迭代器展平"""
    nested = [[1, 2], [3, 4], [5]]
    result = list(flatten(iter(nested)))
    assert result == [1, 2, 3, 4, 5]

def test_generator_pipeline():
    """测试生成器管道组合"""
    source = iter([1, 2, 3, 4, 5])
    def double(items):
        for x in items:
            yield x * 2
    def filter_even(items):
        for x in items:
            if x % 4 == 0:
                yield x

    result = list(generator_pipeline(source, double, filter_even))
    assert result == [4, 8]
```

### test_decorator.py

```python
# tests/test_decorator.py
"""装饰器链测试"""
import pytest
import time
from solutions.decorator_validators import (
    log,
    retry,
    validate,
    timeout,
)

def test_log_decorator(caplog):
    """测试日志装饰器"""
    @log
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    assert result == 3
    assert "调用 add" in caplog.text

def test_retry_decorator():
    """测试重试装饰器"""
    attempts = []

    @retry(max_attempts=3, delay=0.01)
    def flaky_function():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("暂未成功")
        return "成功"

    result = flaky_function()
    assert result == "成功"
    assert len(attempts) == 3

def test_validate_decorator():
    """测试验证装饰器"""
    @validate(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    result = create_user(name="Alice", age=25)
    assert result == {"name": "Alice", "age": 25}

    with pytest.raises(TypeError):
        create_user(name="Bob", age="invalid")  # type: ignore

def test_timeout_decorator():
    """测试超时装饰器"""
    @timeout(seconds=0.1)
    def slow_function():
        time.sleep(1)
        return "完成"

    with pytest.raises(TimeoutError):
        slow_function()
```

### test_descriptor.py

```python
# tests/test_descriptor.py
"""描述符验证测试"""
import pytest
from solutions.descriptors import Record, ValidatedField

def test_valid_record():
    """测试有效记录"""
    record = Record()
    record.id = "1234"
    record.name = "Alice"
    record.age = 25
    record.score = 95.5
    assert record.id == "1234"
    assert record.name == "Alice"

def test_invalid_id():
    """测试无效 ID"""
    record = Record()
    with pytest.raises(ValueError, match="不匹配模式"):
        record.id = "abc"  # 应该匹配 4 位数字

def test_invalid_age():
    """测试无效年龄"""
    record = Record()
    with pytest.raises(ValueError, match="低于最小值"):
        record.age = -1

    with pytest.raises(ValueError, match="超过最大值"):
        record.age = 200

def test_invalid_score():
    """测试无效分数"""
    record = Record()
    with pytest.raises(ValueError):
        record.score = 150  # 超过 100
```

### test_async.py

```python
# tests/test_async.py
"""异步处理测试"""
import pytest
import asyncio
from pathlib import Path
from solutions.async_processor import (
    async_read_file,
    async_process_files,
    RateLimiter,
    stream_process,
)

@pytest.mark.asyncio
async def test_async_read_file(tmp_path):
    """测试异步文件读取"""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"name": "test"}')

    result = await async_read_file(test_file)
    assert result == {"name": "test"}

@pytest.mark.asyncio
async def test_async_process_files(tmp_path):
    """测试并发文件处理"""
    files = []
    for i in range(3):
        f = tmp_path / f"file{i}.json"
        f.write_text(f'{{"id": {i}}}')
        files.append(f)

    results = await async_process_files(files, max_concurrent=2)
    assert len(results) == 3

@pytest.mark.asyncio
async def test_rate_limiter():
    """测试限流器"""
    limiter = RateLimiter(rate=2, per=1.0)

    start = asyncio.get_event_loop().time()
    await limiter.acquire()
    await limiter.acquire()
    elapsed = asyncio.get_event_loop().time() - start

    # 应该至少经过 1 秒
    assert elapsed >= 0.9

@pytest.mark.asyncio
async def test_stream_process(tmp_path):
    """测试流式处理"""
    test_file = tmp_path / "data.json"
    test_file.write_text('{"items": [1, 2, 3, 4, 5]}')

    batches = []
    async for batch in stream_process([test_file], batch_size=2):
        batches.append(batch)

    assert len(batches) == 3  # [1,2], [3,4], [5]
```

---

## 📊 知识点覆盖矩阵

| 课程 | 知识点 | 在 P02 中的应用 | 文件位置 |
|------|--------|----------------|----------|
| L10 | Protocol | `ItemProcessor` 接口定义 | `typed_pipeline.py` |
| L10 | TypeVar | 泛型 `T` | `typed_pipeline.py` |
| L10 | 泛型约束 | `PipelineStage[T, U]` | `typed_pipeline.py` |
| L11 | yield | 生成器管道 | `generator_pipeline.py` |
| L11 | 生成器表达式 | 字段转换 | `generator_pipeline.py` |
| L12 | yield from | 管道组合 | `generator_pipeline.py` |
| L12 | send() | 进度追踪 | `generator_pipeline.py` |
| L14 | @functools.wraps | 装饰器保留元数据 | `decorators.py` |
| L14 | 装饰器工厂 | `@retry(n)` 工厂函数 | `decorators.py` |
| L14 | 装饰器链 | 日志→验证→重试 | `decorators.py` |
| L15 | `__get__`/`__set__` | ValidatedField 描述符 | `descriptors.py` |
| L15 | `__set_name__` | 自动获取属性名 | `descriptors.py` |
| L16 | async/await | 异步文件处理 | `async_processor.py` |
| L16 | asyncio.gather | 并发任务 | `async_processor.py` |
| L16 | AsyncIterator | 流式处理 | `async_processor.py` |
| L17 | map/filter/reduce | 数据转换管道 | `functional_pipeline.py` |
| L17 | functools.reduce | 函数组合 | `functional_pipeline.py` |
| L18 | re.compile | 预编译正则 | `decorators.py` |
| L18 | pattern.match | 字段验证 | `descriptors.py` |

---

## 🚀 扩展挑战

### 挑战 1: 添加类型守卫

```python
# 类型守卫： Narrow[T] → bool
from typing import TypeGuard

def is_valid_record(data: dict) -> TypeGuard[Record]:
    """类型守卫：检查是否为有效记录"""
    return all(
        key in data
        for key in ("id", "name", "age", "score")
    )
```

### 挑战 2: 添加异步迭代器

```python
# AsyncGenerator: yield 无阻塞
async def async_generator_pipeline(
    source: AsyncIterator[dict],
    *processors: Callable[[dict], dict]
) -> AsyncIterator[dict]:
    """异步生成器管道"""
    async for item in source:
        for processor in processors:
            item = processor(item)
        yield item
```

### 挑战 3: 添加性能指标

```python
# 装饰器收集性能数据
from dataclasses import dataclass, field

@dataclass
class PerformanceMetrics:
    """性能指标"""
    calls: int = 0
    total_time: float = 0.0
    errors: int = 0
    _history: list[float] = field(default_factory=list)

    @property
    def avg_time(self) -> float:
        return self.total_time / self.calls if self.calls else 0
```

---

## ✅ 完成标准

完成 P02 后，你应该能够：

- [ ] 定义 TypeVar + Protocol 实现类型安全的管道接口
- [ ] 使用生成器 + yield from 实现惰性数据处理
- [ ] 使用装饰器工厂实现可组合的横切关注点（日志、验证、重试）
- [ ] 使用描述符实现字段级别的数据验证
- [ ] 使用 async/await + gather 实现并发 I/O 处理
- [ ] 使用 map/filter/reduce 实现函数式数据转换
- [ ] 组合以上所有技术构建完整的数据处理管道

---

## 🔗 下一步学习

恭喜完成 Stage 1！

- **Stage 2 L19**: pytest 完整实战 - 学习如何为 P02 编写完整的测试套件
- **Stage 2 L20**: 现代化工具链 - 学习 uv、ruff、mypy 的工程化配置

---

**Stage 1 知识点总结**：
- L10-L18 进阶语法 → P02 综合实战 ✅
- 准备进入 Stage 2 工程化阶段 🚀
