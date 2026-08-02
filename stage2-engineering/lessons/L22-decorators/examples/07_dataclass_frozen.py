"""

使用 @dataclass(frozen=True) 创建不可变数据类。

本文件演示：
- @dataclass 基本用法和常用参数
- frozen=True 实现不可变性
- order=True 自动生成比较方法
- slots=True 内存优化

作者: Python 3.13 全栈课程
日期: 2026-07-13
Python版本: 3.10+
"""

from __future__ import annotations

from dataclasses import dataclass, field, FrozenInstanceError


def demo_basic_dataclass() -> None:
    """演示 @dataclass 基本用法"""
    print("=" * 50)
    print("1. @dataclass 基本用法")
    print("=" * 50)

    @dataclass
    class Point:
        x: float
        y: float
        label: str = "origin"

    p = Point(1.0, 2.0)
    print(f"Point: {p}")
    # 自动生成 __repr__ → Point(x=1.0, y=2.0, label='origin')

    # 自动生成 __eq__
    p2 = Point(1.0, 2.0)
    print(f"p == p2: {p == p2}")  # True（自动 __eq__）

    # 自动生成 __init__
    p3 = Point(3.0, 4.0, "B")
    print(f"Point3: {p3}")
    print()


def demo_frozen_dataclass() -> None:
    """演示 frozen=True 不可变数据类"""
    print("=" * 50)
    print("2. @dataclass(frozen=True) 不可变数据类")
    print("=" * 50)

    @dataclass(frozen=True)
    class Config:
        host: str
        port: int
        timeout: float = 30.0
        debug: bool = False

    config = Config("localhost", 8080, debug=True)
    print(f"Config: {config}")

    # 尝试修改会抛出 FrozenInstanceError
    try:
        config.port = 9000
    except FrozenInstanceError as e:
        print(f"✓ 修改被阻止: {e}")
    print()


def demo_frozen_use_cases() -> None:
    """演示 frozen 数据类的实际应用场景"""
    print("=" * 50)
    print("3. frozen 数据类的应用场景")
    print("=" * 50)

    @dataclass(frozen=True)
    class RGB:
        """不可变的 RGB 颜色值"""

        r: int = field(compare=True)
        g: int = field(compare=True)
        b: int = field(compare=True)

        def to_hex(self) -> str:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    # 场景 1: 作为字典的键（必须是可哈希的）
    color_map: dict[RGB, str] = {
        RGB(255, 0, 0): "red",
        RGB(0, 255, 0): "green",
        RGB(0, 0, 255): "blue",
    }
    print(f"颜色映射: {color_map[RGB(255, 0, 0)]}")  # red

    # 场景 2: 函数式编程中的不可变数据
    def apply_tint(color: RGB, tint: float) -> RGB:
        """返回新的 RGB 对象（不修改原对象）"""
        return RGB(
            r=int(min(255, color.r * tint)),
            g=int(min(255, color.g * tint)),
            b=int(min(255, color.b * tint)),
        )

    original = RGB(100, 150, 200)
    darkened = apply_tint(original, 0.5)
    print(f"原始: {original}")
    print(f"变暗: {darkened}")
    print(f"原始未被修改: {original}")
    print()


def demo_order_dataclass() -> None:
    """演示 order=True 自动生成比较方法"""
    print("=" * 50)
    print("4. @dataclass(order=True) 自动比较方法")
    print("=" * 50)

    @dataclass(order=True)
    class Version:
        major: int
        minor: int
        patch: int

        def __str__(self) -> str:
            return f"v{self.major}.{self.minor}.{self.patch}"

    v1 = Version(1, 0, 0)
    v2 = Version(1, 2, 0)
    v3 = Version(2, 0, 0)

    print(f"版本比较: {v1} < {v2} < {v3}")
    print(f"v1 < v2: {v1 < v2}")  # True
    print(f"v2 > v1: {v2 > v1}")  # True
    print(f"v3 > v2: {v3 > v2}")  # True

    # 支持排序
    versions = [v2, v1, v3]
    print(f"排序前: {versions}")
    versions.sort()
    print(f"排序后: {versions}")
    print()


def demo_slots_dataclass() -> None:
    """演示 slots=True 内存优化"""
    print("=" * 50)
    print("5. @dataclass(slots=True) 内存优化")
    print("=" * 50)

    @dataclass(slots=True)
    class PointSlots:
        x: float
        y: float

    @dataclass
    class PointNormal:
        x: float
        y: float

    p1 = PointSlots(1.0, 2.0)
    p2 = PointNormal(1.0, 2.0)

    print(f"slots=True 对象: {p1}")
    print(f"  是否有 __slots__: {hasattr(PointSlots, '__slots__')}")
    print(f"普通 dataclass 对象: {p2}")
    print()

    # slots 禁止动态属性
    try:
        p1.z = 3.0
    except AttributeError as e:
        print(f"✓ slots 禁止动态属性: {e}")
    print()


def demo_field_options() -> None:
    """演示 field 高级选项"""
    print("=" * 50)
    print("6. field() 高级选项")
    print("=" * 50)

    @dataclass
    class Product:
        id: str
        name: str
        price: float
        tags: list[str] = field(default_factory=list)  # 重要！
        metadata: dict = field(default_factory=dict)  # 重要！

    # 使用 default_factory 避免可变默认值陷阱
    p1 = Product("001", "Apple", 5.99, tags=["fruit"])
    p2 = Product("002", "Banana", 3.99, tags=["fruit"])

    p1.tags.append("organic")
    print(f"p1.tags: {p1.tags}")
    print(f"p2.tags: {p2.tags}")  # 不会受影响
    print()


def main() -> None:
    """主函数"""
    print(">>> @dataclass(frozen=True) 演示\n")

    demo_basic_dataclass()
    demo_frozen_dataclass()
    demo_frozen_use_cases()
    demo_order_dataclass()
    demo_slots_dataclass()
    demo_field_options()

    print(">>> 演示完成！")
    print()
    print("要点总结:")
    print("  1. @dataclass 自动生成 __init__, __repr__, __eq__")
    print("  2. frozen=True 使实例不可变，适合配置和函数式编程")
    print("  3. order=True 自动生成 <, >, <=, >= 比较方法")
    print("  4. slots=True 使用 __slots__ 优化内存")
    print("  5. 可变默认值使用 default_factory，避免共享陷阱")


if __name__ == "__main__":
    main()
