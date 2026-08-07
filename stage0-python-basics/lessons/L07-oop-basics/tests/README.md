# tests/ - 单元测试

**用途**：验证 L07 参考答案是否满足面向对象基础练习的预期行为。

运行方式：

```bash
cd stage0-python-basics/lessons/L07-oop-basics
uv run pytest tests/ -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_oop_basics.py` | `Person`、`BankAccount`、`Rectangle`、`Animal/Dog/Cat`、`Vector` 的核心行为 |
| `conftest.py` | 按物理路径加载当前课程 `solutions` 包，避免不同 lesson 的同名包互相污染 |

## 覆盖重点

- 对象创建与实例属性。
- 存款、取款、非法金额和余额不足处理。
- 矩形尺寸校验、面积和周长。
- 继承后的属性复用与方法重写。
- 向量加法、相等比较和字符串表示。

## 后续可扩展

- 增加 `Vector.__sub__`、`__mul__`、`magnitude()` 的测试。
- 增加 `BankAccount` 初始余额非法值测试。
- 增加 `repr()` 可调试性的断言。
