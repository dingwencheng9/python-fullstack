"""L09 练习2: 数据验证与错误处理

难度: ⭐⭐⭐⭐☆ (较难)
预计时间: 45 分钟
知识点: 数据验证、异常处理、自定义异常、防御性编程

任务描述:
为学员管理系统添加健壮的数据验证机制。

练习内容:
1. 定义自定义异常类（ValidationError、NotFoundError）
2. 实现数据验证器（StudentValidator）
3. 为 Student 类添加验证逻辑
4. 实现安全的 CRUD 操作（带异常处理）

自定义异常设计:
    class ValidationError(Exception):
        '''数据验证失败'''
        pass

    class NotFoundError(Exception):
        '''资源未找到'''
        pass

验证规则:
    - student_id: 非空字符串，格式为 "S" + 数字
    - name: 非空字符串，长度 2-50
    - age: 整数，范围 18-100
"""

from typing import Any


# TODO: 1. 定义自定义异常类
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


# TODO: 2. 定义数据验证器
class StudentValidator:
    """学员数据验证器"""

    @staticmethod
    def validate_student_id(student_id: str) -> None:
        """验证学员 ID 格式

        规则:
        - 非空字符串
        - 格式: "S" + 数字（如 "S001", "S12345"）
        """
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
        """验证姓名

        规则:
        - 非空字符串
        - 长度 2-50
        """
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
        """验证年龄

        规则:
        - 整数
        - 范围 18-100
        """
        if not isinstance(age, int):
            raise ValidationError("age", "年龄必须是整数")
        if age < 18:
            raise ValidationError("age", "年龄不能小于 18")
        if age > 100:
            raise ValidationError("age", "年龄不能超过 100")


# TODO: 3. 定义带验证的 Student 类
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
        """转换为字典"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建（带验证）"""
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
        )


# TODO: 4. 实现带异常处理的 StudentManager
class StudentManagerWithValidation:
    """带验证的学员管理器"""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, data: dict) -> Student:
        """添加学员（带验证）

        Raises:
            ValidationError: 数据验证失败
        """
        student = Student.from_dict(data)
        if student.student_id in self.students:
            raise ValidationError("student_id", "学员 ID 已存在")
        self.students[student.student_id] = student
        return student

    def update_student(self, student_id: str, data: dict) -> Student:
        """更新学员（带验证）

        Raises:
            NotFoundError: 学员不存在
            ValidationError: 数据验证失败
        """
        if student_id not in self.students:
            raise NotFoundError("学员", student_id)
        # 合并数据并验证
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
        """获取学员

        Raises:
            NotFoundError: 学员不存在
        """
        if student_id not in self.students:
            raise NotFoundError("学员", student_id)
        return self.students[student_id]


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== 数据验证与错误处理练习测试 ===\n")

    manager = StudentManagerWithValidation()

    # 测试正常添加
    print("1. 测试正常添加:")
    try:
        student = manager.add_student(
            {
                "student_id": "S001",
                "name": "张三",
                "age": 20,
            }
        )
        print(f"   添加成功: {student}")
    except ValidationError as e:
        print(f"   验证失败: {e}")

    # 测试重复 ID
    print("\n2. 测试重复 ID:")
    try:
        manager.add_student(
            {
                "student_id": "S001",  # 已存在
                "name": "李四",
                "age": 22,
            }
        )
        print("   应该抛出异常")
    except ValidationError as e:
        print(f"   正确捕获: {e}")

    # 测试无效数据
    print("\n3. 测试无效数据:")
    invalid_cases = [
        {"student_id": "", "name": "测试", "age": 20},  # 空 ID
        {"student_id": "123", "name": "测试", "age": 20},  # ID 格式错误
        {"student_id": "S002", "name": "X", "age": 20},  # 姓名太短
        {"student_id": "S002", "name": "测试", "age": 10},  # 年龄太小
    ]
    for data in invalid_cases:
        try:
            manager.add_student(data)
            print(f"   应拒绝: {data}")
        except ValidationError as e:
            print(f"   正确拒绝: {e}")

    # 测试更新不存在的学员
    print("\n4. 测试更新不存在的学员:")
    try:
        manager.update_student("S999", {"name": "王五"})
        print("   应该抛出异常")
    except NotFoundError as e:
        print(f"   正确捕获: {e}")
