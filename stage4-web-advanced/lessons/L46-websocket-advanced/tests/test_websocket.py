"""Tests for WebSocket module."""

from __future__ import annotations

import asyncio
import time
import pytest
from solutions.solution_01_websocket import ConnectionManager, ConnectionInfo


class MockWebSocket:
    """Mock WebSocket for testing."""

    def __init__(self):
        self.accepted = False
        self.messages: list = []
        self.closed = False

    async def accept(self):
        self.accepted = True

    async def send_json(self, data):
        self.messages.append(data)

    async def close(self):
        self.closed = True


class TestConnectionManager:
    """Test ConnectionManager."""

    @pytest.mark.asyncio
    async def test_connection_stats(self):
        """Test connection statistics."""
        manager = ConnectionManager()
        assert manager.connection_count == 0
        assert manager.channel_stats == {}

    @pytest.mark.asyncio
    async def test_disconnect_nonexistent(self):
        """Test disconnecting non-existent connection."""
        manager = ConnectionManager()

        class MockWS:
            pass

        # Should not raise
        await manager.disconnect(MockWS())

    @pytest.mark.asyncio
    async def test_connect_websocket(self):
        """Test connecting a WebSocket."""
        manager = ConnectionManager()
        ws = MockWebSocket()

        result = await manager.connect(ws, channel="test", user_id="user1")

        assert result is True
        assert ws.accepted is True
        assert manager.connection_count == 1
        assert "test" in manager.channels

    @pytest.mark.asyncio
    async def test_connect_multiple_channels(self):
        """Test connecting to multiple channels."""
        manager = ConnectionManager()
        ws1 = MockWebSocket()
        ws2 = MockWebSocket()

        await manager.connect(ws1, channel="ch1", user_id="user1")
        await manager.connect(ws2, channel="ch2", user_id="user2")

        assert manager.connection_count == 2
        stats = manager.channel_stats
        assert stats["ch1"] == 1
        assert stats["ch2"] == 1

    @pytest.mark.asyncio
    async def test_broadcast_to_channel(self):
        """Test broadcasting to a channel."""
        manager = ConnectionManager()
        ws1 = MockWebSocket()
        ws2 = MockWebSocket()

        await manager.connect(ws1, channel="broadcast")
        await manager.connect(ws2, channel="broadcast")

        message = {"type": "broadcast", "content": "hello"}
        await manager.broadcast("broadcast", message)

        assert len(ws1.messages) == 1
        assert len(ws2.messages) == 1
        assert ws1.messages[0] == message
        assert ws2.messages[0] == message

    @pytest.mark.asyncio
    async def test_broadcast_excludes_other_channels(self):
        """Test broadcast only goes to specified channel."""
        manager = ConnectionManager()
        ws1 = MockWebSocket()
        ws2 = MockWebSocket()

        await manager.connect(ws1, channel="ch1")
        await manager.connect(ws2, channel="ch2")

        await manager.broadcast("ch1", {"msg": "ch1 only"})

        assert len(ws1.messages) == 1
        assert len(ws2.messages) == 0

    @pytest.mark.asyncio
    async def test_send_to_user(self):
        """Test sending message to specific user."""
        manager = ConnectionManager()
        ws1 = MockWebSocket()
        ws2 = MockWebSocket()

        await manager.connect(ws1, channel="default", user_id="alice")
        await manager.connect(ws2, channel="default", user_id="bob")

        result = await manager.send_to_user("alice", {"msg": "for alice"})

        assert result is True
        assert len(ws1.messages) == 1
        assert ws1.messages[0]["msg"] == "for alice"
        assert len(ws2.messages) == 0  # bob should not receive

    @pytest.mark.asyncio
    async def test_send_to_nonexistent_user(self):
        """Test sending to non-existent user returns False."""
        manager = ConnectionManager()
        ws = MockWebSocket()
        await manager.connect(ws, channel="default", user_id="alice")

        result = await manager.send_to_user("nonexistent", {"msg": "hello"})

        assert result is False

    @pytest.mark.asyncio
    async def test_heartbeat_updates_timestamp(self):
        """Test heartbeat updates connection timestamp."""
        manager = ConnectionManager()
        ws = MockWebSocket()

        await manager.connect(ws, channel="default", user_id="user1")
        initial_heartbeat = manager.connections[ws].last_heartbeat

        # Wait a tiny bit
        await asyncio.sleep(0.01)

        await manager.handle_heartbeat(ws)
        new_heartbeat = manager.connections[ws].last_heartbeat

        assert new_heartbeat >= initial_heartbeat

    @pytest.mark.asyncio
    async def test_disconnect_removes_from_channel(self):
        """Test disconnect removes connection from channel."""
        manager = ConnectionManager()
        ws = MockWebSocket()

        await manager.connect(ws, channel="test", user_id="user1")
        assert manager.channel_stats["test"] == 1

        await manager.disconnect(ws)

        assert manager.connection_count == 0
        assert manager.channel_stats.get("test", 0) == 0


class TestConnectionInfo:
    """Test ConnectionInfo."""

    def test_info_creation(self):
        """Test creating connection info."""
        info = ConnectionInfo(user_id="user123", channel="general", last_heartbeat=time.time())
        assert info.user_id == "user123"
        assert info.channel == "general"

    def test_info_with_metadata(self):
        """Test creating connection info with metadata."""
        info = ConnectionInfo(
            user_id="user456",
            channel="private",
            last_heartbeat=time.time(),
            metadata={"role": "admin", "session": "abc123"},
        )
        assert info.metadata["role"] == "admin"
        assert info.metadata["session"] == "abc123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
