# examples/ - L10 示例代码

这些示例用于把 `lesson.md` 中的类型系统概念转成可运行代码。建议按编号顺序执行，并主动修改输入观察类型提示与运行时行为的差异。

```bash
cd stage1-python-intermediate/lessons/L10-type-system
python examples/01_type_hints_basics.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_type_hints_basics.py` | 基础类型提示、Union/Optional、类型别名、旧式泛型类 | 类型注解不会自动做运行时校验 |
| `02_protocol.py` | Protocol、结构化子类型、泛型 Protocol | `@runtime_checkable` 只检查结构，不检查完整签名类型 |
| `03_pep695_generics.py` | PEP 695 泛型函数/类/类型别名/约束 | Python 3.12+ 新语法，适合 Python 3.13 课程主线 |
| `04_callable_types.py` | Callable、高阶函数、装饰器、参数规格 | 回调签名如何在类型系统中表达 |
| `05_type_narrowing.py` | `isinstance()`、`TypeGuard`、运行时 Protocol 检查 | 使用 `@runtime_checkable` 才能做 `isinstance(protocol)` |
| `07_typeddict.py` | `TypedDict`、`NotRequired`、`Unpack[TypedDict]` | 结构化字典更适合 API/配置，不等于业务对象 |

> 当前没有 `06_*.py`：TypedDict 示例从历史扩展中保留为 `07_typeddict.py`。文档按实际文件名导航。

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
