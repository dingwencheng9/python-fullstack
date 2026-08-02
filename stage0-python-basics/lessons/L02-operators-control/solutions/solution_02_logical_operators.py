"""参考答案 2: 逻辑运算符与短路求值"""


def safe_get(data: dict | None, key: str, default: str = "") -> str:
    """安全获取字典值。

    Args:
        data: 字典对象（可能为 None）
        key: 键名
        default: 默认值（当 data 为 None 或 key 不存在时返回）

    Returns:
        字典中的值或默认值

    Examples:
        >>> safe_get({"name": "Alice"}, "name")
        'Alice'
        >>> safe_get(None, "name", "Unknown")
        'Unknown'
        >>> safe_get({}, "name", "Unknown")
        'Unknown'
    """
    # 利用短路求值特性实现
    # data and data.get(key, default) 的求值过程：
    # 1. 如果 data 是 None 或空字典 → 短路返回 default
    # 2. 如果 data 有效 → data.get(key, default) 被求值
    return (data and data.get(key, default)) or default


def validate_age(age: int | None) -> str:
    """验证年龄并返回提示信息。

    Args:
        age: 年龄（可能为 None）

    Returns:
        验证结果提示

    Examples:
        >>> validate_age(25)
        '有效年龄: 25'
        >>> validate_age(0)
        '年龄必须大于0'
        >>> validate_age(None)
        '年龄未提供'
        >>> validate_age(150)
        '年龄超出合理范围'
    """
    # - None: "年龄未提供"
    # - <= 0: "年龄必须大于0"
    # - > 120: "年龄超出合理范围"
    # - 其他: "有效年龄: {age}"
    if age is None:
        return "年龄未提供"
    if age <= 0:
        return "年龄必须大于0"
    if age > 120:
        return "年龄超出合理范围"
    return f"有效年龄: {age}"


def get_user_status(is_logged_in: bool, is_premium: bool, has_unsaved_changes: bool) -> str:
    """判断用户状态。

    Args:
        is_logged_in: 是否已登录
        is_premium: 是否是付费用户
        has_unsaved_changes: 是否有未保存的更改

    Returns:
        用户状态描述

    Examples:
        >>> get_user_status(False, False, False)
        '游客'
        >>> get_user_status(True, False, False)
        '普通用户'
        >>> get_user_status(True, True, False)
        'VIP 用户'
        >>> get_user_status(True, False, True)
        '普通用户（有未保存更改）'
    """
    # 使用逻辑运算符组合判断
    if not is_logged_in:
        return "游客"
    if is_premium and has_unsaved_changes:
        return "VIP 用户（有未保存更改）"
    if is_premium:
        return "VIP 用户"
    if has_unsaved_changes:
        return "普通用户（有未保存更改）"
    return "普通用户"


if __name__ == "__main__":
    print("=== 安全字典访问测试 ===")
    test_cases = [
        ({"name": "Alice", "age": 30}, "name", "", "Alice"),
        ({"name": "Bob"}, "age", "N/A", "N/A"),
        (None, "name", "Unknown", "Unknown"),
        ({}, "name", "", ""),
    ]
    for data, key, default, expected in test_cases:
        result = safe_get(data, key, default)
        status = "✓" if result == expected else "✗"
        print(f"{status} safe_get({data}, '{key}', '{default}') = '{result}'")

    print("\n=== 年龄验证测试 ===")
    age_tests = [
        (25, "有效年龄: 25"),
        (0, "年龄必须大于0"),
        (None, "年龄未提供"),
        (150, "年龄超出合理范围"),
        (18, "有效年龄: 18"),
    ]
    for age, expected in age_tests:
        result = validate_age(age)
        status = "✓" if result == expected else "✗"
        print(f"{status} validate_age({age}) = '{result}'")

    print("\n=== 用户状态测试 ===")
    status_tests = [
        ((False, False, False), "游客"),
        ((True, False, False), "普通用户"),
        ((True, True, False), "VIP 用户"),
        ((True, True, True), "VIP 用户（有未保存更改）"),
        ((True, False, True), "普通用户（有未保存更改）"),
    ]
    for args, expected in status_tests:
        result = get_user_status(*args)
        status = "✓" if result == expected else "✗"
        print(f"{status} {args} → '{result}'")
