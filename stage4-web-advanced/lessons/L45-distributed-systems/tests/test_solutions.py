"""L47 分布式系统实战 - 测试"""

from __future__ import annotations


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
