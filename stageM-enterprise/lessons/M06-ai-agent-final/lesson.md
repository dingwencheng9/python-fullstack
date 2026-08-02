# M06: AI Agent 最终项目

> **课程编号**: M06
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 8-10 小时
> **难度**: ⭐⭐⭐⭐⭐ (高级)
> **前置课程**: L54-L65 (Stage 6 全部内容)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **综合应用**：将所学知识整合为完整的 AI Agent 系统
2. **架构设计**：设计生产级 AI 应用架构
3. **性能优化**：优化系统性能和成本
4. **部署运维**：将系统部署到生产环境

---

## 📚 课程内容

### 第一部分：项目概述

#### 1.1 项目背景

**智能企业知识助手 (Enterprise Knowledge Assistant)**

```
用户痛点：
- 企业知识分散在多个系统中（Wiki、邮件、文档、会议记录）
- 员工难以快速找到所需信息
- 知识重复创建，浪费资源
- 跨部门协作困难

解决方案：
构建一个智能助手，能够：
- 统一接入企业知识源
- 理解自然语言查询
- 提供准确、相关的答案
- 支持多轮对话和追问
```

#### 1.2 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Enterprise Knowledge Assistant                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐               │
│  │  Web UI  │     │  Slack   │     │  Teams   │   ← 接入层   │
│  │ (React)  │     │  Bot     │     │  Bot     │               │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘               │
│       │                │                │                        │
│       └────────────────┼────────────────┘                        │
│                        ↓                                         │
│               ┌──────────────────┐                               │
│               │   API Gateway   │   ← 路由、鉴权、限流          │
│               │   (Litestar)    │                               │
│               └────────┬─────────┘                               │
│                        ↓                                         │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              Agent Orchestration Layer               │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │        │
│  │  │ Intent   │  │  Memory  │  │  Tools   │         │        │
│  │  │Classifier│  │  Manager │  │ Registry │         │        │
│  │  └──────────┘  └──────────┘  └──────────┘         │        │
│  └─────────────────────────────────────────────────────┘        │
│                        ↓                                         │
│  ┌─────────────────────────────────────────────────────┐        │
│  │                  RAG Pipeline                        │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │        │
│  │  │ Query    │  │ Hybrid   │  │  LLM     │         │        │
│  │  │Transform │  │ Retrieval│  │ Generate │         │        │
│  │  └──────────┘  └──────────┘  └──────────┘         │        │
│  └─────────────────────────────────────────────────────┘        │
│                        ↓                                         │
│  ┌─────────────────────────────────────────────────────┐        │
│  │               Data & Storage Layer                   │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │        │
│  │  │ Qdrant   │  │  Redis   │  │PostgreSQL│         │        │
│  │  │ (向量)   │  │ (缓存)   │  │ (结构化) │         │        │
│  │  └──────────┘  └──────────┘  └──────────┘         │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1.3 技术栈

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| **前端** | React + Vite | Web 界面 |
| **API** | Litestar | 高性能 Python API |
| **Agent** | LangChain/LangGraph | Agent 编排 |
| **LLM** | GPT-4 / Claude | 主模型 |
| **Embedding** | BGE | 向量化 |
| **向量数据库** | Qdrant | 语义检索 |
| **缓存** | Redis | 热点缓存 |
| **数据库** | PostgreSQL | 结构化存储 |
| **文档处理** | Unstructured.io | PDF/Word 解析 |

---

### 第二部分：核心实现

#### 2.1 Agent 编排器

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Protocol
from datetime import datetime
import asyncio

class Intent(Enum):
    """用户意图"""
    QUERY_KNOWLEDGE = "query_knowledge"
    SEARCH_DOCUMENTS = "search_documents"
    SUMMARIZE = "summarize"
    COMPARE = "compare"
    RECOMMEND = "recommend"
    UNKNOWN = "unknown"

@dataclass
class Message:
    """对话消息"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResponse:
    """Agent 响应"""
    content: str
    intent: Intent
    sources: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float
    follow_up_suggestions: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)

class IntentClassifier:
    """意图分类器"""

    def __init__(self, llm):
        self.llm = llm

    async def classify(self, query: str) -> tuple[Intent, float]:
        """分类用户意图"""
        prompt = f"""Classify the user query into one of these intents:
        - query_knowledge: Ask about company policies, procedures, or knowledge
        - search_documents: Find specific documents or files
        - summarize: Summarize a document or topic
        - compare: Compare two or more items
        - recommend: Get recommendations or suggestions
        - unknown: Cannot be classified

        Query: {query}

        Respond with JSON: {{"intent": "...", "confidence": 0.0}}
        """

        response = await self.llm.acomplete(prompt)
        # 解析响应
        import json
        result = json.loads(str(response))

        intent_map = {
            "query_knowledge": Intent.QUERY_KNOWLEDGE,
            "search_documents": Intent.SEARCH_DOCUMENTS,
            "summarize": Intent.SUMMARIZE,
            "compare": Intent.COMPARE,
            "recommend": Intent.RECOMMEND,
        }

        return (
            intent_map.get(result["intent"], Intent.UNKNOWN),
            result["confidence"]
        )

class MemoryManager:
    """记忆管理器"""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_history = 10

    async def add_message(self, session_id: str, message: Message) -> None:
        """添加消息到记忆"""
        key = f"session:{session_id}:history"
        import json
        await self.redis.rpush(
            key,
            json.dumps({
                "role": message.role,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            })
        )
        # 限制历史长度
        await self.redis.ltrim(key, -self.max_history * 2, -1)

    async def get_history(self, session_id: str) -> List[Message]:
        """获取对话历史"""
        key = f"session:{session_id}:history"
        history_data = await self.redis.lrange(key, 0, -1)

        import json
        messages = []
        for data in history_data:
            msg_dict = json.loads(data)
            messages.append(Message(
                role=msg_dict["role"],
                content=msg_dict["content"],
                timestamp=datetime.fromisoformat(msg_dict["timestamp"])
            ))
        return messages

    async def get_context_window(self, session_id: str, max_turns: int = 5) -> str:
        """获取上下文窗口"""
        history = await self.get_history(session_id)
        # 只取最近 max_turns 轮对话
        relevant = history[-max_turns * 2:]
        return "\n".join([
            f"{msg.role}: {msg.content}"
            for msg in relevant
        ])

class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable, description: str) -> None:
        """注册工具"""
        self.tools[name] = func
        setattr(self, name, func)  # 方便直接调用

    def get_tool(self, name: str) -> Optional[Callable]:
        """获取工具"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        """列出所有工具"""
        return [
            {"name": name, "description": tool.__doc__ or ""}
            for name, tool in self.tools.items()
        ]

class KnowledgeAgent:
    """企业知识助手"""

    def __init__(
        self,
        llm,
        embedder,
        vector_store,
        intent_classifier: IntentClassifier,
        memory: MemoryManager,
        tool_registry: ToolRegistry
    ):
        self.llm = llm
        self.embedder = embedder
        self.vector_store = vector_store
        self.intent_classifier = intent_classifier
        self.memory = memory
        self.tools = tool_registry

    async def process(
        self,
        session_id: str,
        user_query: str
    ) -> AgentResponse:
        """处理用户查询"""
        start_time = datetime.now()

        # 1. 意图分类
        intent, confidence = await self.intent_classifier.classify(user_query)

        # 2. 获取对话历史
        history_context = await self.memory.get_context_window(session_id)

        # 3. 根据意图处理
        if intent == Intent.QUERY_KNOWLEDGE:
            response = await self._handle_knowledge_query(
                user_query, history_context
            )
        elif intent == Intent.SEARCH_DOCUMENTS:
            response = await self._handle_document_search(user_query)
        elif intent == Intent.SUMMARIZE:
            response = await self._handle_summarize(user_query)
        elif intent == Intent.COMPARE:
            response = await self._handle_compare(user_query)
        else:
            response = await self._handle_general(user_query, history_context)

        # 4. 添加记忆
        await self.memory.add_message(
            session_id,
            Message(role="user", content=user_query)
        )
        await self.memory.add_message(
            session_id,
            Message(role="assistant", content=response.content)
        )

        # 5. 计算指标
        duration = (datetime.now() - start_time).total_seconds()
        response.metrics["latency_seconds"] = duration
        response.metrics["intent_confidence"] = confidence
        response.intent = intent

        # 6. 生成跟进建议
        response.follow_up_suggestions = self._generate_follow_ups(
            response.content, intent
        )

        return response

    async def _handle_knowledge_query(
        self,
        query: str,
        history_context: str
    ) -> AgentResponse:
        """处理知识查询"""
        # 1. HyDE 查询变换
        hypothetical = await self._hyde_transform(query)

        # 2. 向量检索
        query_vector = self.embedder.encode([hypothetical])[0]
        search_results = self.vector_store.search(
            collection_name="enterprise_knowledge",
            query_vector=query_vector,
            limit=5
        )

        # 3. 构建上下文
        context = self._build_context(search_results)

        # 4. 生成答案
        prompt = f"""Based on the following context, answer the user query.
        If the context doesn't contain enough information, say so.

        History:
        {history_context}

        Context:
        {context}

        Query: {query}

        Answer:"""

        answer = await self.llm.acomplete(prompt)

        return AgentResponse(
            content=str(answer),
            intent=Intent.QUERY_KNOWLEDGE,
            sources=[
                {"id": r["id"], "title": r["payload"].get("title", ""), "score": r["score"]}
                for r in search_results
            ],
            confidence=0.85
        )

    async def _hyde_transform(self, query: str) -> str:
        """HyDE 查询变换"""
        prompt = f"Generate a hypothetical passage that directly answers: {query}"
        return str(await self.llm.acomplete(prompt))

    def _build_context(self, search_results: List[dict]) -> str:
        """构建检索上下文"""
        context_parts = []
        for i, result in enumerate(search_results):
            doc = result["payload"]
            context_parts.append(
                f"[Document {i+1}] {doc.get('title', 'Untitled')}\n"
                f"{doc.get('content', '')}"
            )
        return "\n\n".join(context_parts)

    def _generate_follow_ups(
        self,
        content: str,
        intent: Intent
    ) -> List[str]:
        """生成跟进建议"""
        suggestions = [
            "你可以让我帮你搜索相关文档",
            "需要我总结一下主要内容吗？",
            "想了解更多细节吗？"
        ]
        return suggestions[:2]
```

#### 2.2 RAG 管道

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import asyncio

@dataclass
class DocumentChunk:
    """文档块"""
    id: str
    content: str
    metadata: dict
    embedding: Optional[List[float]] = None

class HybridRetriever:
    """混合检索器"""

    def __init__(
        self,
        vector_store,
        bm25_index,
        reranker,
        alpha: float = 0.7
    ):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.reranker = reranker
        self.alpha = alpha

    async def retrieve(
        self,
        query: str,
        query_vector: List[float],
        top_k: int = 20,
        filters: Optional[dict] = None
    ) -> List[dict]:
        """执行混合检索"""
        # 1. 并行向量和 BM25 检索
        vector_task = self._vector_search(query_vector, top_k * 2, filters)
        bm25_task = self._bm25_search(query, top_k * 2)

        vector_results, bm25_results = await asyncio.gather(
            vector_task, bm25_task
        )

        # 2. RRF 融合
        fused_results = self._reciprocal_rank_fusion(vector_results, bm25_results)

        # 3. 重排序
        if fused_results:
            reranked = await self.reranker.rerank(
                query=query,
                documents=fused_results[:10],
                top_n=top_k
            )
            return reranked

        return fused_results[:top_k]

    async def _vector_search(
        self,
        query_vector: List[float],
        top_k: int,
        filters: Optional[dict]
    ) -> List[dict]:
        """向量搜索"""
        return self.vector_store.search(
            query_vector=query_vector,
            limit=top_k,
            query_filter=filters
        )

    async def _bm25_search(
        self,
        query: str,
        top_k: int
    ) -> List[dict]:
        """BM25 搜索"""
        # 实现 BM25 搜索
        pass

    def _reciprocal_rank_fusion(
        self,
        results_a: List[dict],
        results_b: List[dict],
        k: int = 60
    ) -> List[dict]:
        """RRF 融合"""
        fused = {}

        # 添加向量结果
        for rank, result in enumerate(results_a):
            doc_id = result.get("id") or result.get("_id")
            fused[doc_id] = {
                "score": fused.get(doc_id, {}).get("score", 0) + self.alpha / (k + rank + 1),
                "doc": result
            }

        # 添加 BM25 结果
        for rank, result in enumerate(results_b):
            doc_id = result.get("id") or result.get("_id")
            if doc_id in fused:
                fused[doc_id]["score"] += (1 - self.alpha) / (k + rank + 1)
            else:
                fused[doc_id] = {
                    "score": (1 - self.alpha) / (k + rank + 1),
                    "doc": result
                }

        # 排序
        sorted_results = sorted(
            fused.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )

        return [item[1]["doc"] for item in sorted_results]

class RAGPipeline:
    """RAG 管道"""

    def __init__(
        self,
        llm,
        retriever: HybridRetriever,
        embedder
    ):
        self.llm = llm
        self.retriever = retriever
        self.embedder = embedder

    async def query(
        self,
        question: str,
        session_id: Optional[str] = None,
        filters: Optional[dict] = None
    ) -> dict:
        """执行 RAG 查询"""
        # 1. 查询向量化
        query_vector = self.embedder.encode([question])[0]

        # 2. 混合检索
        retrieved_docs = await self.retriever.retrieve(
            query=question,
            query_vector=query_vector,
            top_k=10,
            filters=filters
        )

        # 3. 构建上下文
        context = self._build_context(retrieved_docs)

        # 4. 生成答案
        answer = await self._generate(question, context)

        return {
            "answer": answer,
            "sources": [
                {
                    "id": doc.get("id"),
                    "title": doc.get("metadata", {}).get("title", ""),
                    "snippet": doc.get("content", "")[:200],
                    "score": doc.get("rerank_score", doc.get("score", 0))
                }
                for doc in retrieved_docs
            ]
        }

    def _build_context(self, documents: List[dict]) -> str:
        """构建上下文"""
        parts = []
        for i, doc in enumerate(documents):
            parts.append(
                f"[{i+1}] {doc.get('metadata', {}).get('title', 'Untitled')}\n"
                f"{doc.get('content', '')}"
            )
        return "\n\n".join(parts)

    async def _generate(self, question: str, context: str) -> str:
        """生成答案"""
        prompt = f"""You are a helpful assistant. Answer the question based on the provided context.
        If the context doesn't contain enough information to answer the question, say so.

        Context:
        {context}

        Question: {question}

        Answer:"""

        return str(await self.llm.acomplete(prompt))
```

---

### 第三部分：数据处理

#### 3.1 文档解析

```python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from datetime import datetime

@dataclass
class ParsedDocument:
    """解析后的文档"""
    title: str
    content: str
    metadata: dict
    chunks: List["DocumentChunk"] = None

class DocumentParser:
    """文档解析器"""

    def __init__(self):
        self.supported_formats = [".pdf", ".docx", ".pptx", ".txt", ".md"]

    async def parse(self, file_path: Path) -> ParsedDocument:
        """解析文档"""
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return await self._parse_pdf(file_path)
        elif suffix == ".docx":
            return await self._parse_docx(file_path)
        elif suffix == ".pptx":
            return await self._parse_pptx(file_path)
        elif suffix == ".txt":
            return self._parse_txt(file_path)
        elif suffix == ".md":
            return self._parse_markdown(file_path)
        else:
            raise ValueError(f"Unsupported format: {suffix}")

    async def _parse_pdf(self, file_path: Path) -> ParsedDocument:
        """解析 PDF"""
        from unstructured.partition.pdf import partition_pdf

        elements = partition_pdf(filename=str(file_path))

        # 提取文本
        content = "\n\n".join([
            str(el.text) for el in elements if el.text
        ])

        # 提取元数据
        metadata = {
            "source": str(file_path),
            "type": "pdf",
            "num_pages": len(elements),
            "parsed_at": datetime.now().isoformat()
        }

        return ParsedDocument(
            title=file_path.stem,
            content=content,
            metadata=metadata
        )

    async def _parse_docx(self, file_path: Path) -> ParsedDocument:
        """解析 Word 文档"""
        from unstructured.partition.docx import partition_docx

        elements = partition_docx(filename=str(file_path))

        content = "\n\n".join([
            str(el.text) for el in elements if el.text
        ])

        return ParsedDocument(
            title=file_path.stem,
            content=content,
            metadata={
                "source": str(file_path),
                "type": "docx",
                "parsed_at": datetime.now().isoformat()
            }
        )

    def _parse_txt(self, file_path: Path) -> ParsedDocument:
        """解析文本文件"""
        content = file_path.read_text(encoding="utf-8")

        return ParsedDocument(
            title=file_path.stem,
            content=content,
            metadata={
                "source": str(file_path),
                "type": "txt",
                "parsed_at": datetime.now().isoformat()
            }
        )

class TextChunker:
    """文本分块器"""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        document: ParsedDocument,
        metadata_extra: Optional[dict] = None
    ) -> List[DocumentChunk]:
        """分块"""
        content = document.content
        chunks = []

        # 简单的滑动窗口分块
        start = 0
        chunk_id = 0

        while start < len(content):
            end = start + self.chunk_size
            chunk_text = content[start:end]

            # 尝试在句子边界分割
            if end < len(content):
                last_period = chunk_text.rfind("。")
                last_newline = chunk_text.rfind("\n")
                split_pos = max(last_period, last_newline)

                if split_pos > self.chunk_size // 2:
                    chunk_text = chunk_text[:split_pos + 1]
                    end = start + split_pos + 1

            metadata = {
                **document.metadata,
                "chunk_index": chunk_id,
                "total_chunks": None,  # 稍后填充
                **(metadata_extra or {})
            }

            chunks.append(DocumentChunk(
                id=f"{document.metadata.get('source', 'unknown')}_{chunk_id}",
                content=chunk_text.strip(),
                metadata=metadata
            ))

            chunk_id += 1
            start = end - self.chunk_overlap

        # 填充总块数
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)

        return chunks
```

#### 3.2 索引管道

```python
class IndexingPipeline:
    """索引管道"""

    def __init__(
        self,
        parser: DocumentParser,
        chunker: TextChunker,
        embedder,
        vector_store
    ):
        self.parser = parser
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    async def index_document(
        self,
        file_path: Path,
        collection_name: str = "enterprise_knowledge"
    ) -> dict:
        """索引文档"""
        # 1. 解析
        document = await self.parser.parse(file_path)
        print(f"Parsed: {document.title}")

        # 2. 分块
        chunks = self.chunker.chunk(document)
        print(f"Chunked into {len(chunks)} pieces")

        # 3. 向量化
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.encode(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding.tolist()

        # 4. 存储
        vectors = [chunk.embedding for chunk in chunks]
        payloads = [
            {
                "content": chunk.content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]

        self.vector_store.upsert_points(
            collection_name=collection_name,
            vectors=vectors,
            payloads=payloads,
            ids=list(range(len(chunks)))
        )

        return {
            "document": document.title,
            "num_chunks": len(chunks),
            "status": "indexed"
        }

    async def index_batch(
        self,
        file_paths: List[Path],
        collection_name: str = "enterprise_knowledge"
    ) -> List[dict]:
        """批量索引"""
        results = []

        for file_path in file_paths:
            try:
                result = await self.index_document(file_path, collection_name)
                results.append(result)
            except Exception as e:
                results.append({
                    "document": file_path.name,
                    "status": "failed",
                    "error": str(e)
                })

        return results
```

---

### 第四部分：API 层

#### 4.1 Litestar API

```python
from litestar import Litestar, get, post, Request, Controller
from litestar.dto import DTO
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ===== DTO =====
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    content: str
    intent: str
    sources: List[dict]
    confidence: float
    follow_ups: List[str]
    metrics: dict

class IndexRequest(BaseModel):
    file_url: str  # S3 或本地路径
    collection: str = "enterprise_knowledge"

# ===== 控制器 =====
class AgentController(Controller):
    path = "/api/v1"

    @post("/chat")
    async def chat(
        self,
        request: Request,
        data: ChatRequest
    ) -> ChatResponse:
        """对话接口"""
        agent: KnowledgeAgent = request.state.agent

        response = await agent.process(
            session_id=data.session_id or "default",
            user_query=data.query
        )

        return ChatResponse(
            content=response.content,
            intent=response.intent.value,
            sources=[
                {"id": s.get("id"), "title": s.get("title"), "score": s.get("score")}
                for s in response.sources
            ],
            confidence=response.confidence,
            follow_ups=response.follow_up_suggestions,
            metrics=response.metrics
        )

    @post("/index")
    async def index_document(
        self,
        request: Request,
        data: IndexRequest
    ) -> dict:
        """文档索引接口"""
        pipeline: IndexingPipeline = request.state.indexing_pipeline

        result = await pipeline.index_document(
            file_path=data.file_url,
            collection_name=data.collection
        )

        return result

    @get("/history/{session_id}")
    async def get_history(
        self,
        request: Request,
        session_id: str
    ) -> List[dict]:
        """获取对话历史"""
        agent: KnowledgeAgent = request.state.agent

        history = await agent.memory.get_history(session_id)

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in history
        ]

# ===== 依赖注入 =====
async def provide_agent() -> KnowledgeAgent:
    """提供 Agent 实例"""
    # 实际应从依赖注入
    pass

async def provide_indexing_pipeline() -> IndexingPipeline:
    """提供索引管道"""
    pass

# ===== 应用 =====
app = Litestar(
    route_handlers=[AgentController],
    dependencies={
        "agent": provide_agent,
        "indexing_pipeline": provide_indexing_pipeline
    }
)
```

---

### 第五部分：部署与运维

#### 5.1 Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - QDRANT_HOST=qdrant
      - REDIS_HOST=redis
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - qdrant
      - redis
      - postgres
    deploy:
      resources:
        limits:
          memory: 2G

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=knowledge_assistant
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  qdrant_data:
  redis_data:
  postgres_data:
```

#### 5.2 监控配置

```python
# 监控指标
from prometheus_client import Counter, Histogram, Gauge

# 请求指标
REQUEST_COUNT = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["intent", "status"]
)

REQUEST_LATENCY = Histogram(
    "agent_request_latency_seconds",
    "Request latency",
    ["intent"]
)

ACTIVE_SESSIONS = Gauge(
    "agent_active_sessions",
    "Number of active sessions"
)

# 检索指标
RETRIEVAL_LATENCY = Histogram(
    "retrieval_latency_seconds",
    "Retrieval latency",
    ["retriever_type"]
)

RETRIEVAL_HIT_RATE = Gauge(
    "retrieval_hit_rate",
    "Retrieval hit rate",
    ["collection"]
)
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 设计完整的 AI Agent 系统架构
- [ ] 实现意图分类、记忆管理、工具编排
- [ ] 构建 Advanced RAG 管道（HyDE、混合检索、重排序）
- [ ] 实现文档解析、分块、索引全流程
- [ ] 部署高可用的生产环境
- [ ] 设置监控和告警

---

## 🔗 相关资源

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Qdrant 文档](https://qdrant.tech/documentation/)
- [Enterprise RAG 最佳实践](https://github.com/run-llama/llama-recipes)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M07: RAG 评估深度
- 学习 M08: AI 产品发布与运营
- 探索 Stage R: 前沿探索实验室

---

**最后更新**: 2026-07-18
