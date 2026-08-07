# exercises/ - L18 练习题

本目录包含正则表达式验证与提取练习。每个文件都可直接运行，并通过内置断言完成基础自检。

```bash
cd stage1-python-intermediate/lessons/L18-regex
python exercises/01_validation.py
python exercises/02_extraction.py
```

## 文件清单

| 文件 | 练习内容 | 对应参考答案 | 相关测试 |
| ---- | -------- | ------------ | -------- |
| `01_validation.py` | 邮箱、手机号、HTTP/HTTPS URL 校验 | `solutions/solution_01_validation.py` | `tests/test_regex.py` |
| `02_extraction.py` | ISO 日期、美元价格、HTML 起始标签提取 | `solutions/solution_02_extraction.py` | `tests/test_regex.py` |

## 学习建议

1. 验证类函数优先使用 `re.fullmatch()`，避免只匹配字符串的一部分。
2. 提取类函数优先使用 `findall()` 或 `finditer()`，并明确是否需要捕获组。
3. 对非字符串输入保持显式 `TypeError`，便于调用方快速定位错误。
4. 编写 HTML 相关正则时要说明边界：本课只处理简单起始标签，不替代专业 HTML 解析器。
