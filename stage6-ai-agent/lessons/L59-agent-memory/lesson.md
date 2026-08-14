L59: Agent 记忆与上下文管理 - 详细教程

> **所属阶段**: Stage 6 - AI Agent 开发
> **课程编号**: L59
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L57 RAG 向量数据库, L58 LangGraph 工作流编排
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L57**: RAG 向量数据库（理解向量检索）
- **L58**: LangGraph 工作流编排（理解状态机）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 6 AI Agent 系统 - 长期对话上下文管理
> **前置课程**: L57 RAG 向量数据库, L58 LangGraph 进阶
> **后续课程**: L60 Agent 规划与推理, L61 多 Agent 系统  
> **学习时长**: 3-4 小时

---

---

## 📚 目录

- [第一章：记忆类型与选择](#第一章记忆类型与选择)
- [第二章：LangGraph 记忆集成](#第二章langgraph-记忆集成)
- [第三章：Token 管理策略](#第三章token-管理策略)
- [第四章：生产化实践](#第四章生产化实践)
- [第五章：生产级记忆系统](#第五章生产级记忆系统)
- [第六章：多模态记忆](#第六章多模态记忆)

---

## 第一章：记忆类型与选择

### 1.1 四种核心记忆

**Buffer Memory** (缓冲记忆)

- 保留完整对话历史
- 适合: 短对话 (< 10 轮)
- 问题: Token 无限增长

**Summary Memory** (摘要记忆)

- 滚动摘要旧对话
- 适合: 长对话
- 问题: 丢失细节

**Vector Memory** (向量记忆)

- 语义检索历史
- 适合: 长期记忆/知识库
- 问题: 检索延迟

**Entity Memory** (实体记忆)

- 提取并记住关键实体
- 适合: 多人对话/客户管理
- 问题: 实体提取准确性

---

### 1.2 Buffer Memory 实现

```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

# 创建 Buffer Memory
memory = ConversationBufferMemory()

# 绑定到 Chain
llm = ChatOpenAI(model="gpt-4o-mini")
chain = ConversationChain(llm=llm, memory=memory)

# 对话
chain.run("我叫小明")
chain.run("我刚才说我叫什么？")  # Agent 能记住
```python
---

### 1.3 Summary Memory 实现

```python
from langchain.memory import ConversationSummaryMemory

# 创建 Summary Memory
memory = ConversationSummaryMemory(llm=llm)

chain = ConversationChain(llm=llm, memory=memory)

# 对话
for i in range(20):
    chain.run(f"第 {i} 轮对话")

# 获取摘要
print(memory.load_memory_variables({}))
# {'history': '用户进行了20轮对话，主要内容是...'}
```python
---

### 1.4 Vector Memory 实现

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts([""], embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 创建 Vector Memory
memory = VectorStoreRetrieverMemory(retriever=retriever)

# 添加记忆
memory.save_context(
    {"input": "我最喜欢的颜色是蓝色"},
    {"output": "知道了"}
)

# 检索记忆
relevant = memory.load_memory_variables({"input": "我喜欢什么颜色"})
# 返回最相关的 3 条记忆
```python
---

## 第二章：LangGraph 记忆集成

### 2.1 内存 Checkpointer

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph

# 创建图
graph = StateGraph(State)
graph.add_node("agent", agent_node)
# ... 添加边

# 启用记忆
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# 对话 1
config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"messages": [("user", "我叫小明")]}, config)

# 对话 2 (自动恢复上下文)
app.invoke({"messages": [("user", "我叫什么？")]}, config)
# Agent 回答: "你叫小明"
```python
---

### 2.2 PostgreSQL Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver

# PostgreSQL 持久化
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/agent_db"
)

app = graph.compile(checkpointer=checkpointer)

# 跨会话/进程记忆
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": [("user", "你好")]}, config)
```python
---

### 2.3 Redis Checkpointer: 生产级分布式方案

**Redis Checkpointer** 是生产环境推荐方案，支持：
- ✅ 毫秒级状态读写（比 PostgreSQL 快 10x）
- ✅ 多实例共享会话状态（水平扩展）
- ✅ 内置过期时间（TTL）自动清理
- ✅ 支持 Redis Cluster（高可用）

```python
# 安装: uv add langgraph-checkpoint-redis

from langgraph.checkpoint.redis import RedisSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from operator import add
import redis

# 1. Redis 连接配置
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# 2. 创建 Redis Checkpointer
checkpointer = RedisSaver(
    client=redis_client,
    session_ttl=3600,  # 会话 TTL: 1小时
    index="agent_sessions"  # 索引名称
)

# 3. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add]
    context: dict

# 4. 构建图
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_edge(START, "agent")
graph.add_edge("agent", END)

# 5. 编译（带 Redis 持久化）
app = graph.compile(checkpointer=checkpointer)

# 6. 使用 - 分布式多实例共享会话
config = {
    "configurable": {
        "thread_id": "user-123",  # 用户会话 ID
        "checkpoint_ns": "production"  # 命名空间隔离
    }
}

# 实例 A: 处理用户请求
result = app.invoke(
    {"messages": [("user", "你好，我是小明")]},
    config
)

# 实例 B: 同一用户的后续请求（自动恢复上下文）
result = app.invoke(
    {"messages": [("user", "我刚才说我叫什么？")]},
    config
)
# Agent 回答: "你叫小明" - 跨实例共享记忆
```

### 2.4 Redis Checkpointer 生产配置

```python
from langgraph.checkpoint.redis import RedisSaver
import redis.asyncio as aioredis
import os

# 生产环境配置
class ProductionCheckpointer:
    """生产级 Checkpointer 配置"""

    @staticmethod
    def create_redis_checkpointer(
        redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379"),
        session_ttl: int = 3600,
        pool_size: int = 20
    ) -> RedisSaver:
        """
        创建生产级 Redis Checkpointer

        Args:
            redis_url: Redis 连接 URL
            session_ttl: 会话过期时间（秒）
            pool_size: 连接池大小

        Returns:
            RedisSaver 实例
        """
        # 异步 Redis 客户端（推荐生产使用）
        async_redis = aioredis.from_url(
            redis_url,
            max_connections=pool_size,
            decode_responses=True
        )

        return RedisSaver(
            client=async_redis,
            session_ttl=session_ttl,
            index="production_agent_sessions"
        )

    @staticmethod
    def create_ha_redis_checkpointer() -> RedisSaver:
        """
        创建高可用 Redis Checkpointer（Sentinel/Cluster）

        适用于: 多可用区部署、金融级可靠性
        """
        # Redis Sentinel 配置
        sentinel = aioredis.sentinel.Sentinel(
            [
                ("redis-primary.example.com", 26379),
                ("redis-replica-1.example.com", 26379),
                ("redis-replica-2.example.com", 26379),
            ],
            sentinel_kwargs={"password": os.getenv("REDIS_PASSWORD")},
            connection_pool_class=aioredis.sentinel.SentinelConnectionPool,
            connection_pool_kwargs={"password": os.getenv("REDIS_PASSWORD")}
        )

        # 自动故障转移
        master = sentinel.master_for(
            "mymaster",
            reader_class=aioredis.asyncio.ConnectionPool
        )

        return RedisSaver(
            client=master,
            session_ttl=7200,  # 2小时 TTL
            index="ha_agent_sessions"
        )

# Docker Compose 示例
"""
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s

  agent:
    build: .
    depends_on:
      redis:
        condition: service_healthy
    environment:
      - REDIS_URL=redis://redis:6379
      - SESSION_TTL=3600
"""
```

### 2.5 Checkpointer 对比与选型

| Checkpointer | 适用场景 | 延迟 | 扩展性 | 成本 |
|--------------|----------|------|--------|------|
| MemorySaver | 开发/测试 | < 1ms | 单实例 | 免费 |
| PostgresSaver | 中小型生产 | 5-20ms | 垂直扩展 | 中等 |
| **RedisSaver** | **大型生产** | **1-5ms** | **水平扩展** | **中等** |
| AsyncPostgresSaver | 高并发 | 5-15ms | 垂直扩展 | 中等 |

**推荐**:
- 开发测试: `MemorySaver`
- 小型生产: `PostgresSaver`
- **大型生产（推荐）: `RedisSaver`**
- 高可用: `Redis Sentinel / Cluster`

---

### 2.6 记忆状态结构

```python
from typing import TypedDict, Annotated
from operator import add

class ChatState(TypedDict):
    messages: Annotated[list, add]
    summary: str  # 对话摘要
    user_info: dict  # 用户信息

def agent_node(state: ChatState):
    # 读取历史
    history = state["messages"]
    summary = state["summary"]

    # 生成回复
    response = llm.invoke(history)

    return {
        "messages": [response],
        "summary": "更新摘要..."
    }
```python
---

## 第三章：Token 管理策略

### 3.1 滑动窗口 (最简单)

```python
from typing import TypedDict, Annotated

def add_messages(left: list, right: list, max_messages: int = 20):
    """滑动窗口：保留最近 N 条消息"""
    combined = left + right
    return combined[-max_messages:]

class State(TypedDict):
    messages: Annotated[list, lambda l, r: add_messages(l, r, 20)]

# 自动保留最近 20 条消息
```python
---

### 3.2 Token 计数器

```python
import tiktoken

def count_tokens(messages: list) -> int:
    """计算消息 Token 数"""
    encoding = tiktoken.get_encoding("cl100k_base")
    total = 0
    for msg in messages:
        total += len(encoding.encode(msg.content))
    return total

def trim_messages(messages: list, max_tokens: int = 4000) -> list:
    """保持 Token 数 < max_tokens"""
    while count_tokens(messages) > max_tokens and len(messages) > 1:
        messages.pop(0)  # 删除最早的消息
    return messages
```python
---

### 3.3 自动摘要

```python
from langchain_openai import ChatOpenAI

def summarize_conversation(messages: list) -> str:
    """将旧消息摘要为一条"""
    llm = ChatOpenAI(model="gpt-4o-mini")

    text = "\n".join([f"{m.type}: {m.content}" for m in messages])
    prompt = f"总结以下对话（200字内）:\n\n{text}"

    summary = llm.invoke(prompt).content
    return summary

def agent_node(state: State):
    messages = state["messages"]

    # Token 检查
    if count_tokens(messages) > 8000:
        # 摘要前 N 条消息
        old_messages = messages[:10]
        summary_text = summarize_conversation(old_messages)

        # 替换为摘要
        messages = [
            {"role": "system", "content": f"对话摘要: {summary_text}"}
        ] + messages[10:]

    # 继续处理
    response = llm.invoke(messages)
    return {"messages": [response]}
```python
---

## 第四章：生产化实践

### 4.1 Redis 会话存储

```python
import redis
import json

class RedisMemory:
    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url)

    def save(self, thread_id: str, messages: list):
        """保存会话"""
        key = f"chat:{thread_id}"
        self.client.setex(
            key,
            3600,  # 1 小时过期
            json.dumps([m.dict() for m in messages])
        )

    def load(self, thread_id: str) -> list:
        """加载会话"""
        key = f"chat:{thread_id}"
        data = self.client.get(key)
        if not data:
            return []
        return json.loads(data)
```python
---

### 4.2 MongoDB 长期记忆

```python
from pymongo import MongoClient
from datetime import datetime

class MongoMemory:
    def __init__(self, mongo_url: str):
        self.client = MongoClient(mongo_url)
        self.db = self.client["agent_db"]
        self.collection = self.db["conversations"]

    def save_message(self, user_id: str, message: dict):
        """保存单条消息"""
        doc = {
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now()
        }
        self.collection.insert_one(doc)

    def get_recent(self, user_id: str, limit: int = 20) -> list:
        """获取最近消息"""
        cursor = self.collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)

        return list(cursor)
```python
---

### 4.3 向量记忆检索

```python
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

class VectorMemoryStore:
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")
        self.embeddings = OpenAIEmbeddings()
        self.collection = "agent_memory"

    def add_memory(self, user_id: str, content: str):
        """添加记忆"""
        vector = self.embeddings.embed_query(content)

        self.client.upsert(
            collection_name=self.collection,
            points=[{
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {
                    "user_id": user_id,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }
            }]
        )

    def search_memory(self, user_id: str, query: str, top_k: int = 5) -> list:
        """检索相关记忆"""
        query_vector = self.embeddings.embed_query(query)

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter={
                "must": [{"key": "user_id", "match": {"value": user_id}}]
            },
            limit=top_k
        )

        return [r.payload["content"] for r in results]
```text
---

## 第五章：生产级记忆系统

### 5.1 多级记忆架构

```python
class HierarchicalMemory:
    """层级记忆系统"""

    def __init__(self):
        # L1: 短期记忆（最近 N 条消息）
        self.short_term = ConversationBufferWindowMemory(k=10)

        # L2: 中期记忆（摘要 + 重要片段）
        self.mid_term = ConversationSummaryMemory(llm=llm)

        # L3: 长期记忆（向量存储）
        self.long_term = VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(k=5)
        )

    async def add_interaction(self, user_input: str, response: str):
        """添加交互"""
        # L1: 直接添加
        self.short_term.save_context(
            {"input": user_input},
            {"output": response}
        )

        # L2: 定期摘要
        if should_summarize():
            summary = await self.mid_term.llm.apredict(
                self.mid_term.buffer
            )
            self.mid_term.save_context(
                {"input": "对话摘要"},
                {"output": summary}
            )

        # L3: 提取并存储重要信息
        if is_important(user_input):
            self.long_term.save_context(
                {"input": user_input},
                {"output": response}
            )

    async def retrieve(self, query: str) -> list[str]:
        """检索记忆"""
        results = []

        # 短期
        short = self.short_term.load_memory_variables({})
        if query in str(short):
            results.append(("短期", short))

        # 中期
        mid = self.mid_term.load_memory_variables({})
        if query in str(mid):
            results.append(("中期", mid))

        # 长期
        long = self.long_term.load_memory_variables({"input": query})
        results.append(("长期", long))

        return results
```

### 5.2 记忆过期策略

```python
from datetime import datetime, timedelta

class ExpirableMemory:
    """带过期时间的记忆"""

    def __init__(self, ttl: timedelta = timedelta(days=7)):
        self.memory = {}
        self.ttl = ttl

    def save(self, key: str, value: any):
        """保存记忆"""
        self.memory[key] = {
            "value": value,
            "created_at": datetime.now()
        }

    def get(self, key: str) -> any | None:
        """获取记忆"""
        if key not in self.memory:
            return None

        entry = self.memory[key]
        age = datetime.now() - entry["created_at"]

        if age > self.ttl:
            del self.memory[key]
            return None

        return entry["value"]

    def cleanup_expired(self):
        """清理过期记忆"""
        now = datetime.now()
        expired = [
            k for k, v in self.memory.items()
            if now - v["created_at"] > self.ttl
        ]
        for k in expired:
            del self.memory[k]
```

### 5.3 记忆重要性评分

```python
import re

class ImportantMemoryExtractor:
    """重要性提取器"""

    def __init__(self, llm):
        self.llm = llm

    async def extract_importance(self, text: str) -> float:
        """提取重要性分数 (0-1)"""
        # 关键词匹配
        keywords = ["重要", "必须", "紧急", "记住", "别忘"]
        keyword_score = sum(1 for k in keywords if k in text) / len(keywords)

        # 实体提取
        entities = self._extract_entities(text)
        entity_score = min(len(entities) * 0.2, 0.5)

        # LLM 判断
        llm_score = await self._llm_judge_importance(text)

        return min(keyword_score + entity_score + llm_score * 0.3, 1.0)

    def _extract_entities(self, text: str) -> list[str]:
        """提取实体"""
        patterns = [
            r'\d{3,}',  # 数字
            r'[A-Z][a-z]+',  # 英文名
            r'[一-龥]{2,}',  # 中文
        ]
        entities = []
        for pattern in patterns:
            entities.extend(re.findall(pattern, text))
        return entities

    async def _llm_judge_importance(self, text: str) -> float:
        """LLM 判断重要性"""
        prompt = f"评分 (0-1): {text[:100]}"
        response = await self.llm.apredict(prompt)
        try:
            return float(response.strip())
        except:
            return 0.5
```

### 5.4 记忆压缩与总结

```python
class CompressedMemory:
    """压缩记忆"""

    def __init__(self, llm, max_tokens: int = 2000):
        self.llm = llm
        self.max_tokens = max_tokens
        self.summaries = []

    async def compress_if_needed(self, messages: list) -> list:
        """必要时压缩"""
        current_tokens = self._count_tokens(messages)

        if current_tokens <= self.max_tokens:
            return messages

        # 生成摘要
        summary = await self._generate_summary(messages)
        self.summaries.append(summary)

        # 保留最近的消息 + 摘要
        recent = messages[-10:]
        return [
            {"role": "system", "content": f"摘要: {summary}"}
        ] + recent

    async def _generate_summary(self, messages: list) -> str:
        """生成摘要"""
        prompt = f"总结以下对话的要点:\n{messages}"
        return await self.llm.apredict(prompt)

    def _count_tokens(self, messages: list) -> int:
        """计算 Token 数"""
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-4")
        text = " ".join([m.get("content", "") for m in messages])
        return len(enc.encode(text))
```

---

## 第六章：多模态记忆

### 6.1 图像记忆

```python
from PIL import Image
import base64
from io import BytesIO

class ImageMemory:
    """图像记忆"""

    def __init__(self, llm):
        self.llm = llm
        self.images = []

    async def add_image(self, image: Image.Image, caption: str):
        """添加图像记忆"""
        # 转换为 base64
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode()

        # 提取图像描述
        description = await self._describe_image(image)

        self.images.append({
            "base64": b64,
            "caption": caption,
            "description": description
        })

    async def _describe_image(self, image: Image.Image) -> str:
        """描述图像"""
        # 使用 GPT-4V 或其他多模态模型
        prompt = "描述这张图片的关键内容"
        response = await self.llm.vision.analyze(image, prompt)
        return response

    async def search_images(self, query: str) -> list:
        """搜索图像"""
        results = []
        for img in self.images:
            # 语义匹配
            if query.lower() in img["description"].lower():
                results.append(img)
        return results
```

### 6.2 音频记忆

```python
import base64
import speech_recognition as sr

class AudioMemory:
    """音频记忆"""

    def __init__(self, llm):
        self.llm = llm
        self.audio_records = []
        self.recognizer = sr.Recognizer()

    async def add_audio(self, audio_bytes: bytes):
        """添加音频记忆"""
        # 语音转文字
        text = await self._transcribe(audio_bytes)

        # 提取关键信息
        summary = await self._summarize(text)

        self.audio_records.append({
            "audio": base64.b64encode(audio_bytes).decode(),
            "transcript": text,
            "summary": summary
        })

    async def _transcribe(self, audio_bytes: bytes) -> str:
        """语音转文字"""
        with sr.AudioFile(BytesIO(audio_bytes)) as source:
            audio = self.recognizer.record(source)
        return self.recognizer.recognize_google(audio, language="zh-CN")

    async def _summarize(self, text: str) -> str:
        """总结音频内容"""
        return await self.llm.apredict(f"总结: {text}")
```

### 6.3 文件记忆

```python
class FileMemory:
    """文件记忆"""

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    async def add_file(self, filepath: str, content: str):
        """添加文件记忆"""
        # 分割为块
        chunks = self._chunk_content(content)

        # 向量化存储
        self.vectorstore.add_texts(
            texts=chunks,
            metadatas=[{"source": filepath}] * len(chunks)
        )

    def _chunk_content(self, content: str, chunk_size: int = 1000) -> list[str]:
        """分割内容"""
        words = content.split()
        chunks = []
        current = []

        for word in words:
            current.append(word)
            if len(" ".join(current)) > chunk_size:
                chunks.append(" ".join(current))
                current = []

        if current:
            chunks.append(" ".join(current))

        return chunks

    async def search_files(self, query: str) -> list[dict]:
        """搜索文件"""
        docs = self.vectorstore.similarity_search(query, k=5)
        return [
            {"content": doc.page_content, "source": doc.metadata.get("source")}
            for doc in docs
        ]
```

---

## 🎯 最佳实践总结

### ✅ 记忆设计清单

- [ ] 根据对话长度选择记忆类型
- [ ] 设置合理的 Token 上限
- [ ] 实现自动摘要机制
- [ ] 使用 Checkpointer 持久化
- [ ] 关键信息向量化存储
- [ ] 设置会话过期时间
- [ ] 实现记忆检索缓存

### 记忆选择决策树

```text
对话长度 < 10 轮?
  ├─ 是 → Buffer Memory
  └─ 否 → 对话持续 < 1 小时?
      ├─ 是 → Summary Memory + 滑动窗口
      └─ 否 → Vector Memory + 实体提取
```

---

## 🔗 延伸阅读

### 相关课程

- **L56 Agent 基础 LangChain 基础** - Chain 组合
- **L58 LangGraph 进阶** - 状态持久化
- **L57 RAG 向量数据库** - 向量检索

### 推荐资源

- [LangChain Memory 文档](https://python.langchain.com/docs/modules/memory/)
- [LangGraph Checkpointer](https://langchain-ai.github.io/langgraph/how-tos/persistence/)
- [tiktoken Token 计数](https://github.com/openai/tiktoken)

---

## 📝 练习题

### 练习 1: 滑动窗口记忆

实现保留最近 N 条消息:

- Token 计数
- 自动删除旧消息
- 保留系统消息

### 练习 2: 自动摘要

实现 Token 超限自动摘要:

- 检测 Token 数
- 触发摘要生成
- 替换旧消息

### 练习 3: 向量记忆检索

实现语义检索记忆:

- 向量化存储
- 相似度搜索
- 时间衰减权重

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L60 Agent 任务规划](../L60-agent-planning/lesson.md)

## 🔗 下一步


[L60: Agent 规划与推理](../L60-agent-planning/)
