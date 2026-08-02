"""示例2: 多个 except 子句"""


def parse_number(text: str) -> float | None:
    """解析数字字符串"""
    try:
        return float(text)
    except ValueError:
        print(f"错误: '{text}' 不是有效的数字")
        return None
    except TypeError:
        print("错误: 输入类型错误，需要字符串")
        return None


def convert_and_divide(a: str, b: str) -> float | None:
    """字符串转数字后相除"""
    try:
        x = float(a)
        y = float(b)
        return x / y
    except ValueError as e:
        print(f"数值转换错误: {e}")
        return None
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None


# 测试
print(parse_number("3.14"))  # 3.14
print(parse_number("hello"))  # 错误信息
print(parse_number(None))  # 错误信息

print(convert_and_divide("10", "2"))  # 5.0
print(convert_and_divide("10", "0"))  # 错误信息
print(convert_and_divide("a", "2"))  # 错误信息
