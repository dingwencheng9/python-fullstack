"""示例1: 基础魔法方法"""


class Person:
    """演示 __init__, __repr__, __str__"""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age!r})"

    def __str__(self) -> str:
        return f"{self.name}, {self.age}岁"


# 演示
alice = Person("Alice", 30)

print(f"repr: {alice!r}")  # Person(name='Alice', age=30)
print(f"str:  {alice!s}")  # Alice, 30岁
print(f"直接打印: {alice}")  # Alice, 30岁
