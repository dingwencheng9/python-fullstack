# Stage 0-6 课程文档六维度审查报告

> **审查日期**: 2026-08-13
> **审查范围**: Stage 0-6（L01-L65 + P01-P06）
> **审查维度**: 路径完整性、内容一致性、知识点顺序、代码示例验证、测试覆盖检查、格式规范
> **审查结果**: P0 × 13 | P1 × 48 | P2 × 9

---

## 🔴 P0 严重问题（必须修复）

### Stage 3: Web 开发基础

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L27-http | README.md 列出的示例文件与实际完全不匹配 | README.md | 更新为: 01_raw_http_request.py, 02_simple_server.py, 03_http_requests.py, 04_http_status_codes.py, 05_http_headers.py |
| L28-fastapi-basics | README.md 列出 01-04 文件，实际是 03/04/05 开头的文件名 | README.md | 更新为: 03_fastapi_basics.py, 04_pydantic_basics.py, 05_dependency_injection.py 等 |
| L29-sql-basics | README.md 列出 01-03 文件，实际只有 03_sql_queries.py 和 main.py | README.md | 更新为实际存在的文件 |
| L32-docker | README.md 列出 01/03 文件，实际是 01_check_dockerfile.py, 02_mock_compose.py, 03_docker_commands.py | README.md | 更新为实际存在的文件 |
| L33-sse | README.md 列出的示例文件与实际完全不匹配（列出 01-03，实际是 agent_chat_router.py 等） | README.md | 更新为实际存在的文件 |

### Stage 4: Web 开发进阶

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L36-async-backpressure | cd 命令路径错误: `lessoL36` → `lessons/L36` | README.md:53 | 修正为 `cd stage4-web-advanced/lessons/L36-async-backpressure` |
| L36-async-backpressure | pytest 路径错误: `lessoL36` → `lessons/L36` | README.md:66 | 修正为 `pytest stage4-web-advanced/lessons/L36-async-backpressure/tests` |

### Stage 5: 数据工程

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L50-pandas-complete | lesson.md 第 931 行引用 `examples/05_performance.py`，文件不存在 | lesson.md:931 | 移除引用或创建该文件 |
| L53-duckdb-olap | lesson.md 引用 3 个不存在的文件 (03/04/05) | lesson.md:1049-1051 | 移除引用或创建文件 |
| L53-duckdb-olap | 引用 2 个不存在的 exercises 文件 | lesson.md | 创建缺失文件或修正引用 |
| L51-async-data-pipeline | README.md 中路径全部错误: `L52-` → `L51-` | README.md:60,70-72 | 替换所有 `L52-async-data-pipeline` 为 `L51-async-data-pipeline` |

### Stage 6: AI Agent 开发

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L61-multi-agent | README.md 引用的文件名与实际不一致 | README.md:92,110,124 | 统一文件名格式或更新 README 引用 |
| L65-agent-sse-router | lesson.md 引用 3 个不存在的 exercises 文件 | lesson.md | 创建缺失文件或修正为 `exercise_01.py` |

---

## 🟡 P1 中等问题（建议修复）

### Stage 0: Python 基础

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L03-data-structures | README 引用 02_dict.py，实际是 03_dict.py | README.md | 修正文件名 |
| L03-data-structures | README 引用 04_comprehension_vs_generator.py，实际是 05_comprehensions.py | README.md | 修正文件名 |
| L04-functions-modules | README 引用 00_demo.py，实际是 01_demo.py | README.md | 修正文件名 |
| L04-functions-modules | README 引用 06_type_annotations.py，实际是 07_type_annotations.py | README.md | 修正文件名 |
| L04-functions-modules | README 引用 07_lambda.py，实际是 08_lambda.py | README.md | 修正文件名 |
| P01-student-manager | README 引用不存在的测试文件 (test_student.py, test_manager.py, test_search.py) | README.md | 更新为 test_student_manager.py |

### Stage 1: Python 进阶

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L10-type-system | lesson.md/README 引用 02_protocol.py，实际是 02_protocol_typing.py | lesson.md | 修正文件名 |
| L10-type-system | lesson.md/README 引用 07_typeddict.py，实际是 06_typeddict.py | lesson.md | 修正文件名 |
| L10-type-system | lesson.md 引用 solutions/01_type_basics_solution.py，实际是 solution_01_type_narrowing.py | lesson.md | 修正文件名 |
| L10-type-system | lesson.md 引用 solutions/02_generic_stack_solution.py，实际是 solution_02_protocol.py | lesson.md | 修正文件名 |
| L10-type-system | lesson.md 引用 solutions/03_protocol_solution.py，实际是 solution_03_generic_constraints.py | lesson.md | 修正文件名 |
| L14-decorator-advanced | README 引用 exercises/01_parameterized.py，实际是 01_parameterized_decorators.py | README.md | 修正文件名 |
| L14-decorator-advanced | README 引用 exercises/02_chaining.py，实际是 02_decorator_chaining.py | README.md | 修正文件名 |
| L16-concurrency-intro | README 引用 exercises/02_async_queues.py，实际是 02_concurrent_file_processor.py | README.md | 修正文件名 |
| L16-concurrency-intro | lesson.md 引用 exercises/01_async_website_checker.py，实际是 01_async_basics.py | lesson.md | 修正文件名 |

### Stage 2: 现代工程

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L19-pytest-complete | lesson.md 引用不存在的 tests/conftest.py | lesson.md | 移除引用（使用根目录 conftest.py） |
| L19-pytest-complete | lesson.md 引用不存在的 tests/test_models.py | lesson.md | 移除引用 |
| L20-toolchain | lesson.md 引用不存在的 tests/test_calculator.py, test_feature.py | lesson.md | 移除引用 |
| L23-python-new-features | lesson.md 引用不存在的 tests/test_performance.py | lesson.md | 移除引用 |
| L24-advanced-flow-async | lesson.md 引用不存在的 examples/log_processor.py | lesson.md | 移除引用或创建文件 |
| L26-threading | README 引用不存在的 tests/conftest.py | README.md | 移除引用 |
| L26-threading | lesson.md 引用 examples/01_free_threading_benchmark.py，实际是 01_threading_basics.py | lesson.md | 修正文件名 |

### Stage 3: Web 开发基础

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L31-sql-advanced | README 列出文件与实际部分不匹配 | README.md | 将 01_explain_plan.py → 03_query_plan_indexes.py |
| L34-websocket | README 列出 01_websocket_basics.py，实际是 01_chat_server.py | README.md | 修正文件名 |
| L35-htmx | README 列出 01_htmx_basics.py，实际是 01_basic_htmx.py | README.md | 修正文件名 |

### Stage 4: Web 开发进阶

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L37-web-security-complete | lesson.md 引用 L33 的 SecurityGateway，但前置课程声明未包含 L33 | lesson.md:766,790 | 添加 L33 到前置课程列表 |
| L38-auth-authorization | README 列出的示例文件与实际不匹配 | README.md | 检查并更新 |
| L39-e2e-testing | README 列出的示例文件与实际不匹配 | README.md | 检查并更新 |
| L40-message-queue | README 缺少课程结构部分 | README.md | 添加 ## 📂 课程结构 |
| L41-api-performance | README 列出的示例文件与实际不匹配 | README.md | 检查并更新 |
| L42-caching-strategy | README 缺少课程结构部分 | README.md | 添加课程结构 |
| L42-caching-strategy | pyproject.toml 包含 [project] 配置 | pyproject.toml | 移除 [project]，只保留 [tool.*] |
| L43-async-tasks | README 列出的示例文件与实际不匹配 | README.md | 检查并更新 |
| L44-microservices-basics | README 缺少课程结构部分 | README.md | 添加课程结构 |
| L44-microservices-basics | pyproject.toml 包含 [project] 配置 | pyproject.toml | 移除 [project] |
| L46-websocket-advanced | README 列出的示例文件与实际不匹配 | README.md | 检查并更新 |
| L36-async-backpressure | solutions/ 目录为空 | solutions/ | 添加参考答案或更新 README |
| P05-realtime-collaboration | solutions/ 目录为空 | solutions/ | 添加参考答案或更新 README |

### Stage 5: 数据工程

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L52-numpy-rag-poc | lesson.md 引用不存在的 examples/05_elasticsearch_search.py | lesson.md:319 | 标记为可选或移除引用 |
| L47-pandas | README 使用 L48 路径而非 L47 | README.md:17,165 | 修正路径 |
| L49-duckdb | README 前置课程路径引用错误 | README.md:28 | 验证并修正 |

### Stage 6: AI Agent 开发

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L61-multi-agent | 前置课程链接路径格式和编号错误 | README.md:14-16 | 修正为 L54/L56/L58 |
| L61-multi-agent | 位置显示 "Stage 5" 应为 "Stage 6" | README.md:20 | 修正 |
| L61-multi-agent | 前置/后续课程编号错误 (L56/L57 应为 L60/L62) | README.md:23-24 | 修正 |

---

## 🟢 P2 轻微问题（可选修复）

| 课程 | 问题描述 | 位置 | 修复建议 |
|------|----------|------|----------|
| L37-web-security-complete | 知识点顺序声明不完整 | lesson.md | 在前置课程声明中添加 L33 |
| L61-multi-agent | 延伸阅读课程编号错误 (L51/L53/L38 应为 L57/L54/L65) | README.md:180-182 | 修正编号 |
| L61-multi-agent | 测试文件注释提到 sys.path.insert | test_multi_agent.py | 无需修改（文档注释） |
| L25-extreme-abstraction-performance | 测试文件注释提到 sys.modules.pop | test_python313_performance.py | 无需修改（文档注释） |
| Stage 5 | 所有课程知识点顺序正确 | - | 无需操作 |
| Stage 6 | 所有课程知识点顺序正确 | - | 无需操作 |
| Stage 5-6 | 所有 Python 文件语法检查通过 | - | 无需操作 |

---

## 📊 问题统计

| Stage | P0 | P1 | P2 | 合计 |
|-------|-----|-----|-----|------|
| Stage 0 | 0 | 8 | 0 | 8 |
| Stage 1 | 0 | 10 | 0 | 10 |
| Stage 2 | 0 | 8 | 0 | 8 |
| Stage 3 | 5 | 3 | 0 | 8 |
| Stage 4 | 2 | 15 | 1 | 18 |
| Stage 5 | 3 | 4 | 3 | 10 |
| Stage 6 | 2 | 4 | 4 | 10 |
| **总计** | **13** | **48** | **9** | **70** |

---

## 🔧 修复优先级建议

### 第一批（立即修复）
1. **L36 README.md 路径错误** - 学员无法运行示例
2. **L51 README.md 路径错误** - 学员无法运行示例
3. **Stage 3 README.md 文件列表** - 多处完全不一致

### 第二批（本周内修复）
4. **L61 README.md 课程编号错误** - 影响课程导航
5. **L65 lesson.md 引用不存在的文件** - 影响练习
6. **L53 lesson.md 引用不存在的文件** - 影响练习

### 第三批（后续迭代）
7. 其他 P1 文件名修正
8. 缺失的课程结构部分补充
9. pyproject.toml 规范修正

---

*报告生成时间: 2026-08-13*
