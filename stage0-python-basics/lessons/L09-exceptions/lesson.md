# L09: 异常处理（Exceptions）

> **课程编号**: L09
> **所属阶段**: Stage 0 - Python 编程基础
> **预计时长**: 3 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: L08（魔术方法）
> **版本**: v2.2
> **最后更新**: 2026-08-02

---

## 目录

1. [什么是异常](#1-什么是异常)
2. [try-except 基础](#2-try-except-基础)
3. [多个 except 子句](#3-多个-except-子句)
4. [else 和 finally 子句](#4-else-和-finally-子句)
5. [raise 语句](#5-raise-语句)
6. [自定义异常类](#6-自定义异常类)
7. [异常链与 traceback](#7-异常链与-traceback)
8. [异常处理最佳实践](#8-异常处理最佳实践)

---

## 1. 什么是异常

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
    print(f"异常对象: {e}")
```

---

## 2. try-except 基础

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
    print(f"无效的数字: {e}")
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

## 3. 多个 except 子句

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
    print(f"发生错误: {e}")

# 方法 2: 使用裸 except（不推荐）
try:
    result = risky_operation()
except:  # ❌ 捕获所有异常，包括 SystemExit
    print("发生错误")
```

**推荐**：明确捕获需要的异常类型。

---

## 4. else 和 finally 子句

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

## 5. raise 语句

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
    print(f"捕获到异常: {e}")
    # 输出: 捕获到异常: 来自 level2 的错误
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

## 6. 自定义异常类

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

## 7. 异常链与 traceback

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
    print(f"捕获异常: {e}")
    # traceback 会自动打印
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
    print(f"异常 traceback:\n{tb_str}")

    # 访问异常链
    if e.__cause__:
        print(f"原始异常: {e.__cause__}")
    if e.__context__:
        print(f"同时发生的异常: {e.__context__}")
```

---

## 8. 异常处理最佳实践

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

## 扩展阅读

- [Python 官方文档 - 异常](https://docs.python.org/3/library/exceptions.html)
- [Python 官方文档 - try 语句](https://docs.python.org/3/reference/compound_stmts.html#try)
- [Real Python - Python Exceptions](https://realpython.com/python-exceptions/)
- [MDN - HTTP 状态码](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)

---

## 下一步

完成本课程后，继续学习：

- [P01: Python 基础综合项目](../P01-student-manager/lesson.md)

---

## 🔮 在下一课中，我们将学习：

### P01: Python 基础综合项目 — 学员管理系统

恭喜你完成了 Stage 0 的所有理论课程！现在是时候将所学知识综合运用了：

1. **项目目标**
   - 构建一个完整的命令行学员管理系统
   - 实现 CRUD 操作（增删改查）
   - 数据持久化（JSON 文件存储）

2. **技术栈**
   - **数据建模**：使用 @dataclass 定义学员类
   - **业务逻辑**：管理器类封装所有操作
   - **文件操作**：JSON 读写、异常处理
   - **用户交互**：命令行界面（CLI）

3. **核心功能**
   - 添加学员（姓名、学号、年龄）
   - 删除学员
   - 查询学员（按学号、按姓名搜索）
   - 列出所有学员
   - 统计信息（总数、平均年龄）

4. **学到的技能**
   - 如何组织多文件项目
   - 如何设计类的职责划分
   - 如何编写可测试的代码
   - 如何处理边界条件和异常

**这个项目将运用 L01-L08 的全部知识**：

- ✅ L01: 变量、类型注解
- ✅ L02: 控制流、循环
- ✅ L03: 字典、列表数据存储
- ✅ L04: 函数封装业务逻辑
- ✅ L05: JSON 文件持久化
- ✅ L06: 类设计（Student、StudentManager）
- ✅ L07: 魔术方法（__repr__、__eq__）
- ✅ L08: 异常处理（FileNotFoundError、数据验证）

**准备好了吗？** 让我们构建你的第一个完整 Python 项目！

👉 [开始实战项目 P01](../P01-student-manager/lesson.md)
