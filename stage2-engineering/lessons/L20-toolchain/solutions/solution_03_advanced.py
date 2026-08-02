"""练习 3: 验证环境配置（高级）- 参考答案

from __future__ import annotations

本文件提供练习 3 的完整实现，供学习参考。

【解题思路】
1. 使用现代 Python 3.13 类型注解（无需 typing 模块）：
   - VersionInfo: 使用 dict[str, bool | str] 类型注解
   - ValidationReport: 使用嵌套字典类型注解
2. get_python_version():
   - 使用 sys.version_info 获取当前 Python 版本
   - 检查是否 >= (3, 12)
3. get_tool_version():
   - 执行 `tool --version` 获取输出
   - 使用正则表达式提取版本号（模式: 数字.数字.数字）
   - 版本比较：将版本字符串分割为整数列表，使用 >= 比较
   - 捕获 FileNotFoundError（工具未安装）和 CalledProcessError（命令失败）
4. validate_pyproject_config():
   - 使用 tomllib (Python 3.11+) 读取 pyproject.toml
   - 检查 requires-python、ruff.target-version、mypy.python_version
   - 使用 .get() 链式访问嵌套字典，避免 KeyError
5. generate_validation_report():
   - 调用上述函数收集所有信息
   - overall_pass 逻辑：所有工具都已安装且满足版本要求，且配置有效
6. print_report():
   - 使用 rich 库创建美化的表格输出
   - 根据验证结果显示 ✅ 或 ❌

【关键知识点】
- Python 3.13+ 现代类型注解：dict[str, bool | str] 而非 TypedDict
- 正则表达式 re.search() 提取版本号
- 版本号比较：字符串 → 整数列表 → 比较
- subprocess 异常处理：FileNotFoundError vs CalledProcessError
- 链式 dict.get() 安全访问嵌套结构
- rich 库创建表格和美化输出
- tomllib: Python 3.11+ 内置 TOML 解析器
"""

import re
import subprocess
import sys
import tomllib
from pathlib import Path

# 类型别名 - Python 3.13 推荐写法
type VersionInfo = dict[str, bool | str]
type ValidationReport = dict[str, VersionInfo | bool]


def get_python_version() -> VersionInfo:
    """获取 Python 版本信息

    线程安全（Python 3.14）：
    - ✅ 纯函数，无副作用，线程安全
    """
    version_str = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    meets_requirement = sys.version_info >= (3, 13)

    return {
        "installed": True,
        "version": version_str,
        "meets_requirement": meets_requirement,
    }


def get_tool_version(tool: str, min_version: str | None = None) -> VersionInfo:
    """获取工具版本信息"""
    try:
        result = subprocess.run([tool, "--version"], capture_output=True, text=True, check=True)

        # 解析版本号（提取第一个 x.y.z 格式的版本号）
        version_pattern = r"(\d+\.\d+\.\d+)"
        match = re.search(version_pattern, result.stdout)

        if match:
            version = match.group(1)
            meets_requirement = True

            # 如果提供了最低版本要求，进行比较
            if min_version:
                tool_version_parts = [int(x) for x in version.split(".")]
                min_version_parts = [int(x) for x in min_version.split(".")]
                meets_requirement = tool_version_parts >= min_version_parts

            return {
                "installed": True,
                "version": version,
                "meets_requirement": meets_requirement,
            }
        return {"installed": True, "version": "unknown", "meets_requirement": False}

    except (subprocess.CalledProcessError, FileNotFoundError):
        return {
            "installed": False,
            "version": "not installed",
            "meets_requirement": False,
        }


def validate_pyproject_config(project_path: Path) -> bool:
    """验证 pyproject.toml 配置"""
    pyproject_file = project_path / "pyproject.toml"

    if not pyproject_file.exists():
        return False

    try:
        with open(pyproject_file, "rb") as f:
            config = tomllib.load(f)

        # 检查 requires-python
        requires_python = config.get("project", {}).get("requires-python", "")
        has_requires = ">=3.13" in requires_python

        # 检查 ruff
        ruff_target = config.get("tool", {}).get("ruff", {}).get("target-version")
        has_ruff = ruff_target == "py313"

        # 检查 mypy
        mypy_version = config.get("tool", {}).get("mypy", {}).get("python_version")
        has_mypy = mypy_version == "3.13"

        return has_requires and has_ruff and has_mypy

    except Exception:
        return False


def generate_validation_report(project_path: Path) -> ValidationReport:
    """生成完整的验证报告"""
    python_info = get_python_version()
    uv_info = get_tool_version("uv")
    ruff_info = get_tool_version("ruff", "0.8.0")
    mypy_info = get_tool_version("mypy", "1.13.0")
    pytest_info = get_tool_version("pytest", "8.0.0")
    config_valid = validate_pyproject_config(project_path)

    overall_pass = (
        python_info["meets_requirement"]
        and uv_info["installed"]
        and ruff_info["meets_requirement"]
        and mypy_info["meets_requirement"]
        and pytest_info["meets_requirement"]
        and config_valid
    )

    return {
        "python": python_info,
        "uv": uv_info,
        "ruff": ruff_info,
        "mypy": mypy_info,
        "pytest": pytest_info,
        "config_valid": config_valid,
        "overall_pass": overall_pass,
    }


def print_validation_report(report: ValidationReport) -> None:
    """打印验证报告"""
    print("=" * 60)
    print("环境验证报告")
    print("=" * 60)
    print()

    # Python 版本
    print("Python 版本:")
    python = report["python"]
    status = "✅" if python["meets_requirement"] else "❌"
    print(f"  {status} 已安装: Python {python['version']}")
    if python["meets_requirement"]:
        print("  ✅ 满足要求 (>= 3.13)")
    else:
        print("  ❌ 不满足要求 (需要 >= 3.13)")
    print()

    # 工具链
    print("工具链:")
    for tool_name in ["uv", "ruff", "mypy", "pytest"]:
        tool_info = report[tool_name]  # type: ignore
        if tool_info["installed"]:
            status = "✅" if tool_info["meets_requirement"] else "⚠️"
            print(f"  {status} {tool_name}: {tool_info['version']}")
        else:
            print(f"  ❌ {tool_name}: 未安装")
    print()

    # 配置验证
    print("配置验证:")
    config_status = "✅" if report["config_valid"] else "❌"
    print(f"  {config_status} pyproject.toml 配置")
    print()

    # 总体结果
    print("=" * 60)
    overall_status = "✅ 通过" if report["overall_pass"] else "❌ 未通过"
    print(f"总体结果: {overall_status}")
    print("=" * 60)


def fix_common_issues(project_path: Path, report: ValidationReport) -> None:
    """修复常见问题"""
    print("修复建议:")
    print()

    # Python 版本问题
    if not report["python"]["meets_requirement"]:
        print("❌ Python 版本过低")
        print("   建议: 安装 Python 3.13 或更高版本")
        print("   macOS: brew install python@3.13")
        print("   或访问: https://www.python.org/downloads/")
        print()

    # uv 未安装
    if not report["uv"]["installed"]:
        print("❌ uv 未安装")
        print("   修复命令:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print()

    # ruff 问题
    if not report["ruff"]["installed"]:
        print("❌ ruff 未安装")
        print("   修复命令:")
        print("   uv add --dev ruff")
        print()
    elif not report["ruff"]["meets_requirement"]:
        print("⚠️  ruff 版本过低")
        print("   修复命令:")
        print("   uv add --dev ruff --upgrade")
        print()

    # mypy 问题
    if not report["mypy"]["installed"]:
        print("❌ mypy 未安装")
        print("   修复命令:")
        print("   uv add --dev mypy")
        print()
    elif not report["mypy"]["meets_requirement"]:
        print("⚠️  mypy 版本过低")
        print("   修复命令:")
        print("   uv add --dev mypy --upgrade")
        print()

    # pytest 问题
    if not report["pytest"]["installed"]:
        print("❌ pytest 未安装")
        print("   修复命令:")
        print("   uv add --dev pytest")
        print()
    elif not report["pytest"]["meets_requirement"]:
        print("⚠️  pytest 版本过低")
        print("   修复命令:")
        print("   uv add --dev pytest --upgrade")
        print()

    # 配置问题
    if not report["config_valid"]:
        print("❌ pyproject.toml 配置不正确")
        print("   请检查:")
        print("   1. requires-python >= 3.13")
        print("   2. tool.ruff.target-version = 'py313'")
        print("   3. tool.mypy.python_version = '3.13'")
        print()
        print("   参考练习 2 的配置示例")
        print()


def main():
    """主函数"""
    print("=" * 60)
    print("练习 3: 验证环境配置 - 参考答案")
    print("=" * 60)
    print()

    # 获取项目路径
    project_path = Path.cwd()
    print(f"项目路径: {project_path}")
    print()

    # 步骤 1: 检查 Python 版本
    print("步骤 1: 检查 Python 版本")
    python_info = get_python_version()
    status = "✅" if python_info["meets_requirement"] else "❌"
    print(f"  {status} Python {python_info['version']}")
    print()

    # 步骤 2: 检查工具链
    print("步骤 2: 检查工具链")
    tools = ["uv", "ruff", "mypy", "pytest"]
    for tool in tools:
        info = get_tool_version(tool)
        status = "✅" if info["installed"] else "❌"
        version = info["version"] if info["installed"] else "未安装"
        print(f"  {status} {tool}: {version}")
    print()

    # 步骤 3: 验证配置
    print("步骤 3: 验证配置")
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.exists():
        config_valid = validate_pyproject_config(project_path)
        status = "✅" if config_valid else "❌"
        print(f"  {status} pyproject.toml 配置")
    else:
        print("  ⚠️  pyproject.toml 不存在")
    print()

    # 步骤 4: 生成完整报告
    print("步骤 4: 生成完整报告")
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  验证已取消")
        sys.exit(1)
    except ImportError as e:
        print(f"\n❌ 缺少依赖: {e}")
        print("请运行: uv add tomli")
