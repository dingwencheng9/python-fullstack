"""L12 示例2: send() 双向通信

本示例演示如何使用 send() 方法实现生成器的双向通信。
"""

from typing import Optional, Any
from dataclasses import dataclass


def echo_generator():
    """回显生成器 - 接收并打印发送的值"""
    while True:
        value = yield  # 接收 send() 发送的值
        print(f"[echo] Received: {value}")


def counter_generator():
    """计数器生成器 - 可以重置初始值"""
    count = 0
    while True:
        value = yield count  # 产出当前计数
        if value is not None:
            count = value  # 通过 send() 重置计数
        else:
            count += 1


def moving_average_generator():
    """移动平均生成器"""
    total = 0
    count = 0
    avg = None

    while True:
        value = yield avg  # 产出当前平均值
        total += value
        count += 1
        avg = total / count


def bank_account_generator():
    """银行账户协程"""
    balance = 0
    while True:
        operation = yield balance  # 产出当前余额
        if operation is None:
            pass
        elif operation["type"] == "deposit":
            balance += operation["amount"]
        elif operation["type"] == "withdraw":
            balance -= operation["amount"]


@dataclass
class StateMachine:
    """状态机生成器"""
    states: list[str]
    initial: str

    def __post_init__(self):
        self.current = self.initial
        self.index = self.states.index(self.initial)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        event = yield self.current
        self._transition(event)
        return self.current

    def _transition(self, event: str) -> None:
        """根据事件转换状态"""
        transitions = {
            "initial": {"start": "running"},
            "running": {"pause": "paused", "stop": "stopped"},
            "paused": {"resume": "running", "stop": "stopped"},
        }
        if event in transitions.get(self.current, {}):
            self.current = transitions[self.current][event]


def rate_limiter_generator():
    """速率限制器协程"""
    import time
    window_size = 1.0  # 1秒窗口
    max_requests = 5
    timestamps = []

    while True:
        event = yield len(timestamps) < max_requests  # 产出是否允许请求

        if event == "reset":
            timestamps = []
        else:
            now = time.time()
            timestamps = [t for t in timestamps if now - t < window_size]
            if len(timestamps) < max_requests:
                timestamps.append(now)
                yield True
            else:
                yield False


class PipelineStage:
    """管道处理阶段"""
    def __init__(self, processor):
        self.processor = processor
        self.input_buffer = []
        self.output_buffer = []

    def send(self, value):
        """发送值到阶段"""
        self.input_buffer.append(value)
        return self.processor(value)

    def receive(self):
        """从阶段接收值"""
        if self.output_buffer:
            return self.output_buffer.pop(0)
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("1. 基本 send() 示例")
    print("=" * 60)

    gen = echo_generator()
    next(gen)  # 启动生成器
    gen.send("Hello")
    gen.send("World")

    print("\n" + "=" * 60)
    print("2. 计数器示例")
    print("=" * 60)

    counter = counter_generator()
    print(f"初始: {next(counter)}")  # 0
    print(f"next(): {next(counter)}")  # 1
    print(f"next(): {next(counter)}")  # 2
    print(f"send(100): {counter.send(100)}")  # 重置为100
    print(f"next(): {next(counter)}")  # 101

    print("\n" + "=" * 60)
    print("3. 移动平均生成器")
    print("=" * 60)

    avg_gen = moving_average_generator()
    next(avg_gen)  # 启动

    print(f"send(10): {avg_gen.send(10)}")  # 10.0
    print(f"send(20): {avg_gen.send(20)}")  # 15.0
    print(f"send(30): {avg_gen.send(30)}")  # 20.0

    print("\n" + "=" * 60)
    print("4. 银行账户示例")
    print("=" * 60)

    account = bank_account_generator()
    balance = next(account)  # 启动
    print(f"初始余额: {balance}")

    balance = account.send({"type": "deposit", "amount": 1000})
    print(f"存款后余额: {balance}")

    balance = account.send({"type": "withdraw", "amount": 300})
    print(f"取款后余额: {balance}")

    print("\n" + "=" * 60)
    print("5. 状态机示例")
    print("=" * 60)

    sm = StateMachine(
        states=["initial", "running", "paused", "stopped"],
        initial="initial"
    )
    gen = iter(sm)

    print(f"初始状态: {next(gen)}")
    print(f"send('start'): {gen.send('start')}")
    print(f"send('pause'): {gen.send('pause')}")
    print(f"send('resume'): {gen.send('resume')}")
    print(f"send('stop'): {gen.send('stop')}")
