"""

from __future__ import annotations

L21 示例 1: Python 3.13 彩色错误提示

演示 Python 3.13 的改进错误显示功能。
"""

import sys


def demonstrate_colorful_traceback() -> None:
    """演示彩色错误追踪"""

    print("🎨 Python 3.13 彩色错误提示演示")
    print("=" * 70)
    print(f"\nPython 版本: {sys.version}")
    print()

    print("💡 Python 3.13 的错误提示改进：")
    print("  1. 语法高亮（关键字、变量名等）")
    print("  2. 更清晰的错误位置标注")
    print("  3. 改进的异常链显示")
    print("  4. 更好的代码片段展示")


def syntax_error_example() -> None:
    """语法错误示例"""
    # 取消注释下面的代码查看彩色错误
    # def broken_function()  # 缺少冒号
    #     return 42


def type_error_example() -> None:
    """类型错误示例"""
    try:
        _ = "hello" + 42  # ❌ 类型错误（故意触发）
    except TypeError as e:
        print(f"捕获的类型错误: {e}")


def attribute_error_example() -> None:
    """属性错误示例"""
    try:
        x = "hello"
        x.append("world")  # ❌ str 没有 append 方法
    except AttributeError as e:
        print(f"捕获的属性错误: {e}")


def key_error_example() -> None:
    """键错误示例"""
    try:
        data = {"name": "Alice", "age": 25}
        _ = data["email"]  # ❌ 键不存在（故意触发）
    except KeyError as e:
        print(f"捕获的键错误: {e}")


def demonstrate_exception_chaining() -> None:
    """演示异常链"""

    print("\n\n🔗 异常链演示")
    print("=" * 70)

    try:
        try:
            data = {"value": "not_a_number"}
            _ = int(data["value"])  # 转换失败（故意触发）
        except ValueError as e:
            raise RuntimeError("数据处理失败") from e
    except RuntimeError as e:
        print(f"捕获的运行时错误: {e}")
        print(f"原始错误: {e.__cause__}")


def demonstrate_better_suggestions() -> None:
    """演示更好的建议"""

    print("\n\n💡 Python 3.13 改进的错误建议")
    print("=" * 70)

    class Person:
        def __init__(self, name: str) -> None:
            self.name = name

    person = Person("Alice")

    try:
        # 拼写错误
        print(person.nmae)  # 应该是 name
    except AttributeError as e:
        print(f"\n错误信息: {e}")
        print("👆 Python 3.13 会建议: Did you mean 'name'?")


def show_comparison() -> None:
    """对比 Python 3.13 和 3.13"""

    print("\n\n🆚 Python 3.12 vs 3.13 错误提示对比")
    print("=" * 70)

    comparison = """
Python 3.12 错误提示:
  Traceback (most recent call last):
    File "script.py", line 5, in <module>
      result = func(data)
  TypeError: func() missing 1 required positional argument: 'x'

Python 3.13 错误提示:
  Traceback (most recent call last):
    File "script.py", line 5, in <module>
      result = func(data)
               ^^^^^^^^^^
  TypeError: func() missing 1 required positional argument: 'x'

改进点:
  ✅ 用 ^^^ 标注错误位置
  ✅ 彩色语法高亮（在终端中）
  ✅ 更清晰的代码片段展示
  ✅ 改进的建议（拼写错误等）
"""

    print(comparison)


def show_terminal_colors() -> None:
    """展示终端彩色输出"""

    print("\n\n🌈 终端彩色输出")
    print("=" * 70)

    print("\n在支持彩色的终端中，你会看到：")
    print("  • 关键字（def, class, if）使用紫色")
    print("  • 变量名使用蓝色")
    print("  • 字符串使用绿色")
    print("  • 数字使用橙色")
    print("  • 错误位置使用红色下划线")


def demonstrate_examples() -> None:
    """演示各种错误"""

    print("\n\n📋 错误示例演示")
    print("=" * 70)

    print("\n1️⃣ 类型错误:")
    type_error_example()

    print("\n2️⃣ 属性错误:")
    attribute_error_example()

    print("\n3️⃣ 键错误:")
    key_error_example()


def main() -> None:
    """主函数"""

    demonstrate_colorful_traceback()
    demonstrate_examples()
    demonstrate_exception_chaining()
    demonstrate_better_suggestions()
    show_comparison()
    show_terminal_colors()

    print("\n\n✨ 提示：")
    print("  • 在 Python 3.13 环境中运行此文件")
    print("  • 取消注释错误示例代码查看彩色错误")
    print("  • 使用支持 ANSI 彩色的终端")
    print("\n🔑 关键改进：")
    print("  • 彩色语法高亮")
    print("  • 更清晰的错误位置标注（^^^）")
    print("  • 改进的错误建议")
    print("  • 更好的异常链显示")


if __name__ == "__main__":
    main()
