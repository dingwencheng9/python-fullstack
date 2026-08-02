# solutions/ - 参考答案

**用途**：提供 L09 收官项目的参考实现，展示一个小型业务对象管理器的清晰边界和可测试行为。

> ⚠️ 建议先独立完成 `exercises/01_student_manager.py`，再查看本目录。

## 文件清单

| 文件 | 对应练习 | 说明 |
|------|----------|------|
| `student_manager.py` | `01_student_manager.py` | `Student` 数据类与 `StudentManager` 参考实现 |
| `__init__.py` | - | 统一导出 `Student`、`StudentManager` 和 `student_manager` 模块 |

## 使用方式

从课程目录运行：

```bash
python3 - <<'PY'
from solutions import Student, StudentManager

manager = StudentManager()
manager.add_student(Student("001", "张三", 20))
manager.add_student(Student("002", "李四", 25))

print(manager.get_student("001"))
print(manager.search_by_name("张"))
print(manager.get_statistics())
PY
```

也可以直接运行测试：

```bash
uv run pytest tests/ -q
```

## 设计说明

- `Student` 使用手动类定义（`__init__`、`__repr__`、`__eq__`、`to_dict`、`from_dict`），替代 `dataclass`。
- `Student.to_dict()` / `Student.from_dict()` 为后续 JSON 持久化预留边界。
- `StudentManager.students` 使用 `dict[str, Student]`，按学号查询比遍历列表更直接。
- `add_student()`、`remove_student()`、`update_student()` 使用 `bool` 表示业务操作是否成功。
- `list_students()` 返回列表副本，避免调用方直接持有内部 `dict_values` 视图。
- `search_by_name()` 支持部分匹配和大小写不敏感搜索。
- `get_statistics()` 对空管理器返回 0，避免除零错误。
