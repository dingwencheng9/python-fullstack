"""
练习题 1: 构建基础 StateGraph

请根据以下要求构建一个 LangGraph 应用：

1. 定义一个 CounterState，包含:
   - count: int (计数器)
   - history: list[str] (操作历史)

2. 实现以下节点:
   - increment: 将 count 加 1，并记录历史
   - decrement: 将 count 减 1，并记录历史
   - multiply: 将 count 乘以 2，并记录历史

3. 使用条件边实现以下流程:
   - 从 START 进入 increment
   - increment 后根据 count 的值决定下一步:
     - count < 5: 返回 multiply
     - count >= 5: 结束

4. 初始状态: count=0, history=[]
   预期执行流程: increment -> multiply -> increment -> multiply -> ... (直到 count >= 5)
"""

from typing import TypedDict, Literal


class CounterState(TypedDict):
    """计数器状态"""

    count: int
    history: list[str]


def increment(state: CounterState) -> CounterState:
    """增加计数器"""
    # TODO: 实现此函数
    pass


def decrement(state: CounterState) -> CounterState:
    """减少计数器"""
    # TODO: 实现此函数
    pass


def multiply(state: CounterState) -> CounterState:
    """乘以 2"""
    # TODO: 实现此函数
    pass


def should_multiply_or_end(state: CounterState) -> Literal["multiply", "__end__"]:
    """决定下一步: count < 5 时继续，否则结束"""
    # TODO: 实现此函数
    pass


def main() -> None:
    """主函数"""
    # TODO: 构建图
    pass

    # TODO: 编译并执行

    # 预期结果:
    # count 应该 >= 5
    # history 应该记录了每次操作
    pass


if __name__ == "__main__":
    main()
