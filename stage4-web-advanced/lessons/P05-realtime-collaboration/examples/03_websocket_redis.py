"""P05 示例 3: WebSocket 与 Redis PubSub"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Set
import time

# ============ WebSocket 消息类型 ============

class MessageType(str, Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    TASK_UPDATE = "task_update"
    TASK_CREATE = "task_create"
    TASK_DELETE = "task_delete"
    PING = "ping"
    PONG = "pong"
    NOTIFICATION = "notification"


@dataclass
class WebSocketMessage:
    type: MessageType
    data: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


# ============ WebSocket 连接管理 ============

class ConnectionManager:
    """WebSocket 连接管理器 - 参考 L46"""

    def __init__(self):
        # user_id -> set of queues
        self.user_connections: Dict[int, Set[asyncio.Queue]] = {}
        # task_id -> set of user_ids
        self.task_subscriptions: Dict[int, Set[int]] = {}

    def subscribe_user(self, user_id: int, queue: asyncio.Queue):
        """用户订阅"""
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(queue)
        print(f"  → 用户 {user_id} 已连接 (当前 {len(self.user_connections[user_id])} 个连接)")

    def unsubscribe_user(self, user_id: int, queue: asyncio.Queue):
        """用户取消订阅"""
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(queue)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
            print(f"  → 用户 {user_id} 已断开")

    def subscribe_task(self, user_id: int, task_id: int):
        """用户订阅任务更新"""
        if task_id not in self.task_subscriptions:
            self.task_subscriptions[task_id] = set()
        self.task_subscriptions[task_id].add(user_id)
        print(f"  → 用户 {user_id} 订阅了任务 {task_id}")

    def unsubscribe_task(self, user_id: int, task_id: int):
        """用户取消订阅任务"""
        if task_id in self.task_subscriptions:
            self.task_subscriptions[task_id].discard(user_id)
            if not self.task_subscriptions[task_id]:
                del self.task_subscriptions[task_id]
            print(f"  → 用户 {user_id} 取消订阅任务 {task_id}")

    async def send_to_user(self, user_id: int, message: WebSocketMessage):
        """向用户发送消息"""
        if user_id in self.user_connections:
            msg_dict = {
                "type": message.type.value,
                "data": message.data,
                "timestamp": message.timestamp
            }
            disconnected = []
            for queue in self.user_connections[user_id]:
                try:
                    await asyncio.wait_for(queue.put(msg_dict), timeout=1)
                except asyncio.TimeoutError:
                    disconnected.append(queue)
            for q in disconnected:
                self.user_connections[user_id].discard(q)

    async def broadcast_to_task(self, task_id: int, message: WebSocketMessage):
        """向任务订阅者广播消息"""
        if task_id in self.task_subscriptions:
            msg_dict = {
                "type": message.type.value,
                "data": message.data,
                "timestamp": message.timestamp
            }
            print(f"  📢 广播到任务 {task_id} ({len(self.task_subscriptions[task_id])} 个订阅者)")
            for user_id in self.task_subscriptions[task_id]:
                await self.send_to_user(user_id, message)


# ============ Redis PubSub 模拟 ============

class RedisPubSub:
    """Redis PubSub 模拟 - 参考 L40"""

    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self.subscriptions: Dict[str, asyncio.Queue] = {}

    async def publish(self, channel: str, message: dict):
        """发布消息"""
        print(f"  📤 Redis 发布到 {channel}: {message.get('type', 'unknown')}")

        # 模拟 Redis 消息传播
        # 实际使用: await redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str, handler):
        """订阅频道"""
        # 实际使用: pubsub = redis.pubsub(); await pubsub.subscribe(channel)
        print(f"  📥 订阅频道: {channel}")

    async def broadcast_task_update(self, task_id: int, event_type: str, data: dict):
        """广播任务更新"""
        channel = f"task:{task_id}"
        message = {
            "type": event_type,
            "task_id": task_id,
            "data": data,
            "timestamp": time.time()
        }
        await self.publish(channel, message)


# ============ 心跳检测 ============

class HeartbeatManager:
    """心跳管理器 - 参考 L46"""

    def __init__(self, manager: ConnectionManager, interval: int = 30):
        self.manager = manager
        self.interval = interval
        self.last_pong: Dict[int, float] = {}

    async def start_heartbeat(self, user_id: int, queue: asyncio.Queue):
        """为用户启动心跳"""
        print(f"  ❤️ 心跳检测启动 (每 {self.interval}s)")

        while True:
            try:
                # 发送 ping
                await asyncio.wait_for(
                    queue.put({"type": MessageType.PING.value, "timestamp": time.time()}),
                    timeout=1
                )

                # 等待 pong
                # 实际应用中会等待接收响应

                await asyncio.sleep(self.interval)

            except asyncio.TimeoutError:
                print(f"  ⚠️ 心跳超时，用户 {user_id} 可能已断开")
                break


# ============ 演示 ============

async def demonstrate_websocket():
    """演示 WebSocket 与 Redis PubSub"""
    print("=" * 60)
    print("WebSocket 实时通信与 Redis PubSub")
    print("=" * 60)

    manager = ConnectionManager()
    redis_pubsub = RedisPubSub(manager)

    # 1. 用户连接
    print("\n1️⃣ 用户连接 WebSocket")
    user_queues = {}
    for user_id in [1, 2, 3]:
        queue = asyncio.Queue()
        user_queues[user_id] = queue
        manager.subscribe_user(user_id, queue)
        print(f"  ✓ 用户 {user_id} 连接成功")

    # 2. 用户订阅任务
    print("\n2️⃣ 订阅任务更新")
    manager.subscribe_task(1, 100)  # Alice 订阅任务 100
    manager.subscribe_task(2, 100)  # Bob 订阅任务 100
    manager.subscribe_task(3, 200)  # Charlie 订阅任务 200

    # 3. 任务更新广播
    print("\n3️⃣ 任务更新广播")
    await redis_pubsub.broadcast_task_update(
        task_id=100,
        event_type=MessageType.TASK_UPDATE.value,
        data={"title": "完成报告", "status": "in_progress"}
    )

    # 4. WebSocket 消息发送
    print("\n4️⃣ WebSocket 消息发送")
    msg = WebSocketMessage(
        type=MessageType.NOTIFICATION,
        data={"message": "新任务已分配给你"}
    )
    await manager.send_to_user(1, msg)

    # 模拟接收
    try:
        received = await asyncio.wait_for(user_queues[1].get(), timeout=1)
        print(f"  ✓ 用户 1 收到消息: {received['type']}")
    except asyncio.TimeoutError:
        pass

    # 5. 取消订阅
    print("\n5️⃣ 取消订阅")
    manager.unsubscribe_task(1, 100)

    # 6. 用户断开
    print("\n6️⃣ 用户断开连接")
    manager.unsubscribe_user(1, user_queues[1])

    print("\n" + "=" * 60)


async def demonstrate_heartbeat():
    """演示心跳检测"""
    print("\n" + "=" * 60)
    print("心跳检测与断线重连")
    print("=" * 60)

    manager = ConnectionManager()
    heartbeat = HeartbeatManager(manager, interval=5)

    # 模拟连接
    queue = asyncio.Queue()
    manager.subscribe_user(1, queue)

    # 启动心跳 (只演示一次)
    print("\n❤️ 启动心跳检测...")
    # 实际应用中这会持续运行
    await asyncio.sleep(1)  # 模拟运行

    manager.unsubscribe_user(1, queue)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(demonstrate_websocket())
    asyncio.run(demonstrate_heartbeat())
