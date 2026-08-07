"""参考答案 2: 逻辑运算符与短路求值

对应练习: exercises/02_logical_operators.py
知识点: and/or/not 运算符、短路求值、条件判断

本参考答案为演示型练习的完整实现版本。
"""


def safe_get(data, key, default=''):
    """安全获取字典值。

    Args:
        data: 字典对象（可能为 None）
        key: 键名
        default: 默认值（当 data 为 None 或 key 不存在时返回）

    Returns:
        字典中的值或默认值
    """
    if data is None:
        return default
    if key in data:
        return data[key]
    return default


def validate_age(age):
    """验证年龄并返回提示信息。

    Args:
        age: 年龄（可能为 None）

    Returns:
        验证结果提示
    """
    if age is None:
        return '年龄未提供'
    if age > 150:
        return '年龄超出合理范围'
    if age <= 0:
        return '年龄必须大于0'
    return '有效年龄: ' + str(age)


def get_user_status(is_logged_in, is_premium, has_unsaved_changes):
    """判断用户状态。

    Args:
        is_logged_in: 是否已登录
        is_premium: 是否是付费用户
        has_unsaved_changes: 是否有未保存的更改

    Returns:
        用户状态描述
    """
    if not is_logged_in:
        return '游客'
    if is_premium:
        if has_unsaved_changes:
            return 'VIP 用户（有未保存更改）'
        return 'VIP 用户'
    if has_unsaved_changes:
        return '普通用户（有未保存更改）'
    return '普通用户'


if __name__ == '__main__':
    print('=== 安全字典访问测试 ===')
    test_cases = [
        ({'name': 'Alice', 'age': 30}, 'name', '', 'Alice'),
        ({'name': 'Bob'}, 'age', 'N/A', 'N/A'),
        (None, 'name', 'Unknown', 'Unknown'),
        ({}, 'name', '', ''),
    ]
    for data, key, default, expected in test_cases:
        result = safe_get(data, key, default)
        status = '✓' if result == expected else '✗'
        print(f"{status} safe_get({data}, '{key}', '{default}') = '{result}'")

    print('\n=== 年龄验证测试 ===')
    age_tests = [(25, '有效年龄: 25'), (0, '年龄必须大于0'), (None, '年龄未提供'), (150, '年龄超出合理范围')]
    for age, expected in age_tests:
        result = validate_age(age)
        status = '✓' if result == expected else '✗'
        print(f"{status} validate_age({age}) = '{result}'")

    print('\n=== 用户状态测试 ===')
    status_tests = [
        ((False, False, False), '游客'),
        ((True, False, False), '普通用户'),
        ((True, True, False), 'VIP 用户'),
        ((True, True, True), 'VIP 用户（有未保存更改）'),
        ((True, False, True), '普通用户（有未保存更改）'),
    ]
    for args, expected in status_tests:
        result = get_user_status(*args)
        status = '✓' if result == expected else '✗'
        print(f"{status} {args} → '{result}'")
