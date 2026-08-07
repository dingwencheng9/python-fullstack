"""L12 生成器进阶 - send() 测试"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "solutions"))

from solution_02_send import bank_account, moving_average, counter


class TestBankAccount:
    """测试银行账户"""

    def test_initial_balance(self):
        """初始余额"""
        acc = bank_account(1000)
        assert next(acc) == 1000.0

    def test_deposit(self):
        """存款"""
        acc = bank_account(1000)
        next(acc)
        balance = acc.send({'type': 'deposit', 'amount': 500})
        assert balance == 1500.0

    def test_withdraw(self):
        """取款"""
        acc = bank_account(1000)
        next(acc)
        balance = acc.send({'type': 'withdraw', 'amount': 300})
        assert balance == 700.0


class TestMovingAverage:
    """测试移动平均"""

    def test_average(self):
        """计算平均值"""
        gen = moving_average()
        next(gen)
        assert gen.send(10) == 10.0
        assert gen.send(20) == 15.0
        assert gen.send(30) == 20.0


class TestCounter:
    """测试计数器"""

    def test_increment(self):
        """递增"""
        cnt = counter()
        assert next(cnt) == 0
        assert next(cnt) == 1
        assert next(cnt) == 2

    def test_reset(self):
        """重置"""
        cnt = counter()
        next(cnt)
        assert next(cnt) == 1
        assert cnt.send(100) == 100
        assert next(cnt) == 101


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
