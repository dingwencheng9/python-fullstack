# L36: 异步背压机制

> 🔧 **Stage 4 Web 进阶核心课** | ⏱️ 6 小时 | ⭐⭐⭐⭐☆（高级）  
> 前置课程：L19 异步编程核心、L27 FastAPI 可观测性  
> 关键词：Backpressure、Semaphore、Queue、Token Bucket、滑动窗口、熔断、重试、连接池、生产监控

## 📋 课程定位

异步系统的吞吐瓶颈通常不是“不会并发”，而是“并发没有边界”。当上游生产速度持续大于下游处理能力时，系统会从延迟升高逐步演变为队列堆积、内存膨胀、连接耗尽、超时风暴和级联故障。

本课程围绕 **异步背压（Backpressure）** 建立生产级流控能力：让服务在压力下能够主动限流、排队、降级、熔断和恢复，而不是被动崩溃。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 解释背压、限流、节流、熔断、降级之间的边界
- [ ] 使用 `asyncio.Semaphore` 控制协程并发上限
- [ ] 使用有界 `asyncio.Queue` 构建生产者-消费者背压管道
- [ ] 实现 Token Bucket 与滑动窗口限流器
- [ ] 为外部 API、数据库连接池、任务队列设计容量保护
- [ ] 结合超时、重试、指数退避、熔断器避免级联故障
- [ ] 使用指标监控队列长度、等待时间、拒绝率和恢复时间
- [ ] 完成 L36 测试并能解释每个测试背后的生产风险

## 📂 课程结构

```text
L36-async-backpressure/
├── README.md                         # 课程说明与学习路径
├── lesson.md                         # 详细课程讲义
├── examples/
│   ├── 01_backpressure_basics.py      # FastAPI 背压基础：并发、限流、队列
│   ├── 01_semaphore.py                # Semaphore 最小示例
│   ├── 02_production_backpressure.py  # 熔断、重试、自适应限流、连接池
│   └── 02_token_bucket.py             # Token Bucket 最小示例
├── tests/
│   └── test_backpressure.py           # 27 个行为测试
└── solutions/                         # 练习参考解答预留
```

## 🧭 建议学习顺序

1. 阅读 `lesson.md` 的模块 1-3，理解背压模型和容量预算。
2. 运行 `examples/01_semaphore.py` 与 `examples/02_token_bucket.py`，观察限流效果。
3. 阅读 `examples/01_backpressure_basics.py`，理解 FastAPI 接口中的限流、队列和 429 返回。
4. 阅读 `examples/02_production_backpressure.py`，理解熔断、重试和自适应限流。
5. 运行测试，反向理解每个组件的边界条件。

## 🚀 快速开始

```bash
cd stage4-web-advanced/lessons/L36-async-backpressure
uv run --extra dev pytest tests -q
```

运行单个示例：

```bash
uv run python examples/01_semaphore.py
uv run python examples/02_token_bucket.py
```

## 🧪 验收标准

- `uv run --extra dev pytest stage4-web-advanced/lessons/L36-async-backpressure/tests -q` 通过
- 能说明何时返回 429、何时排队等待、何时熔断、何时降级
- 能为一个 FastAPI 接口画出容量预算：入口 QPS、并发数、队列长度、超时、重试次数
- 能指出“无限 `gather` / 无限队列 / 无超时重试”的生产风险

## 🔗 后续课程

- **L37 Web 安全完整指南**：在流控基础上加入认证、授权、输入校验和攻击防护
- **L38 E2E 测试**：用端到端测试验证限流、降级和错误提示
- **L39 API 性能优化**：从压测与 profiling 角度继续优化吞吐和延迟
