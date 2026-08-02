"""L05 练习 2 参考解答: traceback 分析"""

import traceback
from pathlib import Path


def save_error_log(error_message: str, tb_str: str | None = None) -> None:
    """将错误信息保存到日志文件"""
    log_file = Path("error.log")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"时间: {__import__('datetime').datetime.now()}\n")
        f.write(f"错误信息: {error_message}\n")
        if tb_str:
            f.write("调用栈:\n")
            f.write(tb_str)
        f.write("=" * 60 + "\n\n")


def analyze_error() -> None:
    """模拟一个错误场景，分析异常信息"""
    data = {"name": "Alice", "age": 30}
    try:
        _ = data["city"]
    except KeyError as e:
        print(f"捕获到 KeyError: {e}")
        print("\n完整调用栈:")
        traceback.print_exc()


def process_user_data(raw_data: dict) -> None:
    """处理用户数据"""
    required_fields = ["name", "email"]

    missing_fields = []
    for field in required_fields:
        if field not in raw_data:
            missing_fields.append(field)

    if missing_fields:
        # 使用 traceback.format_exc() 获取调用栈用于日志
        try:
            raise ValueError(f"缺少必要字段: {', '.join(missing_fields)}")
        except ValueError as e:
            tb_str = traceback.format_exc()
            # 打印错误和调用栈
            print(f"错误: {e}")
            print(f"调用栈:\n{tb_str}")
            # 实际项目中可以保存到日志文件
            # save_error_log(str(e), tb_str)


if __name__ == "__main__":
    print("traceback 练习 - 参考解答")
    print("=" * 50)

    analyze_error()

    print("\n" + "-" * 50)
    print("处理用户数据:")
    user1 = {"name": "Bob", "email": "bob@example.com", "city": "Beijing"}
    user2 = {"name": "Carol"}

    process_user_data(user1)
    print("user1 处理成功 ✓")

    print()
    process_user_data(user2)
