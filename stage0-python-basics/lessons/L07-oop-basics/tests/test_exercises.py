"""L07 面向对象基础 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
"""

import importlib.util
from pathlib import Path

import pytest


EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def oop_basics_module():
    """加载 exercises/01_oop_basics.py"""
    return _load_exercise_module("_test_oop_basics", EXERCISES_DIR / "01_oop_basics.py")


@pytest.fixture(scope="module")
def inheritance_module():
    """加载 exercises/02_inheritance_practice.py"""
    return _load_exercise_module("_test_inheritance", EXERCISES_DIR / "02_inheritance_practice.py")


@pytest.fixture(scope="module")
def property_module():
    """加载 exercises/03_property_practice.py"""
    return _load_exercise_module("_test_property", EXERCISES_DIR / "03_property_practice.py")


# ============================================================
# 01_oop_basics.py 测试
# ============================================================


class TestPersonClass:
    """测试 Person 类"""

    def test_person_creation(self, oop_basics_module) -> None:
        """测试 Person 对象创建"""
        cls = getattr(oop_basics_module, "Person", None)
        assert cls is not None, "请定义 Person 类"

        person = cls("Alice", 25)
        assert person.name == "Alice"
        assert person.age == 25

    def test_person_introduce(self, oop_basics_module) -> None:
        """测试自我介绍"""
        cls = getattr(oop_basics_module, "Person", None)
        person = cls("Bob", 30)
        assert "Bob" in person.introduce()
        assert "30" in person.introduce()

    def test_person_birthday(self, oop_basics_module) -> None:
        """测试生日"""
        cls = getattr(oop_basics_module, "Person", None)
        person = cls("Charlie", 25)
        person.birthday()
        assert person.age == 26


class TestBankAccountClass:
    """测试 BankAccount 类"""

    def test_account_initialization(self, oop_basics_module) -> None:
        """测试账户初始化"""
        cls = getattr(oop_basics_module, "BankAccount", None)
        assert cls is not None, "请定义 BankAccount 类"

        account = cls("Alice", 1000)
        assert account.owner == "Alice"
        assert account.balance == 1000

    def test_account_deposit(self, oop_basics_module) -> None:
        """测试存款"""
        cls = getattr(oop_basics_module, "BankAccount", None)
        account = cls("Alice", 100)
        assert account.deposit(500) is True
        assert account.balance == 600

    def test_account_withdraw(self, oop_basics_module) -> None:
        """测试取款"""
        cls = getattr(oop_basics_module, "BankAccount", None)
        account = cls("Alice", 500)
        assert account.withdraw(200) is True
        assert account.balance == 300

    def test_account_withdraw_insufficient(self, oop_basics_module) -> None:
        """测试余额不足"""
        cls = getattr(oop_basics_module, "BankAccount", None)
        account = cls("Alice", 100)
        assert account.withdraw(200) is False
        assert account.balance == 100


class TestRectangleClass:
    """测试 Rectangle 类"""

    def test_rectangle_area(self, oop_basics_module) -> None:
        """测试矩形面积"""
        cls = getattr(oop_basics_module, "Rectangle", None)
        assert cls is not None, "请定义 Rectangle 类"

        rect = cls(5, 10)
        assert rect.area() == 50

    def test_rectangle_perimeter(self, oop_basics_module) -> None:
        """测试矩形周长"""
        cls = getattr(oop_basics_module, "Rectangle", None)
        rect = cls(5, 10)
        assert rect.perimeter() == 30


class TestVectorClass:
    """测试 Vector 类"""

    def test_vector_creation(self, oop_basics_module) -> None:
        """测试向量创建"""
        cls = getattr(oop_basics_module, "Vector", None)
        assert cls is not None, "请定义 Vector 类"

        v = cls(3.0, 4.0)
        assert v.x == 3.0
        assert v.y == 4.0

    def test_vector_length(self, oop_basics_module) -> None:
        """测试向量长度"""
        cls = getattr(oop_basics_module, "Vector", None)
        v = cls(3.0, 4.0)
        assert abs(v.length() - 5.0) < 0.001

    def test_vector_dot(self, oop_basics_module) -> None:
        """测试向量点积"""
        cls = getattr(oop_basics_module, "Vector", None)
        v1 = cls(1.0, 2.0)
        v2 = cls(3.0, 4.0)
        assert v1.dot(v2) == 11.0  # 1*3 + 2*4 = 11


# ============================================================
# 02_inheritance_practice.py 测试
# ============================================================


class TestInheritance:
    """测试继承"""

    def test_vehicle_base_class(self, inheritance_module) -> None:
        """测试 Vehicle 基类"""
        cls = getattr(inheritance_module, "Vehicle", None)
        assert cls is not None, "请定义 Vehicle 类"

        vehicle = cls("Toyota", 120)
        assert vehicle.brand == "Toyota"
        assert vehicle.speed == 120

    def test_car_inheritance(self, inheritance_module) -> None:
        """测试 Car 子类"""
        cls = getattr(inheritance_module, "Car", None)
        assert cls is not None, "请定义 Car 类"

        car = cls("Toyota", 120, 4, 4)
        assert car.brand == "Toyota"
        assert car.doors == 4
        assert "Car" in car.drive()

    def test_truck_inheritance(self, inheritance_module) -> None:
        """测试 Truck 子类"""
        cls = getattr(inheritance_module, "Truck", None)
        assert cls is not None, "请定义 Truck 类"

        truck = cls("Volvo", 90, 20.0)
        assert truck.brand == "Volvo"
        assert truck.max_load == 20.0

    def test_truck_load_cargo(self, inheritance_module) -> None:
        """测试卡车载货"""
        cls = getattr(inheritance_module, "Truck", None)
        truck = cls("Volvo", 90, 20.0)

        assert truck.load_cargo(5.0) is True
        assert truck.current_load == 5.0

        # 超载应返回 False
        assert truck.load_cargo(20.0) is False

    def test_drive_all_polymorphism(self, inheritance_module) -> None:
        """测试多态函数 drive_all"""
        func = getattr(inheritance_module, "drive_all", None)
        assert func is not None, "请定义 drive_all 函数"

        car_cls = getattr(inheritance_module, "Car", None)
        truck_cls = getattr(inheritance_module, "Truck", None)
        vehicle_cls = getattr(inheritance_module, "Vehicle", None)

        if all([car_cls, truck_cls, vehicle_cls]):
            car = car_cls("Toyota", 120, 4, 4)
            truck = truck_cls("Volvo", 90, 20.0)
            vehicles = [car, truck]
            results = func(vehicles)
            assert len(results) == 2


# ============================================================
# 03_property_practice.py 测试
# ============================================================


class TestStudentProperty:
    """测试 Student 类 @property"""

    def test_student_name_readonly(self, property_module) -> None:
        """测试 name 属性只读"""
        cls = getattr(property_module, "Student", None)
        assert cls is not None, "请定义 Student 类"

        student = cls("Alice", 85)
        assert student.name == "Alice"

    def test_student_score_validation(self, property_module) -> None:
        """测试 score 属性验证"""
        cls = getattr(property_module, "Student", None)
        student = cls("Bob", 85)

        # 有效范围
        student.score = 90
        assert student.score == 90

        # 超出范围应抛异常
        with pytest.raises(ValueError, match="0.*100"):
            student.score = 150

    def test_student_grade(self, property_module) -> None:
        """测试 grade 计算属性"""
        cls = getattr(property_module, "Student", None)

        s1 = cls("A", 95)
        assert s1.grade == "A"

        s2 = cls("B", 65)
        assert s2.grade == "D"

    def test_student_pass_status(self, property_module) -> None:
        """测试 pass_status 计算属性"""
        cls = getattr(property_module, "Student", None)

        passing = cls("A", 75)
        assert "及格" in passing.pass_status

        failing = cls("B", 45)
        assert "不及格" in failing.pass_status


class TestTemperatureProperty:
    """测试 Temperature 类 @property"""

    def test_temperature_conversion(self, property_module) -> None:
        """测试摄氏/华氏转换"""
        cls = getattr(property_module, "Temperature", None)
        assert cls is not None, "请定义 Temperature 类"

        temp = cls(25)
        assert abs(temp.fahrenheit - 77.0) < 0.1

    def test_temperature_fahrenheit_setter(self, property_module) -> None:
        """测试设置华氏温度"""
        cls = getattr(property_module, "Temperature", None)
        temp = cls(0)
        temp.fahrenheit = 32
        assert abs(temp.celsius - 0) < 0.1
