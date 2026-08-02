"""L05 练习1参考答案"""


def parse_log(filename):
    """解析日志"""
    stats = {"INFO": 0, "ERROR": 0, "WARNING": 0}
    try:
        with open(filename, encoding="utf-8") as f:
            for line in f:
                if "INFO" in line:
                    stats["INFO"] += 1
                elif "ERROR" in line:
                    stats["ERROR"] += 1
                elif "WARNING" in line:
                    stats["WARNING"] += 1
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    return stats


def find_errors(filename):
    """找出所有 ERROR 行。

    Args:
        filename: 日志文件路径

    Returns:
        错误行列表，每个元素为 (行号, 行内容) 元组
    """
    errors: list[tuple[int, str]] = []
    try:
        with open(filename, encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                if "ERROR" in line:
                    errors.append((line_num, line.strip()))
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    return errors
