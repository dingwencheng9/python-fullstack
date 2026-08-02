"""测试 L06 OOP 基础课程

测试类与对象、封装、继承、多态。
注意：魔术方法（__str__、__repr__ 等）在 L07 中学习。
"""

import pytest


class TestClassBasics:
    """测试类与对象基础"""

    def test_person_class(self) -> None:
        """测试 Person 类"""
        from solutions import Person

        person = Person("Alice", 25)
        assert person.name == "Alice"
        assert person.age == 25
        assert "Alice" in person.introduce()
        assert "25" in person.introduce()

    def test_person_birthday(self) -> None:
        """测试 Person 生日"""
        from solutions import Person

        person = Person("Bob", 30)
        person.birthday()
        assert person.age == 31

    def test_bank_account_initialization(self) -> None:
        """测试 BankAccount 初始化"""
        from solutions import BankAccount

        account = BankAccount("Alice", 1000)
        assert account.owner == "Alice"
        assert account.balance == 1000

    def test_bank_account_default_balance(self) -> None:
        """测试 BankAccount 默认余额"""
        from solutions import BankAccount

        account = BankAccount("Bob")
        assert account.balance == 0

    def test_bank_account_deposit(self) -> None:
        """测试存款"""
        from solutions import BankAccount

        account = BankAccount("Alice", 100)
        assert account.deposit(500) is True
        assert account.balance == 600

    def test_bank_account_deposit_negative(self) -> None:
        """测试负数存款被拒绝"""
        from solutions import BankAccount

        account = BankAccount("Alice", 100)
        assert account.deposit(-50) is False
        assert account.balance == 100

    def test_bank_account_withdraw(self) -> None:
        """测试取款"""
        from solutions import BankAccount

        account = BankAccount("Alice", 500)
        assert account.withdraw(200) is True
        assert account.balance == 300

    def test_bank_account_withdraw_insufficient(self) -> None:
        """测试余额不足"""
        from solutions import BankAccount

        account = BankAccount("Alice", 100)
        assert account.withdraw(200) is False
        assert account.balance == 100

    def test_bank_account_private_balance(self) -> None:
        """测试私有属性通过 property 访问（约定访问）"""
        from solutions import BankAccount

        account = BankAccount("Alice", 1000)
        # balance 是只读属性，通过 property 访问（推荐方式）
        assert account.balance == 1000
        # 注意：Python 的 name mangling 不是真正的访问控制
        # 私有属性技术上可以通过 _ClassName__attrname 访问（不推荐）


class TestEncapsulation:
    """测试封装"""

    def test_rectangle_creation(self) -> None:
        """测试 Rectangle 创建"""
        from solutions import Rectangle

        rect = Rectangle(5, 10)
        assert rect.width == 5
        assert rect.height == 10

    def test_rectangle_area(self) -> None:
        """测试矩形面积"""
        from solutions import Rectangle

        rect = Rectangle(4, 5)
        assert rect.area() == 20

    def test_rectangle_perimeter(self) -> None:
        """测试矩形周长"""
        from solutions import Rectangle

        rect = Rectangle(4, 5)
        assert rect.perimeter() == 18

    def test_rectangle_invalid_dimensions(self) -> None:
        """测试无效尺寸"""
        from solutions import Rectangle

        with pytest.raises(ValueError):
            Rectangle(-1, 5)
        with pytest.raises(ValueError):
            Rectangle(5, 0)


class TestInheritance:
    """测试继承"""

    def test_animal_base(self) -> None:
        """测试 Animal 基类"""
        from solutions import Animal

        animal = Animal("Generic")
        assert animal.name == "Generic"
        assert "Generic" in animal.move()

    def test_dog_inheritance(self) -> None:
        """测试 Dog 继承 Animal"""
        from solutions import Dog

        dog = Dog("Buddy")
        assert dog.name == "Buddy"
        assert "Woof" in dog.speak()
        # 继承的方法
        assert "Buddy" in dog.move()

    def test_cat_inheritance(self) -> None:
        """测试 Cat 继承 Animal"""
        from solutions import Cat

        cat = Cat("Whiskers")
        assert cat.name == "Whiskers"
        assert "Meow" in cat.speak()

    def test_polymorphism_shapes(self) -> None:
        """测试多态 - 形状"""
        from solutions import Rectangle

        rect = Rectangle(3, 4)
        # 多态：不同对象有相同的方法
        area = rect.area()
        assert area == 12


class TestPropertyDecorator:
    """测试 @property 装饰器（L06 核心特性）"""

    def test_temperature_celsius(self) -> None:
        """测试 Temperature 摄氏温度属性"""
        from solutions import Temperature

        temp = Temperature(25)
        assert temp.celsius == 25

    def test_temperature_fahrenheit(self) -> None:
        """测试 Temperature 华氏温度属性"""
        from solutions import Temperature

        temp = Temperature(0)
        assert temp.fahrenheit == 32.0
        temp2 = Temperature(100)
        assert temp2.fahrenheit == 212.0

    def test_temperature_fahrenheit_setter(self) -> None:
        """测试 Temperature 华氏温度 setter"""
        from solutions import Temperature

        temp = Temperature(25)
        temp.fahrenheit = 212  # 设置华氏温度
        assert abs(temp.celsius - 100) < 0.1  # 沸点

    def test_student_score_validation(self) -> None:
        """测试 Student 成绩验证"""
        from solutions import Student

        student = Student("Alice", 85)
        assert student.score == 85

    def test_student_score_invalid(self) -> None:
        """测试 Student 无效成绩被拒绝"""
        from solutions import Student

        with pytest.raises(ValueError):
            Student("Bob", 150)
        with pytest.raises(ValueError):
            Student("Carol", -10)


class TestVectorOop:
    """测试 Vector 类的 OOP 实现（L06 级别：普通方法，非魔术方法）"""

    def test_vector_creation(self) -> None:
        """测试 Vector 创建"""
        from solutions import Vector

        v = Vector(3, 4)
        assert v.x == 3
        assert v.y == 4

    def test_vector_length(self) -> None:
        """测试 Vector 长度（普通方法，非 __len__）"""
        from solutions import Vector

        # 3-4-5 直角三角形
        v = Vector(3, 4)
        assert v.length() == 5.0

        # 原点向量
        origin = Vector(0, 0)
        assert origin.length() == 0.0

        # 单位向量
        unit = Vector(1, 0)
        assert unit.length() == 1.0

    def test_vector_dot(self) -> None:
        """测试 Vector 点积"""
        from solutions import Vector

        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        assert v1.dot(v2) == 11  # 1*3 + 2*4

    def test_vector_scale(self) -> None:
        """测试 Vector 缩放（普通方法，非 __mul__）"""
        from solutions import Vector

        v = Vector(3, 4)
        result = v.scale(2)
        assert result.x == 6
        assert result.y == 8


class TestIntegration:
    """集成测试"""

    def test_bank_operations(self) -> None:
        """测试完整的银行操作"""
        from solutions import BankAccount

        account = BankAccount("Alice", 1000)
        assert account.balance == 1000

        # 多次存款
        account.deposit(500)
        account.deposit(300)
        assert account.balance == 1800

        # 多次取款
        account.withdraw(200)
        account.withdraw(100)
        assert account.balance == 1500

        # 尝试取款超过余额
        assert account.withdraw(2000) is False
        assert account.balance == 1500

    def test_person_aging(self) -> None:
        """测试人员年龄增长"""
        from solutions import Person

        person = Person("Bob", 20)

        for _ in range(5):
            person.birthday()

        assert person.age == 25
        assert "25" in person.introduce()
