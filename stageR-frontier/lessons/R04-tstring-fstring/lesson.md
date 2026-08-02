# R04: t-string 与格式化新纪元

> **课程编号**: R04
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: R03, L01
> **版本**: v5.0
> **最后更新**: 2026-07-22
> **核心版本**: Python 3.14 (实验性)

---

## 📌 学习目标

完成本课程后，你将能够：

1. **掌握 t-string 模板字符串**：安全的模板插值语法
2. **理解 t-string 与 f-string 的区别**：使用场景和优势
3. **实现国际化支持**：t-string 的 i18n 集成
4. **迁移现有代码**：从 f-string 到 t-string 的渐进式迁移

---

## 📖 课程导读

### 什么是 t-string？

t-string（模板字符串）是 Python 3.14 引入的新语法：

```python
# f-string：表达式插值
name = "Alice"
print(f"Hello, {name}!")  # Hello, Alice!

# t-string：模板插值（仅允许变量名）
print(t"Hello, {name}!")  # Hello, {name}! - 不执行插值
print(t"Hello, {name}")  # Hello, Alice - 允许变量名
```

### 为什么需要 t-string？

| 场景 | f-string | t-string |
|------|----------|----------|
| 用户输入显示 | ⚠️ 可能导致注入 | ✅ 安全 |
| 国际化 | ⚠️ 需要转义 | ✅ 原生支持 |
| SQL 查询 | ⚠️ 危险 | ✅ 安全模板 |
| 日志消息 | ⚠️ 可能格式化 | ✅ 原始输出 |

---

## Part 1: t-string 基础

### 1.1 语法详解

```python
# t-string 基本语法
name = "Alice"
age = 30

# 模板字符串：不执行插值
template = t"Hello, {name}"
print(template)  # Hello, {name}

# 插值语法：使用 {}
result = t"User: {name}, Age: {age}"
print(result)  # User: Alice, Age: 30

# 与 f-string 对比
print(f"f-string: {1 + 2}")   # f-string: 3
print(t"t-string: {1 + 2}")   # ❌ 错误：t-string 只允许简单名称

# 允许的操作
x = 10
y = 20
print(t"Sum: {x + y}")  # ✅ 允许：简单表达式
print(t"Product: {x * y}")  # ✅ 允许：算术表达式
```

### 1.2 限制与规则

```python
# t-string 的限制

# ❌ 不允许：函数调用
name = "Alice"
print(t"Hello, {name.upper()}")  # ❌ 错误

# ❌ 不允许：方法调用
print(t"Hello, {name.strip()}")  # ❌ 错误

# ❌ 不允许：条件表达式
print(t"{'yes' if age > 18 else 'no'}")  # ❌ 错误

# ✅ 允许：属性访问
class User:
    def __init__(self, name: str):
        self.name = name

user = User("Alice")
print(t"Name: {user.name}")  # ✅ 允许

# ✅ 允许：索引访问
items = ["a", "b", "c"]
print(t"First: {items[0]}")  # ✅ 允许
```

### 1.3 嵌套与转义

```python
# 嵌套花括号
template = t"Use {{name}} to insert name"
print(template)  # Use {name} to insert name

# 多层嵌套
outer = "x"
inner = "y"
result = t"{{{{outer}}}}"  # {{outer}} - 一层解包
print(result)  # {outer}

# 转义序列
print(t"Newline: \n Tab: \t")  # 按字面输出 \n 和 \t

# 原始字符串 + 模板
path = r"C:\Users\Alice"
template = t"{path}\data"  # C:\Users\Alice\data
```

---

## Part 2: 国际化与模板

### 2.1 i18n 集成

```python
# t-string 的国际化支持

from typing import gettext as _

# 翻译函数
def ngettext(singular: str, plural: str, n: int) -> str:
    return singular if n == 1 else plural

# 使用 t-string 进行翻译
name = "Alice"
count = 3

# ❌ f-string 在翻译中的问题
msg_f = f"{name} has {count} items"  # 需要手动翻译

# ✅ t-string 保持翻译键
msg_t = t"{name} has {count} items"  # 可以作为翻译键
# 翻译文件: "{name} has {count} items" -> "{name} 有 {count} 个项目"
```

### 2.2 模板系统

```python
# 构建模板系统

from dataclasses import dataclass
from typing import Any

@dataclass
class Template:
    """模板引擎"""
    pattern: str

    def render(self, **kwargs: Any) -> str:
        """渲染模板"""
        result = self.pattern
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result

# 使用示例
greeting = Template("Hello, {name}! Welcome to {place}.")
print(greeting.render(name="Alice", place="Python"))
# Hello, Alice! Welcome to Python.

# 模板组合
base_template = Template("Dear {name},")
body_template = Template("Your order #{order_id} has been {status}.")
signature = Template("Best regards,\n{sender}")

full = Template(base_template.pattern + "\n" + body_template.pattern + "\n" + signature.pattern)
print(full.render(
    name="Customer",
    order_id="12345",
    status="shipped",
    sender="Support Team"
))
```

### 2.3 SQL 模板（安全）

```python
# t-string 的 SQL 安全模板

class SQLTemplate:
    """安全的 SQL 模板"""

    def __init__(self, template: str):
        self._template = template

    def build(self, **params) -> tuple[str, dict]:
        """
        构建 SQL 和参数
        返回 (sql, params) 供 execute() 使用
        """
        sql = self._template
        for key, value in params.items():
            placeholder = f"{{{key}}}"
            if placeholder in sql:
                sql = sql.replace(placeholder, f"%({key})s")
        return sql, params

# 使用示例
query = SQLTemplate(
    t"SELECT * FROM users WHERE id = {user_id} AND status = {status}"
)

sql, params = query.build(user_id=123, status="active")
print(sql)  # SELECT * FROM users WHERE id = %(user_id)s AND status = %(status)s
print(params)  # {'user_id': 123, 'status': 'active'}

# 配合数据库使用
# cursor.execute(sql, params)  # 安全注入
```

---

## Part 3: 迁移策略

### 3.1 f-string 到 t-string

```python
# 迁移检查清单

"""
从 f-string 迁移到 t-string 时，检查以下模式：

1. 表达式插值 → 变量名插值
2. 方法调用 → 属性访问或预计算
3. 条件表达式 → 预计算变量
4. 嵌套 f-string → 模板组合
"""

# 示例迁移

# 迁移前
def format_user_f(user):
    return f"Name: {user['name'].title()}, Age: {user.get('age', 0)}"

# 迁移后
def format_user_t(user):
    name = user["name"].title()  # 预计算
    age = user.get("age", 0)
    return t"Name: {name}, Age: {age}"
```

### 3.2 自动迁移工具

```python
# 自动迁移工具（简化版）

import re

def migrate_fstring(code: str) -> str:
    """将 f-string 迁移到 t-string"""

    # 匹配 f-string
    pattern = r'f"(.*?)"'

    def replace_fstring(match):
        content = match.group(1)
        # 检测是否包含不允许的操作
        if any(op in content for op in ['.', '(', '[', '?', '+', '-', '*', '/']):
            # 需要更复杂的迁移
            return match.group(0)  # 保持不变

        # 简单变量名，直接转换
        return f't"{content}"'

    return re.sub(pattern, replace_fstring, code)

# 示例
code = '''
name = "Alice"
print(f"Hello, {name}")
print(f"User: {user['name']}")
'''

migrated = migrate_fstring(code)
print(migrated)
```

### 3.3 回退兼容

```python
# 兼容旧版本 Python

import sys

def is_tstring_supported() -> bool:
    """检查 t-string 是否支持"""
    return sys.version_info >= (3, 14)

def template(text: str, **kwargs) -> str:
    """兼容的模板函数"""
    if is_tstring_supported():
        # Python 3.14+: 使用内置 t-string
        # 注意：需要运行时编译
        return eval(f't"{text}"', {}, kwargs)
    else:
        # 回退实现
        for key, value in kwargs.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text

# 使用示例
name = "Alice"
print(template("Hello, {name}", name=name))
```

---

## Part 4: 实战案例

### 4.1 日志消息模板

```python
# 安全日志模板

from datetime import datetime
from dataclasses import dataclass

@dataclass
class LogTemplate:
    """日志模板"""

    timestamp: datetime
    level: str
    message: str
    context: dict

    def format(self) -> str:
        """格式化日志"""
        # t-string 保证消息安全性
        base = t"[{self.timestamp}] [{self.level}] {self.message}"

        if self.context:
            ctx_parts = [f"{k}={v}" for k, v in self.context.items()]
            return f"{base} | {' '.join(ctx_parts)}"
        return base

# 使用示例
log = LogTemplate(
    timestamp=datetime.now(),
    level="INFO",
    message="User logged in",
    context={"user_id": 123, "ip": "192.168.1.1"}
)
print(log.format())
```

### 4.2 API 响应模板

```python
# API 响应模板

from typing import Any, Optional
from dataclasses import dataclass, field

@dataclass
class APIResponse:
    """API 响应模板"""

    status: str
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    request_id: Optional[str] = None

    def to_json(self) -> dict:
        """转换为 JSON"""
        parts = [
            t'status: {self.status}',
            t'message: {self.message}',
        ]

        if self.data is not None:
            parts.append(t'data: {self.data}')

        if self.error:
            parts.append(t'error: {self.error}')

        if self.request_id:
            parts.append(t'request_id: {self.request_id}')

        # 简化版，实际使用 dict
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "request_id": self.request_id,
        }

# 使用示例
response = APIResponse(
    status="success",
    message="User created",
    data={"user_id": 123},
    request_id="req-abc-123"
)
print(response.to_json())
```

---

## 💡 常见陷阱

### 陷阱 1: 混淆 t-string 和 f-string

```python
# ❌ 错误：假设 t-string 和 f-string 行为相同
name = "Alice"
result = t"Hello, {name.upper()}"  # ❌ 错误

# ✅ 正确：理解 t-string 的限制
result = t"Hello, {name}"  # ✅ 正确
upper_name = name.upper()
result = t"Hello, {upper_name}"  # ✅ 正确
```

### 陷阱 2: 在 t-string 中使用敏感字符

```python
# ❌ 错误：t-string 不是完全安全的
user_input = "Alice"  # 用户输入
sql = t"SELECT * FROM users WHERE name = '{user_input}'"
# ⚠️ 仍然存在注入风险，如果 {user_input} 包含引号

# ✅ 正确：参数化查询
from sql_template import SQLTemplate
query = SQLTemplate(t"SELECT * FROM users WHERE name = {name}")
sql, params = query.build(name=user_input)  # 安全
```

---

## 📚 延伸阅读

- [PEP 750 - t-strings](https://peps.python.org/pep-0750/)
- [String Templates in Python](https://peps.python.org/pep-0498/) (f-string 的前身)

---

## ✅ 自检清单

- [ ] 解释 t-string 和 f-string 的区别
- [ ] 识别 t-string 的使用场景
- [ ] 将 f-string 迁移到 t-string
- [ ] 实现安全的 SQL 模板
- [ ] 编写回退兼容代码

---

## 🔗 下一步

- [R05: Python 路线图与未来展望](../R05-python-roadmap/lesson.md)
- [R06: WASI 边缘部署](../R06-wasi-edge-deploy/lesson.md)

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0
