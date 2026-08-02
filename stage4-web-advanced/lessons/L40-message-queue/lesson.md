# L40: 消息队列与实时通信

> **课程编号**: L40
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 6-8 小时
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L36, L37
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **消息队列基础**：理解队列模型、Producer-Consumer 模式
2. ✅ **Celery 任务队列**：掌握 Celery 任务定义、调度、监控
3. ✅ **消息模式**：实现消息确认、重试、死信队列
4. ✅ **WebSocket 实时通信**：实现双向实时通信
5. ✅ **广播与群组**：实现聊天室、实时协作
6. ✅ **混合架构**：组合消息队列与 WebSocket

---

## Part 1: 为什么需要消息队列

### 1.1 同步请求的问题

```
┌─────────────────────────────────────────────────────────┐
│                   同步请求的问题                         │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  用户点击 → API 接收 → [处理 30 秒] → 返回结果        │
│                                                     │
│  问题：                                            │
│  • 用户等待太久，体验差                             │
│  • 请求超时（浏览器 30s 超时）                      │
│  • 高峰期服务被打爆                                 │
│  • 失败后无法重试                                   │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 队列模型

```
┌─────────────────────────────────────────────────────────┐
│                   消息队列模型                          │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  Producer ──→ [Message Queue] ──→ Consumer         │
│                             │                         │
│                             ├──→ Worker 1           │
│                             ├──→ Worker 2           │
│                             └──→ Worker N           │
│                                                     │
│  优势：                                            │
│  • 解耦：生产者与消费者独立                         │
│  • 削峰：高峰期任务排队，平滑处理                   │
│  • 异步：立即响应，后台处理                         │
│  • 重试：失败自动重试，保证可靠性                   │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 1.3 适用场景

| 场景 | 同步/异步 | 原因 |
|------|----------|------|
| 发送邮件 | 异步 | 不阻塞响应 |
| 生成 PDF 报告 | 异步 | 耗时操作 |
| 视频转码 | 异步 | CPU 密集 |
| 发送短信 | 异步 | 依赖外部 API |
| 用户注册确认 | 异步 | 不阻塞注册流程 |
| 订单支付回调 | 同步 | 需要即时结果 |
| 实时聊天消息 | WebSocket | 双向实时 |
| 股票行情推送 | WebSocket | 实时数据 |
| 游戏操作同步 | WebSocket | 低延迟 |

---

## Part 2: 消息队列基础

### 2.1 核心概念

```python
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from datetime import datetime
from typing import Any, Optional

class MessagePriority(str, Enum):
    """消息优先级"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Message:
    """消息模型"""
    topic: str                    # 主题/队列名
    payload: dict                 # 消息内容
    message_id: str = field(default_factory=lambda: str(uuid4()))
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    retry_count: int = 0
    max_retries: int = 3
    headers: dict = field(default_factory=dict)

    @property
    def should_retry(self) -> bool:
        return self.retry_count < self.max_retries

    @property
    def backoff_seconds(self) -> int:
        """指数退避"""
        return min(60, 2 ** self.retry_count)
```

### 2.2 内存版队列

```python
from collections import deque
from threading import Lock
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)

class InMemoryQueue:
    """内存消息队列（仅用于学习和演示）"""

    def __init__(self, max_size: int = 10000):
        self._queue = deque(maxlen=max_size)
        self._results: dict[str, dict] = {}
        self._lock = Lock()

    def enqueue(self, message: Message) -> str:
        """入队"""
        with self._lock:
            self._queue.append(message)
            self._results[message.message_id] = {
                "status": "pending",
                "message": message
            }
        logger.info(f"Enqueued message {message.message_id} to {message.topic}")
        return message.message_id

    def dequeue(self) -> Optional[Message]:
        """出队"""
        with self._lock:
            if self._queue:
                message = self._queue.popleft()
                self._results[message.message_id]["status"] = "processing"
                return message
        return None

    def acknowledge(self, message_id: str, result: Any = None):
        """确认消息已处理"""
        with self._lock:
            if message_id in self._results:
                self._results[message_id]["status"] = "completed"
                self._results[message_id]["result"] = result
                self._results[message_id]["completed_at"] = datetime.now()

    def reject(self, message_id: str, error: str):
        """拒绝消息"""
        with self._lock:
            if message_id in self._results:
                self._results[message_id]["status"] = "failed"
                self._results[message_id]["error"] = error

    def get_status(self, message_id: str) -> Optional[dict]:
        """获取消息状态"""
        return self._results.get(message_id)

    def size(self) -> int:
        """队列大小"""
        with self._lock:
            return len(self._queue)
```

### 2.3 Worker 消费者

```python
import asyncio
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class Worker:
    """消息队列 Worker"""

    def __init__(self, queue: InMemoryQueue):
        self.queue = queue
        self.handlers: dict[str, Callable] = {}
        self._running = False

    def register(self, topic: str, handler: Callable):
        """注册消息处理器"""
        self.handlers[topic] = handler
        logger.info(f"Registered handler for topic: {topic}")

    async def process_message(self, message: Message) -> bool:
        """处理单条消息"""
        handler = self.handlers.get(message.topic)

        if not handler:
            logger.error(f"No handler for topic: {message.topic}")
            return False

        try:
            # 调用处理器
            result = await handler(message.payload)

            # 确认成功
            self.queue.acknowledge(message.message_id, result)
            logger.info(f"Processed message {message.message_id}: {result}")
            return True

        except Exception as e:
            logger.error(f"Failed to process message {message.message_id}: {e}")

            # 判断是否重试
            if message.should_retry:
                message.retry_count += 1
                await asyncio.sleep(message.backoff_seconds)
                self.queue.enqueue(message)
                logger.info(f"Requeued message {message.message_id}, retry {message.retry_count}")
            else:
                # 进入死信队列
                self.queue.reject(message.message_id, str(e))
                logger.error(f"Message {message.message_id} moved to DLQ")

            return False

    async def run(self):
        """运行 Worker"""
        self._running = True
        logger.info("Worker started")

        while self._running:
            message = self.queue.dequeue()

            if message:
                await self.process_message(message)
            else:
                await asyncio.sleep(0.1)  # 避免空转

    def stop(self):
        """停止 Worker"""
        self._running = False
        logger.info("Worker stopped")
```

---

## Part 3: Celery 任务队列

### 3.1 Celery 架构

```
┌─────────────────────────────────────────────────────────┐
│                   Celery 架构                          │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  应用 ──→ [Broker: Redis/RabbitMQ] ──→ [Workers]   │
│          │                              │              │
│          │                              ├──→ Worker 1 │
│          │                              ├──→ Worker 2 │
│          │                              └──→ Worker N │
│          │                                                │
│          └──→ [Result Backend: Redis]                 │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Celery 基础配置

```python
# celery_app.py
from celery import Celery
from celery.schedules import crontab

# 创建 Celery 实例
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',      # 消息队列
    backend='redis://localhost:6379/1',      # 结果存储
    include=['app.tasks']                    # 任务模块
)

# 配置
app.conf.update(
    # 任务序列化
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],

    # 时区
    timezone='Asia/Shanghai',
    enable_utc=True,

    # 任务路由
    task_routes={
        'tasks.high_priority.*': {'queue': 'high'},
        'tasks.default.*': {'queue': 'default'},
        'tasks.low_priority.*': {'queue': 'low'},
    },

    # 任务结果过期
    result_expires=3600,

    # 任务追踪
    task_track_started=True,
    task_send_sent_event=True,

    # 限流
    task_annotations={
        'tasks.send_sms': {'rate_limit': '10/m'}
    },
)

# 定时任务配置
app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'tasks.cleanup_sessions',
        'schedule': 3600.0,  # 每小时
    },
    'send-daily-report': {
        'task': 'tasks.send_daily_report',
        'schedule': crontab(hour=8, minute=0),  # 每天 8:00
    },
    'sync-inventory': {
        'task': 'tasks.sync_inventory',
        'schedule': crontab(minute='*/15'),  # 每 15 分钟
    },
}
```

### 3.3 任务定义

```python
# app/tasks/__init__.py
from celery_app import app

@app.task(bind=True)
def send_email(self, to: str, subject: str, body: str):
    """发送邮件任务"""
    logger = self.logger
    logger.info(f"Sending email to {to}")

    try:
        # 实际发邮件逻辑
        result = email_service.send(to, subject, body)
        return {"status": "sent", "message_id": result.message_id}
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)

@app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def process_payment(self, order_id: int, amount: float):
    """处理支付 - 自动重试"""
    logger = self.logger
    logger.info(f"Processing payment for order {order_id}, amount: {amount}")

    payment = payment_service.charge(order_id, amount)
    return {"payment_id": payment.id, "status": payment.status}

@app.task
def generate_report(report_type: str, date_range: dict) -> dict:
    """生成报告 - 同步返回"""
    report = report_generator.create(
        report_type=report_type,
        start_date=date_range['start'],
        end_date=date_range['end']
    )
    return {
        "report_id": report.id,
        "download_url": report.download_url
    }
```

### 3.4 调用任务

```python
# 调用方式 1：延迟调用（fire and forget）
result = send_email.delay("user@example.com", "Hello", "Body")
print(result.id)  # 获取任务 ID

# 调用方式 2：签名调用
from celery import signature
sig = send_email.s("user@example.com", "Hello", "Body")
sig.apply_async(countdown=60)  # 60 秒后执行

# 调用方式 3：apply_async（高级选项）
send_email.apply_async(
    kwargs={"to": "user@example.com", "subject": "Hello"},
    countdown=60,           # 60 秒后执行
    eta=datetime(2024, 1, 15, 12, 0),  # 指定时间执行
    priority=5,              # 优先级 0-9
    headers={"x-customer-id": "123"},
)

# 等待结果（同步）
result = generate_report.apply_async(
    kwargs={"report_type": "sales", "date_range": {...}}
)
if result.ready():
    print(result.get(timeout=10))  # 获取结果，最多等 10 秒

# 取消任务
result.revoke(terminate=True)

# 任务组（并行执行）
from celery import group, chain, chord

# Group：并行执行多个任务
job = group(
    send_email.s(user.email, "Subject 1", "Body 1"),
    send_email.s(user.email, "Subject 2", "Body 2"),
    send_email.s(user.email, "Subject 3", "Body 3"),
)()

# 等待所有任务完成
results = job.get()
print(results)  # [{status: sent}, {status: sent}, {status: sent}]

# Chain：顺序执行
result = chain(
    fetch_data.s(url="https://api.example.com"),
    process_data.s(),
    store_results.s(),
)()

# Chord：带回调
result = chord(
    [process_item.s(item) for item in items],
    generate_report.s()
)()
```

---

## Part 4: 消息模式与可靠性

### 4.1 消息确认模式

```python
class ReliableQueue:
    """可靠消息队列"""

    def __init__(self, redis_client, queue_name: str):
        self.redis = redis_client
        self.queue_name = queue_name
        self.processing_key = f"processing:{queue_name}"
        self.dlq_key = f"dlq:{queue_name}"

    async def publish(self, message: dict) -> str:
        """发布消息"""
        import json
        message_id = str(uuid4())
        message['message_id'] = message_id
        await self.redis.lpush(self.queue_name, json.dumps(message))
        return message_id

    async def consume(self, timeout: int = 5) -> Optional[dict]:
        """消费消息（带确认）"""
        import json

        # 阻塞获取消息
        result = await self.redis.brpoplpush(
            self.queue_name,
            self.processing_key,
            timeout=timeout
        )

        if result:
            return json.loads(result)
        return None

    async def acknowledge(self, message_id: str):
        """确认消息已处理"""
        import json
        # 从 processing 队列删除
        items = await self.redis.lrange(self.processing_key, 0, -1)
        for item in items:
            msg = json.loads(item)
            if msg.get('message_id') == message_id:
                await self.redis.lrem(self.processing_key, 1, item)
                break

    async def reject(self, message_id: str, error: str):
        """拒绝消息"""
        import json
        items = await self.redis.lrange(self.processing_key, 0, -1)
        for item in items:
            msg = json.loads(item)
            if msg.get('message_id') == message_id:
                msg['error'] = error
                msg['rejected_at'] = datetime.now().isoformat()
                # 移动到 DLQ
                await self.redis.lpush(self.dlq_key, json.dumps(msg))
                await self.redis.lrem(self.processing_key, 1, item)
                break

    async def retry(self, message_id: str):
        """重试消息"""
        import json
        items = await self.redis.lrange(self.processing_key, 0, -1)
        for item in items:
            msg = json.loads(item)
            if msg.get('message_id') == message_id:
                msg['retry_count'] = msg.get('retry_count', 0) + 1
                await self.redis.lpush(self.queue_name, json.dumps(msg))
                await self.redis.lrem(self.processing_key, 1, item)
                break
```

### 4.2 死信队列

```python
class DeadLetterQueue:
    """死信队列处理"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.dlq_key = "dlq:messages"

    async def add(self, original_queue: str, message: dict, error: str):
        """添加到死信队列"""
        import json
        dlq_entry = {
            "original_queue": original_queue,
            "message": message,
            "error": error,
            "failed_at": datetime.now().isoformat(),
            "retry_count": message.get("retry_count", 0)
        }
        await self.redis.lpush(self.dlq_key, json.dumps(dlq_entry))

    async def get_failed_messages(self, limit: int = 10) -> list[dict]:
        """获取失败消息"""
        import json
        items = await self.redis.lrange(self.dlq_key, 0, limit - 1)
        return [json.loads(item) for item in items]

    async def replay(self, message_id: str, target_queue: str):
        """重放消息"""
        import json
        items = await self.redis.lrange(self.dlq_key, 0, -1)
        for item in items:
            dlq_entry = json.loads(item)
            if dlq_entry["message"].get("message_id") == message_id:
                message = dlq_entry["message"]
                message["retry_count"] = 0
                await self.redis.lpush(target_queue, json.dumps(message))
                await self.redis.lrem(self.dlq_key, 1, item)
                break

    async def purge(self, before_date: datetime):
        """清理旧消息"""
        import json
        items = await self.redis.lrange(self.dlq_key, 0, -1)
        count = 0
        for item in items:
            dlq_entry = json.loads(item)
            failed_at = datetime.fromisoformat(dlq_entry["failed_at"])
            if failed_at < before_date:
                await self.redis.lrem(self.dlq_key, 1, item)
                count += 1
        return count
```

### 4.3 幂等性设计

```python
class IdempotentProcessor:
    """幂等处理器"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.processed_key = "processed:messages"

    def generate_dedup_key(self, message: dict) -> str:
        """生成去重键"""
        # 基于消息内容生成唯一键
        import hashlib
        content = f"{message.get('type')}:{message.get('payload', {}).get('id')}"
        return hashlib.md5(content.encode()).hexdigest()

    async def is_processed(self, message: dict) -> bool:
        """检查是否已处理"""
        dedup_key = self.generate_dedup_key(message)
        return await self.redis.exists(f"{self.processed_key}:{dedup_key}")

    async def mark_processed(self, message: dict, ttl: int = 86400):
        """标记已处理"""
        dedup_key = self.generate_dedup_key(message)
        await self.redis.setex(
            f"{self.processed_key}:{dedup_key}",
            ttl,
            json.dumps({"processed_at": datetime.now().isoformat()})
        )

    async def process(self, message: dict, handler: Callable) -> Any:
        """幂等处理"""
        # 检查是否已处理
        if await self.is_processed(message):
            return {"status": "skipped", "reason": "already_processed"}

        # 处理消息
        result = await handler(message)

        # 标记已处理
        await self.mark_processed(message)

        return {"status": "processed", "result": result}


# 使用示例
idempotent = IdempotentProcessor(redis_client)

async def process_payment_handler(payload: dict) -> dict:
    """支付处理（幂等）"""
    payment = payment_service.charge(
        order_id=payload['order_id'],
        amount=payload['amount']
    )
    return {"payment_id": payment.id}

async def handle_payment_message(message: dict):
    """处理支付消息"""
    return await idempotent.process(
        message,
        process_payment_handler
    )
```

---

## Part 5: WebSocket 实时通信

### 5.1 WebSocket vs HTTP

```
┌─────────────────────────────────────────────────────────┐
│                   WebSocket vs HTTP                     │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  HTTP：                                            │
│  客户端 ──→ 请求 ──→ 服务器 ──→ 响应 ──→ 结束    │
│  每次都需要重新建立连接                            │
│  只能客户端主动发起请求                            │
│                                                     │
│  WebSocket：                                       │
│  客户端 ←── 握手 ──→ 服务器 ←── 保持连接 ←──    │
│  建立一次连接，双向持续通信                        │
│  服务器可以主动推送                                │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ WebSocket 适用场景：                         │   │
│  │ • 实时聊天、协作编辑                         │   │
│  │ • 游戏操作、股票行情                         │   │
│  │ • 实时通知、进度更新                         │   │
│  │ • IoT 设备状态监控                          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 5.2 FastAPI WebSocket 基础

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from datetime import datetime

app = FastAPI()

class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # 所有活跃连接
        self.active_connections: Dict[str, WebSocket] = {}
        # 房间 -> 连接列表
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """接受连接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        """断开连接"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            del self.active_connections[client_id]

            # 从所有房间移除
            for room_id, connections in self.rooms.items():
                if websocket in connections:
                    connections.remove(websocket)

    async def send_personal(self, message: dict, client_id: str):
        """发送个人消息"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(message)

    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(client_id)

    async def join_room(self, room_id: str, client_id: str):
        """加入房间"""
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            if websocket not in self.rooms[room_id]:
                self.rooms[room_id].append(websocket)

    async def leave_room(self, room_id: str, client_id: str):
        """离开房间"""
        if room_id in self.rooms and client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(websocket)

    async def broadcast_room(self, room_id: str, message: dict, exclude: str = None):
        """向房间广播消息"""
        if room_id not in self.rooms:
            return

        disconnected = []
        for websocket in self.rooms[room_id]:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)

        # 清理断开的连接
        for ws in disconnected:
            self.rooms[room_id].remove(ws)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket 端点"""
    await manager.connect(websocket, client_id)

    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()

            # 处理不同类型的消息
            msg_type = data.get("type")

            if msg_type == "message":
                # 广播消息
                await manager.broadcast({
                    "type": "message",
                    "sender": client_id,
                    "content": data.get("content"),
                    "timestamp": datetime.now().isoformat()
                })

            elif msg_type == "join_room":
                # 加入房间
                room_id = data.get("room_id")
                await manager.join_room(room_id, client_id)
                await manager.send_personal({
                    "type": "joined",
                    "room_id": room_id
                }, client_id)

            elif msg_type == "leave_room":
                # 离开房间
                room_id = data.get("room_id")
                await manager.leave_room(room_id, client_id)
                await manager.send_personal({
                    "type": "left",
                    "room_id": room_id
                }, client_id)

            elif msg_type == "room_message":
                # 房间消息
                room_id = data.get("room_id")
                await manager.broadcast_room(room_id, {
                    "type": "room_message",
                    "sender": client_id,
                    "content": data.get("content"),
                    "timestamp": datetime.now().isoformat()
                })

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast({
            "type": "disconnect",
            "client_id": client_id
        })
```

### 5.3 心跳机制

```python
import asyncio
from datetime import datetime

class HeartbeatManager:
    """心跳管理器"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.last_ping: Dict[WebSocket, datetime] = {}

    async def start_heartbeat(self, websocket: WebSocket, client_id: str):
        """启动心跳"""
        while True:
            try:
                # 发送 ping
                await websocket.send_json({
                    "type": "ping",
                    "timestamp": datetime.now().isoformat()
                })
                self.last_ping[websocket] = datetime.now()

                # 等待
                await asyncio.sleep(self.timeout)

                # 检查超时
                if websocket in self.last_ping:
                    last = self.last_ping[websocket]
                    if (datetime.now() - last).total_seconds() > self.timeout * 2:
                        await websocket.close()
                        return

            except Exception:
                break

    async def handle_pong(self, websocket: WebSocket):
        """处理 pong 响应"""
        self.last_ping[websocket] = datetime.now()

    def cleanup(self, websocket: WebSocket):
        """清理"""
        self.last_ping.pop(websocket, None)


heartbeat_manager = HeartbeatManager(timeout=30)

@app.websocket("/ws/{client_id}")
async def websocket_with_heartbeat(websocket: WebSocket, client_id: str):
    await websocket.accept()
    manager.connect(websocket, client_id)

    # 启动心跳
    heartbeat_task = asyncio.create_task(
        heartbeat_manager.start_heartbeat(websocket, client_id)
    )

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "pong":
                await heartbeat_manager.handle_pong(websocket)
            else:
                await handle_message(websocket, data)

    except WebSocketDisconnect:
        heartbeat_task.cancel()
        heartbeat_manager.cleanup(websocket)
        manager.disconnect(client_id)
```

### 5.4 聊天室实现

```python
from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    """聊天消息"""
    sender: str
    content: str
    timestamp: datetime = None
    room_id: Optional[str] = None

class ChatRoom:
    """聊天室"""

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        # 房间 -> 消息历史
        self.history: Dict[str, List[ChatMessage]] = {}
        # 房间 -> 连接
        self.connections: Dict[str, List[WebSocket]] = {}

    async def add_message(self, message: ChatMessage):
        """添加消息"""
        room_id = message.room_id or "default"

        if room_id not in self.history:
            self.history[room_id] = []

        self.history[room_id].append(message)

        # 限制历史长度
        if len(self.history[room_id]) > self.max_history:
            self.history[room_id] = self.history[room_id][-self.max_history:]

        # 广播消息
        await self.broadcast(room_id, message)

    async def broadcast(self, room_id: str, message: ChatMessage):
        """广播消息"""
        if room_id not in self.connections:
            return

        message_str = message.model_dump_json()

        disconnected = []
        for ws in self.connections[room_id]:
            try:
                await ws.send_text(message_str)
            except Exception:
                disconnected.append(ws)

        # 清理断开的连接
        for ws in disconnected:
            self.connections[room_id].remove(ws)

    def get_history(self, room_id: str, limit: int = 50) -> List[ChatMessage]:
        """获取历史消息"""
        history = self.history.get(room_id, [])
        return history[-limit:]

    async def join(self, room_id: str, websocket: WebSocket):
        """加入房间"""
        await websocket.accept()

        if room_id not in self.connections:
            self.connections[room_id] = []
        self.connections[room_id].append(websocket)

        # 发送历史消息
        history = self.get_history(room_id)
        for msg in history:
            await websocket.send_text(msg.model_dump_json())

        # 广播加入消息
        await self.add_message(ChatMessage(
            sender="system",
            content=f"User joined {room_id}",
            room_id=room_id
        ))

    async def leave(self, room_id: str, websocket: WebSocket):
        """离开房间"""
        if room_id in self.connections:
            if websocket in self.connections[room_id]:
                self.connections[room_id].remove(websocket)

chat_room = ChatRoom()

@app.websocket("/ws/chat/{room_id}/{username}")
async def chat_websocket(websocket: WebSocket, room_id: str, username: str):
    await chat_room.join(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()

            message = ChatMessage(
                sender=username,
                content=data,
                timestamp=datetime.now(),
                room_id=room_id
            )

            await chat_room.add_message(message)

    except WebSocketDisconnect:
        await chat_room.leave(room_id, websocket)
        await chat_room.add_message(ChatMessage(
            sender="system",
            content=f"User {username} left",
            room_id=room_id
        ))
```

---

## Part 6: 混合架构：消息队列 + WebSocket

### 6.1 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   混合架构                              │
├─────────────────────────────────────────────────────────┤
│                                                     │
│  HTTP 请求 ──→ [FastAPI] ──→ [消息队列] ──→ Worker   │
│                                     │                │
│                                     ↓                │
│  WebSocket ←── [广播服务] ←── [Worker 完成]            │
│                                     │                │
│                                     └──→ [数据库]    │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

### 6.2 实现：任务状态推送

```python
# 发布任务
@app.post("/reports")
async def create_report(req: ReportRequest, websocket_manager: WebSocketManager):
    # 创建任务
    task = Task(name="generate_report", payload=req.model_dump())
    task_id = queue.enqueue(task)

    # 立即返回
    return {"task_id": task_id, "status": "queued"}

# Worker 处理完成后推送
async def report_worker(queue: ReliableQueue, ws_manager: WebSocketManager):
    """报告生成 Worker"""
    while True:
        message = await queue.consume()

        if message and message.get("type") == "generate_report":
            try:
                # 处理任务
                result = await generate_report(message["payload"])

                # 更新数据库
                await update_task_status(message["message_id"], "completed", result)

                # 通过 WebSocket 推送
                await ws_manager.send_to_user(
                    user_id=message["payload"]["user_id"],
                    message={
                        "type": "task_completed",
                        "task_id": message["message_id"],
                        "result": result
                    }
                )

                await queue.acknowledge(message["message_id"])

            except Exception as e:
                await update_task_status(message["message_id"], "failed", str(e))
                await queue.reject(message["message_id"], str(e))
```

### 6.3 实时通知系统

```python
class NotificationService:
    """通知服务"""

    def __init__(
        self,
        queue: ReliableQueue,
        ws_manager: WebSocketManager
    ):
        self.queue = queue
        self.ws_manager = ws_manager

    async def notify_user(self, user_id: int, notification: dict):
        """通知用户（WebSocket + 消息队列）"""
        # 1. 尝试实时推送
        sent_realtime = await self.ws_manager.send_to_user(
            user_id=user_id,
            message={
                "type": "notification",
                "data": notification
            }
        )

        if not sent_realtime:
            # 2. 如果不在线，存入队列等待推送
            await self.queue.publish({
                "type": "notification",
                "user_id": user_id,
                "payload": notification
            })

    async def send_order_updates(self, order_id: int, status: str):
        """发送订单状态更新"""
        # 获取订单用户
        order = await get_order(order_id)

        await self.notify_user(order.user_id, {
            "type": "order_status",
            "order_id": order_id,
            "status": status,
            "message": f"订单状态更新为：{status}"
        })

    async def send_message_notification(self, from_user: str, to_user: str, message: str):
        """发送消息通知"""
        await self.notify_user(to_user, {
            "type": "new_message",
            "from": from_user,
            "content": message
        })
```

### 6.4 进度推送

```python
class ProgressTracker:
    """进度追踪器"""

    def __init__(self, ws_manager: WebSocketManager):
        self.ws_manager = ws_manager
        self.tasks: Dict[str, dict] = {}

    async def start_tracking(self, task_id: str, user_id: int, total: int):
        """开始追踪"""
        self.tasks[task_id] = {
            "user_id": user_id,
            "total": total,
            "current": 0,
            "percent": 0
        }

        await self.ws_manager.send_to_user(user_id, {
            "type": "progress_start",
            "task_id": task_id,
            "total": total
        })

    async def update_progress(self, task_id: str, current: int):
        """更新进度"""
        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]
        task["current"] = current
        task["percent"] = int((current / task["total"]) * 100)

        await self.ws_manager.send_to_user(task["user_id"], {
            "type": "progress_update",
            "task_id": task_id,
            "current": current,
            "total": task["total"],
            "percent": task["percent"]
        })

    async def finish(self, task_id: str):
        """完成追踪"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            await self.ws_manager.send_to_user(task["user_id"], {
                "type": "progress_complete",
                "task_id": task_id
            })
            del self.tasks[task_id]

progress_tracker = ProgressTracker(websocket_manager)

# 在 Worker 中使用
async def process_file_worker(message: dict):
    task_id = message["message_id"]
    user_id = message["payload"]["user_id"]
    file_path = message["payload"]["file_path"]

    total_lines = count_lines(file_path)
    await progress_tracker.start_tracking(task_id, user_id, total_lines)

    with open(file_path) as f:
        for i, line in enumerate(f):
            process_line(line)
            if i % 100 == 0:
                await progress_tracker.update_progress(task_id, i)

    await progress_tracker.finish(task_id)
```

---

## Part 7: 生产部署

### 7.1 Docker 配置

```dockerfile
# Dockerfile.worker
FROM python:3.13-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 启动 Worker
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info", "--concurrency=4"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0

  worker:
    build: .
    command: celery -A celery_app worker --loglevel=info --concurrency=4
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
    deploy:
      replicas: 2

  flower:
    build: .
    command: celery -A celery_app flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0

volumes:
  redis_data:
```

### 7.2 监控配置

```yaml
# celery_exporter 配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: celery-monitoring
data:
  celery_targets: |
    worker1:8001
    worker2:8001
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-exporter
spec:
  template:
    spec:
      containers:
        - name: exporter
          image: docker.io/marketplaceops/celery-exporter:latest
          env:
            - name: CELERY_BROKER_URL
              value: redis://redis:6379/0
            - name: CELERY_RESULT_BACKEND
              value: redis://redis:6379/0
            - name: CELERY_LAGENCY
              value: "5000"
          ports:
            - containerPort: 9808
```

### 7.3 告警规则

```yaml
# prometheus_alert_rules.yml
groups:
  - name: celery
    rules:
      - alert: CeleryWorkerDown
        expr: celery_workers_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Celery worker is down"

      - alert: CeleryQueueLength
        expr: celery_queue_length > 10000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Celery queue {{ $labels.queue }} has {{ $value }} messages"

      - alert: CeleryTaskFailure
        expr: rate(celery_tasks_failed_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High task failure rate"
```

---

## 📝 课程总结

### 核心知识点

1. **消息队列基础**：队列模型、Producer-Consumer
2. **Celery 任务队列**：任务定义、调度、监控
3. **消息可靠性**：确认、重试、死信队列、幂等性
4. **WebSocket 实时通信**：双向通信、心跳、聊天室
5. **混合架构**：消息队列 + WebSocket 组合

### 关键要点

- ✅ 消息队列用于解耦、削峰、异步处理
- ✅ Celery 是 Python 生态最流行的任务队列
- ✅ 幂等性设计确保消息可靠处理
- ✅ WebSocket 提供真正的双向实时通信
- ✅ 混合架构结合两者优势

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解消息队列的核心概念和优势
- [ ] 使用 Celery 定义和调度任务
- [ ] 实现消息确认、重试、死信队列
- [ ] 使用 FastAPI 实现 WebSocket 端点
- [ ] 实现聊天室和实时通知
- [ ] 设计消息队列与 WebSocket 的混合架构

---

**下一步**: 继续学习 [L41: API 性能优化](../L41-api-performance/lesson.md)
