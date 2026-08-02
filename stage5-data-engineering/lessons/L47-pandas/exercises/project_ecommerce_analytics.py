"""练习项目: 电商数据分析系统

from __future__ import annotations

业务场景:
某电商平台需要对 800 万订单数据进行 RFM 分析和用户分层,用于精准营销。
系统要求在 8GB 内存限制下,30 秒内完成全流程分析。

业务需求:
1. 数据清洗: 处理缺失值、异常值、重复订单
2. RFM 分析: 计算最近购买时间(Recency)、购买频率(Frequency)、消费金额(Monetary)
3. 用户分层: 识别高价值用户、潜力用户、流失用户、低价值用户
4. 内存优化: 将内存占用从 8GB 降至 2GB 以下
5. 性能优化: 全流程处理时间 < 30 秒

评分标准:
- 功能正确性: 40 分（RFM 计算、用户分层准确）
- 性能表现: 30 分（处理时间 < 30 秒）
- 内存优化: 20 分（内存占用 < 2GB）
- 代码质量: 10 分（可读性、文档、异常处理）

技术提示:
- 使用向量化操作替代循环和 apply
- 使用 PyArrow 后端加速字符串和数值运算
- 使用 np.select 处理多条件分层逻辑
- 使用类型降级减少内存占用(int64 → int32/int16)
- 使用 category 类型优化重复率高的字符串列

RFM 分析说明:
- Recency (R): 最近一次购买距今天数（值越小越好）
  公式: (分析日期 - 最后购买日期).days

- Frequency (F): 购买频率（值越大越好）
  公式: 该用户的订单总数

- Monetary (M): 消费金额（值越大越好）
  公式: 该用户的订单总金额

用户分层标准:
- 高价值用户: R ≤ 30 天, F ≥ 10 次, M ≥ 10000 元
- 潜力用户: R ≤ 60 天, F ≥ 5 次, M ≥ 5000 元
- 流失用户: R > 180 天
- 低价值用户: 其他所有用户

性能要求:
- 数据加载: < 5 秒
- 数据清洗: < 3 秒
- RFM 计算: < 10 秒
- 用户分层: < 2 秒
- 总处理时间: < 30 秒

内存优化目标:
- 原始数据: ~8GB
- 优化后: < 2GB
- 节省比例: > 75%
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


class EcommerceAnalytics:
    """电商数据分析系统（学员实现）

    本类提供完整的电商数据分析流程,包括数据清洗、RFM 分析、用户分层和性能优化。

    Args:
        analysis_date: 分析基准日期（默认为今天）
        use_pyarrow: 是否使用 PyArrow 后端加速（推荐开启）
        memory_optimize: 是否启用激进内存优化（推荐开启）

    Attributes:
        analysis_date: 分析基准日期（用于计算 Recency）
        use_pyarrow: PyArrow 后端开关
        memory_optimize: 内存优化开关
        _performance_stats: 性能统计字典

    Example:
        >>> analytics = EcommerceAnalytics(
        ...     analysis_date=datetime(2024, 12, 31),
        ...     use_pyarrow=True,
        ...     memory_optimize=True
        ... )
        >>> df = analytics.load_orders("orders.csv")
        >>> df = analytics.calculate_rfm(df)
        >>> df = analytics.segment_customers(df)
        >>> df = analytics.optimize_memory(df)
        >>> report = analytics.generate_report()
        >>> print(report["summary"])
    """

    def __init__(
        self,
        analysis_date: datetime | None = None,
        use_pyarrow: bool = True,
        memory_optimize: bool = True,
    ) -> None:
        """初始化分析系统

        Args:
            analysis_date: 分析基准日期（默认为今天）
            use_pyarrow: 是否使用 PyArrow 后端
            memory_optimize: 是否启用内存优化
        """
        self.analysis_date = analysis_date or datetime.now()
        self.use_pyarrow = use_pyarrow
        self.memory_optimize = memory_optimize
        self._performance_stats: dict[str, Any] = {}

    def load_orders(self, filepath: str) -> pd.DataFrame:
        """加载并初步清洗订单数据

        任务:
        1. 使用分块读取 CSV 文件（避免内存溢出）
        2. 转换为 PyArrow 后端（如果启用）
        3. 删除重复订单（根据 order_id）
        4. 删除金额为负或为 0 的异常订单
        5. 删除缺失关键字段的记录（user_id, order_id, price, quantity）
        6. 转换 order_date 为 datetime 类型
        7. 记录加载时间和内存占用

        Args:
            filepath: CSV 文件路径

        Returns:
            清洗后的 DataFrame，包含以下列:
            - order_id: 订单 ID（整数）
            - user_id: 用户 ID（整数）
            - order_date: 订单日期（datetime）
            - price: 商品单价（浮点数）
            - quantity: 购买数量（整数）
            - category: 商品分类（字符串）

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 数据格式错误

        实现提示:
        - 使用 pd.read_csv() 的 chunksize 参数分块加载
        - 使用 drop_duplicates() 删除重复订单
        - 使用布尔索引过滤异常数据: df = df[df["price"] > 0]
        - 使用 dropna() 删除关键字段缺失的记录
        - 使用 pd.to_datetime() 转换日期列
        - 如果启用 PyArrow，参考示例 01_vectorization_pipeline.py 的 _convert_to_pyarrow 方法

        评分要点:
        - 正确处理重复订单（5 分）
        - 正确过滤异常值（5 分）
        - 正确处理缺失值（5 分）
        - 正确转换日期类型（5 分）
        - 加载时间 < 5 秒（10 分）

        Example:
            >>> analytics = EcommerceAnalytics()
            >>> df = analytics.load_orders("sample_orders.csv")
            >>> print(f"加载 {len(df):,} 条订单")
            >>> print(f"内存占用: {df.memory_usage(deep=True).sum() / 1e9:.2f} GB")
        """
        raise NotImplementedError("TODO: 学员实现 - 加载并清洗订单数据")

    def calculate_rfm(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 RFM 指标（最近购买、频率、消费金额）

        任务:
        1. 计算每个订单的总金额: total_amount = price × quantity
        2. 按用户分组,计算三个 RFM 指标:
           - Recency (R): (分析日期 - 最后购买日期).days
           - Frequency (F): 订单总数
           - Monetary (M): 订单总金额
        3. 使用向量化操作,避免使用 apply 或循环
        4. 记录计算时间（要求 < 10 秒）

        Args:
            df: 清洗后的订单数据

        Returns:
            RFM DataFrame，每行代表一个用户，包含以下列:
            - user_id: 用户 ID（整数）
            - recency: 最近购买距今天数（整数，越小越好）
            - frequency: 购买频率（整数，越大越好）
            - monetary: 消费金额（浮点数，越大越好）

        实现提示:
        - 先计算 total_amount 列（向量化乘法）
        - 使用 groupby().agg() 进行分组聚合:
          * Recency: 使用 max() 获取最后购买日期,然后计算天数差
          * Frequency: 使用 count() 或 size() 计算订单数
          * Monetary: 使用 sum() 计算总金额
        - 避免使用 apply(lambda),改用向量化的日期运算
        - 参考公式:
          recency = (self.analysis_date - df.groupby("user_id")["order_date"].max()).dt.days

        评分要点:
        - Recency 计算正确（10 分）
        - Frequency 计算正确（10 分）
        - Monetary 计算正确（10 分）
        - 使用向量化操作（5 分）
        - 计算时间 < 10 秒（10 分）

        Example:
            >>> rfm_df = analytics.calculate_rfm(orders_df)
            >>> print(rfm_df.head())
               user_id  recency  frequency  monetary
            0        1       15         12   25000.0
            1        2       45          8   18000.0
            2        3      200          2    3000.0
            >>> print(f"用户数: {len(rfm_df):,}")
        """
        raise NotImplementedError("TODO: 学员实现 - 计算 RFM 指标")

    def segment_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        """用户分层（高价值、潜力、流失、低价值）

        任务:
        1. 根据 RFM 指标将用户分为 4 个层级
        2. 使用 np.select 进行多条件分类（避免使用 apply）
        3. 统计每个层级的用户数和贡献金额
        4. 记录分层时间（要求 < 2 秒）

        分层规则:
        - 高价值用户: R ≤ 30 天 AND F ≥ 10 次 AND M ≥ 10000 元
        - 潜力用户: R ≤ 60 天 AND F ≥ 5 次 AND M ≥ 5000 元（且不属于高价值）
        - 流失用户: R > 180 天（无论 F 和 M）
        - 低价值用户: 其他所有用户

        Args:
            df: RFM DataFrame（包含 recency, frequency, monetary 列）

        Returns:
            带有 segment 列的 DataFrame:
            - user_id: 用户 ID
            - recency: 最近购买天数
            - frequency: 购买频率
            - monetary: 消费金额
            - segment: 用户层级（"high_value" | "potential" | "churned" | "low_value"）

        实现提示:
        - 使用 np.select() 处理多条件分支（比 apply 快 10-50 倍）
        - 定义 4 个条件列表和对应的分层标签
        - 注意条件优先级: 先判断高价值,再判断潜力,再判断流失,最后是低价值
        - 示例代码:
          ```python
          import numpy as np
          conditions = [
              (df["recency"] <= 30) & (df["frequency"] >= 10) & (df["monetary"] >= 10000),
              (df["recency"] <= 60) & (df["frequency"] >= 5) & (df["monetary"] >= 5000),
              df["recency"] > 180,
          ]
          choices = ["high_value", "potential", "churned"]
          df["segment"] = np.select(conditions, choices, default="low_value")
          ```

        评分要点:
        - 分层逻辑正确（15 分）
        - 使用 np.select（5 分）
        - 分层时间 < 2 秒（10 分）

        Example:
            >>> segmented_df = analytics.segment_customers(rfm_df)
            >>> print(segmented_df["segment"].value_counts())
            low_value      50000
            high_value     30000
            potential      15000
            churned         5000
            >>> print(segmented_df.groupby("segment")["monetary"].sum())
        """
        raise NotImplementedError("TODO: 学员实现 - 用户分层")

    def optimize_memory(self, df: pd.DataFrame) -> pd.DataFrame:
        """内存优化（目标: 从 8GB 降至 2GB 以下）

        任务:
        1. 优化整数列: int64 → int8/int16/int32（根据数值范围）
        2. 优化浮点列: float64 → float32（精度损失可接受时）
        3. 优化字符串列: object → category（重复率高时）
        4. 记录优化前后的内存占用和节省比例
        5. 确保内存节省 > 75%

        Args:
            df: 待优化的 DataFrame

        Returns:
            内存优化后的 DataFrame（数据内容不变,仅类型改变）

        实现提示:
        - 参考示例 01_vectorization_pipeline.py 的 transform_types() 方法
        - 整数优化策略:
          * 使用 df[col].min() 和 df[col].max() 获取数值范围
          * 0-255 → int8, 0-65535 → int16, 其他 → int32
        - 浮点数优化:
          * 转换为 float32,检查相对误差是否 < 1e-6
        - 字符串优化:
          * 计算唯一值比例: unique_ratio = df[col].nunique() / len(df)
          * 重复率 > 50% (unique_ratio < 0.5) 时转为 category
        - 使用 df.memory_usage(deep=True).sum() 计算总内存

        评分要点:
        - 整数类型优化（5 分）
        - 浮点类型优化（5 分）
        - 字符串类型优化（5 分）
        - 内存节省 > 75%（15 分）

        Example:
            >>> before = df.memory_usage(deep=True).sum() / 1e9
            >>> optimized_df = analytics.optimize_memory(df)
            >>> after = optimized_df.memory_usage(deep=True).sum() / 1e9
            >>> print(f"内存优化: {before:.2f} GB → {after:.2f} GB")
            >>> print(f"节省比例: {(1 - after/before)*100:.1f}%")
        """
        raise NotImplementedError("TODO: 学员实现 - 内存优化")

    def generate_report(self) -> dict[str, Any]:
        """生成分析报告

        任务:
        1. 统计各用户层级的数量和占比
        2. 计算各层级的平均 RFM 指标
        3. 汇总性能统计（加载、计算、分层时间）
        4. 汇总内存统计（优化前后对比）
        5. 返回结构化的报告字典

        Returns:
            报告字典,包含以下键:
            - summary: 总体摘要（用户数、订单数、总金额）
            - segments: 各层级统计（数量、占比、平均 RFM）
            - performance: 性能统计（各阶段耗时、总时间）
            - memory: 内存统计（优化前后、节省比例）

        实现提示:
        - 从 self._performance_stats 中读取各阶段性能数据
        - 使用 groupby().agg() 计算各层级的统计指标
        - 使用 value_counts(normalize=True) 计算占比
        - 示例结构:
          ```python
          {
              "summary": {
                  "total_users": 100000,
                  "total_orders": 800000,
                  "total_revenue": 50000000.0
              },
              "segments": {
                  "high_value": {"count": 30000, "ratio": 0.30, "avg_rfm": {...}},
                  "potential": {"count": 15000, "ratio": 0.15, "avg_rfm": {...}},
                  "churned": {"count": 5000, "ratio": 0.05, "avg_rfm": {...}},
                  "low_value": {"count": 50000, "ratio": 0.50, "avg_rfm": {...}}
              },
              "performance": {
                  "load_time": 4.2,
                  "rfm_time": 8.5,
                  "segment_time": 1.3,
                  "optimize_time": 2.1,
                  "total_time": 16.1
              },
              "memory": {
                  "before_mb": 8192,
                  "after_mb": 1536,
                  "saved_ratio": 0.81
              }
          }
          ```

        评分要点:
        - 报告结构完整（5 分）
        - 统计数据准确（5 分）

        Example:
            >>> report = analytics.generate_report()
            >>> print(f"总用户数: {report['summary']['total_users']:,}")
            >>> print(f"高价值用户: {report['segments']['high_value']['count']:,}")
            >>> print(f"总处理时间: {report['performance']['total_time']:.1f}s")
            >>> print(f"内存节省: {report['memory']['saved_ratio']*100:.1f}%")
        """
        raise NotImplementedError("TODO: 学员实现 - 生成分析报告")


def main() -> None:
    """主函数示例（学员参考）

    演示如何使用 EcommerceAnalytics 类完成完整的分析流程。
    学员可以参考这个框架完成自己的实现。
    """
    print("=" * 60)
    print("📊 电商数据分析系统 - 练习项目")
    print("=" * 60)
    print()

    # 步骤 1: 初始化分析系统
    print("步骤 1: 初始化分析系统")
    _analytics = EcommerceAnalytics(
        analysis_date=datetime(2024, 12, 31),  # 设定分析基准日期
        use_pyarrow=True,  # 启用 PyArrow 加速
        memory_optimize=True,  # 启用内存优化
    )
    print("✅ 初始化完成")
    print()

    # 步骤 2: 加载并清洗数据
    print("步骤 2: 加载订单数据")
    data_dir = Path(__file__).parent.parent / "data"
    orders_file = data_dir / "sample_orders.csv"

    if not orders_file.exists():
        print(f"❌ 数据文件不存在: {orders_file}")
        print("请先运行: python data/generate_data.py")
        return

    # TODO: 学员实现 - 调用 load_orders() 方法
    # df = analytics.load_orders(str(orders_file))
    # print(f"✅ 加载 {len(df):,} 条订单")
    # print()

    # 步骤 3: 计算 RFM 指标
    print("步骤 3: 计算 RFM 指标")
    # TODO: 学员实现 - 调用 calculate_rfm() 方法
    # rfm_df = analytics.calculate_rfm(df)
    # print(f"✅ 计算 {len(rfm_df):,} 个用户的 RFM 指标")
    # print()

    # 步骤 4: 用户分层
    print("步骤 4: 用户分层")
    # TODO: 学员实现 - 调用 segment_customers() 方法
    # segmented_df = analytics.segment_customers(rfm_df)
    # print("✅ 用户分层完成")
    # print(segmented_df["segment"].value_counts())
    # print()

    # 步骤 5: 内存优化
    print("步骤 5: 内存优化")
    # TODO: 学员实现 - 调用 optimize_memory() 方法
    # optimized_df = analytics.optimize_memory(segmented_df)
    # print("✅ 内存优化完成")
    # print()

    # 步骤 6: 生成报告
    print("步骤 6: 生成分析报告")
    # TODO: 学员实现 - 调用 generate_report() 方法
    # report = analytics.generate_report()
    # print("✅ 报告生成完成")
    # print()
    # print("=" * 60)
    # print("📋 分析报告摘要")
    # print("=" * 60)
    # print(f"总用户数: {report['summary']['total_users']:,}")
    # print(f"总订单数: {report['summary']['total_orders']:,}")
    # print(f"总金额: ¥{report['summary']['total_revenue']:,.2f}")
    # print()
    # print("用户分层:")
    # for segment, stats in report['segments'].items():
    #     print(f"  - {segment}: {stats['count']:,} ({stats['ratio']*100:.1f}%)")
    # print()
    # print("性能统计:")
    # print(f"  - 总处理时间: {report['performance']['total_time']:.1f}s")
    # print(f"  - 内存节省: {report['memory']['saved_ratio']*100:.1f}%")
    # print()
    # print("=" * 60)
    # print("✅ 分析完成")
    # print("=" * 60)

    print("⚠️  所有方法均未实现,请完成 EcommerceAnalytics 类的实现")


if __name__ == "__main__":
    main()
