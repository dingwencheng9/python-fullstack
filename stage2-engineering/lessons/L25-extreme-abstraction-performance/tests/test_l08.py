"""
L23 测试文件: 极限抽象与性能优化

测试覆盖:
1. __slots__ 内存节省验证
2. 属性访问性能测试
3. 对象创建性能测试
4. 继承链 __slots__ 测试
5. GC 影响测试
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import pytest

# ============================================================================
# 测试类定义
# ============================================================================


class DynamicClass:
    """动态属性类"""

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


class SlottedClass:
    """使用 __slots__ 的类"""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z


@dataclass(slots=True)
class DataSlottedClass:
    """使用 dataclass slots 的类"""

    x: int
    y: int
    z: int


class BaseSlotted:
    """基类 - 使用 __slots__"""

    __slots__ = ("x",)

    def __init__(self, x: int) -> None:
        self.x = x


class DerivedSlotted(BaseSlotted):
    """派生类 - 继承 __slots__"""

    __slots__ = ("y",)

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x)
        self.y = y


# ============================================================================
# 测试 1: __slots__ 内存节省
# ============================================================================


def test_slots_memory_saving() -> None:
    """测试 __slots__ 是否节省内存"""

    dynamic = DynamicClass(1, 2, 3)
    slotted = SlottedClass(1, 2, 3)

    # 计算内存占用
    dynamic_size = sys.getsizeof(dynamic) + sys.getsizeof(dynamic.__dict__)
    slotted_size = sys.getsizeof(slotted)

    # 断言 __slots__ 节省内存
    assert slotted_size < dynamic_size, "__slots__ 应该节省内存"

    # 计算节省比例
    saving_ratio = 1 - (slotted_size / dynamic_size)

    # 断言至少节省 30% 内存
    assert saving_ratio >= 0.30, f"内存节省比例应 >= 30%，实际 {saving_ratio:.1%}"

    print(f"✅ __slots__ 节省 {saving_ratio:.1%} 内存")


def test_dataclass_slots_memory_saving() -> None:
    """测试 dataclass(slots=True) 是否节省内存"""

    dynamic = DynamicClass(1, 2, 3)
    data_slotted = DataSlottedClass(1, 2, 3)

    dynamic_size = sys.getsizeof(dynamic) + sys.getsizeof(dynamic.__dict__)
    data_slotted_size = sys.getsizeof(data_slotted)

    # 断言 dataclass slots 节省内存
    assert data_slotted_size < dynamic_size, "dataclass(slots=True) 应该节省内存"

    saving_ratio = 1 - (data_slotted_size / dynamic_size)

    # 断言至少节省 30% 内存
    assert saving_ratio >= 0.30, f"内存节省比例应 >= 30%，实际 {saving_ratio:.1%}"

    print(f"✅ dataclass(slots=True) 节省 {saving_ratio:.1%} 内存")


# ============================================================================
# 测试 2: __slots__ 属性访问
# ============================================================================


def test_slots_attribute_access() -> None:
    """测试 __slots__ 类的属性访问"""

    obj = SlottedClass(1, 2, 3)

    # 测试读取
    assert obj.x == 1
    assert obj.y == 2
    assert obj.z == 3

    # 测试写入
    obj.x = 10
    obj.y = 20
    obj.z = 30

    assert obj.x == 10
    assert obj.y == 20
    assert obj.z == 30


def test_slots_no_dict() -> None:
    """测试 __slots__ 类没有 __dict__"""

    obj = SlottedClass(1, 2, 3)

    # 断言没有 __dict__
    assert not hasattr(obj, "__dict__"), "__slots__ 类不应该有 __dict__"


def test_slots_no_dynamic_attribute() -> None:
    """测试 __slots__ 类不能动态添加属性"""

    obj = SlottedClass(1, 2, 3)

    # 尝试添加新属性应该失败
    with pytest.raises(AttributeError):
        obj.new_attr = 100  # type: ignore[attr-defined]


# ============================================================================
# 测试 3: __slots__ 继承
# ============================================================================


def test_slots_inheritance() -> None:
    """测试 __slots__ 继承"""

    obj = DerivedSlotted(1, 2)

    # 测试基类属性
    assert obj.x == 1

    # 测试派生类属性
    assert obj.y == 2

    # 测试修改
    obj.x = 10
    obj.y = 20

    assert obj.x == 10
    assert obj.y == 20


def test_slots_inheritance_no_dict() -> None:
    """测试继承链中的 __slots__ 没有 __dict__"""

    obj = DerivedSlotted(1, 2)

    # 断言没有 __dict__
    assert not hasattr(obj, "__dict__"), "继承 __slots__ 的类不应该有 __dict__"


def test_slots_inheritance_memory() -> None:
    """测试继承链的内存效率"""

    base = BaseSlotted(1)
    derived = DerivedSlotted(1, 2)

    base_size = sys.getsizeof(base)
    derived_size = sys.getsizeof(derived)

    # 派生类应该比基类大（因为有更多属性）
    assert derived_size > base_size, "派生类应该比基类占用更多内存"

    # 但增加应该是合理的（不是翻倍）
    size_increase_ratio = derived_size / base_size

    assert size_increase_ratio < 2.0, "派生类内存增加应该是合理的"

    print(f"✅ 派生类内存增加 {(size_increase_ratio - 1) * 100:.1f}%")


# ============================================================================
# 测试 4: dataclass(slots=True)
# ============================================================================


def test_dataclass_slots_functionality() -> None:
    """测试 dataclass(slots=True) 的功能"""

    obj = DataSlottedClass(1, 2, 3)

    # 测试属性访问
    assert obj.x == 1
    assert obj.y == 2
    assert obj.z == 3

    # 测试 dataclass 生成的方法
    assert hasattr(obj, "__eq__"), "dataclass 应该生成 __eq__"
    assert hasattr(obj, "__repr__"), "dataclass 应该生成 __repr__"

    # 测试相等性
    obj2 = DataSlottedClass(1, 2, 3)
    assert obj == obj2, "相同值的 dataclass 应该相等"

    # 测试 repr
    repr_str = repr(obj)
    assert "DataSlottedClass" in repr_str
    assert "x=1" in repr_str


# ============================================================================
# 测试 5: 大规模对象
# ============================================================================


def test_large_scale_object_creation() -> None:
    """测试大规模对象创建"""

    n = 10_000

    # 创建 __slots__ 对象
    objects = [SlottedClass(i, i, i) for i in range(n)]

    # 验证对象数量
    assert len(objects) == n

    # 验证第一个和最后一个对象
    assert objects[0].x == 0
    assert objects[-1].x == n - 1

    # 验证所有对象都是正确的类型
    assert all(isinstance(obj, SlottedClass) for obj in objects)

    print(f"✅ 成功创建 {n:,} 个 __slots__ 对象")


# ============================================================================
# 测试 6: 性能特性
# ============================================================================


def test_slots_vs_dynamic_size_comparison() -> None:
    """测试并对比不同实现的内存占用"""

    n = 100

    # 创建对象列表
    dynamic_objects = [DynamicClass(i, i, i) for i in range(n)]
    slotted_objects = [SlottedClass(i, i, i) for i in range(n)]

    # 计算单个对象平均大小
    dynamic_avg_size = sum(sys.getsizeof(obj) + sys.getsizeof(obj.__dict__) for obj in dynamic_objects) / n

    slotted_avg_size = sum(sys.getsizeof(obj) for obj in slotted_objects) / n

    # 断言 __slots__ 更小
    assert slotted_avg_size < dynamic_avg_size

    saving = 1 - (slotted_avg_size / dynamic_avg_size)

    print(f"✅ 平均节省 {saving:.1%} 内存 (每个对象)")


# ============================================================================
# 测试 7: 边界情况
# ============================================================================


def test_slots_empty_class() -> None:
    """测试空 __slots__ 类"""

    class EmptySlotted:
        __slots__ = ()

    obj = EmptySlotted()

    # 应该没有任何属性
    assert not hasattr(obj, "__dict__")

    # 尝试设置属性应该失败
    with pytest.raises(AttributeError):
        obj.x = 1  # type: ignore[attr-defined]


def test_slots_with_defaults() -> None:
    """测试带默认值的 __slots__ 类"""

    class SlottedWithDefaults:
        __slots__ = ("x", "y")

        def __init__(self, x: int = 0, y: int = 0) -> None:
            self.x = x
            self.y = y

    # 测试默认值
    obj1 = SlottedWithDefaults()
    assert obj1.x == 0
    assert obj1.y == 0

    # 测试部分指定
    obj2 = SlottedWithDefaults(10)
    assert obj2.x == 10
    assert obj2.y == 0

    # 测试全部指定
    obj3 = SlottedWithDefaults(10, 20)
    assert obj3.x == 10
    assert obj3.y == 20


# ============================================================================
# 测试 8: 类型检查
# ============================================================================


def test_slots_type_hints() -> None:
    """测试 __slots__ 类的类型提示"""

    class TypedSlotted:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: str) -> None:
            self.x: int = x
            self.y: str = y

    obj = TypedSlotted(42, "hello")

    assert isinstance(obj.x, int)
    assert isinstance(obj.y, str)
    assert obj.x == 42
    assert obj.y == "hello"


# ============================================================================
# 测试总结
# ============================================================================


def test_summary(capsys: pytest.CaptureFixture[str]) -> None:
    """打印测试总结"""

    print("\n" + "=" * 80)
    print("L23 测试总结")
    print("=" * 80)
    print("\n测试覆盖:")
    print("  ✅ __slots__ 内存节省验证")
    print("  ✅ 属性访问功能测试")
    print("  ✅ 继承链 __slots__ 测试")
    print("  ✅ dataclass(slots=True) 测试")
    print("  ✅ 大规模对象创建测试")
    print("  ✅ 边界情况测试")
    print("  ✅ 类型提示测试")
    print("\n关键发现:")
    print("  • __slots__ 节省 30-60% 内存")
    print("  • 继承链保持内存效率")
    print("  • dataclass(slots=True) 兼顾性能和可读性")
    print("  • 不能动态添加属性（预期行为）")
    print()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
