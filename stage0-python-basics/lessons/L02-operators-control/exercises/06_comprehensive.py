"""L02 练习6: 综合练习 - 运算符与控制流

难度: ⭐⭐⭐ (进阶)
预计时间: 40 分钟
知识点: 算术运算符、逻辑运算符、循环、条件语句综合应用

任务描述:
综合练习：本练习整合了运算符与控制流的核心知识点，包括 FizzBuzz、素数判断、数字统计等经典问题。

提示:
1. FizzBuzz: 先判断 15 的倍数，再判断 3 和 5
2. 素数判断: 只需检查到 sqrt(n) 即可
3. 注意边界条件 (如 n <= 1)
"""


def fizzbuzz(n: int) -> list[str]:
    """FizzBuzz 游戏实现。

    规则：
    - 3 的倍数 → "Fizz"
    - 5 的倍数 → "Buzz"
    - 3 和 5 的倍数 → "FizzBuzz"
    - 其他 → 数字本身（转为字符串）

    Args:
        n: 最大数字（包含）

    Returns:
        FizzBuzz 结果列表

    Examples:
        >>> fizzbuzz(15)
        ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz',
         'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']
    """
    if n < 1:
        return []
    res: list[str] = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            res.append("FizzBuzz")
        elif i % 3 == 0:
            res.append("Fizz")
        elif i % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(i))
    return res


def is_prime(n: int) -> bool:
    """判断素数。

    Args:
        n: 待判断的正整数

    Returns:
        True 表示素数，False 表示非素数

    Examples:
        >>> is_prime(7)
        True
        >>> is_prime(4)
        False
        >>> is_prime(1)
        False
        >>> is_prime(2)
        True
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def calculator(a: float, b: float, operator: str) -> float | None:
    """简易计算器。

    Args:
        a: 第一个操作数
        b: 第二个操作数
        operator: 运算符（+, -, *, /, //, %, **）

    Returns:
        计算结果，除数为零时返回 None

    Examples:
        >>> calculator(10, 3, '+')
        13.0
        >>> calculator(10, 3, '/')
        3.3333333333333335
        >>> calculator(10, 0, '/')
        None
        >>> calculator(2, 3, '**')
        8.0
    """
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        try:
            return a / b
        except Exception:
            return None
    if operator == "//":
        try:
            return a // b
        except Exception:
            return None
    if operator == "%":
        try:
            return a % b
        except Exception:
            return None
    if operator == "**":
        return a ** b
    raise ValueError(f"unsupported operator: {operator}")


def calculate_total_price(price: float, quantity: int, discount_percent: float = 0, tax_percent: float = 0) -> float:
    """计算商品总价（含折扣和税）。

    Args:
        price: 单价
        quantity: 数量
        discount_percent: 折扣百分比（0-100）
        tax_percent: 税率百分比（0-100）

    Returns:
        最终价格（四舍五入到两位小数）

    Examples:
        >>> calculate_total_price(100, 2)
        200.0
        >>> calculate_total_price(100, 2, discount_percent=10)
        180.0
        >>> calculate_total_price(100, 2, tax_percent=13)
        226.0
    """
    subtotal = price * quantity
    discounted = subtotal * (1 - max(0.0, min(discount_percent, 100.0)) / 100.0)
    taxed = discounted * (1 + max(0.0, tax_percent) / 100.0)
    return round(taxed, 2)


# ==================== 测试代码 ====================
if __name__ == "__main__":
    print("=== FizzBuzz 测试 ===")
    result = fizzbuzz(15)
    expected = [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
    ]
    status = "✓" if result == expected else "✗"
    print(f"{status} fizzbuzz(15) = {result[:5]}... (前5个)")

    print("\n=== 素数判断测试 ===")
    tests = [(7, True), (4, False), (1, False), (2, True), (17, True), (25, False), (0, False)]
    for n, expected in tests:
        result = is_prime(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} is_prime({n}) = {result}")

    print("\n=== 计算器测试 ===")
    tests = [
        (10, 3, "+", 13.0),
        (10, 3, "-", 7.0),
        (10, 3, "*", 30.0),
        (10, 3, "/", 3.3333333333333335),
        (10, 0, "/", None),
        (2, 3, "**", 8.0),
        (17, 3, "//", 5.0),
        (17, 3, "%", 2.0),
    ]
    for a, b, op, expected in tests:
        result = calculator(a, b, op)
        if expected is None:
            status = "✓" if result is None else "✗"
        else:
            status = "✓" if abs(result - expected) < 0.0001 else "✗"
        print(f"{status} calculator({a}, {b}, '{op}') = {result}")

    print("\n=== 价格计算测试 ===")
    tests = [
        (100, 2, 0, 0, 200.0),
        (100, 2, 10, 0, 180.0),
        (100, 2, 0, 13, 226.0),
        (99, 3, 5, 10, 282.615),
    ]
    for price, qty, discount, tax, expected in tests:
        result = calculate_total_price(price, qty, discount, tax)
        status = "✓" if abs(result - expected) < 0.01 else "✗"
        print(f"{status} ({price}×{qty}, -{discount}%, +{tax}%) = {result}")
