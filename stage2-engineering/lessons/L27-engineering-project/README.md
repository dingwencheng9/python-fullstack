# L27: 工程化综合项目

> **课程编号**: L27
> **所属阶段**: Stage 2 - 现代工程
> **预计时长**: 5-8 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L19 (pytest), L20 (工具链), L21-L26 (异步/装饰器/并发)
> **版本**: v1.0
> **核心版本**: Python 3.13

---

## 🚀 快速开始

```bash
# 从仓库根目录进入本课
cd stage2-engineering/lessons/L27-engineering-project

# 运行课程自检
uv run python verify.py

# 运行单元测试
uv run pytest tests/ -q
```

## 📚 学习路径

1. 阅读 [`lesson.md`](lesson.md)，理解工程化项目架构。
2. 运行 `examples/*.py`，观察 Task 模型、异步存储、装饰器与 CLI。
3. 完成 [`exercises/exercise_01_task_model.py`](exercises/exercise_01_task_model.py)。
4. 对照 [`solutions/solution_01_task_model.py`](solutions/solution_01_task_model.py) 优化实现。
5. 运行 `uv run pytest tests/ -q` 和 `uv run python verify.py` 验证理解。

## 📁 目录结构

| 路径 | 用途 |
|------|------|
| [`examples/`](examples/) | 示例代码：模型、存储、装饰器、CLI |
| [`exercises/`](exercises/) | 练习题 |
| [`solutions/`](solutions/) | 参考答案 |
| [`tests/`](tests/) | 单元测试 |
| [`verify.py`](verify.py) | 本课结构、脚本与核心行为自检 |

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解工程化项目架构。
- [ ] 运行全部示例，理解 CLI 工具设计。
- [ ] 完成任务模型练习，并对照参考答案修正边界处理。
- [ ] 通过 `uv run pytest tests/ -q`。
- [ ] 通过 `uv run python verify.py`。
- [ ] 理解 CI/CD 配置示例如何迁移到真实项目。

---

## 🔗 下一步

恭喜完成 Stage 2！接下来进入 **Stage 3: Web 开发基础**：

- [L26: HTTP 协议与抓包基础](../../../stage3-web-basics/lessons/L26-http/README.md)
