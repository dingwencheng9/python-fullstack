# L22: 装饰器深度探索

> **课程编号**: L22
> **所属阶段**: Stage 2 - 工程化进阶
> **预计时长**: 8 小时
> **难度**: ⭐⭐⭐☆☆ (中级)
> **前置课程**: L14 装饰器进阶
> **Python 版本**: 3.13+

---

## 🎯 学习目标

通过本课程，你将能够：

1. **理解装饰器本质**：掌握闭包、高阶函数、`@` 语法糖与函数对象元信息。
2. **实现函数装饰器**：编写计时、日志、调用计数、类型验证和缓存装饰器。
3. **实现参数化装饰器**：掌握三层嵌套、重试、超时、限流、权限验证和可选参数装饰器。
4. **使用类实现装饰器**：理解 `__call__`、实例状态、类装饰器和方法注入。
5. **组合工程化装饰器**：实现装饰器链、条件装饰、事务、性能监控、令牌桶限流和异步装饰器。
6. **结合 Python 3.13 类型实践**：阅读 PEP 695 泛型装饰器示例，并理解 `ParamSpec`/返回类型保留思路。

---

## 📚 课程模块

| 模块 | 主题 | 重点 |
| --- | --- | --- |
| 1 | 装饰器基础 | 闭包、`functools.wraps`、函数元信息 |
| 2 | 参数化装饰器 | 装饰器工厂、重试、TTL 缓存、权限验证 |
| 3 | 类装饰器 | `__call__`、单例、类级状态、方法注入 |
| 4 | 装饰器进阶 | 装饰器链、条件装饰、组合器 |
| 5 | 实战应用 | 性能监控、事务、限流、异步重试 |
| 6 | Python 3.13 特性 | PEP 695 泛型装饰器、异步装饰器测试 |

---

## 🚀 快速开始

### 前置要求

- 已完成 Stage 1 的函数、闭包、类和上下文管理基础。
- 已完成 [L18: 工具链生态](../L18-toolchain/README.md) 与 [L19: 异步编程核心](../L19-async-programming/README.md)。
- 使用 Python 3.13+ 与项目统一的 `uv` 环境。

### 常用命令

从仓库根目录运行：

```bash
# 课程结构与关键模块验证
uv run python stage2-engineering/lessons/L20-decorators/verify.py

# 运行单元测试
uv run pytest stage2-engineering/lessons/L20-decorators/tests -q

# 运行代表性示例
uv run python stage2-engineering/lessons/L20-decorators/examples/demo_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/examples/python313_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/examples/async_decorators_modern.py

# 运行练习自检
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_01_basic_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_02_parameterized_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_03_class_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_04_basic_practice.py
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_05_advanced_decorators.py
uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_06_practical_decorators.py
```

---

## 📂 课程结构

```text
L20-decorators/
├── README.md
├── lesson.md
├── pyproject.toml
├── verify.py
├── examples/
│   ├── 01_detailed_basics.py
│   ├── 06_practical_decorators.py
│   ├── async_decorators_modern.py
│   ├── demo_decorators.py
│   └── python313_decorators.py
├── exercises/
│   ├── exercise_01_basic_decorators.py
│   ├── exercise_02_parameterized_decorators.py
│   ├── exercise_03_class_decorators.py
│   ├── exercise_04_basic_practice.py
│   ├── exercise_05_advanced_decorators.py
│   └── exercise_06_practical_decorators.py
├── solutions/
│   ├── solution_01_basic_decorators.py
│   ├── solution_02_parameterized_decorators.py
│   ├── solution_03_class_decorators.py
│   ├── solution_04_advanced_decorators.py
│   └── solution_05_practical_decorators.py
└── tests/
    ├── test_async_decorators.py
    ├── test_python313_features.py
    ├── test_solutions_01_basic_decorators.py
    ├── test_solutions_02_parameterized_decorators.py
    ├── test_solutions_03_class_decorators.py
    ├── test_solutions_04_advanced_decorators.py
    └── test_solutions_05_practical_decorators.py
```

---

## 🧪 完成标准

- [ ] 阅读 `lesson.md` 并理解装饰器从闭包到类装饰器的演进。
- [ ] 运行 `verify.py` 成功。
- [ ] 完成并运行 6 个练习脚本自检。
- [ ] 通过 `tests/` 下全部测试。
- [ ] 能解释为什么 `functools.wraps` 对测试、调试和文档很重要。
- [ ] 能区分同步装饰器、异步装饰器和类装饰器的适用场景。

---

## 📖 参考资源

- [PEP 318 - Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)
- [Python Decorators](https://docs.python.org/3/glossary.html#term-decorator)
- [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)
- [collections.abc.Callable](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [asyncio.TaskGroup](https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup)

---

## 🔗 下一步

完成本课后继续学习：

- [L23: Python 新特性与版本迁移](../L23-python-new-features/README.md)

> 📖 **学习路径提示**：L23 将学习 Python 3.13+ 的新特性和版本迁移。
