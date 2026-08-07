# L25 练习题

本目录包含 L25 工程化综合项目的练习题。

## 练习题列表

| 编号 | 文件 | 主题 | 难度 |
|------|------|------|------|
| 1 | `exercise_01_task_model.py` | 完善任务模型 | ⭐ |

其余工程化能力通过 `examples/` 与 `tests/` 中的模型、异步存储、装饰器和 CLI 示例综合演练。

## 验收标准

完成练习后，从本课目录运行：

```bash
uv run pytest tests/test_models.py -q
```

也可以从仓库根目录运行完整校验：

```bash
uv run pytest stage2-engineering/lessons/L25-engineering-project/tests -q
uv run python stage2-engineering/lessons/L25-engineering-project/verify.py
```
