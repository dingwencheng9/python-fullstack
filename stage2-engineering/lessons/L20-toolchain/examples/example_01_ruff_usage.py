"""

from __future__ import annotations

L18 示例 1: Ruff 代码质量工具使用

展示 Ruff 的核心功能：格式化和 Linting。
"""

import subprocess
from pathlib import Path

# 需要检查的示例代码（故意包含旧版语法问题）
SAMPLE_CODE_WITH_ISSUES = '''
import sys
import os
from typing import Dict, List
import json


def calculate_sum(numbers:List[int])->int:
    """计算列表总和"""
    total=0
    for num in numbers:
        total+=num
    return total


def process_data(data:Dict[str,any]):
    """处理数据"""
    result=[]
    for key,value in data.items():
        if value>0:
            result.append({"key":key,"value":value})
    return result


class UserManager:
    def __init__(self,name:str,age:int):
        self.name=name
        self.age=age

    def get_info(self)->str:
        return f"{self.name} is {self.age} years old"


# 未使用的导入
import math
import random

# 主函数
if __name__=="__main__":
    numbers=[1,2,3,4,5]
    result=calculate_sum(numbers)
    print(f"Sum: {result}")

    data={"a":10,"b":-5,"c":20}
    processed=process_data(data)
    print(processed)
'''

# 修复后的代码（使用 Python 3.10+ 现代语法）
SAMPLE_CODE_FIXED = '''
"""示例模块：展示 Ruff 格式化后的代码"""

from typing import Any


def calculate_sum(numbers: list[int]) -> int:
    """计算列表总和"""
    total = 0
    for num in numbers:
        total += num
    return total


def process_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    """处理数据"""
    result = []
    for key, value in data.items():
        if value > 0:
            result.append({"key": key, "value": value})
    return result


class UserManager:
    """用户管理器"""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def get_info(self) -> str:
        """获取用户信息"""
        return f"{self.name} is {self.age} years old"


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(f"Sum: {result}")

    data = {"a": 10, "b": -5, "c": 20}
    processed = process_data(data)
    print(processed)
'''


def run_ruff_command(cmd: str, description: str) -> None:
    """运行 Ruff 命令并显示结果"""
    print(f"\n{'=' * 70}")
    print(f"📌 {description}")
    print(f"{'=' * 70}")
    print(f"$ {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)


def demonstrate_ruff_check() -> None:
    """演示 Ruff 检查功能"""

    print("🔍 Ruff Linting 演示")
    print("=" * 70)

    # 创建示例文件
    sample_file = Path("sample_with_issues.py")
    sample_file.write_text(SAMPLE_CODE_WITH_ISSUES)
    print(f"✅ 创建示例文件: {sample_file}")

    # 1. 检查代码
    run_ruff_command(f"ruff check {sample_file}", "检查代码问题")

    # 2. 显示详细信息
    run_ruff_command(f"ruff check {sample_file} --output-format=full", "显示详细的错误信息")

    # 3. 自动修复
    print(f"\n{'=' * 70}")
    print("🔧 尝试自动修复...")
    print(f"{'=' * 70}")

    run_ruff_command(f"ruff check {sample_file} --fix", "自动修复可修复的问题")

    # 4. 再次检查
    run_ruff_command(f"ruff check {sample_file}", "修复后再次检查")


def demonstrate_ruff_format() -> None:
    """演示 Ruff 格式化功能"""

    print("\n\n🎨 Ruff Format 演示")
    print("=" * 70)

    sample_file = Path("sample_with_issues.py")

    # 1. 显示格式化前的代码
    print("\n📄 格式化前的代码（部分）:")
    print("-" * 70)
    lines = sample_file.read_text().split("\n")[:15]
    for i, line in enumerate(lines, 1):
        print(f"{i:3d} | {line}")

    # 2. 格式化代码
    run_ruff_command(f"ruff format {sample_file}", "格式化代码")

    # 3. 显示格式化后的代码
    print("\n📄 格式化后的代码（部分）:")
    print("-" * 70)
    lines = sample_file.read_text().split("\n")[:15]
    for i, line in enumerate(lines, 1):
        print(f"{i:3d} | {line}")


def demonstrate_ruff_rules() -> None:
    """演示 Ruff 规则"""

    print("\n\n📋 Ruff 规则说明")
    print("=" * 70)

    rules = [
        ("E", "pycodestyle 错误", "E501: 行长度超限"),
        ("F", "Pyflakes", "F401: 未使用的导入"),
        ("I", "isort", "I001: 导入顺序错误"),
        ("N", "pep8-naming", "N806: 变量命名不规范"),
        ("W", "pycodestyle 警告", "W291: 行尾空白"),
        ("UP", "pyupgrade", "UP006: 使用旧式类型注解"),
    ]

    print("\n常用规则类别：")
    print("-" * 70)
    for code, name, example in rules:
        print(f"\n  {code:4s} - {name}")
        print(f"        示例: {example}")


def show_ruff_config() -> None:
    """显示 Ruff 配置"""

    print("\n\n⚙️  Ruff 配置示例")
    print("=" * 70)

    config = """
# pyproject.toml
[tool.ruff]
target-version = "py313"
line-length = 100

# 启用的规则
select = [
    "E",   # pycodestyle 错误
    "F",   # Pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle 警告
    "UP",  # pyupgrade
]

# 忽略的规则
ignore = [
    "E501",  # 行长度（由 formatter 处理）
]

# 按文件忽略
[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["S101"]  # 测试中允许 assert
"__init__.py" = ["F401"]    # __init__ 中允许未使用的导入
"""

    print(config)


def show_best_practices() -> None:
    """展示最佳实践"""

    print("\n\n💡 Ruff 使用最佳实践")
    print("=" * 70)

    practices = [
        "1. 格式化 + 检查配合使用",
        "   ruff format . && ruff check .",
        "",
        "2. 在 CI/CD 中运行",
        "   确保提交前代码质量",
        "",
        "3. 使用 --fix 自动修复",
        "   但要检查修复结果",
        "",
        "4. 配置 pre-commit hook",
        "   自动在提交前运行",
        "",
        "5. 逐步启用规则",
        "   从核心规则开始，逐步增加",
    ]

    for line in practices:
        print(f"  {line}")


def main() -> None:
    """主函数"""

    print("🚀 Ruff 代码质量工具完整演示")
    print("=" * 70)

    # 1. 演示检查功能
    demonstrate_ruff_check()

    # 2. 演示格式化功能
    demonstrate_ruff_format()

    # 3. 说明规则
    demonstrate_ruff_rules()

    # 4. 展示配置
    show_ruff_config()

    # 5. 最佳实践
    show_best_practices()

    print("\n\n✨ 演示完成！")
    print("\n🔑 关键要点：")
    print("  • Ruff 集成了多个工具（Black, isort, Flake8 等）")
    print("  • 速度极快（比传统工具快 10-100 倍）")
    print("  • 一个工具完成格式化和检查")
    print("  • 配置简单，开箱即用")


if __name__ == "__main__":
    main()
