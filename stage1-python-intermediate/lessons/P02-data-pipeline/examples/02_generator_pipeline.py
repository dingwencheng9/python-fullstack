"""P02 示例 2: 生成器管道

演示 L11-L12 的生成器核心概念：
- yield 生成器函数
- yield from 委托
- send() 双向通信
- 生成器表达式

运行方式:
    python examples/02_generator_pipeline.py
"""

from typing import Iterator, Callable, Generator, TypeVar
from pathlib import Path
import csv
import json

T = TypeVar("T")
U = TypeVar("U")


# ============================================================
# 1. 基础生成器
# ============================================================

def simple_generator():
    """最简单的生成器"""
    yield 1
    yield 2
    yield 3


def counter_generator(stop: int):
    """计数器生成器"""
    n = 0
    while n < stop:
        yield n
        n += 1


# ============================================================
# 2. 生成器管道
# ============================================================

def generator_pipeline(
    source: Iterator[T],
    *transformers: Callable[[Iterator[T]], Iterator[U]]
) -> Iterator[U]:
    """组合多个转换生成器"""
    result: Iterator = source
    for transformer in transformers:
        result = transformer(result)
    yield from result


def filter_transformer(predicate: Callable[[T], bool]) -> Callable[[Iterator[T]], Iterator[T]]:
    """返回过滤器生成器"""
    def transform(items: Iterator[T]) -> Iterator[T]:
        for item in items:
            if predicate(item):
                yield item
    return transform


def map_transformer(func: Callable[[T], U]) -> Callable[[Iterator[T]], Iterator[U]]:
    """返回映射生成器"""
    def transform(items: Iterator[T]) -> Iterator[U]:
        yield from map(func, items)
    return transform


# ============================================================
# 3. yield from 委托
# ============================================================

def nested_generator():
    """嵌套生成器 - 使用 yield from"""
    yield from [1, 2, 3]
    yield from [4, 5, 6]
    yield from [7, 8, 9]


def flatten_nested(iterables: Iterator[Iterator[T]]) -> Iterator[T]:
    """展平嵌套迭代器 - yield from"""
    for iterable in iterables:
        yield from iterable


# ============================================================
# 4. send() 双向通信
# ============================================================

def progress_tracker(total: int) -> Generator[None, int, int]:
    """进度追踪生成器

    特点：
    - 首次调用 next() 初始化
    - 使用 send(value) 发送增量值
    - 返回累积进度
    """
    progress = 0
    while progress < total:
        increment = yield progress  # 产出当前进度，接收增量
        if increment is None:
            increment = 1
        progress += increment
    return progress  # 生成器结束时返回最终值


def running_average() -> Generator[float, float | None, None]:
    """计算移动平均的生成器

    用法：
        gen = running_average()
        next(gen)  # 初始化
        avg = gen.send(10)  # avg = 10.0
        avg = gen.send(20)  # avg = 15.0
        avg = gen.send(30)  # avg = 20.0
    """
    total = 0.0
    count = 0
    while True:
        value = yield total / count if count > 0 else 0.0
        total += value
        count += 1


# ============================================================
# 5. 批处理生成器
# ============================================================

def batch_generator(items: Iterator[T], batch_size: int) -> Generator[list[T], None, None]:
    """分批 yield 数据

    用于处理大量数据时减少内存占用。
    """
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def window_generator(items: Iterator[T], window_size: int) -> Generator[list[T], None, None]:
    """滑动窗口生成器

    生成固定大小的滑动窗口。
    """
    window: list[T] = []
    for item in items:
        window.append(item)
        if len(window) >= window_size:
            yield window
            window = window[1:]  # 移除最旧的元素


# ============================================================
# 6. 管道组合示例
# ============================================================

def read_csv_as_dict(filepath: str) -> Iterator[dict]:
    """从 CSV 文件读取字典"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        yield from reader


def read_json_lines(filepath: str) -> Iterator[dict]:
    """从 JSON Lines 文件读取"""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def validate_record(record: dict) -> bool:
    """验证记录"""
    required = ["id", "name", "score"]
    return all(field in record for field in required)


def parse_score(record: dict) -> dict:
    """解析分数字段"""
    record["score"] = float(record.get("score", 0))
    return record


def compute_grade(score: float) -> str:
    """根据分数计算等级"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


# ============================================================
# 演示函数
# ============================================================

def demonstrate_basic_generators():
    """演示基础生成器"""
    print("\n=== 基础生成器 ===")

    print("simple_generator():")
    for item in simple_generator():
        print(f"  {item}")

    print("counter_generator(5):")
    for item in counter_generator(5):
        print(f"  {item}")


def demonstrate_yield_from():
    """演示 yield from"""
    print("\n=== yield from 委托 ===")

    print("nested_generator():")
    for item in nested_generator():
        print(f"  {item}", end=" ")
    print()

    print("flatten_nested([[1,2], [3,4], [5]]):")
    nested = [[1, 2], [3, 4], [5]]
    for item in flatten_nested(iter(nested)):
        print(f"  {item}", end=" ")
    print()


def demonstrate_send():
    """演示 send()"""
    print("\n=== send() 双向通信 ===")

    print("progress_tracker(100):")
    tracker = progress_tracker(100)
    next(tracker)  # 初始化

    for increment in [20, 20, 20, 20]:
        try:
            progress = tracker.send(increment)
            print(f"  进度: {progress}/100")
        except StopIteration as e:
            print(f"  完成! 总进度: {e.value}")
            break

    print("\nrunning_average():")
    avg_gen = running_average()
    next(avg_gen)  # 初始化

    for value in [10, 20, 30, 40, 50]:
        result = avg_gen.send(value)
        print(f"  发送 {value} → 平均 {result:.2f}")


def demonstrate_batch():
    """演示批处理"""
    print("\n=== 批处理生成器 ===")

    print("batch_generator(range(10), batch_size=3):")
    for batch in batch_generator(range(10), batch_size=3):
        print(f"  批次: {batch}")

    print("window_generator(range(5), window_size=3):")
    for window in window_generator(iter(range(5)), window_size=3):
        print(f"  窗口: {window}")


def demonstrate_pipeline():
    """演示数据处理管道"""
    print("\n=== 数据处理管道 ===")

    # 原始数据
    raw_data = [
        {"id": "001", "name": "Alice", "score": "92"},
        {"id": "002", "name": "Bob", "score": "78"},
        {"id": "003", "name": "Carol", "score": "88"},
        {"id": "004", "name": "David", "score": "55"},
    ]

    print("输入数据:")
    for record in raw_data:
        print(f"  {record}")

    # 管道：过滤 → 映射 → 过滤
    pipeline_steps = [
        filter_transformer(validate_record),  # 过滤无效记录
        map_transformer(parse_score),  # 解析分数
        filter_transformer(lambda r: r["score"] >= 60),  # 过滤不及格
        map_transformer(lambda r: {**r, "grade": compute_grade(r["score"])}),  # 添加等级
    ]

    result = list(generator_pipeline(iter(raw_data), *pipeline_steps))

    print("\n管道处理后 (score >= 60):")
    for record in result:
        print(f"  {record['name']}: {record['score']} → {record['grade']}")


# ============================================================
# 主函数
# ============================================================

def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 2: 生成器管道")
    print("=" * 60)

    demonstrate_basic_generators()
    demonstrate_yield_from()
    demonstrate_send()
    demonstrate_batch()
    demonstrate_pipeline()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
