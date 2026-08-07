"""参考答案 6: 综合练习 - 运算符与控制流

对应练习: exercises/06_comprehensive.py
知识点: 算术运算符、逻辑运算符、循环、条件语句综合应用

本参考答案为演示型练习的完整实现版本。
"""


def fizzbuzz(n):
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
    """
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append('FizzBuzz')
        elif i % 3 == 0:
            result.append('Fizz')
        elif i % 5 == 0:
            result.append('Buzz')
        else:
            result.append(str(i))
    return result


def is_prime(n):
    """判断素数。

    Args:
        n: 待判断的正整数

    Returns:
        True 表示素数，False 表示非素数
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def calculator(a, b, operator):
    """简易计算器。

    Args:
        a: 第一个操作数
        b: 第二个操作数
        operator: 运算符（+, -, *, /, //, %, **）

    Returns:
        计算结果，除数为零时返回 None
    """
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            return None
        return a / b
    elif operator == '//':
        if b == 0:
            return None
        return a // b
    elif operator == '%':
        if b == 0:
            return None
        return a % b
    elif operator == '**':
        return a ** b
    else:
        return None


def calculate_total_price(price, quantity, discount_percent=0, tax_percent=0):
    """计算商品总价（含折扣和税）。

    Args:
        price: 单价
        quantity: 数量
        discount_percent: 折扣百分比（0-100）
        tax_percent: 税率百分比（0-100）

    Returns:
        最终价格
    """
    subtotal = price * quantity
    discount = subtotal * (discount_percent / 100)
    after_discount = subtotal - discount
    tax = after_discount * (tax_percent / 100)
    return round(after_discount + tax, 2)


if __name__ == '__main__':
    print('=== FizzBuzz 测试 ===')
    result = fizzbuzz(15)
    print(result)

    print('\n=== 素数判断测试 ===')
    for i in range(1, 21):
        status = '素数' if is_prime(i) else '  '
        print(f'{i}: {status}')

    print('\n=== 计算器测试 ===')
    tests = [
        (10, 3, '+', 13.0),
        (10, 3, '-', 7.0),
        (10, 3, '*', 30.0),
        (10, 3, '/', 3.3333333333333335),
        (10, 0, '/', None),
        (2, 3, '**', 8.0),
    ]
    for a, b, op, expected in tests:
        result = calculator(a, b, op)
        if expected is None:
            status = '✓' if result is None else '✗'
        else:
            status = '✓' if abs(result - expected) < 0.0001 else '✗'
        print(f'{status} calculator({a}, {b}, \'{op}\') = {result}')

    print('\n=== 价格计算测试 ===')
    print(f'100 x 2 = {calculate_total_price(100, 2)}')
    print(f'100 x 2, 10%折扣 = {calculate_total_price(100, 2, 10)}')
    print(f'100 x 2, 13%税 = {calculate_total_price(100, 2, 0, 13)}')
