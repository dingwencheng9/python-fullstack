"""L05 示例4: CSV 文件处理

学习目标:
- 掌握 CSV 文件读写
- 了解 csv 模块的使用
- 处理实际数据

示例使用临时目录，避免在课程目录留下 students.csv/new_students.csv。
"""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

# 示例数据
students = [
    ["学号", "姓名", "年龄", "成绩"],
    ["001", "张三", 20, 85],
    ["002", "李四", 21, 92],
    ["003", "王五", 19, 78],
]


# 1. 写入 CSV 文件
def write_csv(filename: str | Path, data: list[list[object]]) -> None:
    """写入 CSV 文件"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"✅ 已写入 {Path(filename).name}")


# 2. 读取 CSV 文件
def read_csv(filename: str | Path) -> list[list[str]]:
    """读取 CSV 文件"""
    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


# 3. 使用 DictReader（推荐）
def read_csv_dict(filename: str | Path) -> list[dict[str, str]]:
    """以字典形式读取 CSV"""
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


# 4. 使用 DictWriter
def write_csv_dict(filename: str | Path, data: list[dict[str, object]]) -> None:
    """以字典形式写入 CSV"""
    if not data:
        return

    fieldnames = list(data[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ 已写入 {Path(filename).name}")


# 5. 实用案例：成绩统计
def analyze_scores(filename: str | Path) -> None:
    """分析成绩"""
    students = read_csv_dict(filename)
    scores = [int(s["成绩"]) for s in students]

    print("\n=== 成绩统计 ===")
    print(f"总人数: {len(scores)}")
    print(f"平均分: {sum(scores) / len(scores):.2f}")
    print(f"最高分: {max(scores)}")
    print(f"最低分: {min(scores)}")


with TemporaryDirectory() as tmpdir:
    workspace = Path(tmpdir)
    students_path = workspace / "students.csv"
    new_students_path = workspace / "new_students.csv"

    print("=== 写入 CSV ===")
    write_csv(students_path, students)

    print("\n=== 读取 CSV ===")
    data = read_csv(students_path)
    for row in data:
        print(row)

    print("\n=== 字典方式读取 ===")
    students_dict = read_csv_dict(students_path)
    for student in students_dict:
        print(f"{student['姓名']}: {student['成绩']}分")

    print("\n=== 字典方式写入 ===")
    new_students = [
        {"学号": "004", "姓名": "赵六", "年龄": 22, "成绩": 88},
        {"学号": "005", "姓名": "孙七", "年龄": 20, "成绩": 95},
    ]
    write_csv_dict(new_students_path, new_students)

    analyze_scores(students_path)

print("\n示例结束后，临时目录会自动清理。")
