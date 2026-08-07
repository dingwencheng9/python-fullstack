"""示例：常用标准库

演示 Python 常用标准库的使用。
"""

# ============ math 模块 ============
import math

print("=== math 模块 ===")
print(f"math.sqrt(16) = {math.sqrt(16)}")  # 平方根
print(f"math.pi = {math.pi}")  # 圆周率
print(f"math.e = {math.e}")  # 自然常数
print(f"math.ceil(3.2) = {math.ceil(3.2)}")  # 向上取整
print(f"math.floor(3.8) = {math.floor(3.8)}")  # 向下取整
print(f"math.pow(2, 3) = {math.pow(2, 3)}")  # 幂运算
print(f"math.log(e) = {math.log(math.e)}")  # 对数

# ============ random 模块 ============
import random  # noqa: E402

print("\n=== random 模块 ===")
print(f"random.random() = {random.random()}")  # 0-1 随机浮点数
print(f"random.randint(1, 10) = {random.randint(1, 10)}")  # 整数随机
print(f"random.choice(['a', 'b', 'c']) = {random.choice(['a', 'b', 'c'])}")  # 随机选择
print(f"random.sample([1,2,3,4,5], 3) = {random.sample([1, 2, 3, 4, 5], 3)}")  # 随机抽样

# 使用固定种子（可复现的随机）
random.seed(42)
print(f"固定种子: {random.random()}, {random.random()}")
random.seed(42)
print(f"相同种子: {random.random()}, {random.random()}")

# ============ datetime 模块 ============
from datetime import datetime, timedelta  # noqa: E402

print("\n=== datetime 模块 ===")
now = datetime.now()
print(f"当前时间: {now}")
print(f"格式化: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 日期计算
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)
print(f"明天: {tomorrow.strftime('%Y-%m-%d')}")
print(f"昨天: {yesterday.strftime('%Y-%m-%d')}")

# ============ json 模块 ============
import json  # noqa: E402

print("\n=== json 模块 ===")
data = {"name": "Alice", "age": 30, "city": "Beijing"}
json_str = json.dumps(data, ensure_ascii=False)
print(f"字典转 JSON: {json_str}")

parsed = json.loads(json_str)
print(f"JSON 转字典: {parsed}")

# ============ os 模块 ============
import os  # noqa: E402

print("\n=== os 模块 ===")
print(f"当前目录: {os.getcwd()}")
print(f"系统路径分隔符: {os.sep}")
print(f"环境变量 HOME: {os.environ.get('HOME', 'N/A')}")

# ============ pathlib 模块 ============
# pathlib 是处理文件路径的现代方式，将在 L05 文件操作 中详细学习
# 基础示例（预告）：
print("\n=== pathlib 模块（预览）===")
from pathlib import Path  # noqa: E402

home = Path.home()
print(f"家目录: {home}")
print(f"当前文件: {Path(__file__).name}")
print("（L05 将详细学习 pathlib 文件操作）")


if __name__ == "__main__":
    print("\n=== 常用标准库总结 ===")
    print("- math: 数学运算")
    print("- random: 随机数")
    print("- datetime: 日期时间")
    print("- json: JSON 序列化")
    print("- os: 操作系统接口")
    print("- pathlib: 路径操作")
    print("- collections: 容器数据类型")
    print("- itertools: 迭代器工具")
    print("- functools: 函数式编程工具")
