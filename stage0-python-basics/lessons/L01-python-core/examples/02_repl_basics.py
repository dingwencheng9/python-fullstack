"""L01 示例2: Python REPL 基础与自学工具

本文件演示 REPL（交互式解释器）的核心用法，以及三个最重要的自学工具：
- type()：查看对象类型
- dir()：探索对象能力
- help()：阅读函数文档

在终端运行 `python` 启动 REPL，逐行输入代码验证。

"""

# ===== 1. type() — 查看对象的类型 =====
print("=== type() — 查看对象类型 ===")
# 场景：你不确定 input() 返回什么？在 REPL 里验证
print(f"type(42)      = {type(42).__name__!r}")  # 'int'
print(f"type(3.14)    = {type(3.14).__name__!r}")  # 'float'
print(f"type('hi')    = {type('hi').__name__!r}")  # 'str'
print(f"type(True)    = {type(True).__name__!r}")  # 'bool'
print(f"type(None)    = {type(None).__name__!r}")  # 'NoneType'

# 关键验证：input() 返回的是字符串，不是数字
user_input = "25"  # 模拟用户输入
print(f"\n🔑 关键验证：type(input()) = {type(user_input)}")  # str，不是 int


# ===== 2. dir() — 探索对象能做什么 =====
print("\n=== dir() — 探索对象能力 ===")
# 场景：字符串有多少方法？看看 str 有哪些常用方法
# 注意：这里列出的是字符串的公开方法（不含下划线开头的方法）
# L03 会学到如何用列表推导式自动筛选，L02 会学到如何用 if 判断
methods = [
    "capitalize",
    "casefold",
    "center",
    "count",
    "encode",
    "endswith",
    "expandtabs",
    "find",
    "format",
    "index",
    "isalnum",
    "isalpha",
    "isascii",
    "isdecimal",
    "isdigit",
    "isidentifier",
    "islower",
    "isnumeric",
    "isprintable",
    "isspace",
    "istitle",
    "isupper",
    "join",
    "ljust",
    "lower",
    "lstrip",
    "maketrans",
    "partition",
    "replace",
    "rfind",
    "rindex",
    "rjust",
    "rpartition",
    "rsplit",
    "rstrip",
    "split",
    "splitlines",
    "startswith",
    "strip",
    "swapcase",
    "title",
    "translate",
    "upper",
    "zfill",
]
print(f"str 共有 {len(methods)} 个公开方法")
print("含 'upper' 的方法: ['upper', 'swapcase']")
print("含 'split' 的方法: ['split', 'rsplit', 'splitlines']")


# ===== 3. help() — 阅读函数文档 =====
print("\n=== help() — 阅读函数文档 ===")
# 在 REPL 中输入 help(print) 查看 print 的完整签名：
#   print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
# 参数说明：
#   sep   : 多个值之间的分隔符，默认是空格
#   end   : 结束时追加的字符，默认是换行符
#   flush : 是否立即刷新输出，默认 False

# 演示 sep 和 end 参数
print("A", "B", "C", sep=" | ", end=" ← 结束\n")


# ===== 4. 整数和字符串的比较（用 ==，不用 is）=====
print("\n=== 整数和字符串的比较 ===")
i = 10
j = 10
print(f"i = {i}, j = {j}")
print(f"i == j: {i == j}")  # True：值相等

# ===== 5. 变量引用与 == =====
print("\n=== 变量比较（用 == 而非 is）===")
x = 100
y = x
print("x = 100, y = x")
print(f"x == y: {x == y}")  # True：值相等

# ===== 6. REPL 快捷键参考 =====
print("\n=== REPL 快捷键参考 ===")
shortcuts = [
    ("↑ / ↓", "浏览历史命令（最重要，必须会用）"),
    ("Tab", "自动补全变量/函数名"),
    ("Ctrl+D", "退出 REPL（Mac/Linux）"),
    ("Ctrl+Z", "退出 REPL（Windows）"),
    ("Ctrl+L", "清屏"),
    ("Ctrl+C", "取消当前输入"),
]
