"""
示例 5: 人机协同与中断

展示如何使用 interrupt 实现需要人工确认的敏感操作。
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langgraph.types import interrupt


class ApprovalState(TypedDict):
    """需要审批的操作状态"""

    action_type: str
    action_details: dict
    approved: bool | None
    result: str | None


def assess_action(state: ApprovalState) -> ApprovalState:
    """
    评估操作是否需要审批

    Args:
        state: 当前状态

    Returns:
        更新后的状态
    """
    action_type = state.get("action_type", "")
    amount = state.get("action_details", {}).get("amount", 0)

    # 敏感操作需要审批
    if action_type in ["transfer", "delete", "send_email"]:
        if amount > 1000:
            # 中断执行，等待人工审批
            confirmation = interrupt(
                {
                    "message": f"需要审批: {action_type}, 金额: {amount}",
                    "action": state["action_details"],
                }
            )
            return {"approved": confirmation.get("approved", False)}

    # 普通操作直接通过
    return {"approved": True}


def execute_action(state: ApprovalState) -> ApprovalState:
    """
    执行已审批的操作

    Args:
        state: 当前状态

    Returns:
        执行结果
    """
    if not state.get("approved"):
        return {"result": "操作已取消"}

    action_type = state.get("action_type", "")
    details = state.get("action_details", {})

    if action_type == "transfer":
        return {"result": f"转账成功: {details.get('amount')} 元"}
    elif action_type == "delete":
        return {"result": f"删除成功: {details.get('target')}"}
    elif action_type == "send_email":
        return {"result": f"邮件已发送: {details.get('to')}"}

    return {"result": "操作完成"}


def main() -> None:
    """主函数"""
    builder = StateGraph(ApprovalState)

    builder.add_node("assess", assess_action)
    builder.add_node("execute", execute_action)

    builder.add_edge(START, "assess")
    builder.add_edge("assess", "execute")
    builder.add_edge("execute", END)

    graph = builder.compile()

    print("=" * 60)
    print("人机协同测试")
    print("=" * 60)

    # 测试 1: 普通操作（不需要审批）
    print("\n--- 测试 1: 普通操作 ---")
    result1 = graph.invoke(
        {
            "action_type": "read",
            "action_details": {"target": "report.pdf"},
            "approved": None,
            "result": None,
        }
    )
    print("操作: read")
    print(f"结果: {result1['result']}")
    print(f"已审批: {result1['approved']}")

    # 测试 2: 小额转账（不需要审批）
    print("\n--- 测试 2: 小额转账 ---")
    result2 = graph.invoke(
        {
            "action_type": "transfer",
            "action_details": {"amount": 500, "to": "account_123"},
            "approved": None,
            "result": None,
        }
    )
    print("操作: transfer, 金额: 500")
    print(f"结果: {result2['result']}")
    print(f"已审批: {result2['approved']}")

    # 测试 3: 大额转账（需要审批）
    print("\n--- 测试 3: 大额转账（需要审批）---")
    print("注意: 在实际运行中，这里会触发 interrupt")
    print("需要通过 graph.invoke(None, config=...) 传入审批结果")

    # 模拟中断状态
    print("\n模拟中断后的审批流程:")
    print("1. graph.invoke(...) 返回中断状态")
    print("2. 用户确认或拒绝")
    print("3. 再次调用 graph.invoke(None, config=...) 继续执行")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert result1["approved"] is True, "普通操作应该自动审批"
    assert result2["approved"] is True, "小额转账应该自动审批"
    assert result1["result"] == "操作完成", "普通操作应该完成"
    assert "转账成功" in result2["result"], "小额转账应该成功"
    print("✅ 人机协同逻辑验证通过!")


if __name__ == "__main__":
    main()
