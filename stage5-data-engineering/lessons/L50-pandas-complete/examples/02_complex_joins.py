"""示例 2: 复杂连接操作

展示多种连接方式：
- merge 的各种 join 类型
- concat 高级用法
- 复合键连接
"""

from __future__ import annotations

import pandas as pd


def create_employees() -> pd.DataFrame:
    """创建员工数据"""
    return pd.DataFrame(
        {
            "emp_id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "dept_id": [101, 102, 101, 103, 102],
            "salary": [50000, 60000, 55000, 70000, 65000],
        }
    )


def create_departments() -> pd.DataFrame:
    """创建部门数据"""
    return pd.DataFrame(
        {
            "dept_id": [101, 102, 103, 104],
            "dept_name": ["Engineering", "Sales", "Marketing", "HR"],
            "location": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen"],
        }
    )


def create_salaries() -> pd.DataFrame:
    """创建薪资历史数据"""
    return pd.DataFrame(
        {
            "emp_id": [1, 1, 2, 2, 3, 5],
            "year": [2022, 2023, 2022, 2023, 2023, 2023],
            "salary": [45000, 50000, 55000, 60000, 50000, 60000],
            "bonus": [5000, 6000, 7000, 8000, 5500, 7000],
        }
    )


def basic_merge(employees: pd.DataFrame, departments: pd.DataFrame) -> pd.DataFrame:
    """基础 merge 操作"""
    # 内连接 - 只保留两边都有的键
    inner = pd.merge(employees, departments, on="dept_id", how="inner")
    print("内连接:\n", inner)

    # 左连接 - 保留左边所有记录
    left = pd.merge(employees, departments, on="dept_id", how="left")
    print("\n左连接:\n", left)

    # 右连接 - 保留右边所有记录
    right = pd.merge(employees, departments, on="dept_id", how="right")
    print("\n右连接:\n", right)

    # 全外连接 - 保留所有记录
    outer = pd.merge(employees, departments, on="dept_id", how="outer")
    print("\n全外连接:\n", outer)

    return inner


def multiple_keys_merge() -> pd.DataFrame:
    """复合键连接"""
    df1 = pd.DataFrame(
        {
            "year": [2020, 2021, 2020, 2021],
            "quarter": ["Q1", "Q1", "Q2", "Q2"],
            "region": ["North", "North", "South", "South"],
            "sales": [100, 150, 200, 250],
        }
    )

    df2 = pd.DataFrame(
        {
            "year": [2020, 2020, 2021, 2021],
            "quarter": ["Q1", "Q2", "Q1", "Q2"],
            "region": ["North", "North", "South", "South"],
            "target": [90, 180, 220, 280],
        }
    )

    result = pd.merge(df1, df2, on=["year", "quarter", "region"])
    print("\n复合键连接:\n", result)
    return result


def concat_examples() -> None:
    """concat 高级用法"""
    df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})
    df3 = pd.DataFrame({"C": [9, 10], "D": [11, 12]})

    # 列拼接
    concat_cols = pd.concat([df1, df2], axis=1)
    print("\n列拼接:\n", concat_cols)

    # 行拼接
    concat_rows = pd.concat([df1, df3], axis=1)
    print("\n行拼接（不同列）:\n", concat_rows)

    # 忽略索引
    concat_ignore = pd.concat([df1, df2], ignore_index=True)
    print("\n忽略索引:\n", concat_ignore)

    # 层次化索引
    concat_keys = pd.concat([df1, df2], keys=["first", "second"])
    print("\n层次化索引:\n", concat_keys)


def cross_join() -> pd.DataFrame:
    """交叉连接（笛卡尔积）"""
    colors = pd.DataFrame({"color": ["红", "绿", "蓝"]})
    sizes = pd.DataFrame({"size": ["S", "M", "L"]})

    result = pd.merge(colors, sizes, how="cross")
    print("\n交叉连接:\n", result)
    return result


def update_with_merge() -> pd.DataFrame:
    """使用 merge 更新数据"""
    original = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "score": [85, 90, 78],
        }
    )

    updates = pd.DataFrame(
        {
            "id": [2, 3, 4],
            "score": [95, 82, 88],
        }
    )

    # 使用 map 更新
    score_map = updates.set_index("id")["score"].to_dict()
    original["score"] = original["id"].map(score_map).fillna(original["score"])
    print("\n使用 map 更新:\n", original)

    return original


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("复杂连接操作示例")
    print("=" * 60)

    employees = create_employees()
    departments = create_departments()
    salaries = create_salaries()

    print("员工数据:\n", employees)
    print("\n部门数据:\n", departments)
    print("\n薪资历史:\n", salaries)

    print("\n" + "=" * 60)
    print("基础 merge")
    print("=" * 60)
    basic_merge(employees, departments)

    print("\n" + "=" * 60)
    print("复合键连接")
    print("=" * 60)
    multiple_keys_merge()

    print("\n" + "=" * 60)
    print("concat 示例")
    print("=" * 60)
    concat_examples()

    print("\n" + "=" * 60)
    print("交叉连接")
    print("=" * 60)
    cross_join()


if __name__ == "__main__":
    main()
