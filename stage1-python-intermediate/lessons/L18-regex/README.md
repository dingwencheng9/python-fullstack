# L18: 正则表达式

> **课程编号**: L18
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 4 小时
> **核心内容**: 正则语法、`re` 模块、字符类、量词、分组捕获、命名分组、环视断言、文本验证与提取

---

## 🎯 课程定位

本课是 Stage 1 的收官课，聚焦 Python 文本处理中的高频工具：正则表达式。你将把前面课程中的函数封装、测试思维和数据处理能力应用到字符串验证、日志/HTML/价格/日期提取等场景中，并为 Stage 2 的工程化测试、工具链和数据处理任务做准备。

完成本课后，你将能够：

- 使用 `re.search()`、`re.match()`、`re.fullmatch()`、`re.findall()`、`re.finditer()`、`re.sub()`。
- 编写字符类、量词、锚点和单词边界等基础模式。
- 使用捕获组、命名分组、非捕获组和反向引用。
- 使用前瞻、后顾和否定环视表达上下文约束。
- 编写可测试的邮箱、手机号、URL 校验函数。
- 编写日期、价格和 HTML 起始标签提取函数。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L18-regex

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_basic_patterns.py
python examples/02_groups_capture.py
python examples/03_lookaround.py

# 3) 完成练习并自检
python exercises/01_validation.py
python exercises/02_extraction.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 正则基础语法 | `lesson.md`、`examples/01_basic_patterns.py` | 字符类、量词、锚点、边界 |
| 2 | 分组与引用 | `examples/02_groups_capture.py` | 捕获组、命名分组、非捕获组、反向引用 |
| 3 | 环视断言 | `examples/03_lookaround.py` | 前瞻、后顾、否定环视、密码校验 |
| 4 | 数据验证练习 | `exercises/01_validation.py` | 邮箱、手机号、URL 完整匹配 |
| 5 | 文本提取练习 | `exercises/02_extraction.py` | 日期、美元价格、HTML 起始标签 |
| 6 | 自动化验证 | `tests/test_regex.py` | 20 个测试用例覆盖 solutions 行为 |

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

- [ ] 阅读 `lesson.md`，理解字符类、量词、锚点、分组和环视断言。
- [ ] 运行 3 个示例文件，并能解释关键匹配结果。
- [ ] 完成 2 个练习文件，并通过脚本自检。
- [ ] 能说明何时使用 `fullmatch()`、`findall()`、`finditer()` 和 `sub()`。
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

完成本课后进入 Stage 2 现代工程：

- [L17: pytest 完整实战](../../../stage2-engineering/lessons/L17-pytest-complete/README.md)
- [Stage 2 概览](../../../stage2-engineering/README.md)

恭喜完成 Stage 1 Python 进阶！🎉
