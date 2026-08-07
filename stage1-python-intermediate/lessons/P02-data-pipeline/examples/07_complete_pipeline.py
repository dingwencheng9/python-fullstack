"""P02 示例 7: 完整数据处理管道

整合所有进阶概念的综合示例：
- 类型系统 (Protocol + TypeVar)
- 生成器管道 (yield + yield from)
- 装饰器链 (@log + @retry + @validate)
- 描述符验证 (ValidatedField)
- 异步处理 (async/await)
- 函数式组合 (map/filter/reduce)

运行方式:
    python examples/07_complete_pipeline.py
"""

import asyncio
import functools
import json
import re
import time
from pathlib import Path
from typing import (
    TypeVar, Protocol, Iterator, AsyncIterator,
    Callable, dataclass, runtime_checkable
)
from dataclasses import field

T = TypeVar("T")
U = TypeVar("U")


# ============================================================
# 1. 装饰器
# ============================================================

def log(func: Callable) -> Callable:
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(*args, **kwargs)
    return wrapper


def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器工厂"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"[RETRY] {func.__name__} failed: {e}, retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator


# ============================================================
# 2. 描述符
# ============================================================

class ValidatedField:
    """数值验证描述符"""

    def __init__(
        self,
        *,
        pattern: str | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> None:
        self.pattern = re.compile(pattern) if pattern else None
        self.min_value = min_value
        self.max_value = max_value
        self.name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: any, objtype: type | None = None) -> any:
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj: any, value: any) -> None:
        if value is not None:
            if self.pattern and not self.pattern.match(str(value)):
                raise ValueError(f"{self.name} 验证失败: {value}")
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f"{self.name} 低于最小值")
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f"{self.name} 超过最大值")
        obj.__dict__[self.name] = value


# ============================================================
# 3. 数据模型
# ============================================================

@dataclass
class DataRecord:
    """数据记录"""
    id: str = field(default="", metadata={"validate": r"^\d{4}$"})
    name: str = field(default="")
    age: int = field(default=0)
    score: float = field(default=0.0)

    # 使用描述符进行验证
    _id = ValidatedField(pattern=r"^\d{4}$")
    _name = ValidatedField(pattern=r"^[A-Za-z一-龥]+$")
    _age = ValidatedField(min_value=0, max_value=150)
    _score = ValidatedField(min_value=0.0, max_value=100.0)

    def __post_init__(self) -> None:
        self._id = self.id
        self._name = self.name
        self._age = self.age
        self._score = self.score

    @classmethod
    def from_dict(cls, data: dict) -> "DataRecord":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            age=int(data.get("age", 0)),
            score=float(data.get("score", 0.0)),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "score": self.score,
        }

    def compute_grade(self) -> str:
        """根据分数计算等级"""
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        return "F"


# ============================================================
# 4. 类型协议
# ============================================================

@runtime_checkable
class DataSource(Protocol):
    """数据源协议"""
    def read(self) -> Iterator[dict]: ...


@runtime_checkable
class DataSink(Protocol):
    """数据汇协议"""
    def write(self, data: dict) -> None: ...


class JSONFileSource:
    """JSON 文件数据源"""
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def read(self) -> Iterator[dict]:
        """读取 JSON 文件"""
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        yield from data


class CSVFileSource:
    """CSV 文件数据源"""
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)

    def read(self) -> Iterator[dict]:
        """读取 CSV 文件"""
        import csv
        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row


# ============================================================
# 5. 生成器管道
# ============================================================

def generator_pipeline(
    source: Iterator[T],
    *transformers: Callable[[Iterator[T]], Iterator[U]]
) -> Iterator[U]:
    """生成器管道组合"""
    result: Iterator = source
    for transformer in transformers:
        result = transformer(result)
    yield from result


def filter_records(
    predicate: Callable[[dict], bool]
) -> Callable[[Iterator[dict]], Iterator[dict]]:
    """返回过滤转换器"""
    def transform(items: Iterator[dict]) -> Iterator[dict]:
        for item in items:
            if predicate(item):
                yield item
    return transform


def transform_record(
    transformer: Callable[[dict], dict]
) -> Callable[[Iterator[dict]], Iterator[dict]]:
    """返回记录转换器"""
    def transform(items: Iterator[dict]) -> Iterator[dict]:
        for item in items:
            yield transformer(item)
    return transform


def map_field(
    field: str,
    func: Callable
) -> Callable[[Iterator[dict]], Iterator[dict]]:
    """返回字段映射器"""
    def transform(items: Iterator[dict]) -> Iterator[dict]:
        for item in items:
            if field in item:
                item[field] = func(item[field])
            yield item
    return transform


# ============================================================
# 6. 异步处理
# ============================================================

async def async_read_json(filepath: Path) -> list[dict]:
    """异步读取 JSON"""
    await asyncio.sleep(0.01)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


async def async_process_file(filepath: Path) -> dict:
    """异步处理单个文件"""
    data = await async_read_json(filepath)
    return {
        "file": filepath.name,
        "records": len(data),
        "avg_score": sum(r.get("score", 0) for r in data) / len(data) if data else 0,
    }


async def async_process_multiple(
    filepaths: list[Path],
    max_concurrent: int = 3
) -> list[dict]:
    """并发处理多个文件"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_process(fp: Path) -> dict:
        async with semaphore:
            return await async_process_file(fp)

    return await asyncio.gather(*[bounded_process(fp) for fp in filepaths])


# ============================================================
# 7. 函数式聚合
# ============================================================

from functools import reduce

def aggregate_records(records: Iterator[dict]) -> dict:
    """聚合记录统计"""
    record_list = list(records)

    if not record_list:
        return {}

    scores = [r.get("score", 0) for r in record_list]
    ages = [r.get("age", 0) for r in record_list]

    return {
        "total": len(record_list),
        "avg_score": sum(scores) / len(scores),
        "max_score": max(scores),
        "min_score": min(scores),
        "avg_age": sum(ages) / len(ages),
        "age_range": (min(ages), max(ages)),
    }


def grade_distribution(records: Iterator[dict]) -> dict[str, int]:
    """计算等级分布"""
    dist: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for record in records:
        score = record.get("score", 0)
        if score >= 90:
            dist["A"] += 1
        elif score >= 80:
            dist["B"] += 1
        elif score >= 70:
            dist["C"] += 1
        elif score >= 60:
            dist["D"] += 1
        else:
            dist["F"] += 1

    return dist


# ============================================================
# 8. 完整管道
# ============================================================

@dataclass
class PipelineConfig:
    """管道配置"""
    min_score: float = 0.0
    max_score: float = 100.0
    min_age: int = 0
    max_age: int = 150
    max_concurrent: int = 3


class DataPipeline:
    """完整数据处理管道"""

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()

    @log
    @retry(max_attempts=2)
    def process_file(self, filepath: Path) -> dict:
        """处理单个文件"""
        source = JSONFileSource(filepath)

        # 管道：读取 → 过滤 → 转换 → 聚合
        pipeline = generator_pipeline(
            source.read(),
            filter_records(lambda r: r.get("age", 0) >= 18),  # 过滤未成年
            transform_record(lambda r: {**r, "processed": True}),  # 标记处理
            map_field("score", lambda s: float(s)),  # 转换分数类型
            map_field("age", lambda a: int(a)),  # 转换年龄类型
        )

        records = list(pipeline)
        stats = aggregate_records(iter(records))
        grades = grade_distribution(iter(records))

        return {
            "file": filepath.name,
            "records_processed": len(records),
            "statistics": stats,
            "grade_distribution": grades,
        }

    async def process_multiple_files(self, filepaths: list[Path]) -> list[dict]:
        """异步并发处理多个文件"""
        results = await async_process_multiple(filepaths, self.config.max_concurrent)
        return results

    def process_source(self, source: DataSource) -> dict:
        """处理通用数据源"""
        records = list(source.read())
        stats = aggregate_records(iter(records))
        grades = grade_distribution(iter(records))

        return {
            "total_records": len(records),
            "statistics": stats,
            "grade_distribution": grades,
        }


# ============================================================
# 演示
# ============================================================

def demonstrate_complete_pipeline():
    """演示完整管道"""
    print("\n=== 完整数据处理管道 ===")

    # 创建测试数据
    test_file = Path("examples/temp_data.json")
    test_data = [
        {"id": "0001", "name": "Alice", "age": 28, "score": 92.5},
        {"id": "0002", "name": "Bob", "age": 35, "score": 78.0},
        {"id": "0003", "name": "Carol", "age": 22, "score": 88.5},
        {"id": "0004", "name": "David", "age": 45, "score": 65.0},
        {"id": "0005", "name": "Eve", "age": 18, "score": 95.0},
    ]
    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    # 配置
    config = PipelineConfig(max_concurrent=2)

    # 创建管道
    pipeline = DataPipeline(config)

    # 处理文件
    print("\n处理文件:")
    result = pipeline.process_file(test_file)
    print(f"  文件: {result['file']}")
    print(f"  处理记录: {result['records_processed']}")
    print(f"  平均分: {result['statistics']['avg_score']:.1f}")
    print(f"  等级分布: {result['grade_distribution']}")

    # 清理
    test_file.unlink()


async def demonstrate_async_pipeline():
    """演示异步管道"""
    print("\n=== 异步并发处理 ===")

    # 创建测试文件
    test_files = []
    for i in range(3):
        test_file = Path(f"examples/temp_data_{i}.json")
        test_data = [
            {"id": f"000{j}", "name": f"User{j}", "age": 20 + j, "score": 80 + j * 2}
            for j in range(i * 2, i * 2 + 2)
        ]
        test_file.write_text(json.dumps(test_data), encoding="utf-8")
        test_files.append(test_file)

    # 处理
    config = PipelineConfig(max_concurrent=2)
    pipeline = DataPipeline(config)
    results = await pipeline.process_multiple_files(test_files)

    print("并发处理结果:")
    for result in results:
        print(f"  {result['file']}: {result['records']} 条记录")

    # 清理
    for f in test_files:
        f.unlink()


def demonstrate_data_record():
    """演示数据记录"""
    print("\n=== 数据记录验证 ===")

    try:
        record = DataRecord(id="0001", name="Alice", age=28, score=92.5)
        print(f"创建记录: {record}")
        print(f"计算等级: {record.compute_grade()}")

        # 测试验证
        print("\n测试描述符验证:")
        record.score = 150  # 应该抛出异常
    except ValueError as e:
        print(f"  ✗ 验证失败: {e}")

    try:
        record.name = "123"
    except ValueError as e:
        print(f"  ✗ 名称验证: {e}")


# ============================================================
# 主函数
# ============================================================

async def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 7: 完整数据处理管道")
    print("=" * 60)

    demonstrate_complete_pipeline()
    await demonstrate_async_pipeline()
    demonstrate_data_record()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
