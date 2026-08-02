"""L05 示例 2: traceback 分析

演示如何使用 traceback 模块分析异常信息。
运行方式: uv run python examples/02_traceback_analysis.py
"""

import traceback
import sys


def level_3():
    """模拟深层调用"""
    raise ValueError("这是深层错误")


def level_2():
    """模拟中层调用"""
    level_3()


def level_1():
    """模拟顶层调用"""
    level_2()


def analyze_exception_with_traceback():
    """使用 traceback 模块分析异常"""
    try:
        level_1()
    except Exception:
        print("=" * 60)
        print("1. 使用 traceback.print_exc() 打印异常:")
        print("=" * 60)
        traceback.print_exc()

        print("\n" + "=" * 60)
        print("2. 使用 traceback.format_exc() 格式化异常:")
        print("=" * 60)
        formatted = traceback.format_exc()
        print(formatted)

        print("\n" + "=" * 60)
        print("3. 使用 sys.last_traceback 分析崩溃:")
        print("=" * 60)
        if hasattr(sys, 'last_traceback') and sys.last_traceback:
            tb = sys.last_traceback
            frame = tb.tb_frame
            print(f"崩溃位置: {frame.f_code.co_filename}:{tb.tb_lineno}")
            print(f"函数名: {frame.f_code.co_name}")
            print("\n调用栈:")
            traceback.print_tb(tb)


def analyze_exception_programmatically():
    """程序化分析异常"""
    print("\n" + "=" * 60)
    print("4. 程序化分析异常:")
    print("=" * 60)

    try:
        data = {"key": "value"}
        _ = data["nonexistent_key"]  # KeyError
    except Exception as e:
        exc_type = type(e).__name__
        exc_value = str(e)
        exc_tb = traceback.format_exception(type(e), e, e.__traceback__)

        print(f"异常类型: {exc_type}")
        print(f"异常信息: {exc_value}")
        print("异常详情:")
        for line in exc_tb:
            print(f"  {line.strip()}")


if __name__ == "__main__":
    print("traceback 模块使用示例\n")
    analyze_exception_with_traceback()
    analyze_exception_programmatically()
    print("\n✓ 脚本执行完成")
