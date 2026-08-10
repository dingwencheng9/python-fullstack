"""L45 分布式系统实战 - 测试"""

from __future__ import annotations

import asyncio
import pytest


def test_transaction_creation():
    """测试事务创建"""
    from solutions.solution_01_two_phase_commit import Transaction, Phase

    tx = Transaction(tx_id="tx-001")

    assert tx.tx_id == "tx-001"
    assert tx.phase == Phase.IDLE
    assert len(tx.participants_votes) == 0


def test_vote_enum():
    """测试投票枚举"""
    from solutions.solution_01_two_phase_commit import Vote

    assert Vote.YES.value == "yes"
    assert Vote.NO.value == "no"


def test_phase_enum():
    """测试阶段枚举"""
    from solutions.solution_01_two_phase_commit import Phase

    assert Phase.IDLE.value == "idle"
    assert Phase.VOTE_REQUEST.value == "vote_request"
    assert Phase.VOTE_COMMIT.value == "vote_commit"


# ============================================================================
# 补充测试: 2PC 核心业务逻辑
# ============================================================================


@pytest.mark.asyncio
async def test_coordinator_creates_transaction():
    """测试协调者创建事务"""
    from solutions.solution_01_two_phase_commit import Coordinator

    coordinator = Coordinator()
    tx = await coordinator.begin_transaction("tx-002", ["p1", "p2"])

    assert tx.tx_id == "tx-002"
    assert tx.phase.value == "idle"
    assert len(tx.participants_votes) == 0
    assert "tx-002:p1" in coordinator._participant_responses
    assert "tx-002:p2" in coordinator._participant_responses


@pytest.mark.asyncio
async def test_all_votes_yes_commits():
    """测试全部投票 YES 时提交"""
    from solutions.solution_01_two_phase_commit import Coordinator, Participant

    coordinator = Coordinator()
    participants = [
        Participant("p1", can_commit=True),
        Participant("p2", can_commit=True),
    ]

    tx = await coordinator.begin_transaction(
        "tx-003", [p.participant_id for p in participants]
    )

    # 模拟参与者投票 YES
    for p in participants:
        vote = await p.receive_vote_request(tx.tx_id)
        coordinator.receive_vote(tx.tx_id, p.participant_id, vote)

    # 协调者收集投票
    success = await coordinator.vote_request("tx-003")

    assert success is True
    assert tx.decided is True


@pytest.mark.asyncio
async def test_any_vote_no_aborts():
    """测试任意 NO 投票时回滚"""
    from solutions.solution_01_two_phase_commit import Coordinator, Participant

    coordinator = Coordinator()
    participants = [
        Participant("p1", can_commit=True),  # YES
        Participant("p2", can_commit=False),  # NO
    ]

    tx = await coordinator.begin_transaction(
        "tx-004", [p.participant_id for p in participants]
    )

    # 模拟参与者投票
    for p in participants:
        vote = await p.receive_vote_request(tx.tx_id)
        coordinator.receive_vote(tx.tx_id, p.participant_id, vote)

    # 协调者收集投票
    success = await coordinator.vote_request("tx-004")

    assert success is False
    assert tx.decided is True


@pytest.mark.asyncio
async def test_vote_request_changes_phase():
    """测试投票请求改变事务阶段"""
    from solutions.solution_01_two_phase_commit import Coordinator, Participant, Phase

    coordinator = Coordinator()
    p = Participant("p1", can_commit=True)

    tx = await coordinator.begin_transaction("tx-005", ["p1"])

    assert tx.phase == Phase.IDLE

    vote = await p.receive_vote_request(tx.tx_id)
    coordinator.receive_vote(tx.tx_id, p.participant_id, vote)
    await coordinator.vote_request("tx-005")

    assert tx.phase == Phase.VOTE_REQUEST


@pytest.mark.asyncio
async def test_vote_commit_changes_phase():
    """测试提交决定改变事务阶段"""
    from solutions.solution_01_two_phase_commit import Coordinator, Participant, Phase

    coordinator = Coordinator()
    p = Participant("p1", can_commit=True)

    tx = await coordinator.begin_transaction("tx-006", ["p1"])

    vote = await p.receive_vote_request(tx.tx_id)
    coordinator.receive_vote(tx.tx_id, p.participant_id, vote)
    await coordinator.vote_request("tx-006")
    await coordinator.vote_commit("tx-006")

    assert tx.phase == Phase.VOTE_COMMIT


@pytest.mark.asyncio
async def test_participant_timeout_handling():
    """测试参与者超时处理"""
    from solutions.solution_01_two_phase_commit import Coordinator

    coordinator = Coordinator()
    tx = await coordinator.begin_transaction("tx-timeout", ["slow-p1"])

    # 不发送投票，模拟超时
    # 5秒后协调者应该超时并返回 False
    success = await coordinator.vote_request("tx-timeout")

    assert success is False


@pytest.mark.asyncio
async def test_concurrent_transactions():
    """测试并发事务处理"""
    from solutions.solution_01_two_phase_commit import Coordinator, Participant

    coordinator = Coordinator()

    # 创建两个并发事务
    tx1 = await coordinator.begin_transaction("tx-concurrent-1", ["p1"])
    tx2 = await coordinator.begin_transaction("tx-concurrent-2", ["p2"])

    assert tx1.tx_id != tx2.tx_id
    assert "tx-concurrent-1:p1" in coordinator._participant_responses
    assert "tx-concurrent-2:p2" in coordinator._participant_responses
    assert len(coordinator.transactions) == 2


@pytest.mark.asyncio
async def test_participant_commit():
    """测试参与者执行提交"""
    from solutions.solution_01_two_phase_commit import Participant

    p = Participant("p1", can_commit=True)
    tx_id = "tx-commit-test"

    vote = await p.receive_vote_request(tx_id)
    assert vote.value == "yes"

    # 执行提交
    await p.do_commit(tx_id)
    assert p._pending_tx is None


@pytest.mark.asyncio
async def test_participant_abort():
    """测试参与者执行回滚"""
    from solutions.solution_01_two_phase_commit import Participant

    p = Participant("p2", can_commit=False)
    tx_id = "tx-abort-test"

    vote = await p.receive_vote_request(tx_id)
    assert vote.value == "no"

    # 执行回滚
    await p.do_abort(tx_id)
    assert p._pending_tx is None
