"""参考答案 5: match-case 模式匹配"""


def describe_http_status(code: int) -> str:
    """描述 HTTP 状态码。

    Args:
        code: HTTP 状态码

    Returns:
        状态码描述

    Examples:
        >>> describe_http_status(200)
        'OK - 请求成功'
        >>> describe_http_status(404)
        'Not Found - 资源不存在'
        >>> describe_http_status(500)
        'Internal Server Error - 服务器错误'
        >>> describe_http_status(418)
        'Unknown status code: 418'
    """
    # 使用 match-case 实现状态码描述
    match code:
        case 200:
            return "OK - 请求成功"
        case 201:
            return "Created - 资源创建成功"
        case 301:
            return "Moved Permanently - 永久重定向"
        case 400:
            return "Bad Request - 请求错误"
        case 401:
            return "Unauthorized - 未授权"
        case 403:
            return "Forbidden - 禁止访问"
        case 404:
            return "Not Found - 资源不存在"
        case 500:
            return "Internal Server Error - 服务器错误"
        case 502:
            return "Bad Gateway - 网关错误"
        case 503:
            return "Service Unavailable - 服务不可用"
        case _:
            return f"Unknown status code: {code}"


def parse_command(command: str) -> str:
    """解析命令行命令。

    Args:
        command: 命令字符串（如 "git commit -m 'fix bug'"）

    Returns:
        命令描述

    Examples:
        >>> parse_command("git status")
        'git 子命令: status'
        >>> parse_command("git checkout main")
        'git 子命令: checkout, 参数: main'
        >>> parse_command("git push origin main")
        'git push 到 origin/main'
        >>> parse_command("npm install")
        'npm 命令: install'
        >>> parse_command("unknown cmd")
        'Unknown command: unknown cmd'
    """
    # 使用 match-case 解析命令
    parts = command.split()
    match parts:
        case ["git", "status"]:
            return "git 子命令: status"
        case ["git", "checkout", arg]:
            return f"git 子命令: checkout, 参数: {arg}"
        case ["git", "push", origin, target]:
            return f"git push 到 {origin}/{target}"
        case ["npm", cmd]:
            return f"npm 命令: {cmd}"
        case _:
            first_word = parts[0] if parts else ""
            return f"Unknown command: {first_word}"


def classify_point(x: int, y: int) -> str:
    """分类二维坐标点。

    Args:
        x: x 坐标
        y: y 坐标

    Returns:
        点的位置描述

    Examples:
        >>> classify_point(0, 0)
        '原点'
        >>> classify_point(5, 0)
        'x轴正半轴'
        >>> classify_point(0, -3)
        'y轴负半轴'
        >>> classify_point(3, 4)
        '第一象限'
        >>> classify_point(-2, 5)
        '第二象限'
        >>> classify_point(-3, -1)
        '第三象限'
        >>> classify_point(2, -4)
        '第四象限'
    """
    # 使用 match-case 分类坐标点
    # 用 (x, y) 元组匹配
    match (x, y):
        case (0, 0):
            return "原点"
        case (x, 0) if x > 0:
            return "x轴正半轴"
        case (x, 0) if x < 0:
            return "x轴负半轴"
        case (0, y) if y > 0:
            return "y轴正半轴"
        case (0, y) if y < 0:
            return "y轴负半轴"
        case (x, y) if x > 0 and y > 0:
            return "第一象限"
        case (x, y) if x < 0 and y > 0:
            return "第二象限"
        case (x, y) if x < 0 and y < 0:
            return "第三象限"
        case (x, y) if x > 0 and y < 0:
            return "第四象限"
        case _:
            # 这应该不会发生，但作为兜底
            return "未知位置"


if __name__ == "__main__":
    print("=== HTTP 状态码测试 ===")
    tests = [
        (200, "OK - 请求成功"),
        (201, "Created - 资源创建成功"),
        (404, "Not Found - 资源不存在"),
        (500, "Internal Server Error - 服务器错误"),
        (418, "Unknown status code: 418"),
    ]
    for code, expected in tests:
        result = describe_http_status(code)
        status = "✓" if result == expected else "✗"
        print(f"{status} describe_http_status({code}) = '{result}'")

    print("\n=== 命令解析测试 ===")
    tests = [
        ("git status", "git 子命令: status"),
        ("git checkout main", "git 子命令: checkout, 参数: main"),
        ("git push origin main", "git push 到 origin/main"),
        ("npm install", "npm 命令: install"),
        ("unknown cmd", "Unknown command: unknown"),
    ]
    for cmd, expected in tests:
        result = parse_command(cmd)
        status = "✓" if result == expected else "✗"
        print(f"{status} parse_command('{cmd}') = '{result}'")

    print("\n=== 坐标分类测试 ===")
    tests = [
        ((0, 0), "原点"),
        ((5, 0), "x轴正半轴"),
        ((-3, 0), "x轴负半轴"),
        ((0, 5), "y轴正半轴"),
        ((0, -3), "y轴负半轴"),
        ((3, 4), "第一象限"),
        ((-2, 5), "第二象限"),
        ((-3, -1), "第三象限"),
        ((2, -4), "第四象限"),
    ]
    for (x, y), expected in tests:
        result = classify_point(x, y)
        status = "✓" if result == expected else "✗"
        print(f"{status} classify_point({x}, {y}) = '{result}'")
