"""

from __future__ import annotations

L21 示例 4: Python 3.10+ match/case 模式匹配

展示 Python 3.10+ 的模式匹配功能（在 Python 3.13 中进一步优化）：
1. 基础模式匹配
2. 结构化模式匹配
3. 守卫条件
4. 错误处理中的模式匹配

作者: Python 3.13 全栈课程
日期: 2026-06-09
Python版本: 3.10+ (在 3.13 中性能更优)
"""

from dataclasses import dataclass

# ============================================
# 1. 基础模式匹配
# ============================================


def handle_http_status(status: int) -> str:
    """
    使用 match/case 处理 HTTP 状态码

    Python 3.13 性能优化:
    - match 语句字节码优化
    - 跳转表加速
    """
    match status:
        case 200:
            return "成功"
        case 201:
            return "已创建"
        case 400:
            return "请求错误"
        case 401:
            return "未授权"
        case 403:
            return "禁止访问"
        case 404:
            return "未找到"
        case 500:
            return "服务器错误"
        case _:
            return f"未知状态码: {status}"


def classify_value(value: int | str | list | dict) -> str:
    """
    使用 match/case 分类值类型
    """
    match value:
        case int(x) if x > 0:
            return f"正整数: {x}"
        case int(x) if x < 0:
            return f"负整数: {x}"
        case int(0):
            return "零"
        case str(s) if len(s) > 0:
            return f"非空字符串: {s}"
        case str():
            return "空字符串"
        case list() if len(value) == 0:
            return "空列表"
        case list():
            return f"列表，长度: {len(value)}"
        case dict() if len(value) == 0:
            return "空字典"
        case dict():
            return f"字典，键数: {len(value)}"
        case _:
            return "未知类型"


# ============================================
# 2. 结构化模式匹配
# ============================================


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Circle:
    center: Point
    radius: int


@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point


def describe_shape(shape: Point | Circle | Rectangle) -> str:
    """
    使用 match/case 描述几何形状

    结构化模式匹配:
    - 解构数据类
    - 提取嵌套属性
    """
    match shape:
        case Point(x=0, y=0):
            return "原点"
        case Point(x=0, y=y):
            return f"Y 轴上的点: (0, {y})"
        case Point(x=x, y=0):
            return f"X 轴上的点: ({x}, 0)"
        case Point(x=x, y=y):
            return f"点: ({x}, {y})"
        case Circle(center=Point(x=cx, y=cy), radius=r):
            return f"圆心在 ({cx}, {cy})，半径 {r}"
        case Rectangle(top_left=Point(x=x1, y=y1), bottom_right=Point(x=x2, y=y2)):
            width = x2 - x1
            height = y2 - y1
            return f"矩形: 宽 {width}，高 {height}"
        case _:
            return "未知形状"


# ============================================
# 3. 错误处理中的模式匹配
# ============================================


def handle_error_with_match(error: Exception) -> str:
    """
    使用 match/case 处理不同错误类型

    Python 3.13 彩色错误 + match/case 完美结合
    """
    match error:
        case TypeError():
            return "类型错误：请检查数据类型"
        case ValueError() if "invalid literal" in str(error):
            return f"值转换错误: {error}"
        case ValueError():
            return "值错误：请检查数据格式"
        case KeyError():
            return f"键错误：字典中不存在键 '{error.args[0] if error.args else 'unknown'}'"
        case IndexError():
            return "索引错误：列表索引超出范围"
        case AttributeError() if "has no attribute" in str(error):
            return f"属性错误: {error}"
        case FileNotFoundError():
            return f"文件未找到: {error}"
        case _:
            return f"其他错误：{type(error).__name__}: {error}"


# ============================================
# 4. 命令处理器示例
# ============================================


@dataclass
class Command:
    action: str
    args: list[str]


def execute_command(cmd: Command) -> str:
    """
    使用 match/case 实现命令处理器

    守卫条件:
    - if 子句添加额外约束
    - 多重条件组合
    """
    match cmd:
        case Command(action="help", args=[]):
            return "显示帮助信息"
        case Command(action="help", args=[topic]):
            return f"显示 {topic} 的帮助"
        case Command(action="list", args=[]):
            return "列出所有项目"
        case Command(action="list", args=[category]):
            return f"列出 {category} 类别的项目"
        case Command(action="get", args=[id]) if id.isdigit():
            return f"获取 ID {id} 的项目"
        case Command(action="get", args=[name]):
            return f"获取名称为 {name} 的项目"
        case Command(action="delete", args=[id]) if id.isdigit():
            return f"删除 ID {id} 的项目"
        case Command(action=action, args=args):
            return f"未知命令: {action}，参数: {args}"
        case _:
            return "无效的命令格式"


# ============================================
# 5. JSON 数据处理
# ============================================


def process_api_response(response: dict[str, str | int | list]) -> str:
    """
    使用 match/case 处理 API 响应

    字典模式匹配:
    - 匹配特定键
    - 提取嵌套值
    """
    match response:
        case {"status": "success", "data": data}:
            return f"成功: {data}"
        case {"status": "error", "message": msg, "code": code}:
            return f"错误 {code}: {msg}"
        case {"status": "error", "message": msg}:
            return f"错误: {msg}"
        case {"status": status}:
            return f"状态: {status}"
        case _:
            return "无效的响应格式"


# ============================================
# 6. 演示函数
# ============================================


def demonstrate_match_case() -> None:
    """演示 match/case 功能"""
    print("=" * 70)
    print("Python 3.10+ match/case 模式匹配演示")
    print("=" * 70)
    print()

    # 示例 1: HTTP 状态码
    print("1️⃣ HTTP 状态码处理")
    print("-" * 70)
    for status in [200, 404, 500, 999]:
        print(f"  {status} → {handle_http_status(status)}")

    # 示例 2: 类型分类
    print("\n\n2️⃣ 值类型分类")
    print("-" * 70)
    values: list[int | str | list | dict] = [
        42,
        -5,
        0,
        "hello",
        "",
        [],
        [1, 2],
        {},
        {"key": "value"},
    ]
    for value in values:
        print(f"  {value!r} → {classify_value(value)}")

    # 示例 3: 几何形状
    print("\n\n3️⃣ 几何形状描述")
    print("-" * 70)
    shapes = [
        Point(0, 0),
        Point(3, 0),
        Point(0, 4),
        Point(3, 4),
        Circle(Point(0, 0), 5),
        Rectangle(Point(0, 0), Point(10, 5)),
    ]
    for shape in shapes:
        print(f"  {describe_shape(shape)}")

    # 示例 4: 错误处理
    print("\n\n4️⃣ 错误处理")
    print("-" * 70)
    errors = [
        TypeError("unsupported operand type(s)"),
        ValueError("invalid literal for int()"),
        KeyError("missing_key"),
        IndexError("list index out of range"),
    ]
    for error in errors:
        print(f"  {type(error).__name__} → {handle_error_with_match(error)}")

    # 示例 5: 命令处理
    print("\n\n5️⃣ 命令处理")
    print("-" * 70)
    commands = [
        Command("help", []),
        Command("help", ["api"]),
        Command("list", []),
        Command("get", ["123"]),
        Command("delete", ["abc"]),
    ]
    for cmd in commands:
        print(f"  {cmd.action} {cmd.args} → {execute_command(cmd)}")

    # 示例 6: API 响应
    print("\n\n6️⃣ API 响应处理")
    print("-" * 70)
    responses = [
        {"status": "success", "data": {"id": 1}},
        {"status": "error", "message": "Not found", "code": 404},
        {"status": "error", "message": "Bad request"},
        {"status": "pending"},
    ]
    for response in responses:
        print(f"  {response}")
        print(f"    → {process_api_response(response)}")


def show_performance_notes() -> None:
    """展示性能说明"""
    print("\n\n" + "=" * 70)
    print("Python 3.13 match/case 性能优化")
    print("=" * 70)

    print("\n性能改进:")
    print("  • 字节码优化: 减少不必要的跳转")
    print("  • 跳转表加速: 整数模式匹配使用跳转表")
    print("  • 模式编译优化: 复杂模式编译更高效")
    print("  • 预期性能提升: 10-20% (相比 Python 3.11)")

    print("\n最佳实践:")
    print("  • 常见情况放在前面")
    print("  • 使用守卫条件细化匹配")
    print("  • 结构化模式匹配解构数据")
    print("  • 配合 dataclass 使用效果更佳")


def main() -> None:
    """主函数"""
    demonstrate_match_case()
    show_performance_notes()

    print("\n\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n💡 关键要点:")
    print("  • match/case 比 if/elif/else 更清晰")
    print("  • 结构化模式匹配功能强大")
    print("  • 守卫条件提供额外约束")
    print("  • Python 3.13 性能进一步优化")
    print()


if __name__ == "__main__":
    main()
