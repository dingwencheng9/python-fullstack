# Stage 0 知识点越界全面审查报告

## 执行摘要

| 指标 | 数值 |
|------|------|
| 审查文件总数 | 124 |
| 发现违规数 | 151 |

### 按违规类型分布

- **term**: 151 个

### 按严重程度分布

- **CRITICAL**: 0 个
- **HIGH**: 0 个
- **MEDIUM**: 151 个

### 按课程分布

- **L01**: 99 个违规
- **L02**: 18 个违规
- **L03**: 24 个违规
- **L04**: 2 个违规
- **L06**: 8 个违规

## 违规详情

### L01

#### `lessons/L01-python-core/lesson.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 19 | term | MEDIUM | `2. **数据建模**：理解变量引用模型（标签 vs 盒子），区分 4 种基本数据类型` | 课程 L01 中出现禁止术语 '类' |
| 20 | term | MEDIUM | `3. **类型安全**：理解 None 的含义，为变量添加类型注解` | 课程 L01 中出现禁止术语 '类' |
| 61 | term | MEDIUM | `> 🔑 **本课的核心转变**：传统课程把"Hello World"和"变量类型"分开讲，导致你前两` | 课程 L01 中出现禁止术语 '类' |
| 74 | term | MEDIUM | `>>> type(42)         # 查看对象类型：<class 'int'>` | 课程 L01 中出现禁止术语 '类' |
| 74 | term | MEDIUM | `>>> type(42)         # 查看对象类型：<class 'int'>` | 课程 L01 中出现禁止术语 'class' |
| 74 | term | MEDIUM | `>>> type(42)         # 查看对象类型：<class 'int'>` | 课程 L01 中出现禁止术语 '对象' |
| 75 | term | MEDIUM | `>>> type("hello")    # 查看对象类型：<class 'str'>` | 课程 L01 中出现禁止术语 '类' |
| 75 | term | MEDIUM | `>>> type("hello")    # 查看对象类型：<class 'str'>` | 课程 L01 中出现禁止术语 'class' |
| 75 | term | MEDIUM | `>>> type("hello")    # 查看对象类型：<class 'str'>` | 课程 L01 中出现禁止术语 '对象' |
| 76 | term | MEDIUM | `>>> help(print)      # 查看函数签名和参数说明` | 课程 L01 中出现禁止术语 '函数' |
| 76 | term | MEDIUM | `>>> help(print)      # 查看函数签名和参数说明` | 课程 L01 中出现禁止术语 '参数' |
| 85 | term | MEDIUM | `<class 'str'>   # ← 原来 input() 返回的是字符串！` | 课程 L01 中出现禁止术语 'class' |
| 198 | term | MEDIUM | `- ✅ 现代类型系统（PEP 695，由 Python 3.12 引入）` | 课程 L01 中出现禁止术语 '类' |
| 251 | term | MEDIUM | `**print() 函数的特点**：` | 课程 L01 中出现禁止术语 '函数' |
| 252 | term | MEDIUM | `- 内置函数（无需导入）` | 课程 L01 中出现禁止术语 '函数' |
| 254 | term | MEDIUM | `- 可接受多个参数` | 课程 L01 中出现禁止术语 '参数' |
| 317 | term | MEDIUM | `\| **探索 API** \| 了解陌生函数 \| `help(len)` → 看函数签名 \|` | 课程 L01 中出现禁止术语 '函数' |
| 326 | term | MEDIUM | `>>> type(42)     # 42 是什么类型？` | 课程 L01 中出现禁止术语 '类' |
| 327 | term | MEDIUM | `<class 'int'>` | 课程 L01 中出现禁止术语 'class' |
| 328 | term | MEDIUM | `>>> type("hi")   # "hi" 是什么类型？` | 课程 L01 中出现禁止术语 '类' |
| 329 | term | MEDIUM | `<class 'str'>` | 课程 L01 中出现禁止术语 'class' |
| 354 | term | MEDIUM | `\| `Tab` \| 自动补全变量/函数名 \| ⭐⭐⭐ 必须 \|` | 课程 L01 中出现禁止术语 '函数' |
| 389 | term | MEDIUM | `**③ 内嵌彩色帮助** — 输入函数名即可查看签名与说明：` | 课程 L01 中出现禁止术语 '函数' |
| 394 | term | MEDIUM | `Prints the values to a stream or to sys.stdout by ` | 课程 L01 中出现禁止术语 'def' |
| 447 | term | MEDIUM | `print(type(name))  # <class 'str'>` | 课程 L01 中出现禁止术语 'class' |
| 448 | term | MEDIUM | `print(type(age))   # <class 'str'> — 注意：这是字符串 "25"` | 课程 L01 中出现禁止术语 'class' |
| 467 | term | MEDIUM | `age: int = int(input("年龄: "))  # 一行完成：获取 → 转类型` | 课程 L01 中出现禁止术语 '类' |
| 473 | term | MEDIUM | `print(type(age))  # <class 'str'>` | 课程 L01 中出现禁止术语 'class' |
| 477 | term | MEDIUM | `print(type(age_int))  # <class 'int'>` | 课程 L01 中出现禁止术语 'class' |
| 517 | term | MEDIUM | `Python 中，变量是**对象的引用（标签）**，不是容器：` | 课程 L01 中出现禁止术语 '对象' |
| 521 | term | MEDIUM | `subgraph memory["内存（对象存储区）"]` | 课程 L01 中出现禁止术语 '对象' |
| 522 | term | MEDIUM | `A["100<br/>(整数对象)"]` | 课程 L01 中出现禁止术语 '对象' |
| 523 | term | MEDIUM | `B["'hello'<br/>(字符串对象)"]` | 课程 L01 中出现禁止术语 '对象' |
| 524 | term | MEDIUM | `C["[1,2,3]<br/>(列表对象)"]` | 课程 L01 中出现禁止术语 '对象' |
| 524 | term | MEDIUM | `C["[1,2,3]<br/>(列表对象)"]` | 课程 L01 中出现禁止术语 '列表' |
| 539 | term | MEDIUM | `x = 100          # ① 创建整数对象 100` | 课程 L01 中出现禁止术语 '对象' |
| 540 | term | MEDIUM | `y = x            # ② y 成为同一个对象的另一个标签` | 课程 L01 中出现禁止术语 '对象' |
| 541 | term | MEDIUM | `x = 200          # ③ x 重新指向新对象 200（y 不受影响）` | 课程 L01 中出现禁止术语 '对象' |
| 552 | term | MEDIUM | `subgraph step2["y = x（x 和 y 指向同一对象）"]` | 课程 L01 中出现禁止术语 '对象' |
| 569 | term | MEDIUM | `> 当你修改 x 的值时，y 不会受影响——因为它们是两个独立的标签，各自指向不同的对象。` | 课程 L01 中出现禁止术语 '对象' |
| 575 | term | MEDIUM | `Python 有 4 种基本数据类型：` | 课程 L01 中出现禁止术语 '类' |
| 582 | term | MEDIUM | `> 📖 **Python 3.13 不可变性说明**：整数、浮点数、字符串、布尔值都是不可变类型，` | 课程 L01 中出现禁止术语 '类' |
| 583 | term | MEDIUM | `> 修改操作会返回新对象，而非就地修改。` | 课程 L01 中出现禁止术语 '对象' |
| 672 | term | MEDIUM | `> 📖 **cmath 模块**：提供 `sqrt`、`sin`、`cos`、`log` 等数学函数` | 课程 L01 中出现禁止术语 '函数' |
| 705 | term | MEDIUM | `**常用方法**：` | 课程 L01 中出现禁止术语 '方法' |
| 714 | term | MEDIUM | `text.split()      # 分割成列表` | 课程 L01 中出现禁止术语 '列表' |
| 717 | term | MEDIUM | `> 📖 **字符串方法速查表**（更多方法见官方文档）：` | 课程 L01 中出现禁止术语 '方法' |
| 719 | term | MEDIUM | `> \| 方法 \| 示例 \| 说明 \|` | 课程 L01 中出现禁止术语 '方法' |
| 721 | term | MEDIUM | `> \| `.split()` \| `"a,b,c".split(",")` \| 按分隔符分割，` | 课程 L01 中出现禁止术语 '列表' |
| 722 | term | MEDIUM | `> \| `.join()` \| `",".join(["a","b","c"])` \| 用分隔` | 课程 L01 中出现禁止术语 '列表' |
| 742 | term | MEDIUM | `b2 = bytes([72, 101, 108, 108, 111])  # 从整数列表` | 课程 L01 中出现禁止术语 '列表' |
| 755 | term | MEDIUM | `print(type(s), type(b))  # <class 'str'> <class 'b` | 课程 L01 中出现禁止术语 'class' |
| 756 | term | MEDIUM | `print(s == b)             # False（类型不同，永不等）` | 课程 L01 中出现禁止术语 '类' |
| 838 | term | MEDIUM | `- 函数默认返回值` | 课程 L01 中出现禁止术语 '函数' |
| 840 | term | MEDIUM | `- 表示"可选参数"` | 课程 L01 中出现禁止术语 '参数' |
| 846 | term | MEDIUM | `Python 可以为变量和函数添加"类型注解"作为文档：` | 课程 L01 中出现禁止术语 '函数' |
| 846 | term | MEDIUM | `Python 可以为变量和函数添加"类型注解"作为文档：` | 课程 L01 中出现禁止术语 '类' |
| 859 | term | MEDIUM | `> 📖 **Python 3.13 提示**：类型注解只是"文档"，运行时不强制检查！` | 课程 L01 中出现禁止术语 '类' |
| 861 | term | MEDIUM | `> x: int = "hello"  # 不会报错！类型注解不是强制约束` | 课程 L01 中出现禁止术语 '类' |
| 864 | term | MEDIUM | `> 💡 **进阶学习**：完整的类型系统（Union、Protocol、PEP 695 泛型、myp` | 课程 L01 中出现禁止术语 '类' |
| 868 | term | MEDIUM | `> 🔑 **本节目标**：掌握 Python 3.6+ 的推荐字符串格式化方法。f-string 不` | 课程 L01 中出现禁止术语 '方法' |
| 874 | term | MEDIUM | `Python 有四种字符串格式化方法：` | 课程 L01 中出现禁止术语 '方法' |
| 978 | term | MEDIUM | ``breakpoint()` 是 Python 3.7+ 引入的内置调试函数，会自动启动调试器：` | 课程 L01 中出现禁止术语 '函数' |
| 989 | term | MEDIUM | `> `def` 函数定义将在 L04 中学习。` | 课程 L01 中出现禁止术语 '函数' |
| 989 | term | MEDIUM | `> `def` 函数定义将在 L04 中学习。` | 课程 L01 中出现禁止术语 'def' |
| 1012 | term | MEDIUM | `\| `step` \| `s` \| 进入函数内部 \| `s` \|` | 课程 L01 中出现禁止术语 '函数' |
| 1037 | term | MEDIUM | `try:` | 课程 L01 中出现禁止术语 'try' |
| 1039 | term | MEDIUM | `except ZeroDivisionError:` | 课程 L01 中出现禁止术语 'except' |
| 1045 | term | MEDIUM | `print(f"最后异常位置: {tb.tb_lineno}")` | 课程 L01 中出现禁止术语 '异常' |
| 1048 | term | MEDIUM | `> ⚠️ **预习提示**：`try/except` 异常处理语法将在 L08 中详细学习。` | 课程 L01 中出现禁止术语 '异常' |
| 1048 | term | MEDIUM | `> ⚠️ **预习提示**：`try/except` 异常处理语法将在 L08 中详细学习。` | 课程 L01 中出现禁止术语 'try' |
| 1048 | term | MEDIUM | `> ⚠️ **预习提示**：`try/except` 异常处理语法将在 L08 中详细学习。` | 课程 L01 中出现禁止术语 'except' |
| 1053 | term | MEDIUM | `> 🔑 **本节关键**：类型转换不是"变魔术"，而是显式告诉 Python"按这种规则重新解释这个` | 课程 L01 中出现禁止术语 '类' |
| 1073 | term | MEDIUM | `**类型转换三原则：**` | 课程 L01 中出现禁止术语 '类' |
| 1075 | term | MEDIUM | `\| 源类型 \| 目标类型 \| 规则 \| 危险场景 \|` | 课程 L01 中出现禁止术语 '类' |
| 1141 | term | MEDIUM | `> 📖 **深入学习**：可变与不可变类型的完整对比（包括 list、dict、set）见 L03《` | 课程 L01 中出现禁止术语 '类' |
| 1145 | term | MEDIUM | `3. **哈希性**：可以作为字典的键（见 L03）` | 课程 L01 中出现禁止术语 '字典' |
| 1155 | term | MEDIUM | `3. **print()**：内置输出函数` | 课程 L01 中出现禁止术语 '函数' |
| 1160 | term | MEDIUM | `1. **引用模型**：变量是对象的标签，不是盒子` | 课程 L01 中出现禁止术语 '对象' |
| 1161 | term | MEDIUM | `2. **5 种基本类型**：int、float、str、bool、None` | 课程 L01 中出现禁止术语 '类' |
| 1163 | term | MEDIUM | `4. **类型注解**：提高可读性（不强制检查）` | 课程 L01 中出现禁止术语 '类' |
| 1184 | term | MEDIUM | `- 🔧 **配置管理**：使用类型注解定义配置结构` | 课程 L01 中出现禁止术语 '类' |
| 1185 | term | MEDIUM | `- 🧮 **计算器**：类型转换 + f-string 格式化输出` | 课程 L01 中出现禁止术语 '类' |
| 1189 | term | MEDIUM | `\| 类型 \| 可变 \| 可哈希 \| 示例 \| 典型用途 \|` | 课程 L01 中出现禁止术语 '类' |
| 1225 | term | MEDIUM | `> 📖 **L02 将学到**：比较两个对象是否"同一个东西"用 `is`，是否"值相等"用 `==` | 课程 L01 中出现禁止术语 '对象' |
| 1313 | term | MEDIUM | `- [Python 内置类型](https://docs.python.org/zh-cn/3/li` | 课程 L01 中出现禁止术语 '类' |
| 1333 | term | MEDIUM | `- [ ] 理解变量是对象的引用（非盒子模型）` | 课程 L01 中出现禁止术语 '对象' |
| 1334 | term | MEDIUM | `- [ ] 区分 4 种基本数据类型（int/float/str/bool）` | 课程 L01 中出现禁止术语 '类' |
| 1336 | term | MEDIUM | `- [ ] 为变量和函数添加类型注解` | 课程 L01 中出现禁止术语 '函数' |
| 1336 | term | MEDIUM | `- [ ] 为变量和函数添加类型注解` | 课程 L01 中出现禁止术语 '类' |
| 1338 | term | MEDIUM | `- [ ] 进行类型转换（int/float/str 互转）` | 课程 L01 中出现禁止术语 '类' |
| 1352 | term | MEDIUM | `- while 和 for 循环` | 课程 L01 中出现禁止术语 '循环' |

#### `lessons/L01-python-core/README.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 5 | term | MEDIUM | `> **定位**: Python 全栈课程入口课，建立运行程序、变量、类型、输入输出和 f-stri` | 课程 L01 中出现禁止术语 '类' |
| 20 | term | MEDIUM | `- 理解变量是“名字绑定到对象”，而不是“盒子里装值”` | 课程 L01 中出现禁止术语 '对象' |
| 21 | term | MEDIUM | `- 区分 `int`、`float`、`str`、`bool`、`None` 等基础类型` | 课程 L01 中出现禁止术语 '类' |
| 22 | term | MEDIUM | `- 使用 `print()`、`input()`、类型转换和 f-string 完成基础交互程序` | 课程 L01 中出现禁止术语 '类' |
| 23 | term | MEDIUM | `- 使用 `is None` 判断空值，并理解类型注解的入门作用` | 课程 L01 中出现禁止术语 '类' |
| 71 | term | MEDIUM | `Hello World → REPL → 输入输出 → 变量引用 → 基础类型 → 类型注解 → f` | 课程 L01 中出现禁止术语 '类' |
| 90 | term | MEDIUM | `- [ ] 阅读 `lesson.md`，理解变量、类型、输入输出和 f-string` | 课程 L01 中出现禁止术语 '类' |

### L02

#### `lessons/L02-operators-control/lesson.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 727 | term | MEDIUM | `> 💡 **L04 将学到**：函数定义（`def`）也需要 `pass` 作为空函数体的占位符。` | 课程 L02 中出现禁止术语 '函数定义' |
| 727 | term | MEDIUM | `> 💡 **L04 将学到**：函数定义（`def`）也需要 `pass` 作为空函数体的占位符。` | 课程 L02 中出现禁止术语 'def' |
| 788 | term | MEDIUM | `> 💡 **L04 将学到**：可以将上述逻辑封装为函数 `def is_prime(n):`，提高` | 课程 L02 中出现禁止术语 'def' |
| 910 | term | MEDIUM | `传统的 if-elif-else 链在处理多个固定值时不够简洁。match-case 提供了更清晰的` | 课程 L02 中出现禁止术语 '类' |
| 1083 | term | MEDIUM | `> 📖 **L03 将学到**：`enumerate()` 和 `zip()` 常与 list（列表` | 课程 L02 中出现禁止术语 '列表' |
| 1083 | term | MEDIUM | `> 📖 **L03 将学到**：`enumerate()` 和 `zip()` 常与 list（列表` | 课程 L02 中出现禁止术语 '字典' |
| 1102 | term | MEDIUM | `> 💡 **L03 实践**：在 L03 学习列表和字典后，再结合 enumerate/zip 进行` | 课程 L02 中出现禁止术语 '列表' |
| 1102 | term | MEDIUM | `> 💡 **L03 实践**：在 L03 学习列表和字典后，再结合 enumerate/zip 进行` | 课程 L02 中出现禁止术语 '字典' |
| 1143 | term | MEDIUM | `**问题**：你能想到 3 个实际场景，在这些场景中 for-else 比传统方法更优雅吗？` | 课程 L02 中出现禁止术语 '方法' |
| 1227 | term | MEDIUM | `\| 类别 \| 运算符 \| 说明 \| 示例 \|` | 课程 L02 中出现禁止术语 '类' |
| 1272 | term | MEDIUM | `- 🔄 **循环遍历**：列表处理、数据聚合、计数器` | 课程 L02 中出现禁止术语 '列表' |
| 1544 | term | MEDIUM | `- 列表（list）：动态数组` | 课程 L02 中出现禁止术语 '列表' |
| 1545 | term | MEDIUM | `- 元组（tuple）：不可变序列` | 课程 L02 中出现禁止术语 '元组' |
| 1546 | term | MEDIUM | `- 字典（dict）：键值对映射` | 课程 L02 中出现禁止术语 '字典' |
| 1547 | term | MEDIUM | `- 集合（set）：无序不重复集合` | 课程 L02 中出现禁止术语 '集合' |

#### `lessons/L02-operators-control/README.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 5 | term | MEDIUM | `> **定位**: 在 L01 的变量与类型基础上，掌握表达式计算、条件分支、循环控制和 Pytho` | 课程 L02 中出现禁止术语 '类' |
| 11 | term | MEDIUM | `- 掌握 L01 Python 核心语法（变量、类型、REPL、f-string）` | 课程 L02 中出现禁止术语 '类' |
| 64 | term | MEDIUM | `2. 运行 examples/*.py，观察每类语法的输出` | 课程 L02 中出现禁止术语 '类' |

### L03

#### `lessons/L03-data-structures/lesson.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 24 | term | MEDIUM | `7. **collections 扩展**：`defaultdict`、`Counter`、`deq` | 课程 L03 中出现禁止术语 'def' |
| 298 | term | MEDIUM | `print(user.get("email"))       # None（不抛异常）` | 课程 L03 中出现禁止术语 '异常' |
| 349 | term | MEDIUM | `email = user.setdefault("email", "default@example.` | 课程 L03 中出现禁止术语 'def' |
| 469 | term | MEDIUM | `普通字典访问不存在的键会报错，`defaultdict` 可以为不存在的键提供默认值：` | 课程 L03 中出现禁止术语 'def' |
| 472 | term | MEDIUM | `from collections import defaultdict` | 课程 L03 中出现禁止术语 'def' |
| 476 | term | MEDIUM | `word_counts = defaultdict(int)` | 课程 L03 中出现禁止术语 'def' |
| 495 | term | MEDIUM | `counts = defaultdict(int)` | 课程 L03 中出现禁止术语 'def' |
| 504 | term | MEDIUM | `people = defaultdict(list)` | 课程 L03 中出现禁止术语 'def' |
| 510 | term | MEDIUM | `from collections import defaultdict` | 课程 L03 中出现禁止术语 'def' |
| 513 | term | MEDIUM | `grouped = defaultdict(list)` | 课程 L03 中出现禁止术语 'def' |
| 516 | term | MEDIUM | `config = defaultdict(dict)` | 课程 L03 中出现禁止术语 'def' |
| 519 | term | MEDIUM | `scores = defaultdict(int)` | 课程 L03 中出现禁止术语 'def' |
| 524 | term | MEDIUM | ``Counter` 是专门用于计数的工具，比 `defaultdict(int)` 更强大：` | 课程 L03 中出现禁止术语 'def' |
| 599 | term | MEDIUM | `def sliding_average(data: List[float], window: int` | 课程 L03 中出现禁止术语 'def' |
| 608 | term | MEDIUM | `def bfs(graph, start: str) -> List[str]:` | 课程 L03 中出现禁止术语 'def' |
| 623 | term | MEDIUM | `> - 需要**默认值** → `defaultdict`` | 课程 L03 中出现禁止术语 'def' |
| 652 | term | MEDIUM | `> 💡 **L08 将学到**：异常处理（`try`/`except`）是另一种处理越界访问的方式。` | 课程 L03 中出现禁止术语 '异常' |
| 652 | term | MEDIUM | `> 💡 **L08 将学到**：异常处理（`try`/`except`）是另一种处理越界访问的方式。` | 课程 L03 中出现禁止术语 'try' |
| 652 | term | MEDIUM | `> 💡 **L08 将学到**：异常处理（`try`/`except`）是另一种处理越界访问的方式。` | 课程 L03 中出现禁止术语 'except' |
| 703 | term | MEDIUM | `> 📖 **提示**：字典的键访问错误（`KeyError`）与列表的索引越界（`IndexErro` | 课程 L03 中出现禁止术语 '异常' |
| 772 | term | MEDIUM | `> 💡 **L04 将学到**：`def` 函数定义，以及如何正确使用可变默认参数。` | 课程 L03 中出现禁止术语 '函数定义' |
| 772 | term | MEDIUM | `> 💡 **L04 将学到**：`def` 函数定义，以及如何正确使用可变默认参数。` | 课程 L03 中出现禁止术语 'def' |
| 812 | term | MEDIUM | `word_count.setdefault(word, 0)` | 课程 L03 中出现禁止术语 'def' |
| 1028 | term | MEDIUM | `value = dict_example.get("key", "default")` | 课程 L03 中出现禁止术语 'def' |

### L04

#### `lessons/L04-functions-modules/lesson.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 1135 | term | MEDIUM | `from module import Class` | 课程 L04 中出现禁止术语 'class' |
| 1143 | term | MEDIUM | `from module import func1, func2, Class1` | 课程 L04 中出现禁止术语 'class' |

### L06

#### `lessons/L06-exceptions/lesson.md`

| 行号 | 类型 | 严重 | 代码片段 | 说明 |
|------|------|------|----------|------|
| 393 | term | MEDIUM | `class InvalidAgeError(Exception):` | 课程 L06 中出现禁止术语 'class' |
| 422 | term | MEDIUM | `class ValidationError(Exception):` | 课程 L06 中出现禁止术语 'class' |
| 426 | term | MEDIUM | `class InvalidAgeError(ValidationError):` | 课程 L06 中出现禁止术语 'class' |
| 430 | term | MEDIUM | `class InvalidEmailError(ValidationError):` | 课程 L06 中出现禁止术语 'class' |
| 438 | term | MEDIUM | `class InvalidAgeError(ValueError):` | 课程 L06 中出现禁止术语 'class' |
| 446 | term | MEDIUM | `class InvalidEmailError(ValueError):` | 课程 L06 中出现禁止术语 'class' |
| 735 | term | MEDIUM | `class HTTPException(Exception):` | 课程 L06 中出现禁止术语 'class' |
| 818 | term | MEDIUM | `- **数据建模**：使用 @dataclass 定义学员类` | 课程 L06 中出现禁止术语 'class' |
