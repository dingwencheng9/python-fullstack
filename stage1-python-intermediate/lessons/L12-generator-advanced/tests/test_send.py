"""L12 生成器进阶 - send() 测试

使用根 conftest.py 提供的 solutions fixture，避免 sys.path 污染。
"""

import pytest


class TestBankAccount:
    """测试银行账户"""

    def test_initial_balance(self, solutions):
        """初始余额"""
        bank_account = getattr(solutions, "bank_account")
        acc = bank_account(1000)
        assert next(acc) == 1000.0

    def test_deposit(self, solutions):
        """存款"""
        bank_account = getattr(solutions, "bank_account")
        acc = bank_account(1000)
        next(acc)
        balance = acc.send({"type": "deposit", "amount": 500})
        assert balance == 1500.0

    def test_withdraw(self, solutions):
        """取款"""
        bank_account = getattr(solutions, "bank_account")
        acc = bank_account(1000)
        next(acc)
        balance = acc.send({"type": "withdraw", "amount": 300})
        assert balance == 700.0


class TestMovingAverage:
    """测试移动平均"""

    def test_average(self, solutions):
        """计算平均值"""
        moving_average = getattr(solutions, "moving_average")
        gen = moving_average()
        next(gen)
        assert gen.send(10) == 10.0
        assert gen.send(20) == 15.0
        assert gen.send(30) == 20.0


class TestCounter:
    """测试计数器"""

    def test_increment(self, solutions):
        """递增"""
        counter = getattr(solutions, "counter")
        cnt = counter()
        assert next(cnt) == 0
        assert next(cnt) == 1
        assert next(cnt) == 2

    def test_reset(self, solutions):
        """重置"""
        counter = getattr(solutions, "counter")
        cnt = counter()
        next(cnt)
        assert next(cnt) == 1
        assert cnt.send(100) == 100
        assert next(cnt) == 101


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
