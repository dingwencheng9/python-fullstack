"""L07 练习3: 创建一个可调用对象 Multiplier

难度: ⭐⭐☆ (中等)
预计时间: 20 分钟
知识点: __call__ 魔术方法、可调用对象、闭包

任务要求:
1. __init__(factor) - 初始化乘数
2. __call__(x) - 返回 x * factor
3. __repr__ - 返回类似 Multiplier(3) 的字符串

提示:
1. __call__ 让对象像函数一样可调用
2. doubler = Multiplier(2); doubler(5) 返回 10
3. 常用于创建配置化的函数

示例:
    doubler = Multiplier(2)
    print(doubler(5))  # 输出: 10
    print(doubler(3))  # 输出: 6
"""


class Multiplier:
    """可调用乘法器"""

    def __init__(self, factor: float) -> None:
        """初始化乘数"""
        self.factor = factor

    def __call__(self, x: float) -> float:
        """返回 x * factor"""
        return x * self.factor

    def __repr__(self) -> str:
        """返回类似 Multiplier(3) 的字符串"""
        return f"Multiplier({self.factor})"


# 测试代码
if __name__ == "__main__":
    doubler = Multiplier(2)
    tripler = Multiplier(3)

    print(doubler(5))  # 预期: 10
    print(tripler(5))  # 预期: 15
    print(doubler(3))  # 预期: 6
    print(f"doubler = {doubler}")  # 预期: Multiplier(2)
