"""
L55 示例: 生产部署与监控

学习目标:
- 图序列化与 JSON 导出
- FastAPI 集成（伪实现）
- Prometheus 监控指标模拟
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GraphNode:
    """简化版图节点。"""

    name: str
    node_type: str  # "agent" | "tool" | "supervisor"


@dataclass
class GraphEdge:
    """简化版图边。"""

    source: str
    target: str


class MockGraph:
    """简化版编译后 LangGraph 图（用于测试序列化）。"""

    def __init__(self, name: str = "agent_graph") -> None:
        self.name = name
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, name: str, node_type: str = "agent") -> None:
        self.nodes[name] = GraphNode(name=name, node_type=node_type)

    def add_edge(self, source: str, target: str) -> None:
        self.edges.append(GraphEdge(source=source, target=target))

    def get_graph_def(self) -> dict:
        return {
            "name": self.name,
            "nodes": list(self.nodes.keys()),
            "edges": [{"from": e.source, "to": e.target} for e in self.edges],
        }


class PrometheusMetrics:
    """简化版 Prometheus 指标，模拟 Counter/Histogram/Gauge。"""

    def __init__(self) -> None:
        self._counters: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = {}
        self._gauges: dict[str, float] = {}

    def counter(self, name: str, labels: dict | None = None) -> None:
        key = f"{name}:{labels or {}}"
        self._counters[key] = self._counters.get(key, 0) + 1

    def histogram(self, name: str, value: float) -> None:
        if name not in self._histograms:
            self._histograms[name] = []
        self._histograms[name].append(value)

    def gauge(self, name: str, value: float) -> None:
        self._gauges[name] = value

    def get(self, name: str) -> float | list[float] | None:
        if name in self._counters:
            return self._counters[name]
        if name in self._histograms:
            return self._histograms[name]
        if name in self._gauges:
            return self._gauges[name]
        return None


# --- 演示运行 ---
if __name__ == "__main__":
    print("=== 1. 图序列化 ===")
    app = MockGraph(name="code_review_graph")
    app.add_node("supervisor", "supervisor")
    app.add_node("coder", "agent")
    app.add_node("reviewer", "agent")
    app.add_edge("supervisor", "coder")
    app.add_edge("coder", "reviewer")
    app.add_edge("reviewer", "supervisor")

    graph_def = app.get_graph_def()
    print(f"图名称: {graph_def['name']}")
    print(f"节点: {graph_def['nodes']}")
    print(f"边: {graph_def['edges']}")

    print("\n=== 2. Prometheus 监控 ===")
    metrics = PrometheusMetrics()
    metrics.counter("langgraph_invocations_total", {"graph": "code_review", "status": "success"})
    metrics.counter("langgraph_invocations_total", {"graph": "code_review", "status": "success"})
    metrics.histogram("langgraph_invocation_duration_seconds", 0.45)
    metrics.histogram("langgraph_invocation_duration_seconds", 1.23)
    metrics.gauge("langgraph_active_threads", 3)

    print(f"  调用次数: {metrics.get('langgraph_invocations_total', {'graph': 'code_review', 'status': 'success'})}")
    print(f"  响应时间: {metrics.get('langgraph_invocation_duration_seconds')}")
    print(f"  活跃线程: {metrics.get('langgraph_active_threads')}")
