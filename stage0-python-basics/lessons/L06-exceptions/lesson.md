# L06: 异常处理（Exceptions）

> **课程编号**: L06
> **所属阶段**: Stage 0 - Python 编程基础
> **预计时长**: 3 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: L05 调试工具
> **版本**: v2.3
> **最后更新**: 2026-08-05

---

## 🎯 学习目标

完成本课程后，你将能够：

1. **异常理解**：理解 Python 异常的概念和类型层次
2. **try-except 捕获**：使用 try-except 语句捕获和处理异常
3. **异常传播**：理解异常的传播机制和 raise 语句
4. **自定义异常**：创建和应用自定义异常类
5. **异常链**：使用异常链传递上下文信息

---

## 📖 课程导读

异常处理是编写健壮程序的关键。本课程将帮助你：

- 理解 Python 异常的工作机制
- 掌握异常捕获和处理的最佳实践
- 学习如何创建自定义异常
- 了解异常链和 traceback 的使用

---

### 异常传播流程（可视化）

```mermaid
flowchart TD
    A["触发异常"] --> B{"当前函数有<br/>try-except?"}
    B -->|"是"| C{"except 匹配?"}
    C -->|"是"| D["处理异常"]
    C -->|"否"| E["异常传播到<br/>调用者"]
    B -->|"否"| E
    
    D --> F["继续执行"]
    E --> G["调用者有<br/>try-except?"}
    G -->|"是"| H{"匹配?"}
    G -->|"否"| I["继续传播..."]
    H -->|"是"| J["处理异常"]
    H -->|"否"| I
    
    I --> K["传播到<br/>顶层"]
    K --> L["程序终止<br/>打印堆栈"]
    
    style A fill:#ffebee,stroke:#c62828
    style L fill:#ffebee,stroke:#c62828
    style F fill:#e8f5e9,stroke:#2e7d32
```

## Part 1: 异常基础

### 1.1 异常的概念

**异常（Exception）**是 Python 程序在执行过程中发生的错误事件。当异常发生时，程序会停止执行并生成一个异常对象，描述发生了什么错误。

### 1.2 内置异常类型

Python 提供了丰富的内置异常类型，形成了一个层次结构：

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── AttributeError
    ├── RuntimeError
    └── ...
```

### 1.3 常见异常示例

```python
# 除数为零
result = 10 / 0  # ZeroDivisionError

# 索引越界
my_list = [1, 2, 3]
item = my_list[10]  # IndexError

# 键不存在
my_dict = {"name": "Alice"}
value = my_dict["age"]  # KeyError

# 类型错误
result = "hello" + 123  # TypeError

# 值错误
number = int("abc")  # ValueError
```

### 1.4 异常对象

当异常发生时，Python 会创建一个异常对象，包含错误信息：

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
        print(f"异常类型: {type(e).__name__}")  # ZeroDivisionError
        print(f"错误信息: {e}")  # division by zero
```

---

## Part 2: try-except 基础

### 2.1 基本语法

```python
try:
    # 可能抛出异常的代码
    risky_code()
except SomeError:
    # 处理该异常的代码
    handle_error()
```

### 2.2 捕获异常并获取信息

```python
try:
    result = int(user_input)
except ValueError as e:
        print(f"无效的数字: {e}")  # 缺少前导空格
```

### 2.3 示例：安全除法

```python
def safe_divide(a: float, b: float) -> float | None:
    """安全除法，除数为零时返回 None"""
    try:
        return a / b
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None

# 测试
print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # None
```

### 2.4 示例：安全类型转换

```python
def safe_parse_int(s: str) -> int | None:
    """安全地将字符串转换为整数，失败时返回 None"""
    try:
        return int(s)
    except ValueError:
        return None

# 测试
print(safe_parse_int("42"))    # 42
print(safe_parse_int("3.14"))  # None
print(safe_parse_int("abc"))   # None
```

---

## Part 3: 多个 except 子句

### 3.1 处理多种异常类型

```python
def process_number(a: str, b: str) -> float | None:
    """处理两个字符串为数字并相除"""
    try:
        num1 = int(a)
        num2 = int(b)
        return num1 / num2
    except ValueError:
        print(f"无效的数字: {a} 或 {b}")
        return None
    except ZeroDivisionError:
        print("除数不能为零")
        return None
```

### 3.2 捕获多种异常（元组形式）

```python
try:
    # 打开文件并解析内容
    with open("data.txt") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"处理失败: {e}")
```

### 3.3 异常捕获顺序

**重要**：except 子句从上到下匹配，**必须从具体到通用**：

```python
try:
    result = some_operation()
except ValueError:
    # 先捕获具体的异常
    print("值错误")
except Exception:
    # 最后捕获通用异常
    print("其他错误")
```

**错误示例**（先捕获 Exception 会导致 ValueError 永远不会被处理）：

```python
# ❌ 错误顺序
try:
    result = some_operation()
except Exception:
    print("其他错误")
except ValueError:  # 永远不会执行到
    print("值错误")
```

### 3.4 捕获所有异常

```python
# 方法 1: 捕获 Exception
try:
    result = risky_operation()
except Exception as e:
        print(f"发生错误: {e}")  # 方法 2: 使用裸 except（不推荐）
try:
    result = risky_operation()
except:  # ❌ 捕获所有异常，包括 SystemExit
    print("发生错误")
```

**推荐**：明确捕获需要的异常类型。

---

## Part 4: else 和 finally 子句

### 4.1 else 子句

`else` 子句在 **try 块中没有发生异常时** 执行：

```python
try:
    number = int(input("请输入数字: "))
except ValueError:
    print("无效输入")
else:
    # 只有在没有异常时才会执行
    print(f"你输入的数字是: {number}")
    print("处理成功！")
```

### 4.2 finally 子句

`finally` 子句 **无论是否发生异常都会执行**：

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("文件不存在")
finally:
    # 无论是否出错，都要关闭文件
    if 'file' in locals():
        file.close()
    print("清理完成")
```

### 4.3 典型用法：资源清理

```python
def read_config(filename: str) -> dict | None:
    """读取配置文件"""
    file = None
    try:
        file = open(filename, "r")
        content = file.read()
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"读取失败: {e}")
        return None
    finally:
        # 确保文件被关闭
        if file is not None:
            file.close()
```

### 4.4 更好的方式：with 语句

Python 3.3+ 推荐使用 `with` 语句自动管理资源：

```python
def read_config(filename: str) -> dict | None:
    """读取配置文件（使用 with 语句）"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"读取失败: {e}")
        return None
```

### 4.5 完整结构

```python
try:
    # 可能抛出异常的代码
    result = operation()
except SpecificError:
    # 处理特定异常
    handle_specific()
except AnotherError:
    # 处理另一种异常
    handle_another()
except Exception as e:
    # 捕获所有其他异常
    handle_general(e)
else:
    # 仅在无异常时执行
    success()
finally:
    # 无论是否有异常都执行
    cleanup()
```

---

## Part 5: raise 语句

### 5.1 抛出异常

使用 `raise` 语句显式抛出异常：

```python
def validate_age(age: int) -> int:
    """验证年龄是否合法"""
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄超出合理范围")
    return age
```

### 5.2 raise 完整语法

```python
# 抛出异常对象
raise ValueError("错误信息")

# 重新抛出当前捕获的异常
raise  # 只能在 except 块中使用

# 使用异常对象重新抛出
try:
    operation()
except ValueError as e:
    # 处理后重新抛出
    raise
```

### 5.3 异常传递

函数中未捕获的异常会向上传播：

```python
def level1():
    """第一层函数"""
    level2()  # 异常会传播到这里

def level2():
    """第二层函数"""
    raise ValueError("来自 level2 的错误")

try:
    level1()
except ValueError as e:
        print(f"捕获到异常: {e}")  # 输出: 捕获到异常: 来自 level2 的错误
```

### 5.4 抛出自定义错误信息

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError(
            f"除数不能为零 (被除数: {a}, 除数: {b})"
        )
    return a / b
```

---

## Part 6: 自定义异常类

### 6.1 创建自定义异常

```python
class InvalidAgeError(Exception):
    """年龄验证错误"""

    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"无效的年龄: {age}，年龄必须在 1-150 之间")
```

### 6.2 使用自定义异常

```python
def validate_age(age: int) -> int:
    """验证年龄 (1-150)"""
    if age < 1 or age > 150:
        raise InvalidAgeError(age)
    return age

# 测试
try:
    validate_age(-5)
except InvalidAgeError as e:
    print(f"年龄验证失败: {e}")
    print(f"无效的年龄值: {e.age}")
```

### 6.3 异常继承层次

```python
class ValidationError(Exception):
    """验证错误基类"""
    pass

class InvalidAgeError(ValidationError):
    """年龄验证错误"""
    pass

class InvalidEmailError(ValidationError):
    """邮箱验证错误"""
    pass
```

### 6.4 示例：用户注册验证

```python
class InvalidAgeError(ValueError):
    """年龄验证错误"""

    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"无效的年龄: {age}，年龄必须在 1-150 之间")

class InvalidEmailError(ValueError):
    """邮箱验证错误"""

    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"无效的邮箱地址: {email}")

def validate_age(age: int) -> int:
    """验证年龄 (1-150)"""
    if age < 1 or age > 150:
        raise InvalidAgeError(age)
    return age

def validate_email(email: str) -> str:
    """验证邮箱格式"""
    if not email:
        raise InvalidEmailError("邮箱不能为空")
    if "@" not in email:
        raise InvalidEmailError(email)
    return email

def register_user(username: str, age: int, email: str) -> dict[str, str]:
    """注册用户，收集所有验证错误"""
    errors: list[str] = []

    if not username:
        errors.append("用户名不能为空")

    try:
        validate_age(age)
    except InvalidAgeError as e:
        errors.append(str(e))

    try:
        validate_email(email)
    except InvalidEmailError as e:
        errors.append(str(e))

    if errors:
        raise ValueError("; ".join(errors))

    return {"username": username, "age": str(age), "email": email}
```

---

## Part 7: 异常链与 traceback

### 7.1 异常传播

当异常在函数中未被捕获时，它会传播到调用者：

```python
def outer():
    """外层函数"""
    inner()  # 异常会传播到这里

def inner():
    """内层函数"""
    raise RuntimeError("内部错误")

try:
    outer()
except RuntimeError as e:
        print(f"捕获异常: {e}")  # traceback 会自动打印
```

### 7.2 显式异常链（from）

使用 `raise ... from ...` 显式设置异常链：

```python
try:
    # 原始操作可能失败
    data = int("not_a_number")
except ValueError as original:
    # 添加上下文信息
    raise RuntimeError("数据解析失败") from original
```

输出：

```
Traceback (most recent call last):
  File "...", line 2, in <module>
    data = int("not_a_number")
ValueError: invalid literal for int() with base 10: 'not_a_number'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "...", line 5, in <module>
    raise RuntimeError("数据解析失败") from original
RuntimeError: 数据解析失败
```

### 7.3 隐式异常链（raise）

使用 `raise` 在 except 块中重新抛出时，会隐式保留原始异常：

```python
try:
    risky_operation()
except ValueError:
    # 隐式异常链：保留原始 traceback
    raise RuntimeError("操作失败")
```

### 7.4 抑制异常链（from None）

```python
try:
    data = int("invalid")
except ValueError:
    # 显式抑制异常链
    raise RuntimeError("解析失败") from None
```

输出（只显示新的异常）：

```
Traceback (most recent call last):
  File "...", line 4, in <module>
    raise RuntimeError("解析失败") from None
RuntimeError: 解析失败
```

### 7.5 访问 traceback 信息

```python
import traceback

try:
    risky_operation()
except Exception as e:
    # 获取 traceback 字符串
    tb_str = traceback.format_exc()
        print(f"异常 traceback:\n{tb_str}")  # 访问异常链
    if e.__cause__:
        print(f"原始异常: {e.__cause__}")
    if e.__context__:
        print(f"同时发生的异常: {e.__context__}")
```

---

## Part 8: 异常处理最佳实践

### 8.1 避免裸 except

```python
# ❌ 不推荐
try:
    result = operation()
except:
    print("发生错误")

# ✅ 推荐
try:
    result = operation()
except ValueError as e:
    print(f"值错误: {e}")
except TypeError as e:
    print(f"类型错误: {e}")
```

### 8.2 异常细化，避免过于宽泛

```python
# ❌ 过于宽泛
try:
    with open(filename) as f:
        return f.read()
except Exception:
    return None

# ✅ 细化捕获
try:
    with open(filename) as f:
        return f.read()
except FileNotFoundError:
    return None  # 文件不存在，返回 None
except PermissionError:
    raise  # 权限错误，应该让调用者知道
```

### 8.3 使用 finally 进行清理

```python
# ✅ 正确
connection = None
try:
    connection = get_connection()
    result = connection.query(sql)
finally:
    if connection:
        connection.close()

# ✅ 更好：使用 with
with get_connection() as connection:
    result = connection.query(sql)
```

### 8.4 异常与控制流

**谨慎使用**：异常不应该用于正常控制流。

```python
# ❌ 不推荐：使用异常控制循环
for item in items:
    try:
        result = lookup(item)
    except KeyError:
        continue

# ✅ 推荐：显式检查
for item in items:
    if item in lookup_dict:
        result = lookup_dict[item]
```

### 8.5 异常信息设计

```python
# ❌ 不友好的错误信息
raise ValueError("Invalid input")

# ✅ 友好的错误信息
raise ValueError(
    f"无效的输入值: '{user_input}'\n"
    f"期望: 正整数 (1-1000)\n"
    f"实际: {type(user_input).__name__}"
)
```

### 8.6 日志记录

```python
import logging

logger = logging.getLogger(__name__)

try:
    risky_operation()
except ValueError as e:
    logger.error(f"值错误，操作中止: {e}", exc_info=True)
    raise
```

### 8.7 异常处理检查清单

| 检查项 | 说明 |
|--------|------|
| 明确捕获 | 指定要捕获的异常类型 |
| 及时清理 | 使用 finally 或 with 释放资源 |
| 保留信息 | 重新抛出时保留原始异常 |
| 用户友好 | 错误信息对用户有帮助 |
| 不过度使用 | 不要用异常代替正常控制流 |
| 记录日志 | 记录异常以便调试 |

---

## 9. Web 框架异常：HTTPException

> ⚠️ **本节为前置铺垫**：为后续 L27 FastAPI 做准备。HTTPException 是 Web 框架特有的异常类型。

### 9.1 为什么需要 HTTPException？

Python 标准库的异常（如 `ValueError`、`TypeError`）是**通用异常**。但在 Web 开发中，我们需要根据 HTTP 协议返回对应的状态码：

| 场景 | HTTP 状态码 | 标准异常 | HTTPException |
|------|------------|---------|---------------|
| 用户不存在 | 404 | — | `HTTPException(404)` |
| 资源冲突 | 409 | — | `HTTPException(409)` |
| 未认证访问 | 401 | — | `HTTPException(401)` |
| 参数校验失败 | 422 | — | `HTTPException(422)` |

`HTTPException` 继承自 `Exception`，但增加了 `status_code` 和 `detail` 字段：

```python
# HTTPException 本质是一个普通的异常类
# 但它携带了 HTTP 状态码信息
class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.detail = detail or ""
        super().__init__(detail)

# FastAPI 中使用
raise HTTPException(status_code=404, detail="User not found")
# → 返回 HTTP 404 响应，body: {"detail": "User not found"}
```

### 9.2 常见 HTTP 状态码与异常

```python
from fastapi import HTTPException

# 400 Bad Request - 请求语法错误
raise HTTPException(status_code=400, detail="Invalid email format")

# 401 Unauthorized - 未认证（未提供或无效凭证）
raise HTTPException(status_code=401, detail="Invalid API key")

# 403 Forbidden - 已认证但无权限
raise HTTPException(status_code=403, detail="Admin access required")

# 404 Not Found - 资源不存在
raise HTTPException(status_code=404, detail="User with id=42 not found")

# 409 Conflict - 资源冲突（如重复创建）
raise HTTPException(status_code=409, detail="Username already taken")

# 422 Unprocessable Entity - 校验失败（请求格式正确但语义错误）
raise HTTPException(status_code=422, detail="Field 'age' must be positive")

# 500 Internal Server Error - 服务器内部错误
raise HTTPException(status_code=500, detail="Database connection failed")
```

### 9.3 HTTPException 与普通异常的层级关系

```
Exception (Python 标准)
├── ValueError / TypeError / RuntimeError  ← L08 已覆盖
└── HTTPException (FastAPI/Starlette 框架) ← 本节新增
        ↑
        ├── 继承 Exception 的所有特性
        ├── 额外携带 status_code（HTTP 状态码）
        └── 额外携带 detail（错误详情）
```

**关键理解**：`HTTPException` 本质上就是一个**携带 HTTP 状态码的普通异常**。在 L27 FastAPI 中，我们将深入使用它。

---

## 💭 课堂思考

### 思考 1: 为什么需要异常处理？

**问题**：既然程序出错会崩溃，为什么不直接在代码中检查所有边界条件？

**引导思考**：
- 防御性编程 vs 异常处理
- EAFP 原则（LBYL 原则）
- 异常传播机制的价值

**代码对比**：
```python
# LBYL (Look Before You Leap)
if os.path.exists('file.txt'):
    with open('file.txt') as f:
        content = f.read()

# EAFP (Easier to Ask for Forgiveness than Permission)
try:
    with open('file.txt') as f:
        content = f.read()
except FileNotFoundError:
    content = ""
```

---

### 思考 2: 捕获异常 vs 防御性检查

**问题**：什么时候应该用 try-except，什么时候应该用 if 检查？

**引导思考**：
- 预期错误 vs 意外错误
- 性能考量：检查 vs 捕获
- 代码可读性

**决策原则**：
- 正常流程的一部分 → if 检查
- 异常情况（不应该发生）→ 异常处理
- 外部输入（不可控）→ 两者结合

---

### 思考 3: 异常链的价值

**问题**：为什么要保留原始异常，而不是直接抛出一个新异常？

**引导思考**：
- 调试信息完整性
- 异常溯源
- 调试成本

**代码示例**：
```python
# 不好的做法：丢失原始信息
def parse_config():
    try:
        return json.loads(data)
    except Exception as e:
        raise ConfigError("配置解析失败")  # 原始错误丢失

# 好的做法：异常链
def parse_config():
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ConfigError("配置解析失败") from e  # 保留原始错误
```

## 🚀 实战案例

### 案例 1: 安全的数据解析器

```python
import json

def safe_parse_json(json_string: str) -> dict | None:
    """安全解析 JSON 字符串，失败时返回 None"""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return None

# 测试
data1 = safe_parse_json('{"name": "Alice", "age": 25}')
data2 = safe_parse_json('invalid json')
print(f"data1: {data1}")  # {'name': 'Alice', 'age': 25}
print(f"data2: {data2}")  # None
```

### 案例 2: 带重试机制的下载器

```python
import time

def download_with_retry(url: str, max_retries: int = 3) -> str | None:
    """带重试机制的下载函数"""
    for attempt in range(max_retries):
        try:
            # 模拟下载（实际使用 requests）
            if attempt == 2:
                return f"Downloaded: {url}"
            else:
                raise ConnectionError("Network timeout")
        except ConnectionError as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # 等待后重试
    print(f"达到最大重试次数 {max_retries}")
    return None

# 测试
result = download_with_retry("https://example.com/data")
print(result)
```

### 案例 3: 配置验证器

```python
class ConfigError(Exception):
    """配置错误基类"""
    pass

class MissingKeyError(ConfigError):
    """缺少必需键"""
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"缺少必需的配置键: {key}")

class InvalidValueError(ConfigError):
    """值无效"""
    def __init__(self, key: str, value: any, expected: str) -> None:
        self.key = key
        self.value = value
        super().__init__(
            f"配置键 '{key}' 的值无效\n"
            f"  期望: {expected}\n"
            f"  实际: {value!r}"
        )

def validate_config(config: dict) -> None:
    """验证配置完整性"""
    required_keys = ["host", "port", "database"]
    
    # 检查必需键
    for key in required_keys:
        if key not in config:
            raise MissingKeyError(key)
    
    # 验证值
    if not isinstance(config.get("port"), int):
        raise InvalidValueError("port", config.get("port"), "int")
    
    if config["port"] < 1 or config["port"] > 65535:
        raise InvalidValueError("port", config["port"], "1-65535 之间的整数")

# 测试
try:
    validate_config({"host": "localhost", "port": 5432, "database": "mydb"})
    print("配置验证通过")
except ConfigError as e:
    print(f"配置错误: {e}")
```

---

## 💡 常见异常处理陷阱

### 陷阱 1: 裸 except 子句

```python
# ❌ 错误：捕获所有异常
try:
    result = risky_operation()
except:
    print("出错了")

# ✅ 正确：捕获特定异常
try:
    result = risky_operation()
except ValueError as e:
    print(f"值错误: {e}")
except ConnectionError as e:
    print(f"连接错误: {e}")
```

### 陷阱 2: 吞掉异常

```python
# ❌ 错误：捕获但不处理
try:
    result = risky_operation()
except Exception:
    pass  # 异常被忽略了！

# ✅ 正确：记录或重新抛出
try:
    result = risky_operation()
except Exception as e:
    logging.error(f"操作失败: {e}")
    raise  # 重新抛出
```

### 陷阱 3: 在 finally 中返回

```python
# ❌ 错误：finally 中的 return 会覆盖异常
def bad_example():
    try:
        return risky_operation()
    finally:
        return "cleanup"  # 异常被吞掉了！

# ✅ 正确：避免在 finally 中返回
def good_example():
    result = None
    error = None
    try:
        result = risky_operation()
    except Exception as e:
        error = e
    finally:
        cleanup()
    return result
```

### 陷阱 4: 使用异常控制流程

```python
# ❌ 错误：用异常代替正常流程
try:
    value = int(text)
except ValueError:
    value = 0  # 期望文本不是数字

# ✅ 正确：先检查再操作
if text.isdigit():
    value = int(text)
else:
    value = 0
```

### 陷阱 5: 忽略异常链

```python
# ❌ 错误：丢失原始异常信息
try:
    risky_operation()
except RuntimeError:
    raise ValueError("操作失败")  # 原始异常信息丢失

# ✅ 正确：保留异常链
try:
    risky_operation()
except RuntimeError as e:
    raise ValueError("操作失败") from e  # 保留异常链
```

---

## 🎓 核心知识点总结

### 异常处理核心概念

| 概念 | 说明 |
|------|------|
| **try-except** | 捕获和处理异常 |
| **raise** | 抛出异常 |
| **else** | 仅在无异常时执行 |
| **finally** | 无论是否有异常都执行 |
| **自定义异常** | 继承 Exception 创建业务异常 |
| **异常链** | `raise ... from ...` 保留原始错误 |

### 常见异常类型

| 异常 | 触发场景 |
|------|----------|
| `ZeroDivisionError` | 除数为零 |
| `IndexError` | 索引越界 |
| `KeyError` | 字典键不存在 |
| `ValueError` | 值不合法 |
| `TypeError` | 类型不匹配 |
| `FileNotFoundError` | 文件不存在 |
| `JSONDecodeError` | JSON 解析失败 |

### 异常处理速查

```python
# 基本捕获
try:
    risky_code()
except SpecificError:
    handle()

# 捕获并获取信息
try:
    risky_code()
except SpecificError as e:
    print(f"错误: {e}")

# 多个异常
try:
    risky_code()
except (Error1, Error2) as e:
    handle()

# 完整结构
try:
    code()
except SpecificError:
    handle_specific()
except Exception as e:
    handle_general(e)
else:
    # 仅在无异常时执行
    success()
finally:
    # 无论是否有异常都执行
    cleanup()

# 抛出异常
raise ValueError("错误信息")

# 异常链
raise NewError("上下文") from original_error
```

### 关键要点

- ✅ 明确捕获具体异常类型，避免裸 except
- ✅ 使用 finally 或 with 确保资源释放
- ✅ 重新抛出时保留原始异常（异常链）
- ✅ 异常信息要用户友好，包含足够上下文
- ❌ 不要用异常代替正常控制流
- ❌ 不要捕获所有异常后什么都不做

### 最佳实践检查清单

| 检查项 | 状态 |
|--------|------|
| 捕获具体异常而非 Exception | ☐ |
| 使用 with 或 finally 释放资源 | ☐ |
| 保留原始异常的异常链 | ☐ |
| 提供用户友好的错误信息 | ☐ |
| 记录日志以便调试 | ☐ |
| 不在正常控制流中使用异常 | ☐ |

---

### 异常类层次结构

```
BaseException
├── SystemExit
├── KeyboardInterrupt
└── Exception
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── RuntimeError
    └── ... (更多异常类型)
```

---

## 📚 延伸阅读

- [Python 官方文档 - 异常](https://docs.python.org/3/library/exceptions.html)
- [Python 官方文档 - try 语句](https://docs.python.org/3/reference/compound_stmts.html#try)
- [Real Python - Python Exceptions](https://realpython.com/python-exceptions/)
- [MDN - HTTP 状态码](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 Python 异常的概念和类型层次
- [ ] 使用 try-except 捕获和处理异常
- [ ] 使用 else 和 finally 子句控制执行流程
- [ ] 使用 raise 语句抛出异常
- [ ] 创建和使用自定义异常类
- [ ] 使用异常链传递上下文信息
- [ ] 避免常见的异常处理反模式
- [ ] 根据 HTTP 状态码选择合适的 HTTPException
- [ ] 能够编写相关代码
- [ ] 解决常见问题

---

## 📝 进阶预告

完成本课程后，你已经掌握了异常处理的精髓。在下一课 [L07: 面向对象基础](../L07-oop-basics/lesson.md) 中，我们将学习：

- 🏛️ **类与对象**：类的定义、__init__ 构造方法、self 参数
- 🔒 **封装**：私有属性、@property 装饰器
- 👨‍👩‍👧 **继承**：单继承、方法重写、super() 调用
- 🔄 **多态**：接口统一、鸭子类型
- 🎭 **魔术方法**：__str__、__repr__、__eq__（L08 深入）

> 💡 **学习路径**：L06 → L07（面向对象）→ L08（魔术方法）→ ...

---

## 🔗 下一步

完成本课程后，继续学习：

- [L07: 面向对象基础](../L07-oop-basics/lesson.md)

---