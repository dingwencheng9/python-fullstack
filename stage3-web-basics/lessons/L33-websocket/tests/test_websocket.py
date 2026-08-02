"""L33 WebSocket 测试"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from solutions.solution_02 import ChatRoom as ChatRoomSolution, DisconnectError


@pytest.mark.asyncio
async def test_chatroom_join():
    """测试加入房间"""
    room = ChatRoomSolution()
    ws = AsyncMock()
    ws.send_text = AsyncMock()
    await room.join("general", ws)
    assert room.get_online_count("general") == 1


@pytest.mark.asyncio
async def test_chatroom_leave():
    """测试离开房间"""
    room = ChatRoomSolution()
    ws = AsyncMock()
    ws.send_text = AsyncMock()
    await room.join("general", ws)
    await room.leave("general", ws)
    assert room.get_online_count("general") == 0


@pytest.mark.asyncio
async def test_broadcast():
    """测试广播消息"""
    room = ChatRoomSolution()
    ws1, ws2 = AsyncMock(), AsyncMock()
    ws1.send_text = AsyncMock()
    ws2.send_text = AsyncMock()
    await room.join("general", ws1)
    await room.join("general", ws2)
    await room.broadcast("general", "hello")
    ws1.send_text.assert_called_once_with("hello")
    ws2.send_text.assert_called_once_with("hello")


@pytest.mark.asyncio
async def test_broadcast_disconnect_handling():
    """测试广播时断开的连接被清理"""
    room = ChatRoomSolution()
    ws1 = AsyncMock()
    ws1.send_text = AsyncMock(side_effect=DisconnectError("连接断开"))
    ws2 = AsyncMock()
    ws2.send_text = AsyncMock()
    await room.join("general", ws1)
    await room.join("general", ws2)
    await room.broadcast("general", "test")
    assert room.get_online_count("general") == 1


@pytest.mark.parametrize(
    "rooms_join,room_check,expected_count",
    [
        ([("alpha", "ws1")], "alpha", 1),
        ([("alpha", "ws1"), ("beta", "ws1")], "alpha", 1),
    ],
)
@pytest.mark.asyncio
async def test_parametrized_room_join(rooms_join, room_check, expected_count):
    """参数化：不同房间的加入和查询"""
    room = ChatRoomSolution()
    ws = AsyncMock()
    ws.send_text = AsyncMock()
    for r, _ in rooms_join:
        await room.join(r, ws)
    assert room.get_online_count(room_check) == expected_count


@pytest.mark.asyncio
async def test_broadcast_nonexistent_room():
    """测试向不存在的房间广播不会报错"""
    room = ChatRoomSolution()
    result = await room.broadcast("ghost", "hello")
    assert result is None


def test_list_rooms():
    """测试列出活跃房间"""
    room = ChatRoomSolution()
    assert room.list_rooms() == []


@pytest.mark.asyncio
async def test_multiple_rooms():
    """测试多房间隔离"""
    room = ChatRoomSolution()
    ws = AsyncMock()
    ws.send_text = AsyncMock()
    await room.join("room-a", ws)
    await room.join("room-b", ws)
    assert room.get_online_count("room-a") == 1
    assert room.get_online_count("room-b") == 1
    assert len(room.list_rooms()) == 2
