"""

from __future__ import annotations

L14-L16 异步数据分析管道 - 核心实战代码
=========================================

本模块展示异步数据工程的五大核心能力：
1. run_in_executor 卸载 CPU 密集型任务
2. Pandas vs Polars 性能对比
3. 装饰器缓存可视化结果（呼应 L05）
4. 与 L12 RAG Agent 深度集成
5. OpenTelemetry 追踪数据处理耗时

架构设计：
---------
API → run_in_executor(Pandas/Polars) → 缓存 → RAG 上下文 → 响应

对标：
-----
- 呼应 L05 装饰器模式
- 呼应 L09 OpenTelemetry 追踪
- 呼应 L12 RAG Agent 集成

作者：Python 3.13 全栈课程
"""

import asyncio
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any, Literal

import numpy as np
import pandas as pd
import polars as pl

# OpenTelemetry 集成
from opentelemetry import trace
from pydantic import BaseModel, Field

tracer = trace.get_tracer(__name__)


# ============================================================
# 1. 装饰器缓存层（呼应 L05）
# ============================================================


def timed_cache(maxsize: int = 128, ttl_seconds: float = 300):
    """
    带 TTL 的缓存装饰器

    **使用场景**: 缓存数据处理结果，避免重复计算
    """

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = hashlib.md5(str((args, kwargs)).encode()).hexdigest()

            # 检查缓存
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    print(f"✅ Cache HIT: {func.__name__}")
                    return result

            # 执行函数
            result = func(*args, **kwargs)

            # 写入缓存
            if len(cache) >= maxsize:
                oldest = min(cache.keys(), key=lambda k: cache[k][1])
                del cache[oldest]

            cache[key] = (result, now)
            print(f"❌ Cache MISS: {func.__name__}")

            return result

        return wrapper

    return decorator


# ============================================================
# 2. 数据模型
# ============================================================


class DataProcessRequest(BaseModel):
    """数据处理请求"""

    operations: list[str] = Field(default=["describe", "null_check"])
    engine: Literal["pandas", "polars"] = Field(default="pandas")


class AnalyticsResult(BaseModel):
    """分析结果"""

    summary_stats: dict[str, Any]
    insights: list[str]
    processing_time_ms: float
    engine: str
    rows: int
    columns: int


# ============================================================
# 3. 异步数据分析服务（核心）
# ============================================================


class AsyncAnalyticsService:
    """
    异步数据分析服务

    **核心原则**: 禁止阻塞 Event Loop
    - 所有 CPU 密集型任务使用 run_in_executor
    """

    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_pandas_async(
        self,
        df: pd.DataFrame,
        operations: list[str],
    ) -> AnalyticsResult:
        """
        异步处理 Pandas DataFrame

        **关键**: 使用 run_in_executor 避免阻塞
        """
        with tracer.start_as_current_span("pandas_process") as span:
            span.set_attribute("rows", len(df))
            span.set_attribute("columns", len(df.columns))

            # 获取事件循环
            loop = asyncio.get_event_loop()

            # CPU 密集型任务在线程池执行（关键！）
            result = await loop.run_in_executor(
                self.executor,
                self._process_pandas_sync,
                df,
                operations,
            )

            span.set_attribute("processing_time_ms", result.processing_time_ms)

            return result

    @timed_cache(maxsize=128, ttl_seconds=300)
    def _process_pandas_sync(
        self,
        df: pd.DataFrame,
        operations: list[str],
    ) -> AnalyticsResult:
        """
        同步 Pandas 处理（在线程池执行）

        **装饰器缓存**: 避免重复计算
        """
        start = time.perf_counter()

        summary_stats = {}
        insights = []

        # 操作 1: 统计摘要
        if "describe" in operations:
            summary_stats["describe"] = df.describe().to_dict()

        # 操作 2: 缺失值检查
        if "null_check" in operations:
            null_counts = df.isnull().sum()
            if null_counts.sum() > 0:
                insights.append(f"发现缺失值: {null_counts[null_counts > 0].to_dict()}")

        # 操作 3: 异常值检测
        if "outlier_detection" in operations:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                if outliers > 0:
                    insights.append(f"{col}: 发现 {outliers} 个异常值")

        elapsed_ms = (time.perf_counter() - start) * 1000

        return AnalyticsResult(
            summary_stats=summary_stats,
            insights=insights,
            processing_time_ms=elapsed_ms,
            engine="pandas",
            rows=len(df),
            columns=len(df.columns),
        )

    async def process_polars_async(
        self,
        df: pl.DataFrame,
        operations: list[str],
    ) -> AnalyticsResult:
        """
        异步处理 Polars DataFrame

        **Polars 优势**: 更快的内存操作
        """
        with tracer.start_as_current_span("polars_process") as span:
            span.set_attribute("rows", len(df))
            span.set_attribute("columns", len(df.columns))

            loop = asyncio.get_event_loop()

            result = await loop.run_in_executor(
                self.executor,
                self._process_polars_sync,
                df,
                operations,
            )

            span.set_attribute("processing_time_ms", result.processing_time_ms)

            return result

    @timed_cache(maxsize=128, ttl_seconds=300)
    def _process_polars_sync(
        self,
        df: pl.DataFrame,
        operations: list[str],
    ) -> AnalyticsResult:
        """同步 Polars 处理"""
        start = time.perf_counter()

        summary_stats = {}
        insights = []

        if "describe" in operations:
            summary_stats["describe"] = df.describe().to_dict()

        if "null_check" in operations:
            null_counts = df.null_count()
            if null_counts.sum_horizontal()[0] > 0:
                insights.append("发现缺失值（Polars）")

        elapsed_ms = (time.perf_counter() - start) * 1000

        return AnalyticsResult(
            summary_stats=summary_stats,
            insights=insights,
            processing_time_ms=elapsed_ms,
            engine="polars",
            rows=len(df),
            columns=len(df.columns),
        )

    async def close(self):
        """关闭线程池"""
        self.executor.shutdown(wait=True)


# ============================================================
# 4. RAG 集成桥（与 L12 深度集成）
# ============================================================


class RAGIntegrationBridge:
    """
    RAG 集成桥

    **核心**: 将数据分析结果转换为 RAG 上下文
    """

    def format_as_rag_context(self, result: AnalyticsResult) -> str:
        """
        格式化为 RAG 上下文

        **使用场景**: 输入到 L12 RAG Agent
        """
        context_parts = [
            f"# 数据分析结果（引擎: {result.engine}）\n",
            f"**数据规模**: {result.rows} 行 × {result.columns} 列",
            f"**处理时间**: {result.processing_time_ms:.2f}ms\n",
            "## 统计摘要",
        ]

        # 添加统计数据
        if "describe" in result.summary_stats:
            context_parts.append("### 数值列统计")
            for col, stats in result.summary_stats["describe"].items():
                context_parts.append(f"**{col}**:")
                for stat_name, value in stats.items():
                    context_parts.append(f"  - {stat_name}: {value:.2f}")

        # 添加洞察
        if result.insights:
            context_parts.append("\n## 关键发现")
            for insight in result.insights:
                context_parts.append(f"- {insight}")

        return "\n".join(context_parts)

    async def query_with_analytics(
        self,
        query: str,
        analytics_result: AnalyticsResult,
    ) -> dict[str, str]:
        """
        使用数据分析结果查询 RAG

        **扩展集成**: 调用后续 Stage 6 RAG Workflow
        """
        with tracer.start_as_current_span("rag_query") as span:
            span.set_attribute("query", query)

            # 构建上下文
            context = self.format_as_rag_context(analytics_result)

            # 这里可在 Stage 6 课程中接入 RAG Workflow
            # response = await rag_workflow.execute(query=query, context=context)

            # 模拟响应
            mock_response = f"基于数据分析结果，{query} 的答案是..."

            span.add_event("rag_response_generated")

            return {
                "query": query,
                "response": mock_response,
                "context": context,
            }


# ============================================================
# 5. 性能基准测试（Pandas vs Polars）
# ============================================================


async def benchmark_engines(df_pandas: pd.DataFrame, df_polars: pl.DataFrame):
    """
    性能基准测试：Pandas vs Polars

    **目标**: 展示 Polars 在大数据集上的优势
    """
    print("\n" + "=" * 80)
    print("性能基准测试：Pandas vs Polars")
    print("=" * 80)

    service = AsyncAnalyticsService()

    operations = ["describe", "null_check", "outlier_detection"]

    # 测试 Pandas
    print("\n📊 测试 Pandas...")
    start = time.time()
    await service.process_pandas_async(df_pandas, operations)
    pandas_time = time.time() - start

    # 测试 Polars
    print("\n⚡ 测试 Polars...")
    start = time.time()
    await service.process_polars_async(df_polars, operations)
    polars_time = time.time() - start

    # 对比结果
    print("\n📈 性能对比:")
    print(f"  Pandas: {pandas_time * 1000:.2f}ms")
    print(f"  Polars: {polars_time * 1000:.2f}ms")
    print(f"  加速比: {pandas_time / polars_time:.2f}x")

    await service.close()


# ============================================================
# 6. 完整示例：FastAPI 集成
# ============================================================

import io

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="异步数据分析 API")
analytics_service = AsyncAnalyticsService()
rag_bridge = RAGIntegrationBridge()


@app.post("/api/analytics/process")
async def process_data(file: UploadFile = File(...), request: DataProcessRequest = DataProcessRequest()):
    """
    处理上传的 CSV 数据

    **核心**: 使用 run_in_executor 避免阻塞 Event Loop
    """
    with tracer.start_as_current_span("api_process_data") as span:
        span.set_attribute("filename", file.filename)
        span.set_attribute("engine", request.engine)

        # 读取文件（I/O 操作，异步）
        contents = await file.read()

        # 解析 CSV（CPU 密集型，使用 executor）
        loop = asyncio.get_event_loop()

        if request.engine == "pandas":
            df = await loop.run_in_executor(None, pd.read_csv, io.BytesIO(contents))
            result = await analytics_service.process_pandas_async(df, request.operations)

        else:  # polars
            df = await loop.run_in_executor(None, pl.read_csv, io.BytesIO(contents))
            result = await analytics_service.process_polars_async(df, request.operations)

        span.set_attribute("rows", result.rows)
        span.set_attribute("processing_time_ms", result.processing_time_ms)

        return JSONResponse(content=result.model_dump())


@app.post("/api/analytics/query")
async def query_with_data(query: str, file: UploadFile = File(...)):
    """
    数据分析 + RAG 查询（深度集成 L12）

    **流程**:
    1. 异步处理数据
    2. 格式化为 RAG 上下文
    3. 调用 RAG Agent
    """
    with tracer.start_as_current_span("api_query_with_data") as span:
        span.set_attribute("query", query)

        # 读取并处理数据
        contents = await file.read()
        loop = asyncio.get_event_loop()

        df = await loop.run_in_executor(None, pd.read_csv, io.BytesIO(contents))

        # 数据分析
        analytics_result = await analytics_service.process_pandas_async(df, ["describe", "null_check"])

        # RAG 集成
        rag_response = await rag_bridge.query_with_analytics(query, analytics_result)

        span.add_event("query_completed")

        return JSONResponse(
            content={
                "analytics": analytics_result.model_dump(),
                "rag_response": rag_response,
            }
        )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "async-analytics"}


# ============================================================
# 7. 主程序演示
# ============================================================


async def main():
    """主函数：演示完整流程"""
    print("=" * 80)
    print("L14-L16 异步数据分析管道 - 核心实战")
    print("=" * 80 + "\n")

    # 创建测试数据
    print("📊 生成测试数据...")
    np.random.seed(42)
    n_rows = 10000

    data = {
        "id": range(n_rows),
        "value": np.random.randn(n_rows) * 100 + 500,
        "category": np.random.choice(["A", "B", "C"], n_rows),
        "timestamp": pd.date_range("2024-01-01", periods=n_rows, freq="H"),
    }

    df_pandas = pd.DataFrame(data)
    df_polars = pl.DataFrame(data)

    print(f"  数据规模: {n_rows} 行 × {len(data)} 列")

    # 示例 1: 异步 Pandas 处理
    print("\n" + "=" * 80)
    print("示例 1: 异步 Pandas 处理（run_in_executor）")
    print("=" * 80)

    service = AsyncAnalyticsService()

    result = await service.process_pandas_async(df_pandas, ["describe", "null_check", "outlier_detection"])

    print("\n✅ 处理完成")
    print(f"  引擎: {result.engine}")
    print(f"  耗时: {result.processing_time_ms:.2f}ms")
    print(f"  洞察: {len(result.insights)} 条")
    for insight in result.insights:
        print(f"    - {insight}")

    # 示例 2: 性能基准测试
    print("\n" + "=" * 80)
    print("示例 2: Pandas vs Polars 性能对比")
    print("=" * 80)

    await benchmark_engines(df_pandas, df_polars)

    # 示例 3: RAG 集成
    print("\n" + "=" * 80)
    print("示例 3: 数据分析 + RAG 查询（L12 集成）")
    print("=" * 80)

    bridge = RAGIntegrationBridge()

    rag_response = await bridge.query_with_analytics("这些数据的主要趋势是什么？", result)

    print("\n✅ RAG 响应:")
    print(f"  查询: {rag_response['query']}")
    print(f"  答案: {rag_response['response']}")
    print("\n📄 RAG 上下文:")
    print(rag_response["context"][:500] + "...")

    await service.close()

    print("\n" + "=" * 80)
    print("演示完成")
    print("=" * 80)

    print("\n💡 核心要点:")
    print("  1. ✅ 使用 run_in_executor 避免阻塞 Event Loop")
    print("  2. ✅ 装饰器缓存避免重复计算（呼应 L05）")
    print("  3. ✅ Polars 提供 2-10x 性能提升")
    print("  4. ✅ 数据分析结果作为 RAG 上下文（L12 集成）")
    print("  5. ✅ OpenTelemetry 追踪完整链路")


if __name__ == "__main__":
    asyncio.run(main())
