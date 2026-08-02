"""L02 练习3: 位运算符应用

难度: ⭐⭐☆ (中等)
预计时间: 30 分钟
知识点: 位运算符（&, |, ^, <<, >>, ~）、权限管理、状态压缩

任务描述:
练习位运算技巧，综合运用：
- 位运算符（&, |, ^, <<, >>, ~）
- 权限标志位管理
- 状态压缩存储

提示:
1. 判断奇偶: number & 1 (最低位为 1 则为奇数)
2. 权限检查: permissions & flag != 0
3. 添加权限: permissions | flag
"""


def is_even(number: int) -> bool:
    """判断奇偶（使用位运算）。

    Args:
        number: 待判断的整数

    Returns:
        True 表示偶数，False 表示奇数

    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
        >>> is_even(0)
        True
    """
    # 偶数的最低位为 0，奇数的最低位为 1
    return (number & 1) == 0


def swap_numbers(a: int, b: int) -> tuple[int, int]:
    """不使用临时变量交换两个数（使用异或）。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        交换后的 (a, b)

    Examples:
        >>> swap_numbers(5, 3)
        (3, 5)
        >>> swap_numbers(10, 20)
        (20, 10)
    """
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return (a, b)


# 权限标志位常量（使用 2 的幂次方）
PERMISSION_READ = 1 << 0  # 1   - 0001
PERMISSION_WRITE = 1 << 1  # 2   - 0010
PERMISSION_DELETE = 1 << 2  # 4   - 0100
PERMISSION_ADMIN = 1 << 3  # 8   - 1000


def grant_permission(current_permissions: int, permission: int) -> int:
    """授予权限（设置标志位）。

    Args:
        current_permissions: 当前权限掩码
        permission: 要授予的权限标志

    Returns:
        更新后的权限掩码

    Examples:
        >>> grant_permission(0, PERMISSION_READ)
        1
        >>> grant_permission(1, PERMISSION_WRITE)
        3
        >>> grant_permission(5, PERMISSION_READ)  # 已有 READ，再授予 READ
        5
    """
    return current_permissions | permission


def revoke_permission(current_permissions: int, permission: int) -> int:
    """撤销权限（清除标志位）。

    Args:
        current_permissions: 当前权限掩码
        permission: 要撤销的权限标志

    Returns:
        更新后的权限掩码

    Examples:
        >>> revoke_permission(7, PERMISSION_WRITE)  # 7=0111, 撤销 WRITE(2)
        5
        >>> revoke_permission(5, PERMISSION_READ)  # 5=0101, 撤销 READ(1)
        4
    """
    return current_permissions & ~permission


def has_permission(current_permissions: int, permission: int) -> bool:
    """检查是否拥有某权限。

    Args:
        current_permissions: 当前权限掩码
        permission: 要检查的权限标志

    Returns:
        是否拥有该权限

    Examples:
        >>> has_permission(7, PERMISSION_READ)
        True
        >>> has_permission(5, PERMISSION_WRITE)
        False
    """
    return (current_permissions & permission) != 0


# ==================== 测试代码 ====================
if __name__ == "__main__":
    print("=== 奇偶判断测试 ===")
    even_tests = [(4, True), (7, False), (0, True), (1, False), (100, True)]
    for n, expected in even_tests:
        result = is_even(n)
        status = "✓" if result == expected else "✗"
        print(f"{status} is_even({n}) = {result}")

    print("\n=== 数字交换测试 ===")
    swap_tests = [(5, 3), (10, 20), (0, 1), (100, 100)]
    for a, b in swap_tests:
        result = swap_numbers(a, b)
        expected = (b, a)
        status = "✓" if result == expected else "✗"
        print(f"{status} swap_numbers({a}, {b}) = {result}")

    print("\n=== 权限管理测试 ===")
    # 初始权限
    perms = 0
    print(f"初始权限: {perms}")

    # 授予读权限
    perms = grant_permission(perms, PERMISSION_READ)
    print(f"授予读权限后: {perms} (二进制: {bin(perms)})")
    assert has_permission(perms, PERMISSION_READ)

    # 授予写权限
    perms = grant_permission(perms, PERMISSION_WRITE)
    print(f"授予写权限后: {perms} (二进制: {bin(perms)})")
    assert has_permission(perms, PERMISSION_READ)
    assert has_permission(perms, PERMISSION_WRITE)

    # 撤销读权限
    perms = revoke_permission(perms, PERMISSION_READ)
    print(f"撤销读权限后: {perms} (二进制: {bin(perms)})")
    assert not has_permission(perms, PERMISSION_READ)
    assert has_permission(perms, PERMISSION_WRITE)

    # 添加管理员权限
    perms = grant_permission(perms, PERMISSION_ADMIN)
    print(f"授予管理员权限后: {perms} (二进制: {bin(perms)})")

    print("\n权限测试全部通过 ✓")
