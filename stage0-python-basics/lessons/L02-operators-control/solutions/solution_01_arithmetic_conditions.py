"""参考答案 1: 算术运算符与条件语句"""


def calculate_bmi(weight: float, height: float) -> tuple:
    """计算 BMI 并返回等级。

    Args:
        weight: 体重（公斤）
        height: 身高（米）

    Returns:
        (bmi值, 等级) 元组
        等级标准（中国标准）：
        - 偏瘦: BMI < 18.5
        - 正常: 18.5 <= BMI < 24
        - 偏胖: 24 <= BMI < 28
        - 肥胖: BMI >= 28

    Examples:
        >>> calculate_bmi(70, 1.75)
        (22.86, '正常')
        >>> calculate_bmi(80, 1.6)
        (31.25, '肥胖')
    """
    # BMI = 体重(kg) / 身高(m)^2
    bmi = weight / (height**2)

    # 根据 BMI 值返回对应等级
    if bmi < 18.5:
        category = "偏瘦"
    elif bmi < 24:
        category = "正常"
    elif bmi < 28:
        category = "偏胖"
    else:
        category = "肥胖"

    return (round(bmi, 2), category)


def calculate_grade(score: int) -> str:
    """根据分数返回等级。

    Args:
        score: 分数（0-100）

    Returns:
        等级: S/A/B/C/D

    Examples:
        >>> calculate_grade(95)
        'S'
        >>> calculate_grade(80)
        'B'
        >>> calculate_grade(45)
        'D'
    """
    # 标准:
    # - S: 90-100
    # - A: 80-89
    # - B: 70-79
    # - C: 60-69
    # - D: 0-59
    if score >= 90:
        return "S"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    return "D"


if __name__ == "__main__":
    # 测试 BMI
    print("=== BMI 计算器测试 ===")
    test_cases = [
        (70, 1.75, (22.86, "正常")),
        (50, 1.6, (19.53, "正常")),
        (90, 1.7, (31.14, "肥胖")),
        (45, 1.8, (13.89, "偏瘦")),
    ]

    for weight, height, expected in test_cases:
        result = calculate_bmi(weight, height)
        status = "✓" if abs(result[0] - expected[0]) < 0.01 and result[1] == expected[1] else "✗"
        print(f"{status} 体重{weight}kg 身高{height}m → BMI={result[0]:.2f} ({result[1]})")

    print("\n=== 成绩等级测试 ===")
    grade_tests = [(95, "S"), (88, "A"), (75, "B"), (65, "C"), (45, "D")]
    for score, expected in grade_tests:
        result = calculate_grade(score)
        status = "✓" if result == expected else "✗"
        print(f"{status} 分数{score} → 等级{result}")
