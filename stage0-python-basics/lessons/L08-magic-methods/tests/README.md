# tests/ - 单元测试

**用途**：验证 L07 魔术方法参考答案是否满足预期行为。

运行方式：

```bash
cd stage0-python-basics/lessons/L08-magic-methods
uv run pytest tests/ -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_magic_methods.py` | `Vector`、`Money`、`Bag` 扩展示范，以及 `Fraction`、`Set`、`Multiplier` 练习对应答案 |
| `conftest.py` | 按物理路径加载当前课程 `solutions` 包，避免不同 lesson 的同名包互相污染 |

## 覆盖重点

- 表示协议：`__repr__`、`__str__`。
- 比较和哈希：`__eq__`、`__hash__`。
- 算术协议：`__add__`、`__sub__`、`__mul__`、`__rmul__`。
- 容器协议：`__len__`、`__contains__`、`__iter__`。
- 可调用对象：`__call__`。

## 后续可扩展

- 为 `Fraction` 增加减法、乘法、除法测试。
- 为 `Set` 增加并集、交集、差集等集合运算测试。
- 为属性访问示例增加更明确的“谨慎使用”说明或单独扩展练习。
