"""Animal 类层次参考答案"""

from typing import override


class Animal:
    """动物基类"""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        """发出声音"""
        return "Some sound"

    def move(self) -> str:
        """移动"""
        return f"{self.name} is moving"


class Dog(Animal):
    """狗类"""

    @override
    def speak(self) -> str:
        """狗叫"""
        return f"{self.name} says Woof!"


class Cat(Animal):
    """猫类"""

    @override
    def speak(self) -> str:
        """猫叫"""
        return f"{self.name} says Meow!"
