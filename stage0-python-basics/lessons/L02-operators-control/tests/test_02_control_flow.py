"""测试 L02 Part 2: 控制流。"""


def test_if_statement():
    """测试 if 语句。"""
    x = 10
    result = "大于5" if x > 5 else "小于等于5"
    assert result == "大于5"


def test_if_elif_else():
    """测试 if/elif/else 语句。"""
    score = 85

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    assert grade == "B"


def test_while_loop():
    """测试 while 循环。"""
    count = 0
    total = 0

    while count < 5:
        total += count
        count += 1

    assert total == 10  # 0+1+2+3+4
    assert count == 5


def test_for_loop_range():
    """测试 for 循环与 range。"""
    total = 0
    for i in range(5):
        total += i

    assert total == 10  # 0+1+2+3+4


def test_for_loop_string():
    """测试遍历字符串。"""
    text = "hello"
    chars = []

    for char in text:
        chars.append(char)

    assert chars == ["h", "e", "l", "l", "o"]


def test_break_statement():
    """测试 break 语句。"""
    numbers = []

    for i in range(10):
        if i == 5:
            break
        numbers.append(i)

    assert numbers == [0, 1, 2, 3, 4]


def test_continue_statement():
    """测试 continue 语句。"""
    numbers = []

    for i in range(5):
        if i == 2:
            continue
        numbers.append(i)

    assert numbers == [0, 1, 3, 4]


def test_nested_loops():
    """测试嵌套循环。"""
    pairs = []

    for i in range(3):
        for j in range(2):
            pairs.append((i, j))

    assert pairs == [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]


def test_range_variations():
    """测试 range 的不同用法。"""
    # range(stop)
    assert list(range(5)) == [0, 1, 2, 3, 4]

    # range(start, stop)
    assert list(range(2, 5)) == [2, 3, 4]

    # range(start, stop, step)
    assert list(range(0, 10, 2)) == [0, 2, 4, 6, 8]

    # 负步长
    assert list(range(5, 0, -1)) == [5, 4, 3, 2, 1]


def test_conditional_expression():
    """测试三元表达式。"""
    x = 10
    result = "大" if x > 5 else "小"
    assert result == "大"

    x = 3
    result = "大" if x > 5 else "小"
    assert result == "小"


def test_while_with_break():
    """测试 while 循环中的 break。"""
    count = 0

    while True:
        count += 1
        if count >= 5:
            break

    assert count == 5


def test_nested_conditions():
    """测试嵌套条件。"""
    x = 10
    y = 20

    result = "both" if y > 15 else ("x only" if x > 5 else "neither")
    assert result == "both"
