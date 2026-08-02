"""Person 类参考答案"""


class Person:
    """人员类"""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """自我介绍"""
        return f"我叫 {self.name}，今年 {self.age} 岁"

    def birthday(self) -> None:
        """过生日，年龄加一"""
        self.age += 1
