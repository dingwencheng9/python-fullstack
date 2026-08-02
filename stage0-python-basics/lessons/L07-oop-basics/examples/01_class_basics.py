"""示例：类与对象基础

演示 Python 类的定义、实例化和基本使用。
"""


# ============ 类的定义 ============
class Dog:
    """狗类（类文档字符串）"""

    # 类属性（所有实例共享）
    species = "Canis familiaris"

    # 构造方法
    def __init__(self, name: str, age: int) -> None:
        # 实例属性（每个实例独有）
        self.name = name
        self.age = age

    # 实例方法
    def bark(self) -> str:
        return f"{self.name} says Woof!"

    def get_info(self) -> str:
        return f"{self.name} is {self.age} years old"


# ============ 创建对象 ============
print("=== 创建对象 ===")
dog1 = Dog("Buddy", 3)
dog2 = Dog("Max", 5)

# 访问属性
print(f"dog1.name = {dog1.name}")
print(f"dog1.age = {dog1.age}")
print(f"dog1.species = {dog1.species}")  # 类属性

# 调用方法
print(f"dog1.bark() = {dog1.bark()}")
print(f"dog1.get_info() = {dog1.get_info()}")

# ============ self 参数 ============
print("\n=== self 参数 ===")


class Counter:
    def __init__(self) -> None:
        self.count = 0  # self 指向当前实例

    def increment(self) -> int:
        self.count += 1
        return self.count

    def reset(self) -> None:
        self.count = 0


counter1 = Counter()
counter2 = Counter()

print(f"counter1.increment() = {counter1.increment()}")  # 1
print(f"counter1.increment() = {counter1.increment()}")  # 2
print(f"counter2.increment() = {counter2.increment()}")  # 1（独立）

# ============ 类属性 vs 实例属性 ============
print("\n=== 类属性 vs 实例属性 ===")


class Cat:
    # 类属性
    kingdom = "Animal"

    def __init__(self, name: str) -> None:
        self.name = name  # 实例属性


cat1 = Cat("Whiskers")
cat2 = Cat("Tom")

print(f"cat1.kingdom = {cat1.kingdom}")  # Animal（从类继承）
print(f"cat2.kingdom = {cat2.kingdom}")  # Animal

# 修改类属性会影响所有实例
Cat.kingdom = "Mammal"
print(f"修改后 cat1.kingdom = {cat1.kingdom}")  # Mammal
print(f"修改后 cat2.kingdom = {cat2.kingdom}")  # Mammal

# 修改实例属性不影响其他实例
cat1.name = "Garfield"
print(f"cat1.name = {cat1.name}")  # Garfield
print(f"cat2.name = {cat2.name}")  # Tom

# ============ 类型注解 ============
print("\n=== 类型注解 ===")


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


p = Point(3.0, 4.0)
print(f"Point(3, 4).distance_from_origin() = {p.distance_from_origin()}")  # 5.0


if __name__ == "__main__":
    print("\n=== 类与对象基础总结 ===")
    print("1. 类定义使用 class 关键字")
    print("2. __init__ 是构造方法，用于初始化实例")
    print("3. self 指向当前实例，必须是实例方法的第一个参数")
    print("4. 类属性所有实例共享，实例属性每个实例独有")
    print("5. 实例方法通过 instance.method() 调用")
