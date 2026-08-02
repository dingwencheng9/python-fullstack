# examples/ — 示例代码

**用途**：展示 L01 每个知识点的具体用法，学员可直接运行验证。

每个文件对应 lesson.md 的一个核心概念，难度从低到高排列：

| 文件 | 难度 | 对应章节 | 说明 |
|------|------|---------|------|
| `01_hello_world.py` | ⭐ | 1.3 | Hello World + print() 基础 |
| `02_repl_basics.py` | ⭐ | 1.4 + Part 0 | REPL 工具链 + type/dir/help 三大自学工具 |
| `03_input_output.py` | ⭐ | 1.5 | input() / print() 交互实战 |
| `04_variables_reference.py` | ⭐⭐ | 2.1 | 变量引用模型 + id() / is |
| `05_basic_types.py` | ⭐ | 2.2 | 5 种基本数据类型 |
| `06_type_annotations.py` | ⭐⭐ | 2.3 | 类型注解入门 |
| `07_fstring_format.py` | ⭐⭐ | 2.4 | f-string 格式化全用法 |
| `08_type_conversion.py` | ⭐⭐ | 2.5 | 类型转换链路 + 陷阱 |
| `09_uv_basics.py` | ⭐ | 1.2 | uv 工具链入门 |
| `10_variable_reference_visual.py` | ⭐⭐⭐ | 2.1 | 引用模型可视化（配 lesson 图） |

## 运行方式

```bash
# 从仓库根目录运行单个示例
uv run python stage0-python-basics/lessons/L01-python-core/examples/01_hello_world.py

# 批量验证（可选）
for f in stage0-python-basics/lessons/L01-python-core/examples/*.py; do
    uv run python "$f"
done
```

## 难度说明

- ⭐ **基础**：纯脚本语句，无函数定义，直接可读
- ⭐⭐ **变体**：展示类型注解、函数组合、工程风格
- ⭐⭐⭐ **可视化**：配合 lesson.md Mermaid 图的代码演示（初学者可跳过）
