"""练习 3: 验证环境配置（高级）

from __future__ import annotations

任务：
创建一个完整的验证脚本，检查环境配置是否符合 v4.1 标准。

学习目标：
- 验证 Python 版本
- 验证工具链安装
- 验证配置正确性
- 生成验证报告

预计时间: 1.5 小时
难度: ⭐⭐⭐☆☆
"""

import sys
from pathlib import Path

# Python 3.13 现代类型别名 - 使用 type 关键字替代 TypedDict
# 线程安全（Python 3.14）：类型别名本身是编译时构造，运行时不可变，线程安全
type VersionInfo = dict[str, bool | str]
type ValidationReport = dict[str, VersionInfo | bool]


def get_python_version() -> VersionInfo:
    """获取 Python 版本信息

    TODO: 实现以下功能
    1. 获取当前 Python 版本
    2. 检查是否 >= 3.13
    3. 返回版本信息

    返回格式: {
        "installed": True,
        "version": "3.13.0",
        "meets_requirement": True
    }
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 get_python_version 函数")


def get_tool_version(tool: str, min_version: str | None = None) -> VersionInfo:
    """获取工具版本信息

    TODO: 实现以下功能
    1. 运行 {tool} --version 获取版本
    2. 解析版本号
    3. 如果提供 min_version，检查是否满足最低版本要求
    4. 返回版本信息

    参数:
        tool: 工具名称 (uv, ruff, mypy, pytest)
        min_version: 最低版本要求 (可选)

    返回格式: {
        "installed": True,
        "version": "0.8.0",
        "meets_requirement": True
    }
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 get_tool_version 函数")


def validate_pyproject_config(project_path: Path) -> bool:
    """验证 pyproject.toml 配置

    TODO: 实现以下功能
    1. 读取 pyproject.toml
    2. 检查 requires-python 是否配置
    3. 检查 tool.ruff.target-version 是否为 "py313"
    4. 检查 tool.mypy.python_version 是否为 "3.13"
    5. 返回是否所有配置都正确

    提示: 使用 tomllib (Python 3.11+ 内置) 解析 TOML 文件
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 validate_pyproject_config 函数")


def generate_validation_report(project_path: Path) -> ValidationReport:
    """生成完整的验证报告

    TODO: 实现以下功能
    1. 调用 get_python_version() 获取 Python 版本
    2. 调用 get_tool_version() 获取各工具版本
    3. 调用 validate_pyproject_config() 验证配置
    4. 汇总所有结果
    5. 返回完整报告

    返回格式: {
        "python": {...},
        "uv": {...},
        "ruff": {...},
        "mypy": {...},
        "pytest": {...},
        "config_valid": True,
        "overall_pass": True
    }
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 generate_validation_report 函数")


def print_validation_report(report: ValidationReport) -> None:
    """打印验证报告

    TODO: 实现以下功能
    1. 以美观的格式打印报告
    2. 使用 ✅ 表示通过，❌ 表示失败
    3. 显示每个工具的版本信息
    4. 显示总体结果

    示例输出:
    ==========================================
    环境验证报告
    ==========================================

    Python 版本:
      ✅ 已安装: Python 3.13.0
      ✅ 满足要求 (>= 3.13)

    工具链:
      ✅ uv: 0.5.0
      ✅ ruff: 0.8.0
      ✅ mypy: 1.13.0
      ✅ pytest: 8.0.0

    配置验证:
      ✅ pyproject.toml 配置正确

    ==========================================
    总体结果: ✅ 通过
    ==========================================
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 print_validation_report 函数")


def fix_common_issues(project_path: Path, report: ValidationReport) -> None:
    """修复常见问题

    TODO: 实现以下功能
    1. 根据验证报告识别问题
    2. 提供修复建议
    3. 可选：自动修复部分问题

    提示：
    - 如果工具未安装，提示安装命令
    - 如果配置错误，提示修正方法
    - 如果版本过低，提示升级命令
    """
    # TODO: 你的代码
    raise NotImplementedError("请实现 fix_common_issues 函数")


def main():
    """主函数"""
    print("=" * 60)
    print("练习 3: 验证环境配置")
    print("=" * 60)
    print()

    # 获取项目路径
    project_path = Path.cwd()
    print(f"项目路径: {project_path}")
    print()

    # 步骤 1: 检查 Python 版本
    print("步骤 1: 检查 Python 版本")
    try:
        python_info = get_python_version()
        status = "✅" if python_info["meets_requirement"] else "❌"
        print(f"  {status} Python {python_info['version']}")
    except NotImplementedError:
        print("  ❌ 请实现 get_python_version 函数")
        return
    print()

    # 步骤 2: 检查工具链
    print("步骤 2: 检查工具链")
    tools = ["uv", "ruff", "mypy", "pytest"]
    for tool in tools:
        try:
            info = get_tool_version(tool)
            status = "✅" if info["installed"] else "❌"
            version = info["version"] if info["installed"] else "未安装"
            print(f"  {status} {tool}: {version}")
        except NotImplementedError:
            print("  ❌ 请实现 get_tool_version 函数")
            return
    print()

    # 步骤 3: 验证配置
    print("步骤 3: 验证配置")
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        try:
            config_valid = validate_pyproject_config(project_path)
            status = "✅" if config_valid else "❌"
            print(f"  {status} pyproject.toml 配置")
        except NotImplementedError:
            print("  ❌ 请实现 validate_pyproject_config 函数")
            return
    else:
        print("  ⚠️  pyproject.toml 不存在")
    print()

    # 步骤 4: 生成完整报告
    print("步骤 4: 生成完整报告")
    try:
        report = generate_validation_report(project_path)
        print()
        print_validation_report(report)
        print()

        # 步骤 5: 修复建议
        if not report["overall_pass"]:
            print("步骤 5: 修复建议")
            print()
            fix_common_issues(project_path, report)
        else:
            print("🎉 恭喜！环境配置完全符合 v4.1 标准！")
            print()
            print("你已经掌握了:")
            print("  ✅ Python 版本管理")
            print("  ✅ 工具链配置")
            print("  ✅ pyproject.toml 配置")
            print("  ✅ 环境验证方法")
            print()
            print("下一步: 进入 L19 学习异步编程核心")

    except NotImplementedError:
        print("  ❌ 请实现 generate_validation_report 和 print_validation_report 函数")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  验证已取消")
        sys.exit(1)
