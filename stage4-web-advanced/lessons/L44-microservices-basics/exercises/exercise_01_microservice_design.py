# exercises/exercise_01_microservice_design.py
"""
练习 1: 微服务设计实践

本练习要求你设计并实现一个简单的微服务通信系统。
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Callable
# ==================== 练习题目 ====================

"""
## 练习要求

实现一个简单的微服务间 RPC 通信系统：

### 架构

```
客户端 → RPC Client → [消息队列] → RPC Server → 服务
```

### 要求

1. **RPC 消息格式**:
   - 包含: method, params, request_id
   - 支持请求/响应模式

2. **消息队列**:
   - 异步消息传递
   - 支持请求-响应匹配

3. **RPC Server**:
   - 注册服务方法
   - 处理请求
   - 返回响应

4. **RPC Client**:
   - 发送请求
   - 等待响应
   - 超时处理

### 示例输出

```
=== 微服务 RPC 演示 ===
[1] 发送请求: calculate_sum(a=10, b=20)
  响应: {'result': 30, 'request_id': 'req-1'}

[2] 发送请求: get_user_info(user_id=42)
  响应: {'user': {'id': 42, 'name': 'User 42'}, 'request_id': 'req-2'}

[3] 测试超时
  请求超时: request_id='req-timeout'
```
"""


# ==================== RPC 消息（需要实现） ====================


@dataclass
class RPCMessage:
    """RPC 消息"""

    method: str
    params: dict
    request_id: str

    def to_dict(self) -> dict:
        """序列化为字典"""
        # TODO: 实现序列化
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "RPCMessage":
        """从字典反序列化"""
        # TODO: 实现反序列化
        pass


# ==================== 消息队列（需要实现） ====================


class MessageQueue:
    """异步消息队列"""

    def __init__(self):
        # TODO: 实现消息队列
        pass

    async def put(self, message: RPCMessage, queue_name: str = "default") -> None:
        """发送消息到队列"""
        # TODO: 实现发送逻辑
        pass

    async def get(self, queue_name: str = "default") -> RPCMessage:
        """从队列获取消息"""
        # TODO: 实现获取逻辑（阻塞等待）
        pass

    async def reply(self, message: RPCMessage, queue_name: str = "default") -> None:
        """发送响应到队列"""
        # TODO: 实现响应逻辑
        pass


# ==================== RPC Server（需要实现） ====================


class RPCServer:
    """RPC 服务器"""

    def __init__(self, queue: MessageQueue):
        self.queue = queue
        self._handlers: dict[str, Callable] = {}

    def register(self, method_name: str, handler: Callable) -> None:
        """注册方法处理器"""
        # TODO: 实现注册逻辑
        pass

    async def start(self) -> None:
        """启动服务器"""
        # TODO: 实现服务循环
        pass


# ==================== RPC Client（需要实现） ====================


class RPCClient:
    """RPC 客户端"""

    def __init__(self, queue: MessageQueue, timeout: float = 5.0):
        self.queue = queue
        self.timeout = timeout
        self._pending: dict[str, asyncio.Future] = {}
        self._request_counter = 0

    def _generate_request_id(self) -> str:
        """生成请求 ID"""
        # TODO: 实现 ID 生成
        pass

    async def call(self, method: str, **params) -> Any:
        """调用远程方法"""
        # TODO: 实现 RPC 调用
        # 1. 生成 request_id
        # 2. 创建请求消息
        # 3. 发送请求到队列
        # 4. 等待响应
        # 5. 返回结果或抛出超时异常
        pass


# ==================== 测试代码（无需修改） ====================


async def test_rpc_system():
    """测试 RPC 系统"""
    print("\n" + "=" * 60)
    print("微服务 RPC 系统测试")
    print("=" * 60)

    # 初始化
    queue = MessageQueue()
    server = RPCServer(queue)
    client = RPCClient(queue)

    # 注册服务
    def calculate_sum(a: int, b: int) -> int:
        return a + b

    def get_user_info(user_id: int) -> dict:
        return {"id": user_id, "name": f"User {user_id}"}

    server.register("calculate_sum", calculate_sum)
    server.register("get_user_info", get_user_info)

    # 启动服务器
    server_task = asyncio.create_task(server.start())

    # 等待服务器启动
    await asyncio.sleep(0.1)

    # 测试调用
    print("\n[1] 调用 calculate_sum")
    result = await client.call("calculate_sum", a=10, b=20)
    print(f"    结果: {result}")

    print("\n[2] 调用 get_user_info")
    result = await client.call("get_user_info", user_id=42)
    print(f"    结果: {result}")

    # 清理
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_rpc_system())


# ==================== 验收标准 ====================

"""
验收标准：

1. [ ] RPCMessage.to_dict() 能正确序列化
2. [ ] RPCMessage.from_dict() 能正确反序列化
3. [ ] MessageQueue.put() 能发送消息
4. [ ] MessageQueue.get() 能阻塞获取消息
5. [ ] RPCServer.register() 能注册方法
6. [ ] RPCServer.start() 能处理请求并返回响应
7. [ ] RPCClient.call() 能发送请求并获取响应
8. [ ] 超时机制能正常工作
9. [ ] 多个并发请求能正确处理
"""
