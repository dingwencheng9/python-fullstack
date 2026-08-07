"""L05 练习 2: traceback 分析

练习使用 traceback 模块分析异常信息。
"""

import traceback


def save_error_log(error_message, traceback_str):
    """将错误信息保存到日志文件

    Args:
        error_message: 错误消息（不含 traceback）
        traceback_str: 完整的 traceback 字符串
    """
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"错误: {error_message}\n")
        f.write("-" * 50 + "\n")
        f.write(traceback_str)
        f.write("=" * 50 + "\n\n")


def analyze_error():
    """模拟一个错误场景，分析异常信息"""
    print("请运行以下代码，观察 traceback 输出:")
    print("-" * 50)

    # 这段代码会抛出异常，请分析 traceback
    data = {"name": "Alice", "age": 30}

    # 尝试访问不存在的键
    # 使用异常处理捕获异常，并使用 traceback 分析
    try:
        result = data["city"]
    except KeyError as e:
        error_msg = f"KeyError: {e}"
        # 使用 traceback.format_exc() 获取完整的 traceback 字符串
        tb_str = traceback.format_exc()
        print(f"\n捕获到异常: {error_msg}")
        print("\nTraceback 详情:")
        print(tb_str)
        # 将错误信息保存到日志
        save_error_log(error_msg, tb_str)
        print("错误信息已保存到 error.log")


def process_user_data(raw_data):
    """处理用户数据"""
    # 模拟处理逻辑
    required_fields = ["name", "email"]

    # 检查必要字段是否存在
    # 如果缺失，抛出有意义的异常
    for field in required_fields:
        if field not in raw_data:
            raise KeyError(f"缺少必要字段: {field}")


if __name__ == "__main__":
    print("traceback 练习")
    print("=" * 50)

    # 练习 1: 分析错误
    analyze_error()

    # 练习 2: 处理用户数据
    print("\n练习 2: 处理用户数据")
    user1 = {"name": "Bob", "email": "bob@example.com", "city": "Beijing"}
    user2 = {"name": "Carol"}  # 缺少 email

    process_user_data(user1)
    print("user1 处理成功")

    process_user_data(user2)
    print("user2 处理成功")
