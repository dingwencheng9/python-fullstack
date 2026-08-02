# solutions/ - L10 参考答案

> ⚠️ 建议先独立完成 `exercises/`，再查看本目录。参考答案侧重“可读、可测、与课程概念一一对应”，不追求复杂技巧。

## 文件清单

| 文件 | 内容 |
| ---- | ---- |
| `solution_01_type_narrowing.py` | `TypeGuard` 示例：字符串列表、字典列表验证与字符串过滤 |
| `solution_02_protocol.py` | `Drawable` / `Resizable` Protocol，以及 `Circle` / `Square` 的结构化实现差异 |
| `solution_03_generic_constraints.py` | `Container[T]`、`NumberBox[int|float]` 与同类型容器合并 |
| `__init__.py` | 标识 solutions 包，供测试按物理路径加载 |

## 设计说明

- `solution_01_type_narrowing.py` 使用 `all(isinstance(...))` 展示类型守卫的典型写法；空列表会被视为满足 `list[str]`，这与 Python 的 `all([]) is True` 一致。
- `solution_02_protocol.py` 对 `Drawable` / `Resizable` 添加 `@runtime_checkable`，使测试可以用 `isinstance()` 演示运行时结构检查。
- `solution_03_generic_constraints.py` 在 `NumberBox` 构造函数中保留运行时数值检查，强调“静态类型提示不能替代边界输入校验”。

## 验证

```bash
uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q
```
