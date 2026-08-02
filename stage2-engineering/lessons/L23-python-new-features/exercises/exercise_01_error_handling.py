"""

from __future__ import annotations

练习 1: 错误处理和彩色堆栈

目标：
  - 创建多层嵌套的函数调用
  - 观察彩色错误堆栈
  - 理解错误追踪的可读性改进

完成标准：
  - 创建至少 3 层函数嵌套
  - 引发不同类型的错误
  - 对比彩色和非彩色输出
"""


# TODO: 实现以下函数


def level_3():
    """
    最深层函数

    提示: 引发一个 TypeError
    例如: 尝试将字符串与整数相加
    """
    # TODO: 实现
    raise NotImplementedError("请实现 level_3 函数")


def level_2():
    """
    中间层函数

    提示: 调用 level_3 并传递参数
    """
    # TODO: 实现
    raise NotImplementedError("请实现 level_2 函数")


def level_1():
    """
    顶层函数

    提示: 调用 level_2 并处理一些数据
    """
    # TODO: 实现
    raise NotImplementedError("请实现 level_1 函数")


# TODO: 实现更多错误场景


def scenario_attribute_error():
    """
    场景: AttributeError

    提示: 访问对象不存在的属性
    """
    # TODO: 实现


def scenario_index_error():
    """
    场景: IndexError

    提示: 访问列表越界索引
    """
    # TODO: 实现


def scenario_key_error():
    """
    场景: KeyError

    提示: 访问字典不存在的键
    """
    # TODO: 实现


def scenario_value_error():
    """
    场景: ValueError

    提示: 传递错误的值类型
    """
    # TODO: 实现


# 测试代码
def test_colored_traceback():
    """测试彩色错误堆栈"""
    print("=" * 60)
    print("练习 1: 彩色错误堆栈测试")
    print("=" * 60)

    scenarios = [
        ("多层嵌套错误", level_1),
        ("AttributeError", scenario_attribute_error),
        ("IndexError", scenario_index_error),
        ("KeyError", scenario_key_error),
        ("ValueError", scenario_value_error),
    ]

    for name, func in scenarios:
        print(f"\n### 测试: {name}")
        print("-" * 60)
        try:
            func()
        except Exception as e:
            print(f"✗ 捕获到 {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()

        print()
        input("按 Enter 继续...")

    print("\n" + "=" * 60)
    print("练习完成！")
    print("\n任务:")
    print("  1. 观察彩色错误堆栈的可读性")
    print("  2. 运行 NO_COLOR=1 python stage2-engineering/lessons/L21-python313-experience/exercises/exercise_01_error_handling.py")
    print("  3. 对比彩色和非彩色输出")
    print("  4. 思考：哪个更容易定位问题？")


if __name__ == "__main__":
    test_colored_traceback()
