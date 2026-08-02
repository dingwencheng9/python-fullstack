"""L09 基础实战参考答案包"""

from . import student_manager

__all__ = [
    "Student",
    "StudentManager",
    "student_manager",
]

# 动态导出类
Student = student_manager.Student
StudentManager = student_manager.StudentManager
