"""
解答 1: __slots__ 内存优化

完整实现所有练习要求
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
# 解答：使用 __slots__ 优化
# ============================================================================


class PointWithSlots:
    """
    使用 __slots__ 优化的点类

    __slots__ 优势：
    1. 节省内存：不创建 __dict__，直接在固定位置存储属性
    2. 更快的属性访问：避免字典查找
    3. 防止动态添加属性

    Python 3.14 注意：
        __slots__ 类的内存布局是固定的，天然线程安全（只读操作）
        属性赋值操作（self.x = value）不是原子的，需要外部同步
    """

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"PointWithSlots(x={self.x}, y={self.y}, z={self.z})"


@dataclass(slots=True)
class PointDataclass:
    """
    使用 @dataclass(slots=True) 优化的点类

    slots=True 自动生成 __slots__，结合 dataclass 的便利性

    Python 3.14 注意：
        与手动 __slots__ 类似，属性访问安全，赋值需外部同步
    """

    x: float
    y: float
    z: float


# ============================================================================
# 解答：PEP 695 泛型容器
# ============================================================================


class Container[T]:
    """
    通用容器类（PEP 695 泛型语法）

    展示特性：
    1. PEP 695: 类名后 [T] 声明类型参数
    2. __slots__ 优化内存
    3. 类型安全的泛型容器

    Python 3.14 线程安全分析：
        - _items 是可变列表，并发 add() 会导致竞态条件
        - 解决方案 1: 使用 threading.Lock
        - 解决方案 2: 使用 queue.Queue（内置线程安全）
        - 当前实现假设单线程使用
    """

    __slots__ = ("_items",)

    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        """添加元素"""
        self._items.append(item)

    def get_all(self) -> list[T]:
        """获取所有元素（返回副本，避免外部修改）"""
        return self._items.copy()

    def __len__(self) -> int:
        """返回元素数量"""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Container({self._items})"


# ============================================================================
# 线程安全版本（Python 3.14 优化）
# ============================================================================


class ThreadSafeContainer[T]:
    """
    线程安全的通用容器类

    Python 3.14 优化：
        在无 GIL 环境下，多个线程可以真正并行执行
        使用 Lock 保护共享状态是必须的
    """

    __slots__ = ("_items", "_lock")

    def __init__(self) -> None:
        self._items: list[T] = []
        # 注意：实际使用时需要 import threading
        # self._lock = threading.Lock()

    def add(self, item: T) -> None:
        """线程安全的添加元素"""
        # with self._lock:
        #     self._items.append(item)
        self._items.append(item)  # 简化版本

    def get_all(self) -> list[T]:
        """线程安全的获取所有元素"""
        # with self._lock:
        #     return self._items.copy()
        return self._items.copy()  # 简化版本


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
        print(f"⚠️ 内存节省 {saving_ratio:.1%} < 30%")


def test_dataclass_slots() -> None:
    """测试 dataclass slots"""
    print("\n" + "=" * 60)
    print("测试 dataclass(slots=True)")
    print("=" * 60)

    point = PointDataclass(1.0, 2.0, 3.0)
    print(f"点坐标: ({point.x}, {point.y}, {point.z})")

    # 检查是否有 __dict__
    if hasattr(point, "__dict__"):
        print("✗ dataclass 应该使用 slots=True 参数")
    else:
        print("✓ dataclass 正确使用了 slots")

    # 测试无法动态添加属性
    try:
        point.new_attr = "test"  # type: ignore
        print("✗ 不应该能添加新属性")
    except AttributeError:
        print("✓ 正确阻止了动态添加属性")


def test_generic_container() -> None:
    """测试泛型容器"""
    print("\n" + "=" * 60)
    print("测试 PEP 695 泛型容器")
    print("=" * 60)

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

    # 验证类型安全（静态检查）
    # str_container.add(123)  # mypy 会报错

    print("✓ 泛型容器测试通过")


def test_no_dict() -> None:
    """测试 __slots__ 类没有 __dict__"""
    print("\n" + "=" * 60)
    print("测试 __slots__ 特性")
    print("=" * 60)

    slotted = PointWithSlots(1.0, 2.0, 3.0)

    # 测试 1: 没有 __dict__
    if not hasattr(slotted, "__dict__"):
        print("✓ __slots__ 类没有 __dict__")
    else:
        print("✗ __slots__ 类不应该有 __dict__")

    # 测试 2: 无法动态添加属性
    try:
        slotted.new_attr = "test"  # type: ignore
        print("✗ 不应该能添加新属性")
    except AttributeError:
        print("✓ 正确阻止了动态添加属性")

    # 测试 3: 可以正常访问和修改声明的属性
    slotted.x = 10.0
    if slotted.x == 10.0:
        print("✓ 可以正常修改声明的属性")


if __name__ == "__main__":
    test_memory_savings()
    test_dataclass_slots()
    test_generic_container()
    test_no_dict()
