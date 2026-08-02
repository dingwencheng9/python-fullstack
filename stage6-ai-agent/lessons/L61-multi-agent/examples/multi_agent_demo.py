"""

from __future__ import annotations

L57: 多 Agent 协同编排 - 示例演示

展示如何使用多 Agent 系统处理复杂查询。

运行方式：
    PYTHONPATH=stage6-ai-agent/lessons/L57-multi-agent-orchestration \
      uv run python -m examples.multi_agent_demo
"""

import asyncio
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 把 lesson 根目录加入 path，让 solutions 包可被 import
try:
    _LESSON_ROOT = Path(__file__).resolve().parent.parent
except Exception as e:
    logger.error(f"无法解析文件路径: {e}")
    _LESSON_ROOT = Path.cwd()

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
except ImportError as e:
    logger.error(f"无法导入 OpenTelemetry 模块: {e}")
    raise

try:
    from solutions.multi_agent.orchestrator import run_multi_agent_query
except ImportError as e:
    logger.error(f"无法导入 run_multi_agent_query: {e}")
    raise

# ============================================================================
# OpenTelemetry 初始化
# ============================================================================


def setup_tracing():
    """初始化 OpenTelemetry 追踪"""
    try:
        # 创建资源
        resource = Resource.create({"service.name": "multi-agent-demo", "service.version": "1.0.0"})

        # 创建 TracerProvider
        provider = TracerProvider(resource=resource)

        # 添加 Console Exporter（用于演示）
        console_exporter = ConsoleSpanExporter()
        span_processor = BatchSpanProcessor(console_exporter)
        provider.add_span_processor(span_processor)

        # 设置全局 TracerProvider
        trace.set_tracer_provider(provider)

        print("✅ OpenTelemetry 追踪已初始化")
    except Exception as e:
        logger.error(f"OpenTelemetry 初始化失败: {e}")
        raise


# ============================================================================
# 示例场景
# ============================================================================


async def example_1_data_analysis():
    """示例 1: 纯数据分析任务"""
    try:
        print("\n" + "=" * 80)
        print("示例 1: 纯数据分析任务")
        print("=" * 80)

        query = "分析销售数据，计算总销售额和最佳产品"

        print(f"\n用户查询: {query}")
        print("\n执行中...")

        result = await run_multi_agent_query(query)

        print("\n执行结果:")
        print(f"  成功: {result['success']}")
        print(f"  任务 ID: {result['task_id']}")
        print(f"  追踪 ID: {result['trace_id']}")
        print(f"  执行任务数: {result['tasks_executed']}/{result['total_tasks']}")
        print(f"  迭代次数: {result['iterations']}")

        if result["success"]:
            print(f"\n最终答案:\n{result['final_answer']}")
        else:
            print(f"\n错误: {result['error']}")

        return result
    except Exception as e:
        logger.error(f"示例 1 执行失败: {e}")
        return {"success": False, "error": str(e)}


async def example_2_knowledge_search():
    """示例 2: 纯知识检索任务"""
    try:
        print("\n" + "=" * 80)
        print("示例 2: 纯知识检索任务")
        print("=" * 80)

        query = "查询 Python 异步编程的相关文档"

        print(f"\n用户查询: {query}")
        print("\n执行中...")

        result = await run_multi_agent_query(query)

        print("\n执行结果:")
        print(f"  成功: {result['success']}")
        print(f"  任务 ID: {result['task_id']}")
        print(f"  追踪 ID: {result['trace_id']}")
        print(f"  执行任务数: {result['tasks_executed']}/{result['total_tasks']}")
        print(f"  迭代次数: {result['iterations']}")

        if result["success"]:
            print(f"\n最终答案:\n{result['final_answer']}")
        else:
            print(f"\n错误: {result['error']}")

        return result
    except Exception as e:
        logger.error(f"示例 2 执行失败: {e}")
        return {"success": False, "error": str(e)}


async def example_3_hybrid_task():
    """示例 3: 混合任务（数据分析 + 知识检索）"""
    try:
        print("\n" + "=" * 80)
        print("示例 3: 混合任务（数据分析 + 知识检索）")
        print("=" * 80)

        query = "分析销售数据并检索相关的数据分析文档"

        print(f"\n用户查询: {query}")
        print("\n执行中...")

        result = await run_multi_agent_query(query)

        print("\n执行结果:")
        print(f"  成功: {result['success']}")
        print(f"  任务 ID: {result['task_id']}")
        print(f"  追踪 ID: {result['trace_id']}")
        print(f"  执行任务数: {result['tasks_executed']}/{result['total_tasks']}")
        print(f"  迭代次数: {result['iterations']}")

        if result["success"]:
            print(f"\n最终答案:\n{result['final_answer']}")

            # 显示各 Agent 的详细结果
            print("\n各 Agent 执行结果:")
            for agent_role, tool_result in result.get("tool_results", {}).items():
                print(f"\n  {agent_role}:")
                if isinstance(tool_result, dict):
                    summary = tool_result.get("summary", "N/A")
                    print(f"    摘要: {summary}")
        else:
            print(f"\n错误: {result['error']}")

        return result
    except Exception as e:
        logger.error(f"示例 3 执行失败: {e}")
        return {"success": False, "error": str(e)}


async def example_4_trace_analysis():
    """示例 4: 追踪分析演示"""
    try:
        print("\n" + "=" * 80)
        print("示例 4: 追踪分析演示")
        print("=" * 80)

        query = "执行数据统计和知识检索"

        print(f"\n用户查询: {query}")
        print("\n执行中...")

        # 执行查询
        result = await run_multi_agent_query(query)

        print("\n执行结果:")
        print(f"  成功: {result['success']}")
        print(f"  追踪 ID: {result['trace_id']}")

        print("\n追踪分析:")
        print("  在 Jaeger UI 中可以看到:")
        print("    1. Supervisor 节点: 任务规划 → 任务委派 → 结果聚合")
        print("    2. Worker 节点: DataAnalyst 和 Knowledge 的并行执行")
        print("    3. 消息传递: Agent 间的消息流转")
        print("    4. Parent-Child 关系: Supervisor → Workers 的调用链")

        print("\n  访问 Jaeger UI:")
        print(f"    http://localhost:16686/trace/{result['trace_id']}")

        return result
    except Exception as e:
        logger.error(f"示例 4 执行失败: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# 主程序
# ============================================================================


async def main():
    """主程序入口"""
    try:
        print("\n" + "=" * 80)
        print("L21: 多 Agent 协同编排 - 示例演示")
        print("=" * 80)

        # 初始化追踪
        try:
            setup_tracing()
        except Exception as e:
            logger.error(f"追踪初始化失败，继续执行: {e}")

        # 运行示例
        await example_1_data_analysis()
        await asyncio.sleep(1)

        await example_2_knowledge_search()
        await asyncio.sleep(1)

        await example_3_hybrid_task()
        await asyncio.sleep(1)

        await example_4_trace_analysis()

        print("\n" + "=" * 80)
        print("所有示例执行完成")
        print("=" * 80)
        print("\n提示:")
        print("  1. 查看 Jaeger UI: http://localhost:16686")
        print("  2. 搜索服务: multi-agent-demo")
        print("  3. 查看追踪链路，观察 Agent 间的协同流程")
        print("=" * 80 + "\n")
    except Exception as e:
        logger.error(f"主程序执行失败: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        exit(1)
