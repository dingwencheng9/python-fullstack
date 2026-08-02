"""
练习 1: __slots__ 内存优化

任务：
为以下类添加 __slots__，并测量内存节省效果

要求：
1. 使用 __slots__ 优化内存
2. 使用 dataclass(slots=True) 优化内存
3. 测量实际内存节省比例
4. 使用 PEP 695 泛型语法创建通用容器类
5. 通过 mypy --strict 检查

Python 3.14 线程安全考量：
- sys.getsizeof() 是线程安全的（只读操作）
- 如果多个线程同时创建大量对象，需要考虑内存分配器的并发性能
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

# ============================================================================
# 原始版本（无优化）
# ============================================================================


class Point:
    """普通点类（无 __slots__）"""

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


# ============================================================================
# TODO: 学生需要实现的部分
# ============================================================================


class PointWithSlots:
    """
    使用 __slots__ 优化的点类

    TODO: 实现以下功能
    1. 添加 __slots__ = ('x', 'y', 'z')
    2. 实现 __init__ 方法
    3. 确保没有 __dict__ 属性
    """

    # TODO: 添加 __slots__

    def __init__(self, x: float, y: float, z: float) -> None:
        # TODO: 实现
        raise NotImplementedError("请实现 PointWithSlots.__init__")


@dataclass
class PointDataclass:
    """
    使用 @dataclass(slots=True) 优化的点类

    TODO: 添加 slots=True 参数
    """

    x: float
    y: float
    z: float


# ============================================================================
# TODO: PEP 695 泛型容器
# ============================================================================


class Container[T]:
    """
    通用容器类（PEP 695 泛型语法）

    TODO: 实现以下功能
    1. 使用 __slots__ = ('_items',)
    2. 实现 add(item: T) 方法
    3. 实现 get_all() -> list[T] 方法
    4. 使用 PEP 695 语法（类名后 [T]）

    Python 3.14 注意：
        如果多线程同时调用 add()，需要使用 threading.Lock 保护 _items
        当前实现假设单线程使用
    """

    # TODO: 添加 __slots__

    def __init__(self) -> None:
        # TODO: 实现
        raise NotImplementedError("请实现 Container.__init__")

    def add(self, item: T) -> None:
        """添加元素"""
        # TODO: 实现
        raise NotImplementedError("请实现 Container.add")

    def get_all(self) -> list[T]:
        """获取所有元素"""
        # TODO: 实现
        raise NotImplementedError("请实现 Container.get_all")


# ============================================================================
# 测试代码
# ============================================================================


def test_memory_savings() -> None:
    """测试内存节省"""
    print("创建 10000 个对象，测量内存占用:\n")

    # 普通类
    normal_points = [Point(i, i + 1, i + 2) for i in range(10000)]
    normal_size = sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in normal_points)

    print(f"普通类总内存: {normal_size:,} bytes")

    try:
        # __slots__ 类
        slotted_points = [PointWithSlots(i, i + 1, i + 2) for i in range(10000)]
        slotted_size = sum(sys.getsizeof(p) for p in slotted_points)

        print(f"__slots__ 类总内存: {slotted_size:,} bytes")

        # 计算节省比例
        saving_ratio = (normal_size - slotted_size) / normal_size
        print(f"\n内存节省: {saving_ratio:.1%}")

        if saving_ratio >= 0.30:
            print("✓ 内存节省 >= 30%，优化成功！")
        else:
            print("✗ 内存节省不足 30%")

    except NotImplementedError as e:
        print(f"✗ {e}")


def test_dataclass_slots() -> None:
    """测试 dataclass slots"""
    print("\n" + "=" * 60)
    print("测试 dataclass(slots=True)")
    print("=" * 60)

    try:
        point = PointDataclass(1.0, 2.0, 3.0)
        print(f"点坐标: ({point.x}, {point.y}, {point.z})")

        # 检查是否有 __dict__
        if hasattr(point, "__dict__"):
            print("✗ dataclass 应该使用 slots=True 参数")
        else:
            print("✓ dataclass 正确使用了 slots")

    except Exception as e:
        print(f"✗ 错误: {e}")


def test_generic_container() -> None:
    """测试泛型容器"""
    print("\n" + "=" * 60)
    print("测试 PEP 695 泛型容器")
    print("=" * 60)

    try:
        # 字符串容器
        str_container: Container[str] = Container()
        str_container.add("Hello")
        str_container.add("World")
        print(f"字符串容器: {str_container.get_all()}")

        # 整数容器
        int_container: Container[int] = Container()
        int_container.add(1)
        int_container.add(2)
        int_container.add(3)
        print(f"整数容器: {int_container.get_all()}")

        print("✓ 泛型容器测试通过")

    except NotImplementedError as e:
        print(f"✗ {e}")


if __name__ == "__main__":
    test_memory_savings()
    test_dataclass_slots()
    test_generic_container()
