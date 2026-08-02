"""
L23 测试套件：验证所有练习题答案

运行方式:
    pytest tests/test_l28_complete.py -v
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# 添加 solutions 到路径
lesson_dir = Path(__file__).parent.parent
solutions_path = lesson_dir / "solutions"
examples_path = lesson_dir / "examples"


def load_example_module(example_file: str):
    """加载 examples 模块的辅助函数"""
    module_name = f"example_{example_file}"
    spec = importlib.util.spec_from_file_location(module_name, examples_path / f"{example_file}.py")
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {example_file}")

    module = importlib.util.module_from_spec(spec)
    # 关键：注册到 sys.modules，解决 dataclass 的 __module__ 查找问题
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_solution_module(solution_file: str):
    """加载 solutions 模块的辅助函数"""
    module_name = f"sol_{solution_file}"
    spec = importlib.util.spec_from_file_location(module_name, solutions_path / f"{solution_file}.py")
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {solution_file}")

    module = importlib.util.module_from_spec(spec)
    # 关键：注册到 sys.modules
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# ============================================================================
# 测试练习 1: __slots__ 内存优化
# ============================================================================


def test_solution_01_point_with_slots() -> None:
    """测试 PointWithSlots 类"""
    sol = load_solution_module("solution_01_slots_memory")
    PointWithSlots = sol.PointWithSlots

    point = PointWithSlots(1.0, 2.0, 3.0)

    # 验证属性
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

    # 验证没有 __dict__
    assert not hasattr(point, "__dict__")

    # 验证不能添加新属性
    with pytest.raises(AttributeError):
        point.new_attr = "test"  # type: ignore


def test_solution_01_dataclass_slots() -> None:
    """测试 PointDataclass"""
    sol = load_solution_module("solution_01_slots_memory")
    PointDataclass = sol.PointDataclass

    point = PointDataclass(1.0, 2.0, 3.0)

    # 验证属性
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

    # 验证使用了 slots
    assert not hasattr(point, "__dict__")


def test_solution_01_generic_container() -> None:
    """测试 PEP 695 泛型容器"""
    sol = load_solution_module("solution_01_slots_memory")
    Container = sol.Container

    # 字符串容器
    str_container: Container[str] = Container()
    str_container.add("Hello")
    str_container.add("World")
    assert str_container.get_all() == ["Hello", "World"]
    assert len(str_container) == 2

    # 整数容器
    int_container: Container[int] = Container()
    int_container.add(1)
    int_container.add(2)
    int_container.add(3)
    assert int_container.get_all() == [1, 2, 3]
    assert len(int_container) == 3


def test_solution_01_memory_savings() -> None:
    """测试内存节省"""
    import sys

    sol = load_solution_module("solution_01_slots_memory")
    Point, PointWithSlots = sol.Point, sol.PointWithSlots

    # 创建 1000 个对象进行测试
    normal_points = [Point(i, i + 1, i + 2) for i in range(1000)]
    slotted_points = [PointWithSlots(i, i + 1, i + 2) for i in range(1000)]

    normal_size = sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in normal_points)
    slotted_size = sum(sys.getsizeof(p) for p in slotted_points)

    saving_ratio = (normal_size - slotted_size) / normal_size

    # 验证节省至少 20%
    assert saving_ratio >= 0.20, f"内存节省 {saving_ratio:.1%} < 20%"


# ============================================================================
# 测试练习 2: 装饰器性能优化
# ============================================================================


def test_solution_02_simple_cache() -> None:
    """测试简单缓存装饰器"""
    import time

    sol = load_solution_module("solution_02_decorator_performance")
    simple_cache = sol.simple_cache

    call_count = 0

    @simple_cache
    def expensive_func(n: int) -> int:
        nonlocal call_count
        call_count += 1
        time.sleep(0.01)
        return n * 2

    # 第一次调用
    result1 = expensive_func(5)
    assert result1 == 10
    assert call_count == 1

    # 第二次调用（应该命中缓存）
    result2 = expensive_func(5)
    assert result2 == 10
    assert call_count == 1  # 没有增加

    # 不同参数（应该重新计算）
    result3 = expensive_func(10)
    assert result3 == 20
    assert call_count == 2


def test_solution_02_ttl_cache() -> None:
    """测试 TTL 缓存装饰器"""
    import time

    sol = load_solution_module("solution_02_decorator_performance")
    ttl_cache = sol.ttl_cache

    @ttl_cache(ttl_seconds=0.5)
    def get_value() -> float:
        return time.time()

    # 第一次调用
    value1 = get_value()

    # 立即第二次调用（应该命中缓存）
    time.sleep(0.1)
    value2 = get_value()
    assert value1 == value2

    # 等待过期
    time.sleep(0.5)
    value3 = get_value()
    assert value3 > value1


def test_solution_02_cache_with_stats() -> None:
    """测试带统计的缓存"""
    sol = load_solution_module("solution_02_decorator_performance")
    cache_with_stats = sol.cache_with_stats

    def compute(n: int) -> int:
        return n * 2

    cached_func, stats = cache_with_stats(compute)

    # 5 次不同参数
    for i in range(5):
        cached_func(i)

    # 5 次重复参数
    for i in range(5):
        cached_func(i)

    assert stats.hits == 5
    assert stats.misses == 5
    assert stats.hit_rate == 0.5


# ============================================================================
# 测试 examples/01_meta_overhead.py
# ============================================================================


def test_example_01_classes_exist() -> None:
    """测试 example_01 中的类定义存在"""
    module = load_example_module("01_meta_overhead")

    # 验证类存在
    assert hasattr(module, "DynamicClass")
    assert hasattr(module, "SlottedClass")
    assert hasattr(module, "DataSlottedClass")

    # 测试动态类
    dynamic = module.DynamicClass(1, 2, 3)
    assert dynamic.x == 1
    assert hasattr(dynamic, "__dict__")

    # 测试 __slots__ 类
    slotted = module.SlottedClass(1, 2, 3)
    assert slotted.x == 1
    assert not hasattr(slotted, "__dict__")

    # 测试 dataclass(slots=True)
    data_slotted = module.DataSlottedClass(1, 2, 3)
    assert data_slotted.x == 1
    assert not hasattr(data_slotted, "__dict__")


def test_example_01_benchmark_functions() -> None:
    """测试 example_01 基准测试函数存在"""
    module = load_example_module("01_meta_overhead")

    # 验证基准测试函数存在且可调用
    assert hasattr(module, "benchmark_attribute_access")
    assert hasattr(module, "benchmark_attribute_write")
    assert hasattr(module, "benchmark_decorator_overhead")
    assert hasattr(module, "benchmark_descriptor_overhead")
    assert hasattr(module, "benchmark_object_creation")
    assert hasattr(module, "benchmark_gc_impact")

    assert callable(module.benchmark_attribute_access)
    assert callable(module.benchmark_gc_impact)


# ============================================================================
# 测试原 test_l28.py 中的核心测试
# ============================================================================


def test_slots_memory_saving() -> None:
    """测试 __slots__ 内存节省"""
    import sys

    module = load_example_module("01_meta_overhead")

    dynamic = module.DynamicClass(1, 2, 3)
    slotted = module.SlottedClass(1, 2, 3)

    dynamic_size = sys.getsizeof(dynamic) + sys.getsizeof(dynamic.__dict__)
    slotted_size = sys.getsizeof(slotted)

    assert slotted_size < dynamic_size, "__slots__ 应该节省内存"

    saving_ratio = (dynamic_size - slotted_size) / dynamic_size
    assert saving_ratio >= 0.20, f"内存节省 {saving_ratio:.1%} < 20%"


def test_slots_no_dynamic_attribute() -> None:
    """测试 __slots__ 类不能动态添加属性"""
    module = load_example_module("01_meta_overhead")

    obj = module.SlottedClass(1, 2, 3)

    with pytest.raises(AttributeError):
        obj.new_attr = "test"  # type: ignore


def test_dataclass_slots_equality() -> None:
    """测试 dataclass(slots=True) 相等性比较"""
    module = load_example_module("01_meta_overhead")

    obj1 = module.DataSlottedClass(1, 2, 3)
    obj2 = module.DataSlottedClass(1, 2, 3)
    obj3 = module.DataSlottedClass(4, 5, 6)

    # 验证相等性
    assert obj1 == obj2
    assert obj1 != obj3


# ============================================================================
# 集成测试
# ============================================================================


def test_integration_all_solutions() -> None:
    """集成测试：验证所有解答可以正常运行"""
    sol = load_solution_module("solution_01_slots_memory")
    Container = sol.Container
    PointDataclass = sol.PointDataclass
    PointWithSlots = sol.PointWithSlots
    sol = load_solution_module("solution_02_decorator_performance")
    cache_with_stats = sol.cache_with_stats
    simple_cache = sol.simple_cache
    ttl_cache = sol.ttl_cache

    # 验证所有类和函数都可以导入和使用
    assert PointWithSlots is not None
    assert PointDataclass is not None
    assert Container is not None
    assert simple_cache is not None
    assert ttl_cache is not None
    assert cache_with_stats is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
