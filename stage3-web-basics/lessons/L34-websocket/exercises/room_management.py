"""

from __future__ import annotations

练习 1: 房间管理增强

当前 ChatRoom 的 broadcast 方法逐个发送消息到每个连接。
当一个连接断开时，会引发 WebSocketDisconnect 异常。

要求:
1. 在 broadcast 中添加异常处理，断开时从 room 移除该连接
2. 添加 get_online_count(room) 方法返回指定房间的在线人数
3. 添加 list_rooms() 方法返回所有活跃房间列表

附加: 为 ChatRoom 类编写文档字符串，说明线程安全性
"""
