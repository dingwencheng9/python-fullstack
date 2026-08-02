# L51: 异步数据管道

> **所属阶段**: Stage 5 - 数据工程  
> **课程编号**: L51  
> **预计时长**: 6-8 小时  
> **难度**: ⭐⭐⭐⭐☆  
> **前置课程**: L51 Pandas 完整实战、L51 DuckDB 分析引擎、L51 NumPy 科学计算、L51 异步编程  
> **后续课程**: Stage 6 AI Agent 与数据应用

## 课程定位

本课程是 Stage 5 的收束课：不再只讲单点的数据处理 API，而是把 **异步采集 → 数据校验 → 批处理/微批 → 幂等写入 → Checkpoint → 指标监控 → 分析落地** 串成一条可以测试、可以恢复、可以扩展的数据工程链路。

学习完成后，你应该能回答：

- 数据源速度大于消费速度时，如何用 `asyncio.Queue` 和限流做背压？
- 批处理失败后如何避免重复写入，如何从 checkpoint 继续跑？
- 什么错误应该重试，什么错误应该进入 dead letter queue？
- 如何把 L51 Pandas、L51 DuckDB、L51 NumPy 的分析能力接入异步采集结果？
- 如何用测试验证吞吐量、成功率、失败路径和恢复路径？

## 与前序课程的衔接

| 前序课程 | 在 L51 中的应用 |
| --- | --- |
| L51 Pandas 完整实战 | 对管道落地后的数据做清洗、聚合、质量检查 |
| L51 数据可视化 | 将吞吐量、失败率、延迟等指标转成运营图表 |
| L51 DuckDB 分析引擎 | 把微批结果写入本地 OLAP，快速做 SQL51 分析 |
| L51 NumPy 科学计算 | 对数值字段进行向量化转换、异常值检测和批量计算 |
| L51 异步编程 | 使用 `asyncio.Queue`、`TaskGroup`、`Semaphore` 组织并发任务 |

## 文件导航

| 路径 | 用途 |
| --- | --- |
| `lesson.md` | 详细教程，包含 ETL、背压、checkpoint、DLQ、质量校验和综合项目 |
| `examples/01_data_pipeline.py` | 完整异步数据管道示例 |
| `examples/02_async_generator.py` | 异步生成器最小示例 |
| `examples/03_checkpointed_pipeline.py` | checkpoint + 幂等 sink 的断点续跑示例 |
| `examples/04_quality_metrics.py` | 数据质量、schema drift 与指标采集示例 |
| `exercises/01_async_stream.py` | 异步流与微批练习 |
| `exercises/02_pipeline_orchestration.py` | 动态 worker 与编排练习 |
| `exercises/03_error_recovery.py` | 错误恢复、重试与 DLQ 练习 |
| `solutions/04_production_pipeline.py` | 生产级模式参考答案：checkpoint、DLQ、幂等写入、指标 |
| `tests/` | 基础异步测试与生产级模式回归测试 |

## 学习路线

1. **先跑通基础异步管道**：理解 producer、transformer、loader 三类角色。
2. **加入队列与背压**：用 `Queue(maxsize=...)` 控制内存和上游速度。
3. **加入批处理/微批**：在吞吐量和延迟之间做权衡。
4. **加入恢复机制**：checkpoint 记录 offset，幂等 sink 避免重复写入。
5. **加入质量门禁**：缺字段、类型漂移、业务规则失败进入 DLQ。
6. **加入指标与测试**：用单元测试覆盖成功、失败、恢复、重复处理和性能边界。
7. **串联 Stage 5 项目**：将管道输出交给 DuckDB/Pandas/NumPy 分析。

## 快速开始

```bash
cd stage5-data-engineering/lessons/L52-async-data-pipeline
python examples/02_async_generator.py
python examples/03_checkpointed_pipeline.py
python examples/04_quality_metrics.py
pytest tests/ -v
```

从仓库根目录运行：

```bash
python3 -m py_compile $(find stage5-data-engineering/lessons/L52-async-data-pipeline -name '*.py' -not -path '*/__pycache__/*' -print)
uv run pytest stage5-data-engineering/lessons/L52-async-data-pipeline -q --no-cov
uv run ruff check stage5-data-engineering/lessons/L52-async-data-pipeline
```

## 练习-答案-测试对应表

| 主题 | 练习 | 参考答案 | 建议测试关注点 |
| --- | --- | --- | --- |
| 异步流与微批 | `exercises/01_async_stream.py` | `solutions/01_async_stream.py` | 批大小、超时 flush、顺序保持 |
| 管道编排 | `exercises/02_pipeline_orchestration.py` | `solutions/02_pipeline_orchestration.py` | worker 数量、sentinel 传播、取消处理 |
| 错误恢复 | `exercises/03_error_recovery.py` | `solutions/03_error_recovery.py` | retry、DLQ、断点保存 |
| 生产级模式 | 自行扩展综合练习 | `solutions/04_production_pipeline.py` | checkpoint、幂等写入、schema drift、metrics |

## 完成标准

- [ ] 能画出 Extract → Transform → Load → Analyze 的异步数据流。
- [ ] 能解释 `Queue(maxsize)` 如何形成背压，以及它与 `Semaphore` 限流的区别。
- [ ] 能实现微批 flush 策略：按 batch size 或 timeout 触发。
- [ ] 能实现 checkpoint/offset 管理，并证明重复运行不会重复写入。
- [ ] 能把不可恢复错误写入 dead letter queue，并保留错误类型、payload、offset。
- [ ] 能用指标描述 processed、failed、retried、throughput、success rate。
- [ ] 能用测试覆盖成功路径、失败路径、恢复路径和 schema drift。

## 是否需要新增课程？

当前 Stage 5 不建议继续新增 L51 数据工程课程编号。原因是 L48-L51 已能形成完整闭环：

1. L48-L51 覆盖数据分析与计算基础；
2. L51 承担生产化集成与项目收束；
3. 继续加课会再次扰动 Stage 6 已顺延后的编号。

更推荐的演进方式：

- 在 L51 内增强生产级数据管道主题；
- 在后续综合项目中加入 Airflow/Prefect、Kafka/Flink、dbt/湖仓、MLOps/Feature Store 等企业级专题；
- 在 CI 中加入 Stage 5 基础必跑与完整数据栈可选跑两层质量门禁。
