# 快速开始指南

> ⏱️ **预计时间**: 5 分钟
> 🎯 **目标**: 快速启动 Python 学习环境

---

## 环境要求

- **Python**: 3.13+
- **包管理器**: uv (推荐)
- **IDE**: VS Code + Pylance (推荐) 或 PyCharm

---

## 快速启动

### 1️⃣ 克隆仓库

```bash
git clone https://github.com/dingwencheng9/python-fullstack-course.git
cd python-fullstack-course
```

### 2️⃣ 安装依赖

```bash
# 使用 uv 安装依赖
uv sync

# 或安装所有可选依赖
uv sync --extra dev --extra web --extra ai --extra docs
```

### 3️⃣ 验证安装

```bash
# 检查 Python 版本
python --version  # 应为 3.13.x

# 检查 uv
uv --version

# 运行一个示例
cd stage0-python-basics/lessons/L01-python-core
uv run python examples/01_hello.py
```

---

## 选择你的学习路径

### 🌱 零基础入门

```
Stage 0 → Stage 1 → Stage 2 → ...
```

从 [L01 Python 核心语法](stage0-python-basics/lessons/L01-python-core/README.md) 开始。

### ⚡ 快速通道（有 Python 基础）

```
Stage 2 (L27) → Stage 3 → Stage 4 → ...
```

适合已有 Python 基础的开发者。

### 🤖 AI Agent 专项

```
Stage 6 (L54) → Stage A
```

深入学习 AI Agent 开发。

---

## 常用命令

```bash
# 运行测试
uv run pytest tests/ -v

# 代码格式化
uv run ruff format .

# 类型检查
uv run mypy --strict .

# 完整 CI 检查
make ci-local
```

---

## 常见问题

### Q: 依赖安装失败？

```bash
# 确保 Python 3.13 已安装
python --version

# 使用 uv 重新安装
uv sync --refresh
```

### Q: 测试运行失败？

```bash
# 查看详细错误
uv run pytest -v --tb=long

# 跳过网络测试
uv run pytest -m "not network"
```

---

## 下一步

- 📖 [完整文档索引](docs/README.md)
- 📋 [课程映射表](COURSE_MAPPING.md)
- 🔧 [开发规范](CLAUDE.md)

---

> 💡 **提示**: 遇到问题？查看 [docs/README.md](docs/README.md) 获取更多帮助。
