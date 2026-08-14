"""
示例 4: OpenTelemetry 分布式追踪

展示如何配置和使用分布式追踪。
"""

import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid


class SpanStatus(Enum):
    """Span 状态"""

    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


@dataclass
class Span:
    """Span 实现"""

    name: str
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    parent_id: Optional[str] = None
    status: SpanStatus = SpanStatus.UNSET
    attributes: dict = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    events: list = field(default_factory=list)

    def set_attribute(self, key: str, value) -> None:
        """设置属性"""
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict = None) -> None:
        """添加事件"""
        self.events.append(
            {
                "name": name,
                "attributes": attributes or {},
                "timestamp": time.time(),
            }
        )

    def set_status(self, status: SpanStatus, description: str = "") -> None:
        """设置状态"""
        self.status = status

    def end(self) -> None:
        """结束 Span"""
        self.end_time = time.time()

    @property
    def duration(self) -> float:
        """获取持续时间"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time


class Tracer:
    """追踪器实现"""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: list[Span] = []

    def start_span(self, name: str, parent: Optional[Span] = None) -> Span:
        """启动新的 Span"""
        span = Span(
            name=name,
            parent_id=parent.span_id if parent else None,
        )
        span.set_attribute("service.name", self.service_name)
        return span

    def record_span(self, span: Span) -> None:
        """记录 Span"""
        self.spans.append(span)

    def get_trace(self, trace_id: str) -> list[Span]:
        """获取指定 Trace 的所有 Span"""
        return [s for s in self.spans if s.trace_id == trace_id]


# 全局追踪器
tracer = Tracer(service_name="ai-agent")


class SpanContext:
    """Span 上下文管理器"""

    def __init__(self, tracer: Tracer, name: str):
        self.tracer = tracer
        self.name = name
        self.span: Optional[Span] = None

    def __enter__(self) -> Span:
        self.span = self.tracer.start_span(self.name)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            if exc_type:
                self.span.set_status(SpanStatus.ERROR, str(exc_val))
                self.span.add_event(
                    "exception",
                    {
                        "type": exc_type.__name__,
                        "message": str(exc_val),
                    },
                )
            else:
                self.span.set_status(SpanStatus.OK)
            self.span.end()
            self.tracer.record_span(self.span)


def traced(name: str):
    """追踪装饰器"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with SpanContext(tracer, name) as span:
                span.set_attribute("function.name", func.__name__)
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    span.set_status(SpanStatus.ERROR, str(e))
                    raise

        return wrapper

    return decorator


# ============== 示例函数 ==============


@traced("agent.llm.call")
def call_llm(prompt: str) -> str:
    """LLM 调用"""
    with SpanContext(tracer, "llm.request") as span:
        span.set_attribute("llm.model", "gpt-4")
        span.set_attribute("prompt.length", len(prompt))

        time.sleep(0.5)  # 模拟 LLM 调用

        response = f"Response to: {prompt[:20]}..."
        span.set_attribute("response.length", len(response))
        return response


@traced("agent.tool.execute")
def execute_tool(tool_name: str, args: dict) -> dict:
    """执行工具"""
    with SpanContext(tracer, "tool.execution") as span:
        span.set_attribute("tool.name", tool_name)

        time.sleep(0.1)  # 模拟工具执行

        return {"success": True, "result": f"Executed {tool_name}"}


# ============== 主函数 ==============


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("OpenTelemetry 分布式追踪示例")
    print("=" * 60)

    # 1. 模拟请求处理
    print("\n--- 模拟请求处理 ---")

    with SpanContext(tracer, "agent.request") as root_span:
        root_span.set_attribute("request.id", "req_001")
        root_span.set_attribute("user.id", "user_123")

        # LLM 调用
        response = call_llm("Hello, how are you?")
        print(f"LLM 响应: {response[:30]}...")

        # 工具调用
        result = execute_tool("search", {"query": "test"})
        print(f"工具结果: {result}")

    # 2. 输出追踪信息
    print("\n--- 追踪信息 ---")
    print(f"总 Span 数: {len(tracer.spans)}")

    for span in tracer.spans:
        print(f"\n  Span: {span.name}")
        print(f"    Trace ID: {span.trace_id}")
        print(f"    Span ID: {span.span_id}")
        print(f"    Parent ID: {span.parent_id or 'None'}")
        print(f"    Duration: {span.duration:.4f}s")
        print(f"    Status: {span.status.value}")
        print(f"    Attributes: {span.attributes}")

    # 3. 生成 OTLP 格式输出（简化版）
    print("\n--- OTLP 格式输出（简化） ---")
    for span in tracer.spans[:3]:  # 只显示前 3 个
        otlp_data = {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": "ai-agent"}}
                        ]
                    },
                    "scopeSpans": [
                        {
                            "spans": [
                                {
                                    "traceId": span.trace_id,
                                    "spanId": span.span_id,
                                    "name": span.name,
                                    "durationNanos": int(span.duration * 1_000_000_000),
                                    "status": {"code": span.status.value.upper()},
                                }
                            ]
                        }
                    ],
                }
            ]
        }
        print(
            f"  {span.name}: {otlp_data['resourceSpans'][0]['scopeSpans'][0]['spans'][0]['name']}"
        )

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert len(tracer.spans) > 0, "应该有记录的 Span"

    # 按 trace_id 分组验证
    traces: dict[str, list[Span]] = {}
    for span in tracer.spans:
        if span.trace_id not in traces:
            traces[span.trace_id] = []
        traces[span.trace_id].append(span)

    # 应该有至少 1 个 trace
    assert len(traces) >= 1, "应该有至少 1 个 trace"

    # 每个 trace 应该有 1 个根 Span（parent_id 为 None）
    for trace_id, spans in traces.items():
        root_spans = [s for s in spans if s.parent_id is None]
        assert len(root_spans) >= 1, f"Trace {trace_id} 应该有至少 1 个根 Span"

    print("✅ 分布式追踪验证通过!")


if __name__ == "__main__":
    main()
