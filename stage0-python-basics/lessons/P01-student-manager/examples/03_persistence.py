"""示例3: 文件持久化（JSON）

使用类 + json 实现数据的持久化存储。
"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory


class Student:
    """学员数据模型"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Student({self.student_id!r}, {self.name!r}, {self.age})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id

    def __hash__(self) -> int:
        return hash(self.student_id)

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


class StudentStorage:
    """学员数据持久化"""

    def __init__(self, filepath: str | Path = "students.json") -> None:
        self.filepath = Path(filepath)

    def save(self, students: list[Student]) -> None:
        """保存学员列表到文件"""
        data = [s.to_dict() for s in students]
        self.filepath.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"✅ 已保存 {len(students)} 名学员到 {self.filepath}")

    def load(self) -> list[Student]:
        """从文件加载学员列表"""
        if not self.filepath.exists():
            print("📁 文件不存在，返回空列表")
            return []

        try:
            content = self.filepath.read_text(encoding="utf-8")
            data = json.loads(content)
            students = [Student.from_dict(item) for item in data]
            print(f"📂 已加载 {len(students)} 名学员")
            return students
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}，返回空列表")
            return []
        except Exception as e:
            print(f"❌ 加载失败: {e}，返回空列表")
            return []


# 使用示例
if __name__ == "__main__":
    # 使用临时目录，避免运行示例后在仓库中留下 students.json。
    with TemporaryDirectory() as tmpdir:
        storage = StudentStorage(Path(tmpdir) / "students.json")

        # 创建学员
        students = [
            Student("001", "张三", 20),
            Student("002", "李四", 21),
            Student("003", "王五", 19),
        ]

        # 保存
        storage.save(students)

        # 模拟程序重启后加载
        print()
        loaded = storage.load()
        for s in loaded:
            print(f"  {s}")
