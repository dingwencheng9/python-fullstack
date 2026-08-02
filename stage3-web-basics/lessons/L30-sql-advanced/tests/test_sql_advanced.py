"""L30 SQL 进阶测试。"""

from __future__ import annotations


def test_top_customers_by_category(solutions) -> None:
    module = solutions.solution_01_advanced_queries
    with module.create_learning_db() as conn:
        rows = module.top_customers_by_category(conn, limit=2)

    assert rows == [
        {"category": "book", "customer": "alice", "total_amount": 200, "row_number": 1},
        {"category": "book", "customer": "bob", "total_amount": 180, "row_number": 2},
        {"category": "tool", "customer": "carol", "total_amount": 260, "row_number": 1},
        {"category": "tool", "customer": "alice", "total_amount": 220, "row_number": 2},
    ]


def test_category_running_total(solutions) -> None:
    module = solutions.solution_01_advanced_queries
    with module.create_learning_db() as conn:
        rows = module.category_running_total(conn, "book")

    assert [row["amount"] for row in rows] == [120, 180, 70, 80]
    assert [row["running_total"] for row in rows] == [120, 300, 370, 450]


def test_common_table_expression_queries(solutions) -> None:
    module = solutions.solution_01_advanced_queries
    with module.create_learning_db() as conn:
        above_average = module.above_department_average(conn)
        paths = module.organization_paths(conn)

    assert [row["name"] for row in above_average] == ["Eve", "Ada"]
    assert {row["name"]: row["depth"] for row in paths} == {
        "Ada": 0,
        "Ben": 1,
        "Chen": 1,
        "Dora": 2,
        "Eve": 0,
        "Finn": 1,
        "Gina": 1,
    }
    assert any(row["path"] == "Ada > Ben > Dora" for row in paths)


def test_index_query_plan_uses_composite_index(solutions) -> None:
    module = solutions.solution_01_advanced_queries
    with module.create_learning_db() as conn:
        before_plan = "\n".join(module.event_query_plan(conn, 5, "purchase")).upper()
        module.create_event_lookup_index(conn)
        after_plan = "\n".join(module.event_query_plan(conn, 5, "purchase")).upper()
        rows = module.find_events(conn, 5, "purchase")

    assert "SCAN" in before_plan
    assert "IDX_EVENTS_USER_TYPE_CREATED" in after_plan
    assert "SEARCH" in after_plan
    assert rows == sorted(rows, key=lambda row: row["created_at"], reverse=True)


def test_top_customers_limit_one(solutions) -> None:
    module = solutions.solution_01_advanced_queries
    with module.create_learning_db() as conn:
        rows = module.top_customers_by_category(conn, limit=1)

    assert rows == [
        {"category": "book", "customer": "alice", "total_amount": 200, "row_number": 1},
        {"category": "tool", "customer": "carol", "total_amount": 260, "row_number": 1},
    ]
