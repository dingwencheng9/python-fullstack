"""L09 练习2参考答案: 数据验证与错误处理"""

from typing import Any


class ValidationError(Exception):
    """数据验证失败异常"""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"验证失败 [{field}]: {message}")


class NotFoundError(Exception):
    """资源未找到异常"""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"未找到 {resource}: {identifier}")


class StudentValidator:
    """学员数据验证器"""

    @staticmethod
    def validate_student_id(student_id: str) -> None:
        if not student_id:
            raise ValidationError("student_id", "ID 不能为空")
        if not isinstance(student_id, str):
            raise ValidationError("student_id", "ID 必须是字符串")
        if not student_id.startswith("S"):
            raise ValidationError("student_id", "ID 必须以 'S' 开头")
        if not student_id[1:].isdigit():
            raise ValidationError("student_id", "ID 格式必须是 'S' + 数字")

    @staticmethod
    def validate_name(name: str) -> None:
        if not name:
            raise ValidationError("name", "姓名不能为空")
        if not isinstance(name, str):
            raise ValidationError("name", "姓名必须是字符串")
        if len(name) < 2:
            raise ValidationError("name", "姓名长度至少 2 个字符")
        if len(name) > 50:
            raise ValidationError("name", "姓名长度不能超过 50 个字符")

    @staticmethod
    def validate_age(age: int | Any) -> None:
        if not isinstance(age, int):
            raise ValidationError("age", "年龄必须是整数")
        if age < 18:
            raise ValidationError("age", "年龄不能小于 18")
        if age > 100:
            raise ValidationError("age", "年龄不能超过 100")


class Student:
    """学员数据类（手动实现，等价于 dataclass）"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        # 数据验证（替代 @dataclass 的 __post_init__）
        StudentValidator.validate_student_id(student_id)
        StudentValidator.validate_name(name)
        StudentValidator.validate_age(age)
        self.student_id = student_id
        self.name = name
        self.age = age

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
        )


class StudentManagerWithValidation:
    """带验证的学员管理器"""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, data: dict) -> Student:
        student = Student.from_dict(data)
        if student.student_id in self.students:
            raise ValidationError("student_id", "学员 ID 已存在")
        self.students[student.student_id] = student
        return student

    def update_student(self, student_id: str, data: dict) -> Student:
        if student_id not in self.students:
            raise NotFoundError("学员", student_id)
        current = self.students[student_id]
        updated_data = {
            "student_id": data.get("student_id", current.student_id),
            "name": data.get("name", current.name),
            "age": data.get("age", current.age),
        }
        student = Student.from_dict(updated_data)
        self.students[student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        if student_id not in self.students:
            raise NotFoundError("学员", student_id)
        return self.students[student_id]
