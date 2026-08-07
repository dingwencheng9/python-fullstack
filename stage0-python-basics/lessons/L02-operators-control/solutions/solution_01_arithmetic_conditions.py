"""参考答案 1: 算术运算符与条件语句

对应练习: exercises/01_arithmetic_conditions.py
知识点: 算术运算符、比较运算符、if/elif/else 多分支

本参考答案为演示型练习的完整实现版本。
"""

# ============================================================
# BMI 计算器
# ============================================================
def calculate_bmi(weight, height):
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
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        return (round(bmi, 2), '偏瘦')
    elif bmi < 24:
        return (round(bmi, 2), '正常')
    elif bmi < 28:
        return (round(bmi, 2), '偏胖')
    else:
        return (round(bmi, 2), '肥胖')


def calculate_grade(score):
    """根据分数返回等级。

    Args:
        score: 分数（0-100）

    Returns:
        等级: S/A/B/C/D
    """
    if score >= 90:
        return 'S'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    else:
        return 'D'


if __name__ == '__main__':
    print('=== BMI 计算器测试 ===')
    test_cases = [
        (70, 1.75, (22.86, '正常')),
        (50, 1.6, (19.53, '正常')),
        (90, 1.7, (31.14, '肥胖')),
        (45, 1.8, (13.89, '偏瘦')),
    ]
    for weight, height, expected in test_cases:
        result = calculate_bmi(weight, height)
        status = '✓' if abs(result[0] - expected[0]) < 0.01 and result[1] == expected[1] else '✗'
        print(f'{status} 体重{weight}kg 身高{height}m → BMI={result[0]:.2f} ({result[1]})')

    print('\n=== 成绩等级测试 ===')
    grade_tests = [(95, 'S'), (88, 'A'), (75, 'B'), (65, 'C'), (45, 'D')]
    for score, expected in grade_tests:
        result = calculate_grade(score)
        status = '✓' if result == expected else '✗'
        print(f'{status} 分数{score} → 等级{result}')
