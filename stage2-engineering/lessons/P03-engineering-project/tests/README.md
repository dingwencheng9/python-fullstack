# L25 工程化综合项目 - 测试

本目录包含 L25 工程化综合项目的测试用例。

## 测试结构

- `conftest.py` - pytest 配置和共享 fixtures
- `test_models.py` - Task 模型测试
- `test_storage.py` - 异步存储层测试
- `test_decorators.py` - 装饰器测试
- `test_cli.py` - CLI 接口测试

## 运行测试

从本课目录运行：

```bash
uv run pytest tests/ -q
uv run pytest tests/test_models.py -q
uv run pytest tests/test_models.py::TestTaskModel::test_task_creation_with_defaults -q
```

从仓库根目录运行：

```bash
uv run pytest stage2-engineering/lessons/L25-engineering-project/tests -q
```
