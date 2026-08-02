"""
L23 示例 01: 元编程抽象开销分析

展示不同抽象层次的性能开销，并提供精确的基准测试。

主题:
1. 动态属性 vs __slots__
2. 装饰器开销
3. 描述符协议开销
4. 属性访问模式对比
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

import functools
import gc
import sys
import timeit
from dataclasses import dataclass
from typing import Any

# ============================================================================
# 第一部分: 动态属性 vs __slots__ 对比
# ============================================================================


class DynamicClass:
    """动态属性类 - 使用 __dict__ 存储"""

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


class SlottedClass:
    """优化类 - 使用 __slots__ 避免 __dict__"""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


@dataclass(slots=True)
class DataSlottedClass:
    """使用 dataclass 的 __slots__ 版本"""

    x: int
    y: int
    z: int


def benchmark_attribute_access() -> None:
    """基准测试: 属性访问性能"""

    print("\n" + "=" * 80)
    print("基准测试 1: 属性访问性能")
    print("=" * 80)

    iterations = 1_000_000

    # 测试动态属性
    dynamic_setup = """
class DynamicClass:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

obj = DynamicClass(1, 2, 3)
"""

    dynamic_time = timeit.timeit("obj.x; obj.y; obj.z", setup=dynamic_setup, number=iterations)

    # 测试 __slots__
    slotted_setup = """
class SlottedClass:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

obj = SlottedClass(1, 2, 3)
"""

    slotted_time = timeit.timeit("obj.x; obj.y; obj.z", setup=slotted_setup, number=iterations)

    # 测试 dataclass with slots
    data_slotted_setup = """
from dataclasses import dataclass

@dataclass(slots=True)
class DataSlottedClass:
    x: int
    y: int
    z: int

obj = DataSlottedClass(1, 2, 3)
"""

    data_slotted_time = timeit.timeit("obj.x; obj.y; obj.z", setup=data_slotted_setup, number=iterations)

    print(f"\n{'类型':<25} {'时间 (秒)':<15} {'相对性能':<15}")
    print("-" * 55)
    print(f"{'动态属性 (__dict__)':<25} {dynamic_time:<15.4f} {'1.00x':<15}")
    print(f"{'__slots__':<25} {slotted_time:<15.4f} {dynamic_time / slotted_time:<15.2f}x")
    print(f"{'dataclass(slots=True)':<25} {data_slotted_time:<15.4f} {dynamic_time / data_slotted_time:<15.2f}x")

    print(f"\n✅ __slots__ 比动态属性快 {dynamic_time / slotted_time:.2f}x")


def benchmark_attribute_write() -> None:
    """基准测试: 属性写入性能"""

    print("\n" + "=" * 80)
    print("基准测试 2: 属性写入性能")
    print("=" * 80)

    iterations = 1_000_000

    # 测试动态属性写入
    dynamic_write_time = timeit.timeit(
        "obj.x = 10; obj.y = 20; obj.z = 30",
        setup="class C:\n    pass\nobj = C()\nobj.x = obj.y = obj.z = 0",
        number=iterations,
    )

    # 测试 __slots__ 写入
    slotted_write_time = timeit.timeit(
        "obj.x = 10; obj.y = 20; obj.z = 30",
        setup="class C:\n    __slots__ = ('x', 'y', 'z')\nobj = C()\nobj.x = obj.y = obj.z = 0",
        number=iterations,
    )

    print(f"\n{'类型':<25} {'时间 (秒)':<15} {'相对性能':<15}")
    print("-" * 55)
    print(f"{'动态属性写入':<25} {dynamic_write_time:<15.4f} {'1.00x':<15}")
    print(f"{'__slots__ 写入':<25} {slotted_write_time:<15.4f} {dynamic_write_time / slotted_write_time:<15.2f}x")


# ============================================================================
# 第二部分: 装饰器开销
# ============================================================================


def simple_decorator[T](func: Callable[..., T]) -> Callable[..., T]:
    """简单装饰器 - 有开销"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # 每次调用都有额外开销
        return func(*args, **kwargs)

    return wrapper


def expensive_decorator[T](func: Callable[..., T]) -> Callable[..., T]:
    """昂贵装饰器 - 包含检查和日志"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # 参数检查
        if not args:
            raise ValueError("需要参数")

        # 执行函数
        result = func(*args, **kwargs)

        # 结果验证
        if result is None:
            raise ValueError("结果不能为 None")

        return result

    return wrapper


def benchmark_decorator_overhead() -> None:
    """基准测试: 装饰器开销"""

    print("\n" + "=" * 80)
    print("基准测试 3: 装饰器开销")
    print("=" * 80)

    iterations = 1_000_000

    # 无装饰器
    no_decorator_time = timeit.timeit(
        "func(42)",
        setup="def func(x: int) -> int: return x * 2",
        number=iterations,
    )

    # 简单装饰器
    simple_decorator_time = timeit.timeit(
        "func(42)",
        setup="""
import functools

def simple_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def func(x: int) -> int:
    return x * 2
""",
        number=iterations,
    )

    # 昂贵装饰器
    expensive_decorator_time = timeit.timeit(
        "func(42)",
        setup="""
import functools

def expensive_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            raise ValueError("需要参数")
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError("结果不能为 None")
        return result
    return wrapper

@expensive_decorator
def func(x: int) -> int:
    return x * 2
""",
        number=iterations,
    )

    print(f"\n{'类型':<25} {'时间 (秒)':<15} {'开销':<15}")
    print("-" * 55)
    print(f"{'无装饰器':<25} {no_decorator_time:<15.4f} {'基准':<15}")
    print(f"{'简单装饰器':<25} {simple_decorator_time:<15.4f} {'+' + f'{((simple_decorator_time / no_decorator_time - 1) * 100):.1f}%':<15}")
    print(f"{'昂贵装饰器':<25} {expensive_decorator_time:<15.4f} {'+' + f'{((expensive_decorator_time / no_decorator_time - 1) * 100):.1f}%':<15}")

    print(f"\n⚠️  简单装饰器增加 {((simple_decorator_time / no_decorator_time - 1) * 100):.1f}% 开销")
    print(f"⚠️  昂贵装饰器增加 {((expensive_decorator_time / no_decorator_time - 1) * 100):.1f}% 开销")


# ============================================================================
# 第三部分: 描述符协议开销
# ============================================================================


class SimpleDescriptor:
    """简单描述符"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, obj: Any, objtype: type[Any] | None = None) -> int:
        if obj is None:
            return self  # type: ignore[return-value]
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj: Any, value: int) -> None:
        obj.__dict__[self.name] = value


class PropertyClass:
    """使用 property 的类"""

    def __init__(self) -> None:
        self._x = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value


class DescriptorClass:
    """使用描述符的类"""

    x = SimpleDescriptor("_x")

    def __init__(self) -> None:
        self._x = 0


class DirectClass:
    """直接属性访问"""

    def __init__(self) -> None:
        self.x = 0


def benchmark_descriptor_overhead() -> None:
    """基准测试: 描述符开销"""

    print("\n" + "=" * 80)
    print("基准测试 4: 描述符协议开销")
    print("=" * 80)

    iterations = 1_000_000

    # 直接属性访问
    direct_time = timeit.timeit(
        "obj.x = 42; _ = obj.x",
        setup="class C:\n    def __init__(self): self.x = 0\nobj = C()",
        number=iterations,
    )

    # property 访问
    property_time = timeit.timeit(
        "obj.x = 42; _ = obj.x",
        setup="""
class C:
    def __init__(self):
        self._x = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

obj = C()
""",
        number=iterations,
    )

    # 描述符访问
    descriptor_time = timeit.timeit(
        "obj.x = 42; _ = obj.x",
        setup="""
class SimpleDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

class C:
    x = SimpleDescriptor('_x')

    def __init__(self):
        self._x = 0

obj = C()
""",
        number=iterations,
    )

    print(f"\n{'类型':<25} {'时间 (秒)':<15} {'相对性能':<15}")
    print("-" * 55)
    print(f"{'直接属性':<25} {direct_time:<15.4f} {'1.00x':<15}")
    print(f"{'@property':<25} {property_time:<15.4f} {property_time / direct_time:<15.2f}x")
    print(f"{'描述符':<25} {descriptor_time:<15.4f} {descriptor_time / direct_time:<15.2f}x")

    print(f"\n⚠️  @property 比直接属性慢 {property_time / direct_time:.2f}x")
    print(f"⚠️  描述符比直接属性慢 {descriptor_time / direct_time:.2f}x")


# ============================================================================
# 第四部分: 对象创建开销
# ============================================================================


def benchmark_object_creation() -> None:
    """基准测试: 对象创建性能"""

    print("\n" + "=" * 80)
    print("基准测试 5: 对象创建性能")
    print("=" * 80)

    iterations = 100_000

    # 动态类
    dynamic_creation_time = timeit.timeit(
        "C(1, 2, 3)",
        setup="""
class C:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
""",
        number=iterations,
    )

    # __slots__ 类
    slotted_creation_time = timeit.timeit(
        "C(1, 2, 3)",
        setup="""
class C:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
""",
        number=iterations,
    )

    # dataclass
    dataclass_creation_time = timeit.timeit(
        "C(1, 2, 3)",
        setup="""
from dataclasses import dataclass

@dataclass
class C:
    x: int
    y: int
    z: int
""",
        number=iterations,
    )

    # dataclass with slots
    dataclass_slotted_creation_time = timeit.timeit(
        "C(1, 2, 3)",
        setup="""
from dataclasses import dataclass

@dataclass(slots=True)
class C:
    x: int
    y: int
    z: int
""",
        number=iterations,
    )

    print(f"\n{'类型':<30} {'时间 (秒)':<15} {'相对性能':<15}")
    print("-" * 60)
    print(f"{'动态类':<30} {dynamic_creation_time:<15.4f} {'1.00x':<15}")
    print(f"{'__slots__ 类':<30} {slotted_creation_time:<15.4f} {dynamic_creation_time / slotted_creation_time:<15.2f}x")
    print(f"{'dataclass':<30} {dataclass_creation_time:<15.4f} {dynamic_creation_time / dataclass_creation_time:<15.2f}x")
    print(f"{'dataclass(slots=True)':<30} {dataclass_slotted_creation_time:<15.4f} {dynamic_creation_time / dataclass_slotted_creation_time:<15.2f}x")


# ============================================================================
# 第五部分: GC 影响测试
# ============================================================================


def benchmark_gc_impact() -> None:
    """基准测试: GC 对性能的影响"""

    print("\n" + "=" * 80)
    print("基准测试 6: GC 影响")
    print("=" * 80)

    def create_objects(n: int) -> list[DynamicClass]:
        """创建大量对象"""
        return [DynamicClass(i, i, i) for i in range(n)]

    n = 100_000

    # 启用 GC
    gc.enable()
    gc_enabled_time = timeit.timeit(lambda: create_objects(n), number=10)

    # 禁用 GC
    gc.disable()
    gc_disabled_time = timeit.timeit(lambda: create_objects(n), number=10)
    gc.enable()  # 恢复

    print(f"\n{'模式':<20} {'时间 (秒)':<15} {'相对性能':<15}")
    print("-" * 50)
    print(f"{'GC 启用':<20} {gc_enabled_time:<15.4f} {'1.00x':<15}")
    print(f"{'GC 禁用':<20} {gc_disabled_time:<15.4f} {gc_enabled_time / gc_disabled_time:<15.2f}x")

    print(f"\n✅ 禁用 GC 可提升 {((gc_enabled_time / gc_disabled_time - 1) * 100):.1f}% 性能")
    print("⚠️  注意: 禁用 GC 后需要手动管理内存")


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """运行所有基准测试"""

    print("\n" + "=" * 80)
    print("L23 示例 01: 元编程抽象开销分析")
    print("=" * 80)
    print("\n本示例展示不同抽象层次的性能开销")
    print("运行环境:")
    print(f"  Python 版本: {sys.version.split()[0]}")
    print(f"  GC 状态: {'启用' if gc.isenabled() else '禁用'}")
    print(f"  GC 阈值: {gc.get_threshold()}")

    # 运行所有基准测试
    benchmark_attribute_access()
    benchmark_attribute_write()
    benchmark_decorator_overhead()
    benchmark_descriptor_overhead()
    benchmark_object_creation()
    benchmark_gc_impact()

    # 总结
    print("\n" + "=" * 80)
    print("性能优化建议")
    print("=" * 80)
    print("\n1. 属性访问:")
    print("   ✅ 使用 __slots__ 可提升 20-50% 性能")
    print("   ✅ 避免不必要的 property 和描述符")
    print("\n2. 装饰器:")
    print("   ⚠️  简单装饰器增加 ~30% 开销")
    print("   ⚠️  复杂装饰器增加 ~100% 开销")
    print("   ✅ 性能关键路径避免装饰器")
    print("\n3. 对象创建:")
    print("   ✅ __slots__ 类创建速度更快")
    print("   ✅ dataclass(slots=True) 兼顾性能和可读性")
    print("\n4. GC 管理:")
    print("   ✅ 性能关键段可临时禁用 GC")
    print("   ✅ 完成后手动触发 gc.collect()")
    print()


if __name__ == "__main__":
    main()
