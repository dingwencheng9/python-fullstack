"""P01 练习1: 学员管理系统

难度: ⭐⭐⭐ (进阶)
预计时间: 60 分钟
知识点: 类设计、字典操作、CRUD 操作、列表推导式

任务描述:
实现完整的学员管理功能，包括增、删、改、查、搜索、统计等操作。

提示:
1. 使用字典存储学员，key 是 student_id
2. 每个方法返回 True/False 表示成功/失败
3. 支持部分更新（只更新提供的字段）
4. 使用列表推导式实现搜索，使用聚合函数实现统计
"""


class Student:
    """学员数据类（手动实现，等价于 dataclass）"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建"""
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
        )


class StudentManager:
    """学员管理器"""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, student: Student) -> bool:
        """添加学员

        步骤:
        1. 检查 student_id 是否已存在
        2. 如果存在，返回 False
        3. 否则添加到字典，返回 True
        """
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def get_student(self, student_id: str) -> Student | None:
        """获取学员

        步骤:
        1. 从字典中获取对应 student_id 的学员
        2. 如果存在返回学员对象，否则返回 None
        """
        return self.students.get(student_id)

    def remove_student(self, student_id: str) -> bool:
        """删除学员

        步骤:
        1. 检查 student_id 是否存在
        2. 如果存在，删除并返回 True
        3. 如果不存在，返回 False
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

        步骤:
        1. 检查 student_id 是否存在
        2. 只更新提供的字段（name 或 age 不为 None）
        3. 返回更新是否成功
        """
        if student_id not in self.students:
            return False
        student = self.students[student_id]
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        return True

    def list_students(self) -> list[Student]:
        """列出所有学员

        💡 返回字典中所有学员的列表（副本）
        """
        return list(self.students.values())

    def search_by_name(self, name: str) -> list[Student]:
        """按姓名搜索（支持部分匹配，不区分大小写）

        步骤:
        1. 遍历所有学员
        2. 检查 name 是否在学员姓名中（转换为小写比较）
        3. 返回所有匹配的学员
        """
        results: list[Student] = []
        key = name.lower()
        for student in self.students.values():
            if key in student.name.lower():
                results.append(student)
        return results

    def get_statistics(self) -> dict[str, int | float]:
        """获取统计信息

        返回字段:
        - total: 学员总数
        - average_age: 平均年龄
        - min_age: 最小年龄
        - max_age: 最大年龄

        💡 空管理器应返回 0，避免除零错误。
        """
        ages = [s.age for s in self.students.values()]
        if not ages:
            return {"total": 0, "average_age": 0, "min_age": 0, "max_age": 0}
        total = len(ages)
        average = sum(ages) / total
        return {"total": total, "average_age": average, "min_age": min(ages), "max_age": max(ages)}


# 测试代码（完成后取消注释运行）
if __name__ == "__main__":
    manager = StudentManager()

    # 添加学员
    s1 = Student("001", "张三", 20)
    result = manager.add_student(s1)
    print(f"添加学员: {'成功' if result else '失败'}")

    # 重复添加
    s2 = Student("001", "李四", 21)
    result = manager.add_student(s2)
    print(f"重复添加: {'失败（预期）' if not result else '错误'}")

    # 获取学员
    found = manager.get_student("001")
    print(f"获取学员: {found}")

    # 更新学员
    result = manager.update_student("001", name="王五", age=22)
    print(f"更新学员: {'成功' if result else '失败'}")

    # 搜索学员
    manager.add_student(Student("002", "张三丰", 30))
    results = manager.search_by_name("张")
    print(f"搜索'张': 找到 {len(results)} 人")

    # 列出所有学员
    all_students = manager.list_students()
    print(f"总学员数: {len(all_students)}")

    # 统计信息
    stats = manager.get_statistics()
    print(f"统计信息: {stats}")

    # 删除学员
    result = manager.remove_student("001")
    print(f"删除学员: {'成功' if result else '失败'}")

    print("\n所有功能测试完成!")
