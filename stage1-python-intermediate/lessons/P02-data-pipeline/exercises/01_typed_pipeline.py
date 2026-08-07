"""P02 练习 1: 类型安全的数据处理管道

课程编号: P02
所属课程: Stage 1 - Python 进阶
练习编号: 01
难度: ⭐⭐⭐⭐
知识点: Protocol + TypeVar + 泛型

任务：
1. 定义 ItemProcessor Protocol，支持 process(item) 方法
2. 实现 UppercaseProcessor：将字符串字段转为大写
3. 实现 LengthFilter：过滤超过指定长度的字段
4. 实现 TypedPipeline[T] 泛型类，支持链式调用

运行方式:
    python exercises/01_typed_pipeline.py

预期输出：
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    result = list(pipeline.process(["hello", "world"]))
    assert result == ["HELLO", "WORLD"]
"""

from typing import TypeVar, Protocol, Iterator

T = TypeVar("T")
U = TypeVar("U")


# ============================================================
# 1. Protocol 定义
# ============================================================

# TODO: 定义 ItemProcessor Protocol
# 提示: 使用 Protocol[T] 定义一个 process(self, item: T) -> T 的接口
class ItemProcessor(Protocol[T]):
    """数据处理器协议

    提示: 实现 process(self, item: T) -> T 方法
    """
    ...


# ============================================================
# 2. 具体处理器实现
# ============================================================

# TODO: 实现 UppercaseProcessor
class UppercaseProcessor:
    """字符串转大写处理器

    预期行为:
        processor = UppercaseProcessor()
        assert processor.process("hello") == "HELLO"
        assert processor.process("World") == "WORLD"
    """
    def process(self, item: str) -> str:
        # TODO: 实现转换逻辑
        pass


# TODO: 实现 LengthFilter
class LengthFilter:
    """按长度过滤

    预期行为:
        filter_ = LengthFilter(max_length=5)
        assert filter_.process("hi") is True
        assert filter_.process("hello world") is False
    """
    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def process(self, item: str) -> bool:
        # TODO: 实现长度检查逻辑
        pass


# ============================================================
# 3. TypedPipeline 泛型类
# ============================================================

# TODO: 实现 TypedPipeline 泛型类
class TypedPipeline:
    """类型安全的数据管道

    预期行为:
        pipeline = TypedPipeline[str]()
        pipeline.add_processor(UppercaseProcessor())
        result = list(pipeline.process(["hello", "world"]))
        assert result == ["HELLO", "WORLD"]
    """
    def __init__(self) -> None:
        # TODO: 初始化处理器列表
        pass

    def add_processor(self, processor: ItemProcessor[T]) -> "TypedPipeline[T]":
        """添加处理器"""
        # TODO: 添加处理器到列表并返回 self（支持链式调用）
        pass

    def process(self, items: Iterator[T]) -> Iterator[T]:
        """处理数据流"""
        # TODO: 依次应用所有处理器
        pass


# ============================================================
# 测试
# ============================================================

def test_uppercase_processor():
    """测试大写处理器"""
    processor = UppercaseProcessor()
    assert processor.process("hello") == "HELLO"
    assert processor.process("World") == "WORLD"
    assert processor.process("") == ""
    print("✓ UppercaseProcessor 测试通过")


def test_length_filter():
    """测试长度过滤器"""
    filter_ = LengthFilter(max_length=5)
    assert filter_.process("hi") is True
    assert filter_.process("hello") is True
    assert filter_.process("hello world") is False
    assert filter_.process("") is True
    print("✓ LengthFilter 测试通过")


def test_typed_pipeline():
    """测试泛型管道"""
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    result = list(pipeline.process(iter(["hello", "world"])))
    assert result == ["HELLO", "WORLD"]
    print("✓ TypedPipeline 基本测试通过")


def test_pipeline_chain():
    """测试管道链式调用"""
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    pipeline.add_processor(LengthFilter(max_length=10))
    result = list(pipeline.process(iter(["hello", "world", "THIS IS VERY LONG TEXT"])))
    assert result == ["HELLO", "WORLD"]
    print("✓ TypedPipeline 链式测试通过")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("P02 练习 1: 类型安全管道")
    print("=" * 50)

    try:
        test_uppercase_processor()
        test_length_filter()
        test_typed_pipeline()
        test_pipeline_chain()
        print("\n🎉 所有测试通过!")
    except (AssertionError, NotImplementedError) as e:
        print(f"\n❌ 测试失败: {e}")
        print("请实现 TODO 部分")


if __name__ == "__main__":
    main()
