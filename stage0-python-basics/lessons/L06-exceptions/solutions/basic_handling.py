"""练习1参考答案: 基本异常处理"""

# ruff: noqa: N999


def safe_divide(a: float, b: float) -> float | None:
    """安全除法，捕获 ZeroDivisionError"""
    try:
        return a / b
    except ZeroDivisionError:
        return None


def safe_parse_int(text: str) -> int | None:
    """安全解析整数，捕获 ValueError"""
    try:
        return int(text)
    except ValueError:
        return None


def safe_getitem(items: list[str], index: int) -> str | None:
    """安全获取列表元素，捕获 IndexError"""
    try:
        return items[index]
    except IndexError:
        return None


# 测试代码
if __name__ == "__main__":
    # 测试 safe_divide
    print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")  # 5.0
    print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")  # None

    # 测试 safe_parse_int
    print(f"safe_parse_int('42') = {safe_parse_int('42')}")  # 42
    print(f"safe_parse_int('abc') = {safe_parse_int('abc')}")  # None

    # 测试 safe_getitem
    items = ["apple", "banana", "cherry"]
    print(f"safe_getitem(items, 1) = {safe_getitem(items, 1)}")  # banana
    print(f"safe_getitem(items, 10) = {safe_getitem(items, 10)}")  # None
