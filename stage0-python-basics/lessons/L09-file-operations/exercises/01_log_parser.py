"""L09 练习1: 日志解析器

难度: ⭐⭐☆ (中等)
预计时间: 25 分钟
知识点: 文件读取、with 语句、字符串匹配、异常处理

任务描述:
读取日志文件，统计错误数量

提示:
1. 使用 with open(filename, 'r', encoding='utf-8') as f
2. 逐行读取: for line in f
3. 使用 'ERROR' in line 判断日志级别
"""


def parse_log(filename: str) -> dict[str, int]:
    """解析日志文件

    Args:
        filename: 日志文件名

    Returns:
        字典: {'INFO': count, 'ERROR': count, 'WARNING': count}
    """
    # 实现提示：
    # 1. 初始化统计字典 stats = {'INFO': 0, 'ERROR': 0, 'WARNING': 0}
    # 2. 使用 with open(filename, 'r', encoding='utf-8') as f 打开文件
    # 3. 遍历每一行，用 'INFO'/'ERROR'/'WARNING' in line 判断级别
    # 4. try-except FileNotFoundError 处理文件不存在

    stats: dict[str, int] = {"INFO": 0, "ERROR": 0, "WARNING": 0}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if "INFO" in line:
                    stats["INFO"] += 1
                elif "ERROR" in line:
                    stats["ERROR"] += 1
                elif "WARNING" in line:
                    stats["WARNING"] += 1
    except FileNotFoundError:
        return stats
    return stats


def find_errors(filename: str) -> list[tuple[int, str]]:
    """找出所有ERROR行"""
    # 实现提示：
    # 1. 创建空列表 errors = []
    # 2. 用 enumerate(f, 1) 遍历，行号从1开始
    # 3. 'ERROR' in line 时 append((line_num, line.strip()))
    # 4. try-except FileNotFoundError

    errors: list[tuple[int, str]] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if "ERROR" in line:
                    errors.append((line_num, line.strip()))
    except FileNotFoundError:
        return errors
    return errors


if __name__ == "__main__":
    # 测试（需要先创建test.log）
    stats = parse_log("test.log")
    print(f"统计: {stats}")
