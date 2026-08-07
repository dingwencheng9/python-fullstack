"""L35 Docker 容器化基础测试。"""

from __future__ import annotations

from pathlib import Path

import pytest
from solutions.solution_01_validate_dockerfile import validate_dockerfile
from solutions.solution_02_validate_compose import validate_compose

LESSON_DIR = Path(__file__).parent.parent


def test_dockerfile_example_exists():
    path = LESSON_DIR / "examples" / "Dockerfile.fastapi"
    assert path.exists()
    assert "FROM python:3.13-slim" in path.read_text()


def test_compose_example_exists():
    path = LESSON_DIR / "examples" / "docker-compose.yml"
    assert path.exists()
    content = path.read_text()
    assert "services:" in content
    assert "redis:" in content


def test_validate_dockerfile_success():
    text = """
FROM python:3.13-slim
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
"""
    assert validate_dockerfile(text) == []


@pytest.mark.parametrize("missing_keyword", ["FROM", "WORKDIR", "COPY"])
def test_validate_dockerfile_missing_required(missing_keyword: str):
    text = "FROM python:3.13\nWORKDIR /app\nCOPY . .\nCMD python app.py"
    text = text.replace(missing_keyword, "")
    errors = validate_dockerfile(text)
    assert any(missing_keyword in e for e in errors)


def test_validate_dockerfile_missing_cmd():
    text = "FROM python:3.13\nWORKDIR /app\nCOPY . ."
    errors = validate_dockerfile(text)
    assert any("CMD" in e or "ENTRYPOINT" in e for e in errors)


def test_validate_compose_success():
    config = {
        "services": {
            "api": {"ports": ["8000:8000"], "depends_on": ["redis"]},
            "redis": {"volumes": ["redis_data:/data"]},
        }
    }
    assert validate_compose(config) == []


def test_validate_compose_missing_services():
    assert validate_compose({}) == ["missing services"]


@pytest.mark.parametrize(
    "config,expected",
    [
        ({"services": {"redis": {"volumes": ["v:/data"]}}}, "missing api"),
        (
            {"services": {"api": {"depends_on": ["redis"]}, "redis": {"volumes": ["v:/data"]}}},
            "ports",
        ),
        (
            {"services": {"api": {"ports": ["8000:8000"]}, "redis": {"volumes": ["v:/data"]}}},
            "depend",
        ),
        (
            {"services": {"api": {"ports": ["8000:8000"], "depends_on": ["redis"]}, "redis": {}}},
            "volume",
        ),
    ],
)
def test_validate_compose_errors(config: dict, expected: str):
    errors = validate_compose(config)
    assert any(expected in e for e in errors)
