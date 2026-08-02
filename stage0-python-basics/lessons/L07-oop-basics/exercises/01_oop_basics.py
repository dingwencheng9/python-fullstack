"""L06 练习1: 面向对象基础

难度: ⭐⭐☆ (中等)
预计时间: 35 分钟
知识点: 类定义、__init__、继承、特殊方法

任务描述:
完成以下 5 个面向对象编程练习：
1. Person 类 - 基本属性和方法
2. BankAccount 类 - 封装和私有属性
3. Rectangle 类 - 计算方法和验证
4. Animal 继承层次 - 继承和方法重写
5. Vector 类 - 特殊方法实现

提示:
1. 使用 __init__ 初始化对象状态
2. 私有属性使用双下划线前缀 (如 __balance)
3. 继承时调用父类方法: super().__init__()
"""

# ============ 练习 1: Person 类 ============
# 创建一个 Person 类，包含姓名和年龄


class Person:
    """人员类"""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """自我介绍"""
        return f"我叫 {self.name}，今年 {self.age} 岁"

    def birthday(self) -> None:
        """过生日，年龄加一"""
        self.age += 1


# ============ 练习 2: BankAccount 类 ============
# 实现银行账户的存取款功能


class BankAccount:
    """银行账户类"""

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner
        self.__balance = balance  # 私有属性

    @property
    def balance(self) -> float:
        """获取余额（只读）"""
        return self.__balance

    def deposit(self, amount: float) -> bool:
        """存款"""
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True


# ============ 练习 3: Rectangle 类 ============
# 实现矩形类，支持面积和周长计算


class Rectangle:
    """矩形类"""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("宽和高必须为正数")
        self.width = width
        self.height = height

    def area(self) -> float:
        """计算面积"""
        return self.width * self.height

    def perimeter(self) -> float:
        """计算周长"""
        return 2 * (self.width + self.height)


# ============ 练习 4: 继承 - Animal 类层次 ============
class Animal:
    """动物基类"""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return "Some sound"

    def move(self) -> str:
        return f"{self.name} is moving"


class Dog(Animal):
    """狗类"""

    def speak(self) -> str:
        return f"{self.name} says Woof!"


class Cat(Animal):
    """猫类"""

    def speak(self) -> str:
        return f"{self.name} says Meow!"


# ============ 练习 5: Vector 类 ============
class Vector:
    """二维向量类

    提示：实例方法可以访问 self.x 和 self.y
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def length(self) -> float:
        """计算向量长度（勾股定理）"""
        return (self.x**2 + self.y**2) ** 0.5

    def dot(self, other: "Vector") -> float:
        """计算点积"""
        return self.x * other.x + self.y * other.y

    def scale(self, factor: float) -> "Vector":
        """缩放向量"""
        return Vector(self.x * factor, self.y * factor)


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== 练习测试 ===\n")

    # 测试 Person
    print("1. Person 类:")
    person = Person("Alice", 25)
    print(f"   {person.introduce()}")
    person.birthday()
    print(f"   生日后: {person.introduce()}")

    # 测试 BankAccount
    print("\n2. BankAccount 类:")
    account = BankAccount("Bob", 1000)
    account.deposit(500)
    print(f"   存款后余额: ${account.balance}")
    account.withdraw(300)
    print(f"   取款后余额: ${account.balance}")

    # 测试 Rectangle
    print("\n3. Rectangle 类:")
    rect = Rectangle(5, 10)
    print(f"   面积: {rect.area()}")
    print(f"   周长: {rect.perimeter()}")

    # 测试继承
    print("\n4. Animal 继承层次:")
    dog = Dog("Buddy")
    cat = Cat("Whiskers")
    print(f"   {dog.speak()}")
    print(f"   {cat.speak()}")
    print(f"   {dog.move()}")

    # 测试 Vector
    print("\n5. Vector 类:")
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"   v1.x={v1.x}, v1.y={v1.y}")
    print(f"   v2.x={v2.x}, v2.y={v2.y}")
    print(f"   v1.length() = {v1.length():.2f}")
    print(f"   v1.dot(v2) = {v1.dot(v2)}")
    v3 = v1.scale(2)
    print(f"   v1.scale(2) = ({v3.x}, {v3.y})")
