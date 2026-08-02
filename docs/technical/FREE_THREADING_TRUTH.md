# Python Free-threading 事实手册

> **文档层级**: L3 - 权威源
> **受众**: 所有开发者
> **适用范围**: Python 3.13/3.14 free-threading
> **更新频率**: 极低（Python 版本升级时）
> **最后更新**: 2026-06-28

**核心原则**: Free-threading 命令、术语、操作的唯一权威源

---

## 📋 快速导航

1. [一句话事实](#1-一句话事实)
2. [标准命令对照表](#2-标准命令对照表)
3. [安装 free-threading 构建](#3-安装-free-threading-构建)
4. [课程基线策略](#4-课程基线策略适用于本课程)
5. [PEP 演进](#5-pep-703-vs-pep-779--状态演进)
6. [兼容性现状](#6-兼容性现状截至-202606本机实测)
7. [GIL 状态检测](#7-检测-gil-状态的标准代码片段)
8. [常见错误诊断](#8-常见错误诊断)
9. [快速决策树](#9-快速决策树)
10. [课程文档约定](#10-本课程文档约定)

---

## 1. 一句话事实

> **Python 3.14 的 free-threading 仍然是独立构建版本（`python3.14t`），不是标准 `python3.14` 的命令行 flag。** PEP 779 把它从"试验性"提升为"官方支持"，**没有**取消独立构建。

---

## 2. 标准命令对照表

| 场景                                           | 正确命令                                                                       | 错误命令（请勿使用）          |
| ---------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------- |
| 标准 Python 3.13（带 GIL）                     | `python3.13`                                                                   | —                             |
| Python 3.13 free-threading（试验性）           | `python3.13t`                                                                  | ❌ `python3.13 --disable-gil` |
| 标准 Python 3.14（带 GIL，PEP 649 新语法）     | `python3.14`                                                                   | —                             |
| Python 3.14 free-threading（PEP 779 官方支持） | `python3.14t`                                                                  | ❌ `python3.14 --disable-gil` |
| 强制启用 free-threading（在 t 构建上）         | `PYTHON_GIL=0 python3.13t script.py`<br>或 `python3.13t -X gil=0 script.py`    | ❌ 任何 `--disable-gil`       |
| 强制启用 GIL（在 t 构建上做对照实验）          | `PYTHON_GIL=1 python3.13t script.py`                                           | —                             |
| 检测当前进程的 GIL 状态                        | `python -c "import sys; print(sys._is_gil_enabled())"`<br>（3.13+ 才有此 API） | —                             |

> **关键：** `--disable-gil` 这个命令行参数**从不存在**于任何 Python 发行版。它是早期社区 RFC 草案中的提议，最终未被采纳。如果你看到任何文档/AI 输出说"用 `--disable-gil` 启用无 GIL"，那是事实错误。

---

## 3. 安装 free-threading 构建

### macOS（Homebrew）

```bash
# Python 3.13 free-threading（试验性）
brew install python-freethreaded@3.13   # 提供 python3.13t 命令

# Python 3.14 free-threading（PEP 779 官方支持）
brew install python-freethreaded@3.14   # 提供 python3.14t 命令
```

> 验证：`which python3.13t && python3.13t --version`

### Ubuntu / Debian（deadsnakes PPA）

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Python 3.13 free-threading
sudo apt install python3.13-nogil      # 提供 python3.13t

# Python 3.14 free-threading
sudo apt install python3.14-nogil      # 提供 python3.14t
```

### 官方源码构建（任何平台）

```bash
git clone https://github.com/python/cpython.git
cd cpython
./configure --disable-gil               # 注意：这是 configure 的 flag，不是 python 的
make
./python -X gil=0 your_script.py
```

> ✅ `--disable-gil` 是 **configure 脚本**的 flag（编译期开关），**不是**运行时 python 的 flag。这正是事实混淆的根源。

### 使用 uv（推荐）

```bash
uv python install 3.13t                  # 安装 3.13 free-threading 构建
uv python install 3.14t                  # 安装 3.14 free-threading 构建
uv venv --python 3.13t .venv-ft
```

---

## 4. 课程基线策略（适用于本课程）

| 优先级           | 用途                                 | 命令                         |
| ---------------- | ------------------------------------ | ---------------------------- |
| **基线（必须）** | 所有非 free-threading 课程           | `python3.13`                 |
| **基线（可选）** | 试验 free-threading                  | `python3.13t`                |
| **试验性补充**   | 学习 PEP 779、PEP 649 等 3.14 新特性 | `python3.14` / `python3.14t` |

**默认教学命令**：除 L26 Part 4「Python 3.14 新特性预览」之外，所有课程基线 free-threading 演示均使用 **`python3.13t`**。

---

## 5. PEP 703 vs PEP 779 — 状态演进

| PEP         | 版本                   | 状态变化                                                                                                              |
| ----------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **PEP 703** | Python 3.13（2024.10） | 引入 free-threading 作为**试验性**特性。需要独立构建 `python3.13t`。承诺可能在未来版本变更或移除。                    |
| **PEP 779** | Python 3.14（2025.10） | 把 free-threading 从"试验性"升级为"**官方支持**（supported）但**非默认**"。仍需独立构建 `python3.14t`。承诺向前兼容。 |
| **PEP TBD** | Python 3.16+（推测）   | 可能让 free-threading 成为**默认构建**（届时 `python3.16` 即支持 `-X gil=0`，`python3.16t` 可能合并消失）。           |

> 当前（Python 3.14）阶段，free-threading 仍**需要独立构建**。这一点在 PEP 3.16 / 3.17 之前不会改变。

---

## 6. 兼容性现状（截至 2026.06，本机实测）

下表为 Python 3.13t（uv 安装的 freethreaded 构建）上的真实测试结果，
import 后 `sys._is_gil_enabled()` 是判断"是否真正享受无 GIL"的标准信号。

| 库             | 实测版本 | import 后 GIL       | 评级     | 备注                             |
| -------------- | -------- | ------------------- | -------- | -------------------------------- |
| **numpy**      | 2.4.6    | ✅ False            | 真无 GIL | 2.4 已原生适配                   |
| **asyncpg**    | 0.31.0   | ✅ False            | 真无 GIL | 0.31 加入 cp313t wheel           |
| **pydantic**   | 2.13.4   | ✅ False            | 真无 GIL | 纯 Python + Rust core            |
| **httpx**      | 0.28.1   | ✅ False            | 真无 GIL | —                                |
| **fastapi**    | 0.136.3  | ✅ False            | 真无 GIL | —                                |
| **sqlalchemy** | 2.0.50   | ✅ False            | 真无 GIL | 纯 Python 部分                   |
| **pandas**     | 2.3.3    | ⚠️ True（自动重启） | 需强制   | C 扩展未声明 free-threading 安全 |
| **duckdb**     | 1.5.3    | ⚠️ True（自动重启） | 需强制   | 同上                             |
| **lxml**       | 6.1.1    | ⚠️ True（自动重启） | 需强制   | 同上                             |

> ⚠️ **GIL 自动重启机制**：当 free-threading 构建检测到 C 扩展未声明 `Py_mod_gil` 标记时，
> 会自动重新启用 GIL 以避免崩溃。这意味着 import pandas 后，虽然你跑的是 `python3.13t`，
> 但实际行为已经退化成标准 GIL 构建。
>
> 想强制覆盖（自担风险）：`PYTHON_GIL=0 python3.13t script.py`
>
> 用 `python3.13t -c "import sys; pd...; print(sys._is_gil_enabled())"` 自检每个库的真实状态。

**实战建议**：

- 多线程数值计算（numpy）→ 直接 `python3.13t`
- 多线程 web 请求（fastapi/asyncpg/httpx）→ `python3.13t`
- 多线程 dataframe 操作（pandas）→ `PYTHON_GIL=0 python3.13t`（自担风险）
- 学员若在 free-threading 构建下遇到 `ImportError: ... was built without free-threading support`，
  说明该 wheel 没标 `cp313t`/`cp314t` ABI。解决：升级库版本，或回退到 `python3.13`。

---

## 7. 检测 GIL 状态的标准代码片段

```python
import sys

if hasattr(sys, "_is_gil_enabled"):
    gil_state = "启用" if sys._is_gil_enabled() else "已禁用"
    print(f"GIL 状态：{gil_state}")
    print(f"Python 版本：{sys.version_info}")
else:
    print("当前 Python < 3.13，没有 _is_gil_enabled API")
```

> ⚠️ `sys._is_gil_enabled()` 是 **Python 3.13+ 才有的 API**。在 3.12 及以下调用会 `AttributeError`。务必先 `hasattr` 检查。

---

## 8. 常见错误诊断

### 错误 1：`Unknown option: --disable-gil`

**原因**：把 configure 的 flag 当成了 python 的运行时 flag。  
**解决**：删掉 `--disable-gil`，改用 `python3.13t` 命令；或在 t 构建上用 `-X gil=0`。

### 错误 2：`Fatal Python error: config_read_gil: Disabling the GIL is not supported by this build`

**原因**：在标准（GIL）构建上尝试 `-X gil=0` 或 `PYTHON_GIL=0`。  
**解决**：必须用 freethreaded 构建（`python3.13t`/`python3.14t`），或重新编译 CPython 加 `--disable-gil`。

### 错误 3：`ImportError: ... 'somelib' was not built with free-threading support`

**原因**：该库的 wheel 没标 `cp313t`/`cp314t` ABI。  
**解决**：`pip install -U somelib`；如仍不行，提 issue 给上游或回到标准 `python3.13`。

### 错误 4：性能反而变慢

**原因 A**：单线程任务在 free-threading 构建上比 GIL 构建慢 ~10-40%（解释器开销）。  
**原因 B**：锁开销 > 并行收益（纯 I/O 或快速任务）。  
**解决**：free-threading 只对**长时间 CPU 密集型多线程**真正有收益。

---

## 9. 快速决策树

### 我应该使用 free-threading 吗？

```
你的任务是？
  │
  ├─ CPU 密集型 + 多线程？
  │   ├─ 是 → ✅ 使用 python3.13t/3.14t + PYTHON_GIL=0
  │   └─ 否 → 继续检查
  │
  ├─ I/O 密集型？
  │   └─ 使用 asyncio + 标准 python3.13（GIL 不是瓶颈）
  │
  ├─ 单线程？
  │   └─ 使用标准 python3.13（free-threading 会更慢）
  │
  └─ 学习目的？
      └─ ✅ 使用 python3.13t（体验无 GIL 编程）
```

### 我应该使用哪个版本？

```
需求
  │
  ├─ 生产环境？
  │   └─ ❌ 不推荐 free-threading（等 Python 3.16+ 正式版）
  │
  ├─ 学习 + 实验？
  │   ├─ 基础学习 → python3.13t
  │   └─ 最新特性 → python3.14t
  │
  └─ 课程作业？
      └─ python3.13（课程基线，除非课程明确要求 *t 构建）
```

### 遇到错误怎么办？

```
错误类型
  │
  ├─ "Unknown option: --disable-gil"
  │   └─ 修复：删除 --disable-gil，使用 python3.13t
  │
  ├─ "Disabling the GIL is not supported"
  │   └─ 修复：必须使用 *t 构建（python3.13t/3.14t）
  │
  ├─ "not built with free-threading support"
  │   └─ 修复：升级库版本或回退到标准 python3.13
  │
  └─ 性能更慢？
      └─ 检查：是否真的是 CPU 密集型 + 多线程任务
```

---

## 10. 本课程文档约定

- 所有命令片段一律使用本表中的标准命令。
- 任何课程文档里出现 `--disable-gil` 都视为 bug，应立即修正。
- 涉及 free-threading 的课程必须在开头链接到本文档：`参见 [FREE_THREADING_TRUTH.md](../../docs/technical/FREE_THREADING_TRUTH.md)`。
- 当 Python 3.15/3.16 释出新事实时，**只更新本文件**，其他文档通过链接保持一致。

**相关文档约定**:

- [PYTHON_VERSION.md](PYTHON_VERSION.md) - Python 版本规则（包含 free-threading 版本要求）
- [CLAUDE.md](https://github.com/nexo/python313-fullstack/blob/main/CLAUDE.md) - 开发规范（包含 Python 版本事实规则）

---

## 11. 参考资料（带状态标注）

- [PEP 703 — Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/)（试验性，3.13 引入）
- [PEP 779 — Free-threaded CPython is Officially Supported](https://peps.python.org/pep-0779/)（3.14 升级为正式支持）
- [Python 3.13 free-threading HOWTO](https://docs.python.org/3.13/howto/free-threading-python.html)
- [Python 3.14 What's New — Free-threading](https://docs.python.org/3.14/whatsnew/3.14.html)（待 3.14 GA 后链接稳定）
- [free-threading-compatible packages tracker](https://py-free-threading.github.io/tracking/)

---

## 🔗 相关资源

- [Python 版本规则](PYTHON_VERSION.md) - Python 版本唯一权威源
