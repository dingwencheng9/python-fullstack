"""
示例 7: 多 Agent 子图协作

展示如何使用子图实现多 Agent 协作。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add


# ============== 子图状态 ==============


class ResearchState(TypedDict):
    """研究 Agent 状态"""

    topic: str
    sources: list[str]
    findings: list[str]


class CoordinatorState(TypedDict):
    """协调 Agent 状态"""

    task: str
    research_results: Annotated[list[dict], add]
    writing: dict
    final_output: str | None


# ============== 研究 Agent ==============


def search_sources(state: ResearchState) -> ResearchState:
    """搜索相关资料"""
    topic = state["topic"]
    sources = [f"source_{i}_for_{topic}" for i in range(3)]
    return {"sources": sources}


def analyze_sources(state: ResearchState) -> ResearchState:
    """分析资料并提取发现"""
    sources = state.get("sources", [])
    findings = [f"finding from {s}" for s in sources]
    return {"findings": findings}


# ============== 协调 Agent ==============


def run_research(state: CoordinatorState) -> CoordinatorState:
    """运行研究子图"""
    # 构建并执行研究子图
    research_builder = StateGraph(ResearchState)
    research_builder.add_node("search", search_sources)
    research_builder.add_node("analyze", analyze_sources)
    research_builder.add_edge(START, "search")
    research_builder.add_node(
        "write_outline", lambda s: {"findings": s["findings"] + ["已生成大纲"]}
    )
    research_builder.add_edge("search", "analyze")
    research_builder.add_edge("analyze", "write_outline")
    research_builder.add_edge("write_outline", END)
    research_graph = research_builder.compile()

    result = research_graph.invoke({"topic": state["task"], "sources": [], "findings": []})

    return {
        "research_results": [
            {
                "topic": result["topic"],
                "findings": result["findings"],
            }
        ]
    }


def compile_results(state: CoordinatorState) -> CoordinatorState:
    """编译最终结果"""
    research = state.get("research_results", [])
    findings_text = "\n".join(f"  - {f}" for r in research for f in r.get("findings", []))

    output = f"""任务: {state["task"]}

研究发现:
{findings_text}

写作内容: 基于研究结果生成
"""
    return {"final_output": output}


def main() -> None:
    """主函数：构建多 Agent 协作系统"""
    builder = StateGraph(CoordinatorState)

    builder.add_node("research", run_research)
    builder.add_node("compile", compile_results)

    builder.add_edge(START, "research")
    builder.add_edge("research", "compile")
    builder.add_edge("compile", END)

    graph = builder.compile()

    # 执行
    result = graph.invoke(
        {
            "task": "Python 异步编程最佳实践",
            "research_results": [],
            "writing": {},
            "final_output": None,
        }
    )

    print("=" * 60)
    print("多 Agent 协作测试")
    print("=" * 60)

    print(f"\n任务: {result['task']}")
    print("\n研究结果:")
    for r in result["research_results"]:
        print(f"  主题: {r['topic']}")
        for f in r["findings"]:
            print(f"    - {f}")

    print("\n最终输出:")
    print(result["final_output"])

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert result["task"] == "Python 异步编程最佳实践"
    assert len(result["research_results"]) == 1
    assert result["final_output"] is not None
    print("✅ 多 Agent 协作验证通过!")


if __name__ == "__main__":
    main()
