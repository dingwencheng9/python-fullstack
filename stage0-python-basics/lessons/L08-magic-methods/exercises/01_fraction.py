"""L07 练习1: 创建一个分数类 Fraction

难度: ⭐⭐⭐ (进阶)
预计时间: 45 分钟
知识点: __init__、__repr__、__str__、__eq__、__add__ 等魔术方法

任务要求:
1. __init__(self, numerator, denominator) - 初始化分数
2. __repr__ - 返回类似 Fraction(1, 2) 的字符串
3. __str__ - 返回类似 1/2 的字符串
4. __eq__ - 判断两个分数是否相等（如 1/2 == 2/4）
5. __add__ - 分数相加

提示:
1. 约分使用最大公约数 (GCD)
2. from math import gcd 可计算 GCD
3. __repr__ 用于调试，__str__ 用于显示
"""

from math import gcd


class Fraction:
    """分数类"""

    def __init__(self, numerator: int, denominator: int) -> None:
        if denominator == 0:
            raise ValueError("分母不能为零")
        # 约分：使分子分母互质
        common = gcd(abs(numerator), abs(denominator))
        sign = -1 if numerator * denominator < 0 else 1
        self.numerator = sign * abs(numerator) // common
        self.denominator = abs(denominator) // common

    def __repr__(self) -> str:
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fraction):
            return False
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __add__(self, other: "Fraction") -> "Fraction":
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)


# 测试代码
if __name__ == "__main__":
    f1 = Fraction(1, 2)
    f2 = Fraction(2, 4)
    print(f"f1 = {f1}")  # 预期: 1/2
    print(f"f2 = {f2}")  # 预期: 1/2
    print(f"f1 == f2: {f1 == f2}")  # 预期: True

    f3 = Fraction(1, 3)
    f4 = Fraction(1, 6)
    print(f"f3 + f4 = {f3 + f4}")  # 预期: 1/2
