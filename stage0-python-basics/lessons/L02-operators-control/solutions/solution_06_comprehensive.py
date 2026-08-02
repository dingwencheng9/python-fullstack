"""参考答案 6: 综合练习 - 运算符与控制流"""


def fizzbuzz(n: int) -> list:
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
    # 实现 FizzBuzz
    # 综合运用: 算术运算符(%), 逻辑运算符, 条件语句
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:  # 3 和 5 的倍数
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


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
    # 素数定义: 大于 1 的自然数，除了 1 和它本身外，不能被其他自然数整除
    # 优化: 只需检查到 sqrt(n)
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # 只需检查到 sqrt(n)
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
    # 使用 match-case 实现计算器
    match operator:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            if b == 0:
                return None
            return a / b
        case "//":
            if b == 0:
                return None
            return a // b
        case "%":
            if b == 0:
                return None
            return a % b
        case "**":
            return a**b
        case _:
            return None


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
    # 实现价格计算
    # 1. 计算小计: price * quantity
    subtotal = price * quantity
    # 2. 计算折后价: 小计 * (1 - discount_percent / 100)
    discounted = subtotal * (1 - discount_percent / 100)
    # 3. 计算含税价: 折后价 * (1 + tax_percent / 100)
    total = discounted * (1 + tax_percent / 100)
    # 4. 四舍五入到两位小数
    return round(total, 2)


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
