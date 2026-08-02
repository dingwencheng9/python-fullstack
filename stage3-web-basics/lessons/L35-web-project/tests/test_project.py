"""L35 综合项目 - 测试文件"""

from __future__ import annotations


class TestProjectStructure:
    """测试项目结构"""

    def test_solution_01_import(self, solutions) -> None:
        """测试 solution_01 可以导入"""
        assert hasattr(solutions, "solution_01"), "solution_01 模块未找到"

    def test_solution_02_import(self, solutions) -> None:
        """测试 solution_02 可以导入"""
        assert hasattr(solutions, "solution_02"), "solution_02 模块未找到"

    def test_solution_03_import(self, solutions) -> None:
        """测试 solution_03 可以导入"""
        assert hasattr(solutions, "solution_03"), "solution_03 模块未找到"


class TestDataModels:
    """测试数据模型"""

    def test_user_model_structure(self, solutions) -> None:
        """测试 User 模型结构"""
        from solutions import solution_02

        # 验证模型定义了正确的属性
        assert hasattr(solution_02, "User"), "User 模型未定义"
        assert hasattr(solution_02, "Task"), "Task 模型未定义"


class TestAPIEndpoints:
    """测试 API 端点"""

    def test_solution_03_has_routes(self, solutions) -> None:
        """测试 API 路由定义"""
        from solutions import solution_03

        # 验证路由定义
        assert hasattr(solution_03, "users_router"), "users_router 未定义"
        assert hasattr(solution_03, "tasks_router"), "tasks_router 未定义"
