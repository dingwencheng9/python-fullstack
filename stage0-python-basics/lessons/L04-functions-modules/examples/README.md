# examples/ - 示例代码

**用途**：展示 L04 函数、模块、包和标准库的具体用法。每个主示例文件都可以独立运行。

从本课目录运行：

```bash
uv run python examples/00_demo.py
```

或进入 examples 目录运行：

```bash
cd stage0-python-basics/lessons/L04-functions-modules/examples
python 00_demo.py
```

## 文件清单

| 文件/目录 | 说明 |
|-----------|------|
| `00_demo.py` | 函数定义、默认参数、可变参数、返回值、入口点基础 |
| `01_module_imports.py` | `import`、`from import`、别名导入和导入风格对比 |
| `02_package_imports.py` | 包、子模块、子包和 `__init__.py` 重导出 |
| `03_name_main.py` | `__name__` 与 `if __name__ == "__main__"` 入口点模式 |
| `04_all_exports.py` | `__all__` 如何控制 `from module import *` 的导出范围 |
| `05_stdlib.py` | `math`、`random`、`datetime`、`json`、`os`、`pathlib` 等常用标准库 |
| `06_type_annotations.py` | 函数签名类型注解、局部变量注解、`None` 类型 |
| `07_lambda.py` | lambda 表达式基础、`sorted`/`map`/`filter` 配合使用 |
| `my_module.py` | 示例模块：配合 `04_all_exports.py` 演示公开 API 与私有命名约定 |
| `my_package/` | 示例包：包含计算器、验证器和子包工具模块 |
