# L18: 正则表达式

> **课程编号**: L18
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 4 小时
> **难度**: ⭐⭐⭐☆☆（中级）
> **前置课程**: L03 数据结构、L10 类型系统
> **版本**: v1.0
> **最后更新**: 2026-08-07
> **学习目标**: 掌握正则表达式语法、re 模块 API、字符类、量词、分组捕获、环视断言

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 理解正则表达式的核心概念和匹配原理
2. ✅ 熟练使用字符类、量词、锚点
3. ✅ 掌握分组捕获和命名分组
4. ✅ 使用环视断言进行高级匹配
5. ✅ 熟练使用 re 模块的常用方法
6. ✅ 编写高效且可维护的正则表达式

---

## 📚 核心内容

### Part 1: 正则表达式基础

#### 1.1 什么是正则表达式？

正则表达式（Regular Expression）是一种**用于匹配字符串模式**的强大工具。

```python
import re

# 最简单的匹配
pattern = r"hello"
text = "hello world"

if re.search(pattern, text):
    print("找到匹配！")  # 输出: 找到匹配！
```

**为什么需要正则表达式？**

| 场景 | 字符串方法 | 正则表达式 |
|------|------------|------------|
| 验证邮箱格式 | `email.count("@") == 1` | `r"^[\w.-]+@[\w.-]+\.\w+$"` |
| 提取数字 | `for c in s if c.isdigit()` | `r"\d+"` |
| 替换格式 | 多次 replace | `re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", s)` |
| 验证手机号 | 长度+首位判断 | `r"^1[3-9]\d{9}$"` |

#### 1.2 re 模块核心方法

```python
import re

text = "订单号: A123, 日期: 2024-01-15, 金额: ¥299.00"

# search: 查找第一个匹配
match = re.search(r"\d{4}-\d{2}-\d{2}", text)
if match:
    print(f"找到日期: {match.group()}")  # 2024-01-15

# match: 从字符串开头匹配
result = re.match(r"订单号:", text)
print(result is not None)  # True

# fullmatch: 完全匹配
pattern = r"^[\w\s,:-]+$"
print(re.fullmatch(pattern, text))  # Match object

# findall: 查找所有匹配
numbers = re.findall(r"\d+", text)
print(numbers)  # ['123', '2024', '01', '15', '299', '00']

# finditer: 返回迭代器
for m in re.finditer(r"\d+", text):
    print(f"数字 {m.group()} 在位置 {m.start()}-{m.end()}")
```

#### 1.3 原始字符串的重要性

```python
# ❌ 错误：\n 被解释为换行符
pattern1 = "\n+"  # 匹配一个或多个换行

# ✅ 正确：使用原始字符串
pattern2 = r"\n+"  # 匹配一个或多个字面反斜杠+n

# 更复杂的例子
# 匹配数字：\d 需要写成 r"\d" 而非 "\d"
text = "价格: 199元"
print(re.search(r"\d+", text).group())  # 199
```

---

### Part 2: 字符类

#### 2.1 内置字符类

```python
import re

text = "Hello World! 123"

# \d: 数字 [0-9]
print(re.findall(r"\d", text))  # ['1', '2', '3']

# \D: 非数字 [^0-9]
print(re.findall(r"\D", text))  # ['H', 'e', 'l', 'l', 'o', ...]

# \w: 单词字符 [a-zA-Z0-9_]
print(re.findall(r"\w", text))  # ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd', '1', '2', '3']

# \W: 非单词字符
print(re.findall(r"\W", text))  # [' ', ' ', '!']

# \s: 空白字符（空格、tab、换行）
print(re.findall(r"\s", "a b\tc\nd"))  # [' ', '\t', '\n']

# \S: 非空白字符
print(re.findall(r"\S", "a b c"))  # ['a', 'b', 'c']

# . : 任意字符（除换行）
print(re.findall(r".{3}", "abc def"))  # ['abc', ' de'] (最后可能截断)
```

#### 2.2 自定义字符类

```python
import re

# [abc]: 匹配 a、b 或 c
print(re.findall(r"[aeiou]", "hello world"))  # ['e', 'o', 'o']

# [a-z]: 匹配小写字母
print(re.findall(r"[a-z]+", "Hello World"))  # ['ello', 'orld']

# [A-Z]: 匹配大写字母
print(re.findall(r"[A-Z][a-z]*", "Hello World"))  # ['Hello', 'World']

# [0-9]: 匹配数字
print(re.findall(r"[0-9]{2}", "a1b22c333"))  # ['22', '33']

# [^abc]: 排除字符
print(re.findall(r"[^aeiou\s]", "hello world"))  # ['h', 'l', 'l', 'w', 'r', 'l', 'd']
```

#### 2.3 字符类实战

```python
import re

# 匹配中国手机号
china_mobile = r"1[3-9]\d{9}"
phones = ["13812345678", "12345678901", "+86-13812345678"]
for phone in phones:
    match = re.search(china_mobile, phone)
    print(f"{phone}: {'有效' if match else '无效'}")

# 匹配 IPv4 地址
ipv4 = r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
text = "服务器: 192.168.1.1, DNS: 8.8.8.8"
print(re.findall(ipv4, text))  # ['192.168.1.1', '8.8.8.8']

# 匹配十六进制颜色
hex_color = r"#[0-9a-fA-F]{6}\b"
colors = ["#FF5733", "#abc123", "#GGG"]  # GGG 不匹配
for color in colors:
    match = re.fullmatch(hex_color, color)
    print(f"{color}: {'有效' if match else '无效'}")
```

---

### Part 3: 量词

#### 3.1 基本量词

```python
import re

text = "go gogle google gooogle color colour"

# * : 0 次或多次
print(re.findall(r"go*le", text))  # ['gogle', 'google', 'gooogle']

# + : 1 次或多次
print(re.findall(r"go+le", text))  # ['gogle', 'google', 'gooogle']

# ? : 0 次或 1 次
print(re.findall(r"colou?r", text))  # ['color', 'colour']

# {n} : 恰好 n 次
print(re.findall(r"\d{3}", "abc123def45"))  # ['123']

# {n,} : 至少 n 次
print(re.findall(r"\d{2,}", "1 22 333 4444"))  # ['22', '333', '4444']

# {n,m} : n 到 m 次
print(re.findall(r"\d{2,3}", "1 22 333 4444"))  # ['22', '333', '444']
```

#### 3.2 贪婪 vs 非贪婪

```python
import re

html = "<div>内容1</div><div>内容2</div>"

# 贪婪：尽可能多地匹配
print(re.search(r"<div>.*</div>", html).group())
# 输出: <div>内容1</div><div>内容2</div> (整个字符串)

# 非贪婪：尽可能少地匹配
print(re.search(r"<div>.*?</div>", html).group())
# 输出: <div>内容1</div> (第一个匹配)

# 常见陷阱：提取数字
numbers = "a123b456c"
print(re.search(r"\d+", numbers).group())  # 贪婪: 123456
print(re.search(r"\d+?", numbers).group())  # 非贪婪: 1

# 量词后跟 ?: 变成非贪婪
print(re.findall(r"\d{2,4}?", numbers))  # ['12', '34', '56']
```

#### 3.3 锚点

```python
import re

lines = """第一行
第二行
第三行"""

# ^ : 行首（配合 re.MULTILINE）
print(re.findall(r"^\w+", lines, re.MULTILINE))  # ['第一', '第二', '第三']

# $ : 行尾
print(re.findall(r"\w+$", lines, re.MULTILINE))  # ['行', '行', '行']

# \b : 单词边界
text = "cat scatter category bobcat"
print(re.findall(r"\bcat\b", text))  # ['cat'] (不含 category/cat*)

# \B : 非单词边界
print(re.findall(r"\Bcat\B", text))  # ['cat'] (在 category 中)

# ^$ : 匹配空行
multiline_text = "a\n\nb\n\n\nc"
print(len(re.findall(r"^$", multiline_text, re.MULTILINE)))  # 3
```

---

### Part 4: 分组与捕获

#### 4.1 普通捕获组

```python
import re

# 用 () 创建捕获组
date_text = "日期: 2024-01-15"

match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_text)
if match:
    print(match.group())      # 2024-01-15 (完整匹配)
    print(match.group(1))     # 2024 (第一个组)
    print(match.group(2))     # 01 (第二个组)
    print(match.group(3))     # 15 (第三个组)
    print(match.groups())     # ('2024', '01', '15')

# findall 与捕获组
# 无捕获组：返回所有匹配
print(re.findall(r"\d{4}-\d{2}-\d{2}", "2024-01-15, 2024-02-20"))
# ['2024-01-15', '2024-02-20']

# 有捕获组：只返回捕获的内容
print(re.findall(r"(\d{4})-(\d{2})-(\d{2})", "2024-01-15, 2024-02-20"))
# [('2024', '01', '15'), ('2024', '02', '20')]
```

**findall 返回值规则表**：

| 情况 | 模式 | 返回值示例 |
|------|------|-----------|
| 无分组 | `r"\d+"` | `['123', '456']` |
| 普通分组 | `r"(\d+)-(\d+)"` | `[('123', 'a'), ('456', 'b')]` |
| 多层分组 | `r"(\d+)-(\d+)-(\d+)"` | `[('2024', '01', '15')]` |
| 命名分组 | `r"(?P<year>\d+)"` | `[{'year': '2024'}]` |
| 嵌套分组 | `r"(a(b))"` | `[('ab', 'b')]` — 外层+内层 |
| 非捕获组 | `r"(?:\d+)-(\d+)"` | `[('456',)]` — 忽略非捕获组 |

> ⚠️ **常见陷阱**：`findall` 返回的是列表，不是 Match 对象。如果需要完整匹配+分组，用 `re.finditer()`。

#### 4.2 命名分组

```python
import re

# (?P<name>...) 命名分组
log = "2024-01-15 INFO Server started on port 8080"

pattern = r"(?P<date>\d{4}-\d{2}-\d{2})\s+" \
          r"(?P<level>\w+)\s+" \
          r"(?P<message>.+)"

match = re.search(pattern, log)
if match:
    print(match.groupdict())
    # {'date': '2024-01-15', 'level': 'INFO', 'message': 'Server started on port 8080'}

# 使用命名访问
print(match.group("date"))   # 2024-01-15
print(match.group("level"))   # INFO
print(match.group("message")) # Server started on port 8080
```

#### 4.3 反向引用

```python
import re

# \1 \2 引用前面的捕获组
# 匹配重复的单词
text = "the the cat sat on on the mat"
print(re.findall(r"\b(\w+)\s+\1\b", text))  # ['the', 'on']

# 匹配引号内的内容（成对引号）
quoted = "'hello' and \"world\" and 'foo'"
# 单引号内容
single = re.findall(r"'([^']+)'", quoted)
print(single)  # ['hello', 'foo']
# 双引号内容
double = re.findall(r'"([^"]+)"', quoted)
print(double)  # ['world']

# 匹配 HTML 标签
html = "<div>content</div><span>more</span>"
tags = re.findall(r"<(\w+)>.*?</\1>", html)
print(tags)  # ['div', 'span']
```

#### 4.4 非捕获组

```python
import re

# (?:...) 非捕获组：不创建分组
# 用于只分组不捕获
text = "https://example.com http://test.org"

# 只想匹配，不捕获协议
urls = re.findall(r"(?:https?|ftp)://[\w.-]+", text)
print(urls)  # ['https://example.com', 'http://test.org']

# findall 与捕获组 vs 非捕获组
# 捕获组：返回捕获内容
print(re.findall(r"(https?)://([\w.-]+)", "https://a.com http://b.org"))
# [('https', 'a.com'), ('http', 'b.org')]

# 非捕获组：返回完整匹配
print(re.findall(r"(?:https?)://([\w.-]+)", "https://a.com http://b.org"))
# ['a.com', 'b.org']
```

---

### Part 5: 环视断言

#### 5.1 正向前瞻

```python
import re

# (?=...) 正向前瞻：后面跟着某模式
text = "内存16GB，硬盘512GB，价格999美元"

# 找出后面跟着 GB 的数字
print(re.findall(r"\d+(?=GB)", text))  # ['16', '512']

# 找出后面跟着 美元 的数字
print(re.findall(r"\d+(?=美元)", text))  # ['999']

# 实战：密码强度验证（需要包含大写、小写、数字、特殊字符）
password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$"
passwords = ["Passw0rd!", "password", "PASSWORD1", "Short1!"]
for pwd in passwords:
    print(f"{pwd}: {bool(re.fullmatch(password_pattern, pwd))}")
```

#### 5.2 负向前瞻

```python
import re

# (?!...) 负向前瞻：后面不跟着某模式
files = ["app.py", "app.tmp", "test.py", "cache.tmp", "main.py"]

# 排除 .tmp 文件
non_tmp = [f for f in files if re.search(r"\.py$", f) and not re.search(r"\.tmp$", f)]
print(non_tmp)  # ['app.py', 'test.py', 'main.py']

# 更简洁的写法：负向前瞻
print([f for f in files if re.search(r"\.py$", f) and not re.search(r"\.tmp$", f)])
print(re.findall(r"\b\w+\.py\b", "app.py test.tmp main.py"))  # ['app.py', 'main.py']

# 实战：提取不是注释的行
code = """
def func():
    pass  # comment
    return 1
"""
lines = code.strip().split("\n")
code_lines = [line for line in lines if re.search(r"^\s*[^#\s]", line)]
print(code_lines)
```

#### 5.3 正向后顾

```python
import re

# (?<=...) 正向后顾：前面是某模式
text = "价格 $19.99，折扣 $5.00，库存 20"

# 找出 $ 后面的价格数字
prices = re.findall(r"(?<=\$)\d+(?:\.\d{2})?", text)
print(prices)  # ['19.99', '5.00']

# 实战：提取特定标签内的内容
html = """
<div class="price">¥199.00</div>
<div class="name">商品名称</div>
"""
prices = re.findall(r'(?<=<div class="price">)[^<]+', html)
print(prices)  # ['¥199.00']
```

#### 5.4 负向后顾

```python
import re

# (?<!...) 负向后顾：前面不是某模式
text = "user@example.com 和 @invalid 没有@符号"

# 提取 @ 前面不是空白的用户名
users = re.findall(r"(?<!\S)[\w.-]+@[\w.-]+", text)
print(users)  # ['user@example.com']

# 实战：提取数字，但排除百分比后的数字
measurements = "温度 25°C，湿度 60%，压力 101.3kPa"
# 提取温度和压力，不提取百分比
numbers = re.findall(r"\d+(?:\.\d+)?(?![%\d])", measurements)
print(numbers)  # ['25', '101.3']
```

---

### Part 6: re.compile 与性能优化

#### 6.1 编译正则表达式

```python
import re

# 多次使用同一模式时，先编译
pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

dates = ["2024-01-15", "生日: 2024-03-20", "2024-12-25"]
for date in dates:
    match = pattern.search(date)
    if match:
        print(f"找到: {match.group()}")

# 编译后可复用
pattern.findall("2024-01-15 2024-02-20")  # ['2024-01-15', '2024-02-20']
pattern.fullmatch("2024-01-15")  # Match object
```

#### 6.2 标志位

```python
import re

text = "Hello World\nPython Java"

# re.IGNORECASE / re.I: 忽略大小写
print(re.findall(r"python", text, re.I))  # ['Python']

# re.MULTILINE / re.M: ^$ 匹配行首行尾
print(re.findall(r"^\w+", text, re.M))  # ['Hello', 'Python', 'Java']

# re.DOTALL / re.S: . 匹配包括换行
html = "<div>text</div>\n<span>more</span>"
print(re.findall(r"<div>.*?</div>", html, re.S))  # ['<div>text</div>']

# re.VERBOSE / re.X: 忽略空白和注释
pattern = re.compile(r"""
    \d{4}      # 年份
    -          # 分隔符
    \d{2}      # 月份
    -          # 分隔符
    \d{2}      # 日期
""", re.VERBOSE)
print(pattern.search("2024-01-15"))  # Match object

# 组合标志
pattern = re.compile(r"python", re.I | re.M)
```

#### 6.3 性能最佳实践

```python
import re
import time

# ❌ 低效：每次调用都编译
text = "a" * 1000 + "b"
start = time.time()
for _ in range(1000):
    re.search(r"b", text)
print(f"未编译: {time.time() - start:.4f}s")

# ✅ 高效：预编译
pattern = re.compile(r"b")
start = time.time()
for _ in range(1000):
    pattern.search(text)
print(f"已编译: {time.time() - start:.4f}s")

# 避免灾难性回溯
# ❌ 危险模式：可能造成 ReDoS
# r"(a+)+b" 对 "aaaaaaaaaac" 极慢

# ✅ 安全模式
# r"a+b" 效果相同但安全
```

---

## 🚀 快速开始

从仓库根目录进入本课：

```bash
cd stage1-python-intermediate/lessons/L18-regex
```

### 1. 运行示例代码

```bash
# 基础语法
python examples/01_basic_patterns.py

# 分组与捕获
python examples/02_groups_capture.py

# 环视断言
python examples/03_lookaround.py

# verbose 模式
python examples/04_verbose_pattern.py
```

### 2. 完成练习题

```bash
python exercises/01_validation.py
python exercises/02_extraction.py
```

---

## 📝 练习题

### 练习 1: 验证函数

使用正则表达式实现以下验证函数：

```python
def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    ...

def validate_phone(phone: str) -> bool:
    """验证中国手机号"""
    ...

def validate_url(url: str) -> bool:
    """验证 URL 格式"""
    ...
```

### 练习 2: 提取函数

从文本中提取结构化数据：

```python
def extract_dates(text: str) -> list[str]:
    """提取所有日期 (YYYY-MM-DD 格式)"""
    ...

def extract_prices(text: str) -> list[tuple[str, float]]:
    """提取价格 (货币符号 + 金额)"""
    ...
```

## 🔗 下一步



恭喜完成 Stage 1 Python 进阶！🎉

---

**课程说明**: 本课程从 archived 目录迁移而来，补充了新课程体系缺失的正则表达式内容。
