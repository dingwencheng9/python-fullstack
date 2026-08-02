"""练习 3: pytest 测试框架 - 参考答案

from __future__ import annotations

本文件提供练习 3 的完整实现，展示如何使用 pytest 编写测试。

【解题思路】
1. save_source_code():
   - 创建 src/ 目录并保存待测试的源代码（calculator.py）
2. create_test_for_add():
   - 返回测试 add() 函数的测试代码字符串
   - 使用 assert 断言验证结果
   - 覆盖多种场景：正数、负数、零
3. create_test_for_divide():
   - 测试除法函数，包括正常情况和异常情况
   - 使用 pytest.raises(ValueError) 测试异常抛出
4. create_test_for_calculator_class():
   - 测试 Calculator 类的多个方法
   - 使用 fixture 或直接实例化对象
   - 测试状态变化（history 列表）
5. create_complete_test_file():
   - 将所有测试组合成完整的测试文件
   - 添加必要的 import 语句
6. run_pytest():
   - subprocess.run(["pytest", "-v", str(test_dir)]) 执行测试
   - -v 参数显示详细输出
   - 解析输出统计通过/失败的测试数量
7. main():
   - 流程：保存源代码 → 创建测试文件 → 运行 pytest → 显示结果

【关键知识点】
- pytest 测试函数命名：test_* 前缀
- assert 语句替代 unittest 的 assertEqual
- pytest.raises(Exception) 上下文管理器测试异常
- 测试覆盖：正常路径 + 边界情况 + 异常情况
- pytest -v 显示详细输出，-k 过滤测试
- 测试文件命名：test_*.py 或 *_test.py
"""

import re
import subprocess
from pathlib import Path

# 待测试的源代码
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
    """保存源代码"""
    # 创建 src 目录
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入源代码
    file_path.write_text(SOURCE_CODE)
    print(f"✅ 源代码已保存到: {file_path}")


def create_test_for_add() -> str:
    """创建 add 函数的测试"""
    return '''def test_add():
    """测试加法函数"""
    from src.calculator import add

    # 测试正数相加
    assert add(1, 2) == 3
    assert add(10, 20) == 30

    # 测试负数相加
    assert add(-1, 1) == 0
    assert add(-5, -3) == -8

    # 测试零相加
    assert add(0, 0) == 0
    assert add(5, 0) == 5
'''


def create_test_for_divide() -> str:
    """创建 divide 函数的测试"""
    return '''def test_divide():
    """测试除法函数"""
    import pytest
    from src.calculator import divide

    # 测试正常除法
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(1, 2) == 0.5

    # 测试除以零（应该抛出异常）
    with pytest.raises(ValueError, match="除数不能为 0"):
        divide(10, 0)

    with pytest.raises(ValueError):
        divide(5, 0)
'''


def create_test_for_calculator() -> str:
    """创建 Calculator 类的测试"""
    return '''def test_calculator():
    """测试 Calculator 类"""
    from src.calculator import Calculator

    # 创建计算器实例
    calc = Calculator()

    # 测试 calculate 方法 - 加法
    result = calc.calculate(5, 3, "+")
    assert result == 8.0

    # 测试 calculate 方法 - 减法
    result = calc.calculate(10, 4, "-")
    assert result == 6.0

    # 测试 calculate 方法 - 乘法
    result = calc.calculate(6, 7, "*")
    assert result == 42.0

    # 测试 calculate 方法 - 除法
    result = calc.calculate(15, 3, "/")
    assert result == 5.0

    # 测试 get_history 方法
    history = calc.get_history()
    assert len(history) == 4
    assert "5.0 + 3.0 = 8.0" in history
    assert "10.0 - 4.0 = 6.0" in history

    # 测试 clear_history 方法
    calc.clear_history()
    assert len(calc.get_history()) == 0

    # 测试不支持的操作
    import pytest
    with pytest.raises(ValueError, match="不支持的操作"):
        calc.calculate(1, 2, "%")
'''


def save_test_code(test_file: Path, test_code: str) -> None:
    """保存测试代码"""
    # 创建 tests 目录
    test_file.parent.mkdir(parents=True, exist_ok=True)

    # 添加必要的导入和头部
    full_test_code = (
        '''"""
测试计算器模块

这个文件包含了所有计算器功能的测试用例。
"""

from pathlib import Path

# 添加 src 到 Python 路径

'''
        + test_code
    )

    # 写入测试代码
    test_file.write_text(full_test_code)
    print(f"✅ 测试代码已保存到: {test_file}")


def run_pytest(project_path: Path) -> tuple[bool, str]:
    """运行 pytest 测试"""
    try:
        # 运行 pytest -v
        result = subprocess.run(
            ["pytest", "-v", "tests/"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        # 返回是否通过和输出
        passed = result.returncode == 0
        output = result.stdout + "\n" + result.stderr

        return (passed, output)

    except FileNotFoundError:
        return (False, "pytest 未安装，请运行: uv add --dev pytest")
    except subprocess.TimeoutExpired:
        return (False, "测试超时")
    except Exception as e:
        return (False, str(e))


def run_pytest_with_coverage(project_path: Path) -> tuple[bool, dict]:
    """运行 pytest 并生成覆盖率报告"""
    try:
        # 运行 pytest --cov=src tests/
        result = subprocess.run(
            ["pytest", "--cov=src", "--cov-report=term-missing", "tests/"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        # 解析覆盖率信息
        output = result.stdout
        coverage_data = {"coverage": 0.0, "statements": 0, "missing": 0}

        # 查找覆盖率百分比
        # 格式: src/calculator.py    85%    100    15
        coverage_match = re.search(r"(\d+)%", output)
        if coverage_match:
            coverage_data["coverage"] = float(coverage_match.group(1))

        # 查找语句数
        # TOTAL                      100    15    85%
        total_match = re.search(r"TOTAL\s+(\d+)\s+(\d+)\s+(\d+)%", output)
        if total_match:
            coverage_data["statements"] = int(total_match.group(1))
            coverage_data["missing"] = int(total_match.group(2))

        passed = result.returncode == 0
        return (passed, coverage_data)

    except FileNotFoundError:
        return (
            False,
            {
                "coverage": 0.0,
                "statements": 0,
                "missing": 0,
                "error": "pytest-cov 未安装，请运行: uv add --dev pytest-cov",
            },
        )
    except Exception as e:
        return (
            False,
            {"coverage": 0.0, "statements": 0, "missing": 0, "error": str(e)},
        )


def create_pytest_config(project_path: Path) -> None:
    """创建 pytest 配置"""
    try:
        import tomli_w
    except ImportError:
        print("❌ 错误: tomli_w 未安装，请运行: uv add --dev tomli-w")
        return

    # pytest 配置
    config = {
        "tool": {
            "pytest": {
                "ini_options": {
                    "testpaths": ["tests"],
                    "python_files": ["test_*.py"],
                    "python_classes": ["Test*"],
                    "python_functions": ["test_*"],
                    "addopts": [
                        "--cov=src",
                        "--cov-report=term-missing",
                        "--cov-report=html",
                        "-v",
                    ],
                }
            }
        }
    }

    # 配置文件路径
    config_file = project_path / "pyproject.toml"

    # 如果文件已存在，读取并合并
    if config_file.exists():
        try:
            import tomli

            with config_file.open("rb") as f:
                existing_config = tomli.load(f)

            # 合并配置
            if "tool" not in existing_config:
                existing_config["tool"] = {}
            existing_config["tool"]["pytest"] = config["tool"]["pytest"]
            config = existing_config
        except ImportError:
            print("⚠️  tomli 未安装，将覆盖现有配置")

    # 写入配置
    with config_file.open("wb") as f:
        tomli_w.dump(config, f)

    print(f"✅ pytest 配置已写入: {config_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 3: pytest 测试框架 - 参考答案")
    print("=" * 60)
    print()

    # 创建测试目录
    project_path = Path("./pytest_test")
    src_file = project_path / "src" / "calculator.py"
    test_file = project_path / "tests" / "test_calculator.py"

    # 创建 __init__.py 文件
    (project_path / "src" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
    (project_path / "src" / "__init__.py").touch()
    (project_path / "tests" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
    (project_path / "tests" / "__init__.py").touch()

    # 步骤 1: 保存源代码
    print("步骤 1: 保存源代码")
    save_source_code(src_file)
    print()

    # 步骤 2-4: 创建测试
    print("步骤 2-4: 创建测试用例")
    test_add_code = create_test_for_add()
    test_divide_code = create_test_for_divide()
    test_calculator_code = create_test_for_calculator()

    print("✅ add 测试已创建（3 组测试）")
    print("✅ divide 测试已创建（包含异常测试）")
    print("✅ Calculator 测试已创建（完整功能测试）")
    print()

    # 步骤 5: 保存所有测试
    print("步骤 5: 保存测试代码")
    all_tests = "\n\n".join([test_add_code, test_divide_code, test_calculator_code])
    save_test_code(test_file, all_tests)
    print()

    # 步骤 6: 运行测试
    print("步骤 6: 运行 pytest 测试")
    passed, output = run_pytest(project_path)
    if passed:
        print("✅ 所有测试通过")
        # 显示部分输出
        lines = output.splitlines()
        for line in lines:
            if "test_" in line or "passed" in line.lower():
                print(f"   {line}")
    else:
        print("❌ 部分测试失败")
        print(output[:500])  # 只显示前 500 字符
    print()

    # 步骤 7: 运行覆盖率测试
    print("步骤 7: 运行覆盖率测试")
    passed, coverage_data = run_pytest_with_coverage(project_path)

    if "error" in coverage_data:
        print(f"❌ 错误: {coverage_data['error']}")
    else:
        coverage = coverage_data.get("coverage", 0)
        print(f"  覆盖率: {coverage:.1f}%")
        print(f"  总语句数: {coverage_data.get('statements', 0)}")
        print(f"  未覆盖: {coverage_data.get('missing', 0)}")

        if coverage >= 80:
            print("  ✅ 达到 80% 覆盖率目标！")
        else:
            print(f"  ⚠️  覆盖率不足 80%，还需要 {80 - coverage:.1f}%")
    print()

    # 步骤 8: 创建 pytest 配置
    print("步骤 8: 创建 pytest 配置")
    create_pytest_config(project_path)
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
    print("测试的重要性:")
    print("  - 提前发现 bug")
    print("  - 提高代码质量")
    print("  - 便于重构")
    print("  - 作为代码文档")
    print()
    print("下一步:")
    print("  - 学习 pytest fixtures（测试夹具）")
    print("  - 学习 pytest parametrize（参数化测试）")
    print("  - 学习测试覆盖率分析")
    print("  - 集成到 CI/CD 流程")
    print()
    print("🎊 L18 课程所有练习完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
