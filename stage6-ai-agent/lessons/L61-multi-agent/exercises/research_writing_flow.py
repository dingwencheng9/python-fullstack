"""

from __future__ import annotations

L21 练习题: 研究员 + 审稿人双 Agent 写作流

任务描述:
    实现一个学术写作助手，包含两个协同工作的 Agent：
    1. Researcher Agent: 根据主题生成学术论文初稿
    2. Reviewer Agent: 审核初稿，提出修改建议

工作流要求:
    START → researcher → reviewer → [判断质量]
               ↑                        ↓
               └───[需要修改]───────────┘
                                       ↓
                             [Human 最终审核] → END

技术要求:
    1. 使用 Supervisor 模式协调两个 Agent
    2. 实现迭代修改机制（最多 3 轮）
    3. 在最终提交前引入 Human-in-the-Loop
    4. 使用 TypedDict 定义清晰的状态结构
    5. 添加完整的类型提示

评分标准:
    - 状态定义清晰 (20%)
    - 路由逻辑正确 (30%)
    - 迭代机制有效 (20%)
    - HITL 实现正确 (20%)
    - 代码质量 (10%)

提示:
    - 参考 examples/02_supervisor_router.py 的路由模式
    - 参考 examples/03_human_in_the_loop.py 的中断机制
    - 定义 quality_score 字段判断是否需要修改
    - 使用 interrupt_before 在最终提交前中断
"""

from __future__ import annotations

from typing import TypedDict


# ============================================================================
# 任务 1: 定义状态结构
# ============================================================================
class AcademicWritingState(TypedDict):
    """
    学术写作工作流状态

    👉 TODO: 定义以下状态字段

    必需字段:
    1. messages: 消息历史
       - 类型: Annotated[list[BaseMessage], operator.add]
       - 用途: 存储所有 Agent 的对话历史

    2. topic: 论文主题
       - 类型: str
       - 用途: 写作主题

    3. draft_content: 当前草稿内容
       - 类型: str
       - 用途: 存储论文当前版本

    4. review_feedback: 审稿人反馈
       - 类型: str
       - 用途: 存储审稿意见

    5. quality_score: 质量评分
       - 类型: int
       - 范围: 0-100
       - 用途: 判断是否需要修订

    6. revision_count: 修订次数
       - 类型: int
       - 用途: 防止无限循环

    7. approved: 是否最终批准
       - 类型: bool
       - 用途: 人类审核结果

    💡 提示:
    - 需要 from operator import add
    - 需要 from typing import Annotated
    - messages 字段需要使用 Annotated 来支持追加操作

    示例代码:
    ```python
    messages: Annotated[list[BaseMessage], add]
    topic: str
    draft_content: str
    ```
    """

    pass  # TODO: 在此定义状态字段
