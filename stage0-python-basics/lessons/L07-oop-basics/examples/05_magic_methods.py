"""Example: Class Basics and Advanced Concepts.

Demonstrates core Python OOP concepts: classes, inheritance, methods, @property.
This is the core example for L06. Magic methods will be covered in L07."""

# ============ L06 Review: Simple Dog Class ============
# Only using L06 concepts: class, __init__, self, methods


class Dog:
    """Dog class using only L06 concepts."""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def bark(self) -> str:
        return f"{self.name} says: Woof!"

    def get_info(self) -> str:
        return f"{self.name} is {self.age} years old"


if __name__ == "__main__":
    dog = Dog("Buddy", 3)
    print(f"\n{dog.get_info()}")
    print(f"{dog.bark()}")
