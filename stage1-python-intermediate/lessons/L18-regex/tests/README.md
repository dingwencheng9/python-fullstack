# tests/ - L18 单元测试

本目录用于自动验证 L18 参考答案。

```bash
cd stage1-python-intermediate/lessons/L18-regex
uv run pytest tests -q
```

## 测试覆盖

| 测试文件 | 用例数 | 验证内容 |
| -------- | ------ | -------- |
| `test_regex.py` | 20 | 邮箱、手机号、URL 校验；日期、价格、HTML 标签提取；非字符串异常路径 |

## 加载策略

`conftest.py` 使用 `importlib.util.spec_from_file_location()` 按物理路径加载 `solutions/`，避免不同课程中同名 `solutions` 包互相污染。

## 维护提示

- 修改正则模式时，应同步检查正例、反例和异常路径。
- 新增验证/提取函数时，请同步更新 exercises、solutions、tests 和本 README。
- 不建议把 HTML/XML 解析扩展为复杂正则；需要完整解析时应引导学习者使用专用解析库。
