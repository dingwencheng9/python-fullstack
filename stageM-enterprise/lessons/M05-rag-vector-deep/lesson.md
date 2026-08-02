# M05: RAG 向量库深入

> **课程编号**: M05
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 5-6 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: M02 (LlamaIndex 高级 RAG)、L49 (DuckDB)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **向量数据库**：掌握主流向量数据库的原理和选型
2. **索引优化**：实现 HNSW、IVF 等高级索引
3. **混合搜索**：结合向量搜索与全文搜索
4. **生产部署**：构建高可用向量搜索服务

---

## 📚 课程内容

### 第一部分：向量数据库概述

#### 1.1 为什么需要向量数据库

```
传统数据库 vs 向量数据库：

传统数据库：
- 精确匹配
- 结构化查询
- 适合 ACID 事务

向量数据库：
- 近似最近邻 (ANN) 搜索
- 高维向量检索
- 适合语义相似度
```

#### 1.2 主流向量数据库对比

| 数据库 | 特点 | 适用场景 | 性能 |
|--------|------|----------|------|
| **Qdrant** | Rust 实现，持久化强 | 生产环境 | ⭐⭐⭐⭐⭐ |
| **Milvus** | 功能丰富，分布式 | 大规模数据 | ⭐⭐⭐⭐ |
| **Weaviate** | 原生 GraphQL | 知识图谱 | ⭐⭐⭐ |
| **Pinecone** | 全托管，云原生 | 快速上线 | ⭐⭐⭐⭐ |
| **Chroma** | 轻量，Python 优先 | 原型/MLOps | ⭐⭐⭐ |

#### 1.3 向量表示与度量

```python
import numpy as np
from typing import Literal

class VectorMetric:
    """向量相似度度量"""

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """余弦相似度"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @staticmethod
    def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
        """欧几里得距离"""
        return np.linalg.norm(a - b)

    @staticmethod
    def dot_product(a: np.ndarray, b: np.ndarray) -> float:
        """点积"""
        return np.dot(a, b)

class EmbeddingGenerator:
    """嵌入向量生成器"""

    def __init__(self, model_name: str = "BAAI/bge-large-zh-v1.5"):
        from transformers import AutoTokenizer, AutoModel
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def encode(self, texts: list[str], normalize: bool = True) -> np.ndarray:
        """生成嵌入向量"""
        import torch
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            # Mean pooling
            embeddings = outputs.last_hidden_state.mean(dim=1)

        if normalize:
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

        return embeddings.numpy()

    def similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的相似度"""
        vec1, vec2 = self.encode([text1, text2])
        return VectorMetric.cosine_similarity(vec1[0], vec2[0])
```

---

### 第二部分：Qdrant 实战

#### 2.1 Qdrant 核心概念

```
Qdrant 架构：

┌─────────────────────────────────────────┐
│              Qdrant Server               │
├─────────────────────────────────────────┤
│                                          │
│  ┌──────────┐    ┌──────────┐           │
│  │ Collection│ ← │ Points   │           │
│  │ (索引)    │    │ (向量)    │           │
│  └──────────┘    └──────────┘           │
│        ↓                                  │
│  ┌──────────┐    ┌──────────┐           │
│  │ HNSW     │    │ Payload  │           │
│  │ (索引)    │    │ (元数据)  │           │
│  └──────────┘    └──────────┘           │
│                                          │
└─────────────────────────────────────────┘
         ↑
    Qdrant Client (Python)
```

#### 2.2 基础操作

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http import models
from typing import List, Optional
import numpy as np

class QdrantVectorStore:
    """Qdrant 向量存储"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        vector_size: int = 1024
    ):
        self.client = QdrantClient(host=host, port=port)
        self.vector_size = vector_size

    def create_collection(
        self,
        collection_name: str,
        distance: Distance = Distance.COSINE
    ) -> bool:
        """创建 Collection"""
        collections = self.client.get_collections().collections
        if collection_name in [c.name for c in collections]:
            print(f"Collection {collection_name} already exists")
            return False

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=distance
            )
        )
        print(f"Collection {collection_name} created")
        return True

    def upsert_points(
        self,
        collection_name: str,
        vectors: List[np.ndarray],
        payloads: List[dict],
        ids: Optional[List[int]] = None
    ) -> None:
        """批量插入向量"""
        if ids is None:
            ids = list(range(len(vectors)))

        points = [
            PointStruct(
                id=idx,
                vector=vec.tolist(),
                payload=payload
            )
            for idx, vec, payload in zip(ids, vectors, payloads)
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Upserted {len(points)} points")

    def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        limit: int = 5,
        score_threshold: Optional[float] = None,
        query_filter: Optional[dict] = None
    ) -> List[dict]:
        """向量搜索"""
        search_params = models.SearchParams(
            hnsw_ef=128,  # HNSW 参数
            exact=False
        )

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector.tolist(),
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
            search_params=search_params
        )

        return [
            {
                "id": r.id,
                "score": r.score,
                "payload": r.payload
            }
            for r in results
        ]

    def search_batch(
        self,
        collection_name: str,
        query_vectors: List[np.ndarray],
        limit: int = 5
    ) -> List[List[dict]]:
        """批量搜索"""
        results = self.client.search_batch(
            collection_name=collection_name,
            query_vector=query_vectors.tolist(),
            limit=limit
        )

        return [
            [
                {"id": r.id, "score": r.score, "payload": r.payload}
                for r in batch_results
            ]
            for batch_results in results
        ]

    def delete_collection(self, collection_name: str) -> None:
        """删除 Collection"""
        self.client.delete_collection(collection_name=collection_name)
        print(f"Collection {collection_name} deleted")
```

#### 2.3 过滤与条件查询

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range, Must, MustNot

class QdrantFilteredSearch:
    """Qdrant 过滤搜索"""

    def __init__(self, client: QdrantClient):
        self.client = client

    def search_with_filter(
        self,
        collection_name: str,
        query_vector: List[float],
        filter_conditions: dict
    ) -> List[dict]:
        """带过滤条件的搜索"""
        # 构建过滤器
        filter_model = Filter(**filter_conditions)

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=filter_model,
            limit=10
        )

        return results

    def search_by_metadata(
        self,
        collection_name: str,
        query_vector: List[float],
        category: Optional[str] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> List[dict]:
        """基于元数据过滤"""
        must_conditions = []

        # 分类过滤
        if category:
            must_conditions.append(
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category)
                )
            )

        # 范围过滤
        if min_year or max_year:
            range_dict = {}
            if min_year:
                range_dict["gte"] = min_year
            if max_year:
                range_dict["lte"] = max_year
            must_conditions.append(
                FieldCondition(
                    key="year",
                    range=Range(**range_dict)
                )
            )

        # 标签过滤（至少匹配一个）
        if tags:
            must_conditions.append(
                FieldCondition(
                    key="tags",
                    match=models.MatchAny(any=tags)
                )
            )

        if must_conditions:
            filter_model = Filter(must=must_conditions)
        else:
            filter_model = None

        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=filter_model,
            limit=10
        )

        return results

    def search_with_exclude(
        self,
        collection_name: str,
        query_vector: List[float],
        exclude_ids: List[int]
    ) -> List[dict]:
        """排除特定 ID"""
        filter_model = Filter(
            must_not=[
                FieldCondition(
                    key="id",
                    match=models.MatchAny(any=[str(i) for i in exclude_ids])
                )
            ]
        )

        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=filter_model,
            limit=10
        )
```

---

### 第三部分：高级索引

#### 3.1 HNSW 算法原理

```
HNSW (Hierarchical Navigable Small World)：

Level 3:    ○ ────── ○           (稀疏，跨度大)
            │       │
Level 2:    ○ ─ ○ ─ ○ ─ ○       (中层)
            │   │   │   │
Level 1:    ○ ─ ○ ─ ○ ─ ○ ─ ○   (密集，跨度小)
            │   │   │   │   │
Level 0:    ● ═ ● ═ ● ═ ● ═ ●   (最底层，原始数据)

搜索过程：
1. 从顶层入口开始
2. 贪心搜索最近邻
3. 下降到下一层
4. 重复直到最底层
```

#### 3.2 索引配置优化

```python
from qdrant_client.models import HnswConfigDiff, QuantizationConfig, ScalarQuantization

class VectorIndexOptimizer:
    """向量索引优化器"""

    @staticmethod
    def create_hnsw_optimized() -> HnswConfigDiff:
        """
        创建优化的 HNSW 配置

        参数说明：
        - m: 每个节点的最大连接数（影响召回率和内存）
        - ef_construct: 构建时的搜索范围（影响构建速度和召回率）
        - full_scan_threshold: 超过此数量的数据使用 HNSW
        - on_disk: 是否将索引存储在磁盘上
        """
        return HnswConfigDiff(
            m=16,                    # 默认 16，更高 = 更准确但更慢
            ef_construct=200,        # 默认 100，更高 = 更准确但更慢
            full_scan_threshold=10000,  # 超过 1 万条数据使用 HNSW
            on_disk=False,           # 小数据可以不开启
            index_type=models.HnswIndexType.HNSW,  # HNSW 算法
            quantization=models.VectorParamsDiff.QuantizationConfig(
                scalar=ScalarQuantization(
                    scalar=ScalarQuantizationConfig(
                        type=models.ScalarQuantizationType.INT8,
                        quantile=0.99,
                        always_ram=True
                    )
                )
            )
        )

    @staticmethod
    def create_memory_optimized() -> HnswConfigDiff:
        """内存优化配置（用于大规模数据）"""
        return HnswConfigDiff(
            m=8,                     # 减少连接数
            ef_construct=64,         # 减少构建搜索范围
            full_scan_threshold=5000,
            on_disk=True,            # 索引存磁盘
        )

class CollectionOptimizer:
    """Collection 优化"""

    def __init__(self, client: QdrantClient):
        self.client = client

    def optimize_collection(
        self,
        collection_name: str,
        vectors_config: dict,
        hnsw_config: Optional[HnswConfigDiff] = None,
        quantization: Optional[QuantizationConfig] = None
    ) -> None:
        """优化 Collection 配置"""

        # 更新向量配置
        if vectors_config:
            self.client.update_collection(
                collection_name=collection_name,
                vectors_config=vectors_config
            )

        # 更新 HNSW 配置
        if hnsw_config:
            self.client.update_collection(
                collection_name=collection_name,
                hnsw_config=hnsw_config
            )

        print(f"Collection {collection_name} optimized")

    def rebuild_index(self, collection_name: str) -> None:
        """重建索引"""
        # 删除现有索引
        self.client.delete_payload_index(
            collection_name=collection_name,
            payload_field="*"
        )

        # 触发优化
        self.client.optimizers(
            collection_name=collection_name,
            vacuum_min_vector_size=1,
            default_segment_number=0
        )

        print(f"Index rebuilt for {collection_name}")
```

---

### 第四部分：混合搜索

#### 4.1 向量 + BM25 混合

```python
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import numpy as np

@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    score: float
    vector_score: float = 0.0
    keyword_score: float = 0.0
    payload: dict = field(default_factory=dict)

class HybridSearchEngine:
    """混合搜索引擎（向量 + BM25）"""

    def __init__(
        self,
        vector_store: QdrantVectorStore,
        bm25_index,  # 如 rank_bm25
        alpha: float = 0.7  # 向量权重
    ):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.alpha = alpha  # alpha=1.0 只用向量，alpha=0.0 只用 BM25

    def search(
        self,
        collection_name: str,
        query_text: str,
        query_vector: np.ndarray,
        limit: int = 10,
        keyword_weight: float = 0.3
    ) -> List[SearchResult]:
        """
        执行混合搜索

        融合策略：Reciprocal Rank Fusion (RRF)
        """
        # 1. 向量搜索
        vector_results = self.vector_store.search(
            collection_name,
            query_vector,
            limit=limit * 3  # 多取一些用于融合
        )

        # 2. BM25 搜索
        bm25_scores = self._bm25_search(query_text, limit=limit * 3)

        # 3. RRF 融合
        fused_scores = self._reciprocal_rank_fusion(
            vector_results,
            bm25_scores,
            k=60  # RRF 参数
        )

        # 4. 合并结果
        results = []
        for item_id, rrf_score in fused_scores[:limit]:
            # 找到向量搜索结果中的详情
            vec_result = next(
                (r for r in vector_results if r["id"] == item_id),
                None
            )

            if vec_result:
                results.append(SearchResult(
                    id=item_id,
                    score=rrf_score,
                    vector_score=vec_result.get("score", 0),
                    payload=vec_result.get("payload", {})
                ))
            else:
                # 只在 BM25 中找到
                results.append(SearchResult(
                    id=item_id,
                    score=rrf_score,
                    keyword_score=bm25_scores.get(item_id, 0),
                    payload={}
                ))

        return results

    def _bm25_search(
        self,
        query: str,
        limit: int
    ) -> dict[str, float]:
        """BM25 搜索"""
        # 使用 rank_bm25 库
        bm25_scores = {}

        # 实际应使用 bm25_index.get_scores(query)
        # 这里简化处理
        scores = self.bm25_index.get_scores(query.split())

        # 获取 top-k
        indexed_scores = list(enumerate(scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        for idx, score in indexed_scores[:limit]:
            bm25_scores[str(idx)] = score

        return bm25_scores

    def _reciprocal_rank_fusion(
        self,
        results_a: List[dict],
        scores_b: dict,
        k: int = 60
    ) -> List[Tuple[str, float]]:
        """
        Reciprocal Rank Fusion

        RRF(a, b) = Σ 1/(k + rank(a))
        """
        fused = {}

        # 添加向量搜索结果
        for rank, result in enumerate(results_a):
            doc_id = str(result["id"])
            rrf_score = 1 / (k + rank + 1)
            fused[doc_id] = fused.get(doc_id, 0) + self.alpha * rrf_score

        # 添加 BM25 结果
        for doc_id, score in scores_b.items():
            rank = list(scores_b.keys()).index(doc_id)
            rrf_score = 1 / (k + rank + 1)
            fused[doc_id] = fused.get(doc_id, 0) + (1 - self.alpha) * rrf_score

        # 排序
        sorted_results = sorted(
            fused.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_results
```

---

### 第五部分：生产部署

#### 5.1 Docker 部署 Qdrant

```yaml
# docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"      # REST API
      - "6334:6334"      # gRPC
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__LOG_LEVEL=INFO
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  qdrant_storage:
```

#### 5.2 高可用配置

```python
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionConfig, OptimizersConfig

class QdrantClusterManager:
    """Qdrant 集群管理器"""

    def __init__(self, hosts: List[str], port: int = 6333):
        self.clients = [QdrantClient(host=h, port=port) for h in hosts]

    def create_collection_all(
        self,
        collection_name: str,
        vector_size: int,
        replication_factor: int = 2
    ) -> None:
        """在所有节点创建 Collection"""
        for client in self.clients:
            try:
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config={
                        "size": vector_size,
                        "distance": "Cosine"
                    },
                    replicas=replication_factor
                )
                print(f"Created on {client._host}")
            except Exception as e:
                print(f"Failed on {client._host}: {e}")

    def health_check_all(self) -> dict:
        """检查所有节点健康状态"""
        status = {}
        for client in self.clients:
            try:
                info = client.get_collections()
                status[client._host] = {
                    "status": "healthy",
                    "collections": len(info.collections)
                }
            except Exception as e:
                status[client._host] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        return status

    def distribute_data(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: List[dict]
    ) -> None:
        """数据分布写入"""
        # 简单的 round-robin 分布
        for i, (vec, payload) in enumerate(zip(vectors, payloads)):
            target_client = self.clients[i % len(self.clients)]

            target_client.upsert(
                collection_name=collection_name,
                points=[{
                    "id": i,
                    "vector": vec,
                    "payload": payload
                }]
            )
```

---

### 第五部分：GraphRAG 与知识图谱融合

#### 5.1 什么是 GraphRAG

GraphRAG（Graph Retrieval-Augmented Generation）将**知识图谱**与**向量检索**深度融合，解决传统向量 RAG 在复杂关系推理上的短板：

```
传统向量 RAG 的局限：
- 只捕捉语义相似性，忽略实体关系
- 无法处理多跳推理问题
- 答案碎片化，缺乏全局视图

GraphRAG 的优势：
- 利用知识图谱建立实体关系网络
- 支持多跳关系推理（2-hop, 3-hop）
- 提供全局性的总结性答案
```

#### 5.2 GraphRAG 架构

```
┌──────────────────────────────────────────────────────────────┐
│                      GraphRAG 架构                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│   │  原始文档   │ ───→ │ 实体抽取+   │ ───→ │   知识图谱   │ │
│   │  (Documents)│      │ 关系抽取    │      │ (Neo4j等)   │ │
│   └─────────────┘      └─────────────┘      └──────┬──────┘ │
│                                                      │        │
│   ┌─────────────┐      ┌─────────────┐              │        │
│   │  查询理解   │ ───→ │ 混合召回    │ ←─────────────┘        │
│   │  (Query)    │      │ (Vector+KG) │                       │
│   └─────────────┘      └──────┬──────┘                       │
│                               │                              │
│                        ┌──────▼──────┐                       │
│                        │  LLM 生成   │                       │
│                        │  (Answer)   │                       │
│                        └─────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

#### 5.3 实体与关系抽取

```python
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from enum import Enum

class EntityType(Enum):
    """实体类型"""
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    CONCEPT = "CONCEPT"

@dataclass
class Entity:
    """实体"""
    id: str
    name: str
    type: EntityType
    description: str = ""
    properties: Dict = None

@dataclass
class Relation:
    """关系"""
    source_id: str
    target_id: str
    relation_type: str  # 如: "WORKS_AT", "LOCATED_IN", "PRODUCED_BY"
    properties: Dict = None

class GraphExtractor:
    """基于 LLM 的图谱抽取器"""

    def __init__(self, llm):
        self.llm = llm

    def extract_entities(self, text: str) -> List[Entity]:
        """从文本中抽取实体"""
        prompt = f"""
从以下文本中抽取实体，返回 JSON 格式：
[
  {{"name": "实体名", "type": "实体类型", "description": "描述"}}
]

支持的实体类型: PERSON, ORGANIZATION, LOCATION, PRODUCT, EVENT, CONCEPT

文本: {text}
"""
        # 调用 LLM 抽取
        response = self.llm.invoke(prompt)
        # 解析 JSON 响应
        import json
        entities_data = json.loads(response.content)

        return [
            Entity(
                id=f"entity_{i}",
                name=e["name"],
                type=EntityType(e["type"]),
                description=e.get("description", "")
            )
            for i, e in enumerate(entities_data)
        ]

    def extract_relations(self, text: str, entities: List[Entity]) -> List[Relation]:
        """从文本中抽取关系"""
        entity_names = [e.name for e in entities]

        prompt = f"""
从以下文本中抽取实体之间的关系，返回 JSON 格式：
[
  {{"source": "实体A", "target": "实体B", "type": "关系类型"}}
]

已识别的实体: {entity_names}

关系类型示例: WORKS_AT, FOUNDED_BY, LOCATED_IN, PRODUCED_BY, PART_OF

文本: {text}
"""
        response = self.llm.invoke(prompt)
        import json
        relations_data = json.loads(response.content)

        # 建立名称到实体的映射
        name_to_entity = {e.name: e for e in entities}

        return [
            Relation(
                source_id=name_to_entity[r["source"]].id,
                target_id=name_to_entity[r["target"]].id,
                relation_type=r["type"]
            )
            for r in relations_data
            if r["source"] in name_to_entity and r["target"] in name_to_entity
        ]
```

#### 5.4 Neo4j 图数据库集成

```python
from neo4j import AsyncGraphDatabase
from typing import List, Optional

class Neo4jGraphStore:
    """Neo4j 图数据库存储"""

    def __init__(self, uri: str, username: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(username, password))

    async def close(self):
        await self.driver.close()

    async def create_entity(self, entity: Entity) -> None:
        """创建实体节点"""
        cypher = """
        MERGE (e:Entity {name: $name})
        SET e.type = $type,
            e.description = $description,
            e.id = $id
        """
        async with self.driver.session() as session:
            await session.run(cypher,
                name=entity.name,
                type=entity.type.value,
                description=entity.description,
                id=entity.id
            )

    async def create_relation(self, relation: Relation) -> None:
        """创建关系边"""
        cypher = """
        MATCH (s:Entity {id: $source_id})
        MATCH (t:Entity {id: $target_id})
        MERGE (s)-[r:RELATES {type: $relation_type}]->(t)
        """
        async with self.driver.session() as session:
            await session.run(cypher,
                source_id=relation.source_id,
                target_id=relation.target_id,
                relation_type=relation.relation_type
            )

    async def find_neighbors(self, entity_name: str, depth: int = 1) -> List[Dict]:
        """查找实体邻居（支持多跳）"""
        cypher = f"""
        MATCH (start:Entity {{name: $name}})-[r*1..{depth}]-(neighbor)
        RETURN start, relationships(r) as rels, neighbor
        LIMIT 50
        """
        async with self.driver.session() as session:
            result = await session.run(cypher, name=entity_name)
            records = await result.data()
            return records
```

#### 5.5 混合召回策略

```python
class HybridRetriever:
    """混合检索器：向量 + 图谱"""

    def __init__(
        self,
        vector_store: QdrantStore,
        graph_store: Neo4jGraphStore,
        embedder: EmbeddingGenerator
    ):
        self.vector_store = vector_store
        self.graph_store = graph_store
        self.embedder = embedder

    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        graph_depth: int = 2
    ) -> List[Dict]:
        """混合召回：向量检索 + 图谱扩展"""

        # 1. 向量检索
        vector_results = self.vector_store.search_documents(query, limit=top_k)
        vector_context = "\n".join([
            r["content"] for r in vector_results
        ])

        # 2. 从查询中提取实体
        query_entities = self._extract_query_entities(query)

        # 3. 图谱扩展（多跳关系）
        graph_contexts = []
        for entity_name in query_entities:
            neighbors = await self.graph_store.find_neighbors(
                entity_name, depth=graph_depth
            )
            for record in neighbors:
                neighbor = record["neighbor"]
                # 构建关系描述
                rel_desc = self._format_relationship(record["rels"])
                graph_contexts.append(
                    f"{entity_name} {rel_desc} {neighbor['name']}"
                )

        graph_context = "\n".join(graph_contexts)

        # 4. 融合上下文
        combined_context = f"""
# 向量检索结果
{vector_context}

# 知识图谱关系
{graph_context}
"""
        return combined_context

    def _extract_query_entities(self, query: str) -> List[str]:
        """从查询中提取关键实体（简化版）"""
        # 实际应用中应使用 NER 模型
        # 这里用关键词匹配演示
        common_entities = [
            "Apple", "Google", "Microsoft", "OpenAI",
            "Python", "LangChain", "FastAPI", "Neo4j"
        ]
        return [e for e in common_entities if e in query]

    def _format_relationship(self, rels: List[Dict]) -> str:
        """格式化关系描述"""
        if not rels:
            return "相关"
        return rels[0].get("type", "相关")
```

#### 5.6 GraphRAG 应用场景

| 场景 | 传统向量 RAG | GraphRAG |
|------|-------------|----------|
| **简单问答** | ✅ 高效 | ⚠️ 开销较高 |
| **关系推理** | ❌ 无法处理 | ✅ 原生支持 |
| **多跳查询** | ❌ 碎片化 | ✅ 链路追踪 |
| **全局总结** | ❌ 局部信息 | ✅ 图谱社区汇总 |
| **企业知识库** | ⚠️ 需要微调 | ✅ 可解释性强 |

#### 5.7 性能对比

```python
# GraphRAG vs 传统 RAG 性能对比

@dataclass
class PerformanceComparison:
    """性能对比数据"""
    metric: str
    vector_rag: float
    graph_rag: float

benchmarks = [
    PerformanceComparison("简单语义匹配", 0.95, 0.92),
    PerformanceComparison("2-hop 关系推理", 0.35, 0.88),
    PerformanceComparison("3-hop 关系推理", 0.15, 0.82),
    PerformanceComparison("全局总结任务", 0.45, 0.85),
    PerformanceComparison("查询延迟 (ms)", 45, 120),
]

print("| 指标 | 向量 RAG | GraphRAG |")
print("|------|----------|----------|")
for b in benchmarks:
    print(f"| {b.metric} | {b.vector_rag} | {b.graph_rag} |")
```

---

## 🚀 实战案例

### 案例：企业文档搜索系统

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import numpy as np

@dataclass
class Document:
    """文档"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime

class EnterpriseDocumentSearch:
    """企业文档搜索系统"""

    def __init__(
        self,
        vector_store: QdrantVectorStore,
        embedder,
        hybrid_searcher: HybridSearchEngine
    ):
        self.vector_store = vector_store
        self.embedder = embedder
        self.hybrid_searcher = hybrid_searcher
        self.collection_name = "enterprise_documents"

    def index_document(self, doc: Document) -> None:
        """索引文档"""
        # 生成向量
        vector = self.embedder.encode([doc.content])[0]

        # 构建 payload
        payload = {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "category": doc.category,
            "tags": doc.tags,
            "created_at": doc.created_at.isoformat(),
            "updated_at": doc.updated_at.isoformat()
        }

        # 存储
        self.vector_store.upsert_points(
            collection_name=self.collection_name,
            vectors=[vector],
            payloads=[payload],
            ids=[int(doc.id)]
        )

    def search_documents(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[dict]:
        """搜索文档"""
        # 生成查询向量
        query_vector = self.embedder.encode([query])[0]

        # 构建过滤器
        filter_conditions = {"must": []}

        if category:
            filter_conditions["must"].append({
                "key": "category",
                "match": {"value": category}
            })

        if tags:
            filter_conditions["must"].append({
                "key": "tags",
                "match": {"any": tags}
            })

        # 搜索
        results = self.vector_store.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter_conditions if filter_conditions["must"] else None
        )

        return results
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解主流向量数据库的特点和选型依据
- [ ] 使用 Qdrant 进行向量存储和检索
- [ ] 配置 HNSW 索引参数优化性能
- [ ] 实现向量搜索与 BM25 的混合搜索
- [ ] 使用 RRF 算法融合多种搜索结果
- [ ] 部署高可用的向量搜索服务
- [ ] **理解 GraphRAG 与知识图谱融合原理**
- [ ] **实现基于 Neo4j 的图谱存储与多跳查询**

---

## 🔗 相关资源

- [Qdrant 文档](https://qdrant.tech/documentation/)
- [HNSW 算法论文](https://arxiv.org/abs/1603.09320)
- [向量数据库对比](https://superlinked.com/vector-db-benchmark/)
- [GraphRAG 微软论文](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-through-graph-based-retrieval-augmentation/)
- [Neo4j 图数据库](https://neo4j.com/)
- [LlamaIndex GraphRAG](https://docs.llamaindex.ai/en/latest/examples/query_engine/knowledge_graph_query_engine.html)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M06: AI Agent 最终项目
- 学习 M07: RAG 评估深度
- 探索 Stage R: 前沿探索实验室

---

**最后更新**: 2026-07-23（新增 GraphRAG 与知识图谱融合章节）
