"""P02 参考答案 1: 类型安全的数据处理管道"""

from typing import TypeVar, Protocol, Iterator, Generic

T = TypeVar("T")
U = TypeVar("U")


# ============================================================
# Protocol 定义
# ============================================================

class ItemProcessor(Protocol[T]):
    """数据处理器协议"""

    def process(self, item: T) -> T: ...


# ============================================================
# 具体处理器实现
# ============================================================

class UppercaseProcessor:
    """字符串转大写处理器"""

    def process(self, item: str) -> str:
        return item.upper()


class LengthFilter:
    """按长度过滤"""

    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def process(self, item: str) -> bool:
        return len(item) <= self.max_length


# ============================================================
# TypedPipeline 泛型类
# ============================================================

class TypedPipeline(Generic[T]):
    """类型安全的数据管道"""

    def __init__(self) -> None:
        self._processors: list = []

    def add_processor(self, processor: ItemProcessor) -> "TypedPipeline[T]":
        """添加处理器"""
        self._processors.append(processor)
        return self

    def process(self, items: Iterator[T]) -> Iterator[T]:
        """处理数据流"""
        for item in items:
            for processor in self._processors:
                if isinstance(processor, LengthFilter):
                    # LengthFilter 返回 bool，需要特殊处理
                    if not processor.process(item):
                        break
                else:
                    item = processor.process(item)
            else:
                # 只有当所有 LengthFilter 都通过时才 yield
                yield item
