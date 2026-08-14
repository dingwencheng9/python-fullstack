"""K01 AI Agent 部署与可观测性 - 测试套件"""

import time


# ============== 配置测试 ==============


class TestConfiguration:
    """配置管理测试"""

    def test_settings_defaults(self) -> None:
        """测试默认配置"""
        from examples.environment_config import Settings

        settings = Settings()

        assert settings.app_name == "ai-agent"
        assert settings.app_version == "1.0.0"
        assert settings.debug is False
        assert settings.metrics_enabled is True

    def test_settings_custom_values(self) -> None:
        """测试自定义配置"""
        from examples.environment_config import Settings

        settings = Settings(
            app_name="custom-agent",
            debug=True,
        )

        assert settings.app_name == "custom-agent"
        assert settings.debug is True

    def test_api_key_validation(self) -> None:
        """测试 API Key 验证"""
        from examples.environment_config import validate_api_key

        # 有效格式
        assert validate_api_key("sk-test12345678") is True
        assert validate_api_key("sk-ant-api03-xxxxx") is True
        assert validate_api_key("ghp_xxxxxxxxxxxx") is True

        # 无效格式
        assert validate_api_key("") is False
        assert validate_api_key("invalid-key") is False


# ============== 指标测试 ==============


class TestMetrics:
    """Prometheus 指标测试"""

    def test_counter_increment(self) -> None:
        """测试计数器增加"""
        from examples.prometheus_metrics import Counter

        counter = Counter("test_counter", "Test counter")
        counter.inc()
        counter.inc(5)

        assert counter.value == 6

    def test_histogram_observe(self) -> None:
        """测试直方图观察"""
        from examples.prometheus_metrics import Histogram

        histogram = Histogram("test_histogram", "Test histogram")
        histogram.observe(0.1)
        histogram.observe(0.5)
        histogram.observe(1.0)

        assert histogram._count == 3
        assert histogram._sum == 1.6

    def test_gauge_set_value(self) -> None:
        """测试仪表设置值"""
        from examples.prometheus_metrics import Gauge

        gauge = Gauge("test_gauge", "Test gauge")
        gauge.set(10)
        gauge.inc(5)
        gauge.dec(3)

        assert gauge.value == 12


# ============== 追踪测试 ==============


class TestTracing:
    """分布式追踪测试"""

    def test_tracer_create_span(self) -> None:
        """测试创建追踪跨度"""
        from examples.otel_tracing import Tracer, SpanStatus

        tracer = Tracer("test-service")
        span = tracer.start_span("test-span")

        assert span.name == "test-span"
        assert span.status == SpanStatus.UNSET
        assert span.trace_id is not None
        assert span.span_id is not None

    def test_span_attributes(self) -> None:
        """测试跨度属性"""
        from examples.otel_tracing import Tracer

        tracer = Tracer("test-service")
        span = tracer.start_span("test-span")

        span.set_attribute("key1", "value1")
        span.set_attribute("key2", 123)

        assert span.attributes["key1"] == "value1"
        assert span.attributes["key2"] == 123

    def test_span_duration(self) -> None:
        """测试跨度持续时间"""
        from examples.otel_tracing import Tracer

        tracer = Tracer("test-service")
        span = tracer.start_span("test-span")
        time.sleep(0.05)
        span.end()

        assert span.duration >= 0.05
        assert span.end_time is not None


# ============== 日志测试 ==============


class TestLogging:
    """结构化日志测试"""

    def test_log_level_filtering(self) -> None:
        """测试日志级别过滤"""
        from examples.structured_logging import StructuredLogger, LogLevel

        logger = StructuredLogger("test", min_level=LogLevel.WARNING)

        logger.debug("debug message")  # 应该被过滤
        logger.info("info message")  # 应该被过滤
        logger.warning("warning message")  # 应该记录

        assert len(logger.records) == 1
        assert logger.records[0].level == "WARNING"

    def test_agent_logger(self) -> None:
        """测试 Agent 日志记录"""
        from examples.structured_logging import AgentLogger

        agent_log = AgentLogger("test")

        agent_log.log_request(
            user_id="user_123",
            request_id="req_001",
            duration_ms=150.5,
            status="success",
        )

        assert len(agent_log.records) == 1
        assert agent_log.records[0].context["user_id"] == "user_123"
        assert agent_log.records[0].context["duration_ms"] == 150.5

    def test_cost_logging(self) -> None:
        """测试成本日志"""
        from examples.structured_logging import AgentLogger

        agent_log = AgentLogger("test")

        agent_log.log_cost(
            user_id="user_123",
            model="gpt-4o-mini",
            tokens=1000,
            cost_usd=0.0015,
        )

        assert len(agent_log.records) == 1
        assert agent_log.records[0].context["tokens"] == 1000
        assert agent_log.records[0].context["cost_usd"] == 0.0015


# ============== 健康检查测试 ==============


class TestHealthCheck:
    """健康检查测试"""

    def test_health_status(self) -> None:
        """测试健康状态"""
        from examples.dockerfile_agent import AgentServer

        server = AgentServer()
        health = server.health_check()

        assert health.status == "healthy"
        assert health.version == "1.0.0"
        assert all(health.checks.values())

    def test_readiness_check(self) -> None:
        """测试就绪检查"""
        from examples.dockerfile_agent import AgentServer

        server = AgentServer()
        ready = server.readiness_check()

        assert ready["ready"] is True
        assert ready["status_code"] == 200
