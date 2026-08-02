"""

from __future__ import annotations

L54示例: Agent评估与调试

学习目标:
- 评估指标
- 调试技术
- 性能优化
"""

import time

# 1. 评估指标
print("=== 1. 评估指标 ===")


class AgentMetrics:
    """Agent评估指标"""

    def __init__(self):
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_tokens = 0
        self.total_time = 0.0

    def record_task(self, success: bool, tokens: int, duration: float):
        """记录任务结果"""
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1

        self.total_tokens += tokens
        self.total_time += duration

    def get_metrics(self) -> dict:
        """获取指标"""
        total_tasks = self.tasks_completed + self.tasks_failed
        return {
            "success_rate": self.tasks_completed / total_tasks if total_tasks > 0 else 0,
            "avg_tokens": self.total_tokens / total_tasks if total_tasks > 0 else 0,
            "avg_time": self.total_time / total_tasks if total_tasks > 0 else 0,
            "total_tasks": total_tasks,
        }


# 测试
metrics = AgentMetrics()
metrics.record_task(True, 100, 0.5)
metrics.record_task(True, 150, 0.7)
metrics.record_task(False, 80, 0.3)

result = metrics.get_metrics()
print(f"成功率: {result['success_rate']:.2%}")
print(f"平均Token: {result['avg_tokens']:.0f}")
print(f"平均耗时: {result['avg_time']:.2f}s")

# 2. 调试日志
print("\n=== 2. 调试日志 ===")


class AgentLogger:
    """Agent调试日志"""

    def __init__(self):
        self.logs: list[dict] = []

    def log(self, level: str, message: str, data: dict = None):
        """记录日志"""
        entry = {"timestamp": time.time(), "level": level, "message": message, "data": data or {}}
        self.logs.append(entry)
        print(f"[{level}] {message}")

    def get_errors(self) -> list[dict]:
        """获取错误日志"""
        return [log for log in self.logs if log["level"] == "ERROR"]


logger = AgentLogger()
logger.log("INFO", "Agent启动")
logger.log("DEBUG", "处理查询", {"query": "test"})
logger.log("ERROR", "工具调用失败", {"tool": "search"})

errors = logger.get_errors()
print(f"\n错误数: {len(errors)}")

# 3. 性能分析
print("\n=== 3. 性能分析 ===")


def profile_agent_step(func):
    """性能分析装饰器"""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"  {func.__name__}: {duration:.3f}s")
        return result

    return wrapper


@profile_agent_step
def llm_call():
    """模拟LLM调用"""
    time.sleep(0.1)
    return "response"


@profile_agent_step
def tool_call():
    """模拟工具调用"""
    time.sleep(0.05)
    return "result"


print("执行分析:")
llm_call()
tool_call()

# 4. 优化建议
print("\n=== 4. 优化建议 ===")


def analyze_performance(metrics: dict) -> list[str]:
    """分析性能并给出建议"""
    suggestions = []

    if metrics.get("avg_time", 0) > 5:
        suggestions.append("⚠️  平均响应时间过长，考虑优化Prompt")

    if metrics.get("avg_tokens", 0) > 1000:
        suggestions.append("⚠️  Token使用量大，考虑压缩上下文")

    if metrics.get("success_rate", 1) < 0.8:
        suggestions.append("⚠️  成功率低，检查工具可靠性")

    return suggestions


suggestions = analyze_performance(result)
if suggestions:
    print("优化建议:")
    for s in suggestions:
        print(f"  {s}")
else:
    print("✅ 性能良好")

print("\n✅ 评估与调试示例完成")
