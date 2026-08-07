"""L06 练习1: 基本异常处理

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: try-except 语句、ZeroDivisionError、ValueError、IndexError

任务要求:
1. 实现 safe_divide 函数，处理 ZeroDivisionError
2. 实现 safe_parse_int 函数，处理 ValueError
3. 实现 safe_getitem 函数，处理 IndexError

提示:
1. 使用 try-except 捕获异常
2. 返回适当的默认值或 None
3. except ZeroDivisionError: return None
"""


def safe_divide(a: float, b: float) -> float | None:
    """安全除法，捕获 ZeroDivisionError"""
    try:
        return a / b
    except ZeroDivisionError:
        return None
    except Exception:
        return None


def safe_parse_int(text: str) -> int | None:
    """安全解析整数，捕获 ValueError"""
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def safe_getitem(items: list[str], index: int) -> str | None:
    """安全获取列表元素，捕获 IndexError"""
    try:
        return items[index]
    except Exception:
        return None


# 测试代码
if __name__ == "__main__":
    # 测试 safe_divide
    print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")  # 预期: 5.0
    print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")  # 预期: None

    # 测试 safe_parse_int
    print(f"safe_parse_int('42') = {safe_parse_int('42')}")  # 预期: 42
    print(f"safe_parse_int('abc') = {safe_parse_int('abc')}")  # 预期: None

    # 测试 safe_getitem
    items = ["apple", "banana", "cherry"]
    print(f"safe_getitem(items, 1) = {safe_getitem(items, 1)}")  # 预期: banana
    print(f"safe_getitem(items, 10) = {safe_getitem(items, 10)}")  # 预期: None
