"""练习 1: Ruff 代码格式化和检查（基础）

from __future__ import annotations

任务：
使用 Ruff 修复和格式化有问题的代码，理解 Ruff 的工作原理。

学习目标：
- 理解代码格式化的重要性
- 掌握 Ruff 的基本使用
- 学会配置 Ruff
- 修复常见的代码问题

预计时间: 1 小时
难度: ⭐☆☆☆☆
"""

from pathlib import Path

# 这是一段格式混乱的代码，需要用 Ruff 修复（故意包含旧版语法和格式问题）
SAMPLE_CODE = '''import sys
import os
from typing import Dict,List,Optional


def get_users(  ):
    """获取用户列表"""
    users=[1,2,3,]
    return users

def process_data( data:List[int] )->Dict[str,int]:
    """处理数据"""
    result={}
    for item in data:
        result[str(item)]=item*2
    return result


class UserManager:
    def __init__(self,name:str,age:int):
        self.name=name
        self.age=age

    def get_info(self)->str:
        return f"{self.name}:{self.age}"
'''


def save_sample_code(file_path: Path) -> None:
    """保存示例代码到文件

    TODO: 实现以下功能
    1. 创建文件所在目录（如果不存在）
    2. 将 SAMPLE_CODE 写入文件
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 save_sample_code 函数")


def run_ruff_format(file_path: Path) -> bool:
    """运行 Ruff 格式化

    TODO: 实现以下功能
    1. 运行 ruff format 命令
    2. 返回是否成功

    提示: 使用 subprocess.run()
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_ruff_format 函数")


def run_ruff_check(file_path: Path) -> tuple[bool, str]:
    """运行 Ruff 检查

    TODO: 实现以下功能
    1. 运行 ruff check 命令
    2. 返回 (是否通过, 检查结果)

    返回格式: (True, "All checks passed") 或 (False, "错误信息")
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_ruff_check 函数")


def run_ruff_fix(file_path: Path) -> bool:
    """运行 Ruff 自动修复

    TODO: 实现以下功能
    1. 运行 ruff check --fix 命令
    2. 自动修复可以修复的问题
    3. 返回是否成功

    提示: 使用 --fix 参数
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 run_ruff_fix 函数")


def compare_code(original: str, formatted: str) -> dict[str, int]:
    """比较原始代码和格式化后的代码

    TODO: 实现以下功能
    1. 比较两段代码的差异
    2. 统计改变的行数、空格数等
    3. 返回统计结果

    返回格式: {
        "lines_changed": 改变的行数,
        "imports_sorted": 导入是否排序,
        "spacing_fixed": 空格是否修复
    }
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 compare_code 函数")


def create_ruff_config(project_path: Path) -> None:
    """创建 Ruff 配置文件

    TODO: 实现以下功能
    1. 在项目目录创建 pyproject.toml
    2. 添加 Ruff 配置
    3. 配置项：
       - target-version = "py313"
       - line-length = 100
       - select = ["E", "F", "I", "N", "W"]

    提示: 使用 tomli_w 库
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 create_ruff_config 函数")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 1: Ruff 代码格式化和检查")
    print("=" * 60)
    print()

    # 创建测试目录
    test_dir = Path("./ruff_test")
    test_file = test_dir / "sample.py"

    # 步骤 1: 保存示例代码
    print("步骤 1: 保存示例代码")
    try:
        save_sample_code(test_file)
        print("✅ 示例代码已保存")
        print(f"   文件位置: {test_file}")
    except NotImplementedError:
        print("❌ 请实现 save_sample_code 函数")
        return
    print()

    # 步骤 2: 显示原始代码
    print("步骤 2: 原始代码（格式混乱）")
    print("-" * 60)
    print(SAMPLE_CODE)
    print("-" * 60)
    print()

    # 步骤 3: 运行 Ruff 格式化
    print("步骤 3: 运行 Ruff 格式化")
    try:
        if run_ruff_format(test_file):
            print("✅ 代码格式化完成")
        else:
            print("❌ 格式化失败")
            return
    except NotImplementedError:
        print("❌ 请实现 run_ruff_format 函数")
        return
    print()

    # 步骤 4: 显示格式化后的代码
    print("步骤 4: 格式化后的代码")
    print("-" * 60)
    formatted_code = test_file.read_text()
    print(formatted_code)
    print("-" * 60)
    print()

    # 步骤 5: 运行 Ruff 检查
    print("步骤 5: 运行 Ruff 检查")
    try:
        passed, result = run_ruff_check(test_file)
        if passed:
            print("✅ 代码检查通过")
        else:
            print("⚠️  发现问题:")
            print(result)
    except NotImplementedError:
        print("❌ 请实现 run_ruff_check 函数")
        return
    print()

    # 步骤 6: 自动修复问题
    print("步骤 6: 自动修复问题")
    try:
        if run_ruff_fix(test_file):
            print("✅ 问题已自动修复")
        else:
            print("⚠️  部分问题无法自动修复")
    except NotImplementedError:
        print("❌ 请实现 run_ruff_fix 函数")
        return
    print()

    # 步骤 7: 比较代码差异
    print("步骤 7: 比较代码差异")
    try:
        final_code = test_file.read_text()
        diff = compare_code(SAMPLE_CODE, final_code)
        print(f"  改变的行数: {diff.get('lines_changed', 0)}")
        print(f"  导入已排序: {'✅' if diff.get('imports_sorted') else '❌'}")
        print(f"  空格已修复: {'✅' if diff.get('spacing_fixed') else '❌'}")
    except NotImplementedError:
        print("❌ 请实现 compare_code 函数")
        return
    print()

    # 步骤 8: 创建配置文件
    print("步骤 8: 创建 Ruff 配置")
    try:
        create_ruff_config(test_dir)
        config_file = test_dir / "pyproject.toml"
        if config_file.exists():
            print("✅ Ruff 配置已创建")
            print(f"   配置文件: {config_file}")
        else:
            print("❌ 配置文件创建失败")
    except NotImplementedError:
        print("❌ 请实现 create_ruff_config 函数")
        return
    print()

    # 总结
    print("=" * 60)
    print("🎉 恭喜！练习 1 完成！")
    print("=" * 60)
    print()
    print("你已经学会了:")
    print("  ✅ 使用 Ruff 格式化代码")
    print("  ✅ 使用 Ruff 检查代码")
    print("  ✅ 使用 Ruff 自动修复问题")
    print("  ✅ 配置 Ruff")
    print()
    print("下一步:")
    print("  - 查看参考答案: solutions/01-ruff.py")
    print("  - 在自己的项目中使用 Ruff")
    print("  - 继续练习 2: mypy 类型检查")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
