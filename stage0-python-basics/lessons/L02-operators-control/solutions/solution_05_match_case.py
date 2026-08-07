"""参考答案 5: match-case 模式匹配

对应练习: exercises/05_match_case.py
知识点: match-case 模式匹配、值匹配、条件匹配

本参考答案为演示型练习的完整实现版本。
"""


def describe_http_status(code):
    """描述 HTTP 状态码。

    Args:
        code: HTTP 状态码

    Returns:
        状态码描述
    """
    match code:
        case 200:
            return 'OK - 请求成功'
        case 201:
            return 'Created - 资源创建成功'
        case 204:
            return 'No Content - 无内容'
        case 301:
            return 'Moved Permanently - 永久重定向'
        case 302:
            return 'Found - 临时重定向'
        case 400:
            return 'Bad Request - 请求错误'
        case 401:
            return 'Unauthorized - 未授权'
        case 403:
            return 'Forbidden - 禁止访问'
        case 404:
            return 'Not Found - 资源不存在'
        case 500:
            return 'Internal Server Error - 服务器错误'
        case 502:
            return 'Bad Gateway - 网关错误'
        case 503:
            return 'Service Unavailable - 服务不可用'
        case _:
            return f'Unknown status code: {code}'


def parse_command(command):
    """解析命令行命令。

    Args:
        command: 命令字符串

    Returns:
        命令描述
    """
    parts = command.split()
    if not parts:
        return f'Unknown command: {command}'

    match parts:
        case ['git', 'push', origin, branch]:
            return f'git push 到 {origin}/{branch}'
        case ['git', subcmd]:
            return f'git 子命令: {subcmd}'
        case ['git', subcmd, *_]:
            return f'git 子命令: {subcmd}'
        case ['npm', action]:
            return f'npm 命令: {action}'
        case ['npm', action, *_]:
            return f'npm 命令: {action}'
        case [cmd]:
            return f'Unknown command: {cmd}'
        case _:
            return f'Unknown command: {command}'


def classify_point(x, y):
    """分类二维坐标点。

    Args:
        x: x 坐标
        y: y 坐标

    Returns:
        点的位置描述
    """
    match (x, y):
        case (0, 0):
            return '原点'
        case (x, 0) if x > 0:
            return 'x轴正半轴'
        case (x, 0) if x < 0:
            return 'x轴负半轴'
        case (0, y) if y > 0:
            return 'y轴正半轴'
        case (0, y) if y < 0:
            return 'y轴负半轴'
        case (x, y) if x > 0 and y > 0:
            return '第一象限'
        case (x, y) if x < 0 and y > 0:
            return '第二象限'
        case (x, y) if x < 0 and y < 0:
            return '第三象限'
        case (x, y) if x > 0 and y < 0:
            return '第四象限'
        case _:
            return '未知位置'


if __name__ == '__main__':
    print('=== HTTP 状态码测试 ===')
    tests = [
        (200, 'OK - 请求成功'),
        (201, 'Created - 资源创建成功'),
        (404, 'Not Found - 资源不存在'),
        (500, 'Internal Server Error - 服务器错误'),
        (418, 'Unknown status code: 418'),
    ]
    for code, expected in tests:
        result = describe_http_status(code)
        status = '✓' if result == expected else '✗'
        print(f"{status} describe_http_status({code}) = '{result}'")

    print('\n=== 命令解析测试 ===')
    tests = [
        ('git status', 'git 子命令: status'),
        ('git checkout main', 'git 子命令: checkout'),
        ('git push origin main', 'git push 到 origin/main'),
        ('npm install', 'npm 命令: install'),
        ('unknown cmd', 'Unknown command: unknown cmd'),
    ]
    for cmd, expected in tests:
        result = parse_command(cmd)
        status = '✓' if result == expected else '✗'
        print(f"{status} parse_command('{cmd}') = '{result}'")

    print('\n=== 坐标分类测试 ===')
    tests = [
        ((0, 0), '原点'),
        ((5, 0), 'x轴正半轴'),
        ((-3, 0), 'x轴负半轴'),
        ((0, 5), 'y轴正半轴'),
        ((0, -3), 'y轴负半轴'),
        ((3, 4), '第一象限'),
        ((-2, 5), '第二象限'),
        ((-3, -1), '第三象限'),
        ((2, -4), '第四象限'),
    ]
    for (x, y), expected in tests:
        result = classify_point(x, y)
        status = '✓' if result == expected else '✗'
        print(f"{status} classify_point({x}, {y}) = '{result}'")
