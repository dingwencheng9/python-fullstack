"""Solution 02: Vector Search 高级检索

from __future__ import annotations

实现三个特定检索场景：模糊搜索、元数据过滤、相似度排序。
严格遵循异步设计模式，生产级异常处理。
"""

import asyncio
from collections import defaultdict
from typing import NamedTuple

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
    Range,
    ScoredPoint,
)


class SearchError(Exception):
    """检索异常基类"""


class WeightedQuery(NamedTuple):
    """加权查询"""

    vector: list[float]
    weight: float


async def fuzzy_search(
    client: AsyncQdrantClient,
    collection_name: str,
    query_vector: list[float],
    threshold: float = 0.7,
    limit: int = 5,
) -> list[ScoredPoint]:
    """
    模糊搜索（基于相似度阈值）

    Args:
        client: Qdrant 客户端
        collection_name: 集合名称
        query_vector: 查询向量
        threshold: 相似度阈值
        limit: 返回结果数量

    Returns:
        符合阈值的检索结果

    Raises:
        ValueError: 参数无效时
        SearchError: 检索失败时
    """
    if threshold < 0 or threshold > 1:
        raise ValueError(f"threshold 必须在 [0, 1] 之间，当前: {threshold}")
    if limit <= 0:
        raise ValueError(f"limit 必须大于 0，当前: {limit}")

    try:
        query_response = await client.query_points(
            collection_name=collection_name,
            query=query_vector,
            score_threshold=threshold,
            limit=limit,
        )
        results: list[ScoredPoint] = query_response.points
        return results
    except Exception as e:
        raise SearchError(f"模糊搜索失败: {e}") from e


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

    Raises:
        ValueError: 参数无效时
        SearchError: 检索失败时
    """
    if limit <= 0:
        raise ValueError(f"limit 必须大于 0，当前: {limit}")
    if not languages:
        raise ValueError("languages 列表不能为空")

    try:
        filter_condition = Filter(
            must=[
                FieldCondition(key="category", match=MatchValue(value=category)),
                FieldCondition(key="publish_year", range=Range(gte=min_year)),
            ],
            should=[FieldCondition(key="language", match=MatchValue(value=lang)) for lang in languages],
        )

        query_response = await client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=filter_condition,
            limit=limit,
        )
        results: list[ScoredPoint] = query_response.points
        return results
    except Exception as e:
        raise SearchError(f"元数据过滤检索失败: {e}") from e


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
        SearchError: 检索失败时
    """
    if not queries:
        raise ValueError("查询列表不能为空")

    total_weight = sum(q.weight for q in queries)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"权重总和必须为 1.0，当前: {total_weight}")

    try:
        tasks = [
            client.query_points(
                collection_name=collection_name,
                query=query.vector,
                limit=limit * 2,
            )
            for query in queries
        ]
        results = await asyncio.gather(*tasks)

        scores_by_id: defaultdict[int, list[float]] = defaultdict(list)
        points_by_id: dict[int, ScoredPoint] = {}

        for i, result in enumerate(results):
            weight = queries[i].weight
            for hit in result.points:
                # 类型缩窄：确保 doc_id 是 int
                if not isinstance(hit.id, int):
                    continue
                doc_id: int = hit.id
                if hit.score is not None:
                    scores_by_id[doc_id].append(hit.score * weight)
                    if doc_id not in points_by_id:
                        points_by_id[doc_id] = hit

        fused_results: list[tuple[ScoredPoint, float]] = []
        for doc_id, scores in scores_by_id.items():
            fused_score = sum(scores)
            point = points_by_id[doc_id]
            fused_results.append((point, fused_score))

        fused_results.sort(key=lambda x: x[1], reverse=True)
        return fused_results[:limit]

    except Exception as e:
        raise SearchError(f"相似度排序失败: {e}") from e


async def main() -> None:
    """主测试函数"""
    print("Solution 02: Vector Search - 已就绪")


if __name__ == "__main__":
    asyncio.run(main())
