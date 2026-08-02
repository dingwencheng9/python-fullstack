"""示例：继承

演示 Python 的继承机制：单继承、多重继承、方法重写、super()。
"""

# ============ 基本继承 ============
print("=== 基本继承 ===")


class Animal:
    """动物基类"""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "Some sound"

    def move(self) -> str:
        return f"{self.name} is moving"


class Dog(Animal):
    """狗类继承自动物类"""

    def speak(self) -> str:
        """重写父类方法"""
        return f"{self.name} says Woof!"


class Cat(Animal):
    """猫类继承自动物类"""

    def speak(self) -> str:
        return f"{self.name} says Meow!"


dog = Dog("Buddy")
cat = Cat("Whiskers")

print(f"dog.speak() = {dog.speak()}")  # "Buddy says Woof!"
print(f"dog.move() = {dog.move()}")  # "Buddy is moving"（继承的方法）
print(f"cat.speak() = {cat.speak()}")  # "Whiskers says Meow!"

# ============ super() 调用父类 ============
print("\n=== super() 调用父类 ===")


class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    def get_info(self) -> str:
        return f"{self.name}: ${self.salary}"


class Manager(Employee):
    def __init__(self, name: str, salary: float, department: str) -> None:
        super().__init__(name, salary)  # 调用父类构造方法
        self.department = department

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info}, Dept: {self.department}"

    def get_department(self) -> str:
        return f"{self.name} manages {self.department}"


manager = Manager("Alice", 80000, "Engineering")
print(manager.get_info())  # "Alice: $80000, Dept: Engineering"
print(manager.get_department())  # "Alice manages Engineering"

# ============ 多重继承 ============
print("\n=== 多重继承 ===")


class Flyable:
    def __init__(self) -> None:
        self.altitude = 0

    def fly(self) -> str:
        self.altitude = 100
        return "Flying in the sky"


class Swimmable:
    def __init__(self) -> None:
        self.depth = 0

    def swim(self) -> str:
        self.depth = 5
        return "Swimming in water"


class Duck(Flyable, Swimmable):
    """鸭子既能飞又能游"""

    def __init__(self) -> None:
        Flyable.__init__(self)
        Swimmable.__init__(self)
        self.name = "Duck"

    def quack(self) -> str:
        return "Quack!"

    def describe(self) -> str:
        return f"{self.name}: altitude={self.altitude}, depth={self.depth}"


duck = Duck()
print(f"duck.fly() = {duck.fly()}")
print(f"duck.swim() = {duck.swim()}")
print(f"duck.quack() = {duck.quack()}")
print(f"duck.describe() = {duck.describe()}")

# ============ 方法解析顺序（MRO） ============
print("\n=== 方法解析顺序（MRO） ===")


class A:
    def greet(self) -> str:
        return "Hello from A"


class B(A):
    def greet(self) -> str:
        return "Hello from B"


class C(A):
    def greet(self) -> str:
        return "Hello from C"


class D(B, C):
    def greet(self) -> str:
        return "Hello from D"


d = D()
print(f"d.greet() = {d.greet()}")  # "Hello from D"
print(f"D.__mro__ = {D.__mro__}")  # 方法解析顺序


# ============ 继承中的 isinstance 和 issubclass ============
print("\n=== isinstance 和 issubclass ===")

print(f"isinstance(dog, Dog) = {isinstance(dog, Dog)}")
print(f"isinstance(dog, Animal) = {isinstance(dog, Animal)}")
print(f"issubclass(Dog, Animal) = {issubclass(Dog, Animal)}")
print(f"issubclass(Dog, object) = {issubclass(Dog, object)}")

# ============ 完整示例：几何形状 ============
print("\n=== 完整示例：几何形状继承体系 ===")


class Shape:
    """几何形状基类"""

    def __init__(self, name: str) -> None:
        self.name = name

    def area(self) -> float:
        """子类必须实现此方法"""
        # raise TypeError: 子类必须实现 area() 方法  # L08 将学到

    def perimeter(self) -> float:
        """子类必须实现此方法"""
        # raise TypeError: 子类必须实现 perimeter() 方法  # L08 将学到


class Rectangle(Shape):
    """矩形类"""

    def __init__(self, width: float, height: float) -> None:
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    """圆形类"""

    def __init__(self, radius: float) -> None:
        super().__init__("Circle")
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius**2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Square(Rectangle):
    """正方形类"""

    def __init__(self, side: float) -> None:
        super().__init__(side, side)


# 使用
shapes: list[Shape] = [
    Rectangle(5, 10),
    Circle(7),
    Square(4),
]

for shape in shapes:
    print(f"{shape}: area={shape.area():.2f}, perimeter={shape.perimeter():.2f}")


if __name__ == "__main__":
    print("\n=== 继承总结 ===")
    print("1. 单继承: class Child(Parent):")
    print("2. 多重继承: class Child(Parent1, Parent2):")
    print("3. super(): 调用父类方法")
    print("4. 方法重写: 子类覆盖父类方法")
    print("5. MRO: 方法解析顺序决定了多继承时的查找路径")
