"""L09 基础实战 - 学员管理系统参考答案"""


class Student:
    """学员数据类（手动实现，等价于 dataclass）"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def to_dict(self) -> dict[str, str | int]:
        """转换为字典（用于序列化）"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Student":
        """从字典创建实例"""
        return cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            age=int(data["age"]),  # type: ignore[call-overload]
        )


class StudentManager:
    """学员管理器"""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, student: Student) -> bool:
        """添加学员

        Args:
            student: 学员对象

        Returns:
            bool: 添加是否成功
        """
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def get_student(self, student_id: str) -> Student | None:
        """获取学员

        Args:
            student_id: 学员ID

        Returns:
            Student | None: 学员对象，不存在则返回 None
        """
        return self.students.get(student_id)

    def remove_student(self, student_id: str) -> bool:
        """删除学员

        Args:
            student_id: 学员ID

        Returns:
            bool: 删除是否成功
        """
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False

    def update_student(
        self,
        student_id: str,
        name: str | None = None,
        age: int | None = None,
    ) -> bool:
        """更新学员信息

        Args:
            student_id: 学员ID
            name: 新姓名（可选）
            age: 新年龄（可选）

        Returns:
            bool: 更新是否成功
        """
        student = self.students.get(student_id)
        if student is None:
            return False
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        return True

    def list_students(self) -> list[Student]:
        """列出所有学员（返回副本，避免外部修改）"""
        return list(self.students.values())

    def search_by_name(self, name: str) -> list[Student]:
        """按姓名搜索（支持部分匹配，不区分大小写）

        Args:
            name: 搜索关键字

        Returns:
            list[Student]: 匹配的学员列表
        """
        name_lower = name.lower()
        return [s for s in self.students.values() if name_lower in s.name.lower()]

    def get_statistics(self) -> dict[str, int | float]:
        """获取统计信息

        Returns:
            dict: 统计数据
        """
        ages = [s.age for s in self.students.values()]
        return {
            "total": len(self.students),
            "average_age": sum(ages) / len(ages) if ages else 0,
            "min_age": min(ages) if ages else 0,
            "max_age": max(ages) if ages else 0,
        }
