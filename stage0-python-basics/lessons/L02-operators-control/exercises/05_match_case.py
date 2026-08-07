"""L02 练习5: match-case 模式匹配

难度: ⭐⭐☆ (中等)
预计时间: 25 分钟
知识点: match-case 模式匹配、值匹配、条件匹配

学习方式:
本练习是"演示型练习"——代码已经完整实现，
你需要运行它，观察输出，理解代码的工作原理。

任务描述:
练习 Python 3.10+ 的 match-case 语句，综合运用：
- 简单值匹配
- 带条件的匹配（if 子句）
- 通配符与变量绑定
"""

# ============================================================
# 演示：HTTP 状态码匹配
# ============================================================
print("=== HTTP 状态码匹配演示 ===\n")

print("测试用例 1: code=200")
code = 200
match code:
    case 200:
        result = 'OK - 请求成功'
    case 201:
        result = 'Created - 资源创建成功'
    case 204:
        result = 'No Content - 无内容'
    case 301:
        result = 'Moved Permanently - 永久重定向'
    case 302:
        result = 'Found - 临时重定向'
    case 400:
        result = 'Bad Request - 请求错误'
    case 401:
        result = 'Unauthorized - 未授权'
    case 403:
        result = 'Forbidden - 禁止访问'
    case 404:
        result = 'Not Found - 资源不存在'
    case 500:
        result = 'Internal Server Error - 服务器错误'
    case 502:
        result = 'Bad Gateway - 网关错误'
    case 503:
        result = 'Service Unavailable - 服务不可用'
    case _:
        result = f'Unknown status code: {code}'
print(f"   200 → '{result}'")

print("\n测试用例 2: code=201")
code = 201
match code:
    case 200:
        result = 'OK - 请求成功'
    case 201:
        result = 'Created - 资源创建成功'
    case 204:
        result = 'No Content - 无内容'
    case 301:
        result = 'Moved Permanently - 永久重定向'
    case 302:
        result = 'Found - 临时重定向'
    case 400:
        result = 'Bad Request - 请求错误'
    case 401:
        result = 'Unauthorized - 未授权'
    case 403:
        result = 'Forbidden - 禁止访问'
    case 404:
        result = 'Not Found - 资源不存在'
    case 500:
        result = 'Internal Server Error - 服务器错误'
    case 502:
        result = 'Bad Gateway - 网关错误'
    case 503:
        result = 'Service Unavailable - 服务不可用'
    case _:
        result = f'Unknown status code: {code}'
print(f"   201 → '{result}'")

print("\n测试用例 3: code=404")
code = 404
match code:
    case 200:
        result = 'OK - 请求成功'
    case 201:
        result = 'Created - 资源创建成功'
    case 204:
        result = 'No Content - 无内容'
    case 301:
        result = 'Moved Permanently - 永久重定向'
    case 302:
        result = 'Found - 临时重定向'
    case 400:
        result = 'Bad Request - 请求错误'
    case 401:
        result = 'Unauthorized - 未授权'
    case 403:
        result = 'Forbidden - 禁止访问'
    case 404:
        result = 'Not Found - 资源不存在'
    case 500:
        result = 'Internal Server Error - 服务器错误'
    case 502:
        result = 'Bad Gateway - 网关错误'
    case 503:
        result = 'Service Unavailable - 服务不可用'
    case _:
        result = f'Unknown status code: {code}'
print(f"   404 → '{result}'")

print("\n测试用例 4: code=500")
code = 500
match code:
    case 200:
        result = 'OK - 请求成功'
    case 201:
        result = 'Created - 资源创建成功'
    case 204:
        result = 'No Content - 无内容'
    case 301:
        result = 'Moved Permanently - 永久重定向'
    case 302:
        result = 'Found - 临时重定向'
    case 400:
        result = 'Bad Request - 请求错误'
    case 401:
        result = 'Unauthorized - 未授权'
    case 403:
        result = 'Forbidden - 禁止访问'
    case 404:
        result = 'Not Found - 资源不存在'
    case 500:
        result = 'Internal Server Error - 服务器错误'
    case 502:
        result = 'Bad Gateway - 网关错误'
    case 503:
        result = 'Service Unavailable - 服务不可用'
    case _:
        result = f'Unknown status code: {code}'
print(f"   500 → '{result}'")

print("\n测试用例 5: code=418")
code = 418
match code:
    case 200:
        result = 'OK - 请求成功'
    case 201:
        result = 'Created - 资源创建成功'
    case 204:
        result = 'No Content - 无内容'
    case 301:
        result = 'Moved Permanently - 永久重定向'
    case 302:
        result = 'Found - 临时重定向'
    case 400:
        result = 'Bad Request - 请求错误'
    case 401:
        result = 'Unauthorized - 未授权'
    case 403:
        result = 'Forbidden - 禁止访问'
    case 404:
        result = 'Not Found - 资源不存在'
    case 500:
        result = 'Internal Server Error - 服务器错误'
    case 502:
        result = 'Bad Gateway - 网关错误'
    case 503:
        result = 'Service Unavailable - 服务不可用'
    case _:
        result = f'Unknown status code: {code}'
print(f"   418 → '{result}'")

# ============================================================
# 演示：命令解析（使用 match-case）
# ============================================================
print("\n=== 命令解析演示 ===\n")

print("测试用例 1: 'git status'")
command = 'git status'
match command:
    case 'git status':
        result = 'git 子命令: status'
    case s if s.startswith('git checkout '):
        result = 'git 子命令: checkout'
    case s if s.startswith('git push '):
        result = 'git push 命令'
    case s if s.startswith('npm '):
        result = 'npm 命令'
    case _:
        result = f'Unknown command: {command}'
print(f"   '{command}' → '{result}'")

print("\n测试用例 2: 'git checkout main'")
command = 'git checkout main'
match command:
    case 'git status':
        result = 'git 子命令: status'
    case s if s.startswith('git checkout '):
        result = 'git 子命令: checkout'
    case s if s.startswith('git push '):
        result = 'git push 命令'
    case s if s.startswith('npm '):
        result = 'npm 命令'
    case _:
        result = f'Unknown command: {command}'
print(f"   '{command}' → '{result}'")

print("\n测试用例 3: 'git push origin main'")
command = 'git push origin main'
match command:
    case 'git status':
        result = 'git 子命令: status'
    case s if s.startswith('git checkout '):
        result = 'git 子命令: checkout'
    case s if s.startswith('git push '):
        result = 'git push 命令'
    case s if s.startswith('npm '):
        result = 'npm 命令'
    case _:
        result = f'Unknown command: {command}'
print(f"   '{command}' → '{result}'")

print("\n测试用例 4: 'npm install'")
command = 'npm install'
match command:
    case 'git status':
        result = 'git 子命令: status'
    case s if s.startswith('git checkout '):
        result = 'git 子命令: checkout'
    case s if s.startswith('git push '):
        result = 'git push 命令'
    case s if s.startswith('npm '):
        result = 'npm 命令'
    case _:
        result = f'Unknown command: {command}'
print(f"   '{command}' → '{result}'")

print("\n测试用例 5: 'unknown cmd'")
command = 'unknown cmd'
match command:
    case 'git status':
        result = 'git 子命令: status'
    case s if s.startswith('git checkout '):
        result = 'git 子命令: checkout'
    case s if s.startswith('git push '):
        result = 'git push 命令'
    case s if s.startswith('npm '):
        result = 'npm 命令'
    case _:
        result = f'Unknown command: {command}'
print(f"   '{command}' → '{result}'")

# ============================================================
# 演示：坐标分类（使用 match-case）
# ============================================================
print("\n=== 坐标分类演示 ===\n")

print("测试用例 1: x=0, y=0 → 原点")
x, y = 0, 0
match (x, y):
    case (0, 0):
        result = '原点'
    case (px, 0) if px > 0:
        result = 'x轴正半轴'
    case (nx, 0) if nx < 0:
        result = 'x轴负半轴'
    case (0, py) if py > 0:
        result = 'y轴正半轴'
    case (0, ny) if ny < 0:
        result = 'y轴负半轴'
    case (px, py) if px > 0 and py > 0:
        result = '第一象限'
    case (nx, py) if nx < 0 and py > 0:
        result = '第二象限'
    case (nx, ny) if nx < 0 and ny < 0:
        result = '第三象限'
    case (px, ny) if px > 0 and ny < 0:
        result = '第四象限'
    case _:
        result = '未知位置'
print(f"   (0, 0) → '{result}'")

print("\n测试用例 2: x=5, y=0 → x轴正半轴")
x, y = 5, 0
match (x, y):
    case (0, 0):
        result = '原点'
    case (px, 0) if px > 0:
        result = 'x轴正半轴'
    case (nx, 0) if nx < 0:
        result = 'x轴负半轴'
    case (0, py) if py > 0:
        result = 'y轴正半轴'
    case (0, ny) if ny < 0:
        result = 'y轴负半轴'
    case (px, py) if px > 0 and py > 0:
        result = '第一象限'
    case (nx, py) if nx < 0 and py > 0:
        result = '第二象限'
    case (nx, ny) if nx < 0 and ny < 0:
        result = '第三象限'
    case (px, ny) if px > 0 and ny < 0:
        result = '第四象限'
    case _:
        result = '未知位置'
print(f"   (5, 0) → '{result}'")

print("\n测试用例 3: x=3, y=4 → 第一象限")
x, y = 3, 4
match (x, y):
    case (0, 0):
        result = '原点'
    case (px, 0) if px > 0:
        result = 'x轴正半轴'
    case (nx, 0) if nx < 0:
        result = 'x轴负半轴'
    case (0, py) if py > 0:
        result = 'y轴正半轴'
    case (0, ny) if ny < 0:
        result = 'y轴负半轴'
    case (px, py) if px > 0 and py > 0:
        result = '第一象限'
    case (nx, py) if nx < 0 and py > 0:
        result = '第二象限'
    case (nx, ny) if nx < 0 and ny < 0:
        result = '第三象限'
    case (px, ny) if px > 0 and ny < 0:
        result = '第四象限'
    case _:
        result = '未知位置'
print(f"   (3, 4) → '{result}'")

# ============================================================
# 思考题
# ============================================================
print("\n=== 思考题 ===")
print("1. match-case 和 if-elif-else 的区别是什么？")
print("2. case _ 的作用是什么？")
print("3. 带守卫的条件匹配（if）什么时候会执行？")
