# exercises/ - L13 练习题

本目录包含描述符练习。练习文件可直接运行，并通过内置断言完成基础自检。

```bash
cd stage1-python-intermediate/lessons/L13-descriptors
python exercises/01_descriptors.py
```

## 文件清单

| 文件 | 练习内容 | 对应参考答案 | 相关测试 |
| ---- | -------- | ------------ | -------- |
| `01_descriptors.py` | 实现验证描述符基类、正数验证、范围验证与懒加载描述符 | `solutions/solution_01_descriptors.py` | `tests/test_descriptors.py` |
| `02_property_descriptor.py` | SimpleProperty 描述符实现、类级 vs 实例级访问、描述符优先级与继承 | `solutions/solution_02_property.py` | `tests/test_descriptors.py` |

## 学习建议

1. 先补齐 `Validator.__set__()` 和 `Positive.validate()`，确认负数会抛出 `ValueError`。
2. 再实现 `Range`，关注边界值是否包含 `min_val` 和 `max_val`。
3. 最后实现 `Lazy`，要求第一次访问调用 `_load_<name>()`，后续访问使用缓存。
4. 完成后运行 pytest，对照参考答案检查异常消息和类级访问行为。
