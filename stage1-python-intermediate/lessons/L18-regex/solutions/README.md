# solutions/ - L18 参考答案

本目录提供正则表达式练习的参考实现。建议先独立完成 `exercises/`，遇到困难再阅读。

## 文件清单

| 文件 | 说明 |
| ---- | ---- |
| `solution_01_validation.py` | 邮箱、手机号、HTTP/HTTPS URL 校验参考实现 |
| `solution_02_extraction.py` | ISO 日期、美元价格、HTML 起始标签提取参考实现 |
| `__init__.py` | 参考答案包入口 |

## 实现要点

- 校验函数统一使用 `re.Pattern.fullmatch()`，确保输入整体符合模式。
- 提取函数统一先检查输入类型，非字符串抛出 `TypeError`。
- 邮箱与 URL 模式覆盖课程练习需要，不追求 RFC 级完整性。
- HTML 标签提取只匹配简单起始标签名，例如 `<div>`、`<span>`、`<br>`。
