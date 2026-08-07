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
    # ========================================
    # 👉 TODO 1: 实现日志解析
    # ========================================

    # 步骤 1: 初始化统计字典
    # stats = {'INFO': 0, 'ERROR': 0, 'WARNING': 0}

    # 步骤 2: 打开并读取文件
    # try:
    #     with open(filename, 'r', encoding='utf-8') as f:
    #         for line in f:
    #             # 步骤 3: 检查每一行包含哪种日志级别
    #             if 'INFO' in line:
    #                 stats['INFO'] += 1
    #             elif 'ERROR' in line:
    #                 stats['ERROR'] += 1
    #             elif 'WARNING' in line:
    #                 stats['WARNING'] += 1
    # except FileNotFoundError:
    #     print(f"文件 {filename} 不存在")
    #     return stats

    # 步骤 4: 返回统计结果
    # return stats

    # 💡 提示:
    # - with open() 自动关闭文件
    # - 'r' 是读取模式
    # - encoding='utf-8' 处理中文
    # - try-except 处理文件不存在的情况

    # 💡 扩展:
    # - 使用正则表达式更精确匹配
    # - 统计每种级别的具体行号
    # - 支持更多日志级别

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
    # ========================================
    # 👉 TODO 2: 实现错误行查找
    # ========================================

    # 步骤 1: 创建列表保存错误行
    # errors = []

    # 步骤 2: 打开并读取文件
    # try:
    #     with open(filename, 'r', encoding='utf-8') as f:
    #         for line_num, line in enumerate(f, 1):
    #             # 步骤 3: 检查是否包含 ERROR
    #             if 'ERROR' in line:
    #                 # 保存行号和内容
    #                 errors.append((line_num, line.strip()))
    # except FileNotFoundError:
    #     print(f"文件 {filename} 不存在")
    #     return errors

    # 步骤 4: 返回所有错误行
    # return errors

    # 💡 提示:
    # - enumerate(f, 1) 从 1 开始计数行号
    # - strip() 移除首尾空白字符
    # - 返回 (行号, 内容) 元组列表
    # - 处理文件不存在的异常

    # 💡 扩展:
    # - 支持多种错误级别（ERROR, CRITICAL）
    # - 添加上下文（前后几行）
    # - 输出到新文件

    # 💡 使用示例:
    # errors = find_errors("test.log")
    # for line_num, content in errors:
    #     print(f"Line {line_num}: {content}")

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
