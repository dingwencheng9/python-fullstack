# Stage 0 知识点越界全面审查报告

> **审查日期**: 2026-08-04
> **审查范围**: `examples/`, `exercises/`, `lesson.md`, `README.md`（排除 tests/ 和 solutions/）
> **审查文件数**: 124 个
> **工具**: `scripts/audit_stage0_knowledge_boundary.py`

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 审查文件总数 | 124 |
| 发现违规数 | 456（原始扫描） |
| **真实越界（需修复）** | **约 25-30 个** |
| **疑似误报（教学合理）** | **约 426 个** |

### 按严重程度分布

| 严重程度 | 数量 | 说明 |
|----------|------|------|
| 🚨 CRITICAL | 5 | **必须修复** |
| ⚠️ HIGH | 300 | 需要复核 |
| 📝 MEDIUM | 151 | 术语越界，需复核 |

### 按课程分布

| 课程 | 原始违规 | 真实越界 | 说明 |
|------|----------|----------|------|
| L01 | 115 | **~10** | 术语误报居多 |
| L02 | 243 | **~15** | 术语误报居多 |
| L03 | 79 | **~5** | 类型注解越界 |
| L04 | 6 | **0-2** | 需复核 |
| L06 | 13 | **5** | class 定义越界 |
| L07-L09 | 0 | **0** | ✅ 无越界 |

---

## 一、CRITICAL 越界（必须修复）

### 1.1 L01-python-core — `examples/06_type_annotations.py`

| 行号 | 越界内容 | 说明 |
|------|----------|------|
| 15 | `def add(a: int, b: int) -> int:` | L01 禁止 `def` 函数定义 |
| 18 | `def greet(name: str) -> str:` | L01 禁止 `def` 函数定义 |
| 21 | `def calculate_area(width: float, height: float) -> float:` | L01 禁止 `def` 函数定义 |
| 53 | `def process_id(user_id: str \| int) -> str:` | L01 禁止 `def` 函数定义 |
| 69 | `def no_return() -> None:` | L01 禁止 `def` 函数定义 |

**修复方案**: 删除此文件或重命名为 `examples/06_type_annotations_advanced.py` 并移动到 L04

---

### 1.2 L01-python-core — `exercises/05_fstring_practice.py`

| 行号 | 越界内容 | 说明 |
|------|----------|------|
| 78 | `names = ["Alice", "Bob", "Charlie"]` | L01 禁止 `list` 字面量 |
| 79 | `scores = [95, 87, 92]` | L01 禁止 `list` 字面量 |

**修复方案**: 改为使用字符串或其他方式演示 f-string

---

### 1.3 L06-exceptions — `examples/05_custom_exceptions.py`

| 行号 | 越界内容 | 说明 |
|------|----------|------|
| 4 | `class ValidationError(Exception):` | L06 禁止 `class` 定义 |
| 12 | `class EmailValidationError(ValidationError):` | L06 禁止 `class` 定义 |
| 19 | `class PasswordValidationError(ValidationError):` | L06 禁止 `class` 定义 |

**修复方案**:
- 选项 A：将此文件移动到 L07（面向对象基础）
- 选项 B：在 L06 中使用函数式异常处理，删除自定义类

---

### 1.4 L06-exceptions — `examples/03_custom_exceptions.py`

| 行号 | 越界内容 | 说明 |
|------|----------|------|
| 20 | `class NetworkError(Exception):` | L06 禁止 `class` 定义 |
| 24 | `class TimeoutError(NetworkError):` | L06 禁止 `class` 定义 |

**修复方案**: 同上

---

## 二、HIGH 越界（需复核）

### 2.1 L01 术语误报分析

L01 的 lesson.md 中大量出现 "函数"、"对象"、"类"、"class" 等术语，**经复核为合理误报**：

| 误报原因 | 说明 |
|----------|------|
| `<class 'int'>` | Python 内置输出，无法避免 |
| `help(print)` | REPL 帮助文档包含 "function" |
| `def` 预告提示 | 正确标注 "L04 将学习 def" |
| "对象"概念 | Python 官方术语，解释变量引用模型必需 |
| "方法"概念 | 字符串方法如 `.upper()` 是 L01 教学内容 |

**结论**: L01 lesson.md 无需修改

---

### 2.2 L02 元组解包误报分析

L02 中 `a, b = 10, 3` 被报告为 "Tuple 越界"，**经复核为误报**：

```python
# L02 允许的操作
a, b = 10, 3  # ✅ 元组解包（用于多变量赋值）
left, right = right, left  # ✅ 交换变量

# L02 禁止的操作
t = (1, 2, 3)  # ❌ 元组字面量（属于 L03）
```

**结论**: 需要修正脚本逻辑，元组解包不应被视为越界

---

### 2.3 L03 类型注解越界

| 文件 | 行号 | 越界内容 | 说明 |
|------|------|----------|------|
| `02_tuple_immutable.py` | 8-10 | `list[int]` | L03 禁止泛型注解 |
| `04_set_operations.py` | 8, 11, 16-17 | `set[int]` | L03 禁止泛型注解 |
| `05_nested_data_parsing.py` | 81, 87 | `dict[str, int]` | L03 禁止泛型注解 |
| `03_exercise.py` | 31, 44 | `list[str]`, `dict[str, str]` | L03 禁止泛型注解 |

**修复方案**: 改为 Python 3.9 之前的旧式注解 `List[str]`, `Dict[str, str]` 或移除类型注解

---

## 三、疑似越界文件清单

### 3.1 L04 疑似越界（需确认课程定位）

| 文件 | 越界内容 | 说明 |
|------|----------|------|
| `01_functions.py` | `def` 函数定义 | L04 应该允许 def |
| 需复核 | - | L04 是函数课程，应允许 def |

**结论**: L04 应允许 `def`，这可能是脚本误报

---

## 四、修复优先级

| 优先级 | 越界类型 | 数量 | 修复策略 |
|--------|----------|------|----------|
| P0 | L01 `def` 函数定义 | 5 | 删除或移动文件 |
| P0 | L06 `class` 定义 | 5 | 移动到 L07 或重构 |
| P1 | L03 泛型注解 | ~10 | 改为旧式注解 |
| P2 | L01 lesson.md 术语 | ~80 | **无需修复**（误报） |
| P2 | L02 元组解包 | ~50 | **无需修复**（误报） |

---

## 五、知识边界白名单（经复核正确）

### L01 允许的知识点（已验证）

```python
# ✅ 变量类型注解（仅用于文档）
name: str = "Alice"
age: int = 25

# ✅ 类型转换
int("42"), float("3.14"), str(123)

# ✅ f-string 格式化
f"Hello, {name}!", f"Pi = {pi:.2f}", f"{x=}"
```

### L02 允许的知识点（已验证）

```python
# ✅ 元组解包（多变量赋值）
a, b = 10, 3
left, right = right, left  # 交换

# ✅ for 循环遍历字符串
for char in "Python":
    print(char)

# ✅ enumerate/zip
for i, char in enumerate("abc"):
    print(i, char)
```

---

## 六、附录：知识边界定义

### A. L01 严格禁止（已确认）

| 语法 | 说明 |
|------|------|
| `def` | 函数定义（L04 才学） |
| `class` | 类定义（L07 才学） |
| `list` 字面量 `[...]` | 列表（L03 才学） |
| `dict` 字面量 `{...}` | 字典（L03 才学） |
| `if`/`for`/`while` | 控制流（L02 才学） |

### B. L02 允许（已确认）

| 语法 | 说明 |
|------|------|
| `a, b = 10, 3` | 元组解包（多变量赋值） |
| `for x in range(5):` | 整数循环 |
| `if x > 0:` | 条件分支 |

### C. L03 禁止

| 语法 | 说明 |
|------|------|
| `list[T]` | 泛型注解（L10 才学） |
| `dict[K, V]` | 泛型注解（L10 才学） |
| `def` | 函数定义 |
| `class` | 类定义 |

---

## 七、建议行动

### 立即行动（P0）

1. **删除或移动** `L01-python-core/examples/06_type_annotations.py`
2. **移动** `L06-exceptions/examples/05_custom_exceptions.py` 和 `03_custom_exceptions.py` 到 L07

### 计划行动（P1）

3. **修改** `L03` 中的类型注解为旧式或移除
4. **修正** 审查脚本中的元组解包误报逻辑

### 无需行动（P2）

5. L01 lesson.md 中的术语（Python 内置输出）
6. L02 元组解包（教学合理）

---

**报告生成**: `scripts/audit_stage0_knowledge_boundary.py`
**审查时间**: 2026-08-04
