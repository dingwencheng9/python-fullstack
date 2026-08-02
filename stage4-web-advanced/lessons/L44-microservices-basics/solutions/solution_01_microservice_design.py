# solutions/solution_01_microservice_design.py
"""
练习 1 参考答案: 微服务 RPC 系统
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Callable
# ==================== RPC 消息 ====================


@dataclass
class RPCMessage:
    """RPC 消息"""

    method: str
    params: dict
    request_id: str

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {"method": self.method, "params": self.params, "request_id": self.request_id}

    @classmethod
    def from_dict(cls, data: dict) -> "RPCMessage":
        """从字典反序列化"""
        return cls(method=data["method"], params=data["params"], request_id=data["request_id"])


# ==================== 消息队列 ====================


class MessageQueue:
    """异步消息队列"""

    def __init__(self):
        self._queues: dict[str, asyncio.Queue] = {}

    def _get_or_create_queue(self, name: str) -> asyncio.Queue:
        """获取或创建队列"""
        if name not in self._queues:
            self._queues[name] = asyncio.Queue()
        return self._queues[name]

    async def put(self, message: RPCMessage, queue_name: str = "default") -> None:
        """发送消息到队列"""
        queue = self._get_or_create_queue(queue_name)
        await queue.put(message)

    async def get(self, queue_name: str = "default") -> RPCMessage:
        """从队列获取消息"""
        queue = self._get_or_create_queue(queue_name)
        return await queue.get()

    async def reply(self, message: RPCMessage, queue_name: str = "default") -> None:
        """发送响应到队列"""
        await self.put(message, queue_name)


# ==================== RPC Server ====================


class RPCServer:
    """RPC 服务器"""

    def __init__(self, queue: MessageQueue):
        self.queue = queue
        self._handlers: dict[str, Callable] = {}
        self._running = False

    def register(self, method_name: str, handler: Callable) -> None:
        """注册方法处理器"""
        self._handlers[method_name] = handler

    async def _handle_request(self, message: RPCMessage) -> RPCMessage:
        """处理请求"""
        handler = self._handlers.get(message.method)

        if not handler:
            return RPCMessage(
                method=message.method,
                params={"error": f"方法不存在: {message.method}"},
                request_id=message.request_id,
            )

        try:
            result = handler(**message.params)
            # 如果是协程，等待完成
            if asyncio.iscoroutinefunction(handler):
                result = await result
            return RPCMessage(
                method=message.method, params={"result": result}, request_id=message.request_id
            )
        except Exception as e:
            return RPCMessage(
                method=message.method, params={"error": str(e)}, request_id=message.request_id
            )

    async def start(self) -> None:
        """启动服务器"""
        self._running = True
        queue_name = "rpc_requests"

        while self._running:
            try:
                # 等待请求
                request = await asyncio.wait_for(self.queue.get(queue_name), timeout=1.0)

                # 处理请求
                response = await self._handle_request(request)

                # 发送响应
                response_queue = f"rpc_response_{request.request_id}"
                await self.queue.reply(response, response_queue)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"  [Server] 错误: {e}")


# ==================== RPC Client ====================


class RPCClient:
    """RPC 客户端"""

    def __init__(self, queue: MessageQueue, timeout: float = 5.0):
        self.queue = queue
        self.timeout = timeout
        self._pending: dict[str, asyncio.Future] = {}
        self._request_counter = 0

    def _generate_request_id(self) -> str:
        """生成请求 ID"""
        self._request_counter += 1
        return f"req-{self._request_counter}"

    async def call(self, method: str, **params) -> Any:
        """调用远程方法"""
        request_id = self._generate_request_id()
        request_queue = "rpc_requests"

        # 创建响应 Future
        response_future: asyncio.Future = asyncio.Future()
        self._pending[request_id] = response_future

        try:
            # 发送请求
            request = RPCMessage(method=method, params=params, request_id=request_id)
            await self.queue.put(request, request_queue)

            # 等待响应
            response = await asyncio.wait_for(response_future, timeout=self.timeout)

            # 检查错误
            if "error" in response.params:
                raise RPCError(f"RPC 调用失败: {response.params['error']}")

            return response.params.get("result")

        except asyncio.TimeoutError:
            raise RPCError(f"RPC 调用超时: {method}")

        finally:
            self._pending.pop(request_id, None)


class RPCError(Exception):
    """RPC 错误"""

    pass


# ==================== 测试代码 ====================


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

    def slow_operation(value: int) -> int:
        import time

        time.sleep(0.1)
        return value * 2

    server.register("calculate_sum", calculate_sum)
    server.register("get_user_info", get_user_info)
    server.register("slow_operation", slow_operation)

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

    print("\n[3] 并发调用")
    results = await asyncio.gather(
        client.call("calculate_sum", a=1, b=2),
        client.call("calculate_sum", a=3, b=4),
        client.call("get_user_info", user_id=100),
    )
    print(f"    结果: {results}")

    # 测试超时
    print("\n[4] 测试超时")
    try:
        result = await asyncio.wait_for(client.call("slow_operation", value=42), timeout=0.05)
        print(f"    结果: {result}")
    except asyncio.TimeoutError:
        print("    操作超时（预期行为）")

    # 测试不存在的方法
    print("\n[5] 测试不存在的方法")
    try:
        result = await client.call("nonexistent_method")
    except RPCError as e:
        print(f"    错误: {e}")

    # 清理
    server._running = False
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
