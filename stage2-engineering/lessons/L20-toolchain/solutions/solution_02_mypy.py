"""练习 2: mypy 类型检查 - 参考答案（Python 3.13+ 现代化版本）

from __future__ import annotations

本文件提供练习 2 的完整实现，展示如何使用 mypy 进行类型检查。

【解题思路】
1. save_code_without_types():
   - 保存一份无类型注解的代码作为起点
2. add_basic_types():
   - 使用字符串替换 str.replace() 为函数签名添加简单类型注解
   - ✅ 使用 Python 3.9+ 内置泛型：list, dict（不再导入 typing.List/Dict）
   - ✅ 使用 Python 3.10+ 联合类型语法：X | None（不再使用 Optional）
   - 处理基础类型：str, int, float, bool
3. add_complex_types():
   - 添加复杂类型注解：list[dict[str, str | int]]（现代语法）
   - X | None 表示可能为 None（替代 Optional[X]）
   - X | Y 表示联合类型（替代 Union[X, Y]）
   - 为类属性添加类型注解（self.attr: Type = value）
4. run_mypy_check():
   - subprocess.run(["mypy", str(file_path)]) 执行类型检查
   - 返回码 0 表示无类型错误
   - 解析 stderr 输出，提取错误信息列表
   - 返回 tuple[bool, list[str]]：(是否通过, 错误列表)
5. main():
   - 流程：无类型 → 基础类型 → 复杂类型 → 每步运行 mypy 检查
   - 展示类型注解如何逐步消除 mypy 错误

【关键知识点 - Python 3.13+ 现代化版本】
- 类型注解语法：def func(param: Type) -> ReturnType:
- ✅ 内置泛型（Python 3.9+）：list[T], dict[K, V], set[T], tuple[T, ...]
- ✅ 联合类型（Python 3.10+）：X | Y 替代 Union[X, Y]
- ✅ 可选类型（Python 3.10+）：X | None 替代 Optional[X]
- ❌ 不再使用：typing.List, typing.Dict, typing.Optional, typing.Union
- typing.Any 仍需导入（当类型真的不确定时使用）
- mypy 检查规则：--strict 模式要求所有函数都有类型注解
- 类属性类型注解：self.attr: Type = value
- mypy 输出格式：file:line: error: message

【Python 3.13 并发安全注释】
本代码为单线程教学示例，无需特别考虑 Free-threading。
若在生产环境使用 Python 3.14（无 GIL 版本），需注意：
- 列表/字典的并发修改需要加锁保护
- 可使用 threading.Lock 或 asyncio.Lock 保护共享状态
"""

import re
import subprocess
from pathlib import Path

# 无类型注解的代码示例
SAMPLE_CODE_NO_TYPES = '''def greet(name):
    """问候用户"""
    return f"Hello, {name}"


def calculate_total(prices):
    """计算总价"""
    total = 0
    for price in prices:
        total += price
    return total


def find_user(users, user_id):
    """查找用户"""
    for user in users:
        if user["id"] == user_id:
            return user
    return None


class UserManager:
    def __init__(self, database_url):
        self.database_url = database_url
        self.users = []

    def add_user(self, name, age):
        user = {"name": name, "age": age, "id": len(self.users) + 1}
        self.users.append(user)
        return user

    def get_user(self, user_id):
        return find_user(self.users, user_id)
'''


def save_code_without_types(file_path: Path) -> None:
    """保存无类型注解的代码"""
    # 创建父目录
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入代码
    file_path.write_text(SAMPLE_CODE_NO_TYPES)
    print(f"✅ 代码已保存到: {file_path}")


def add_basic_types(code: str) -> str:
    """添加基础类型注解（Python 3.10+ 现代语法）"""
    # 为 greet 函数添加类型注解
    code = code.replace("def greet(name):", "def greet(name: str) -> str:")

    # 为 calculate_total 函数添加类型注解
    # ✅ 使用 list[float] 而不是 List[float]
    return code.replace(
        "def calculate_total(prices):",
        "def calculate_total(prices: list[float]) -> float:",
    )

    # ✅ 不需要导入 typing.List/Dict/Optional/Union
    # Python 3.9+ 内置泛型和 Python 3.10+ 联合类型语法已足够


def add_complex_types(code: str) -> str:
    """添加复杂类型注解（Python 3.10+ 现代语法）"""
    # 为 find_user 函数添加类型注解
    # ✅ 使用 list[dict[str, str | int]] 和 X | None
    # ❌ 不再使用 List[Dict[str, Union[str, int]]] 和 Optional
    code = code.replace(
        "def find_user(users, user_id):",
        ("def find_user(users: list[dict[str, str | int]], user_id: int) -> dict[str, str | int] | None:"),
    )

    # 为 UserManager.__init__ 添加类型注解
    code = code.replace(
        "def __init__(self, database_url):",
        "def __init__(self, database_url: str) -> None:",
    )

    # 为 UserManager.add_user 添加类型注解
    code = code.replace(
        "def add_user(self, name, age):",
        "def add_user(self, name: str, age: int) -> dict[str, str | int]:",
    )

    # 为 UserManager.get_user 添加类型注解
    code = code.replace(
        "def get_user(self, user_id):",
        "def get_user(self, user_id: int) -> dict[str, str | int] | None:",
    )

    # 添加类属性类型注解
    return code.replace(
        "self.database_url = database_url\n        self.users = []",
        ("self.database_url: str = database_url\n        self.users: list[dict[str, str | int]] = []"),
    )


def run_mypy_check(file_path: Path) -> tuple[bool, list[str]]:
    """运行 mypy 类型检查"""
    try:
        # 运行 mypy 命令
        result = subprocess.run(
            ["mypy", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # 返回码为 0 表示没有问题
        if result.returncode == 0:
            return (True, [])
        # 解析错误信息
        errors = []
        for line in result.stdout.splitlines():
            if "error:" in line:
                errors.append(line.strip())

        return (False, errors)

    except FileNotFoundError:
        return (False, ["mypy 未安装"])
    except subprocess.TimeoutExpired:
        return (False, ["命令超时"])
    except Exception as e:
        return (False, [str(e)])


def fix_mypy_errors(code: str, errors: list[str]) -> str:
    """根据 mypy 错误自动修复代码"""
    # 这是一个简化的自动修复示例
    # 实际项目中，建议手动修复或使用专业工具

    fixed_code = code

    for error in errors:
        # 示例：修复 "Missing return statement"
        if "Missing return statement" in error:
            # 提取函数名
            match = re.search(r'in function "(\w+)"', error)
            if match:
                func_name = match.group(1)
                # 在函数末尾添加 return None
                fixed_code = fixed_code.replace(
                    f"def {func_name}",
                    f"def {func_name}",  # 这里只是示例，实际修复更复杂
                )

    return fixed_code


def show_type_evolution() -> None:
    """展示类型注解的演进（Python 3.8 → 3.13+）"""
    print("\n\n📚 Python 类型注解演进史")
    print("=" * 70)

    examples = [
        (
            "Python 3.5-3.8",
            ("from typing import List, Dict, Optional\ndef func(items: List[str]) -> Optional[Dict[str, int]]:"),
        ),
        (
            "Python 3.9+",
            "# 内置泛型\ndef func(items: list[str]) -> dict[str, int] | None:  # 还需要 Optional",
        ),
        (
            "Python 3.10+",
            "# 联合类型\ndef func(items: list[str]) -> dict[str, int] | None:  # ✅ 完全现代化",
        ),
        (
            "Python 3.13",
            "# PEP 695 泛型语法\ndef process[T](items: list[T]) -> T | None:  # 类型参数",
        ),
        (
            "Python 3.13+",
            "# 改进的错误消息 + 更好的类型推导\n# 新增：类型参数默认值、TypeIs、@override 装饰器",
        ),
    ]

    for version, example in examples:
        print(f"\n{version}:")
        print(f"  {example}")

    print("\n\n💡 最佳实践（Python 3.10+）:")
    print("  ✅ 使用 list[T], dict[K,V], set[T], tuple[T, ...]")
    print("  ✅ 使用 X | Y 表示联合类型")
    print("  ✅ 使用 X | None 表示可选类型")
    print("  ❌ 不再导入 typing.List, Dict, Optional, Union")
    print("  ⚠️  typing.Any 仍需导入（类型真的不确定时使用）")

    print("\n\n🆕 Python 3.13 新特性:")
    print("  - 更清晰的类型错误消息（指向具体位置）")
    print("  - 类型参数默认值：def func[T = int](x: T) -> T:")
    print("  - TypeIs 类型守卫（比 TypeGuard 更精确）")
    print("  - @override 装饰器（明确标记重写方法）")
    print("  - 改进的泛型类型推导性能")


def create_mypy_config(project_path: Path) -> None:
    """创建 mypy 配置文件"""
    try:
        import tomli_w
    except ImportError:
        print("❌ 错误: tomli_w 未安装，请运行: uv add --dev tomli-w")
        return

    # mypy 配置
    config = {
        "tool": {
            "mypy": {
                "python_version": "3.13",
                "strict": True,
                "warn_return_any": True,
                "warn_unused_configs": True,
                "disallow_untyped_defs": True,
                "ignore_missing_imports": True,
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
            existing_config["tool"]["mypy"] = config["tool"]["mypy"]
            config = existing_config
        except ImportError:
            print("⚠️  tomli 未安装，将覆盖现有配置")

    # 写入配置
    with config_file.open("wb") as f:
        tomli_w.dump(config, f)

    print(f"✅ mypy 配置已写入: {config_file}")


def analyze_type_coverage(file_path: Path) -> dict[str, int | float]:
    """分析代码的类型覆盖率（简化版本）"""
    import ast

    try:
        code = file_path.read_text()
        tree = ast.parse(code)

        total_functions = 0
        typed_functions = 0
        total_params = 0
        typed_params = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_functions += 1

                # 检查返回类型注解
                if node.returns is not None:
                    typed_functions += 1

                # 检查参数类型注解
                for arg in node.args.args:
                    total_params += 1
                    if arg.annotation is not None:
                        typed_params += 1

        coverage = (typed_params / total_params * 100) if total_params > 0 else 0.0

        return {
            "total_functions": total_functions,
            "typed_functions": typed_functions,
            "total_params": total_params,
            "typed_params": typed_params,
            "coverage": round(coverage, 2),
        }

    except Exception as e:
        return {"error": str(e), "coverage": 0.0}


def main() -> None:
    """主函数"""
    print("=" * 70)
    print("练习 2: mypy 类型检查 - 参考答案（Python 3.13+ 现代化版本）")
    print("=" * 70)
    print()

    # 创建测试目录
    test_dir = Path("./mypy_test")
    test_file = test_dir / "sample.py"

    # 步骤 1: 保存无类型注解的代码
    print("步骤 1: 保存无类型注解的代码")
    save_code_without_types(test_file)
    print()

    # 步骤 2: 显示原始代码
    print("步骤 2: 原始代码（无类型注解）")
    print("-" * 70)
    print(SAMPLE_CODE_NO_TYPES)
    print("-" * 70)
    print()

    # 步骤 3: 运行 mypy 检查（预期失败）
    print("步骤 3: 运行 mypy 检查（无类型注解）")
    passed, errors = run_mypy_check(test_file)
    if not passed:
        print("⚠️  发现类型问题:")
        for error in errors[:5]:  # 只显示前 5 个错误
            print(f"  {error}")
        if len(errors) > 5:
            print(f"  ... 还有 {len(errors) - 5} 个错误")
    print()

    # 步骤 4: 添加基础类型注解
    print("步骤 4: 添加基础类型注解（Python 3.10+ 现代语法）")
    code_with_basic_types = add_basic_types(SAMPLE_CODE_NO_TYPES)
    test_file.write_text(code_with_basic_types)
    print("✅ 已添加基础类型注解")
    print("-" * 70)
    print(code_with_basic_types[:500] + "...")
    print("-" * 70)
    print()

    # 步骤 5: 再次运行 mypy 检查
    print("步骤 5: 运行 mypy 检查（基础类型注解后）")
    passed, errors = run_mypy_check(test_file)
    if not passed:
        print("⚠️  仍有类型问题:")
        for error in errors[:3]:
            print(f"  {error}")
    else:
        print("✅ 部分检查通过")
    print()

    # 步骤 6: 添加复杂类型注解
    print("步骤 6: 添加复杂类型注解（Python 3.10+ 现代语法）")
    code_with_all_types = add_complex_types(code_with_basic_types)
    test_file.write_text(code_with_all_types)
    print("✅ 已添加所有类型注解")
    print("-" * 70)
    print(code_with_all_types)
    print("-" * 70)
    print()

    # 步骤 7: 最终 mypy 检查
    print("步骤 7: 最终 mypy 检查")
    passed, errors = run_mypy_check(test_file)
    if passed:
        print("✅ 所有类型检查通过！")
    else:
        print("⚠️  仍有问题:")
        for error in errors:
            print(f"  {error}")
    print()

    # 展示类型注解演进
    show_type_evolution()

    # 总结
    print("\n\n" + "=" * 70)
    print("🎉 恭喜！练习 2 完成！")
    print("=" * 70)
    print()
    print("你已经学会了:")
    print("  ✅ 使用现代 Python 3.10+ 类型语法")
    print("  ✅ 使用 list[T], dict[K,V] 内置泛型")
    print("  ✅ 使用 X | Y 联合类型语法")
    print("  ✅ 使用 X | None 替代 Optional[X]")
    print("  ✅ 使用 mypy 进行静态类型检查")
    print()
    print("提示:")
    print("  - 在 VS Code 中安装 Pylance 插件，实时类型检查")
    print("  - 使用 mypy --strict 启用最严格的类型检查")
    print("  - Python 3.13 支持 PEP 695 泛型语法（def func[T](...): ...）")
    print()
    print("下一步:")
    print("  - 继续练习 3: pytest 测试框架")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
