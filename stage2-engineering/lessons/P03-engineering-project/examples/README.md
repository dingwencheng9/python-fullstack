# L25 示例代码

本目录包含工程化综合项目的四个可独立运行示例。

| 文件 | 主题 |
|------|------|
| `01_task_model.py` | 任务数据模型、枚举、序列化 |
| `02_task_storage.py` | 异步 JSON 存储与 `asyncio.to_thread` |
| `03_decorators.py` | 日志、缓存、重试装饰器 |
| `04_cli_interface.py` | 基于 `argparse` 的 CLI 接口 |

## 运行示例

```bash
uv run python examples/01_task_model.py
uv run python examples/02_task_storage.py
uv run python examples/03_decorators.py
uv run python examples/04_cli_interface.py --help
```
