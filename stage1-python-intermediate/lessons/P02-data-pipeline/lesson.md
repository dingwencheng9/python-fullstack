# P02: 数据处理管道系统（Stage 1 收官项目）

> **课程编号**: P02
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 8-10 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: L10-L18 全部进阶课程
> **版本**: v1.0
> **最后更新**: 2026-08-06
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

---

## 📁 目录结构

```
P02-data-pipeline/
├── examples/               # 7 个教学示例
│   ├── 01_protocol_types.py
│   ├── 02_generator_pipeline.py
│   ├── 03_decorator_chain.py
│   ├── 04_descriptor_validators.py
│   ├── 05_async_processing.py
│   ├── 06_functional_pipeline.py
│   └── 07_complete_pipeline.py
├── exercises/              # 4 个练习模板
│   ├── 01_typed_pipeline.py
│   ├── 02_generator_pipeline.py
│   ├── 03_decorator_validators.py
│   └── 04_async_processor.py
├── solutions/              # 参考答案
│   ├── solution_01_typed_pipeline.py
│   ├── solution_02_generator_pipeline.py
│   ├── solution_03_decorator_validators.py
│   └── solution_04_async_processor.py
├── tests/                  # 测试用例
│   ├── conftest.py
│   ├── test_protocol.py
│   ├── test_generator.py
│   ├── test_decorator.py
│   └── test_async.py
├── data/                   # 示例数据
│   ├── users.json
│   └── users.csv
├── README.md
└── lesson.md
```

---

## 🚀 快速开始

### 运行示例

```bash
cd stage1-python-intermediate/lessons/P02-data-pipeline

# 运行所有示例
python examples/01_protocol_types.py
python examples/02_generator_pipeline.py
python examples/03_decorator_chain.py
python examples/04_descriptor_validators.py
python examples/05_async_processing.py
python examples/06_functional_pipeline.py
python examples/07_complete_pipeline.py

# 运行练习
python exercises/01_typed_pipeline.py
python exercises/02_generator_pipeline.py
python exercises/03_decorator_validators.py
python exercises/04_async_processor.py

# 运行测试
uv run pytest tests/ -v
```

---

## 📝 练习题概览

### 练习 1: 类型安全管道（L10）

**任务**：
- 定义 `ItemProcessor[T]` Protocol
- 实现 `UppercaseProcessor` 和 `LengthFilter`
- 实现 `TypedPipeline[T]` 泛型类

**验收标准**：
```python
pipeline = TypedPipeline[str]()
pipeline.add_processor(UppercaseProcessor())
result = list(pipeline.process(["hello", "world"]))
assert result == ["HELLO", "WORLD"]
```

### 练习 2: 生成器管道（L11-L12）

**任务**：
- 实现 `generator_pipeline` 组合多个生成器
- 实现 `batch_generator` 分批 yield
- 实现 `progress_tracker` 带 send() 的进度追踪

**验收标准**：
```python
tracker = progress_tracker(100)
next(tracker)
assert tracker.send(10) == 10
assert tracker.send(20) == 30
```

### 练习 3: 装饰器链（L14）

**任务**：
- 实现 `@log` 日志装饰器
- 实现 `@retry(max_attempts, delay)` 重试工厂
- 实现 `@validate(**schemas)` 验证工厂
- 实现 `@timeout(seconds)` 超时工厂

**验收标准**：
```python
@log
@retry(max_attempts=3)
@validate(name=str, age=int)
def register_user(name: str, age: int) -> dict:
    return {"name": name, "age": age}
```

### 练习 4: 异步处理（L16）

**任务**：
- 实现 `async_read_file` 异步读取
- 实现 `async_process_files` 并发处理
- 实现 `RateLimiter` 限流器
- 实现 `stream_process` 流式处理

**验收标准**：
```python
results = await async_process_files([fp1, fp2, fp3], max_concurrent=2)
assert len(results) == 3
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

## 💡 最佳实践

### 1. 类型安全优先

```python
# ✅ 好的做法：使用 Protocol 定义接口
class DataProcessor(Protocol[T]):
    def process(self, item: T) -> T: ...

# ❌ 不好的做法：缺少类型约束
class DataProcessor:
    def process(self, item):
        return item
```

### 2. 惰性计算原则

```python
# ✅ 好的做法：使用生成器避免一次性加载
def process_large_file(filepath):
    with open(filepath) as f:
        for line in f:
            yield parse(line)

# ❌ 不好的做法：一次性加载全部数据
def process_large_file(filepath):
    with open(filepath) as f:
        return [parse(line) for line in f]  # 内存爆炸风险
```

### 3. 装饰器组合顺序

```python
# ✅ 正确的顺序：从内到外
@log           # 最外层：最后执行
@retry        # 中间层：失败时重试
@validate     # 最内层：最先验证
def func():
    ...
# 执行顺序：validate → retry → log

# ❌ 错误的顺序
@validate
@retry
@log
def func():
    ...
```

---

## 🚀 扩展挑战

### 挑战 1: 添加类型守卫

```python
from typing import TypeGuard

def is_valid_record(data: dict) -> TypeGuard[Record]:
    """类型守卫：检查是否为有效记录"""
    return all(key in data for key in ("id", "name", "age", "score"))
```

### 挑战 2: 添加异步迭代器管道

```python
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

### 挑战 3: 添加性能指标收集

```python
from dataclasses import dataclass, field

@dataclass
class PerformanceMetrics:
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

- **Stage 2 L19**: [pytest 完整实战](../L19-pytest-complete/) - 学习如何为 P02 编写完整的测试套件
- **Stage 2 L20**: [现代化工具链](../L20-toolchain/) - 学习 uv、ruff、mypy 的工程化配置
- **Stage 2 L21**: [异步核心进阶](../L21-async-programming/) - 深入 asyncio 高级用法

---

## 🎓 Stage 1 知识点总结

```
Stage 1: Python 进阶
├── L10: 类型系统完整指南
│   ├── Protocol + TypeVar + 泛型
│   └── TypedDict + TypeGuard
├── L11: 迭代器与生成器
│   ├── __iter__ / __next__
│   ├── yield + 生成器表达式
│   └── itertools 工具
├── L12: 生成器进阶
│   ├── yield from 委托
│   ├── send() 双向通信
│   └── 异步生成器
├── L13: Python 高级特性
│   ├── 闭包
│   └── 上下文管理器
├── L14: 装饰器进阶
│   ├── functools.wraps
│   ├── 装饰器工厂
│   └── 装饰器链
├── L15: 描述符与属性
│   ├── __get__ / __set__ / __delete__
│   ├── __set_name__
│   └── 数据描述符 vs 非数据描述符
├── L16: 并发编程入门
│   ├── async / await
│   ├── asyncio.gather
│   └── AsyncIterator
├── L17: 函数式编程
│   ├── map / filter / reduce
│   ├── functools.reduce
│   └── 管道组合
└── L18: 正则表达式
    ├── re.compile
    └── 模式匹配

P02: 综合实战 ⭐
└── 整合以上所有知识点
```

---

**Stage 1 进阶完成！** 🎉

准备进入 **Stage 2: 现代工程** 阶段，学习 pytest、工具链和高级异步编程。
