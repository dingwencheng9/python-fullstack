# solutions/ - L13 参考答案

> ⚠️ 建议先独立完成 `exercises/`，再查看本目录。参考答案兼顾教学可读性与 pytest 覆盖的边界行为。

## 文件清单

| 文件 | 内容 |
| ---- | ---- |
| `solution_01_decorators.py` | 计时、重试、参数验证、记忆化、调用计数和日志装饰器 |
| `solution_02_context_managers.py` | 文件管理器、事务、计时器、资源管理、输出重定向和事务上下文 |
| `__init__.py` | 标识 solutions 包，供测试按物理路径加载 |

## 设计说明

- 装饰器实现统一使用 `functools.wraps`，避免丢失函数名、文档字符串和调试信息。
- `retry()` 是装饰器工厂：外层接收配置，内层接收目标函数。
- `validate_args()` 通过函数参数名绑定位置参数和关键字参数，用 validator 统一校验。
- 上下文管理器的 `__exit__()` 默认返回 `False`，不抑制异常，让调用方或测试能感知失败。
- `transaction_context()` 在异常时清空操作列表并重新抛出异常，体现事务回滚语义。

## 验证

```bash
uv run pytest stage1-python-intermediate/lessons/L13-advanced-features/tests -q
```
