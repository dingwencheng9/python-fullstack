"""
练习题 3 参考解答: 分布式追踪集成
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from datetime import datetime
import time
import uuid
import json


@dataclass
class Span:
    """追踪跨度"""

    name: str
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: dict = field(default_factory=dict)
    events: list = field(default_factory=list)
    status: str = "UNSET"

    def set_attribute(self, key: str, value: Any) -> None:
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

    def end(self, status: str = "OK") -> None:
        """结束跨度"""
        self.end_time = time.time()
        self.status = status

    @property
    def duration_ms(self) -> float:
        """获取持续时间（毫秒）"""
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return (time.time() - self.start_time) * 1000

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat()
            if self.end_time
            else None,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
        }


class Tracer:
    """追踪器"""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: list[Span] = []
        self._current_span: Optional[Span] = None

    def start_span(self, name: str, parent: Optional[Span] = None) -> Span:
        """启动新的跨度"""
        span = Span(
            name=name,
            parent_id=parent.span_id if parent else None,
        )
        span.set_attribute("service.name", self.service_name)
        self._current_span = span
        return span

    def end_span(self, span: Span, status: str = "OK") -> None:
        """结束跨度"""
        span.end(status)
        self.spans.append(span)
        self._current_span = span.parent_id

    def get_trace(self, trace_id: str) -> list[Span]:
        """获取指定 Trace 的所有跨度"""
        return [s for s in self.spans if s.trace_id == trace_id]

    @property
    def current_span(self) -> Optional[Span]:
        """获取当前跨度"""
        return self._current_span


class TracingContext:
    """追踪上下文管理器"""

    def __init__(self, tracer: Tracer, name: str):
        self.tracer = tracer
        self.name = name
        self.span: Optional[Span] = None

    def __enter__(self) -> Span:
        self.span = self.tracer.start_span(self.name, self.tracer._current_span)
        return self.span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.span:
            status = "OK" if exc_type is None else "ERROR"
            self.tracer.end_span(self.span, status)


def traced(tracer: Tracer, span_name: str):
    """追踪装饰器"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            with TracingContext(tracer, span_name) as span:
                span.set_attribute("function.name", func.__name__)

                # 记录函数参数
                if args:
                    span.set_attribute("args.count", len(args))
                if kwargs:
                    span.set_attribute("kwargs.keys", list(kwargs.keys()))

                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    span.add_event(
                        "exception",
                        {
                            "type": type(e).__name__,
                            "message": str(e),
                        },
                    )
                    span.status = "ERROR"
                    raise

        # 复制函数属性
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


def inject_context(headers: dict) -> dict:
    """将追踪上下文注入到 HTTP 头"""
    # 简化实现：存储当前 trace_id 和 span_id
    return {
        "X-Trace-Id": headers.get("trace_id", uuid.uuid4().hex[:16]),
        "X-Parent-Span-Id": headers.get("span_id", ""),
    }


def extract_context(headers: dict) -> Optional[dict]:
    """从 HTTP 头提取追踪上下文"""
    trace_id = headers.get("X-Trace-Id")
    parent_span_id = headers.get("X-Parent-Span-Id")

    if trace_id:
        return {
            "trace_id": trace_id,
            "parent_span_id": parent_span_id,
        }
    return None


def export_traces(tracer: Tracer, format: str = "json") -> str:
    """导出追踪数据"""
    if format == "json":
        return json.dumps([s.to_dict() for s in tracer.spans], indent=2, default=str)
    elif format == "otlp":
        # 简化的 OTLP 格式
        return json.dumps(
            {
                "resourceSpans": [
                    {
                        "resource": {
                            "attributes": [
                                {
                                    "key": "service.name",
                                    "value": {"stringValue": tracer.service_name},
                                }
                            ]
                        },
                        "scopeSpans": [{"spans": [s.to_dict() for s in tracer.spans]}],
                    }
                ]
            },
            indent=2,
            default=str,
        )
    else:
        raise ValueError(f"Unsupported format: {format}")


# ============== 示例 ==============


@traced(Tracer("example-agent"), "agent.llm.call")
def call_llm(prompt: str) -> str:
    """模拟 LLM 调用"""
    time.sleep(0.1)
    return f"Response to: {prompt[:20]}..."


@traced(Tracer("example-agent"), "agent.tool.execute")
def execute_tool(tool_name: str, args: dict) -> dict:
    """模拟工具执行"""
    time.sleep(0.05)
    return {"success": True, "result": f"Executed {tool_name}"}


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 3 参考解答: 分布式追踪集成")
    print("=" * 60)

    # 创建追踪器
    tracer = Tracer("ai-agent")

    # 1. 基本追踪
    print("\n--- 基本追踪 ---")
    with TracingContext(tracer, "agent.request") as span:
        span.set_attribute("request.id", "req_001")
        span.set_attribute("user.id", "user_123")

        # LLM 调用
        response = call_llm("Hello!")
        print(f"LLM 响应: {response[:30]}...")

        # 工具调用
        result = execute_tool("search", {"query": "test"})
        print(f"工具结果: {result}")

    # 2. 上下文传播
    print("\n--- 上下文传播 ---")
    headers = {"trace_id": "abc123", "span_id": "def456"}
    injected = inject_context(headers)
    print(f"注入的上下文: {injected}")

    extracted = extract_context(injected)
    print(f"提取的上下文: {extracted}")

    # 3. 导出追踪
    print("\n--- 导出追踪 ---")
    trace_id = tracer.spans[0].trace_id if tracer.spans else None
    if trace_id:
        trace = tracer.get_trace(trace_id)
        print(f"Trace {trace_id} 包含 {len(trace)} 个 Span")

    # JSON 导出
    json_output = export_traces(tracer, "json")
    print(f"\nJSON 导出长度: {len(json_output)} 字符")

    # 4. 统计信息
    print("\n--- 统计信息 ---")
    print(f"总 Span 数: {len(tracer.spans)}")

    root_spans = [s for s in tracer.spans if s.parent_id is None]
    print(f"根 Span 数: {len(root_spans)}")

    total_duration = sum(s.duration_ms for s in tracer.spans)
    print(f"总持续时间: {total_duration:.2f}ms")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert len(tracer.spans) > 0, "应该有记录的 Span"
    assert len(root_spans) >= 1, "应该有根 Span"

    # 验证追踪树结构
    span_ids = {s.span_id for s in tracer.spans}
    parent_ids = {s.parent_id for s in tracer.spans if s.parent_id}
    assert parent_ids.issubset(span_ids | {None}), "所有 parent_id 应该指向有效的 span_id"

    print("✅ 分布式追踪验证通过!")


if __name__ == "__main__":
    main()
