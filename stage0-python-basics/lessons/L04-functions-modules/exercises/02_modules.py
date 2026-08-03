"""L04 练习2: 模块与包

难度: ⭐☆☆ (入门)
预计时间: 20 分钟
知识点: 模块定义、__all__、公开/私有API、导入机制

任务描述:
完成以下练习：创建模块、控制导出、区分公开/私有函数。

提示:
1. __all__ 定义模块公开 API
2. 下划线开头的函数 (_function) 是私有的
3. from module import * 只导入 __all__ 中的名称
"""


# ============ 练习 1: 创建简单模块 ============
# 在下方定义一个函数，计算列表的平均值


def calculate_average(numbers: list[float]) -> float | None:
    """计算列表的平均值

    Args:
        numbers: 数字列表

    Returns:
        平均值，如果列表为空则返回 None
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


# ============ 练习 2: __all__ 控制导出 ============
# 定义一个模块，包含公开函数和私有函数

VALID_STATUS = ("pending", "active", "completed")

__all__ = ["VALID_STATUS", "calculate_total", "public_api"]


def public_api(data: list) -> dict:
    """公开 API 函数"""
    return {"count": len(data), "data": data}


def _private_helper(value: int) -> int:
    """私有辅助函数（不应该被外部直接使用）"""
    return value * 2


def calculate_total(items: list[int]) -> int:
    """计算商品总价（每个商品 10 元）"""
    return len(items) * 10


# ============ 练习 3: 使用字典定义配置 ============
# 注意：L04 阶段我们使用字典来模拟配置对象
# 类定义将在 L07（面向对象基础）中学习


def create_config(name: str, version: str, debug: bool = False) -> dict:
    """创建应用配置（字典形式）

    注意：这是演示型练习，使用字典代替类。
    真正的类定义将在 L07 中学习。
    """
    return {
        "name": name,
        "version": version,
        "debug": debug,
    }


def get_config_value(config: dict, key: str, default=None):
    """从配置字典中获取值"""
    return config.get(key, default)


def is_debug_mode(config: dict) -> bool:
    """检查是否开启调试模式"""
    return config.get("debug", False)


# ============ 练习 4: 模块导入与使用 ============
# 假设以下是从其他模块导入的函数
def format_username(username: str) -> str:
    """格式化用户名（转小写）"""
    return username.lower().strip()


def validate_length(text: str, min_len: int = 3, max_len: int = 20) -> bool:
    """验证文本长度"""
    return min_len <= len(text) <= max_len


# ============ 练习 5: 入口点模式 ============
def process_user_input(username: str) -> tuple[bool, str]:
    """处理用户输入

    Args:
        username: 用户名

    Returns:
        (是否成功, 消息)
    """
    if not username:
        return False, "用户名不能为空"

    formatted = format_username(username)

    if not validate_length(formatted):
        return False, "用户名长度必须在 3-20 个字符之间"

    return True, f"欢迎, {formatted}!"


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== 模块练习测试 ===\n")

    # 测试平均值
    print("1. calculate_average:")
    print(f"   [1, 2, 3, 4, 5] = {calculate_average([1, 2, 3, 4, 5])}")
    print(f"   [] = {calculate_average([])}")

    # 测试 __all__
    print("\n2. __all__ 导出控制:")
    print(f"   __all__ = {__all__}")

    # 测试配置
    print("\n3. AppConfig:")
    config = create_config("MyApp", "1.0.0", debug=True)
    print(f"   {config}")

    # 测试用户输入处理
    print("\n4. process_user_input:")
    success, msg = process_user_input("  Alice123  ")
    print(f"   '  Alice123  ' -> {msg}")

    success, msg = process_user_input("ab")
    print(f"   'ab' -> {msg}")
