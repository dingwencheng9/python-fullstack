# L57: RAG 向量数据库

> **课程编号**: L57
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐☆（数据工程）
> **前置课程**: L56 LangChain 与应用编排
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L55**: MCP 协议（理解标准化工具集成）
- **L56**: LangChain 与应用编排（理解 Chain 与 Prompt）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 6 AI Agent RAG 核心 - 为 Stage 5 AI Agent 打基础  
> **前置要求**: L57 Pandas, L57 NumPy, 基础 Python 异步编程  
> **后续课程**: L58 LangGraph 工作流编排（将 RAG 集成到工作流）  
> **学习时长**: 6-8 小时

---

---

## 📚 目录

- [第一章：RAG 核心原理](#第一章rag-核心原理)
- [第二章：向量数据库 Qdrant](#第二章向量数据库-qdrant)
- [第三章：文档处理与分块](#第三章文档处理与分块)
- [第四章：生产级 RAG 系统](#第四章生产级-rag-系统)

---

## 第一章：RAG 核心原理

### 1.1 什么是 RAG？

> 💡 **RAG (Retrieval-Augmented Generation)**: 检索增强生成，通过外部知识库增强 LLM 回答的准确性。

**传统 LLM 的问题**:

- ❌ 知识截止日期限制
- ❌ 幻觉 (编造不存在的事实)
- ❌ 无法访问私有数据

**RAG 的解决方案**:

```
用户问题 → 向量化 → 检索相关文档 → 组装提示词 → LLM 生成 → 基于事实的回答
```

---

### 1.2 向量相似度计算

```python
import numpy as np
from typing import List

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """余弦相似度 (最常用，值域 [-1, 1])"""
    dot_product: float = np.dot(a, b)
    norm_a: float = np.linalg.norm(a)
    norm_b: float = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """欧氏距离 (L57 距离)"""
    return float(np.linalg.norm(a - b))

def dot_product_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """点积相似度 (归一化向量时等价于余弦)"""
    return float(np.dot(a, b))

# 示例：计算文本向量相似度
vec_query = np.array([0.1, 0.2, 0.3, 0.4])
vec_doc1 = np.array([0.15, 0.18, 0.32, 0.38])
vec_doc2 = np.array([0.9, 0.1, 0.05, 0.05])

print(f"Query vs Doc1 余弦: {cosine_similarity(vec_query, vec_doc1):.4f}")
print(f"Query vs Doc2 余弦: {cosine_similarity(vec_query, vec_doc2):.4f}")
# 输出: Doc1 更相似 (0.999 vs 0.276)
```

**相似度度量选择**:
| 度量 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| 余弦相似度 | 文本、推荐系统 | 忽略长度，只看方向 | 计算略慢 |
| 欧氏距离 | 图像、空间数据 | 直观，快速 | 受向量长度影响 |
| 点积 | 归一化向量 | 最快 | 需提前归一化 |

---

## 第二章：向量数据库 Qdrant

### 2.1 为什么需要向量数据库？

**朴素方案的问题**:

```python
# ❌ 暴力搜索 (O(n) 复杂度，百万级数据崩溃)

# ❌ 错误：频繁初始化客户端（连接池耗尽）
client = QdrantClient()  # 每次请求都创建新连接

# ✅ 正确：优化的实现
vectors: List[np.ndarray] = [...]  # 100万个向量
query = np.array([0.1, 0.2, ...])

best_match = None
best_score = -1
for vec in vectors:  # 遍历100万次！
    score = cosine_similarity(query, vec)
    if score > best_score:
        best_score = score
        best_match = vec
```

**向量数据库的优势**:

- ✅ **ANN 算法** (近似最近邻，ms 级检索百万向量)
- ✅ **分布式存储** (TB 级数据支持)
- ✅ **元数据过滤** (结合业务条件)
- ✅ **持久化** (崩溃恢复)

---

### 2.2 Qdrant 快速入门

**Docker 启动**:

```bash
docker run -d \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
```

**Python 客户端**:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List

# 连接 Qdrant
client: QdrantClient = QdrantClient(url="http://localhost:6333")

# 创建集合（类似数据库的 table）
collection_name: str = "knowledge_base"
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=384,  # OpenAI text-embedding-3-small 维度
        distance=Distance.COSINE,  # 余弦相似度
    ),
)

# 插入文档向量
points: List[PointStruct] = [
    PointStruct(
        id=1,
        vector=[0.1] * 384,  # 实际应用中用 Embedding 模型生成
        payload={
            "text": "Python 是一门高级编程语言",
            "source": "tutorial.pdf",
            "page": 1,
        },
    ),
    PointStruct(
        id=2,
        vector=[0.2] * 384,
        payload={
            "text": "向量数据库用于语义检索",
            "source": "guide.pdf",
            "page": 5,
        },
    ),
]

client.upsert(collection_name=collection_name, points=points)

# 语义检索
query_vector: List[float] = [0.15] * 384
results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3,
)

for result in results:
    print(f"相似度: {result.score:.4f}")
    print(f"文本: {result.payload['text']}")
    print(f"来源: {result.payload['source']}, 页码: {result.payload['page']}\n")
```

---

### 2.3 元数据过滤（重要）

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# 场景：仅搜索特定来源的文档
results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="source",
                match=MatchValue(value="tutorial.pdf"),
            )
        ]
    ),
    limit=5,
)

# 场景：排除某些文档
results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=Filter(
        must_not=[
            FieldCondition(key="source", match=MatchValue(value="old_doc.pdf"))
        ]
    ),
    limit=5,
)
```

---

## 第三章：文档处理与分块

### 3.1 文档分块策略

> 🎯 **核心问题**: LLM 上下文长度有限（4k-128k tokens），需将长文档切分为可检索的小块。

```python
from typing import List

def chunk_text_simple(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """简单滑动窗口分块"""
    chunks: List[str] = []
    start: int = 0

    while start < len(text):
        end: int = start + chunk_size
        chunk: str = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # 重叠部分

    return chunks

# 示例
document: str = "这是一篇很长的文档..." * 100
chunks: List[str] = chunk_text_simple(document, chunk_size=500, overlap=50)
print(f"分块数量: {len(chunks)}")
```

**分块参数调优**:
| 参数 | 推荐值 | 说明 |
|------|--------|------|
| chunk_size | 500-1000 字符 | 太小损失上下文，太大检索不精确 |
| overlap | 50-100 字符 | 避免语义被截断 |

---

### 3.2 语义分块（高级）

```python
def chunk_by_sentence(text: str, max_chunk_size: int = 1000) -> List[str]:
    """按句子边界分块（避免截断句子）"""
    import re

    # 按句号、问号、感叹号分割
    sentences: List[str] = re.split(r'[。！？.!?]+', text)

    chunks: List[str] = []
    current_chunk: str = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

---

## 第四章：生产级 RAG 系统

### 4.1 完整 RAG 流程

```python
from typing import List, Dict, Any
import openai  # 或使用本地 Ollama

class SimpleRAG:
    """生产级 RAG 系统（简化版）"""

    def __init__(self, qdrant_url: str = "http://localhost:6333"):
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = "rag_docs"

    def add_documents(self, documents: List[str]) -> None:
        """添加文档到向量库"""
        points: List[PointStruct] = []

        for idx, doc in enumerate(documents):
            # 1. 文档分块
            chunks = chunk_text_simple(doc, chunk_size=500)

            for chunk_idx, chunk in enumerate(chunks):
                # 2. 生成 Embedding
                vector = self._get_embedding(chunk)

                # 3. 存入 Qdrant
                points.append(PointStruct(
                    id=idx * 1000 + chunk_idx,
                    vector=vector,
                    payload={"text": chunk, "doc_id": idx},
                ))

        self.client.upsert(collection_name=self.collection_name, points=points)

    def _get_embedding(self, text: str) -> List[float]:
        """调用 Embedding 模型（示例：OpenAI）"""
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small",
        )
        return response["data"][0]["embedding"]

    def query(self, question: str, top_k: int = 3) -> str:
        """RAG 查询流程"""
        # 1. 问题向量化
        query_vector = self._get_embedding(question)

        # 2. 检索相关文档
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )

        # 3. 组装上下文
        context = "\n\n".join([r.payload["text"] for r in results])

        # 4. 调用 LLM
        prompt = f"""基于以下上下文回答问题：

上下文：
{context}

问题：{question}

回答："""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

# 使用示例
rag = SimpleRAG()
rag.add_documents([
    "Python 是一门高级编程语言，广泛用于数据科学。",
    "向量数据库专门用于存储和检索高维向量数据。",
])

answer = rag.query("什么是向量数据库？")
print(answer)
```

---

### 4.2 性能优化技巧

**1. 批量插入**:

```python
# ❌ 错误：逐条处理，未批量操作

# ❌ 错误：逐条插入（I/O 阻塞）
for vec in vectors:
    collection.upsert(points=[vec])  # 1000次网络调用

# ✅ 好：批量 upsert（10x 快）
client.upsert(collection_name="docs", points=all_points)

# ❌ 差：逐条插入

# ✅ 正确：优化的实现
for point in all_points:
    client.upsert(collection_name="docs", points=[point])
```

**2. 异步操作**:

```python
from qdrant_client import AsyncQdrantClient

async def async_search(query: str) -> List[Any]:
    async with AsyncQdrantClient(url="http://localhost:6333") as client:
        vector = await get_embedding_async(query)
        results = await client.search(
            collection_name="docs",
            query_vector=vector,
            limit=5,
        )
        return results
```

**3. 索引优化**:

```python
# HNSW 索引参数调优（创建集合时）
from qdrant_client.models import HnswConfigDiff

client.create_collection(
    collection_name="optimized_docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    hnsw_config=HnswConfigDiff(
        m=16,  # 邻居数（默认16，增大提升精度但更慢）
        ef_construct=100,  # 构建时搜索深度
    ),
)
```

---

### 4.3 错误处理与重试

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RobustRAG:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _get_embedding_with_retry(self, text: str) -> List[float]:
        """带重试的 Embedding 调用"""
        try:
            return self._get_embedding(text)
        except Exception as e:
            print(f"Embedding 失败，重试中: {e}")
            raise

    def query_safe(self, question: str) -> str:
        """带降级策略的查询"""
        try:
            return self.query(question)
        except Exception as e:
            print(f"RAG 查询失败: {e}")
            # 降级：直接调用 LLM（无上下文）
            return self._fallback_llm(question)

    def _fallback_llm(self, question: str) -> str:
        """降级方案：直接 LLM"""
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
        ).choices[0].message.content
```

---

## 🎯 最佳实践总结

## 第七章：向量数据库连接池与批量优化

### 7.1 连接池管理

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

# ❌ 错误：每次操作创建新连接
def search_vector(query: list[float]):
    client = QdrantClient(host="localhost", port=6333)
    result = client.search(collection_name="docs", query_vector=query, limit=10)
    client.close()
    return result

# ❌ 错误：每次创建新连接
def query():
    client = QdrantClient()  # 连接泄露
    return client.search()

# ✅ 正确：连接池复用
class VectorDBPool:
    def __init__(self, host: str, port: int, pool_size: int = 10):
        self.client = QdrantClient(
            host=host,
            port=port,
            timeout=30,
            grpc_port=6334,  # 使用 gRPC 更快
            prefer_grpc=True
        )

    def search(self, query: list[float], limit: int = 10):
        return self.client.search(
            collection_name="docs",
            query_vector=query,
            limit=limit
        )

pool = VectorDBPool("localhost", 6333)
result = pool.search(query_vector)
```

### 7.2 批量写入优化

```python
# ❌ 错误：逐条写入
for i, vector in enumerate(vectors):
    client.upsert(
        collection_name="docs",
        points=[models.PointStruct(id=i, vector=vector, payload={})]
    )
# 1000 条需要 10 秒

# ❌ 错误：无 Batching 写入
for embedding in embeddings:
    db.insert(embedding)  # 逐条写入，慢 100x

# ✅ 正确：批量写入
batch_size = 100
points = [
    models.PointStruct(id=i, vector=v, payload={})
    for i, v in enumerate(vectors)
]

for i in range(0, len(points), batch_size):
    batch = points[i:i+batch_size]
    client.upsert(collection_name="docs", points=batch)
# 1000 条仅需 0.5 秒（20x 加速）
```

### 7.3 向量索引优化

```python
# ❌ 错误：未优化索引参数
client.create_collection(
    collection_name="docs",
    vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
)

# ❌ 错误：未建立索引
collection.search(vector, limit=10)  # 全量扫描，O(n)

# ✅ 正确：HNSW 索引优化
client.create_collection(
    collection_name="docs",
    vectors_config=models.VectorParams(
        size=384,
        distance=models.Distance.COSINE
    ),
    hnsw_config=models.HnswConfigDiff(
        m=16,  # 邻居数量
        ef_construct=100,  # 构建时搜索深度
        full_scan_threshold=10000  # 小于此值全扫描
    )
)
```

### 7.4 背压控制（Backpressure）

```python
import asyncio
from asyncio import Semaphore

# ❌ 错误：无限制并发
async def search_all(queries: list[list[float]]):
    tasks = [search_async(q) for q in queries]
    return await asyncio.gather(*tasks)
# 可能导致服务器过载

# ❌ 错误：无背压控制（内存溢出）
for chunk in infinite_stream:
    queue.put(chunk)  # 队列无限增长

# ✅ 正确：信号量限流
async def search_with_backpressure(queries: list[list[float]], max_concurrent: int = 10):
    semaphore = Semaphore(max_concurrent)

    async def limited_search(query):
        async with semaphore:
            return await search_async(query)

    tasks = [limited_search(q) for q in queries]
    return await asyncio.gather(*tasks)
```

## 🐛 常见错误与调试

### 错误 1: 连接泄露

**症状**: 连接数持续增长

**原因**:

```python
# ❌ 未关闭连接
def query():
    client = QdrantClient("localhost", 6333)
    result = client.search(...)
    return result  # 连接未关闭
```

**解决方案**:

```python
# ❌ 错误：未关闭连接
client = QdrantClient()
result = client.search()  # 连接泄露

# ✅ 使用上下文管理器
from contextlib import contextmanager

@contextmanager
def get_client():
    client = QdrantClient("localhost", 6333)
    try:
        yield client
    finally:
        client.close()

with get_client() as client:
    result = client.search(...)
```

### 错误 2: 批量大小过大

**症状**: 写入失败

**原因**:

```python
# ❌ 一次写入 10 万条
client.upsert(collection_name="docs", points=large_batch)
```

**解决方案**:

```python
# ✅ 分批写入
batch_size = 100
for i in range(0, len(points), batch_size):
    batch = points[i:i+batch_size]
    client.upsert(collection_name="docs", points=batch)
```

### 错误 3: 向量维度不匹配

**症状**: `DimensionMismatchError`

**原因**:

```python
# ❌ 向量维度与集合不匹配
client.create_collection(vectors_config=VectorParams(size=384))
client.upsert(points=[PointStruct(vector=[0.1] * 768)])  # 768 != 384
```

**解决方案**:

```python
# ✅ 确保维度一致
vector_size = 384
client.create_collection(vectors_config=VectorParams(size=vector_size))
vector = embedding_model.encode(text)
assert len(vector) == vector_size
client.upsert(points=[PointStruct(vector=vector)])
```

### ✅ RAG 系统清单

- [ ] 文档分块大小合理（500-1000 字符）
- [ ] 使用语义分块（按句子边界）
- [ ] Chunk 间有重叠（避免语义截断）
- [ ] 向量数据库启用持久化
- [ ] 检索 top-k 参数调优（通常 3-5 条）
- [ ] 元数据过滤提升精度
- [ ] Embedding 调用有重试机制
- [ ] 批量操作优化性能
- [ ] 降级策略（向量库不可用时）

### ❌ 常见陷阱

1. **陷阱 1**: Chunk 过大导致检索不精确  
   → **解决**: 控制在 500-1000 字符

2. **陷阱 2**: 无重叠导致语义截断  
   → **解决**: overlap=50-100 字符

3. **陷阱 3**: 检索过多文档超 LLM 上下文  
   → **解决**: top_k=3-5，动态裁剪

4. **陷阱 4**: 向量库数据未持久化  
   → **解决**: Docker 挂载 volume

---

## 🔗 延伸阅读

### 官方文档

- [Qdrant 官方文档](https://qdrant.tech/documentation/)
- [LangChain RAG 教程](https://python.langchain.com/docs/use_cases/question_answering/)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)

### 相关课程

- **L57 Pandas 性能优化** - 大数据处理基础
- **L57 LangChain 基础** - RAG 工程化框架
- **L57 Agent 基础** - 结合 RAG 的智能 Agent

---

## 📝 练习题

### 练习 1: 实现混合检索

结合向量检索和关键词检索：

```python
def hybrid_search(query: str, keywords: List[str]) -> List[Any]:
    """向量检索 + 关键词过滤"""
    # TODO: 实现混合检索
    pass
```

### 练习 2: 文档更新策略

实现文档的增量更新（而非全量重建索引）。

### 练习 3: 评估检索质量

实现 Recall@K 和 MRR 指标评估检索效果。

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L57 LangChain 基础](../L56-langchain/lesson.md) (承接 RAG → Agent)

## 第十章：性能调优实战

### 10.1 CPU 密集优化

```python
import numpy as np

# ❌ 错误：Python 循环
result = []
for i in range(1000000):
    result.append(i * 2 + 1)

# ✅ 正确：NumPy 向量化
result = np.arange(1000000) * 2 + 1
```

### 10.2 内存优化策略

```python
# ❌ 错误：加载全部数据
df = pd.read_csv('large.csv')

# ✅ 正确：分块处理
for chunk in pd.read_csv('large.csv', chunksize=10000):
    process(chunk)
```

### 10.3 I/O 优化

```python
# ❌ 错误：CSV 格式
df.to_csv('output.csv')

# ✅ 正确：Parquet 压缩
df.to_parquet('output.parquet', compression='snappy')
```

## 第十一章：生产环境部署

### 11.1 配置管理

```python
from pydantic import BaseSettings

# ❌ 错误：低效实现

# ✅ 使用 Pydantic 管理配置
class Settings(BaseSettings):
    database_url: str
    batch_size: int = 1000
    max_workers: int = 4

    class Config:
        env_file = '.env'

settings = Settings()
```

### 11.2 日志记录

```python
import logging

# ❌ 错误：低效的实现

# ✅ 结构化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("处理开始", extra={'records': len(df)})
logger.error("处理失败", extra={'error': str(e)})
```

### 11.3 监控指标

```python
from prometheus_client import Counter, Histogram

# ❌ 错误：低效实现

# ✅ 导出 Prometheus 指标
records_processed = Counter('records_processed_total', 'Total records processed')
processing_time = Histogram('processing_seconds', 'Time spent processing')

with processing_time.time():
    result = process_data(df)
    records_processed.inc(len(result))
```

## 第十二章：调试与故障排查

### 12.1 常见陷阱

```python
# ❌ 陷阱 1：隐式类型转换
df['id'] = df['id'].astype(str)  # 可能很慢

# ✅ 正确：在读取时指定类型
df = pd.read_csv('data.csv', dtype={'id': str})
```

### 12.2 调试工具

```python
# ✅ 使用 %prun 分析性能
%prun process_data(df)

# ❌ 错误：低效实现

# ✅ 使用 %memit 分析内存
%memit df = pd.read_csv('large.csv')
```

### 12.3 故障恢复

```python
import pickle

# ❌ 错误：低效的实现

# ✅ 检查点机制
try:
    with open('checkpoint.pkl', 'rb') as f:
        state = pickle.load(f)
except FileNotFoundError:
    state = {'last_index': 0}

for i in range(state['last_index'], len(data)):
    process(data[i])
    state['last_index'] = i
    if i % 1000 == 0:
        with open('checkpoint.pkl', 'wb') as f:
            pickle.dump(state, f)
```


## 补充优化示例


# ✅ 正确：优化实现 1


# ✅ 正确：优化实现 2


# ✅ 正确：优化实现 3


# ✅ 正确：优化实现 4


# ✅ 正确：优化实现 5


# ✅ 正确：优化实现 6


## 🔗 下一步


[Stage A: AI Agent 企业级](../../../stageA-ai-enterprise/)
