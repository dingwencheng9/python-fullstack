"""

from __future__ import annotations

Python 3.13 彩色错误提示演示

本脚本演示 Python 3.13 的彩色错误堆栈功能。
运行此脚本将看到彩色化的错误信息。
"""

import sys


def divide(a: int, b: int) -> float:
    """除法运算"""
    return a / b


def process_numbers(numbers: list[int]) -> list[float]:
    """处理数字列表"""
    results = []
    for num in numbers:
        result = divide(num, 0)  # 故意的 ZeroDivisionError
        results.append(result)
    return results


class UserProfile:
    """用户配置类"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.data = None

    def load_data(self):
        """加载用户数据"""
        # 模拟数据库连接错误
        raise ConnectionError("Database connection failed")

    def get_username(self) -> str:
        """获取用户名"""
        if self.data is None:
            self.load_data()
        return self.data["username"]


def fetch_user_info(user_id: int) -> str:
    """获取用户信息"""
    profile = UserProfile(user_id)
    return profile.get_username()


def demo_type_error():
    """演示 TypeError"""
    value = "hello"
    result = value * [1, 2, 3]  # 类型错误
    return result


def demo_attribute_error():
    """演示 AttributeError"""
    data = {"name": "Python"}
    return data.version  # 属性错误


def demo_index_error():
    """演示 IndexError"""
    items = [1, 2, 3]
    return items[10]  # 索引错误


def demo_key_error():
    """演示 KeyError"""
    data = {"name": "Python", "version": 3.13}
    return data["author"]  # 键错误


def demo_nested_error():
    """演示嵌套错误"""

    def level_3():
        return 1 / 0

    def level_2():
        return level_3()

    def level_1():
        return level_2()

    return level_1()


def main():
    """主函数 - 运行各种错误演示"""
    print("Python 3.13 彩色错误提示演示")
    print(f"Python 版本: {sys.version}")
    print("=" * 60)

    demos = [
        ("ZeroDivisionError", lambda: process_numbers([10, 20, 30])),
        ("ConnectionError", lambda: fetch_user_info(123)),
        ("TypeError", demo_type_error),
        ("AttributeError", demo_attribute_error),
        ("IndexError", demo_index_error),
        ("KeyError", demo_key_error),
        ("嵌套错误", demo_nested_error),
    ]

    for name, func in demos:
        print(f"\n### 演示: {name}")
        print("-" * 60)
        try:
            func()
        except Exception as e:
            print(f"✗ 捕获到 {type(e).__name__}: {e}")
            print()
            # 让错误堆栈显示出来
            import traceback

            traceback.print_exc()

        print()
        input("按 Enter 继续下一个演示...")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n提示:")
    print("  - 红色: 错误类型和消息")
    print("  - 蓝色: 文件路径")
    print("  - 黄色: 行号")
    print("  - 绿色: 代码片段")
    print("\n环境变量控制:")
    print("  - FORCE_COLOR=1: 强制启用彩色")
    print("  - NO_COLOR=1: 禁用彩色")


if __name__ == "__main__":
    main()
