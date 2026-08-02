# solutions/ - 参考答案

**用途**：提供练习对应答案，并保留部分扩展示范类用于展示更多魔术方法组合。

> ⚠️ 建议先独立完成 exercises，再查看本目录。

## 与 exercises 对应的答案

| 文件 | 对应练习 | 说明 |
|------|----------|------|
| `fraction.py` | `01_fraction.py` | `Fraction`：分数约分、表示、相等、哈希、加法 |
| `set_class.py` | `02_set_class.py` | `Set`：简化集合与容器协议 |
| `callable.py` | `03_callable.py` | `Multiplier`：可调用对象 |

## 扩展示范答案

| 文件 | 说明 |
|------|------|
| `vector.py` | `Vector`：向量运算、字符串表示、哈希和长度计算 |
| `money.py` | `Money`：金额归一化、加减乘、格式化输出 |
| `collection.py` | `Bag`：允许重复元素的容器与自定义迭代器 |
| `__init__.py` | 统一导出所有答案类 |

## 使用方式

从课程目录运行：

```bash
python3 - <<'PY'
from solutions import Fraction, Multiplier, Set

print(Fraction(1, 3) + Fraction(1, 6))
print(Multiplier(2)(5))

s = Set()
s.add("apple")
print("apple" in s)
PY
```

或者直接运行测试：

```bash
uv run pytest tests/ -q
```
