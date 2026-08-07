"""L12 练习2: send() 实现协程"""

def bank_account(initial_balance=0.0):
    """银行账户协程"""
    balance = initial_balance
    while True:
        operation = yield balance
        if operation and operation.get('type') == 'deposit':
            balance += operation.get('amount', 0)
        elif operation and operation.get('type') == 'withdraw':
            amount = operation.get('amount', 0)
            if amount <= balance:
                balance -= amount
            else:
                raise ValueError("余额不足")


def moving_average():
    """移动平均生成器"""
    total = 0
    count = 0
    avg = None
    while True:
        value = yield avg
        total += value
        count += 1
        avg = total / count


def counter():
    """计数器，可重置"""
    count = 0
    while True:
        value = yield count
        if value is not None:
            count = value
        else:
            count += 1


if __name__ == "__main__":
    # 测试银行账户
    acc = bank_account(1000)
    print(f"初始余额: {next(acc)}")
    print(f"存款后: {acc.send({'type': 'deposit', 'amount': 500})}")
    print(f"取款后: {acc.send({'type': 'withdraw', 'amount': 200})}")

    # 测试移动平均
    avg_gen = moving_average()
    next(avg_gen)
    print(f"\n发送10: {avg_gen.send(10)}")
    print(f"发送20: {avg_gen.send(20)}")
    print(f"发送30: {avg_gen.send(30)}")

    # 测试计数器
    cnt = counter()
    print(f"\n初始: {next(cnt)}")
    print(f"next: {next(cnt)}")
    print(f"send(100): {cnt.send(100)}")
    print(f"next: {next(cnt)}")
