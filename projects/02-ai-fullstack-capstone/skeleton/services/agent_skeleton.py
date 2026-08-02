# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】Agent 回答生成服务

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from collections.abc import Iterator

# TODO: 导入
# from ...models import SearchResult
# from ...config import config


class AgentService:
    """Agent 回答生成服务，支持 Mock 和真实 LLM"""

    def __init__(self, use_mock: bool = True):
        # TODO:
        # 1. self.use_mock = use_mock
        # 2. 如果不是 mock，初始化 OpenAI 客户端
        # ← 你的代码写在这里
        pass

    def generate_answer(self, query: str, sources: list[SearchResult]) -> str:
        """同步生成回答

        步骤：
        1. 构建 prompt：拼接查询和来源
        2. 如果 mock，返回模拟回答
        3. 如果真实，调用 OpenAI API 生成
        """
        # TODO: 实现生成
        # ← 你的代码写在这里

    def generate_answer_stream(self, query: str, sources: list[SearchResult]) -> Iterator[str]:
        """流式生成回答

        步骤同上，但逐块输出
        """
        # TODO: 实现流式生成
        # ← 你的代码写在这里
