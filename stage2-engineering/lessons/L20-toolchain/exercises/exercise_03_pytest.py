"""练习 3: pytest 测试框架（中级）

from __future__ import annotations

任务：
为给定的代码编写测试用例，并达到 80% 的测试覆盖率。

学习目标：
- 理解单元测试的重要性
- 掌握 pytest 的基本使用
- 学会编写测试用例
- 理解测试覆盖率

预计时间: 1.5 小时
难度: ⭐⭐☆☆☆
"""

from pathlib import Path

# 待测试的代码
SOURCE_CODE = '''"""计算器模块"""


def add(a: int, b: int) -> int:
    """加法"""
    return a + b


def subtract(a: int, b: int) -> int:
    """减法"""
    return a - b


def multiply(a: int, b: int) -> int:
    """乘法"""
    return a * b


def divide(a: float, b: float) -> float:
    """除法"""
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b


def power(base: int, exponent: int) -> int:
    """幂运算"""
    if exponent < 0:
        raise ValueError("指数必须为非负数")
    result = 1
    for _ in range(exponent):
        result *= base
    return result


class Calculator:
    """计算器类"""

    def __init__(self):
        self.history: list[str] = []

    def calculate(self, a: float, b: float, operation: str) -> float:
        """执行计算"""
        if operation == "+":
            result = add(int(a), int(b))
        elif operation == "-":
            result = subtract(int(a), int(b))
        elif operation == "*":
            result = multiply(int(a), int(b))
        elif operation == "/":
            result = divide(a, b)
        else:
            raise ValueError(f"不支持的操作: {operation}")

        self.history.append(f"{a} {operation} {b} = {result}")
        return float(result)

    def get_history(self) -> list[str]:
        """获取计算历史"""
        return self.history.copy()

    def clear_history(self) -> None:
        """清除历史"""
        self.history.clear()
'''


def save_source_code(file_path: Path) -> None:
    """保存源代码

    TODO: 实现以下功能
    1. 创建 src 目录
    2. 将 SOURCE_CODE 写入文件
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 save_source_code 函数")


def create_test_for_add() -> str:
    """创建 add 函数的测试

    TODO: 实现以下功能
    1. 创建测试函数 test_add
    2. 测试正数相加
    3. 测试负数相加
    4. 测试零相加
    5. 返回测试代码字符串

    示例:
    def test_add():
        assert add(1, 2) == 3
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_test_for_add 函数")


def create_test_for_divide() -> str:
    """创建 divide 函数的测试

    TODO: 实现以下功能
    1. 创建测试函数 test_divide
    2. 测试正常除法
    3. 测试除以零（应该抛出异常）
    4. 返回测试代码字符串

    提示: 使用 pytest.raises() 测试异常
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_test_for_divide 函数")


def create_test_for_calculator() -> str:
    """创建 Calculator 类的测试

    TODO: 实现以下功能
    1. 创建测试函数 test_calculator
    2. 测试 calculate 方法
    3. 测试 get_history 方法
    4. 测试 clear_history 方法
    5. 返回测试代码字符串
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_test_for_calculator 函数")


def save_test_code(test_file: Path, test_code: str) -> None:
    """保存测试代码

    TODO: 实现以下功能
    1. 创建 tests 目录
    2. 将测试代码写入文件
    3. 确保包含必要的导入语句
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 save_test_code 函数")


def run_pytest(project_path: Path) -> tuple[bool, str]:
    """运行 pytest 测试

    TODO: 实现以下功能
    1. 运行 pytest 命令
    2. 返回 (是否通过, 输出结果)

    提示: pytest -v
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_pytest 函数")


def run_pytest_with_coverage(project_path: Path) -> tuple[bool, dict]:
    """运行 pytest 并生成覆盖率报告

    TODO: 实现以下功能
    1. 运行 pytest --cov=src tests/
    2. 解析覆盖率信息
    3. 返回 (是否通过, 覆盖率数据)

    返回格式: (True, {
        "coverage": 85.5,  # 覆盖率百分比
        "statements": 100,  # 总语句数
        "missing": 15       # 未覆盖的语句数
    })
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_pytest_with_coverage 函数")


def create_pytest_config(project_path: Path) -> None:
    """创建 pytest 配置

    TODO: 实现以下功能
    1. 在项目目录创建或更新 pyproject.toml
    2. 添加 pytest 配置
    3. 配置项：
       - testpaths = ["tests"]
       - python_files = ["test_*.py"]
       - addopts = ["--cov=src", "--cov-report=term-missing"]

    提示: 使用 tomli/tomli_w 库
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_pytest_config 函数")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 3: pytest 测试框架")
    print("=" * 60)
    print()

    # 创建测试目录
    project_path = Path("./pytest_test")
    src_file = project_path / "src" / "calculator.py"
    test_file = project_path / "tests" / "test_calculator.py"

    # 步骤 1: 保存源代码
    print("步骤 1: 保存源代码")
    try:
        save_source_code(src_file)
        print("✅ 源代码已保存")
        print(f"   文件位置: {src_file}")
    except NotImplementedError:
        print("❌ 请实现 save_source_code 函数")
        return
    print()

    # 步骤 2: 创建测试 - add 函数
    print("步骤 2: 创建 add 函数的测试")
    try:
        test_add_code = create_test_for_add()
        print("✅ add 测试已创建")
        print("   测试用例:")
        print("   - 正数相加")
        print("   - 负数相加")
        print("   - 零相加")
    except NotImplementedError:
        print("❌ 请实现 create_test_for_add 函数")
        return
    print()

    # 步骤 3: 创建测试 - divide 函数
    print("步骤 3: 创建 divide 函数的测试")
    try:
        test_divide_code = create_test_for_divide()
        print("✅ divide 测试已创建")
        print("   测试用例:")
        print("   - 正常除法")
        print("   - 除以零异常")
    except NotImplementedError:
        print("❌ 请实现 create_test_for_divide 函数")
        return
    print()

    # 步骤 4: 创建测试 - Calculator 类
    print("步骤 4: 创建 Calculator 类的测试")
    try:
        test_calculator_code = create_test_for_calculator()
        print("✅ Calculator 测试已创建")
        print("   测试用例:")
        print("   - calculate 方法")
        print("   - get_history 方法")
        print("   - clear_history 方法")
    except NotImplementedError:
        print("❌ 请实现 create_test_for_calculator 函数")
        return
    print()

    # 步骤 5: 保存所有测试
    print("步骤 5: 保存测试代码")
    try:
        all_tests = "\n\n".join([test_add_code, test_divide_code, test_calculator_code])
        save_test_code(test_file, all_tests)
        print("✅ 测试代码已保存")
        print(f"   文件位置: {test_file}")
    except NotImplementedError:
        print("❌ 请实现 save_test_code 函数")
        return
    print()

    # 步骤 6: 运行测试
    print("步骤 6: 运行 pytest 测试")
    try:
        passed, output = run_pytest(project_path)
        if passed:
            print("✅ 所有测试通过")
        else:
            print("❌ 部分测试失败")
            print(output)
    except NotImplementedError:
        print("❌ 请实现 run_pytest 函数")
        return
    print()

    # 步骤 7: 运行覆盖率测试
    print("步骤 7: 运行覆盖率测试")
    try:
        passed, coverage_data = run_pytest_with_coverage(project_path)
        coverage = coverage_data.get("coverage", 0)
        print(f"  覆盖率: {coverage:.1f}%")
        print(f"  总语句数: {coverage_data.get('statements', 0)}")
        print(f"  未覆盖: {coverage_data.get('missing', 0)}")

        if coverage >= 80:
            print("✅ 达到 80% 覆盖率目标！")
        else:
            print(f"⚠️  覆盖率不足 80%，还需要 {80 - coverage:.1f}%")
    except NotImplementedError:
        print("❌ 请实现 run_pytest_with_coverage 函数")
        return
    print()

    # 步骤 8: 创建 pytest 配置
    print("步骤 8: 创建 pytest 配置")
    try:
        create_pytest_config(project_path)
        config_file = project_path / "pyproject.toml"
        if config_file.exists():
            print("✅ pytest 配置已创建")
            print(f"   配置文件: {config_file}")
        else:
            print("❌ 配置文件创建失败")
    except NotImplementedError:
        print("❌ 请实现 create_pytest_config 函数")
        return
    print()

    # 总结
    print("=" * 60)
    print("🎉 恭喜！练习 3 完成！")
    print("=" * 60)
    print()
    print("你已经学会了:")
    print("  ✅ 编写单元测试")
    print("  ✅ 使用 pytest 运行测试")
    print("  ✅ 测试异常情况")
    print("  ✅ 检查测试覆盖率")
    print("  ✅ 配置 pytest")
    print()
    print("下一步:")
    print("  - 查看参考答案: solutions/03-pytest.py")
    print("  - 在自己的项目中使用 pytest")
    print("  - 学习 pytest 的高级特性（fixtures、parametrize）")
    print()
    print("🎊 L18 课程所有练习完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
