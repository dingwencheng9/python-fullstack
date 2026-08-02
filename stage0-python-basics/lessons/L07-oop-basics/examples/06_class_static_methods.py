"""示例：类方法和静态方法

演示 Python 的实例方法、类方法和静态方法的区别和使用场景。
"""

from datetime import UTC, datetime
from typing import ClassVar

# ============ 三种方法对比 ============
print("=== 三种方法对比 ===")


class MyClass:
    class_var = "类变量"

    def __init__(self, value: int) -> None:
        self.instance_var = value

    def instance_method(self) -> str:
        """实例方法：可以访问实例和类属性"""
        return f"实例方法: self.instance_var={self.instance_var}, class_var={self.class_var}"

    @classmethod
    def class_method(cls) -> str:
        """类方法：可以访问类属性"""
        return f"类方法: class_var={cls.class_var}"

    @staticmethod
    def static_method() -> str:
        """静态方法：不访问实例或类"""
        return "静态方法: 不访问实例或类属性"


obj = MyClass(42)

# 实例方法需要实例调用
print(obj.instance_method())

# 类方法可以通过类或实例调用
print(MyClass.class_method())
print(obj.class_method())

# 静态方法可以通过类或实例调用
print(MyClass.static_method())
print(obj.static_method())

# ============ 类方法作为工厂方法 ============
# 注意：datetime 已在文件顶部导入，保持示例符合常规导入风格。
print("\n=== 类方法作为工厂方法 ===")


class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name: str, birth_year: int) -> "Person":
        """工厂方法：从出生年份创建实例"""
        age = datetime.now(UTC).date().year - birth_year
        return cls(name, age)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Person":
        """工厂方法：从字典创建实例"""
        return cls(data["name"], data["age"])

    @staticmethod
    def is_adult(age: int) -> bool:
        """静态方法：工具函数"""
        return age >= 18


# 使用工厂方法
p1 = Person("Alice", 25)
p2 = Person.from_birth_year("Bob", 1995)
p3 = Person.from_dict({"name": "Charlie", "age": 30})

print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"p3 = {p3}")
print(f"is_adult(20) = {Person.is_adult(20)}")
print(f"is_adult(16) = {Person.is_adult(16)}")

# ============ 静态方法作为工具函数 ============
print("\n=== 静态方法作为工具函数 ===")


class StringHelper:
    """字符串处理工具类"""

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """检查是否是回文"""
        return s == s[::-1]

    @staticmethod
    def reverse_words(s: str) -> str:
        """反转单词"""
        return " ".join(s.split()[::-1])

    @staticmethod
    def count_vowels(s: str) -> int:
        """计算元音字母数量"""
        vowels = "aeiouAEIOU"
        return sum(1 for c in s if c in vowels)


text = "racecar"
print(f"is_palindrome('{text}') = {StringHelper.is_palindrome(text)}")

text = "hello world"
print(f"reverse_words('{text}') = {StringHelper.reverse_words(text)}")

text = "Hello World"
print(f"count_vowels('{text}') = {StringHelper.count_vowels(text)}")

# ============ 类方法操作类属性 ============
print("\n=== 类方法操作类属性 ===")


class Bank:
    """银行类"""

    interest_rate = 0.05  # 类属性：利率
    total_accounts = 0  # 类属性：总账户数

    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner
        self.balance = balance
        Bank.total_accounts += 1  # 更新类属性

    @classmethod
    def set_interest_rate(cls, rate: float) -> None:
        """类方法：设置利率"""
        cls.interest_rate = rate

    @classmethod
    def get_interest_rate(cls) -> float:
        """类方法：获取利率"""
        return cls.interest_rate

    @classmethod
    def get_total_accounts(cls) -> int:
        """类方法：获取总账户数"""
        return cls.total_accounts

    def apply_interest(self) -> None:
        """实例方法：应用利息"""
        self.balance *= 1 + self.interest_rate


# 创建账户
acc1 = Bank("Alice", 1000)
acc2 = Bank("Bob", 2000)

print(f"总账户数: {Bank.get_total_accounts()}")
print(f"当前利率: {Bank.get_interest_rate()}")

# 修改利率
Bank.set_interest_rate(0.07)
print(f"新利率: {Bank.get_interest_rate()}")

# 应用利息
acc1.apply_interest()
print(f"Alice 账户余额（应用利息后）: {acc1.balance:.2f}")

# ============ 继承中的类方法 ============
print("\n=== 继承中的类方法 ===")


class Animal:
    species = "Unknown"

    @classmethod
    def get_species(cls) -> str:
        return f"Species: {cls.species}"


class Dog(Animal):
    species = "Canis familiaris"


class Cat(Animal):
    species = "Felis catus"


print(Animal.get_species())  # Species: Unknown
print(Dog.get_species())  # Species: Canis familiaris
print(Cat.get_species())  # Species: Felis catus

# ============ 完整示例：配置类 ============
print("\n=== 完整示例：配置类 ===")


class AppConfig:
    """应用配置类"""

    _instance: "AppConfig | None" = None  # 类属性：单例实例
    _config: ClassVar[dict[str, object]] = {
        "debug": False,
        "version": "1.0.0",
        "max_connections": 100,
    }

    def __new__(cls) -> "AppConfig":
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get(cls, key: str, default: object = None) -> object:
        """获取配置值"""
        return cls._config.get(key, default)

    @classmethod
    def set(cls, key: str, value: object) -> None:
        """设置配置值"""
        cls._config[key] = value

    @classmethod
    def all(cls) -> dict[str, object]:
        """获取所有配置"""
        return cls._config.copy()

    @classmethod
    def reset(cls) -> None:
        """重置配置（用于测试）"""
        cls._config = {
            "debug": False,
            "version": "1.0.0",
            "max_connections": 100,
        }


# 使用配置
config1 = AppConfig()
config2 = AppConfig()

print(f"config1 is config2: {config1 is config2}")  # True，单例
print(f"当前配置: {AppConfig.all()}")

AppConfig.set("debug", True)
print(f"debug 模式: {AppConfig.get('debug')}")


if __name__ == "__main__":
    print("\n=== 方法类型总结 ===")
    print("1. 实例方法: 需要 self，访问实例和类属性")
    print("2. 类方法: 需要 cls，访问类属性，工厂方法")
    print("3. 静态方法: 不需要参数，工具函数，分组组织")
    print()
    print("选择建议：")
    print("- 需要访问实例属性 → 实例方法")
    print("- 需要访问类属性/工厂方法 → 类方法")
    print("- 不需要访问实例/类属性 → 静态方法")
