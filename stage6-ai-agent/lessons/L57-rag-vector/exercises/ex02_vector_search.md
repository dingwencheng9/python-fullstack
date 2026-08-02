# Exercise 02: Vector Search 高级检索

**难度**: ⭐⭐⭐⭐  
**预计时间**: 60 分钟  
**学习目标**: 掌握 Qdrant 的高级检索功能与元数据过滤

---

## 📋 任务描述

在 Jupyter Notebook 环境下，使用 `AsyncQdrantClient` 实现三个特定检索场景。

---

## 🎯 核心要求

### 场景 1: 模糊搜索（Fuzzy Search）

实现一个支持模糊匹配的检索器，在相似度搜索的基础上，允许一定程度的误差。

**输入**:

- 查询文本: "Python 编程"
- 相似度阈值: 0.7
- Top-K: 5

**输出**: 返回相似度 >= 0.7 的前 5 个结果

```python
async def fuzzy_search(
    client: AsyncQdrantClient,
    collection_name: str,
    query_vector: list[float],
    threshold: float = 0.7,
    limit: int = 5,
) -> list[ScoredPoint]:
    """
    模糊搜索

    Args:
        client: Qdrant 客户端
        collection_name: 集合名称
        query_vector: 查询向量
        threshold: 相似度阈值
        limit: 返回结果数量

    Returns:
        符合阈值的检索结果
    """
    pass  # TODO: 实现模糊搜索逻辑
```

---

### 场景 2: 元数据过滤（Metadata Filtering）

实现一个支持复杂元数据过滤的检索器。

**需求**:

1. **基础过滤**: 只返回 `category="tutorial"` 的文档
2. **范围过滤**: `publish_year >= 2023`
3. **OR 条件**: `language="zh"` 或 `language="en"`
4. **组合查询**: 向量相似度 + 元数据过滤

```python
async def metadata_search(
    client: AsyncQdrantClient,
    collection_name: str,
    query_vector: list[float],
    category: str,
    min_year: int,
    languages: list[str],
    limit: int = 10,
) -> list[ScoredPoint]:
    """
    元数据过滤检索

    Args:
        client: Qdrant 客户端
        collection_name: 集合名称
        query_vector: 查询向量
        category: 分类过滤
        min_year: 最小年份
        languages: 支持的语言列表
        limit: 返回结果数量

    Returns:
        符合所有条件的检索结果
    """
    pass  # TODO: 实现元数据过滤逻辑
```

**提示**: 使用 `Filter` 和 `FieldCondition`

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

filter_condition = Filter(
    must=[
        FieldCondition(key="category", match=MatchValue(value=category)),
        FieldCondition(key="publish_year", range=Range(gte=min_year)),
    ],
    should=[
        FieldCondition(key="language", match=MatchValue(value=lang))
        for lang in languages
    ],
)
```

---

### 场景 3: 相似度排序（Similarity Ranking）

实现一个多查询融合的检索器，对多个查询向量的结果进行加权融合。

**需求**:

1. 接收多个查询向量（如：主查询 + 扩展查询）
2. 每个查询向量有不同的权重
3. 融合结果并按最终得分排序

```python
from typing import NamedTuple

class WeightedQuery(NamedTuple):
    """加权查询"""
    vector: list[float]
    weight: float

async def similarity_ranking(
    client: AsyncQdrantClient,
    collection_name: str,
    queries: list[WeightedQuery],
    limit: int = 10,
) -> list[tuple[ScoredPoint, float]]:
    """
    多查询融合排序

    Args:
        client: Qdrant 客户端
        collection_name: 集合名称
        queries: 加权查询列表
        limit: 返回结果数量

    Returns:
        排序后的结果列表，每项包含 (ScoredPoint, 融合得分)

    Raises:
        ValueError: 查询列表为空或权重总和不为 1.0
    """
    pass  # TODO: 实现多查询融合逻辑
```

**算法提示**:

```python
# 1. 对每个查询向量执行检索
# 2. 收集所有结果，按 document_id 分组
# 3. 计算融合得分：final_score = Σ(weight_i * score_i)
# 4. 按融合得分排序，返回 Top-K
```

---

## 🔧 实现提示

### 提示 1: 异步批量查询

```python
import asyncio

# 并发执行多个查询
tasks = [
    client.query_points(
        collection_name=collection_name,
        query=query.vector,
        limit=limit * 2,  # 多取一些结果用于融合
    )
    for query in queries
]
results = await asyncio.gather(*tasks)
```

### 提示 2: 结果融合算法

```python
from collections import defaultdict

# 按 document_id 分组
scores_by_id: defaultdict[int, list[float]] = defaultdict(list)

for i, result in enumerate(results):
    weight = queries[i].weight
    for hit in result.points:
        if hit.score is not None:
            scores_by_id[hit.id].append(hit.score * weight)

# 计算融合得分
fused_scores = {
    doc_id: sum(scores)
    for doc_id, scores in scores_by_id.items()
}
```

### 提示 3: 类型安全

确保所有函数都有完整的类型注解：

```python
from qdrant_client.models import ScoredPoint

async def my_search(...) -> list[ScoredPoint]:
    query_response = await client.query_points(...)
    results: list[ScoredPoint] = query_response.points
    return results
```

---

## ✅ 验收标准

### 功能要求

**场景 1: 模糊搜索**

- [ ] 正确实现相似度阈值过滤
- [ ] 返回结果数量 <= limit
- [ ] 所有结果的 score >= threshold

**场景 2: 元数据过滤**

- [ ] 正确实现 AND 条件（must）
- [ ] 正确实现 OR 条件（should）
- [ ] 正确实现范围查询（Range）
- [ ] 组合向量相似度 + 元数据过滤

**场景 3: 相似度排序**

- [ ] 正确实现多查询并发执行
- [ ] 正确实现得分融合算法
- [ ] 验证权重总和为 1.0
- [ ] 按融合得分正确排序

### 代码质量

- [ ] 通过 `mypy --strict` 检查
- [ ] 通过 `ruff check` 检查
- [ ] 完整的异常处理
- [ ] 完整的类型注解

### Jupyter 环境测试

在 Jupyter Notebook 中运行以下测试：

```python
# Cell 1: 初始化
import asyncio
from qdrant_client import AsyncQdrantClient

client = AsyncQdrantClient(":memory:")
collection_name = "test_search"

# 准备测试数据
await prepare_test_data(client, collection_name)

# Cell 2: 测试场景 1
query_vector = [0.1] * 384
results = await fuzzy_search(
    client, collection_name, query_vector, threshold=0.7, limit=5
)
print(f"找到 {len(results)} 个结果")
assert all(r.score >= 0.7 for r in results if r.score is not None)

# Cell 3: 测试场景 2
results = await metadata_search(
    client, collection_name, query_vector,
    category="tutorial", min_year=2023, languages=["zh", "en"], limit=10
)
print(f"找到 {len(results)} 个符合条件的结果")

# Cell 4: 测试场景 3
queries = [
    WeightedQuery(vector=[0.1] * 384, weight=0.7),
    WeightedQuery(vector=[0.2] * 384, weight=0.3),
]
results = await similarity_ranking(client, collection_name, queries, limit=10)
print(f"融合后返回 {len(results)} 个结果")
```

---

## 💡 扩展挑战

1. **实现 Reciprocal Rank Fusion (RRF)**: 使用 RRF 算法替代简单加权
2. **实现 Hybrid Search**: 结合 BM25 稀疏检索 + 向量密集检索
3. **实现 Re-ranking**: 使用 Cross-Encoder 对初排结果进行重排序
4. **实现缓存机制**: 缓存热门查询的结果

---

## 📚 参考资源

- `demos/demo_03_semantic_search.py` - 高级检索示例
- Qdrant 官方文档: https://qdrant.tech/documentation/concepts/filtering/
- `core/vector_store.py` - 向量存储参考实现

---

**提交方式**: 将代码保存为 Jupyter Notebook `exercises/ex02_vector_search.ipynb`  
**验收命令**: `jupyter nbconvert --execute ex02_vector_search.ipynb`
