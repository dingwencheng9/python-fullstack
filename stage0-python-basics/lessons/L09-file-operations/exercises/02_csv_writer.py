"""L09 练习2: CSV 写入

难度: ⭐☆☆ (入门)
预计时间: 15 分钟
知识点: csv 模块、DictWriter、文件写入

任务描述:
编写函数 save_scores(scores: list[dict], path: str)，
将成绩列表写入 CSV 文件。

提示:
1. 使用 csv.DictWriter 处理字典数据
2. 记得调用 writeheader() 写入表头
3. 使用 with 语句确保文件正确关闭

"""

import csv  # noqa: F401 - 学员需要使用此模块完成练习


# ========================================
# 📝 练习：实现 CSV 写入函数
#
# 🎯 目标：掌握 CSV 文件的写入操作
#
# 📌 要求：
# 1. 实现 save_scores 函数
# 2. 将成绩字典列表写入 CSV 文件
# 3. CSV 文件应包含表头（字典的键）
# 4. 正确处理文件打开和关闭
#
# 💡 实现提示：
# - 使用 csv.DictWriter 处理字典数据
# - 步骤1：打开文件（'w' 模式，encoding='utf-8'）
# - 步骤2：创建 DictWriter 对象
# - 步骤3：写入表头 writeheader()
# - 步骤4：写入所有行 writerows(scores)
# - 使用 with 语句自动关闭文件
#
# ✅ 验收标准：
# - CSV 文件正确创建
# - 包含表头行
# - 所有数据正确写入
# - 文件格式符合 CSV 标准
# ========================================


def save_scores(scores: list[dict[str, str | int]], path: str) -> None:
    """将成绩列表写入 CSV 文件

    Args:
        scores: 成绩字典列表，如 [{"name": "Alice", "score": 95}, ...]
        path: CSV 文件路径

    Examples:
        >>> scores = [
        ...     {"name": "Alice", "score": 95},
        ...     {"name": "Bob", "score": 87}
        ... ]
        >>> save_scores(scores, "scores.csv")
        # 文件内容：
        # name,score
        # Alice,95
        # Bob,87
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        if not scores:
            return
        writer = csv.DictWriter(f, fieldnames=list(scores[0].keys()))
        writer.writeheader()
        writer.writerows(scores)


if __name__ == "__main__":
    # 测试代码
    test_scores = [
        {"name": "Alice", "score": 95},
        {"name": "Bob", "score": 87},
        {"name": "Charlie", "score": 92},
    ]

    print("💡 完成 save_scores 函数后，取消下面的注释测试：")
    # save_scores(test_scores, "test_scores.csv")
    # print("✅ CSV 文件已创建，请检查 test_scores.csv")
