"""

from __future__ import annotations

练习 1: 错误处理和彩色堆栈 - 参考答案

===============================================================================
解题思路: Python 3.13 彩色错误堆栈展示多层调用链和各种错误类型
===============================================================================
"""


def level_3():
    """触发 TypeError"""
    user_input = "100"
    calculation = 50
    return user_input + calculation  # TypeError


def level_2():
    """中间层调用"""
    _user_data = {"name": "Alice", "age": 30}  # 模拟中间层数据
    return level_3()


def level_1():
    """顶层入口"""
    print("开始执行...")
    return level_2()


def scenario_attribute_error():
    """AttributeError 示例"""

    class User:
        def __init__(self, name: str, email: str):
            self.name = name
            self.email = email

    user = User(name="Bob", email="bob@example.com")
    return user.emial  # 拼写错误


def scenario_index_error():
    """IndexError 示例"""
    users = ["Alice", "Bob", "Charlie"]
    return users[10]


def scenario_key_error():
    """KeyError 示例"""
    config = {"database": "postgresql", "host": "localhost"}
    return config["password"]


def scenario_value_error():
    """ValueError 示例"""
    from datetime import datetime

    return datetime.strptime("2024-13-45", "%Y-%m-%d")


def test_colored_traceback():
    """测试彩色堆栈"""
    import os
    import sys

    print("=" * 70)
    print("Python 3.13 彩色错误堆栈测试")
    print("=" * 70)
    print(f"Python 版本: {sys.version}")

    no_color = os.environ.get("NO_COLOR", "")
    if no_color:
        print("⚠️  彩色输出已禁用")
    else:
        print("✓ 彩色输出已启用")

    scenarios = [
        ("多层嵌套 (TypeError)", level_1),
        ("属性错误", scenario_attribute_error),
        ("索引错误", scenario_index_error),
        ("键错误", scenario_key_error),
        ("值错误", scenario_value_error),
    ]

    for name, func in scenarios:
        print(f"\n{'=' * 70}")
        print(f"测试: {name}")
        print("=" * 70)
        try:
            func()
        except Exception:
            import traceback

            traceback.print_exc()
        try:
            input("\n按 Enter 继续...")
        except EOFError:
            print("\n非交互环境：跳过等待输入")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    test_colored_traceback()
