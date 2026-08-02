"""
L47: 分布式系统实战 - 练习 1: 两阶段提交 (2PC)

任务：
1. 实现协调者（Coordinator）
2. 实现参与者（Participant）
3. 实现两阶段提交协议
4. 处理超时和故障恢复
"""

import asyncio
from dataclasses import dataclass
from enum import Enum

class Phase(Enum):
    """2PC 阶段"""

    IDLE = "idle"
    VOTE_REQUEST = "vote_request"  # 投票请求阶段
    VOTE_COMMIT = "vote_commit"  # 提交阶段


class Vote(Enum):
    """投票结果"""

    YES = "yes"
    NO = "no"


@dataclass
class Transaction:
    """分布式事务"""

    tx_id: str
    phase: Phase = Phase.IDLE
    participants_votes: dict[str, Vote] = None

    def __post_init__(self):
        if self.participants_votes is None:
            self.participants_votes = {}


class Coordinator:
    """
    两阶段提交协调者

    职责：
    1. 向所有参与者发送投票请求
    2. 收集投票结果
    3. 根据投票结果决定提交或回滚
    4. 向所有参与者发送最终决定
    """

    def __init__(self):
        self.transactions: dict[str, Transaction] = {}
        self._lock = asyncio.Lock()

    async def begin_transaction(self, tx_id: str, participants: list[str]) -> Transaction:
        """开始新事务"""
        # TODO: 实现

    async def vote_request(self, tx_id: str) -> bool:
        """发送投票请求"""
        # TODO: 实现

    async def vote_commit(self, tx_id: str) -> None:
        """发送提交决定"""
        # TODO: 实现

    async def vote_abort(self, tx_id: str) -> None:
        """发送回滚决定"""
        # TODO: 实现


class Participant:
    """
    两阶段提交参与者

    职责：
    1. 响应投票请求
    2. 根据本地状态投票
    3. 执行或回滚事务
    """

    def __init__(self, participant_id: str):
        self.participant_id = participant_id
        self._can_commit = True  # 本地是否可以提交

    async def receive_vote_request(self, tx_id: str) -> Vote:
        """接收投票请求"""
        # TODO: 实现

    async def do_commit(self, tx_id: str) -> None:
        """执行提交"""
        # TODO: 实现

    async def do_abort(self, tx_id: str) -> None:
        """执行回滚"""
        # TODO: 实现


# ============ 测试代码 ============


async def test_two_phase_commit():
    """测试两阶段提交"""
    coordinator = Coordinator()
    participants = [Participant(f"participant-{i}") for i in range(3)]
    participant_ids = [p.participant_id for p in participants]

    # 1. 开始事务
    tx = await coordinator.begin_transaction("tx-001", participant_ids)
    print(f"事务创建: {tx.tx_id}")

    # 2. 执行两阶段提交
    success = await coordinator.vote_request("tx-001")
    print(f"投票请求结果: {success}")

    if success:
        await coordinator.vote_commit("tx-001")
        print("事务提交成功")
    else:
        await coordinator.vote_abort("tx-001")
        print("事务回滚")


if __name__ == "__main__":
    asyncio.run(test_two_phase_commit())
