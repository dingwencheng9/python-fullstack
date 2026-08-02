"""练习 2: mypy 类型检查（中级 - Python 3.13+ 现代化版本）

from __future__ import annotations

任务：
为现有代码添加类型注解，并使用 mypy 进行类型检查。

学习目标：
- 理解类型注解的重要性
- ✅ 掌握 Python 3.10+ 现代类型注解语法
- ✅ 使用内置泛型（list, dict）而非 typing.List/Dict
- ✅ 使用联合类型（X | Y）而非 Union
- ✅ 使用可选类型（X | None）而非 Optional
- 学会使用 mypy 检查类型
- 修复常见的类型错误

预计时间: 1.5 小时
难度: ⭐⭐☆☆☆
"""

from pathlib import Path

# 这是一段没有类型注解的代码，需要添加类型注解
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
    """保存无类型注解的代码

    TODO: 实现以下功能
    1. 创建文件所在目录
    2. 将 SAMPLE_CODE_NO_TYPES 写入文件
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 save_code_without_types 函数")


def add_basic_types(code: str) -> str:
    """添加基础类型注解（Python 3.10+ 现代语法）

    TODO: 实现以下功能
    1. 为 greet 函数添加类型注解
       - 参数 name: str
       - 返回值: str
    2. 为 calculate_total 函数添加类型注解
       - ✅ 参数 prices: list[float]（不是 List[float]）
       - 返回值: float
    3. 返回修改后的代码

    ⚠️ 注意：使用 Python 3.9+ 内置泛型
    - ✅ list[T] 而不是 List[T]
    - ✅ dict[K, V] 而不是 Dict[K, V]
    - ❌ 不要导入 typing.List/Dict

    提示: 可以使用字符串替换，或者解析 AST
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 add_basic_types 函数")


def add_complex_types(code: str) -> str:
    """添加复杂类型注解（Python 3.10+ 现代语法）

    TODO: 实现以下功能
    1. 为 find_user 函数添加类型注解
       - ✅ 参数 users: list[dict[str, str | int]]（现代语法）
       - 参数 user_id: int
       - ✅ 返回值: dict[str, str | int] | None（不是 Optional）
    2. 为 UserManager 类的方法添加类型注解
       - __init__(database_url: str) -> None
       - ✅ add_user(...) -> dict[str, str | int]
       - ✅ get_user(...) -> dict[str, str | int] | None
    3. 为类属性添加类型注解
       - ✅ self.users: list[dict[str, str | int]] = []
    4. 返回修改后的代码

    ⚠️ 注意：使用 Python 3.10+ 联合类型语法
    - ✅ X | Y 而不是 Union[X, Y]
    - ✅ X | None 而不是 Optional[X]
    - ❌ 不要导入 typing.Union/Optional

    提示: 使用字符串替换处理复杂类型
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 add_complex_types 函数")


def run_mypy_check(file_path: Path) -> tuple[bool, list[str]]:
    """运行 mypy 类型检查

    TODO: 实现以下功能
    1. 使用 subprocess.run() 运行 mypy 命令
    2. 检查返回码（0 表示通过）
    3. 解析输出中的错误信息
    4. 返回 (是否通过, 错误列表)

    返回格式:
    - (True, []) 表示通过
    - (False, ["error1", "error2"]) 表示失败
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_mypy_check 函数")


def fix_mypy_errors(code: str, errors: list[str]) -> str:
    """根据 mypy 错误自动修复代码

    TODO: 实现以下功能
    1. 解析 mypy 错误信息
    2. 自动修复常见错误
       - "Missing return statement" -> 添加 return None
       - "Incompatible return value type" -> 修正返回类型
    3. 返回修复后的代码

    提示: 这是一个进阶功能，可以简化实现
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 fix_mypy_errors 函数")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 2: mypy 类型检查（Python 3.13+ 现代化版本）")
    print("=" * 60)
    print()

    # 创建测试目录
    test_dir = Path("./mypy_test")
    test_file = test_dir / "sample.py"

    # 步骤 1: 保存无类型注解的代码
    print("步骤 1: 保存无类型注解的代码")
    try:
        save_code_without_types(test_file)
        print("✅ 代码已保存")
    except NotImplementedError:
        print("❌ 请实现 save_code_without_types 函数")
        return
    print()

    # 步骤 2: 显示原始代码
    print("步骤 2: 原始代码（无类型注解）")
    print("-" * 60)
    print(SAMPLE_CODE_NO_TYPES[:300] + "...")
    print("-" * 60)
    print()

    # 步骤 3: 添加基础类型注解
    print("步骤 3: 添加基础类型注解（Python 3.10+ 现代语法）")
    try:
        code_with_basic_types = add_basic_types(SAMPLE_CODE_NO_TYPES)
        test_file.write_text(code_with_basic_types)
        print("✅ 已添加基础类型注解")
        print("   提示: 使用 list[float] 而不是 List[float]")
    except NotImplementedError:
        print("❌ 请实现 add_basic_types 函数")
        return
    print()

    # 步骤 4: 运行 mypy 检查
    print("步骤 4: 运行 mypy 检查")
    try:
        passed, errors = run_mypy_check(test_file)
        if passed:
            print("✅ 基础类型检查通过")
        else:
            print("⚠️  发现问题:")
            for error in errors[:3]:
                print(f"  {error}")
    except NotImplementedError:
        print("❌ 请实现 run_mypy_check 函数")
        return
    print()

    # 步骤 5: 添加复杂类型注解
    print("步骤 5: 添加复杂类型注解（Python 3.10+ 现代语法）")
    try:
        code_with_all_types = add_complex_types(code_with_basic_types)
        test_file.write_text(code_with_all_types)
        print("✅ 已添加所有类型注解")
        print("   提示: 使用 X | Y 而不是 Union[X, Y]")
        print("   提示: 使用 X | None 而不是 Optional[X]")
    except NotImplementedError:
        print("❌ 请实现 add_complex_types 函数")
        return
    print()

    # 步骤 6: 最终 mypy 检查
    print("步骤 6: 最终 mypy 检查")
    try:
        passed, errors = run_mypy_check(test_file)
        if passed:
            print("✅ 所有类型检查通过！")
        else:
            print("⚠️  仍有问题:")
            for error in errors:
                print(f"  {error}")
    except NotImplementedError:
        print("❌ 请实现 run_mypy_check 函数")
        return
    print()

    # 总结
    print("=" * 60)
    print("🎉 恭喜！练习 2 完成！")
    print("=" * 60)
    print()
    print("你已经学会了:")
    print("  ✅ 使用 Python 3.10+ 现代类型注解语法")
    print("  ✅ 使用 list[T], dict[K,V] 内置泛型")
    print("  ✅ 使用 X | Y 联合类型")
    print("  ✅ 使用 X | None 替代 Optional[X]")
    print("  ✅ 使用 mypy 进行静态类型检查")
    print()
    print("下一步:")
    print("  - 查看参考答案: solutions/02-mypy.py")
    print("  - 在自己的项目中使用类型注解")
    print("  - 继续练习 3: pytest 测试框架")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
