"""BankAccount 类参考答案"""


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
        """存款

        Args:
            amount: 存款金额

        Returns:
            是否成功
        """
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """取款

        Args:
            amount: 取款金额

        Returns:
            是否成功
        """
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
