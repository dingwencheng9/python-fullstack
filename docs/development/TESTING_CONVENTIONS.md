# Python 测试约定与最佳实践

> **文档层级**: L3 - 权威源
> **受众**: 贡献者、重构者
> **适用范围**: Python 3.13 全栈开发课程
> **更新频率**: 低（测试约定变更时）
> **最后更新**: 2026-06-28

**核心原则**: 项目专有测试规范权威源

---

## 📋 目录

1. [测试模块加载规范](#测试模块加载规范)
2. [Fixture 使用规范](#fixture-使用规范)
3. [测试文件组织](#测试文件组织)
4. [验证策略](#验证策略)
5. [常见反模式](#常见反模式)

---

## 测试模块加载规范

### ✅ 推荐：使用 importlib 物理路径加载

**适用场景**：加载非包结构的测试目标文件（如 lesson 独立项目）

```python
import importlib.util
from pathlib import Path
import pytest

@pytest.fixture
def sol():
    """加载 solutions_01 模块（使用 importlib 加载物理路径）"""
    solution_file = Path(__file__).parent.parent / "solutions" / "solutions_01.py"
    spec = importlib.util.spec_from_file_location("solutions_01", solution_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_something(sol):
    """测试函数通过 fixture 获取模块"""
    assert sol.some_function() == expected
    assert hasattr(sol, "SomeClass")
```

**核心原则**：

- ✅ 使用 `importlib.util.spec_from_file_location` + 物理路径
- ✅ 每个 lesson 目录视为独立项目，不依赖包结构或 `__init__.py`
- ✅ 通过 pytest fixture 注入模块，避免全局污染
- ✅ 路径使用 `Path(__file__).parent.parent / ...` 相对定位

### ❌ 禁止：污染 sys.path

**严禁在测试代码中使用**：

```python
# ❌ 错误示例 1：直接修改 sys.path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))
from solutions_01 import greet

# ❌ 错误示例 2：操纵 sys.modules
sys.modules.pop("old_module", None)

# ❌ 错误示例 3：重置 sys.path
sys.path[:] = original_path
```

**为什么禁止**：

1. **全局污染**：`sys.path` 是进程级全局变量，修改后影响所有后续导入
2. **测试顺序依赖**：批量测试时不同文件的修改相互影响
3. **缓存问题**：`sys.modules` 缓存可能导致旧版本模块被重用
4. **难以调试**：导入错误难以追溯到真实原因

### ⚠️ 例外：业务逻辑保留

以下情况的 `sys.path` / `sys.modules` 操作是**业务逻辑**，应保留：

```python
# ✅ 正确：有意的模块注入（用于测试）
sys.modules["py313_improvements"] = py313

# ✅ 正确：运行时环境检测
if "pytest" in sys.modules:
    # 测试环境特殊处理
    pass

# ✅ 正确：框架/库内部的合法使用
# （通常在 conftest.py 的 pytest 钩子中）
```

**判断标准**：

- 删除后测试全绿且功能不变 → **真污染**，必须删除
- 删除后测试失败 → 仔细分析是否为必要的**业务逻辑**

---

## Fixture 使用规范

### 模块加载 Fixture

```python
@pytest.fixture
def sol():
    """加载 solutions_01 模块"""
    solution_file = Path(__file__).parent.parent / "solutions" / "solutions_01.py"
    spec = importlib.util.spec_from_file_location("solutions_01", solution_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

### 异步环境 Fixture

```python
@pytest.fixture(scope="session")
def event_loop():
    """提供全局事件循环"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
```

### 数据库 Fixture

```python
@pytest.fixture
def db():
    """提供测试数据库会话"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
```

---

## 测试文件组织

### 标准目录结构

```
L{XX}-课程名/
├── solutions/           # 参考答案
│   ├── solutions_01.py
│   └── solutions_02.py
├── tests/               # 测试文件
│   ├── conftest.py      # Fixture 定义
│   ├── test_solutions_01.py
│   └── test_solutions_02.py
└── README.md
```

### conftest.py 职责

```python
"""测试配置与公共 Fixture"""

from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def event_loop():
    """全局事件循环（异步测试必需）"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sol():
    """通用模块加载 fixture（按需修改文件名）"""
    solution_file = Path(__file__).parent.parent / "solutions" / "solutions_01.py"
    spec = importlib.util.spec_from_file_location("solutions_01", solution_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

---

## 验证策略

### 渐进式验证原则（Progressive Verification）

**核心理念**：立即验证 → 快速反馈 → 精准定位

```bash
# ❌ 错误：修改 10 个文件后批量验证（失败时难以定位）
# ✅ 正确：修改 1 个文件立即验证（快速反馈循环）
```

### 三级验证层级

#### 1️⃣ 立即验证（单文件）

**时机**：修改完单个文件后立即运行

```bash
# 验证单个测试文件（~3-5 个测试，< 1 秒）
uv run pytest stage2-foundation/lessons/L24-async-programming/tests/test_solutions_01.py -v
```

**特点**：

- ⚡ 极快反馈（< 1 秒）
- 🎯 精准定位错误
- 🔄 支持快速迭代

#### 2️⃣ 模块验证（目录级）

**时机**：完成一个 lesson 目录后运行

```bash
# 验证整个 lesson 的所有测试（~10-20 个测试，< 5 秒）
uv run pytest stage2-foundation/lessons/L24-async-programming/tests/ -v
```

**特点**：

- 📦 验证模块完整性
- 🔗 检测跨文件交互问题
- ⚖️ 平衡速度与覆盖面

#### 3️⃣ 全量验证（CI 门禁）

**时机**：最终交付前运行

```bash
# 验证整个仓库（2091 个测试，~60 秒）
make ci-local
```

**特点**：

- 🛡️ 确保无回归
- 🏁 PR 前必跑
- 🔍 四件套门禁（ruff + mypy + mkdocs + pytest）

### 验证时机决策树

```
文件修改完成
    │
    ├─ 单文件修改？
    │   └─ YES → 立即验证（单文件测试）
    │       │
    │       ├─ PASS → 继续开发
    │       └─ FAIL → 立即修复
    │
    ├─ 完成一个 lesson？
    │   └─ YES → 模块验证（目录测试）
    │       │
    │       ├─ PASS → 继续下一个
    │       └─ FAIL → 检查跨文件交互
    │
    └─ 准备 PR？
        └─ YES → 全量验证（make ci-local）
            │
            ├─ PASS → 可以提交 PR
            └─ FAIL → 修复回归问题
```

---

## 常见反模式

### ❌ 反模式 1：批量修改后批量验证

```bash
# ❌ 错误做法
# 修改了 10 个文件
# 然后一次性跑全量测试
make ci-local  # 60 秒后发现第 3 个文件有问题
```

**问题**：

- 失败时难以定位是哪个文件导致
- 浪费大量验证时间
- 可能需要回溯多次修改

**正确做法**：

```bash
# ✅ 正确做法
# 修改文件 1 → 立即验证文件 1
uv run pytest path/to/test_file1.py -v

# 修改文件 2 → 立即验证文件 2
uv run pytest path/to/test_file2.py -v

# 所有文件修改完成 → 全量验证收尾
make ci-local
```

### ❌ 反模式 2：过度测试

```bash
# ❌ 错误：改一行代码就跑 2091 个测试
echo "# comment" >> file.py
make ci-local  # 浪费 60 秒
```

**问题**：

- 浪费大量 Token 和时间
- 降低开发效率

**正确做法**：

```bash
# ✅ 正确：只跑相关测试
echo "# comment" >> stage2-foundation/lessons/L24-async-programming/solutions/solutions_01.py
uv run pytest stage2-foundation/lessons/L24-async-programming/tests/ -v  # < 5 秒
```

### ❌ 反模式 3：忽略残留分类

```python
# ❌ 错误：看到 sys.modules 就删除
# 实际这是业务逻辑！
sys.modules["py313_improvements"] = py313  # 有意的模块注入

# ❌ 错误：看到 sys.path 就删除
# 实际这是运行时检测！
if "pytest" in sys.modules:  # 测试环境检测
    pass
```

**正确做法**：

1. 先删除怀疑的代码
2. 运行测试验证
3. 如果测试失败 → 仔细分析是否为业务逻辑
4. 如果测试通过 → 确认是真污染，提交删除

---

## 📚 参考资源

### 相关文档

- [CLAUDE.md](https://github.com/nexo/python313-fullstack/blob/main/CLAUDE.md) - 项目开发规范

### 示例代码

- [stage2-engineering/lessons/L19-async-programming/](../../stage2-engineering/lessons/L19-async-programming/) - importlib fixture 标准示例
- [stage2-engineering/lessons/L19-async-programming/tests/conftest.py](https://github.com/nexo/python313-fullstack/blob/main/stage2-engineering/lessons/L19-async-programming/tests/conftest.py) - 清理后的标准 conftest

---

**维护者**: Python 3.13 全栈课程团队

---

## 🔗 相关资源

- [CLAUDE.md](https://github.com/nexo/python313-fullstack/blob/main/CLAUDE.md) - 项目开发规范
- [LESSON_FORMAT_STANDARD.md](./LESSON_FORMAT_STANDARD.md) - 课程格式标准
