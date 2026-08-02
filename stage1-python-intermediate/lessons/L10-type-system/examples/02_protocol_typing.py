"""L10: 类型系统 - Protocol 示例"""

from typing import Protocol, TypeVar, runtime_checkable, Sequence

T = TypeVar("T")

# === Part 0: Drawable & Resizable 协议（测试所需）===


@runtime_checkable
class Drawable(Protocol):
    """可绘制协议"""

    def draw(self) -> str: ...


@runtime_checkable
class Resizable(Protocol):
    """可调整大小协议"""

    def resize(self, factor: float) -> None: ...


class Circle:
    """圆形 - 同时支持 Drawable 和 Resizable"""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(r={self.radius})"

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Square:
    """正方形 - 只支持 Drawable"""

    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> str:
        return f"Square(side={self.side})"


def render_shapes(shapes: Sequence[Drawable]) -> None:
    """渲染所有形状"""
    for shape in shapes:
        print(shape.draw())


def process_resizable(shapes: Sequence[object]) -> None:
    """处理可调整大小的对象"""
    for shape in shapes:
        if isinstance(shape, Resizable):
            shape.resize(2.0)


# === Part 1: Protocol 定义 ===


@runtime_checkable
class Sized(Protocol):
    """支持大小操作的协议"""

    def __len__(self) -> int: ...


@runtime_checkable
class Addable(Protocol[T]):
    """支持加法操作的协议"""

    def __add__(self, other: T) -> T: ...


def total_length(items: list[Sized]) -> int:
    """计算所有元素的总长度"""
    return sum(len(item) for item in items)


# 测试
print(total_length(["hello", "world"]))  # 10
print(total_length([[1], [2], [3]]))  # 3
print(total_length({"a": 1, "b": 2}))  # 2

# === Part 2: 结构子类型示例 ===


class Duck:
    """鸭子类型：只要会叫就是鸭子"""

    def quack(self) -> str:
        return "Quack!"


class Robot:
    """机器人也能"叫"（说话）"""

    def quack(self) -> str:
        return "Beep-boop!"


class Person:
    """人不会 quack"""

    def speak(self) -> str:
        return "Hello!"


def make_it_quack(obj: object) -> str:
    """Protocol 检查对象是否有 quack 方法"""
    if isinstance(obj, Sized):
        return f"Length: {len(obj)}"
    return "Unknown"


duck = Duck()
robot = Robot()
person = Person()

print(make_it_quack(duck))  # Unknown (Duck 没实现 Sized)
print(make_it_quack("hello"))  # Length: 5 (str 实现了 Sized)

# === Part 3: 泛型 Protocol ===

from typing import TypeVar

U = TypeVar("U")


class Transformer(Protocol[T, U]):
    """转换器协议"""

    def transform(self, value: T) -> U: ...


class StringToInt:
    """字符串转整数"""

    def transform(self, value: str) -> int:
        return len(value)


class IntToString:
    """整数转字符串"""

    def transform(self, value: int) -> str:
        return str(value)


def apply_transform(transformer: Transformer[T, U], value: T) -> U:
    """应用转换器"""
    return transformer.transform(value)


string_to_int = StringToInt()
int_to_string = IntToString()

print(apply_transform(string_to_int, "hello"))  # 5
print(apply_transform(int_to_string, 42))  # "42"

# === Part 4: 运行时检查 ===

from typing import get_type_hints, get_origin, get_args


class MyClass:
    value: int
    name: str


hints = get_type_hints(MyClass)
print(f"类型提示: {hints}")
# {'value': <class 'int'>, 'name': <class 'str'>}

# 检查泛型
# 演示旧的 List[int] 形式（Python 3.8 之前）
print(f"list[int] 起源: {get_origin(list[int])}")  # list
print(f"list[int] 参数: {get_args(list[int])}")  # (int,)

print("\n=== Protocol 示例完成 ===")
