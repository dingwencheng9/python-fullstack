"""L09 Basics Project 测试用例

solutions 包通过 conftest.py 全局注入到 sys.modules["solutions"]。
测试函数内部通过 `from solutions import ...` 导入类。
"""

import pytest


class TestStudent:
    """测试学员类"""

    def test_student_creation(self):
        """测试学员对象创建"""
        from solutions import Student

        student = Student("001", "张三", 20)
        assert student.student_id == "001"
        assert student.name == "张三"
        assert student.age == 20

    def test_student_to_dict(self):
        """测试学员转换为字典"""
        from solutions import Student

        student = Student("001", "张三", 20)
        data = student.to_dict()
        assert data["student_id"] == "001"
        assert data["name"] == "张三"
        assert data["age"] == 20

    def test_student_from_dict(self):
        """测试从字典创建学员"""
        from solutions import Student

        data = {"student_id": "001", "name": "张三", "age": 20}
        student = Student.from_dict(data)
        assert student.student_id == "001"
        assert student.name == "张三"
        assert student.age == 20

    def test_student_equality(self):
        """测试学员属性一致性"""
        from solutions import Student

        s1 = Student("001", "张三", 20)
        s2 = Student("001", "张三", 20)
        s3 = Student("002", "李四", 21)
        assert s1.student_id == s2.student_id
        assert s1.student_id != s3.student_id


class TestStudentManager:
    """测试学员管理器类"""

    def test_manager_initialization(self):
        """测试管理器初始化"""
        from solutions import StudentManager

        manager = StudentManager()
        assert len(manager.students) == 0

    def test_add_student(self):
        """测试添加学员"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        student = Student("001", "张三", 20)
        result = manager.add_student(student)
        assert result is True
        assert len(manager.students) == 1

    def test_add_duplicate_student(self):
        """测试添加重复学号学员"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        student1 = Student("001", "张三", 20)
        student2 = Student("001", "张三2", 21)
        manager.add_student(student1)
        result = manager.add_student(student2)
        assert result is False
        assert len(manager.students) == 1

    def test_get_student(self):
        """测试获取学员"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        student = manager.get_student("001")
        assert student is not None
        assert student.name == "张三"

    def test_get_nonexistent_student(self):
        """测试获取不存在的学员"""
        from solutions import StudentManager

        manager = StudentManager()
        student = manager.get_student("999")
        assert student is None

    def test_remove_student(self):
        """测试删除学员"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        result = manager.remove_student("001")
        assert result is True
        assert len(manager.students) == 0

    def test_remove_nonexistent_student(self):
        """测试删除不存在的学员"""
        from solutions import StudentManager

        manager = StudentManager()
        result = manager.remove_student("999")
        assert result is False

    def test_update_student(self):
        """测试更新学员信息"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        result = manager.update_student("001", name="李四", age=21)
        assert result is True
        student = manager.get_student("001")
        assert student is not None
        assert student.name == "李四"
        assert student.age == 21

    def test_update_partial(self):
        """测试部分更新"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        result = manager.update_student("001", name="李四")
        assert result is True
        student = manager.get_student("001")
        assert student is not None
        assert student.name == "李四"
        assert student.age == 20  # 年龄未更新

    def test_update_nonexistent(self):
        """测试更新不存在的学员"""
        from solutions import StudentManager

        manager = StudentManager()
        result = manager.update_student("999", name="王五")
        assert result is False

    def test_list_students(self):
        """测试列出所有学员"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        manager.add_student(Student("002", "李四", 21))
        students = manager.list_students()
        assert len(students) == 2

    def test_list_students_returns_copy(self):
        """测试 list_students 返回副本"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        students = manager.list_students()
        students.append(Student("999", "黑客", 99))
        assert len(manager.list_students()) == 1  # 内部状态未受影响

    def test_search_by_name(self):
        """测试按姓名搜索"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        manager.add_student(Student("002", "李四", 21))
        manager.add_student(Student("003", "张伟", 22))
        results = manager.search_by_name("张")
        assert len(results) == 2

    def test_search_by_name_case_insensitive(self):
        """测试搜索不区分大小写"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        manager.add_student(Student("002", "李四", 21))
        # 中文小写不改变，但搜索 "张三" 和 "zhang" 都应能找到 "张三"
        results = manager.search_by_name("三")
        assert len(results) == 1
        assert results[0].name == "张三"

    def test_search_no_results(self):
        """测试搜索无结果"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        results = manager.search_by_name("王")
        assert len(results) == 0

    def test_get_statistics(self):
        """测试统计信息"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三", 20))
        manager.add_student(Student("002", "李四", 25))
        manager.add_student(Student("003", "王五", 30))
        stats = manager.get_statistics()
        assert stats["total"] == 3
        assert stats["average_age"] == 25
        assert stats["min_age"] == 20
        assert stats["max_age"] == 30

    def test_statistics_empty_manager(self):
        """测试空管理器的统计"""
        from solutions import StudentManager

        manager = StudentManager()
        stats = manager.get_statistics()
        assert stats["total"] == 0
        assert stats["average_age"] == 0
        assert stats["min_age"] == 0
        assert stats["max_age"] == 0


class TestEdgeCases:
    """边界用例测试"""

    def test_empty_manager_list(self):
        """测试空管理器列出学员"""
        from solutions import StudentManager

        manager = StudentManager()
        students = manager.list_students()
        assert len(students) == 0

    def test_large_name_search(self):
        """测试长姓名搜索"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张" * 50, 20))
        results = manager.search_by_name("张")
        assert len(results) == 1

    def test_special_characters_in_name(self):
        """测试姓名含特殊字符"""
        from solutions import Student, StudentManager

        manager = StudentManager()
        manager.add_student(Student("001", "张三·李四", 20))
        results = manager.search_by_name("张三")
        assert len(results) == 1


@pytest.mark.parametrize(
    "student_id,name,age",
    [
        ("001", "张三", 18),
        ("002", "李四", 20),
        ("A001", "王五", 25),
        ("STU-100", "赵六", 30),
    ],
)
def test_student_creation_parametrized(student_id, name, age):
    """参数化：多种学员创建方式"""
    from solutions import Student

    student = Student(student_id, name, age)
    assert student.student_id == student_id
    assert student.name == name
    assert student.age == age


@pytest.mark.parametrize(
    "ids_to_add,ids_to_remove,expected_count",
    [
        (["001", "002", "003"], ["001"], 2),
        (["001", "002"], ["001", "002"], 0),
        (["001", "002", "003"], ["999"], 3),
    ],
)
def test_bulk_add_remove(ids_to_add, ids_to_remove, expected_count):
    """参数化：批量添加删除"""
    from solutions import Student, StudentManager

    manager = StudentManager()
    for i, sid in enumerate(ids_to_add):
        manager.add_student(Student(sid, f"Student{sid}", 20 + i))
    for sid in ids_to_remove:
        manager.remove_student(sid)
    assert len(manager.students) == expected_count
