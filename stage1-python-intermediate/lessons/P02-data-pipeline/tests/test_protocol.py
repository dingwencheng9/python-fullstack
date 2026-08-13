"""test_protocol.py - Protocol + TypeVar 类型测试"""
# noqa: F401 - 未来可能需要 pytest.mark 用于参数化测试

from solutions.solution_01_typed_pipeline import (
    ItemProcessor,
    UppercaseProcessor,
    LengthFilter,
    TypedPipeline,
)


def test_item_processor_protocol():
    """验证 Protocol 定义正确"""
    proc: ItemProcessor[str] = UppercaseProcessor()
    assert callable(proc.process)


def test_uppercase_processor():
    """测试大写处理器"""
    processor = UppercaseProcessor()
    assert processor.process("hello") == "HELLO"
    assert processor.process("World") == "WORLD"
    assert processor.process("") == ""


def test_length_filter():
    """测试长度过滤器"""
    filter_ = LengthFilter(max_length=5)
    assert filter_.process("hi") is True
    assert filter_.process("hello") is True
    assert filter_.process("hello world") is False
    assert filter_.process("") is True


def test_typed_pipeline():
    """测试泛型管道"""
    from solutions.solution_01_typed_pipeline import UppercaseProcessor, TypedPipeline

    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    result = list(pipeline.process(iter(["hello", "world"])))
    assert result == ["HELLO", "WORLD"]


def test_pipeline_chain():
    """测试管道链式调用"""
    pipeline = TypedPipeline[str]()
    pipeline.add_processor(UppercaseProcessor())
    pipeline.add_processor(LengthFilter(max_length=10))
    result = list(pipeline.process(iter(["hello", "world", "THIS IS VERY LONG TEXT"])))
    assert result == ["HELLO", "WORLD"]


def test_pipeline_return_type():
    """测试管道返回类型"""
    pipeline = TypedPipeline[int]()
    pipeline.add_processor(UppercaseProcessor())  # 这个只处理 str，应该报错或跳过
    # TypedPipeline 应该在类型层面阻止这种情况
