# examples/ - 示例代码

**用途**：通过可直接运行的脚本观察 OOP 概念在 Python 中的具体表现。

运行方式：

```bash
cd stage0-python-basics/lessons/L07-oop-basics
python3 examples/01_class_basics.py
```

也可以批量运行：

```bash
for f in examples/*.py; do python3 "$f"; done
```

## 文件清单

| 文件 | 重点 |
|------|------|
| `01_class_basics.py` | 类定义、实例化、`self`、类属性与实例属性 |
| `02_encapsulation.py` | 单下划线、双下划线、`@property`、受控访问 |
| `03_inheritance.py` | 继承、方法重写、`super()`、MRO 入门 |
| `04_polymorphism.py` | 鸭子类型、统一接口、Protocol 入门 |
| `05_magic_methods.py` | ⚠️ 仅 L08 预告，使用纯 L07 知识点演示 |
| `06_class_static_methods.py` | ⚠️ 仅 Stage 1 预告，不要求掌握 |

## 学习建议

- 先逐个运行，再回到源码中查找产生输出的类和方法。
- 重点观察"对象保存状态，方法改变状态"的过程。
- `05_magic_methods.py` 和 `06_class_static_methods.py` 只作为后续课程的预告，不要求一次掌握。
