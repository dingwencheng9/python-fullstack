# exercises - 练习题

**用途**：供学员独立完成的练习题，docstring 包含任务说明。

## 运行方式

```bash
# 查看任务说明
cat exercises/01_hello_practice.py

# 运行验证（手动运行脚本）
uv run python exercises/01_hello_practice.py

# 自动评分（pytest）
uv run pytest tests/ -q
```

## 文件清单

| 文件 | 难度 | 主题 |
|------|------|------|
| `01_hello_practice.py` | ⭐ | Hello World + uv 项目初始化 |
| `02_io_practice.py` | ⭐ | input/output 综合练习 |
| `03_type_basics.py` | ⭐ | 5 种基本类型练习 |
| `04_type_conversion.py` | ⭐ | 类型转换练习 |
| `05_fstring_practice.py` | ⭐ | f-string 格式化练习 |
| `06_uv_practice.py` | ⭐ | uv 工具链练习 |
