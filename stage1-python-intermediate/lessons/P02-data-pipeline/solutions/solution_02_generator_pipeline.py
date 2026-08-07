"""P02 参考答案 2: 生成器数据处理管道"""

from typing import Iterator, Callable, Generator, TypeVar

T = TypeVar("T")


def generator_pipeline(
    source: Iterator[T],
    *transformers: Callable[[Iterator[T]], Iterator[T]]
) -> Iterator[T]:
    """组合多个转换生成器"""
    result: Iterator[T] = source
    for transformer in transformers:
        result = transformer(result)
    yield from result


def batch_generator(items: Iterator[T], batch_size: int) -> Generator[list[T], None, None]:
    """分批 yield 数据"""
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def flatten(nested_iterators: Iterator[Iterator[T]]) -> Iterator[T]:
    """展平嵌套迭代器"""
    for nested in nested_iterators:
        yield from nested


def progress_tracker(total: int) -> Generator[int, int | None, int]:
    """进度追踪生成器"""
    progress = 0
    while progress < total:
        increment = yield progress
        if increment is None:
            increment = 1
        progress += increment
    return progress


def transform_generator(
    items: Iterator[T],
    *transforms: Callable[[T], T]
) -> Iterator[T]:
    """应用多个转换函数到每个元素"""
    for item in items:
        result = item
        for transform in transforms:
            result = transform(result)
        yield result
