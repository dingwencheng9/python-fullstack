"""

from __future__ import annotations

L54练习: Agent评估与调试

任务: 实现完整的Agent评估和调试系统
"""


class AgentMetrics:
    """Agent评估指标"""

    def __init__(self):
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_tokens = 0
        self.total_time = 0.0

    def record_task(self, success: bool, tokens: int, duration: float):
        """
        记录任务执行结果

        参数:
            success: 是否成功
            tokens: 消耗的token数
            duration: 执行时间(秒)
        """
        # ========================================
        # 👉 TODO: 实现任务记录逻辑
        # ========================================

        # 步骤 1: 根据任务是否成功更新计数器
        # if success:
        #     self.tasks_completed += 1
        # else:
        #     self.tasks_failed += 1

        # 步骤 2: 累加 token 使用量
        # self.total_tokens += tokens

        # 步骤 3: 累加执行时间
        # self.total_time += duration

        # 💡 提示:
        # - 使用 += 进行累加
        # - 成功和失败任务分别计数
        # - 所有指标都累加，便于后续计算平均值

        # 💡 完整示例:
        # # 更新任务计数
        # if success:
        #     self.tasks_completed += 1
        # else:
        #     self.tasks_failed += 1
        #
        # # 累加 token 和时间
        # self.total_tokens += tokens
        # self.total_time += duration

        # 👉 在下方实现你的代码
        raise NotImplementedError("请实现 record_task 方法")

    def get_metrics(self) -> dict:
        """
        获取评估指标

        返回格式:
        {
            "success_rate": float,
            "avg_tokens": float,
            "avg_time": float,
            "total_tasks": int
        }
        """
        # ========================================
        # 👉 TODO: 实现指标计算
        # ========================================

        # 步骤 1: 计算总任务数
        # total_tasks = self.tasks_completed + self.tasks_failed

        # 步骤 2: 计算成功率
        # 成功率 = 成功任务数 / 总任务数
        #
        # 注意处理除零:
        # if total_tasks == 0:
        #     success_rate = 0.0
        # else:
        #     success_rate = self.tasks_completed / total_tasks

        # 步骤 3: 计算平均 token 使用量
        # 平均 tokens = 总 tokens / 总任务数
        #
        # if total_tasks == 0:
        #     avg_tokens = 0.0
        # else:
        #     avg_tokens = self.total_tokens / total_tasks

        # 步骤 4: 计算平均执行时间
        # 平均时间 = 总时间 / 总任务数
        #
        # if total_tasks == 0:
        #     avg_time = 0.0
        # else:
        #     avg_time = self.total_time / total_tasks

        # 步骤 5: 构建返回字典
        # return {
        #     "success_rate": success_rate,
        #     "avg_tokens": avg_tokens,
        #     "avg_time": avg_time,
        #     "total_tasks": total_tasks
        # }

        # 💡 提示:
        # - 注意处理除零情况
        # - 可以使用 round() 保留小数位数
        # - success_rate 通常是 0.0-1.0 的浮点数

        # 💡 完整示例:
        # total_tasks = self.tasks_completed + self.tasks_failed
        #
        # # 处理除零情况
        # if total_tasks == 0:
        #     return {
        #         "success_rate": 0.0,
        #         "avg_tokens": 0.0,
        #         "avg_time": 0.0,
        #         "total_tasks": 0
        #     }
        #
        # # 计算各项指标
        # success_rate = self.tasks_completed / total_tasks
        # avg_tokens = self.total_tokens / total_tasks
        # avg_time = self.total_time / total_tasks
        #
        # return {
        #     "success_rate": round(success_rate, 4),
        #     "avg_tokens": round(avg_tokens, 2),
        #     "avg_time": round(avg_time, 4),
        #     "total_tasks": total_tasks
        # }

        # 👉 在下方实现你的代码
        raise NotImplementedError("请实现 get_metrics 方法")


class AgentDebugger:
    """Agent调试器"""

    def __init__(self):
        self.logs: list[dict] = []

    def log(self, level: str, message: str, data: dict = None):
        """
        记录日志

        参数:
            level: 日志级别 (INFO/DEBUG/ERROR)
            message: 日志消息
            data: 附加数据
        """
        # ========================================
        # 👉 TODO: 实现日志记录
        # ========================================

        # 步骤 1: 获取当前时间戳
        # from datetime import datetime
        # timestamp = datetime.now().isoformat()

        # 步骤 2: 创建日志条目字典
        # log_entry = {
        #     "timestamp": timestamp,
        #     "level": level,
        #     "message": message,
        #     "data": data if data else {}
        # }

        # 步骤 3: 添加到日志列表
        # self.logs.append(log_entry)

        # 💡 提示:
        # - 使用 datetime.now() 获取当前时间
        # - isoformat() 生成标准时间格式
        # - data 参数可能为 None，需要处理
        # - 日志按时间顺序追加

        # 💡 完整示例:
        # from datetime import datetime
        #
        # # 创建日志条目
        # log_entry = {
        #     "timestamp": datetime.now().isoformat(),
        #     "level": level,
        #     "message": message,
        #     "data": data if data is not None else {}
        # }
        #
        # # 添加到日志列表
        # self.logs.append(log_entry)

        # 👉 在下方实现你的代码
        raise NotImplementedError("请实现 log 方法")

    def get_errors(self) -> list[dict]:
        """获取所有错误日志"""
        # ========================================
        # 👉 TODO: 实现错误提取
        # ========================================

        # 步骤 1: 筛选出 level 为 "ERROR" 的日志
        # 使用列表推导式或 filter
        #
        # 列表推导式（推荐）:
        # errors = [log for log in self.logs if log["level"] == "ERROR"]
        #
        # filter 方式:
        # errors = list(filter(lambda log: log["level"] == "ERROR", self.logs))

        # 步骤 2: 返回错误日志列表
        # return errors

        # 💡 提示:
        # - 使用列表推导式最简洁
        # - 检查 log["level"] 是否等于 "ERROR"
        # - 如果没有错误，返回空列表

        # 💡 完整示例:
        # return [log for log in self.logs if log["level"] == "ERROR"]

        # 👉 在下方实现你的代码
        raise NotImplementedError("请实现 get_errors 方法")

    def analyze_performance(self, metrics: dict) -> list[str]:
        """
        分析性能并给出建议

        规则:
        - 平均时间>5s: 建议优化
        - 平均tokens>1000: 建议压缩
        - 成功率<0.8: 建议检查

        返回:
            优化建议列表
        """
        # ========================================
        # 👉 TODO: 实现性能分析
        # ========================================

        # 步骤 1: 提取指标数据
        # avg_time = metrics.get("avg_time", 0)
        # avg_tokens = metrics.get("avg_tokens", 0)
        # success_rate = metrics.get("success_rate", 0)

        # 步骤 2: 根据规则生成建议
        # suggestions = []

        # 步骤 3: 检查平均时间
        # if avg_time > 5.0:
        #     suggestions.append("平均响应时间过长（>5秒），建议优化处理逻辑")

        # 步骤 4: 检查 token 使用量
        # if avg_tokens > 1000:
        #     suggestions.append("平均 token 使用量过高（>1000），建议压缩提示词或优化上下文")

        # 步骤 5: 检查成功率
        # if success_rate < 0.8:
        #     suggestions.append("成功率偏低（<80%），建议检查错误日志和改进错误处理")

        # 步骤 6: 返回建议列表
        # return suggestions

        # 💡 提示:
        # - 使用 get() 方法安全获取字典值
        # - 按优先级排序建议（成功率 > 时间 > tokens）
        # - 如果所有指标都正常，返回空列表
        # - 建议应该具体、可操作

        # 💡 完整示例:
        # # 提取指标
        # avg_time = metrics.get("avg_time", 0)
        # avg_tokens = metrics.get("avg_tokens", 0)
        # success_rate = metrics.get("success_rate", 0)
        #
        # # 生成建议
        # suggestions = []
        #
        # # 按优先级检查（成功率最重要）
        # if success_rate < 0.8:
        #     suggestions.append(
        #         f"成功率偏低（{success_rate:.1%}），建议检查错误日志和改进错误处理"
        #     )
        #
        # if avg_time > 5.0:
        #     suggestions.append(
        #         f"平均响应时间过长（{avg_time:.2f}秒），建议优化处理逻辑或使用缓存"
        #     )
        #
        # if avg_tokens > 1000:
        #     suggestions.append(
        #         f"平均 token 使用量过高（{avg_tokens:.0f}），建议压缩提示词或优化上下文管理"
        #     )
        #
        # # 如果所有指标都正常
        # if not suggestions:
        #     suggestions.append("所有性能指标正常，继续保持！")
        #
        # return suggestions

        # 👉 在下方实现你的代码
        raise NotImplementedError("请实现 analyze_performance 方法")
