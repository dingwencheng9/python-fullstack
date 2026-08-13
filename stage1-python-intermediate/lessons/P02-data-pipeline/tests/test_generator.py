"""test_generator.py - 生成器管道测试"""
# noqa: F401 - 未来可能需要 pytest.mark 用于参数化测试

from solutions.solution_02_generator_pipeline import (
    generator_pipeline,
    batch_generator,
    flatten,
    progress_tracker,
    transform_generator,
)


def test_batch_generator():
    """测试分批生成器"""
    items = range(10)
    batches = list(batch_generator(items, batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert len(batches) == 4


def test_batch_generator_exact():
    """测试精确分批"""
    items = range(6)
    batches = list(batch_generator(items, batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5]]


def test_flatten():
    """测试嵌套迭代器展平"""
    nested = [[1, 2], [3, 4], [5]]
    result = list(flatten(iter(nested)))
    assert result == [1, 2, 3, 4, 5]


def test_flatten_empty():
    """测试空嵌套"""
    nested = [[], [], []]
    result = list(flatten(iter(nested)))
    assert result == []


def test_progress_tracker():
    """测试进度追踪器"""
    tracker = progress_tracker(100)
    next(tracker)  # 初始化

    assert tracker.send(10) == 10
    assert tracker.send(20) == 30
    assert tracker.send(5) == 35


def test_progress_tracker_default():
    """测试进度追踪器默认值"""
    tracker = progress_tracker(10)
    next(tracker)  # 初始化

    assert tracker.send(None) == 1  # 默认增量 1
    assert tracker.send(None) == 2


def test_generator_pipeline():
    """测试生成器管道组合"""
    def double(items):
        for x in items:
            yield x * 2

    def filter_even(items):
        for x in items:
            if x % 4 == 0:
                yield x

    source = iter([1, 2, 3, 4, 5])
    result = list(generator_pipeline(source, double, filter_even))
    assert result == [4, 8]


def test_transform_generator():
    """测试变换生成器"""
    data = [1, 2, 3]
    result = list(transform_generator(
        iter(data),
        lambda x: x * 2,
        lambda x: x + 1,
    ))
    assert result == [3, 5, 7]
