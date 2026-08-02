"""Example 2: Redis PubSub Integration"""

import asyncio
from collections.abc import Callable
import redis.asyncio as redis
import json
from dataclasses import dataclass


@dataclass
class RedisManager:
    """Redis connection manager."""

    client: redis.Redis
    pubsub: redis.client.PubSub

    @classmethod
    async def create(cls, url: str = "redis://localhost:6379"):
        client = redis.from_url(url)
        pubsub = client.pubsub()
        return cls(client=client, pubsub=pubsub)

    async def publish(self, channel: str, message: dict):
        """Publish message to channel."""
        await self.client.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str):
        """Subscribe to channel."""
        await self.pubsub.subscribe(channel)

    async def listen(self, callback: Callable):
        """Listen for messages."""
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await callback(message["channel"], data)


class WebSocketBridge:
    """Bridge WebSocket connections with Redis PubSub."""

    def __init__(self, redis_manager: RedisManager):
        self.redis = redis_manager
        self.subscriptions: dict[str, set[asyncio.Queue]] = {}

    async def subscribe_websocket(self, channel: str, queue: asyncio.Queue):
        """Subscribe a WebSocket to a Redis channel."""
        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()
            await self.redis.subscribe(channel)

        self.subscriptions[channel].add(queue)

    async def broadcast_to_websocket(self, channel: str, message: dict):
        """Send message to all WebSockets subscribed to channel."""
        if channel in self.subscriptions:
            for queue in self.subscriptions[channel]:
                await queue.put(message)

    async def handle_redis_message(self, channel: str, data: dict):
        """Handle message from Redis, broadcast to WebSockets."""
        await self.broadcast_to_websocket(channel, data)

    async def start_listener(self):
        """Start listening to Redis channels."""
        await self.redis.listen(self.handle_redis_message)


async def main():
    # Create Redis manager
    redis_mgr = await RedisManager.create()

    # Create bridge
    bridge = WebSocketBridge(redis_mgr)

    # Simulate WebSocket subscription
    ws_queue = asyncio.Queue()
    await bridge.subscribe_websocket("updates", ws_queue)

    # Simulate Redis publish
    await redis_mgr.publish("updates", {"type": "update", "data": "Hello"})

    # Receive in WebSocket
    message = await asyncio.wait_for(ws_queue.get(), timeout=5.0)
    print(f"Received: {message}")

    await redis_mgr.client.close()


if __name__ == "__main__":
    asyncio.run(main())
