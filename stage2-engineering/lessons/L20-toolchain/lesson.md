# L20: 现代化工具链 - 从环境到生态

> **课程编号**: L20
> **所属阶段**: Stage 2 - 现代工程
> **预计时长**: 15-18 小时
> **难度**: ⭐⭐⭐⭐☆（中高级）
> **前置课程**: L04, L19
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

>
> 1. 理解脚本与工程的区别，掌握项目结构设计
> 2. 掌握 Git 工作流、约定式提交和协作开发流程
> 3. 掌握 uv 包管理器和虚拟环境管理
> 4. 掌握 Ruff、mypy、pytest 核心工具链
> 5. 理解 CI/CD 概念与 GitHub Actions 完整配置（详见 L19）

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L07**: 模块与包
- **L12**: 类型注解基础
- **L19**: Pytest 完整实战

**如果你还没有学习以上课程，建议先完成前置课程。**

---

## 📚 课程内容

## Part A: 从脚本到工程（2h）

### A.1 脚本 vs 工程的区别

**脚本的特点**：

- 一个 .py 文件解决所有问题
- 没有测试
- 没有项目结构
- 手动管理依赖

**工程的特点**：

- 清晰的项目结构（src/tests/docs）
- 自动化测试
- 依赖锁定
- CI/CD 自动化

### A.2 为什么需要工程化？

```python
# 脚本方式 - 单文件
import requests

def fetch_data(url):
    return requests.get(url).json()

data = fetch_data("https://api.example.com/users")
print(data)
```

**问题**：

1. 没有版本控制（Git）
2. 没有依赖管理（别人无法复现环境）
3. 没有测试（改了代码不知道是否破坏功能）
4. 没有项目结构（代码多了找不到）

### A.3 工程化第一步：项目结构

```
my_project/
├── src/               # 源代码
│   ├── __init__.py
│   ├── api.py
│   └── models.py
├── tests/             # 测试
│   ├── test_api.py
│   └── test_models.py
├── docs/              # 文档
│   └── README.md
├── pyproject.toml     # 项目配置
├── .gitignore         # Git 忽略文件
└── .env.example       # 环境变量模板
```

### A.4 项目结构选择：src-layout vs flat-layout

**src-layout**（推荐用于库/大型项目）：

```
my_project/
├── src/
│   └── my_package/     # 源码在 src/ 下
│       ├── __init__.py
│       └── core.py
├── tests/
├── pyproject.toml
└── README.md
```

**优点**:

- ✅ 防止意外导入未安装的包
- ✅ 强制以可安装方式测试（更接近用户实际安装方式）
- ✅ Python 生态主流（Django、FastAPI、Pydantic 都采用）

**flat-layout**（适合简单应用/微服务）：

```
my_project/
├── my_package/         # 源码直接在根目录
│   ├── __init__.py
│   └── core.py
├── tests/
├── pyproject.toml
└── README.md
```

**优点**:

- ✅ 导入路径短（`import my_package` vs `import src.my_package`）
- ✅ 适合 REST API、CLI 工具等非库项目
- ✅ 项目根目录结构更扁平

**选择建议**：

| 场景           | 推荐        | 理由               |
| -------------- | ----------- | ------------------ |
| Python 库/框架 | src-layout  | 安全隔离，标准化   |
| REST API 服务  | flat-layout | 简单直接，导入方便 |
| CLI 工具       | flat-layout | 减少嵌套层级       |
| Monorepo 多包  | src-layout  | 明确包边界         |
| 微服务         | flat-layout | 少即是多           |

---

## Part B: Git 工作流实战（3h）

### B.1 Git 基础

```bash
# 初始化仓库
git init

# 配置用户信息
git config user.name "Your Name"
git config user.email "your@email.com"

# 查看状态
git status

# 添加文件到暂存区
git add src/api.py

# 提交
git commit -m "feat: add API module"

# 查看历史
git log --oneline
```

### B.2 分支管理

```bash
# 创建并切换到新分支
git checkout -b feature/new-endpoint

# 查看所有分支
git branch -a

# 合并分支
git checkout main
git merge feature/new-endpoint
```

### B.3 约定式提交 (Conventional Commits)

统一的提交格式让团队协作更高效，还能自动生成 CHANGELOG。

**格式**：

```
<type>: <description>
```

**常用类型**：

| type       | 说明      | 示例                         |
| ---------- | --------- | ---------------------------- |
| `feat`     | 新功能    | `feat: 添加用户登录接口`     |
| `fix`      | Bug 修复  | `fix: 修复分页计算错误`      |
| `docs`     | 文档更新  | `docs: 补充 API 使用示例`    |
| `refactor` | 代码重构  | `refactor: 提取公共验证逻辑` |
| `test`     | 测试相关  | `test: 增加边界条件测试`     |
| `chore`    | 构建/工具 | `chore: 更新依赖到最新版`    |
| `ci`       | CI/CD     | `ci: 添加多平台测试矩阵`     |
| `perf`     | 性能优化  | `perf: 优化数据库查询`       |

### B.4 Code Review 流程与检查清单

Reviewer 检查清单：

**安全** 🔴:

- [ ] 无硬编码密钥（API Key、密码）
- [ ] 用户输入已校验（类型、长度、范围）
- [ ] SQL 使用参数化查询（无拼接）

**正确性** 🟡:

- [ ] 边界条件已处理（空列表、None、超大输入）
- [ ] 异常有明确的处理逻辑（非裸 except）
- [ ] 类型标注完整且正确

**可维护性** 🟢:

- [ ] 函数 < 50 行（职责单一）
- [ ] 变量名清晰（无 `x`, `tmp`, `data2`）
- [ ] 关键逻辑有注释说明"为什么"而非"做什么"

**测试** 🔵:

- [ ] 新功能有对应测试
- [ ] 测试覆盖主要路径 + 边界条件
- [ ] 现有测试全部通过

---

## Part C: uv 包管理器（2.5h）

### C.1 什么是 uv？

uv 是由 Astral 开发的极速 Python 包管理器，用 Rust 编写，比 pip 快 **10-20 倍**。

**uv vs pip 对比**：

| 特性     | pip              | uv             |
| -------- | ---------------- | -------------- |
| 速度     | 30-60秒          | 2-5秒 ⚡       |
| 依赖解析 | 较慢             | 极快           |
| 工具整合 | 分散             | 统一           |
| 配置文件 | requirements.txt | pyproject.toml |

**核心优势**:

- ⚡ 极速安装（2-5 秒 vs pip 的 30-60 秒）
- 🔒 依赖锁定（确保一致性）
- 🎯 单文件配置（pyproject.toml）
- 🌐 全局缓存（节省磁盘空间）

### C.2 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uv --version
```

### C.3 创建项目

```bash
# 1. 创建项目目录
mkdir ~/projects/my-first-project
cd ~/projects/my-first-project

# 2. 初始化项目
uv init

# 3. 创建虚拟环境（使用 Python 3.13）
uv venv --python 3.13

# 4. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux

# 5. 验证 Python 版本
python --version  # 应显示 Python 3.13.x
```

### C.4 管理依赖

```bash
# 添加生产依赖
uv add fastapi uvicorn

# 添加开发依赖
uv add --dev pytest ruff mypy

# 安装所有依赖
uv sync

# 查看已安装的包
uv pip list
```

### C.5 uv 常用命令速查

| 命令        | 作用          | 替代                   |
| ----------- | ------------- | ---------------------- |
| `uv init`   | 初始化项目    | —                      |
| `uv add`    | 添加依赖      | pip install            |
| `uv remove` | 移除依赖      | pip uninstall          |
| `uv sync`   | 同步依赖      | pip install -r req.txt |
| `uv lock`   | 生成/更新锁定 | pip freeze             |
| `uv run`    | 在环境中运行  | source venv + python   |
| `uv build`  | 构建包        | python -m build        |
| `uv venv`   | 创建虚拟环境  | python -m venv         |

---

## Part D: Ruff - 极速代码质量工具（3h）

### D.1 什么是 Ruff？

Ruff 是用 Rust 编写的极速 Python 代码检查和格式化工具。

**核心优势**:

- ⚡ 极快（比 Black 快 10-100 倍）
- 🎯 All-in-One（格式化 + Linting）
- 🔧 易配置（pyproject.toml）
- 🌟 兼容 Black、isort、Flake8

### D.2 安装和基础使用

```bash
# 安装 Ruff
uv add --dev ruff

# 查看版本
ruff --version

# 格式化代码
ruff format src/

# 检查代码
ruff check src/

# 自动修复
ruff check --fix src/
```

### D.3 配置 Ruff

**pyproject.toml**:

```toml
[tool.ruff]
target-version = "py313"
line-length = 100

# 选择检查规则
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "W",    # pycodestyle warnings
]

# 忽略特定规则
ignore = ["E501"]  # 行长度由 formatter 处理

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # 允许 __init__.py 中的未使用导入
```

---

## Part E: mypy - 静态类型检查（3h）

### E.1 什么是 mypy？

mypy 是 Python 的静态类型检查器，在代码运行前发现类型错误。

**核心优势**:

- 🐛 提前发现类型错误
- 📖 提高代码可读性
- 🔧 增强 IDE 支持
- ✅ 大型项目必备

### E.2 基础类型注解

```python
# 基本类型
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 数字类型
def add(a: int, b: int) -> int:
    return a + b

# 布尔类型
def is_valid(value: str) -> bool:
    return len(value) > 0

# None 类型
def log(message: str) -> None:
    print(message)
```

### E.3 复杂类型

```python
# Python 3.10+ 现代语法（推荐）

# 列表
def get_numbers() -> list[int]:
    return [1, 2, 3]

# 字典
def get_user() -> dict[str, str]:
    return {"name": "Alice", "email": "alice@example.com"}

# 可选值
def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Alice"
    return None

# 联合类型
def process(value: str | int) -> str:
    return str(value)
```

> ⚠️ **旧式语法兼容**：如果你需要支持 Python 3.9 或更早版本，可以使用 `from typing import List, Dict, Optional, Union`，但新代码建议使用上述现代语法。

### E.4 mypy 严格模式

**pyproject.toml**:

```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
warn_unused_ignores = true
```

### E.5 运行 mypy

```bash
# 检查单个文件
mypy src/main.py

# 检查整个目录
mypy src/

# 查看详细报告
mypy --show-error-codes src/
```

---

## Part F: pytest 深入（2h）

### F.1 编写第一个测试

**src/calculator.py**:

```python
def add(a: int, b: int) -> int:
    """加法"""
    return a + b


def subtract(a: int, b: int) -> int:
    """减法"""
    return a - b
```

**tests/test_calculator.py**:

```python
from src.calculator import add, subtract


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0
```

### F.2 运行测试

```bash
# 运行所有测试
pytest

# 详细输出
pytest -v

# 查看覆盖率
pytest --cov=src tests/

# 生成覆盖率报告
pytest --cov=src --cov-report=html tests/
```

### F.3 pytest 配置

**pyproject.toml**:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]
```

---

## Part G: Git 进阶操作（2h）

### G.1 git rebase — 变基操作

rebase 将提交历史"变基"到另一个分支上，使历史更线性：

```bash
# 将 feature 分支变基到 main
git checkout feature
git rebase main

# 或者用 merge base 变基（更安全）
git rebase --onto main feature~3 feature
```

**交互式 rebase（压缩历史）**：

```bash
# 修改最近 3 个提交
git rebase -i HEAD~3

# 在编辑界面中，可以：
# - pick  → 保留提交
# - squash → 合并到上一个提交
# - drop  → 删除提交
# - reword → 修改提交信息
```

**使用场景**：
- 保持提交历史整洁
- 在合并前更新功能分支
- 压缩多个"工作进度"提交为一个有意义的提交

**⚠️ 注意**：不要对已推送到远程的提交执行 rebase！

### G.2 merge vs rebase — 何时用哪个

| 操作    | 适用场景           | 特点             |
| ------- | ------------------ | ---------------- |
| merge   | 团队协作、保留完整历史 | 保留所有分支历史，产生 merge commit |
| rebase  | 个人分支、保持线性历史 | 重写历史，历史更清晰 |

**建议**：
- 公共分支（main）永远使用 merge
- 个人功能分支使用 rebase 保持线性
- PR 合并时用 Squash and Merge 压缩历史

### G.3 git cherry-pick — 选择性应用提交

cherry-pick 允许选择性地应用某个提交，而不合并整个分支：

```bash
# 应用单个提交
git cherry-pick abc123

# 应用多个提交
git cherry-pick abc123 def456

# 应用并继续（处理冲突后）
git cherry-pick --continue

# 撤销 cherry-pick
git cherry-pick --abort
```

**使用场景**：
- 需要 backport 修复到旧版本分支
- 误删的提交需要恢复
- 部分功能需要跨分支复用

### G.4 git reflog — 误操作恢复

reflog 记录所有 HEAD 移动历史，可用于恢复误操作的提交：

```bash
# 查看 reflog
git reflog

# 输出示例：
# abc123 HEAD@{0}: commit: feat: add feature X
# def456 HEAD@{1}: rebase: 修复冲突
# ghi789 HEAD@{2}: checkout: 从 main 切换

# 恢复到指定位置
git checkout HEAD@{2}

# 基于 reflog 恢复分支
git branch recovery-branch HEAD@{5}
```

**⚠️ 注意**：reflog 默认有效期 90 天（未引用后），可使用 `git reflog expire` 清理。

### G.5 git bisect — 二分查找 Bug

bisect 使用二分查找快速定位引入 bug 的提交：

```bash
# 开始二分查找
git bisect start

# 标记已知好的提交
git bisect good v1.0.0

# 标记已知坏的提交（当前版本）
git bisect bad HEAD

# Git 自动 checkout 中间版本，测试后标记
git bisect good  # 或 git bisect bad

# 找到后自动显示第一个坏的提交
# 结束 bisect
git bisect reset
```

**自动化 bisect**：

```bash
# 使用测试脚本自动判断
git bisect start
git bisect good v1.0.0
git bisect bad HEAD
git bisect run pytest tests/test_feature.py
```

### G.6 git stash — 临时保存工作区

stash 临时保存未提交的修改，切换分支时不丢失工作：

```bash
# 保存当前修改
git stash

# 保存并添加描述
git stash push -m "WIP: 新功能开发中"

# 查看 stash 列表
git stash list
# 输出：stash@{0}: WIP: 新功能开发中
#      stash@{1}: On main: feat: add feature X

# 恢复最新 stash
git stash pop

# 恢复指定 stash
git stash apply stash@{1}

# 删除 stash
git stash drop stash@{0}

# 清空所有 stash
git stash clear
```

**进阶用法**：

```bash
# stash 包含未跟踪文件（新增文件）
git stash -u

# stash 保留暂存区内容
git stash -k

# 查看 stash 内容
git stash show -p stash@{0}
```

### G.7 Git 进阶操作速查

| 命令                              | 作用                     |
| --------------------------------- | ------------------------ |
| `git rebase -i HEAD~3`            | 交互式压缩最近 3 个提交   |
| `git cherry-pick abc123`          | 选择性应用某个提交       |
| `git reflog`                      | 查看所有 HEAD 历史       |
| `git bisect start`                | 开始二分查找 bug         |
| `git stash`                       | 临时保存工作区           |
| `git stash pop`                   | 恢复并删除 stash         |

---

## 💻 实践练习

### 练习 1: 创建项目 (基础 - 30min)

**任务**: 创建一个新的 Python 项目，配置开发环境

```bash
mkdir ~/practice/ex01-setup
cd ~/practice/ex01-setup
uv init
uv venv --python 3.13
source .venv/bin/activate
uv add fastapi
uv add --dev pytest ruff mypy
```

### 练习 2: 配置工具链 (中级 - 1h)

**任务**: 配置 pyproject.toml，实现 Python 3.13 现代化环境

### 练习 3: Git 协作演练 (中高级 - 1h)

**任务**: 模拟一次完整的 PR 流程

### 练习 4: Ruff + mypy + pytest 集成 (高级 - 1.5h)

**任务**: 为代码添加类型注解、格式化、编写测试

---

## 🎓 知识检查

### 选择题

1. **uv 比 pip 快多少倍？**
   - C. 10-20 倍 ✅

2. **Ruff 比 Black 快多少倍？**
   - C. 10-100 倍 ✅

3. **约定式提交中 `feat:` 前缀表示？**
   - B. 新功能 ✅

4. **mypy 在什么时候检查类型？**
   - C. 开发时（静态检查）✅

---

## 📖 扩展阅读

1. **uv 官方文档**: https://docs.astral.sh/uv/
2. **Ruff 文档**: https://docs.astral.sh/ruff/
3. **mypy 文档**: https://mypy.readthedocs.io/
4. **pytest 文档**: https://docs.pytest.org/
5. **GitHub Actions 文档**: https://docs.github.com/en/actions

---

## ✅ 学习检查清单

完成本课程后，确认你已经：

- [ ] 理解了脚本与工程的区别
- [ ] 掌握了 Git 工作流、约定式提交
- [ ] 掌握了 Git 进阶操作（rebase、cherry-pick、reflog、bisect、stash）
- [ ] 掌握了 uv 包管理器
- [ ] 掌握了 Ruff、mypy、pytest 工具链
- [ ] 理解了 CI/CD 概念与工具链在 CI 中的角色
- [ ] 完成了所有实践练习
- [ ] 通过了知识检查

> 📚 **GitHub Actions 完整配置**：参见 [L19 Pytest完整实战](../L19-pytest-complete/lesson.md) 第二部分（CI/CD 自动化集成）

---

## 🔗 下一步

[L19: 异步编程核心](../L19-async-programming/README.md)
