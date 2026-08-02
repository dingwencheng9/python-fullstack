"""L05 练习 2: traceback 分析

练习使用 traceback 模块分析异常信息。
"""


def save_error_log(error_message, traceback_str):
    """将错误信息保存到日志文件"""
    # TODO: 实现这个函数，将错误信息追加到 error.log
    pass


def analyze_error():
    """模拟一个错误场景，分析异常信息"""
    print("请运行以下代码，观察 traceback 输出:")
    print("-" * 50)

    # 这段代码会抛出异常，请分析 traceback
    data = {"name": "Alice", "age": 30}
    try:
        # 尝试访问不存在的键
        _ = data["city"]
    except KeyError as e:
        print(f"捕获到 KeyError: {e}")
        # TODO: 使用 traceback 模块打印完整的调用栈


def process_user_data(raw_data):
    """处理用户数据"""
    # 模拟处理逻辑
    required_fields = ["name", "email"]

    # TODO: 检查必要字段是否存在
    # 如果缺失，抛出有意义的异常
    for field in required_fields:
        if field not in raw_data:
            # 抛出异常，让调用者知道缺少哪个字段
            pass


if __name__ == "__main__":
    print("traceback 练习")
    print("=" * 50)

    # 练习 1: 分析错误
    analyze_error()

    # 练习 2: 处理用户数据
    print("\n练习 2: 处理用户数据")
    user1 = {"name": "Bob", "email": "bob@example.com", "city": "Beijing"}
    user2 = {"name": "Carol"}  # 缺少 email

    try:
        process_user_data(user1)
        print("user1 处理成功")
    except Exception as e:
        print(f"user1 处理失败: {e}")

    try:
        process_user_data(user2)
        print("user2 处理成功")
    except Exception as e:
        print(f"user2 处理失败: {e}")
