# tests/ - L17 单元测试

本目录用于自动验证 L17 参考答案。

```bash
cd stage1-python-intermediate/lessons/L17-functional
uv run pytest tests -q
```

## 测试覆盖

| 测试文件 | 用例数 | 验证内容 |
| -------- | ------ | -------- |
| `test_functional_pipeline.py` | 9 | 数据处理、空列表、字符串转换、`compose()`、`pipe()` |
| `test_data_transformation.py` | 8 | 折扣偏函数、税费偏函数、最终价格、舍入 |
| `test_compose_decorator.py` | 6 | 日志、重试、缓存、装饰器组合顺序、管道组合顺序 |

## 加载策略

`conftest.py` 使用 `importlib.util.spec_from_file_location()` 按物理路径加载 `solutions/`，避免不同课程中同名 `solutions` 包互相污染。

## 维护提示

- 新增函数式练习时，请同步更新 `solutions/`、本 README 和测试覆盖表。
- 修改组合顺序语义时，应同步更新 `compose()` / `pipe()` 文档、练习自检和测试断言。
- 涉及浮点计算时优先使用 `pytest.approx()` 或统一舍入策略。
