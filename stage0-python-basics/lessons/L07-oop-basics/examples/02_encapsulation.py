"""示例：封装

演示 Python 的封装特性：私有属性、受保护属性、@property。
"""

# ============ 私有属性 ============
print("=== 私有属性 ===")


class BankAccount:
    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner
        self.__balance = balance  # 私有属性（双下划线开头）

    def deposit(self, amount: float) -> None:
        """存款"""
        if amount > 0:
            self.__balance += amount
            print(f"存款 ${amount:.2f} 成功，当前余额 ${self.__balance:.2f}")

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount > self.__balance:
            print("余额不足")
            return False
        self.__balance -= amount
        print(f"取款 ${amount:.2f} 成功，当前余额 ${self.__balance:.2f}")
        return True

    def get_balance(self) -> float:
        """公开方法访问私有属性"""
        return self.__balance

    def __validate(self, amount: float) -> bool:
        """私有方法"""
        return amount > 0


account = BankAccount("Alice", 1000)
print(f"账户所有者: {account.owner}")
print(f"当前余额: ${account.get_balance():.2f}")

# 无法直接访问私有属性（名称改写机制）
# account.__balance  → AttributeError
print("尝试访问 account.__balance（不可见，Python 使用名称改写）")

# 私有属性会被名称改写
print(f"account._BankAccount__balance = {account._BankAccount__balance}")

# ============ @property 装饰器 ============
print("\n=== @property 装饰器 ===")


class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius  # 单下划线：约定私有

    @property
    def celsius(self) -> float:
        """获取摄氏温度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """设置摄氏温度（带验证）"""
        if value < -273.15:
            print("温度不能低于绝对零度，已设为 -273.15°C")
            self._celsius = -273.15
        else:
            self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """计算华氏温度（只读属性）"""
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        """计算开尔文温度（只读属性）"""
        return self._celsius + 273.15


temp = Temperature(25)
print(f"摄氏温度: {temp.celsius}°C")
print(f"华氏温度: {temp.fahrenheit}°F")
print(f"开尔文温度: {temp.kelvin}K")

# 使用 setter
temp.celsius = 30
print(f"设置后摄氏温度: {temp.celsius}°C")

# 验证 setter
temp.celsius = -300
print(f"验证后摄氏温度: {temp.celsius}°C")

# ============ 受保护属性 ============
print("\n=== 受保护属性 ===")


class User:
    def __init__(self, username: str, email: str) -> None:
        self.username = username
        self._email = email  # 受保护：约定不应直接访问
        self.__password = "default"  # 私有

    def update_email(self, new_email: str) -> None:
        """公开方法更新邮箱"""
        if "@" in new_email and "." in new_email:
            self._email = new_email
            print(f"邮箱已更新为: {new_email}")
        else:
            print("无效的邮箱格式")

    def get_email(self) -> str:
        """公开方法获取邮箱"""
        return self._email


user = User("alice", "alice@example.com")
print(f"用户名: {user.username}")
print(f"邮箱: {user.get_email()}")

# 受保护属性仍可直接访问（但不推荐）
print(f"直接访问 _email: {user._email}")

user.update_email("alice@newdomain.com")

# ============ 完整示例：SecureBankAccount ============
print("\n=== 完整示例：银行账户 ===")


class SecureBankAccount:
    """更安全的银行账户类"""

    def __init__(self, owner: str, initial_balance: float = 0) -> None:
        self.owner = owner
        self.__balance = initial_balance
        self.__transaction_history: list[str] = []

    @property
    def balance(self) -> float:
        """获取余额（只读）"""
        return self.__balance

    @property
    def transaction_count(self) -> int:
        """获取交易次数"""
        return len(self.__transaction_history)

    def deposit(self, amount: float) -> None:
        """存款"""
        if amount <= 0:
            print("存款金额必须为正数")
            return
        self.__balance += amount
        self.__transaction_history.append(f"+{amount}")

    def withdraw(self, amount: float) -> bool:
        """取款"""
        if amount <= 0:
            print("取款金额必须为正数")
            return False
        if amount > self.__balance:
            print("余额不足")
            return False
        self.__balance -= amount
        self.__transaction_history.append(f"-{amount}")
        return True

    def get_history(self) -> list[str]:
        """获取交易历史"""
        return self.__transaction_history.copy()


# 使用
acc = SecureBankAccount("Bob", 5000)
print(f"余额: ${acc.balance:.2f}")
acc.deposit(1000)
acc.withdraw(500)
print(f"余额: ${acc.balance:.2f}")
print(f"交易次数: {acc.transaction_count}")
print(f"交易历史: {acc.get_history()}")


if __name__ == "__main__":
    print("\n=== 封装总结 ===")
    print("1. _protected: 受保护属性，约定不直接访问")
    print("2. __private: 私有属性，名称会被改写")
    print("3. @property: 提供受控的属性访问方式")
    print("4. getter/setter: 通过方法验证和保护数据")
