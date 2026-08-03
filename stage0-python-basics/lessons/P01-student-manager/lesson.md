# P01: Python 基础实战

> **课程编号**: P01
> **所属阶段**: Stage 0 - Python 编程基础
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: L01-L09 (Stage 0 全部课程)
> **版本**: v3.0
> **最后更新**: 2026-08-02
> **核心版本**: Python 3.13

---

## 📚 项目概述

### 项目：学员管理系统（Student Management System）

一个完整的命令行学员管理工具，综合运用 Stage 0 基础内容：

- **变量与数据类型**：存储学员信息
- **控制流**：用户交互循环
- **数据结构**：列表、字典管理数据
- **函数**：功能模块化
- **文件操作**：持久化存储
- **模块化**：多文件组织
- **异常处理**：容错处理
- **面向对象**：使用类简化数据模型

### 功能需求

1. **添加学员**：创建新学员记录
2. **查看学员**：列出所有学员
3. **查询学员**：按 ID 获取单个学员
4. **更新学员**：修改学员信息
5. **删除学员**：移除学员记录
6. **搜索学员**：按姓名模糊搜索
7. **统计信息**：学员数量和年龄统计

---

## 🏗️ 项目结构

### 目录组织

```text
P01-student-manager/
├── examples/                  # 示例代码
│   ├── 01_student_basics.py # 基础结构
│   ├── 02_class_student.py  # 类的定义
│   ├── 03_persistence.py     # 数据持久化
│   └── 04_cli_demo.py        # CLI 交互演示
├── exercises/                # 练习题
│   └── 01_student_manager.py # 学员管理器练习
├── solutions/                # 参考答案
│   ├── __init__.py
│   └── student_manager.py
├── tests/                    # 测试用例
│   ├── conftest.py
│   └── test_student_manager.py
├── README.md
└── lesson.md
```

---

## 📝 实现步骤

### 步骤 1: 数据模型（类定义）

使用类和 `__init__` 定义数据模型：

```python
class Student:
    """学员数据模型"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        self.student_id = student_id
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """用于调试和显示"""
        return f"Student({self.student_id!r}, {self.name!r}, {self.age})"

    def __eq__(self, other: object) -> bool:
        """按学号比较"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id

    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建实例"""
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
        )
```

**为什么要用类？**

| 特性 | 字典 | 类实例 |
|------|------|--------|
| 代码量 | 多处重复字段名 | 字段集中定义 |
| 提示 | 无 IDE 补全 | 有类型补全 |
| 扩展 | 需改多处 | 改一处即可 |
| 方法 | 无 | 可内嵌行为 |

### 步骤 2: 数据管理器

```python
class StudentManager:
    """学员管理器"""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}

    def add_student(self, student: Student) -> bool:
        """添加学员"""
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True

    def get_student(self, student_id: str) -> Student | None:
        """获取学员"""
        return self.students.get(student_id)

    def remove_student(self, student_id: str) -> bool:
        """删除学员"""
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False

    def update_student(
        self,
        student_id: str,
        name: str | None = None,
        age: int | None = None,
    ) -> bool:
        """更新学员信息"""
        student = self.students.get(student_id)
        if student is None:
            return False
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        return True

    def list_students(self) -> list[Student]:
        """列出所有学员（返回副本）"""
        return list(self.students.values())

    def search_by_name(self, name: str) -> list[Student]:
        """按姓名搜索（不区分大小写）"""
        name_lower = name.lower()
        return [
            s for s in self.students.values()
            if name_lower in s.name.lower()
        ]
```

### 步骤 3: 数据持久化

```python
import json
from pathlib import Path

class StudentStorage:
    """学员数据持久化"""

    def __init__(self, filepath: str = "students.json"):
        self.filepath = Path(filepath)

    def save(self, students: list[Student]) -> None:
        """保存到文件"""
        data = [s.to_dict() for s in students]
        self.filepath.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self) -> list[Student]:
        """从文件加载"""
        if not self.filepath.exists():
            return []
        try:
            content = self.filepath.read_text(encoding="utf-8")
            data = json.loads(content)
            return [Student.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []
```

---

## 🔑 关键概念

### 1. 返回副本而非原对象

```python
def list_students(self) -> list[Student]:
    """返回副本，避免外部修改影响内部状态"""
    return list(self.students.values())
```

**为什么重要？**

```python
# ❌ 危险：返回原始列表
def bad_list(self):
    return list(self.students.values())

# ✅ 安全：返回副本
def good_list(self):
    return list(self.students.values())

# 测试
mgr.list_students().append(hacker_student)
assert len(mgr.list_students()) == 1  # 内部状态未受影响
```

### 2. 返回值表示成功/失败

```python
def add_student(self, student: Student) -> bool:
    """返回 True 表示成功，False 表示失败"""
    if student.student_id in self.students:
        return False  # 已存在
    self.students[student.student_id] = student
    return True
```

### 3. 可选参数的更新模式

```python
def update_student(
    self,
    student_id: str,
    name: str | None = None,
    age: int | None = None,
) -> bool:
    """只更新提供的字段"""
    student = self.students.get(student_id)
    if student is None:
        return False
    if name is not None:
        student.name = name
    if age is not None:
        student.age = age
    return True
```

---

## 💡 最佳实践

### 1. 类型注解

```python
# ✅ 好：完整的类型注解
def search_by_name(self, name: str) -> list[Student]:
    ...

# ❌ 差：缺少类型注解
def search_by_name(self, name):
    ...
```

### 2. 文档字符串

```python
def add_student(self, student: Student) -> bool:
    """添加学员

    Args:
        student: 学员对象

    Returns:
        bool: 添加是否成功（学号已存在时返回 False）
    """
    ...
```

### 3. 一致性返回

```python
# ✅ 一致：都返回 bool
def add_student(...) -> bool: ...
def remove_student(...) -> bool: ...
def update_student(...) -> bool: ...

# ❌ 不一致：有时返回对象，有时返回 None
def get_student(...) -> Student | None: ...  # 这是可以的
```

---

## 🧪 测试要点

### 单元测试覆盖

```python
# 测试基本功能
def test_add_student():
    manager = StudentManager()
    result = manager.add_student(Student("001", "张三", 20))
    assert result is True

# 测试边界情况
def test_add_duplicate():
    manager = StudentManager()
    manager.add_student(Student("001", "张三", 20))
    result = manager.add_student(Student("001", "李四", 21))
    assert result is False  # 重复添加应失败

# 测试返回副本
def test_list_returns_copy():
    manager = StudentManager()
    manager.add_student(Student("001", "张三", 20))
    snapshot = manager.list_students()
    snapshot.append(Student("999", "黑客", 99))
    assert len(manager.list_students()) == 1
```

---

## ⚠️ 常见错误

### 1. 返回原始字典而非副本

```python
# ❌ 错误
def list_students(self):
    return self.students.values()  # 返回 dict_values，可迭代但非列表

# ✅ 正确
def list_students(self):
    return list(self.students.values())  # 返回真正的列表
```

### 2. 更新时未检查存在性

```python
# ❌ 错误
def update_student(self, student_id, name):
    self.students[student_id].name = name  # KeyError 如果不存在

# ✅ 正确
def update_student(self, student_id, name):
    if student_id not in self.students:
        return False
    self.students[student_id].name = name
    return True
```

### 3. 硬编码文件路径

```python
# ❌ 错误
self.filepath = "students.json"  # 相对路径，可能在不同目录出问题

# ✅ 正确
self.filepath = Path(filepath)  # 使用 pathlib，支持绝对/相对路径
```

---

## 📊 Stage 0 知识图谱

本项目综合运用了 Stage 0 的以下知识点：

```
Stage 0 知识图谱
├── L01-L02: 变量、类型、运算符与控制流
│   └── 字段赋值、条件判断、循环交互
├── L03: 数据结构
│   └── dict / list 存储和检索学员
├── L04: 函数与模块
│   └── 方法封装、参数设计、模块组织
├── L05: 文件操作
│   └── JSON 持久化和 pathlib 路径处理
├── L06: 面向对象基础
│   └── Student / StudentManager 职责划分
├── L07: 魔术方法
│   └── 自定义 __repr__ / __eq__ 实现表示与比较
├── L08: 异常处理
│   └── 输入转换、文件读写异常捕获
└── P01: 综合实战 ⭐
    └── 完整项目管理
```

---

## 🎯 学习检查清单

完成项目后，检查是否掌握：

- [ ] 类的定义和使用
- [ ] 字典的增删改查操作
- [ ] 返回值表示成功/失败的设计模式
- [ ] 返回副本而非原对象
- [ ] 可选参数的处理
- [ ] 文件的读写操作
- [ ] 类型注解的编写
- [ ] 单元测试的编写

---

## 🚀 扩展挑战

### 1. 添加持久化

```python
class StudentManager:
    def __init__(self, storage: StudentStorage | None = None):
        self.storage = storage or StudentStorage()
        self.students = {}
        self._load()

    def _load(self) -> None:
        """从文件加载"""
        for student in self.storage.load():
            self.students[student.student_id] = student

    def _save(self) -> None:
        """保存到文件"""
        self.storage.save(list(self.students.values()))
```

### 2. 添加排序功能

```python
def list_students_sorted(self, key: str = "name") -> list[Student]:
    """返回排序后的学员列表"""
    valid_keys = {"name", "age", "student_id"}
    if key not in valid_keys:
        raise ValueError(f"无效的排序键: {key}")
    return sorted(self.students.values(), key=lambda s: getattr(s, key))
```

### 3. 添加数据验证

```python
class Student:
    """带数据验证的学员模型"""

    def __init__(self, student_id: str, name: str, age: int) -> None:
        # L08 将在后面学到：这里的数据验证
        # 目前阶段可以在 __init__ 中做基础检查
        if not student_id:
            student_id = "UNKNOWN"
        if not name:
            name = "未命名"
        if age < 0:
            age = 0
        elif age > 150:
            age = 150
        self.student_id = student_id
        self.name = name
        self.age = age
```

---

## 📚 扩展阅读

### 下一步学习

- **Stage 1 L10**: Python 类型系统 - 类型注解与类型守卫
- **Stage 1 L11**: 迭代器与生成器 - 内存高效的数据处理
- **Stage 1 L12**: Python 高级特性 - 装饰器与上下文管理器

> **📌 深入学习**: 完整的正则表达式语法参见 L18（第 18 课）。


### 推荐练习

1. **扩展功能**：添加学员的入学日期、班级信息
2. **改进存储**：支持 CSV 格式导入导出
3. **单元测试**：为每个方法编写测试
4. **GUI 界面**：使用 tkinter 制作图形界面

---

## 🎉 总结

### 已掌握的核心技能

✅ **基础语法**：变量、数据类型、运算符
✅ **控制流**：条件分支、循环、异常处理
✅ **数据结构**：列表、字典、集合、元组
✅ **函数编程**：函数定义、参数、返回值
✅ **文件操作**：读写文件、路径处理
✅ **模块化**：导入模块、创建包
✅ **面向对象**：类实例封装数据与行为
✅ **项目实战**：完整项目的组织与实现

### 下一阶段预告

**Stage 1: Python 进阶**
- 列表推导式与生成器表达式
- 上下文管理器
- 装饰器
- 迭代器与生成器
- 正则表达式

**恭喜你完成 Stage 0！** 🎊
