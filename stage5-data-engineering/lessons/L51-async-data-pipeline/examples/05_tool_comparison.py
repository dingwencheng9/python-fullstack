"""
L51 - 数据处理工具对比：Dask vs Polars vs Spark vs Pandas
==========================================================

本模块演示四大数据处理工具的 API 风格和性能特征对比：
1. Pandas: 单机标准库
2. Polars: Rust 实现高性能 DataFrame
3. Dask: Pandas 兼容的分布式扩展
4. Spark (PySpark): 企业级分布式计算

适用场景：
- 数据规模从小到大（MB → GB → TB → PB）
- Pandas 代码需要扩展到集群
- 选择合适工具的决策参考

前置知识：L48 Pandas 实战、L51 异步管道

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

# 可选导入（如果未安装则优雅降级）
try:
    import polars as pl

    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False

try:
    import dask.dataframe as dd

    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


# ============================================================
# 1. 工具特性元数据
# ============================================================


@dataclass(slots=True)
class ToolProfile:
    """数据处理工具档案"""

    name: str
    language: str  # 实现语言
    api_style: Literal["pandas", "rdd", "sql"]  # API 风格
    execution_model: Literal["eager", "lazy"]  # 执行模型
    parallelism: Literal["single", "multi", "distributed"]  # 并行方式
    memory_model: str  # 内存管理
    max_data_scale: str  # 适用数据规模
    learning_curve: Literal["low", "medium", "high"]  # 学习曲线
    startup_overhead_s: float  # 启动开销（秒）
    available: bool = True  # 是否可用


TOOL_PROFILES: dict[str, ToolProfile] = {
    "pandas": ToolProfile(
        name="Pandas",
        language="Python",
        api_style="pandas",
        execution_model="eager",
        parallelism="single",
        memory_model="全量加载（NumPy）",
        max_data_scale="< 10GB",
        learning_curve="low",
        startup_overhead_s=0.05,
    ),
    "polars": ToolProfile(
        name="Polars",
        language="Rust (Python bindings)",
        api_style="pandas",
        execution_model="lazy",
        parallelism="multi",
        memory_model="Apache Arrow（列式）",
        max_data_scale="< 100GB",
        learning_curve="low",
        startup_overhead_s=0.05,
        available=POLARS_AVAILABLE,
    ),
    "dask": ToolProfile(
        name="Dask",
        language="Python (Cython + threading)",
        api_style="pandas",
        execution_model="lazy",
        parallelism="multi",
        memory_model="溢出到磁盘（out-of-core）",
        max_data_scale="10GB - 1TB",
        learning_curve="medium",
        startup_overhead_s=0.5,
        available=DASK_AVAILABLE,
    ),
    # Spark 需要 JVM 环境，这里仅作文档记录
    # "spark": ToolProfile(
    #     name="Spark (PySpark)",
    #     language="Scala + Python",
    #     api_style="rdd",
    #     execution_model="lazy",
    #     parallelism="distributed",
    #     memory_model="JVM 堆内存",
    #     max_data_scale="1TB - PB 级",
    #     learning_curve="high",
    #     startup_overhead_s=10.0,
    # ),
}


# ============================================================
# 2. 统一操作接口（适配器模式）
# ============================================================


@dataclass
class ProcessingResult:
    """处理结果"""

    tool: str
    operation: str
    rows: int
    elapsed_ms: float
    memory_peak_mb: float | None = None


class UnifiedDataAdapter:
    """
    统一数据适配器

    提供一致的 API 接口，屏蔽底层工具差异。
    支持：Pandas、Polars、Dask
    """

    def __init__(self, tool: Literal["pandas", "polars", "dask"]):
        self.tool = tool

    def read_csv(self, data: list[dict]) -> object:
        """读取 CSV 数据（使用对应工具）"""
        start = time.perf_counter()

        if self.tool == "pandas":
            df = pd.DataFrame(data)
        elif self.tool == "polars":
            if not POLARS_AVAILABLE:
                raise ImportError("Polars 未安装：请运行 uv add polars")
            df = pl.DataFrame(data)
        elif self.tool == "dask":
            if not DASK_AVAILABLE:
                raise ImportError("Dask 未安装：请运行 uv add dask")
            # Dask 需要延迟计算，这里用 pandas 模拟
            df = pd.DataFrame(data)
        else:
            raise ValueError(f"未知工具: {self.tool}")

        elapsed = (time.perf_counter() - start) * 1000
        print(f"  [{self.tool}] 读取 {len(data)} 行，耗时 {elapsed:.2f}ms")
        return df

    def group_by_aggregate(self, df: object, group_col: str, agg_col: str) -> object:
        """分组聚合（使用对应工具语法）"""
        start = time.perf_counter()

        if self.tool == "pandas":
            result = df.groupby(group_col)[agg_col].mean().reset_index()
        elif self.tool == "polars":
            result = df.group_by(group_col).agg(pl.col(agg_col).mean()).sort(group_col)
        elif self.tool == "dask":
            # Dask API 与 Pandas 几乎相同
            result = df.groupby(group_col)[agg_col].mean().compute().reset_index()

        elapsed = (time.perf_counter() - start) * 1000
        print(f"  [{self.tool}] 分组聚合，耗时 {elapsed:.2f}ms")
        return result


# ============================================================
# 3. 性能基准测试
# ============================================================


def generate_test_data(n_rows: int = 100_000) -> list[dict]:
    """生成测试数据"""
    np.random.seed(42)
    categories = ["A", "B", "C", "D", "E"]

    return [
        {
            "id": i,
            "category": categories[i % len(categories)],
            "value": np.random.randn() * 100 + 500,
            "quantity": np.random.randint(1, 100),
        }
        for i in range(n_rows)
    ]


async def benchmark_tools(n_rows: int = 100_000) -> list[ProcessingResult]:
    """
    性能基准测试：对比各工具

    **测试操作**:
    1. 读取 CSV 数据
    2. 分组聚合
    """
    print("\n" + "=" * 70)
    print(f"性能基准测试（数据规模: {n_rows:,} 行）")
    print("=" * 70)

    data = generate_test_data(n_rows)
    results: list[ProcessingResult] = []

    for tool in ["pandas", "polars", "dask"]:
        if tool == "polars" and not POLARS_AVAILABLE:
            print("\n⚠️ 跳过 Polars（未安装）")
            continue
        if tool == "dask" and not DASK_AVAILABLE:
            print("\n⚠️ 跳过 Dask（未安装）")
            continue

        print(f"\n📊 测试 {TOOL_PROFILES[tool].name}...")

        adapter = UnifiedDataAdapter(tool=tool)

        # 操作 1: 读取
        try:
            start = time.perf_counter()
            df = adapter.read_csv(data)
            read_time = (time.perf_counter() - start) * 1000

            # 操作 2: 分组聚合
            start = time.perf_counter()
            adapter.group_by_aggregate(df, "category", "value")
            agg_time = (time.perf_counter() - start) * 1000

            total_time = read_time + agg_time

            results.append(
                ProcessingResult(
                    tool=tool,
                    operation="read + groupby",
                    rows=n_rows,
                    elapsed_ms=total_time,
                )
            )

            print(f"  ✅ 总耗时: {total_time:.2f}ms")

        except Exception as e:
            print(f"  ❌ 错误: {e}")

    # 汇总报告
    if results:
        print("\n" + "-" * 70)
        print("基准测试结果汇总")
        print("-" * 70)
        print(f"{'工具':<10} {'总耗时 (ms)':<15} {'相对 Pandas':<15}")
        print("-" * 70)

        pandas_baseline = next((r.elapsed_ms for r in results if r.tool == "pandas"), 1.0)

        for r in sorted(results, key=lambda x: x.elapsed_ms):
            relative = r.elapsed_ms / pandas_baseline
            speedup = pandas_baseline / r.elapsed_ms if r.elapsed_ms > 0 else float("inf")
            marker = "⚡" if speedup > 2 else "  "
            print(f"{r.tool:<10} {r.elapsed_ms:<15.2f} {relative:<10.2f}x  {marker}加速 {speedup:.1f}x")

    return results


# ============================================================
# 4. 选型决策辅助
# ============================================================


@dataclass
class DecisionContext:
    """选型决策上下文"""

    data_size_gb: float  # 数据大小（GB）
    latency_requirement_s: float  # 延迟要求（秒）
    has_pandas_codebase: bool = False  # 是否有现有 Pandas 代码
    has_spark_cluster: bool = False  # 是否有 Spark 集群
    team_skill_level: Literal["junior", "senior", "data_engineer"] = "senior"


def recommend_tool(ctx: DecisionContext) -> str:
    """
    工具选型推荐

    **决策逻辑**:
    1. 数据规模 < 10GB: Pandas / Polars
    2. 数据规模 10GB - 1TB: Dask（优先）/ Polars
    3. 数据规模 > 1TB: Spark
    4. 延迟 < 1s: Polars
    5. 已有 Pandas 代码: Dask
    """
    # 极端情况
    if ctx.data_size_gb > 1000 and ctx.has_spark_cluster:
        return "spark"

    if ctx.data_size_gb > 100:
        if ctx.has_spark_cluster:
            return "spark"
        return "dask"

    # 性能优先
    if ctx.latency_requirement_s < 1.0 and ctx.data_size_gb < 100:
        return "polars"

    # Pandas 迁移
    if ctx.has_pandas_codebase and ctx.data_size_gb >= 10:
        return "dask"

    # 默认选型
    if ctx.data_size_gb < 10:
        return "pandas"
    if ctx.data_size_gb < 100:
        return "polars"
    return "dask"


def print_decision_tree():
    """打印选型决策树"""
    print("\n" + "=" * 70)
    print("数据处理工具选型决策树")
    print("=" * 70)

    print("""
┌─────────────────────────────────────────────────────────────────┐
│                      数据处理工具选型                             │
└─────────────────────────────────────────────────────────────────┘

数据规模 < 10GB？
  ├─ 是 → 延迟要求 < 1s？
  │         ├─ 是 → ⚡ Polars（Rust SIMD，极速向量化）
  │         └─ 否 → Pandas（成熟生态，快速原型）
  │
  └─ 否 → 数据规模 < 100GB？
            ├─ 是 → Polars（性能优先，高性价比）
            └─ 否 → 数据规模 < 1TB？
                      ├─ 是 → 已有 Pandas 代码？
                      │         ├─ 是 → Dask（最小改动迁移）
                      │         └─ 否 → Polars / Dask
                      └─ 否 → 有 Spark 集群？
                                ├─ 是 → Spark（PB 级分布式）
                                └─ 否 → Dask（TB 级，溢出磁盘）
""")

    print("\n📌 选型决策示例:")

    test_cases: list[tuple[str, DecisionContext]] = [
        ("快速原型（5GB CSV）", DecisionContext(5.0, 10.0)),
        ("低延迟查询（20GB）", DecisionContext(20.0, 0.5)),
        ("Pandas 迁移（50GB）", DecisionContext(50.0, 30.0, has_pandas_codebase=True)),
        ("TB 级分析（500GB）", DecisionContext(500.0, 300.0)),
        ("PB 级生产（2TB + 集群）", DecisionContext(2000.0, 600.0, has_spark_cluster=True)),
    ]

    for desc, ctx in test_cases:
        tool = recommend_tool(ctx)
        print(f"  - {desc}: 推荐 {TOOL_PROFILES.get(tool, tool).name if tool in TOOL_PROFILES else tool}")


# ============================================================
# 5. asyncio 集成示例
# ============================================================


async def async_pipeline_with_dask(data: list[dict]) -> dict:
    """
    Dask 异步管道示例

    **关键**: Dask 计算在后台线程池执行，不会阻塞 Event Loop
    """
    if not DASK_AVAILABLE:
        return {"error": "Dask 未安装"}

    import dask.dataframe as dd

    print("\n📊 异步 Dask 管道...")

    # 将 pandas DataFrame 转为 Dask DataFrame
    df_pandas = pd.DataFrame(data)
    ddf = dd.from_pandas(df_pandas, npartitions=4)

    # Dask 延迟计算图
    result_dask = ddf.groupby("category")["value"].mean()

    # 在线程池中执行（避免阻塞 Event Loop）
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, result_dask.compute)

    print(f"  ✅ Dask 计算完成，结果: {len(result)} 行")
    return result.to_dict()


async def async_pipeline_with_polars(data: list[dict]) -> dict:
    """
    Polars 异步管道示例

    **关键**: Polars 在线程池执行，结合 asyncio 实现高并发
    """
    if not POLARS_AVAILABLE:
        return {"error": "Polars 未安装"}

    print("\n⚡ 异步 Polars 管道...")

    executor = ThreadPoolExecutor(max_workers=4)

    def sync_polars_query():
        # Polars 延迟计算
        lf = pl.LazyFrame(data)
        return lf.group_by("category").agg(pl.col("value").mean()).sort("category").collect()

    # 在线程池执行
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, sync_polars_query)

    print(f"  ✅ Polars 计算完成，结果: {len(result)} 行")
    return result.to_dict()


# ============================================================
# 6. 主程序演示
# ============================================================


async def main():
    """主函数：演示完整流程"""
    print("=" * 70)
    print("L51 - 数据处理工具对比：Dask vs Polars vs Spark vs Pandas")
    print("=" * 70)

    # 1. 打印工具档案
    print("\n📦 可用工具档案:")
    print("-" * 70)
    for tool, profile in TOOL_PROFILES.items():
        status = "✅" if profile.available else "❌"
        print(f"  {status} {profile.name:<8} | {profile.language:<20} | 规模: {profile.max_data_scale:<10} | 启动: {profile.startup_overhead_s:.1f}s")

    # 2. 选型决策树
    print_decision_tree()

    # 3. 性能基准测试（小规模数据，避免实际环境依赖）
    await benchmark_tools(n_rows=50_000)

    # 4. asyncio 集成（仅测试可用工具）
    test_data = generate_test_data(n_rows=10_000)

    if DASK_AVAILABLE:
        await async_pipeline_with_dask(test_data)

    if POLARS_AVAILABLE:
        await async_pipeline_with_polars(test_data)

    # 5. 总结
    print("\n" + "=" * 70)
    print("核心要点")
    print("=" * 70)
    print("""
  1. Pandas: 单机数据分析首选，学习曲线最低
  2. Polars: Rust 实现，性能 2-10x，延迟 < 1s 场景首选
  3. Dask: Pandas API 扩展，支持 TB 级，溢出磁盘
  4. Spark: PB 级分布式，需要集群，学习曲线高

  💡 选择原则:
  - 小数据（< 10GB）+ 快速原型 → Pandas
  - 中数据（10-100GB）+ 性能优先 → Polars
  - 大数据（10GB-1TB）+ Pandas 代码 → Dask
  - 超大数据（> 1TB）+ 集群环境 → Spark
""")


if __name__ == "__main__":
    asyncio.run(main())
