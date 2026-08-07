"""P02 示例 1: Protocol + TypeVar 类型系统

演示 L10 类型系统的核心概念：
- Protocol 定义接口协议
- TypeVar 实现泛型
- 泛型约束

运行方式:
    python examples/01_protocol_types.py
"""

from typing import TypeVar, Protocol, Iterator, runtime_checkable

# ============================================================
# 1. TypeVar 定义
# ============================================================

T = TypeVar("T")  # 泛型变量
U = TypeVar("U")  # 另一个泛型变量


# ============================================================
# 2. Protocol 接口定义
# ============================================================

@runtime_checkable
class DataSource(Protocol[T]):
    """数据源协议 - 定义数据读取接口"""

    def read(self) -> Iterator[T]: ...


@runtime_checkable
class DataSink(Protocol[T]):
    """数据汇协议 - 定义数据写入接口"""

    def write(self, item: T) -> None: ...


class PipelineStage(Protocol[T, U]):
    """管道阶段协议 - 定义数据转换接口"""

    def process(self, items: Iterator[T]) -> Iterator[U]: ...


# ============================================================
# 3. 具体实现
# ============================================================

class ListSource:
    """列表数据源实现"""

    def __init__(self, data: list[T]) -> None:
        self._data = data

    def read(self) -> Iterator[T]:
        """生成器方式迭代"""
        yield from self._data


class DictSource:
    """字典数据源实现"""

    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def read(self) -> Iterator[dict]:
        """从文件读取字典"""
        import json
        with open(self._filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        yield from data


class ConsoleSink:
    """控制台数据汇实现"""

    def write(self, item: T) -> None:
        """输出到控制台"""
        print(f"  → {item}")


# ============================================================
# 4. 泛型管道类
# ============================================================

class TypedPipeline:
    """类型安全的数据处理管道"""

    def __init__(self) -> None:
        self._processors: list[callable] = []

    def add_processor(self, processor: PipelineStage[T, U]) -> "TypedPipeline":
        """添加处理器"""
        self._processors.append(processor)
        return self

    def process(self, source: DataSource[T]) -> Iterator[T]:
        """处理数据流"""
        items = source.read()
        for processor in self._processors:
            items = processor.process(items)
        yield from items


# ============================================================
# 5. 具体处理器实现
# ============================================================

class UppercaseProcessor:
    """字符串转大写处理器"""

    def process(self, items: Iterator[str]) -> Iterator[str]:
        for item in items:
            yield item.upper()


class LengthFilter:
    """按长度过滤"""

    def __init__(self, min_length: int = 0, max_length: int = 100) -> None:
        self._min = min_length
        self._max = max_length

    def process(self, items: Iterator[str]) -> Iterator[str]:
        for item in items:
            if self._min <= len(item) <= self._max:
                yield item


class MapProcessor:
    """映射转换处理器"""

    def __init__(self, func: callable) -> None:
        self._func = func

    def process(self, items: Iterator) -> Iterator:
        yield from map(self._func, items)


# ============================================================
# 6. Protocol 运行时检查
# ============================================================

def demonstrate_protocol():
    """演示 Protocol 运行时检查"""
    print("\n=== Protocol 运行时检查 ===")

    # 符合协议的对象
    source = ListSource([1, 2, 3])
    print(f"ListSource 是 DataSource: {isinstance(source, DataSource)}")

    # 字典对象
    d = {"a": 1}
    print(f"dict 是 DataSource: {isinstance(d, DataSource)}")

    # 列表对象
    lst = [1, 2, 3]
    print(f"list 是 DataSource: {isinstance(lst, DataSource)}")


# ============================================================
# 7. 泛型管道演示
# ============================================================

def demonstrate_pipeline():
    """演示泛型管道"""
    print("\n=== 泛型管道演示 ===")

    # 创建数据源
    source = ListSource(["hello", "world", "python", "data"])

    # 创建管道
    pipeline = TypedPipeline()
    pipeline.add_processor(UppercaseProcessor())
    pipeline.add_processor(LengthFilter(min_length=4, max_length=10))

    # 处理数据
    print("输入: ['hello', 'world', 'python', 'data']")
    print("管道: Uppercase → LengthFilter(4-10)")
    print("输出:")
    for item in pipeline.process(source):
        print(f"  {item}")


# ============================================================
# 8. 映射转换演示
# ============================================================

def demonstrate_map_processor():
    """演示映射转换"""
    print("\n=== 映射转换演示 ===")

    source = ListSource([1, 2, 3, 4, 5])
    pipeline = TypedPipeline()
    pipeline.add_processor(MapProcessor(lambda x: x * 2))
    pipeline.add_processor(MapProcessor(lambda x: f"值: {x}"))

    print("输入: [1, 2, 3, 4, 5]")
    print("管道: x → x*2 → f'值: {x}'")
    print("输出:")
    for item in pipeline.process(source):
        print(f"  {item}")


# ============================================================
# 主函数
# ============================================================

def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 1: Protocol + TypeVar 类型系统")
    print("=" * 60)

    demonstrate_protocol()
    demonstrate_pipeline()
    demonstrate_map_processor()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
