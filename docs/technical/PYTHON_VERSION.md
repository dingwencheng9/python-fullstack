# Python 版本兼容性说明

> **文档层级**: L3 - 权威源
> **受众**: 所有开发者
> **适用范围**: Python 3.13/3.14 版本
> **更新频率**: 极低（Python 版本升级时）
> **最后更新**: 2026-06-28

**核心原则**: Python 版本要求、PEP 归属的唯一权威源

---

## 📋 快速导航

1. [版本要求](#版本要求)
2. [PEP 版本归属（关键）](#pep-版本归属关键)
3. [Python 3.13 新特性](#python-313-新特性)
4. [Python 3.14 新特性](#python-314-新特性)
5. [安装指南](#安装-python-313314)
6. [常见问题](#常见问题)

---

## 🎯 课程支持的 Python 版本

本课程全面支持 **Python 3.13** 和 **Python 3.14** 版本：

- **Python 3.13**：课程基线版本，所有课程内容均基于此版本开发，兼容性最成熟
- **Python 3.14**：试验性补充版本，包含 PEP 649（延迟注解）、PEP 750（t-string）、PEP 779（free-threading 官方支持）等新特性。Free-threading 需要单独的 `python3.14t` 构建（详见 [FREE_THREADING_TRUTH.md](./FREE_THREADING_TRUTH.md)）

## 版本要求

> 💡 **课程基线**: Python 3.13 是本课程的标准版本，所有课程和测试均基于此版本开发。
>
> 虽然 PEP 695 语法在 Python 3.12 即可使用，但为保证完整体验和最佳性能，**强烈推荐使用 Python 3.13+**。

| Stage                      | 最低版本 | 推荐版本 | 说明                                                 |
| -------------------------- | -------- | -------- | ---------------------------------------------------- |
| Stage 0: Basics            | 3.12     | 3.13     | 使用 PEP 695 类型参数语法                            |
| Stage 1: Intermediate      | 3.12     | 3.13     | 使用 PEP 695 类型参数语法                            |
| Stage 2: Foundation        | 3.12     | 3.13     | 使用 PEP 695 + asyncio 改进                          |
| Stage 3: Web APIs          | 3.12     | 3.13     | FastAPI + Pydantic V2                                |
| Stage 4: Data Intelligence | 3.12     | 3.13     | pandas + SQLAlchemy 2.0                              |
| Stage 5: AI Agent          | 3.12     | 3.13     | LangGraph + MCP                                      |
| Free-threading 课程        | 3.13t    | 3.14t    | 需要独立的 `*t` 构建（详见 FREE_THREADING_TRUTH.md） |

**相关文档**: [CLAUDE.md Python 版本事实规则](https://github.com/nexo/python313-fullstack/blob/main/CLAUDE.md#-python-版本事实规则)

---

## 📊 PEP 版本归属（关键）

> ⚠️ **常见误区纠正**: 本表格是课程中 PEP 归属的唯一权威源，避免版本漂移错误。

| PEP         | 标题                    | 引入版本        | 课程使用版本 | 说明                                          |
| ----------- | ----------------------- | --------------- | ------------ | --------------------------------------------- |
| **PEP 695** | 类型参数语法            | **Python 3.12** | Python 3.13  | ⚠️ **不是** 3.13 引入！课程在 3.13 基线下使用 |
| **PEP 692** | TypedDict Unpack        | Python 3.11     | Python 3.13  | —                                             |
| **PEP 703** | 可选 GIL（试验性）      | Python 3.13     | Python 3.13t | Free-threading 试验性支持                     |
| **PEP 779** | Free-threading 官方支持 | Python 3.14     | Python 3.14t | 仍需独立构建，不是默认                        |
| **PEP 649** | 延迟评估注解            | Python 3.14     | Python 3.14  | —                                             |
| **PEP 750** | t-string                | Python 3.14     | Python 3.14  | —                                             |

**关键说明**:

- ✅ **PEP 695 是 Python 3.12 引入的**，不是 3.13
- ✅ 课程使用 Python 3.13 作为基线，但使用的是 3.12 引入的 PEP 695 语法
- ❌ 禁止写"PEP 695 是 Python 3.13 新特性"（常见错误）
- ❌ 禁止写"Python 3.13 引入 PEP 695"（常见错误）

**相关文档**: [FREE_THREADING_TRUTH.md](FREE_THREADING_TRUTH.md) - PEP 703/779 详细说明

---

## Python 3.13 新特性

本课程使用的 Python 3.13 新特性：

### PEP 695: 类型参数语法

> ⚠️ **重要说明**: PEP 695 实际上是 **Python 3.12** 引入的特性，但本课程基于 Python 3.13。
> 课程代码使用此语法，因此要求 Python 3.12+ 才能运行，但**推荐使用 Python 3.13** 作为课程基线版本。

**Python 3.12+:**

```python
class Component[T]:
    def __init__(self, props: T) -> None:
        self.props = props

class Repository[T]:
    def __init__(self) -> None:
        self._storage: dict[int, T] = {}
```

**Python 3.9-3.12 兼容写法:**

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Component(Generic[T]):
    def __init__(self, props: T) -> None:
        self.props = props

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._storage: dict[int, T] = {}
```

### PEP 692: TypedDict 的 Unpack

**Python 3.13+:**

```python
from typing import TypedDict, Unpack

class Person(TypedDict):
    name: str
    age: int

def greet(**kwargs: Unpack[Person]) -> str:
    return f"Hello {kwargs['name']}, age {kwargs['age']}"
```

### 其他改进

- **性能提升**: Python 3.13 比 3.12 快约 5%
- **更好的错误消息**: 更清晰的类型错误提示
- **f-string 改进**: 支持更复杂的表达式

## Python 3.14 新特性

本课程中使用的 Python 3.14 新特性：

### Free-threading（无 GIL）模式

> ⚠️ **所有 free-threading 命令、安装、兼容性以 [FREE_THREADING_TRUTH.md](./FREE_THREADING_TRUTH.md) 为唯一权威源。**
>
> 本文档仅说明 free-threading 与课程版本的关系，不重复命令细节。

### PEP 649: 延迟评估注解

**Python 3.14+:**

```python
# 无需 `from __future__ import annotations`
class Tree:
    def get_child(self) -> Tree:  # 前向引用自动处理
        ...
```

### 其他改进

- **性能提升**: Python 3.14 比 3.13 快约 5-15%
- **Free-threading 稳定性提升**: 大幅改善 C 扩展兼容性
- **JIT 编译器优化**: 实验性 JIT 编译器性能进一步提升
- **标准库改进**: 优化了 `pathlib`、`datetime` 等模块

## 使用 Python 3.13/3.14 特性的文件

以下文件使用 Python 3.13/3.14 特性，提供了兼容版本：

| 文件                                          | 兼容版本                    | 说明         |
| --------------------------------------------- | --------------------------- | ------------ |
| 03-web-frontend/examples/generics_frontend.py | generics_frontend_compat.py | 前端泛型示例 |
| 04-web-backend/examples/generics_backend.py   | generics_backend_compat.py  | 后端泛型示例 |

**注意**: 兼容版本文件需要手动创建（可选）。

## 安装 Python 3.13/3.14

### 推荐方式

**uv（推荐）**：

```bash
uv python install 3.13
uv python install 3.14
```

**系统包管理器**：

- macOS: `brew install python@3.13`
- Ubuntu: `sudo apt install python3.13`（需 deadsnakes PPA）
- Windows: 访问 [python.org](https://www.python.org/downloads/)

**pyenv（多版本管理）**：

```bash
pyenv install 3.13.0
pyenv global 3.13.0
```

> 详细安装步骤见 [QUICKSTART.md - 前置要求](https://github.com/nexo/python313-fullstack/blob/main/QUICKSTART.md)

## 检查 Python 版本

```bash
# 检查默认 Python 版本
python3 --version

# 检查 Python 3.13
python3.13 --version

# 检查 Python 3.14
python3.14 --version

# 在脚本中检查版本
python3 -c "import sys; print(sys.version_info)"
```

## 虚拟环境

推荐使用 **uv**（最快）：

```bash
uv venv --python 3.13    # 创建 Python 3.13 虚拟环境
source .venv/bin/activate  # 激活（macOS/Linux）
```

或使用标准 **venv**：

```bash
python3.13 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

> 详细环境配置见 [QUICKSTART.md - 步骤 2](https://github.com/nexo/python313-fullstack/blob/main/QUICKSTART.md)

## 兼容性建议

### 如果必须使用 Python 3.9-3.12

1. **避免使用 PEP 695 语法**
   - 使用 `Generic[T]` 和 `TypeVar` 代替 `class Component[T]`

2. **使用类型检查工具**

   ```bash
   pip install mypy
   mypy --python-version 3.9 your_file.py
   ```

3. **测试兼容性**
   ```bash
   # 使用 tox 测试多个 Python 版本
   pip install tox
   tox
   ```

### 推荐的开发环境

- **Python 版本**: 3.14+
- **包管理器**: uv 或 pip
- **虚拟环境**: venv 或 virtualenv
- **类型检查**: mypy
- **代码格式化**: ruff 或 black
- **代码检查**: ruff 或 pylint

## 常见问题

### Q: 我的系统只有 Python 3.11，可以学习这门课程吗？

A: **不可以**。课程代码使用 PEP 695 类型参数语法（Python 3.12 引入），Python 3.11 会报 `SyntaxError`。

**必须升级到 Python 3.12+ 才能运行课程代码**，但强烈推荐 Python 3.13（课程基线版本）。

### Q: Python 3.12 和 3.13 有什么区别？为什么推荐 3.13？

A: 虽然 Python 3.12 支持 PEP 695 语法，但 Python 3.13 是课程的**标准基线版本**，原因：

1. ✅ **测试保证**: 所有 2036 个教学测试基于 3.13 运行
2. ✅ **性能提升**: 3.13 比 3.12 快约 5%
3. ✅ **错误信息**: 3.13 的类型错误提示更清晰
4. ✅ **Free-threading**: L26 Free-threading 课程需要 3.13t 构建

### Q: 课程代码在 Python 3.14 上能运行吗？

A: 可以。Python 3.14 向后兼容 3.13。课程代码在 3.14 上运行正常。

**注意**: Free-threading 相关特性需使用 `python3.14t` 独立构建（详见 [FREE_THREADING_TRUTH.md](FREE_THREADING_TRUTH.md)）。

### Q: 如何检查代码是否兼容特定 Python 版本？

A: 使用 vermin 工具：

```bash
pip install vermin
vermin --target=3.9 your_file.py
```

## 参考资料

- [Python 3.13 新特性](https://docs.python.org/3.13/whatsnew/3.13.html)
- [Python 3.14 新特性](https://docs.python.org/3.14/whatsnew/3.14.html)
- [PEP 695 - 类型参数语法](https://peps.python.org/pep-0695/)
- [PEP 649 - 延迟评估注解](https://peps.python.org/pep-0649/)
- [Python 版本支持策略](https://devguide.python.org/versions/)
- [pyenv 文档](https://github.com/pyenv/pyenv)
- [uv 文档](https://github.com/astral-sh/uv)

---

## 🔗 相关资源

- [Free-threading 权威源](FREE_THREADING_TRUTH.md) - Free-threading 详细说明
- [课程架构](https://github.com/nexo/python313-fullstack/blob/main/COURSE_MAPPING.md) - 课程体系架构

---

**最后更新**: 2026-06-28
**维护者**: Python 3.13/3.14 全栈课程团队
