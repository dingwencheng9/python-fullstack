# L16 正则表达式练习 3：日志解析实战

> 本练习将帮助你掌握正则表达式在实际日志分析中的应用。

## 练习目标

1. 使用正则表达式解析结构化日志
2. 提取关键信息（时间戳、级别、模块、消息）
3. 过滤和分类日志条目

## 数据格式

假设有以下日志格式：

```
2024-01-15 10:23:45 [INFO] [AppServer] Server started on port 8080
2024-01-15 10:23:46 [DEBUG] [Database] Connection pool initialized: 10 connections
2024-01-15 10:23:47 [WARNING] [Auth] Invalid login attempt from 192.168.1.100
2024-01-15 10:23:48 [ERROR] [Database] Query timeout after 30s: SELECT * FROM users
2024-01-15 10:23:49 [INFO] [API] Request completed: GET /api/users 200 OK 45ms
```

## 练习要求

### 1. 实现 `parse_log_line(line: str) -> dict | None` 函数

解析单行日志，返回字典：

```python
{
    "timestamp": "2024-01-15 10:23:45",
    "level": "INFO",
    "module": "AppServer",
    "message": "Server started on port 8080"
}
```

### 2. 实现 `filter_by_level(logs: list[dict], level: str) -> list[dict]` 函数

按日志级别过滤：

```python
errors = filter_by_level(parsed_logs, "ERROR")
```

### 3. 实现 `count_by_level(logs: list[dict]) -> dict[str, int]` 函数

统计各级别日志数量：

```python
counts = count_by_level(parsed_logs)
# {'INFO': 2, 'DEBUG': 1, 'WARNING': 1, 'ERROR': 1}
```

## 提示

### 正则模式参考

```python
# 时间戳: YYYY-MM-DD HH:MM:SS
TIMESTAMP_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

# 日志级别: [INFO], [ERROR], etc.
LEVEL_PATTERN = r"\[(INFO|DEBUG|WARNING|ERROR|CRITICAL)\]"

# 模块名: [ModuleName]
MODULE_PATTERN = r"\[(\w+)\]"

# 完整模式
FULL_PATTERN = rf"({TIMESTAMP_PATTERN}) ({LEVEL_PATTERN}) ({MODULE_PATTERN}) (.+)"
```

## 答案参考

参见 `../solutions/solution_03_log_parser.py`
