"""
L45: 分布式系统实战 - 示例 2: Saga 模式

Saga 模式：将长事务拆分为多个本地事务，每个事务都有对应的补偿操作。
"""

from dataclasses import dataclass
from enum import Enum

class SagaStepStatus(Enum):
    """Saga 步骤状态"""

    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATED = "compensated"
    FAILED = "failed"


@dataclass
class SagaStep:
    """Saga 步骤"""

    name: str
    forward: Callable  # 正向操作
    backward: Callable  # 补偿操作
    status: SagaStepStatus = SagaStepStatus.PENDING


class Saga:
    """
    Saga 编排器

    使用方式：
    1. 添加步骤（正向操作 + 补偿操作）
    2. 执行 saga
    3. 失败时自动回滚
    """

    def __init__(self, name: str):
        self.name = name
        self.steps: list[SagaStep] = []
        self.completed_steps: list[SagaStep] = []

    def add_step(self, name: str, forward: Callable, backward: Callable) -> "Saga":
        """添加步骤"""
        self.steps.append(SagaStep(name, forward, backward))
        return self

    async def execute(self) -> bool:
        """执行 Saga"""
        print(f"\n{'=' * 60}")
        print(f"Saga 执行: {self.name}")
        print("=" * 60)

        for step in self.steps:
            print(f"\n📦 执行步骤: {step.name}")

            try:
                await step.forward()
                step.status = SagaStepStatus.COMPLETED
                self.completed_steps.append(step)
                print(f"   ✅ 步骤完成: {step.name}")
            except Exception as e:
                print(f"   ❌ 步骤失败: {step.name} - {e}")
                step.status = SagaStepStatus.FAILED

                # 触发回滚
                print("\n🔄 开始回滚...")
                await self._compensate()
                return False

        print(f"\n✅ Saga 执行成功: {self.name}")
        return True

    async def _compensate(self) -> None:
        """补偿已完成的步骤（倒序）"""
        for step in reversed(self.completed_steps):
            print(f"🔙 补偿步骤: {step.name}")
            try:
                await step.backward()
                step.status = SagaStepStatus.COMPENSATED
                print(f"   ✅ 补偿完成: {step.name}")
            except Exception as e:
                print(f"   ❌ 补偿失败: {step.name} - {e}")


# ============ 订单创建 Saga 示例 ============


async def create_order(order_id: int, user_id: int) -> None:
    """创建订单"""
    print(f"   创建订单: order_id={order_id}, user_id={user_id}")
    # 模拟业务逻辑
    # 实际会调用订单服务


async def cancel_order(order_id: int) -> None:
    """取消订单（补偿操作）"""
    print(f"   取消订单: order_id={order_id}")


async def reserve_inventory(product_id: int, quantity: int) -> None:
    """预留库存"""
    print(f"   预留库存: product_id={product_id}, qty={quantity}")
    # 模拟可能失败


async def release_inventory(product_id: int, quantity: int) -> None:
    """释放库存（补偿操作）"""
    print(f"   释放库存: product_id={product_id}, qty={quantity}")


async def process_payment(order_id: int, amount: float) -> None:
    """处理支付"""
    print(f"   处理支付: order_id={order_id}, amount={amount}")
    # 模拟可能失败
    raise Exception("支付网关不可用")


async def refund_payment(order_id: int, amount: float) -> None:
    """退款（补偿操作）"""
    print(f"   退款: order_id={order_id}, amount={amount}")


async def send_notification(order_id: int) -> None:
    """发送通知"""
    print(f"   发送通知: order_id={order_id}")


async def cancel_notification(order_id: int) -> None:
    """取消通知（补偿操作）"""
    print(f"   取消通知: order_id={order_id}")


async def demo_order_creation_saga():
    """演示订单创建 Saga"""
    saga = Saga("创建订单")

    saga.add_step("创建订单", lambda: create_order(1001, 1), lambda: cancel_order(1001))
    saga.add_step("预留库存", lambda: reserve_inventory(101, 2), lambda: release_inventory(101, 2))
    saga.add_step("处理支付", lambda: process_payment(1001, 199.99), lambda: refund_payment(1001, 199.99))
    saga.add_step("发送通知", lambda: send_notification(1001), lambda: cancel_notification(1001))

    success = await saga.execute()
    print(f"\n最终结果: {'成功' if success else '失败'}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(demo_order_creation_saga())
