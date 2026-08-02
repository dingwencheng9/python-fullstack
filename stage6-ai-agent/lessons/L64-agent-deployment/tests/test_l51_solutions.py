"""L59 Agent 部署与监控测试用例。"""

from __future__ import annotations

import pytest

try:
    pytest.importorskip("fastapi", reason="fastapi 未安装")
    from fastapi.testclient import TestClient
except ImportError as e:
    pytest.skip(f"fastapi 未安装: {str(e)}")

# 使用 module 级别的全局变量，由 fixture 注入
HealthMetrics = None  # type: ignore[assignment]
app = None  # type: ignore[assignment]


@pytest.fixture(autouse=True)
def _inject_solutions(solutions, request) -> None:
    """从 solutions 模块动态注入被测类，避免静态导入。

    取代原先顶层的 ``import_module("solutions.xxx")`` 静态导入，
    避免依赖 sys.path 注入。测试体保持原样，运行时通过模块全局名解析。
    """
    try:
        _solution_module = getattr(solutions, "01_deployment_monitoring")
        request.module.HealthMetrics = _solution_module.HealthMetrics
        request.module.app = _solution_module.app
    except (AttributeError, ImportError) as e:
        pytest.skip(f"无法导入解决方案模块: {str(e)}")


@pytest.fixture
def client() -> TestClient:
    """共享 TestClient fixture。"""
    try:
        return TestClient(app)
    except Exception as e:
        pytest.skip(f"无法创建 TestClient: {str(e)}")


def test_health_metrics_initial_state() -> None:
    """初始状态无请求。"""
    try:
        m = HealthMetrics()
        metrics = m.get_metrics()
        assert metrics["total_requests"] == 0
        assert metrics["error_rate"] == 0
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_health_metrics_record_success() -> None:
    """成功请求不增加 error_count。"""
    try:
        m = HealthMetrics()
        m.record_request(0.1, success=True)
        m.record_request(0.2, success=True)
        metrics = m.get_metrics()
        assert metrics["total_requests"] == 2
        assert metrics["error_count"] == 0
        assert metrics["avg_duration"] == pytest.approx(0.15)
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_health_metrics_record_failure() -> None:
    """失败请求触发 error_rate。"""
    try:
        m = HealthMetrics()
        m.record_request(0.1, success=True)
        m.record_request(0.2, success=False)
        metrics = m.get_metrics()
        assert metrics["error_count"] == 1
        assert metrics["error_rate"] == 0.5
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


@pytest.mark.parametrize(
    ("successes", "failures", "expected_error_rate"),
    [
        (10, 0, 0.0),
        (0, 5, 1.0),
        (8, 2, 0.2),
        (3, 7, 0.7),
    ],
)
def test_health_metrics_error_rate_parametrized(
    successes: int,
    failures: int,
    expected_error_rate: float,
) -> None:
    """参数化：不同成功失败比例的 error_rate。"""
    try:
        m = HealthMetrics()
        for _ in range(successes):
            m.record_request(0.1, success=True)
        for _ in range(failures):
            m.record_request(0.1, success=False)
        assert m.get_metrics()["error_rate"] == pytest.approx(expected_error_rate)
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_health_metrics_empty_division_safe() -> None:
    """边界：无请求时不触发除零。"""
    try:
        m = HealthMetrics()
        metrics = m.get_metrics()
        assert metrics["error_rate"] == 0
        assert metrics["avg_duration"] == 0
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_agent_endpoint_returns_response(client: TestClient) -> None:
    """API 端点接受请求并返回结构化响应。"""
    try:
        response = client.post("/agent", json={"query": "hello", "session_id": "test"})
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tokens" in data
        assert "duration" in data
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_agent_endpoint_default_session(client: TestClient) -> None:
    """边界：未提供 session_id 时使用 default。"""
    try:
        response = client.post("/agent", json={"query": "test"})
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_health_endpoint_returns_healthy(client: TestClient) -> None:
    """/health 端点返回状态、时间戳和指标。"""
    try:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "metrics" in data
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")


def test_metrics_endpoint_returns_metrics(client: TestClient) -> None:
    """/metrics 端点返回完整健康指标。"""
    try:
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_requests" in data
        assert "error_rate" in data
        assert "avg_duration" in data
    except Exception as e:
        pytest.fail(f"测试失败: {str(e)}")
