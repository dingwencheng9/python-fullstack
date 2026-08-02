"""Money 类参考答案 - 演示数值运算魔法方法"""


class Money:
    """货币类，支持加减运算"""

    def __init__(self, dollars: int, cents: int = 0) -> None:
        # 先计算总 cents 数（处理进位）
        total_cents = dollars * 100 + cents
        if total_cents < 0:
            raise ValueError("金额不能为负")
        self._dollars = total_cents // 100
        self._cents = total_cents % 100

    @property
    def dollars(self) -> int:
        return self._dollars

    @property
    def cents(self) -> int:
        return self._cents

    def __repr__(self) -> str:
        return f"Money({self._dollars}, {self._cents:02d})"

    def __str__(self) -> str:
        return f"${self._dollars}.{self._cents:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self._dollars == other._dollars and self._cents == other._cents

    def __hash__(self) -> int:
        return hash((self._dollars, self._cents))

    def __add__(self, other: "Money") -> "Money":
        """加法"""
        total_cents = self._dollars * 100 + self._cents
        total_cents += other._dollars * 100 + other._cents
        return Money(0, total_cents)

    def __sub__(self, other: "Money") -> "Money":
        """减法"""
        total_cents = self._dollars * 100 + self._cents
        total_cents -= other._dollars * 100 + other._cents
        if total_cents < 0:
            raise ValueError("余额不能为负")
        return Money(0, total_cents)

    def __mul__(self, multiplier: float) -> "Money":
        """标量乘法"""
        if multiplier < 0:
            raise ValueError("乘数必须为正")
        total_cents = (self._dollars * 100 + self._cents) * multiplier
        return Money(0, int(total_cents))
