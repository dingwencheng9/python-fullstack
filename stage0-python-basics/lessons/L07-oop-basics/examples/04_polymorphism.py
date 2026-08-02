"""示例：多态

演示 Python 的多态特性：接口统一、鸭子类型、抽象基类概念。
"""

# ============ 多态基础 ============
print("=== 多态基础 ===")


class Shape:
    def area(self) -> float:
        # raise TypeError: 子类必须实现此方法  # L08 将学到
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius**2


# 多态：不同对象调用相同方法，表现不同
shapes: list[Shape] = [Rectangle(5, 10), Circle(7)]

print("计算各形状面积：")
for shape in shapes:
    print(f"  {shape.__class__.__name__}: {shape.area():.2f}")

# ============ 鸭子类型 ============
print("\n=== 鸭子类型 ===")


class Dog:
    def speak(self) -> str:
        return "Woof!"


class Cat:
    def speak(self) -> str:
        return "Meow!"


class Duck:
    def speak(self) -> str:
        return "Quack!"


# 鸭子类型：不关心类型，只关心行为
def make_speak(obj: object) -> str:
    """只要对象有 speak 方法就能调用"""
    return obj.speak()


animals = [Dog(), Cat(), Duck()]
for animal in animals:
    print(f"make_speak({animal.__class__.__name__}) = {make_speak(animal)}")


# ============ 协议（Protocol） ============
# ruff: noqa: E402  # 教学演示：展示导入通常放在文件顶部
print("\n=== Protocol 类型（Python 3.8+） ===")

from typing import Protocol


class Speakable(Protocol):
    """可说话协议"""

    def speak(self) -> str: ...


def greet(speaker: Speakable) -> str:
    """只要实现 speak 方法即可"""
    return speaker.speak()


class Robot:
    def speak(self) -> str:
        return "Beep boop!"


robot = Robot()
print(f"greet(robot) = {greet(robot)}")  # 自动满足 Speakable 协议


# ============ 多态与函数 ============
print("\n=== 多态与函数 ===")


def print_info(obj: object) -> None:
    """多态函数"""
    if hasattr(obj, "name"):
        print(f"  Name: {obj.name}")
    if hasattr(obj, "area"):
        print(f"  Area: {obj.area():.2f}")
    if hasattr(obj, "speak"):
        print(f"  Sound: {obj.speak()}")


class Bird:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "Tweet!"


bird = Bird("Sparrow")
print_info(bird)

print()

rect = Rectangle(3, 4)
print_info(rect)


# ============ 多态与容器 ============
print("\n=== 多态与容器 ===")


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


# 存储不同类型的对象
animals: list[Animal] = [
    Dog("Buddy"),
    Cat("Whiskers"),
    Dog("Max"),
]

# 统一处理
for animal in animals:
    print(f"{animal.name}: {animal.speak()}")


# ============ 运算符多态 ============
print("\n=== 运算符多态 ===")


class Text:
    def __init__(self, content: str) -> None:
        self.content = content


t1 = Text("Hello ")
t2 = Text("World")
t3 = t1  # 不支持 + 运算符，仅作演示
t4 = t1  # 不支持 * 运算符，仅作演示

print(f"t1.content = {t1.content}")
print(f"t2.content = {t2.content}")


# ============ 多态的实际应用 ============
print("\n=== 多态的实际应用 ===")


class DataSerializer:
    """数据序列化器"""

    def serialize(self, obj: object) -> str:
        """多态序列化"""
        if isinstance(obj, str):
            return f'"{obj}"'
        if isinstance(obj, (int, float)):
            return str(obj)
        if isinstance(obj, list):
            items = ", ".join(self.serialize(item) for item in obj)
            return f"[{items}]"
        if hasattr(obj, "__dict__"):
            # 对于自定义对象，序列化其属性
            return str(obj)
        return str(obj)


serializer = DataSerializer()
print(f"serialize('hello') = {serializer.serialize('hello')}")
print(f"serialize(42) = {serializer.serialize(42)}")
print(f"serialize([1, 2, 3]) = {serializer.serialize([1, 2, 3])}")
dict_data = {"a": 1}
print(f"serialize({dict_data}) = {serializer.serialize(dict_data)}")


if __name__ == "__main__":
    print("\n=== 多态总结 ===")
    print("1. 多态：同一接口不同实现")
    print("2. 鸭子类型：'如果它走路像鸭子，叫声像鸭子，那它就是鸭子'")
    print("3. Protocol：类型注解中定义接口契约")
    print("4. 多态让我们编写通用代码，操作不同类型的对象")
