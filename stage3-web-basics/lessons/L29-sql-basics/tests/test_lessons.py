"""L28 SQL 基础测试。"""

from __future__ import annotations

import sqlite3


def test_list_published_posts(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        rows = module.list_published_posts(conn)

    assert [row["title"] for row in rows] == ["FastAPI 路由", "SQL 基础", "HTTP 入门"]
    assert rows[0] == {
        "id": 3,
        "title": "FastAPI 路由",
        "author": "bob",
        "published_at": "2026-01-04T11:00:00",
    }


def test_count_posts_by_user(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        rows = module.count_posts_by_user(conn)

    assert rows == [
        {"username": "alice", "post_count": 2},
        {"username": "bob", "post_count": 1},
        {"username": "carol", "post_count": 1},
    ]


def test_search_posts_uses_keyword_and_filters_drafts(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        rows = module.search_posts(conn, "SQL")
        draft_rows = module.search_posts(conn, "未发布")

    assert rows == [{"id": 2, "title": "SQL 基础", "author": "alice"}]
    assert draft_rows == []


def test_create_user_and_post(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        user_id = module.create_user(conn, "dave", "dave@example.com")
        post_id = module.create_post(
            conn,
            user_id=user_id,
            title="事务入门",
            content="commit 与 rollback",
            published=True,
            published_at="2026-01-05T12:00:00",
        )
        post = conn.execute(
            """
            SELECT p.id, p.title, u.username AS author
            FROM posts p
            JOIN users u ON u.id = p.user_id
            WHERE p.id = ?
            """,
            (post_id,),
        ).fetchone()

    assert dict(post) == {"id": post_id, "title": "事务入门", "author": "dave"}


def test_unique_email_constraint(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        try:
            module.create_user(conn, "alice2", "alice@example.com")
        except sqlite3.IntegrityError as exc:
            assert "UNIQUE" in str(exc).upper()
        else:  # pragma: no cover - 防止约束失效
            raise AssertionError("重复 email 应触发唯一约束")


def test_foreign_key_constraint(solutions) -> None:
    module = solutions.solution_01_sql_basics
    with module.create_blog_db() as conn:
        try:
            module.create_post(
                conn,
                user_id=999,
                title="孤儿文章",
                content="不存在的作者",
            )
        except sqlite3.IntegrityError as exc:
            assert "FOREIGN KEY" in str(exc).upper()
        else:  # pragma: no cover - 防止约束失效
            raise AssertionError("不存在的 user_id 应触发外键约束")
