"""L03 练习2 参考答案"""


def get_user_name(response: dict) -> str:
    """安全提取用户名"""
    return response.get("data", {}).get("user", {}).get("name", "Unknown")


def get_total_count(response: dict) -> int:
    """安全提取分页 total"""
    return response.get("data", {}).get("pagination", {}).get("total", 0)


def merge_defaults(defaults: dict, user_config: dict) -> dict:
    """使用 | 运算符合并配置"""
    return defaults | user_config
