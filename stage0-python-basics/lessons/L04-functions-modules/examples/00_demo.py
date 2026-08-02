"""示例代码：L04 函数与模块"""

# ============ Part 1: 函数基础 ============


def greet(name: str, greeting: str = "Hello") -> str:
    """生成个性化问候语"""
    return f"{greeting}, {name}!"


def add(a: int, b: int) -> int:
    """两数相加"""
    return a + b


def sum_all(*numbers: int) -> int:
    """求和任意数量的数字"""
    return sum(numbers)


def build_profile(name: str, **info: str) -> dict:
    """构建用户档案"""
    profile = {"name": name}
    profile.update(info)
    return profile


def divide(a: float, b: float) -> float | None:
    """安全除法"""
    if b == 0:
        return None
    return a / b


# ============ Part 2: 模块与包 ============


# 以下演示模块的 __name__ 行为
def get_module_name() -> str:
    """获取当前模块名称"""
    return __name__


if __name__ == "__main__":
    # 测试函数
    print("=== 函数测试 ===")
    print(greet("Alice"))
    print(greet("Bob", "Hi"))
    print(add(3, 5))
    print(sum_all(1, 2, 3, 4, 5))
    print(build_profile("Alice", age="25", city="Beijing"))
    print(f"10 / 2 = {divide(10, 2)}")
    print(f"10 / 0 = {divide(10, 0)}")

    # 测试 __name__
    print("\n=== 模块名称测试 ===")
    print(f"当前模块名称: {get_module_name()}")
    print("当直接运行时，__name__ 为 '__main__'")
    print("当被导入时，__name__ 为模块名")
