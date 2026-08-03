# L10: Python 类型系统完整指南

> **课程编号**: L10
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 6 小时
> **前置课程**: L04 函数与模块, L06 文件操作
> **核心内容**: 类型注解、Union/Optional、Callable、Protocol、PEP 695 泛型、TypedDict、mypy

---

## 🎯 课程定位

本课是 Stage 1 的入口课程：把 Stage 0 中“能运行的 Python 代码”升级为“可被 IDE、类型检查器和团队协作流程理解的 Python 代码”。

完成本课后，你将能够：

- 为变量、函数、容器和类添加清晰的类型注解。
- 使用 `T | None`、`TypeGuard` 和 `isinstance()` 做类型收窄。
- 用 `Callable` 描述回调、装饰器和高阶函数。
- 用 `Protocol` 设计结构化接口，理解 duck typing 与静态类型的结合。
- 使用 PEP 695 泛型语法（Python 3.12 引入并在 3.13 广泛应用）：`class Box[T]`、`def first[T]()`、`type Alias = ...`。本课程使用 Python 3.13 基线运行，示例兼容 3.12+。
- 使用 `TypedDict` + `Unpack` 描述 API/配置字典与类型安全的 `**kwargs`。
- 初步理解 mypy 在工程中的作用与配置方式。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L10-type-system

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_type_hints_basics.py
python examples/02_protocol.py
python examples/03_pep695_generics.py
python examples/04_callable_types.py
python examples/05_type_narrowing.py
python examples/07_typeddict.py

# 3) 完成练习并自检
python exercises/01_type_narrowing.py
python exercises/02_protocol.py
python exercises/03_generic_constraints.py

# 4) 运行单元测试
uv run pytest tests -q
```

> 注：PEP 695 泛型语法由 Python 3.12 引入（Python 3.13 广泛应用），示例使用 Python 3.13 基线运行，兼容 3.12+。

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 类型注解基础 | `lesson.md` Part 1-3、`examples/01_type_hints_basics.py` | 函数签名、容器类型、类型别名 |
| 2 | Callable 与高阶函数 | Part 4、`examples/04_callable_types.py` | 回调、装饰器、参数规格 |
| 3 | Protocol | Part 5、`examples/02_protocol.py` | 结构化子类型、`@runtime_checkable` |
| 4 | PEP 695 泛型 | Part 6、`examples/03_pep695_generics.py` | 新式泛型函数/类/类型别名 |
| 5 | TypeGuard 与类型收窄 | `examples/05_type_narrowing.py`、练习 1 | `isinstance()`、自定义类型守卫 |
| 6 | TypedDict 与 kwargs | Part 7、`examples/07_typeddict.py` | API/配置字典建模 |
| 7 | mypy 与测试 | Part 8、`tests/` | 静态检查与运行时行为的边界 |

---

## 📁 目录结构

| 目录 | 用途 |
| ---- | ---- |
| [examples/](examples/) | 可直接运行的主题示例，覆盖基础类型、Protocol、PEP 695、Callable、TypeGuard、TypedDict |
| [exercises/](exercises/) | 3 个动手练习：类型收窄、Protocol、泛型约束 |
| [solutions/](solutions/) | 与测试对齐的参考答案，建议完成练习后再查看 |
| [tests/](tests/) | 18 个 pytest 用例，验证参考答案的关键行为 |
| [lesson.md](lesson.md) | 完整教程与扩展说明 |

---

## ✅ 完成标准

- [ ] 能独立解释 `list[str]`、`dict[str, object]`、`T | None`、`Callable[[A], B]` 的含义。
- [ ] 能写出至少一个 `TypeGuard` 函数并用它收窄类型。
- [ ] 能定义一个 `Protocol`，并说明静态结构化类型与运行时 `isinstance()` 检查的区别。
- [ ] 能用 PEP 695 语法编写泛型函数、泛型类和类型别名。
- [ ] 能用 `TypedDict` 描述结构化字典，并知道它主要服务于静态检查。
- [ ] 本课测试通过：`uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q`。

---

## 🧪 测试与静态检查

```bash
# 定向测试
uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q

# 语法/导入层面检查
python -m py_compile \
  stage1-python-intermediate/lessons/L10-type-system/examples/*.py \
  stage1-python-intermediate/lessons/L10-type-system/exercises/*.py \
  stage1-python-intermediate/lessons/L10-type-system/solutions/*.py \
  stage1-python-intermediate/lessons/L10-type-system/tests/*.py
```

如果你安装了 mypy，可进一步运行：

```bash
uv run mypy stage1-python-intermediate/lessons/L10-type-system/solutions
```

---

## 🔗 下一步

完成本课后继续学习：

- [L11: 迭代器与生成器](../L11-generators/README.md)
- 后续 Stage 2 将把类型注解接入 pytest、ruff、mypy 和真实工程项目。
