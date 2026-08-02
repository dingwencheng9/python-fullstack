"""L47 RAG 检索管道测试：使用 mock 向量数据库避免网络依赖。"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock

import pytest

pytest.importorskip("qdrant_client", reason="qdrant-client 未安装")

from qdrant_client.models import ScoredPoint

SOLUTIONS_DIR = Path(__file__).parent.parent / "solutions"


def _load_solution(module_name: str, filename: str) -> ModuleType:
    """动态加载 solutions 中的参考答案模块。"""
    module_path = SOLUTIONS_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


embedding_module = _load_solution("l43_sol01_embedding_pipeline", "sol01_embedding_pipeline.py")
search_module = _load_solution("l43_sol02_vector_search", "sol02_vector_search.py")
TextChunker = embedding_module.TextChunker
EmbeddingPipeline = embedding_module.EmbeddingPipeline
StorageError = embedding_module.StorageError
SearchError = search_module.SearchError
WeightedQuery = search_module.WeightedQuery
fuzzy_search = search_module.fuzzy_search
metadata_search = search_module.metadata_search
similarity_ranking = search_module.similarity_ranking


@pytest.mark.parametrize(
    ("chunk_size", "overlap", "text", "expected_chunks"),
    [
        (5, 0, "abcdefghij", ["abcde", "fghij"]),
        (5, 2, "abcdefgh", ["abcde", "defgh", "gh"]),
    ],
)
@pytest.mark.asyncio
async def test_text_chunker_splits_with_expected_overlap(
    chunk_size: int,
    overlap: int,
    text: str,
    expected_chunks: list[str],
) -> None:
    """参数化验证文本分块大小与重叠边界。"""
    chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)

    chunks = await chunker.chunk(text)

    assert chunks == expected_chunks


@pytest.mark.parametrize(
    ("chunk_size", "overlap", "message"),
    [
        (0, 0, "chunk_size 必须大于 0"),
        (10, -1, "overlap 必须大于等于 0"),
        (10, 10, "必须小于 chunk_size"),
    ],
)
def test_text_chunker_rejects_invalid_boundaries(
    chunk_size: int,
    overlap: int,
    message: str,
) -> None:
    """参数化验证分块器构造参数边界异常。"""
    with pytest.raises(ValueError, match=message):
        TextChunker(chunk_size=chunk_size, overlap=overlap)


@pytest.mark.asyncio
async def test_embedding_pipeline_uses_mock_vector_db_for_storage() -> None:
    """EmbeddingPipeline 应将分块向量写入 mock 向量数据库。"""
    client = AsyncMock()
    client.recreate_collection = AsyncMock()
    client.upsert = AsyncMock()
    pipeline = EmbeddingPipeline(
        qdrant_client=client,
        collection_name="mock_collection",
        vector_size=8,
        chunk_size=4,
        overlap=0,
    )

    count = await pipeline.process_document("abcdefghijkl", metadata={"source": "unit"})

    assert count == 3
    client.recreate_collection.assert_awaited_once()
    client.upsert.assert_awaited_once()
    points = client.upsert.await_args.kwargs["points"]
    assert [point.payload["chunk_index"] for point in points] == [0, 1, 2]
    assert all(len(point.vector) == 8 for point in points)


@pytest.mark.asyncio
async def test_embedding_pipeline_wraps_vector_db_storage_error() -> None:
    """mock 向量数据库写入失败时应包装为 StorageError。"""
    client = AsyncMock()
    client.recreate_collection = AsyncMock()
    client.upsert = AsyncMock(side_effect=RuntimeError("disk full"))
    pipeline = EmbeddingPipeline(client, "mock_collection", vector_size=4, chunk_size=4, overlap=0)

    with pytest.raises(StorageError, match="向量存储失败"):
        await pipeline.process_document("abcdefgh")


@pytest.mark.parametrize(
    ("threshold", "limit"),
    [(0.5, 1), (0.8, 3)],
)
@pytest.mark.asyncio
async def test_fuzzy_search_passes_threshold_and_limit_to_vector_db(
    threshold: float,
    limit: int,
) -> None:
    """参数化验证模糊检索会传递阈值和 Top-K 限制。"""
    point = ScoredPoint(id=1, version=1, score=0.9, payload={"text": "python"}, vector=None)
    client = AsyncMock()
    client.query_points = AsyncMock(return_value=SimpleNamespace(points=[point]))

    results = await fuzzy_search(client, "docs", [0.1, 0.2], threshold=threshold, limit=limit)

    assert results == [point]
    client.query_points.assert_awaited_once_with(
        collection_name="docs",
        query=[0.1, 0.2],
        score_threshold=threshold,
        limit=limit,
    )


@pytest.mark.asyncio
async def test_fuzzy_search_rejects_invalid_limit_boundary() -> None:
    """Top-K limit 为 0 时应抛出 ValueError。"""
    with pytest.raises(ValueError, match="limit 必须大于 0"):
        await fuzzy_search(AsyncMock(), "docs", [0.1], limit=0)


@pytest.mark.asyncio
async def test_metadata_search_rejects_empty_languages_boundary() -> None:
    """元数据检索语言过滤列表为空时应抛出 ValueError。"""
    with pytest.raises(ValueError, match="languages 列表不能为空"):
        await metadata_search(AsyncMock(), "docs", [0.1], "tech", 2024, [])


@pytest.mark.asyncio
async def test_similarity_ranking_fuses_weighted_query_scores() -> None:
    """多查询融合排序应按加权分数降序返回结果。"""
    first_points = [
        ScoredPoint(id=1, version=1, score=0.8, payload={}, vector=None),
        ScoredPoint(id=2, version=1, score=0.4, payload={}, vector=None),
    ]
    second_points = [
        ScoredPoint(id=1, version=1, score=0.2, payload={}, vector=None),
        ScoredPoint(id=2, version=1, score=1.0, payload={}, vector=None),
    ]
    client = AsyncMock()
    client.query_points = AsyncMock(side_effect=[SimpleNamespace(points=first_points), SimpleNamespace(points=second_points)])
    queries = [WeightedQuery([1.0, 0.0], 0.25), WeightedQuery([0.0, 1.0], 0.75)]

    results = await similarity_ranking(client, "docs", queries, limit=2)

    assert len(results) == 2
    assert results[0][0].id == 2
    assert results[0][1] == pytest.approx(0.85)
    assert results[1][0].id == 1
    assert results[1][1] == pytest.approx(0.35)


@pytest.mark.asyncio
async def test_similarity_ranking_rejects_empty_queries() -> None:
    """空查询列表应抛出 ValueError。"""
    with pytest.raises(ValueError, match="查询列表不能为空"):
        await similarity_ranking(AsyncMock(), "docs", [], limit=2)


@pytest.mark.asyncio
async def test_similarity_ranking_wraps_vector_db_error() -> None:
    """mock 向量数据库异常应包装为 SearchError。"""
    client = AsyncMock()
    client.query_points = AsyncMock(side_effect=RuntimeError("timeout"))
    queries = [WeightedQuery([1.0], 1.0)]

    with pytest.raises(SearchError, match="相似度排序失败"):
        await similarity_ranking(client, "docs", queries, limit=2)
