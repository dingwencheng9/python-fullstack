"""

from __future__ import annotations

L21 练习题参考答案: 研究员 + 审稿人双 Agent 写作流

完整实现包含：
1. 清晰的状态定义
2. Researcher 和 Reviewer Agent 实现
3. 迭代修订机制
4. Human-in-the-Loop 集成
5. 完整的路由逻辑

运行方式:
    python solutions/research_writing_flow.py
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


# ============================================================================
# 第一步: 定义状态结构
# ============================================================================
class AcademicWritingState(TypedDict):
    """
    学术写作工作流状态

    Attributes:
        messages: 消息历史（累加）
        topic: 论文主题
        draft_content: 当前草稿内容
        review_feedback: 审稿人反馈
        quality_score: 质量评分 (0-100)
        revision_count: 修订次数
        approved: 是否最终批准
    """

    messages: Annotated[list[BaseMessage], operator.add]
    topic: str
    draft_content: str
    review_feedback: str
    quality_score: int
    revision_count: int
    approved: bool


# ============================================================================
# 第二步: 实现 Researcher Agent 节点
# ============================================================================
def researcher_node(state: AcademicWritingState) -> dict:
    """
    Researcher Agent: 生成或修订论文内容

    逻辑:
    1. 如果是首次生成 (revision_count == 0):
       - 根据 topic 生成初稿
       - 包含: 摘要、引言、方法、结果、结论
    2. 如果是修订 (revision_count > 0):
       - 根据 review_feedback 改进内容

    返回:
    - 更新 draft_content
    - 添加 AIMessage 到 messages
    """
    revision_count = state["revision_count"]
    topic = state["topic"]

    if revision_count == 0:
        # 首次生成初稿
        print(f"\n📝 Researcher Agent: 生成初稿（主题: {topic}）...")

        draft = f"""
# {topic}

## 摘要
本文探讨了{topic}的理论基础和实际应用。通过系统性分析，
我们阐明了该领域的关键技术挑战和未来发展方向。

## 1. 引言
近年来，量子计算技术取得了突破性进展。本文聚焦于其在密码学
领域的应用，分析了量子算法对现有加密体系的影响。

## 2. 理论基础
### 2.1 量子计算原理
量子计算利用量子叠加和量子纠缠实现并行计算。

### 2.2 现代密码学体系
当前密码学基于数学难题（如大数分解）的计算复杂度。

## 3. 量子算法对密码学的影响
### 3.1 Shor 算法
可以在多项式时间内分解大整数，威胁 RSA 等公钥密码。

### 3.2 Grover 算法
可以加速对称密钥搜索，需要增加密钥长度应对。

## 4. 后量子密码学
### 4.1 格密码
基于格问题的密码方案，抗量子攻击。

### 4.2 基于编码的密码
利用纠错码的数学难题。

## 5. 结论
量子计算对密码学既是挑战也是机遇。后量子密码学的研究至关重要。

## 参考文献
[1] Shor, P. W. (1997). Polynomial-time algorithms...
[2] Grover, L. K. (1996). A fast quantum mechanical algorithm...
        """
        message_content = f"已生成初稿，共约 {len(draft.split())} 词"

    else:
        # 修订草稿
        print(f"\n📝 Researcher Agent: 第 {revision_count} 次修订...")
        print(f"   根据反馈: {state['review_feedback'][:60]}...")

        # 在实际应用中，这里会使用 LLM 根据反馈改进内容
        # 这里我们模拟改进
        current_draft = state["draft_content"]
        improvements = f"""

## 修订历史（第 {revision_count} 次）
根据审稿人反馈进行了以下改进：
- {state["review_feedback"]}
- 增强了理论论证的严谨性
- 补充了最新的研究进展
- 改进了语言表达的准确性
        """
        draft = current_draft + improvements
        message_content = f"已完成第 {revision_count} 次修订"

    researcher_message = AIMessage(content=message_content, name="researcher")

    return {"messages": [researcher_message], "draft_content": draft}


# ============================================================================
# 第三步: 实现 Reviewer Agent 节点
# ============================================================================
def reviewer_node(state: AcademicWritingState) -> dict:
    """
    Reviewer Agent: 审核论文并给出反馈

    评估维度:
    1. 结构完整性 (20%) - 是否包含必要章节
    2. 论证严谨性 (30%) - 逻辑是否清晰
    3. 语言表达 (20%) - 表达是否准确
    4. 创新性 (30%) - 是否有新见解

    返回:
    - 更新 quality_score (0-100)
    - 更新 review_feedback
    - 添加 AIMessage 到 messages
    """
    print("\n🔍 Reviewer Agent: 审核论文质量...")

    draft = state["draft_content"]
    del draft  # 仅用于调试，生产环境会使用
    revision_count = state["revision_count"]

    # 模拟质量评分（在实际应用中使用 LLM）
    # 初稿通常分数较低，修订后逐步提高
    if revision_count == 1:
        # 第一次审核（初稿）
        structure_score = 18  # 结构基本完整
        rigor_score = 20  # 论证需要加强
        language_score = 16  # 语言表达一般
        innovation_score = 18  # 创新性不足
        quality_score = structure_score + rigor_score + language_score + innovation_score
        # quality_score = 72

        feedback = """
审稿意见:
1. 结构完整性 (18/20): 章节齐全，但某些部分过于简略
2. 论证严谨性 (20/30): 需要补充更多理论推导和实验数据
3. 语言表达 (16/20): 部分表述不够准确，建议使用更专业的术语
4. 创新性 (18/30): 综述性内容较多，缺乏独特见解

具体建议:
- 在第 3 节增加量子算法的数学推导
- 补充后量子密码学的安全性证明
- 引用最新的研究成果（2024-2025）
- 增强结论部分的深度和前瞻性
        """

    elif revision_count == 2:
        # 第二次审核（首次修订后）
        structure_score = 20
        rigor_score = 26
        language_score = 18
        innovation_score = 24
        quality_score = structure_score + rigor_score + language_score + innovation_score
        # quality_score = 88

        feedback = """
审稿意见:
1. 结构完整性 (20/20): ✅ 结构完整
2. 论证严谨性 (26/30): 理论推导已补充，但实验验证不足
3. 语言表达 (18/20): 表述更加专业准确
4. 创新性 (24/30): 已有一定的独特见解

改进显著！质量达到发表标准。建议:
- 可选：补充实验结果或案例分析
        """

    else:
        # 后续审核或初稿质量异常高（不太可能）
        quality_score = 85
        feedback = "论文质量良好，建议提交最终审核"

    print(f"   质量评分: {quality_score}/100")

    # 评分说明
    if quality_score >= 85:
        assessment = "优秀，达到发表标准"
    elif quality_score >= 75:
        assessment = "良好，需要小幅改进"
    elif quality_score >= 60:
        assessment = "及格，需要显著改进"
    else:
        assessment = "不及格，需要大幅修订"

    print(f"   综合评价: {assessment}")

    reviewer_message = AIMessage(
        content=f"审核完成。评分: {quality_score}/100. {assessment}", name="reviewer"
    )

    return {
        "messages": [reviewer_message],
        "quality_score": quality_score,
        "review_feedback": feedback,
    }


# ============================================================================
# 第四步: 实现 Human Final Review 节点
# ============================================================================
def human_final_review_node(state: AcademicWritingState) -> dict:
    """
    Human Final Review: 最终人类审核节点

    这个节点作为中断点，实际审核在恢复执行时完成
    """
    print("\n👤 进入最终人类审核环节...")
    print("   （工作流将在此中断，等待人类决策）")

    system_message = SystemMessage(content="[系统] 等待人类最终审核...")

    return {"messages": [system_message]}


# ============================================================================
# 第五步: 实现路由逻辑
# ============================================================================
def should_continue_revision(state: AcademicWritingState) -> str:
    """
    判断是否需要继续修订

    逻辑:
    1. 如果 quality_score >= 80，进入最终人类审核
    2. 如果 revision_count >= 3，强制进入最终审核（防止无限循环）
    3. 否则，返回 researcher 继续修订

    返回:
    - "researcher": 继续修订
    - "human_final_review": 进入最终审核
    """
    quality_score = state["quality_score"]
    revision_count = state["revision_count"]

    if quality_score >= 80:
        print(f"\n✅ 质量达标（{quality_score}/100），进入最终人类审核")
        return "human_final_review"
    if revision_count >= 3:
        print(f"\n⚠️  已达最大修订次数（{revision_count}），强制进入最终审核")
        return "human_final_review"
    print(f"\n🔄 质量未达标（{quality_score}/100 < 80），继续修订")
    return "researcher"


def should_approve(state: AcademicWritingState) -> str:
    """
    判断是否最终批准

    逻辑:
    - 如果 approved == True，结束流程
    - 否则，返回 researcher 继续修订

    返回:
    - END: 结束
    - "researcher": 继续修订
    """
    if state["approved"]:
        print("\n🎉 论文已批准，工作流结束")
        return END
    print("\n🔄 人类要求继续修订")
    return "researcher"


# ============================================================================
# 第六步: 构建工作流图
# ============================================================================
def create_academic_writing_graph() -> StateGraph:
    """
    创建学术写作工作流图

    流程:
        START → researcher → reviewer → [判断质量]
                   ↑                         ↓
                   └────[需要修订]──────────┘
                                            ↓
                                  human_final_review (中断点)
                                            ↓
                                       [批准判断]
                                       ↓         ↓
                                  [修订]      [END]

    关键配置:
    - interrupt_before=["human_final_review"]
    - checkpointer=MemorySaver()

    返回:
        编译后的可执行图
    """
    # 1. 初始化状态图
    workflow = StateGraph(AcademicWritingState)

    # 2. 添加所有节点
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("human_final_review", human_final_review_node)

    # 3. 添加边
    workflow.add_edge(START, "researcher")  # 起点到 researcher
    workflow.add_edge("researcher", "reviewer")  # researcher 到 reviewer

    # 4. 添加条件边: reviewer 后判断是否需要修订
    workflow.add_conditional_edges(
        "reviewer",
        should_continue_revision,
        {
            "researcher": "researcher",  # 需要修订，回到 researcher
            "human_final_review": "human_final_review",  # 质量达标，进入人类审核
        },
    )

    # 5. 添加条件边: 人类审核后判断是否批准
    workflow.add_conditional_edges(
        "human_final_review",
        should_approve,
        {
            "researcher": "researcher",  # 人类要求修订，回到 researcher
            END: END,  # 批准，结束流程
        },
    )

    # 6. 编译图（关键配置）
    memory = MemorySaver()
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_final_review"],  # 在人类审核前中断
    )


# ============================================================================
# 主函数
# ============================================================================
def main() -> None:
    """主函数：测试学术写作工作流"""
    print("=" * 70)
    print("L21 练习题参考答案: 研究员 + 审稿人双 Agent 写作流")
    print("=" * 70)

    # 创建图
    graph = create_academic_writing_graph()

    # 准备初始状态
    initial_state: AcademicWritingState = {
        "messages": [HumanMessage(content="请写一篇关于《量子计算在密码学中的应用》的学术论文")],
        "topic": "量子计算在密码学中的应用",
        "draft_content": "",
        "review_feedback": "",
        "quality_score": 0,
        "revision_count": 0,
        "approved": False,
    }

    print("\n📥 论文主题:")
    print(f"  {initial_state['topic']}")

    # 配置
    config = {"configurable": {"thread_id": "academic_writing_001"}}

    # ========================================================================
    # 第一次执行：生成初稿 → 审核 → 修订 → 再审核 → 中断
    # ========================================================================
    print("\n" + "=" * 70)
    print("🚀 阶段 1: 自动迭代修订（直到质量达标或达到最大次数）")
    print("=" * 70)

    result = graph.invoke(initial_state, config)

    # ========================================================================
    # 中断后：展示内容并等待人类决策
    # ========================================================================
    print("\n" + "=" * 70)
    print("⏸️  工作流已中断，等待最终人类审核")
    print("=" * 70)

    print("\n📊 当前状态:")
    print(f"  质量评分: {result['quality_score']}/100")
    print(f"  修订次数: {result['revision_count']}")

    print("\n📄 论文内容预览（前 500 字符）:")
    print("-" * 70)
    print(result["draft_content"][:500])
    print("...")
    print("-" * 70)

    # ========================================================================
    # 模拟人类最终审核
    # ========================================================================
    print("\n" + "=" * 70)
    print("👤 模拟人类最终审核...")
    print("=" * 70)

    # 在实际应用中，这里会等待真实用户输入
    # human_decision = input("请输入决策（输入 'approve' 批准，或提供修改意见）: ")
    human_decision = "approve"  # 模拟批准

    print(f"人类决策: {human_decision}")

    # ========================================================================
    # 第二次执行：注入人类决策并继续
    # ========================================================================
    print("\n🔄 阶段 2: 根据人类决策继续执行...")
    print("-" * 70)

    # 更新状态：注入人类决策
    updated_state = {**result, "approved": human_decision.lower() in ["approve", "批准", "通过"]}

    # 如果人类提供了具体修改意见而非批准
    if not updated_state["approved"]:
        updated_state["review_feedback"] = human_decision

    # 恢复执行
    final_result = graph.invoke(updated_state, config)

    # ========================================================================
    # 输出最终结果
    # ========================================================================
    print("-" * 70)
    print("\n" + "=" * 70)
    print("✅ 工作流执行完成！")
    print("=" * 70)

    print("\n📊 最终统计:")
    print(f"  质量评分: {final_result['quality_score']}/100")
    print(f"  修订次数: {final_result['revision_count']}")
    print(f"  批准状态: {'✅ 已批准' if final_result['approved'] else '❌ 未批准'}")
    print(f"  总消息数: {len(final_result['messages'])}")

    print("\n📝 执行轨迹:")
    for i, msg in enumerate(final_result["messages"], 1):
        msg_type = msg.__class__.__name__  # noqa: F841
        agent = msg.name if hasattr(msg, "name") and msg.name else "System"
        content = msg.content[:60].replace("\n", " ")
        print(f"  {i}. [{agent:12}] {content}...")

    print("\n" + "=" * 70)
    print("🎓 实现要点总结:")
    print("  ✅ 清晰的状态定义（TypedDict + Annotated）")
    print("  ✅ Researcher 和 Reviewer 两个独立 Agent")
    print("  ✅ 基于质量分数的条件路由")
    print("  ✅ 迭代次数限制防止无限循环")
    print("  ✅ Human-in-the-Loop 最终审核")
    print("  ✅ 使用 MemorySaver 实现状态持久化")
    print("=" * 70)


if __name__ == "__main__":
    main()
