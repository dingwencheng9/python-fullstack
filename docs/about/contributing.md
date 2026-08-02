# 贡献指南

> 🎉 感谢你考虑为 Python 全栈课程贡献代码！

---

## 如何贡献

### 1. Fork 仓库

点击 GitHub 页面右上角的 **Fork** 按钮。

### 2. 克隆你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/python-fullstack-course.git
cd python-fullstack-course
```

### 3. 创建分支

```bash
git checkout -b feat/your-feature-name
# 或
git checkout -b fix/issue-description
```

### 4. 进行修改

遵循以下规范：

- **代码风格**: 使用 `uv run ruff format .` 格式化代码
- **类型检查**: 使用 `uv run mypy --strict .` 检查类型
- **测试**: 确保所有测试通过 `uv run pytest`

### 5. 提交更改

```bash
git add .
git commit -m "feat(stageX): 添加课程内容"
```

**提交消息格式**:

| 类型 | 描述 |
|------|------|
| `feat:` | 新功能或课程内容 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 代码重构 |
| `test:` | 测试相关 |

### 6. 推送分支

```bash
git push origin feat/your-feature-name
```

### 7. 创建 Pull Request

在 GitHub 上创建 PR，描述你的更改。

---

## 课程贡献规范

### lesson.md 格式

```markdown
# 课程标题

> **课程编号**: LXX
> **所属阶段**: Stage X
> **课程时长**: X 小时
> **难度**: ⭐⭐☆☆☆
> **前置课程**: LXX

---

## 📚 课程概述

## 🎯 学习目标

## 📋 课程大纲

## 🔧 环境准备

## 📖 详细内容

### Part 1: ...

---

## 📝 练习题

## ✅ 课后检查
```

### 代码示例

- 示例代码放在 `examples/` 目录
- 练习答案放在 `solutions/` 目录
- 测试代码放在 `tests/` 目录

---

## 测试要求

所有课程必须包含：

- ✅ `README.md` - 课程入口
- ✅ `lesson.md` - 完整教学内容
- ✅ `examples/` - 示例代码（可选）
- ✅ `exercises/` - 练习题（可选）
- ✅ `tests/` - 单元测试（可选）

---

## 审查流程

1. 提交 PR 后，CI 会自动运行
2. 所有检查必须通过才能合并
3. 代码审查由维护者进行

---

## 问题反馈

- 🐛 **Bug**: 创建 [GitHub Issue](https://github.com/dingwencheng9/python-fullstack-course/issues)
- 💡 **建议**: 创建 Feature Request
- ❓ **问题**: 加入讨论

---

## License

通过贡献，你同意你的代码遵循项目的 MIT License。
