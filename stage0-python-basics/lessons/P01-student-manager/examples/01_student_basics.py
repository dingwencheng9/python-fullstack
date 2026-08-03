"""示例1: 学员管理系统基础结构"""


class Student:
    """学员类"""

    def __init__(self, student_id: str, name: str, age: int):
        self.student_id = student_id
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"[{self.student_id}] {self.name} (年龄: {self.age})"

    def __repr__(self) -> str:
        return f"Student(student_id={self.student_id!r}, name={self.name!r}, age={self.age!r})"


class StudentManager:
    """学员管理器"""

    def __init__(self):
        self.students = {}

    def add_student(self, student: Student) -> None:
        """添加学员"""
        self.students[student.student_id] = student
        print(f"✅ 已添加学员: {student}")

    def get_student(self, student_id: str) -> Student | None:
        """获取学员"""
        return self.students.get(student_id)

    def list_students(self) -> list[Student]:
        """列出所有学员"""
        return list(self.students.values())

    def remove_student(self, student_id: str) -> bool:
        """删除学员"""
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False


# 使用示例
if __name__ == "__main__":
    # 创建管理器
    manager = StudentManager()

    # 添加学员
    student1 = Student("001", "张三", 20)
    student2 = Student("002", "李四", 21)

    manager.add_student(student1)
    manager.add_student(student2)

    # 查询学员
    found = manager.get_student("001")
    print(f"\n找到学员: {found}")

    # 列出所有学员
    print("\n所有学员:")
    for student in manager.list_students():
        print(f"  {student}")

    # 删除学员
    manager.remove_student("001")
    print(f"\n删除后剩余学员数: {len(manager.list_students())}")
