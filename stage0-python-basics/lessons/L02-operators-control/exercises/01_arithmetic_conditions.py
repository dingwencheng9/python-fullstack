"""L02 练习1: 算术运算符与条件语句

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: 算术运算符、比较运算符、if/elif/else 多分支

任务描述:
练习 BMI（身体质量指数）计算器，综合运用：
- 算术运算符（/, **）
- 比较运算符（<, >, <=, >=）
- if/elif/else 多分支

提示:
1. BMI 公式: 体重(kg) / 身高(m)^2
2. 使用 if/elif/else 判断 BMI 范围
3. 注意浮点数计算精度
"""


def calculate_bmi(weight: float, height: float) -> tuple[float, str]:
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
    if height <= 0:
        raise ValueError("height must be > 0")

    bmi = weight / (height ** 2)
    bmi_rounded = round(bmi, 2)

    if bmi < 18.5:
        level = "偏瘦"
    elif bmi < 24:
        level = "正常"
    elif bmi < 28:
        level = "偏胖"
    else:
        level = "肥胖"

    return bmi_rounded, level


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
    if not isinstance(score, (int, float)):
        raise TypeError("score must be a number")

    s = int(score)
    if s < 0 or s > 100:
        raise ValueError("score must be between 0 and 100")

    if s >= 90:
        return "S"
    if s >= 80:
        return "A"
    if s >= 70:
        return "B"
    if s >= 60:
        return "C"
    return "D"


# ==================== 测试代码 ====================
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
