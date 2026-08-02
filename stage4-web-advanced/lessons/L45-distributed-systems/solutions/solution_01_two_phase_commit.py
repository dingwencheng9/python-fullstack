"""
L47: 分布式系统实战 - 参考解答 1: 两阶段提交 (2PC)

实现两阶段提交协议。
"""

import asyncio
from dataclasses import dataclass, field
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
    participants_votes: dict[str, Vote] = field(default_factory=dict)
    decided: bool = False


class Coordinator:
    """
    两阶段提交协调者
    """

    def __init__(self):
        self.transactions: dict[str, Transaction] = {}
        self._lock = asyncio.Lock()
        self._participant_responses: dict[str, asyncio.Queue] = {}

    async def begin_transaction(self, tx_id: str, participants: list[str]) -> Transaction:
        """开始新事务"""
        async with self._lock:
            tx = Transaction(tx_id=tx_id)
            self.transactions[tx_id] = tx

            # 为每个参与者创建响应队列
            for pid in participants:
                self._participant_responses[f"{tx_id}:{pid}"] = asyncio.Queue()

            print(f"✅ 协调者: 事务 {tx_id} 创建，参与者: {participants}")
            return tx

    async def vote_request(self, tx_id: str) -> bool:
        """发送投票请求"""
        if tx_id not in self.transactions:
            raise ValueError(f"事务 {tx_id} 不存在")

        tx = self.transactions[tx_id]
        tx.phase = Phase.VOTE_REQUEST

        # 向所有参与者发送投票请求
        votes = []
        for pid in self._participant_responses:
            if pid.startswith(f"{tx_id}:"):
                participant_id = pid.split(":")[1]

                # 模拟发送投票请求
                print(f"📨 协调者 -> {participant_id}: 投票请求")

                # 等待参与者响应
                try:
                    response_queue = self._participant_responses[pid]
                    vote = await asyncio.wait_for(response_queue.get(), timeout=5.0)
                    votes.append(vote)
                    tx.participants_votes[participant_id] = vote
                except asyncio.TimeoutError:
                    print(f"❌ 协调者: {participant_id} 投票超时")
                    votes.append(Vote.NO)

        # 判断结果
        all_yes = all(v == Vote.YES for v in votes)
        tx.decided = True

        if all_yes:
            print("✅ 协调者: 所有参与者投票 YES")
        else:
            print("❌ 协调者: 存在 NO 投票，需要回滚")

        return all_yes

    async def vote_commit(self, tx_id: str) -> None:
        """发送提交决定"""
        tx = self.transactions[tx_id]
        tx.phase = Phase.VOTE_COMMIT

        for pid in self._participant_responses:
            if pid.startswith(f"{tx_id}:"):
                participant_id = pid.split(":")[1]
                print(f"📨 协调者 -> {participant_id}: COMMIT")

    async def vote_abort(self, tx_id: str) -> None:
        """发送回滚决定"""
        for pid in self._participant_responses:
            if pid.startswith(f"{tx_id}:"):
                participant_id = pid.split(":")[1]
                print(f"📨 协调者 -> {participant_id}: ABORT")

    def receive_vote(self, tx_id: str, participant_id: str, vote: Vote) -> None:
        """接收投票"""
        queue = self._participant_responses.get(f"{tx_id}:{participant_id}")
        if queue:
            queue.put_nowait(vote)


class Participant:
    """
    两阶段提交参与者
    """

    def __init__(self, participant_id: str, can_commit: bool = True):
        self.participant_id = participant_id
        self._can_commit = can_commit
        self._pending_tx: str | None = None

    async def receive_vote_request(self, tx_id: str) -> Vote:
        """接收投票请求"""
        self._pending_tx = tx_id
        print(f"📨 {self.participant_id}: 收到投票请求")

        # 本地决策（这里简化模拟）
        if self._can_commit:
            vote = Vote.YES
        else:
            vote = Vote.NO

        print(f"📤 {self.participant_id}: 投票 {vote.value}")
        return vote

    async def do_commit(self, tx_id: str) -> None:
        """执行提交"""
        print(f"✅ {self.participant_id}: 提交事务 {tx_id}")
        self._pending_tx = None

    async def do_abort(self, tx_id: str) -> None:
        """执行回滚"""
        print(f"❌ {self.participant_id}: 回滚事务 {tx_id}")
        self._pending_tx = None


async def test_two_phase_commit():
    """测试两阶段提交"""
    coordinator = Coordinator()
    participants = [Participant(f"participant-{i}") for i in range(3)]
    participant_ids = [p.participant_id for p in participants]

    # 1. 开始事务
    tx = await coordinator.begin_transaction("tx-001", participant_ids)
    print(f"事务创建: {tx.tx_id}")

    # 2. 模拟参与者投票
    async def participant_voting(p: Participant):
        vote = await p.receive_vote_request(tx.tx_id)
        coordinator.receive_vote(tx.tx_id, p.participant_id, vote)

    # 并发执行参与者投票
    await asyncio.gather(*[participant_voting(p) for p in participants])

    # 3. 协调者收集投票
    success = await coordinator.vote_request("tx-001")

    # 4. 协调者发送最终决定
    if success:
        await coordinator.vote_commit("tx-001")
        for p in participants:
            await p.do_commit(tx.tx_id)
        print("\n✅ 事务提交成功")
    else:
        await coordinator.vote_abort("tx-001")
        for p in participants:
            await p.do_abort(tx.tx_id)
        print("\n❌ 事务回滚")


if __name__ == "__main__":
    asyncio.run(test_two_phase_commit())
