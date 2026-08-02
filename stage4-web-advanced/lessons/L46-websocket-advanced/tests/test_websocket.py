"""Tests for WebSocket module."""

import pytest
from solutions.solution_01_websocket import ConnectionManager, ConnectionInfo


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


class TestConnectionInfo:
    """Test ConnectionInfo."""

    def test_info_creation(self):
        """Test creating connection info."""
        import time

        info = ConnectionInfo(user_id="user123", channel="general", last_heartbeat=time.time())
        assert info.user_id == "user123"
        assert info.channel == "general"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
