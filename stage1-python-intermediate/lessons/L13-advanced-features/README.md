# L13: Python 高级特性

> **课程编号**: L13
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 9 小时
> **核心内容**: 闭包、装饰器、装饰器工厂、上下文管理器、`contextlib`

---

## 🎯 课程定位

本课把函数和对象进一步提升为“可组合的行为单元”：用闭包封装状态，用装饰器横切增强函数，用上下文管理器可靠管理资源。它是后续描述符、异步上下文、测试夹具和 Web 框架中间件的基础。

完成本课后，你将能够：

- 解释闭包如何捕获外层作用域变量。
- 使用 `functools.wraps` 编写保留元数据的装饰器。
- 编写带参数的装饰器工厂，例如重试、验证、限流和缓存。
- 实现 `__enter__()` / `__exit__()` 上下文管理器，并理解异常传播语义。
- 使用 `contextlib.contextmanager`、`suppress`、`ExitStack`、`nullcontext` 管理资源。
- 将装饰器与上下文管理器用于日志、计时、事务、文件和资源清理。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L13-advanced-features

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_closures_decorators.py
python examples/02_context_managers.py

# 3) 完成练习并自检
python exercises/01_decorators.py
python exercises/02_context_managers.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 闭包与作用域 | `lesson.md` Part 1-2、`examples/01_closures_decorators.py` | 状态封装、`nonlocal`、函数工厂 |
| 2 | 装饰器基础 | Part 3-4、`exercises/01_decorators.py` | `@decorator`、`wraps`、返回 wrapper |
| 3 | 装饰器工厂 | Part 4、`solutions/solution_01_decorators.py` | 重试、校验、缓存、调用计数 |
| 4 | 上下文管理器协议 | Part 5-6、`examples/02_context_managers.py` | `__enter__`、`__exit__`、异常是否抑制 |
| 5 | contextlib | Part 7、`exercises/02_context_managers.py` | `@contextmanager`、资源清理、重定向输出 |
| 6 | 测试验证 | `tests/` | 16 个用例覆盖参考答案关键行为 |

---

## 📁 目录结构

| 目录 | 用途 |
| ---- | ---- |
| [examples/](examples/) | 可直接运行的示例：闭包/装饰器与上下文管理器 |
| [exercises/](exercises/) | 2 个动手练习：装饰器与上下文管理器 |
| [solutions/](solutions/) | 与测试对齐的参考答案，建议完成练习后再查看 |
| [tests/](tests/) | 16 个 pytest 用例，验证参考答案行为 |
| [lesson.md](lesson.md) | 完整教程与扩展说明 |

---

## ✅ 完成标准

- [ ] 能写出至少一个闭包，并解释它捕获了哪些变量。
- [ ] 能实现保留函数元数据的装饰器。
- [ ] 能实现带参数装饰器工厂，例如 `retry(max_attempts=3)`。
- [ ] 能实现类形式和 `@contextmanager` 形式的上下文管理器。
- [ ] 能说明 `__exit__()` 返回 `True` / `False` 对异常传播的影响。
- [ ] 本课测试通过：`uv run pytest stage1-python-intermediate/lessons/L13-advanced-features/tests -q`。

---

## 🧪 测试与检查

```bash
# 定向测试
uv run pytest stage1-python-intermediate/lessons/L13-advanced-features/tests -q

# 语法/导入层面检查
python -m py_compile   stage1-python-intermediate/lessons/L13-advanced-features/examples/*.py   stage1-python-intermediate/lessons/L13-advanced-features/exercises/*.py   stage1-python-intermediate/lessons/L13-advanced-features/solutions/*.py   stage1-python-intermediate/lessons/L13-advanced-features/tests/*.py
```

---

## 🔗 下一步

完成本课后继续学习：

- [L13: 描述符与属性](../L13-descriptors/README.md)
- L13 会继续深入对象属性访问协议，是理解 ORM、验证框架和属性管理的关键。
