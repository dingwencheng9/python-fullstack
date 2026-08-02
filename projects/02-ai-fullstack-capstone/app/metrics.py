"""Prometheus 指标导出模块

from __future__ import annotations

提供全局指标收集器，用于监控：
- HTTP 请求延迟（P50/P95/P99）
- RAG 上下文截断触发率
- 速率限制拒绝计数
- 服务健康状态
"""

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# ==============================================================================
# Global Registry
# ==============================================================================
# 使用独立注册表，避免与默认注册表冲突
registry = CollectorRegistry()

# ==============================================================================
# HTTP Metrics
# ==============================================================================
# HTTP 请求计数器（按方法、路径、状态码分组）
http_requests_total = Counter(
    name="http_requests_total",
    documentation="Total HTTP requests",
    labelnames=["method", "path", "status_code"],
    registry=registry,
)

# HTTP 请求延迟直方图（秒）
# Buckets 覆盖快速响应到慢速 LLM 流式响应的全范围
http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    documentation="HTTP request latency in seconds",
    labelnames=["method", "path"],
    buckets=(
        0.01,  # 10ms
        0.05,  # 50ms
        0.1,  # 100ms
        0.25,  # 250ms
        0.5,  # 500ms
        1.0,  # 1s
        2.5,  # 2.5s
        5.0,  # 5s
        10.0,  # 10s
        30.0,  # 30s（LLM 流式响应）
    ),
    registry=registry,
)

# HTTP 请求大小（字节）
http_request_size_bytes = Histogram(
    name="http_request_size_bytes",
    documentation="HTTP request size in bytes",
    labelnames=["method", "path"],
    registry=registry,
)

# HTTP 响应大小（字节）
http_response_size_bytes = Histogram(
    name="http_response_size_bytes",
    documentation="HTTP response size in bytes",
    labelnames=["method", "path"],
    registry=registry,
)

# ==============================================================================
# RAG Metrics
# ==============================================================================
# RAG 上下文截断计数器
rag_context_truncations_total = Counter(
    name="rag_context_truncations_total",
    documentation="Total number of RAG context truncations triggered",
    labelnames=["workspace"],
    registry=registry,
)

# RAG 上下文字符数直方图
rag_context_chars_histogram = Histogram(
    name="rag_context_chars",
    documentation="RAG context size in characters before truncation",
    labelnames=["workspace"],
    buckets=(
        500,
        1000,
        2000,
        4000,  # MAX_CONTEXT_CHARS 阈值
        8000,
        16000,
        32000,
    ),
    registry=registry,
)

# RAG 检索文档数量直方图
rag_retrieved_chunks_histogram = Histogram(
    name="rag_retrieved_chunks",
    documentation="Number of chunks retrieved from vector store",
    labelnames=["workspace"],
    buckets=(1, 3, 5, 10, 20, 50),
    registry=registry,
)

# ==============================================================================
# Rate Limiting Metrics
# ==============================================================================
# 速率限制拒绝计数器（由 Nginx 或应用层触发）
rate_limit_rejections_total = Counter(
    name="rate_limit_rejections_total",
    documentation="Total number of requests rejected by rate limiting",
    labelnames=["path"],
    registry=registry,
)

# ==============================================================================
# Application Metrics
# ==============================================================================
# 应用启动时间戳
app_start_time = Gauge(
    name="app_start_time_seconds",
    documentation="Application start time in Unix epoch seconds",
    registry=registry,
)

# 当前活跃请求数
active_requests = Gauge(
    name="active_requests",
    documentation="Number of requests currently being processed",
    labelnames=["method", "path"],
    registry=registry,
)

# ==============================================================================
# Workspace Metrics
# ==============================================================================
# Workspace 文档总数
workspace_documents_total = Gauge(
    name="workspace_documents_total",
    documentation="Total number of documents in workspace",
    labelnames=["workspace"],
    registry=registry,
)

# ==============================================================================
# Helper Functions
# ==============================================================================


def get_metrics_content() -> tuple[bytes, str]:
    """生成 Prometheus 指标内容

    Returns:
        (content, content_type) 元组
    """
    return generate_latest(registry), CONTENT_TYPE_LATEST
