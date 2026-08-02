"""练习 1: Ruff 代码格式化和检查 - 参考答案

from __future__ import annotations

本文件提供练习 1 的完整实现，展示如何使用 Ruff 工具。

【解题思路】
1. save_sample_code():
   - 使用 Path.parent.mkdir(parents=True, exist_ok=True) 确保父目录存在
   - 使用 Path.write_text() 将字符串写入文件
2. run_ruff_format():
   - subprocess.run(["ruff", "format", str(file_path)]) 执行格式化命令
   - check=False 允许非零返回码（我们手动检查 returncode）
   - timeout=30 防止命令挂死
   - 捕获 FileNotFoundError（ruff 未安装）和 TimeoutExpired（超时）
3. run_ruff_check():
   - subprocess.run(["ruff", "check", str(file_path)]) 执行检查命令
   - 返回码 0 表示无问题，非 0 表示有 linting 错误
   - 返回 tuple[bool, str]：(是否通过, 错误信息)
4. show_diff():
   - 读取文件前后内容并对比
   - 使用简单的行对比展示差异
5. main():
   - 流程：保存代码 → 格式化 → 显示差异 → 检查代码质量

【关键知识点】
- subprocess.run() 的 capture_output, text, check, timeout 参数
- Path.write_text() 和 Path.read_text() 文件读写
- ruff format 自动格式化（符合 Black 风格）
- ruff check 执行 linting 检查（Flake8, isort, pyupgrade 等）
- 返回码含义：0=成功，非0=失败/有问题
"""

import subprocess
from pathlib import Path

# 待格式化的代码示例（故意包含旧版语法和格式问题）
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
    """保存示例代码到文件"""
    # 创建父目录（如果不存在）
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入示例代码
    file_path.write_text(SAMPLE_CODE)
    print(f"✅ 代码已保存到: {file_path}")


def run_ruff_format(file_path: Path) -> bool:
    """运行 Ruff 格式化"""
    try:
        # 运行 ruff format 命令
        result = subprocess.run(
            ["ruff", "format", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # 检查是否成功
        if result.returncode == 0:
            print("✅ Ruff 格式化成功")
            return True
        print(f"❌ Ruff 格式化失败: {result.stderr}")
        return False

    except FileNotFoundError:
        print("❌ 错误: Ruff 未安装，请运行: uv add --dev ruff")
        return False
    except subprocess.TimeoutExpired:
        print("❌ 错误: 命令超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def run_ruff_check(file_path: Path) -> tuple[bool, str]:
    """运行 Ruff 检查"""
    try:
        # 运行 ruff check 命令
        result = subprocess.run(
            ["ruff", "check", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # 返回码为 0 表示没有问题
        if result.returncode == 0:
            return (True, "所有检查通过！")
        # 返回错误信息
        error_msg = result.stdout if result.stdout else result.stderr
        return (False, error_msg)

    except FileNotFoundError:
        return (False, "Ruff 未安装")
    except subprocess.TimeoutExpired:
        return (False, "命令超时")
    except Exception as e:
        return (False, str(e))


def run_ruff_fix(file_path: Path) -> bool:
    """运行 Ruff 自动修复"""
    try:
        # 运行 ruff check --fix 命令
        result = subprocess.run(
            ["ruff", "check", "--fix", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # 即使有无法自动修复的问题，也可能返回非 0
        # 但如果修复了一些问题，仍然算成功
        if "Fixed" in result.stdout or result.returncode == 0:
            print("✅ Ruff 自动修复完成")
            if result.stdout:
                print(f"   修复信息: {result.stdout.strip()}")
            return True
        print("⚠️  部分问题无法自动修复")
        if result.stdout:
            print(f"   {result.stdout}")
        return False

    except FileNotFoundError:
        print("❌ 错误: Ruff 未安装")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def compare_code(original: str, formatted: str) -> dict[str, int | bool]:
    """比较原始代码和格式化后的代码"""
    # 按行分割
    original_lines = original.splitlines()
    formatted_lines = formatted.splitlines()

    # 计算改变的行数
    lines_changed = 0
    for orig, form in zip(original_lines, formatted_lines, strict=False):
        if orig != form:
            lines_changed += 1

    # 检查导入是否排序
    # 原始代码中导入顺序: sys, os, typing
    # 格式化后应该按字母顺序: os, sys, typing
    original_imports = [line for line in original_lines if line.startswith(("import", "from"))]
    formatted_imports = [line for line in formatted_lines if line.startswith(("import", "from"))]
    imports_sorted = original_imports != formatted_imports

    # 检查空格是否修复
    # 原始代码有很多不规范的空格
    spacing_fixed = "  )" not in formatted and ",]" not in formatted

    return {
        "lines_changed": lines_changed,
        "imports_sorted": imports_sorted,
        "spacing_fixed": spacing_fixed,
    }


def create_ruff_config(project_path: Path) -> None:
    """创建 Ruff 配置文件"""
    try:
        import tomli_w
    except ImportError:
        print("❌ 错误: tomli_w 未安装，请运行: uv add --dev tomli-w")
        return

    # Ruff 配置
    config = {
        "tool": {
            "ruff": {
                "target-version": "py313",
                "line-length": 100,
                "select": [
                    "E",  # pycodestyle errors
                    "F",  # pyflakes
                    "I",  # isort
                    "N",  # pep8-naming
                    "W",  # pycodestyle warnings
                ],
                "ignore": [],
                "fixable": ["ALL"],
                "unfixable": [],
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
            existing_config["tool"]["ruff"] = config["tool"]["ruff"]
            config = existing_config
        except ImportError:
            print("⚠️  tomli 未安装，将覆盖现有配置")

    # 写入配置
    with config_file.open("wb") as f:
        tomli_w.dump(config, f)

    print(f"✅ Ruff 配置已写入: {config_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 1: Ruff 代码格式化和检查 - 参考答案")
    print("=" * 60)
    print()

    # 创建测试目录
    test_dir = Path("./ruff_test")
    test_file = test_dir / "sample.py"

    # 步骤 1: 保存示例代码
    print("步骤 1: 保存示例代码")
    save_sample_code(test_file)
    print()

    # 步骤 2: 显示原始代码
    print("步骤 2: 原始代码（格式混乱）")
    print("-" * 60)
    print(SAMPLE_CODE)
    print("-" * 60)
    print()

    # 步骤 3: 运行 Ruff 格式化
    print("步骤 3: 运行 Ruff 格式化")
    if run_ruff_format(test_file):
        print("✅ 代码格式化完成")
    else:
        print("❌ 格式化失败，但继续执行")
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
    passed, result = run_ruff_check(test_file)
    if passed:
        print("✅ 代码检查通过")
    else:
        print("⚠️  发现问题:")
        print(result)
    print()

    # 步骤 6: 自动修复问题
    print("步骤 6: 自动修复问题")
    if run_ruff_fix(test_file):
        print("✅ 问题已自动修复")
    else:
        print("⚠️  部分问题无法自动修复")
    print()

    # 步骤 7: 比较代码差异
    print("步骤 7: 比较代码差异")
    final_code = test_file.read_text()
    diff = compare_code(SAMPLE_CODE, final_code)
    print(f"  改变的行数: {diff['lines_changed']}")
    print(f"  导入已排序: {'✅' if diff['imports_sorted'] else '❌'}")
    print(f"  空格已修复: {'✅' if diff['spacing_fixed'] else '❌'}")
    print()

    # 步骤 8: 创建配置文件
    print("步骤 8: 创建 Ruff 配置")
    create_ruff_config(test_dir)
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
    print("提示:")
    print("  - 在实际项目中，建议将 Ruff 集成到 pre-commit hook")
    print("  - 可以在 VS Code 中安装 Ruff 插件，实时检查代码")
    print("  - Ruff 比 Black + isort + flake8 快 10-100 倍")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  练习已取消")
