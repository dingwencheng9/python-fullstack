"""L10: 类型系统 - 类型收窄与类型守卫"""

from typing import TypeGuard, Any

# === Part 1: isinstance 收窄 ===


def process_value(value: int | str | list) -> str:
    """使用 isinstance 进行类型收窄"""
    if isinstance(value, int):
        return f"整数: {value * 2}"
    if isinstance(value, str):
        return f"字符串: {value.upper()}"
    return f"列表: {len(value)} 项"


print(process_value(42))  # 整数: 84
print(process_value("hello"))  # 字符串: HELLO
print(process_value([1, 2, 3]))  # 列表: 3 项

# === Part 2: 类型守卫函数 ===


def is_string_list(value: list[object]) -> TypeGuard[list[str]]:
    """类型守卫：检查列表是否全是字符串"""
    return all(isinstance(item, str) for item in value)


def filter_strings(items: list[int | str]) -> list[str]:
    """过滤出字符串"""
    return [item for item in items if isinstance(item, str)]


def process_mixed(items: list[int | str]) -> list[str]:
    """处理混合列表"""
    strings: list[str] = []
    for item in items:
        if isinstance(item, str):
            strings.append(item)
    return strings


# 使用类型守卫
mixed_list: list[int | str] = [1, "hello", 2, "world", 3]
string_items = filter_strings(mixed_list)
print(string_items)  # ['hello', 'world']

# === Part 3:  discriminated union ===

from typing import Literal

type Shape = Literal["circle", "rectangle", "triangle"]


def area(shape_type: Shape, **kwargs: float) -> float:
    """计算形状面积"""
    match shape_type:
        case "circle":
            import math

            radius = kwargs["radius"]
            return math.pi * radius**2
        case "rectangle":
            width = kwargs["width"]
            height = kwargs["height"]
            return width * height
        case "triangle":
            base = kwargs["base"]
            height = kwargs["height"]
            return 0.5 * base * height


print(area("circle", radius=5))  # 78.54
print(area("rectangle", width=4, height=6))  # 24
print(area("triangle", base=3, height=4))  # 6.0

# === Part 4: 泛型类型守卫 ===

from typing import TypeVar

T = TypeVar("T")


def is_non_empty(value: list[T] | None) -> TypeGuard[list[T]]:
    """检查列表是否非空"""
    return value is not None and len(value) > 0


def process_list(value: list[int] | None) -> int:
    """安全处理列表"""
    if is_non_empty(value):
        # 在这里，type checker 知道 value 是 list[int] 非空
        return sum(value)
    return 0


print(process_list([1, 2, 3]))  # 6
print(process_list([]))  # 0
print(process_list(None))  # 0

# === Part 5: 运行时类型检查工具 ===


def get_type_name(value: Any) -> str:
    """获取值的类型名称"""
    return type(value).__name__


def validate_type(value: Any, expected_type: type) -> bool:
    """验证值是否符合预期类型"""
    return isinstance(value, expected_type)


def safe_cast(value: Any, expected_type: type[T]) -> T | None:
    """安全类型转换，失败返回 None"""
    if isinstance(value, expected_type):
        return value
    return None


# 测试
data: list[Any] = [42, "hello", [1, 2, 3], {"key": "value"}]

for item in data:
    type_name = get_type_name(item)
    print(f"类型: {type_name}, 值: {item}")

# 安全转换
maybe_int = safe_cast("42", int)
print(f"safe_cast('42', int) = {maybe_int}")  # None

maybe_str = safe_cast("hello", str)
print(f"safe_cast('hello', str) = {maybe_str}")  # hello

# === Part 6: Protocol + 收窄 ===

from typing import Protocol, runtime_checkable


@runtime_checkable
class Printable(Protocol):
    def __str__(self) -> str: ...


class RichString:
    def __init__(self, content: str):
        self.content = content

    def __str__(self) -> str:
        return self.content


class NotPrintable:
    pass


def to_string(value: Printable) -> str:
    """转换为字符串"""
    return str(value)


def try_convert(value: Printable | object) -> str | None:
    """尝试转换，可能失败"""
    if isinstance(value, Printable):
        return to_string(value)
    return None


items: list[Printable | object] = [RichString("Hello"), NotPrintable(), "plain string", 42]

for item in items:
    result = try_convert(item)
    print(f"转换结果: {result}")

print("\n=== 类型收窄示例完成 ===")
