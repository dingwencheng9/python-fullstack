"""

from __future__ import annotations

L18 示例 2: mypy 类型检查演示

展示 mypy 的核心功能和类型检查最佳实践。
"""

from typing import Any, Protocol

# ============================================================================
# 示例 1: 基础类型注解
# ============================================================================


def greet(name: str) -> str:
    """正确的类型注解"""
    return f"Hello, {name}!"


def add_numbers(a: int, b: int) -> int:
    """整数加法"""
    return a + b


# ❌ 类型错误示例（mypy 会检测）
def buggy_function(value: int) -> str:
    """类型不匹配"""
    # return value  # ❌ mypy: error: Incompatible return value type
    return str(value)  # ✅ 修复


# ============================================================================
# 示例 2: 可选类型（Union 和 None）
# ============================================================================


def find_user(user_id: int) -> dict[str, Any] | None:
    """查找用户，可能返回 None"""
    if user_id > 0:
        return {"id": user_id, "name": "Alice"}
    return None


def process_user(user_id: int) -> None:
    """处理用户数据"""
    user = find_user(user_id)

    # ❌ 直接使用可能是 None 的值
    # print(user["name"])  # mypy: error: Item "None" has no attribute

    # ✅ 正确做法：检查 None
    if user is not None:
        print(user["name"])  # ✅ mypy 知道这里 user 不是 None


# ============================================================================
# 示例 3: 泛型类型
# ============================================================================


def get_first_item(items: list[str]) -> str | None:
    """获取列表第一项"""
    return items[0] if items else None


def process_items(items: list[int]) -> list[int]:
    """处理整数列表"""
    return [item * 2 for item in items]


# ============================================================================
# 示例 4: 类型收窄（Type Narrowing）
# ============================================================================


def process_value(value: int | str | None) -> str:
    """处理多种类型的值"""

    # mypy 会跟踪类型变化
    if value is None:
        return "No value"
    if isinstance(value, int):
        # 这里 mypy 知道 value 是 int
        return f"Number: {value * 2}"
    # 这里 mypy 知道 value 是 str
    return f"String: {value.upper()}"


# ============================================================================
# 示例 5: 字典类型注解
# ============================================================================


def create_user(name: str, age: int) -> dict[str, int | str]:
    """创建用户字典"""
    return {"name": name, "age": age}


def get_config() -> dict[str, Any]:
    """获取配置（值类型不确定时使用 Any）"""
    return {
        "host": "localhost",
        "port": 8000,
        "debug": True,
    }


# ============================================================================
# 示例 6: 类的类型注解
# ============================================================================


class User:
    """用户类"""

    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def get_info(self) -> str:
        """获取用户信息"""
        return f"{self.name}, {self.age} years old"

    def update_age(self, new_age: int) -> None:
        """更新年龄"""
        if new_age < 0:
            raise ValueError("Age cannot be negative")
        self.age = new_age


# ============================================================================
# 示例 7: 协议（Protocol）- 结构化子类型
# ============================================================================


class Drawable(Protocol):
    """可绘制对象协议"""

    def draw(self) -> str:
        """绘制方法"""
        ...


class Circle:
    """圆形（实现了 Drawable 协议但不需要继承）"""

    def draw(self) -> str:
        return "Drawing a circle"


class Square:
    """正方形"""

    def draw(self) -> str:
        return "Drawing a square"


def render(obj: Drawable) -> None:
    """渲染对象"""
    print(obj.draw())


# ============================================================================
# 演示函数
# ============================================================================


def demonstrate_type_checking() -> None:
    """演示类型检查"""

    print("🔍 mypy 类型检查演示")
    print("=" * 70)

    # 1. 基础类型
    print("\n1️⃣ 基础类型注解")
    print("-" * 70)
    result = greet("Alice")
    print(f"  {result}")
    sum_result = add_numbers(10, 20)
    print(f"  10 + 20 = {sum_result}")

    # 2. 可选类型
    print("\n2️⃣ 可选类型处理")
    print("-" * 70)
    process_user(1)
    process_user(-1)

    # 3. 泛型类型
    print("\n3️⃣ 泛型类型")
    print("-" * 70)
    numbers = [1, 2, 3, 4, 5]
    doubled = process_items(numbers)
    print(f"  原始: {numbers}")
    print(f"  加倍: {doubled}")

    # 4. 类型收窄
    print("\n4️⃣ 类型收窄")
    print("-" * 70)
    print(f"  int: {process_value(42)}")
    print(f"  str: {process_value('hello')}")
    print(f"  None: {process_value(None)}")

    # 5. 类的使用
    print("\n5️⃣ 类的类型注解")
    print("-" * 70)
    user = User("Bob", 25)
    print(f"  {user.get_info()}")
    user.update_age(26)
    print(f"  更新后: {user.get_info()}")

    # 6. 协议
    print("\n6️⃣ 协议（Protocol）")
    print("-" * 70)
    circle = Circle()
    square = Square()
    render(circle)
    render(square)


def show_mypy_configuration() -> None:
    """展示 mypy 配置"""

    print("\n\n⚙️  mypy 配置示例")
    print("=" * 70)

    config = """
# pyproject.toml
[tool.mypy]
python_version = "3.13"
strict = true                    # 启用所有严格检查
warn_return_any = true          # 警告返回 Any
warn_unused_configs = true      # 警告未使用的配置
disallow_untyped_defs = true    # 禁止无类型定义

# 第三方库类型存根
[[tool.mypy.overrides]]
module = "some_library.*"
ignore_missing_imports = true

# 测试文件放宽要求
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
"""

    print(config)


def show_common_errors() -> None:
    """展示常见类型错误"""

    print("\n\n❌ 常见 mypy 错误及修复")
    print("=" * 70)

    errors = [
        (
            "error: Incompatible return value type",
            "返回值类型不匹配",
            "检查函数签名和实际返回值",
        ),
        (
            "error: Argument has incompatible type",
            "参数类型不匹配",
            "检查调用时传入的参数类型",
        ),
        (
            "error: Item 'None' has no attribute",
            "对 None 调用属性/方法",
            "在使用前检查是否为 None",
        ),
        (
            "error: Unsupported operand type(s)",
            "不支持的操作类型",
            "检查操作符两边的类型",
        ),
    ]

    for error, description, fix in errors:
        print(f"\n  {error}")
        print(f"  → {description}")
        print(f"  ✅ 修复: {fix}")


def show_best_practices() -> None:
    """展示最佳实践"""

    print("\n\n💡 mypy 使用最佳实践")
    print("=" * 70)

    practices = [
        "1. 始终为函数参数和返回值添加类型注解",
        "2. 使用 | None 而不是 Optional（Python 3.10+）",
        "3. 使用 list[str] 而不是 List[str]（Python 3.9+）",
        "4. 启用 strict 模式，从一开始就严格",
        "5. 使用 isinstance() 进行类型收窄",
        "6. 避免过度使用 Any，它会关闭类型检查",
        "7. 使用 Protocol 而不是继承（鸭子类型）",
        "8. Python 3.13: 使用 PEP 695 泛型语法（def func[T](...): ...）",
    ]

    for practice in practices:
        print(f"  {practice}")

    # PEP 695 泛型语法示例（Python 3.13）
    print("\n\n🆕 Python 3.13 PEP 695 泛型语法示例:")
    print("-" * 70)
    print("""
    # 旧语法（Python 3.11 及更早）
    from typing import TypeVar
    T = TypeVar('T')
    def old_style[T](items: list[T]) -> T:
        return items[0]

    # 新语法（Python 3.13）- 更简洁
    def new_style[T](items: list[T]) -> T:
        return items[0]

    # 带约束的泛型
    def process[T: (int, float)](value: T) -> T:
        return value * 2

    # 带默认值的泛型（Python 3.13+）
    def with_default[T = int](value: T) -> T:
        return value
    """)
    print("-" * 70)


def main() -> None:
    """主函数"""

    # 1. 演示类型检查
    demonstrate_type_checking()

    # 2. 展示配置
    show_mypy_configuration()

    # 3. 常见错误
    show_common_errors()

    # 4. 最佳实践
    show_best_practices()

    print("\n\n✨ 演示完成！")
    print("\n🔑 运行 mypy 检查:")
    print("  $ mypy example_02_mypy_types.py")
    print("  $ mypy --strict example_02_mypy_types.py")


if __name__ == "__main__":
    main()
