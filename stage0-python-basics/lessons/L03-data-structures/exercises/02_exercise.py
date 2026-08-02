"""L03 练习2: API 响应防御性解析

难度: ⭐⭐☆ (中等)
预计时间: 20 分钟
知识点: 字典 get() 方法、链式访问、默认值处理


任务描述:
TODO: 实现安全的 API 数据提取函数

提示:
1. 使用 .get(键, 默认值) 链式访问嵌套字典
2. 每一层都要检查是否存在
3. 使用 isinstance() 验证类型
"""


def get_user_name(response: dict) -> str:
    """
    从 API 响应中安全提取用户名。

    数据结构:
        response = {
            "data": {"user": {"name": "Alice"}}
        }

    要求:
    1. 用 .get() 链式访问
    2. 任何层级缺失返回 "Unknown"
    3. 必须带类型注解
    """
    return response.get("data", {}).get("user", {}).get("name", "Unknown")


def get_total_count(response: dict) -> int:
    """
    从分页响应中提取 total 字段。

    数据结构:
        response = {
            "data": {
                "items": [...],
                "pagination": {"total": 100}
            }
        }

    要求:
    1. 安全获取 pagination.total
    2. 缺失时返回 0
    3. 必须带类型注解
    """
    return response.get("data", {}).get("pagination", {}).get("total", 0)


def merge_defaults(defaults: dict, user_config: dict) -> dict:
    """
    合并默认配置和用户配置（用户配置优先）。

    要求:
    1. 使用 Python 3.9+ 的 | 运算符
    2. 不修改原字典
    3. 必须带类型注解
    """
    return defaults | user_config


if __name__ == "__main__":
    # 测试 1
    response_1: dict = {"data": {"user": {"name": "Alice"}}}
    print(get_user_name(response_1))  # 应输出: Alice
    print(get_user_name({}))  # 应输出: Unknown

    # 测试 2
    response_2: dict = {"data": {"pagination": {"total": 100}}}
    print(get_total_count(response_2))  # 应输出: 100
    print(get_total_count({}))  # 应输出: 0

    # 测试 3
    defaults: dict = {"timeout": 30, "retries": 3}
    user: dict = {"timeout": 60}
    print(merge_defaults(defaults, user))  # {"timeout": 60, "retries": 3}
