# L15: 描述符与属性

> **课程编号**: L15
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 5 小时
> **前置课程**: L10 类型系统, L13 Python 高级特性
> **核心内容**: 描述符协议、`property`、数据描述符/非数据描述符、懒加载、属性验证

---

## 🎯 课程定位

描述符是 Python 属性访问机制的底层协议，也是 `property`、`classmethod`、`staticmethod`、ORM 字段、数据验证框架和缓存属性的基础。本课承接 L12 的装饰器与上下文协议，继续深入“对象协议驱动行为”的设计方式。

完成本课后，你将能够：

- 解释 `__get__()`、`__set__()`、`__delete__()` 与 `__set_name__()` 的调用时机。
- 区分数据描述符和非数据描述符，并理解属性查找优先级。
- 使用 `property` 实现受控读写、计算属性和验证逻辑。
- 编写可复用的验证描述符、范围描述符和懒加载描述符。
- 将描述符用于数据校验、缓存、日志、自动转换等工程场景。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L15-descriptors

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_descriptor_basics.py
python examples/02_descriptor_advanced.py

# 3) 完成练习并自检
python exercises/01_descriptors.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 描述符协议基础 | `lesson.md`、`examples/01_descriptor_basics.py` | `__get__`、`__set__`、`__set_name__` |
| 2 | 属性验证与 `property` | `lesson.md`、`examples/01_descriptor_basics.py` | 受控属性、范围校验、计算属性 |
| 3 | 高级描述符模式 | `examples/02_descriptor_advanced.py` | 自定义 property、访问日志、描述符优先级 |
| 4 | 动手练习 | `exercises/01_descriptors.py` | `Positive`、`Range`、`Lazy` |
| 5 | 对照参考答案 | `solutions/solution_01_descriptors.py` | 可复用基类与异常消息 |
| 6 | 自动化验证 | `tests/test_descriptors.py` | 7 个测试用例覆盖核心行为 |

---

## 📁 目录结构

| 路径 | 用途 |
| ---- | ---- |
| [lesson.md](lesson.md) | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的示例代码 |
| [exercises/](exercises/) | 学员练习与脚本自检 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | pytest 单元测试 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解描述符协议和属性查找顺序。
- [ ] 能够独立解释数据描述符与非数据描述符的区别。
- [ ] 运行 2 个示例文件，并观察输出中的属性访问过程。
- [ ] 完成 `exercises/01_descriptors.py` 并通过脚本自检。
- [ ] 通过 `uv run pytest tests -q`。

---

## 🧪 检查命令

```bash
# Python 语法/导入检查
python3 -m py_compile examples/*.py exercises/*.py solutions/*.py tests/*.py

# 示例运行
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done

# 练习自检
for f in exercises/*.py; do
  echo "== $f =="
  python "$f"
done

# 单元测试
uv run pytest tests -q
```

---

## 🔗 下一步

完成本课后继续学习：

- [L16: 并发编程入门](../L16-concurrency-intro/README.md)
- L14 会进入线程、进程和协程的并发基础，为后续工程化异步编程做准备。
