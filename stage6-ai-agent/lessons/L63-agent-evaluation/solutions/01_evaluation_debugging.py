"""

from __future__ import annotations

L54参考答案: Agent评估与调试
"""

import time


class AgentMetrics:
    """Agent评估指标"""

    def __init__(self):
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_tokens = 0
        self.total_time = 0.0

    def record_task(self, success: bool, tokens: int, duration: float):
        """记录任务执行结果"""
        if success:
            self.tasks_completed += 1
        else:
            self.tasks_failed += 1

        self.total_tokens += tokens
        self.total_time += duration

    def get_metrics(self) -> dict:
        """获取评估指标"""
        total_tasks = self.tasks_completed + self.tasks_failed

        return {
            "success_rate": self.tasks_completed / total_tasks if total_tasks > 0 else 0,
            "avg_tokens": self.total_tokens / total_tasks if total_tasks > 0 else 0,
            "avg_time": self.total_time / total_tasks if total_tasks > 0 else 0,
            "total_tasks": total_tasks,
        }


class AgentDebugger:
    """Agent调试器"""

    def __init__(self):
        self.logs: list[dict] = []

    def log(self, level: str, message: str, data: dict = None):
        """记录日志"""
        entry = {"timestamp": time.time(), "level": level, "message": message, "data": data or {}}
        self.logs.append(entry)

    def get_errors(self) -> list[dict]:
        """获取所有错误日志"""
        return [log for log in self.logs if log["level"] == "ERROR"]

    def analyze_performance(self, metrics: dict) -> list[str]:
        """分析性能并给出建议"""
        suggestions = []

        if metrics.get("avg_time", 0) > 5:
            suggestions.append("⚠️ 平均响应时间过长，建议优化Prompt或工具")

        if metrics.get("avg_tokens", 0) > 1000:
            suggestions.append("⚠️ Token使用量大，建议压缩上下文")

        if metrics.get("success_rate", 1) < 0.8:
            suggestions.append("⚠️ 成功率低，建议检查工具可靠性和错误处理")

        return suggestions
