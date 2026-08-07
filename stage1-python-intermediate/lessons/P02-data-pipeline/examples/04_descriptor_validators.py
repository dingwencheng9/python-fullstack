"""P02 示例 4: 描述符验证器

演示 L15 描述符与属性的核心概念：
- __get__/__set__/__delete__ 方法
- __set_name__ 自动获取属性名
- 数据描述符 vs 非数据描述符
- ValidatedField 通用验证描述符

运行方式:
    python examples/04_descriptor_validators.py
"""

import re
from typing import Any, Callable, TypeVar
from dataclasses import dataclass

T = TypeVar("T")


# ============================================================
# 1. 基础描述符
# ============================================================

class PrivateAttribute:
    """私有属性描述符 - 演示 __get__ 和 __set__"""

    def __init__(self, default: T | None = None) -> None:
        self.default = default
        self.name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        """自动获取属性名"""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> T:
        """获取属性"""
        if obj is None:
            return self  # type: ignore
        return getattr(obj, f"_private_{self.name}", self.default)

    def __set__(self, obj: Any, value: T) -> None:
        """设置属性"""
        if obj is None:
            raise AttributeError("Cannot set attribute on class")
        object.__setattr__(obj, f"_private_{self.name}", value)


# ============================================================
# 2. 验证描述符
# ============================================================

class ValidatedField:
    """通用验证描述符

    支持：
    - 数值范围验证
    - 正则表达式验证
    - 自定义验证函数
    """

    def __init__(
        self,
        *,
        default: T | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        pattern: str | None = None,
        validator: Callable[[T], bool] | None = None,
        choices: list[T] | None = None,
    ) -> None:
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.pattern = re.compile(pattern) if pattern else None
        self.validator = validator
        self.choices = choices
        self.name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        """自动获取属性名"""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> T | None:
        """获取属性"""
        if obj is None:
            return self
        return obj.__dict__.get(self.name)  # type: ignore

    def __set__(self, obj: Any, value: T) -> None:
        """设置属性并进行验证"""
        # 类型检查
        if value is not None:
            # 数值范围验证
            if self.min_value is not None and value < self.min_value:
                raise ValueError(
                    f"{self.name} 不能小于 {self.min_value}，"
                    f"实际值: {value}"
                )
            if self.max_value is not None and value > self.max_value:
                raise ValueError(
                    f"{self.name} 不能大于 {self.max_value}，"
                    f"实际值: {value}"
                )
            # 正则验证
            if self.pattern and not self.pattern.match(str(value)):
                raise ValueError(
                    f"{self.name} 不匹配模式 {self.pattern.pattern}，"
                    f"实际值: {value}"
                )
            # 自定义验证
            if self.validator and not self.validator(value):
                raise ValueError(f"{self.name} 验证失败，实际值: {value}")
            # 枚举验证
            if self.choices and value not in self.choices:
                raise ValueError(
                    f"{self.name} 必须是 {self.choices} 之一，"
                    f"实际值: {value}"
                )
        obj.__dict__[self.name] = value  # type: ignore


# ============================================================
# 3. 委托描述符
# ============================================================

class LazyAttribute:
    """延迟加载描述符 - 首次访问时计算"""

    def __init__(self, factory: Callable[[], T]) -> None:
        self.factory = factory
        self.name: str | None = None
        self._cached: dict[int, T] = {}

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self._cached[id(owner)] = None  # 标记未初始化

    def __get__(self, obj: Any, objtype: type | None = None) -> T:
        if obj is None:
            return self
        obj_id = id(obj)
        if self._cached.get(obj_id) is None:
            self._cached[obj_id] = self.factory()
        return self._cached[obj_id]


# ============================================================
# 4. 只读描述符
# ============================================================

class ReadOnly:
    """只读描述符 - 设置后不可修改"""

    def __init__(self) -> None:
        self.name: str | None = None
        self._values: dict[int, Any] = {}

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return self._values.get(id(obj))

    def __set__(self, obj: Any, value: Any) -> None:
        if id(obj) in self._values:
            raise AttributeError(f"{self.name} 是只读属性")
        self._values[id(obj)] = value


# ============================================================
# 5. 观察者描述符
# ============================================================

class Observable:
    """可观察描述符 - 值变化时通知观察者"""

    def __init__(self) -> None:
        self.name: str | None = None
        self._values: dict[int, Any] = {}
        self._observers: dict[int, list[Callable]] = {}

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        return self._values.get(id(obj))

    def __set__(self, obj: Any, value: Any) -> None:
        old_value = self._values.get(id(obj))
        self._values[id(obj)] = value

        # 通知观察者
        if observers := self._observers.get(id(obj)):
            for callback in observers:
                callback(obj, self.name, old_value, value)

    def add_observer(self, obj: Any, callback: Callable) -> None:
        """添加观察者"""
        obj_id = id(obj)
        if obj_id not in self._observers:
            self._observers[obj_id] = []
        self._observers[obj_id].append(callback)


# ============================================================
# 6. 使用示例：数据模型
# ============================================================

class UserRecord:
    """用户记录 - 演示描述符应用"""

    # ID: 4位数字
    id = ValidatedField(
        pattern=r"^\d{4}$",
        default="0000"
    )

    # 名称: 只允许字母和中文
    name = ValidatedField(
        pattern=r"^[A-Za-z一-龥]+$",
        default=""
    )

    # 年龄: 0-150
    age = ValidatedField(
        min_value=0,
        max_value=150,
        default=0
    )

    # 分数: 0-100
    score = ValidatedField(
        min_value=0.0,
        max_value=100.0,
        default=0.0
    )

    # 状态: 枚举
    status = ValidatedField(
        choices=["active", "inactive", "pending"],
        default="pending"
    )

    # 延迟加载的配置
    config = LazyAttribute(lambda: {"theme": "light"})

    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.id = user_id
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return (
            f"UserRecord(id={self.id}, name={self.name}, "
            f"age={self.age}, score={self.score}, status={self.status})"
        )


# ============================================================
# 7. 描述符 vs property
# ============================================================

class DescriptorVsProperty:
    """对比描述符和 property"""

    # 方式 1: 使用 property
    @property
    def email_property(self) -> str:
        return self._email

    @email_property.setter
    def email_property(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("无效的邮箱")
        self._email = value

    # 方式 2: 使用描述符
    class EmailDescriptor:
        def __set_name__(self, owner, name):
            self.name = name

        def __get__(self, obj, objtype=None):
            return getattr(obj, f"_{self.name}", "")

        def __set__(self, obj, value):
            if "@" not in value:
                raise ValueError("无效的邮箱")
            object.__setattr__(obj, f"_{self.name}", value)

    email_descriptor = EmailDescriptor()


# ============================================================
# 演示函数
# ============================================================

def demonstrate_basic_descriptor():
    """演示基础描述符"""
    print("\n=== 基础描述符 ===")

    class Person:
        name = PrivateAttribute()
        age = PrivateAttribute(0)

    p = Person()
    print(f"默认 name: {p.name}")
    print(f"默认 age: {p.age}")

    p.name = "Alice"
    p.age = 25
    print(f"设置后 name: {p.name}")
    print(f"设置后 age: {p.age}")


def demonstrate_validated_field():
    """演示验证描述符"""
    print("\n=== 验证描述符 ===")

    # 测试有效值
    record = UserRecord("0001", "Alice", 25)
    record.score = 95.5
    record.status = "active"
    print(f"创建记录: {record}")

    # 测试范围验证
    print("\n测试范围验证:")
    try:
        record.age = -1
    except ValueError as e:
        print(f"  ✗ 年龄 -1: {e}")

    try:
        record.score = 150
    except ValueError as e:
        print(f"  ✗ 分数 150: {e}")

    # 测试正则验证
    print("\n测试正则验证:")
    try:
        record.id = "abc"
    except ValueError as e:
        print(f"  ✗ ID abc: {e}")

    try:
        record.name = "123"
    except ValueError as e:
        print(f"  ✗ 名称 123: {e}")

    # 测试枚举验证
    print("\n测试枚举验证:")
    try:
        record.status = "unknown"
    except ValueError as e:
        print(f"  ✗ 状态 unknown: {e}")


def demonstrate_readonly():
    """演示只读描述符"""
    print("\n=== 只读描述符 ===")

    class ImmutablePoint:
        """不可变点"""
        x = ReadOnly()
        y = ReadOnly()

        def __init__(self, x: float, y: float) -> None:
            self.x = x  # 设置只读属性
            self.y = y

    point = ImmutablePoint(3.14, 2.71)
    print(f"只读点: ({point.x}, {point.y})")

    try:
        point.x = 0  # 尝试修改
    except AttributeError as e:
        print(f"修改只读: {e}")


def demonstrate_lazy():
    """演示延迟加载"""
    print("\n=== 延迟加载 ===")

    class LazyDemo:
        data = LazyAttribute(lambda: {"computed": True})

    demo = LazyDemo()
    print(f"延迟加载数据: {demo.data}")


def demonstrate_observable():
    """演示可观察属性"""
    print("\n=== 可观察属性 ===")

    # 使用可变对象存储观察者
    observers: list[Callable] = []

    class ObservableRecord:
        """可观察记录"""
        name = ""

        @property
        def score(self):
            return self._score

        @score.setter
        def score(self, value):
            nonlocal observers
            old = getattr(self, '_score', None)
            self._score = value
            for callback in observers:
                callback(self.__class__.__name__, 'score', old, value)

    record = ObservableRecord()
    record._score = 0

    def on_score_change(name, field, old, new):
        print(f"  {field} 从 {old} 变为 {new}")

    observers.append(on_score_change)
    record.score = 85.0
    record.score = 90.0


def demonstrate_descriptor_vs_property():
    """演示描述符 vs property"""
    print("\n=== 描述符 vs Property ===")

    obj = DescriptorVsProperty()

    # property 方式
    obj.email_property = "test@example.com"
    print(f"property 方式: {obj.email_property}")

    # 描述符方式
    obj.email_descriptor = "user@domain.org"
    print(f"描述符方式: {obj.email_descriptor}")


# ============================================================
# 主函数
# ============================================================

def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 4: 描述符验证器")
    print("=" * 60)

    demonstrate_basic_descriptor()
    demonstrate_validated_field()
    demonstrate_readonly()
    demonstrate_lazy()
    demonstrate_observable()
    demonstrate_descriptor_vs_property()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
