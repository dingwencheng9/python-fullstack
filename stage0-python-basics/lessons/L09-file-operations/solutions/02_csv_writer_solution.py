"""练习 2 答案。"""

import csv


def save_scores(scores: list[dict[str, str | int]], path: str) -> None:
    """将成绩列表写入 CSV 文件。

    空列表时创建一个空文件并直接返回；非空时使用首行字典的键作为表头。
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        if not scores:
            return
        w = csv.DictWriter(f, fieldnames=list(scores[0].keys()))
        w.writeheader()
        w.writerows(scores)
