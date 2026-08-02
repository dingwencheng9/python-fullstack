"""
练习题 3: 分布式追踪集成

将 OpenTelemetry 追踪集成到 Agent 代码中：
1. 配置追踪提供者
2. 创建追踪装饰器
3. 为 LLM 调用和工具执行添加追踪

要求：
- 追踪跨度包含必要的属性（model, tool_name, duration）
- 支持上下文传播
- 生成可导出的追踪数据
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Any
import time
import uuid


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


class Tracer:
    """
    追踪器

    TODO: 实现以下功能
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: list[Span] = []
        self._current_span: Optional[Span] = None

    def start_span(self, name: str, parent: Optional[Span] = None) -> Span:
        """启动新的跨度"""
        raise NotImplementedError("需要实现")

    def end_span(self, span: Span, status: str = "OK") -> None:
        """结束跨度"""
        raise NotImplementedError("需要实现")

    def get_trace(self, trace_id: str) -> list[Span]:
        """获取指定 Trace 的所有跨度"""
        raise NotImplementedError("需要实现")


def traced(tracer: Tracer, span_name: str):
    """
    追踪装饰器

    用法:
        @traced(my_tracer, "agent.llm.call")
        async def call_llm(prompt: str) -> str:
            ...
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # TODO: 实现追踪逻辑
            raise NotImplementedError("需要实现")

        return wrapper

    return decorator


class TracingContext:
    """
    追踪上下文管理器

    用法:
        tracer = Tracer("my-agent")
        with TracingContext(tracer, "operation.name") as span:
            span.set_attribute("key", "value")
            # 执行操作
    """

    def __init__(self, tracer: Tracer, name: str):
        raise NotImplementedError("需要实现")

    def __enter__(self) -> Span:
        raise NotImplementedError("需要实现")

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError("需要实现")


def inject_context(headers: dict) -> dict:
    """
    将追踪上下文注入到 HTTP 头

    用于服务间调用时的上下文传播
    """
    raise NotImplementedError("需要实现")


def extract_context(headers: dict) -> Optional[dict]:
    """
    从 HTTP 头提取追踪上下文

    用于接收上游服务的追踪上下文
    """
    raise NotImplementedError("需要实现")


def export_traces(tracer: Tracer, format: str = "json") -> str:
    """
    导出追踪数据

    支持格式: json, otlp
    """
    raise NotImplementedError("需要实现")


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 3: 分布式追踪集成")
    print("=" * 60)

    print("\n任务：")
    print("1. 实现 Tracer 类")
    print("2. 实现 TracingContext 上下文管理器")
    print("3. 实现 traced 装饰器")
    print("4. 实现上下文注入/提取函数")
    print("5. 实现导出功能")

    print("\n提示：")
    print("- 每个 Trace 有一个 trace_id")
    print("- Span 有 parent_id 形成调用链")
    print("- 属性包含 key-value 对")

    print("\n完成后运行示例代码测试追踪功能")


if __name__ == "__main__":
    main()
