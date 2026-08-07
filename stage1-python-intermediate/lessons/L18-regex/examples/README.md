# examples/ - L18 示例代码

这些示例用于演示正则表达式基础语法、分组捕获、环视断言和 verbose 模式。每个文件都可独立运行。

```bash
cd stage1-python-intermediate/lessons/L18-regex
python examples/01_basic_patterns.py
```

## 文件清单

| 文件 | 主题 | 建议关注 |
| ---- | ---- | -------- |
| `01_basic_patterns.py` | 字符类、量词与锚点 | `[]`、`\d`、`*`/`+`/`?`、`^`/`$`、`\b` |
| `02_groups_capture.py` | 分组、命名分组、非捕获组与反向引用 | `()`、`(?P<name>...)`、`(?:...)`、`\1` |
| `03_lookaround.py` | 前瞻、后顾与否定环视 | `(?=...)`、`(?!...)`、`(?<=...)`、`(?<!...)` |
| `04_verbose_pattern.py` | verbose 模式、注释与模式复用 | `(?#...)`、`re.VERBOSE`、编译复用 |

## 批量运行

```bash
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done
```
