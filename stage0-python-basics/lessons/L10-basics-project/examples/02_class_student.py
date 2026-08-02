"""示例2: 使用类定义数据模型

使用类 + L07 魔术方法实现 dataclass 的等价功能。
本课综合 Stage 0 的类定义知识（L06）和魔术方法（L07）。
"""

from typing import Any


class Student:
    """学员数据模型

    手工实现 __init__、__repr__、__eq__，
    对比 Stage 1 的 @dataclass 自动生成版本。
    """

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """用于调试和显示"""
        return f"Student({self.student_id!r}, {self.name!r}, {self.age})"

    def __eq__(self, other: object) -> bool:
        """按学号比较（同一学号视为同一学员）"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id

    def __hash__(self) -> int:
        """支持将 Student 加入 set 或作为 dict key"""
        return hash(self.student_id)

    def to_dict(self) -> dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Student":
        """从字典创建实例"""
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
        )

    def is_adult(self) -> bool:
        """判断是否成年"""
        return self.age >= 18


class StudentWithDefaults:
    """带默认值的学员模型

    展示可选参数的构造函数设计。
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        age: int = 18,
        grade: str = "A",
        active: bool = True,
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.active = active

    def __repr__(self) -> str:
        return f"StudentWithDefaults({self.student_id!r}, {self.name!r}, age={self.age}, grade={self.grade!r}, active={self.active})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StudentWithDefaults):
            return NotImplemented
        return self.student_id == other.student_id


# 使用示例
if __name__ == "__main__":
    # 基础 Student
    s1 = Student("001", "张三", 20)
    print(f"学员: {s1}")
    print(f"repr: {s1!r}")

    # __eq__ 按学号比较（同一学号视为同一学员）
    s2 = Student("001", "张三", 20)
    print(f"s1 == s2: {s1 == s2}")

    # to_dict / from_dict 序列化
    data = s1.to_dict()
    print(f"序列化为字典: {data}")
    s3 = Student.from_dict(data)
    print(f"从字典恢复: {s3}")

    print()

    # 带默认值的学员
    s4 = StudentWithDefaults("002", "李四")
    print(f"带默认值: {s4}")
    print(f"成年?: {s4.age >= 18}")

    s5 = StudentWithDefaults("003", "王五", age=16, grade="C")
    print(f"自定义参数: {s5}")

    print()

    # __hash__ 支持 set 存储（仅 Student 类，StudentWithDefaults 未定义）
    student_set = {s1, s2}
    print(f"set 中不重复学员数: {len(student_set)}")
