# Scripts 目录

CI 工具、共享模块和 MkDocs hooks。

## 目录结构

```
scripts/
├── ci/
│   ├── check_markdown_links.py    # Markdown 链接检查
│   └── verify_course_metadata.py   # 课程元数据验证
├── common/
│   ├── __init__.py                # 共享模块导出
│   ├── colors.py                  # 终端颜色输出
│   ├── course_scanner.py          # 课程目录扫描
│   └── logger.py                 # 日志配置
├── docs/
│   └── mkdocs_hooks.py           # MkDocs 构建钩子
└── README.md
```

## 使用方法

### 课程元数据验证

```bash
python scripts/ci/verify_course_metadata.py
```

### Markdown 链接检查

```bash
python scripts/ci/check_markdown_links.py
```

## 依赖关系

- `verify_course_metadata.py` 依赖 `common/` 模块
- `check_markdown_links.py` 依赖 `common/` 模块
- `mkdocs_hooks.py` 独立运行，被 MkDocs 自动调用
