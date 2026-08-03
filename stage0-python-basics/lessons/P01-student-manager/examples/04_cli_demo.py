"""示例4: 学员管理系统 CLI 完整演示

整合所有功能模块，展示完整的命令行交互流程。
这是一个自包含的完整示例，展示了如何将数据持久化与 CLI 结合。
"""

import json
from pathlib import Path


class Student:
    """学员数据模型"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"Student({self.student_id!r}, {self.name!r}, {self.age})"

    def __str__(self) -> str:
        """友好字符串表示"""
        return f"Student(id={self.student_id}, name={self.name}, age={self.age})"

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


class StudentManager:
    """学员管理器（带文件持久化）"""

    def __init__(self, storage_path: Path | str = "students.json") -> None:
        self.storage_path = Path(storage_path)
        self.students: dict[str, Student] = {}

    def add_student(self, student: Student) -> bool:
        """添加学员"""
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def get_student(self, student_id: str) -> Student | None:
        """获取学员"""
        return self.students.get(student_id)

    def delete_student(self, student_id: str) -> bool:
        """删除学员"""
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
        """更新学员信息"""
        if student_id not in self.students:
            return False
        student = self.students[student_id]
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        return True

    def list_students(self) -> list[Student]:
        """列出所有学员"""
        return list(self.students.values())

    def search_by_name(self, name: str) -> list[Student]:
        """按姓名搜索"""
        name_lower = name.lower()
        return [s for s in self.students.values() if name_lower in s.name.lower()]

    def save(self) -> bool:
        """保存到文件"""
        try:
            data = [s.to_dict() for s in self.students.values()]
            self.storage_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            return True
        except Exception:
            return False

    def load(self) -> bool:
        """从文件加载"""
        if not self.storage_path.exists():
            return False
        try:
            content = self.storage_path.read_text(encoding="utf-8")
            data = json.loads(content)
            self.students = {item["student_id"]: Student.from_dict(item) for item in data}
            return True
        except Exception:
            return False

    def clear(self) -> None:
        """清空所有学员"""
        self.students.clear()


def print_header(text: str) -> None:
    """打印分隔标题。"""
    print(f"\n{'=' * 50}")
    print(f" {text}")
    print("=" * 50)


def print_student(s: Student) -> None:
    """打印学员信息。"""
    print(f"  学号: {s.student_id} | 姓名: {s.name} | 年龄: {s.age}")


def main() -> None:
    """学员管理系统主函数。"""
    # 初始化管理器
    storage_path = Path("students_demo.json")
    manager = StudentManager(storage_path)

    print_header("学员管理系统 v1.0")
    print("输入 help 查看命令帮助")

    while True:
        try:
            cmd = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 再见！")
            break

        if not cmd:
            continue

        # 解析命令
        parts = cmd.split()
        action = parts[0]

        # ---- help ----
        if action == "help":
            print(
                """
命令帮助:
  add <学号> <姓名> <年龄>  - 添加学员
  list                          - 显示所有学员
  get <学号>                    - 查询学员
  search <姓名>                 - 按姓名搜索
  update <学号> [name=<姓名>] [age=<年龄>] - 更新学员
  delete <学号>                 - 删除学员
  save                          - 保存到文件
  load                          - 从文件加载
  clear                         - 清空所有学员
  exit                          - 退出程序
  help                          - 显示帮助
            """.strip()
            )

        # ---- add ----
        elif action == "add":
            if len(parts) != 4:
                print("用法: add <学号> <姓名> <年龄>")
                continue

            student_id, name, age_str = parts[1], parts[2], parts[3]
            try:
                age = int(age_str)
            except ValueError:
                print("❌ 年龄必须是整数")
                continue

            student = Student(student_id, name, age)
            if manager.add_student(student):
                print(f"✅ 已添加: {name} ({student_id})")
            else:
                print(f"❌ 学号 {student_id} 已存在")

        # ---- list ----
        elif action == "list":
            students = manager.list_students()
            if not students:
                print("📭 暂无学员记录")
            else:
                print_header(f"学员列表 (共 {len(students)} 人)")
                for s in students:
                    print_student(s)

        # ---- get ----
        elif action == "get":
            if len(parts) != 2:
                print("用法: get <学号>")
                continue

            student = manager.get_student(parts[1])
            if student:
                print_header("学员详情")
                print_student(student)
            else:
                print(f"❌ 未找到学号: {parts[1]}")

        # ---- search ----
        elif action == "search":
            if len(parts) != 2:
                print("用法: search <姓名>")
                continue

            results = manager.search_by_name(parts[1])
            if not results:
                print(f"📭 未找到姓名包含 '{parts[1]}' 的学员")
            else:
                print_header(f"搜索结果 (共 {len(results)} 人)")
                for s in results:
                    print_student(s)

        # ---- update ----
        elif action == "update":
            if len(parts) < 2:
                print("用法: update <学号> [name=<姓名>] [age=<年龄>]")
                continue

            student_id = parts[1]
            name = None
            age = None

            for part in parts[2:]:
                if part.startswith("name="):
                    name = part[5:]
                elif part.startswith("age="):
                    try:
                        age = int(part[4:])
                    except ValueError:
                        print("❌ 年龄必须是整数")
                        continue

            if name is None and age is None:
                print("❌ 至少需要提供 name= 或 age= 参数")
                continue

            if manager.update_student(student_id, name=name, age=age):
                print(f"✅ 已更新学号: {student_id}")
            else:
                print(f"❌ 未找到学号: {student_id}")

        # ---- delete ----
        elif action == "delete":
            if len(parts) != 2:
                print("用法: delete <学号>")
                continue

            if manager.delete_student(parts[1]):
                print(f"✅ 已删除学号: {parts[1]}")
            else:
                print(f"❌ 未找到学号: {parts[1]}")

        # ---- save ----
        elif action == "save":
            if manager.save():
                print(f"✅ 已保存到 {storage_path}")
            else:
                print("❌ 保存失败")

        # ---- load ----
        elif action == "load":
            if manager.load():
                count = len(manager.list_students())
                print(f"✅ 已从 {storage_path} 加载 ({count} 人)")
            else:
                print("❌ 加载失败或文件不存在")

        # ---- clear ----
        elif action == "clear":
            confirm = input("确认清空所有学员? (y/N): ").strip().lower()
            if confirm == "y":
                manager.clear()
                print("✅ 已清空所有学员")
            else:
                print("已取消")

        # ---- exit ----
        elif action in ("exit", "quit", "q"):
            # 自动保存
            if manager.save():
                print(f"💾 已自动保存到 {storage_path}")
            print("👋 再见！")
            break

        else:
            print(f"❌ 未知命令: {action}，输入 help 查看帮助")


if __name__ == "__main__":
    main()
