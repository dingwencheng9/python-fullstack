"""示例6: 异常链与 traceback"""

import traceback


def level3() -> int:
    """第三层函数"""
    raise ValueError("原始错误")


def level2() -> None:
    """第二层函数"""
    level3()


def level1() -> None:
    """第一层函数"""
    try:
        level2()
    except ValueError as e:
        # 重新抛出，保留原始异常链
        raise RuntimeError("调用失败") from e


# 测试异常链
print("=== 异常链演示 ===")
try:
    level1()
except RuntimeError as e:
    print(f"捕获异常: {e}")
    print(f"原始异常: {e.__cause__}")


def handle_with_traceback() -> None:
    """演示 traceback 模块"""
    try:
        _ = 1 / 0
    except Exception:
        print("捕获异常，跟踪信息:")
        traceback.print_exc()


print("\n=== Traceback 演示 ===")
handle_with_traceback()


def safe_divide(a: float, b: float) -> float | None:
    """返回 None 而不是抛出异常"""
    try:
        return a / b
    except ZeroDivisionError:
        return None


print("\n=== 使用 None 代替异常 ===")
print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # None
