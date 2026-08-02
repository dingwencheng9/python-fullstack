"""练习 2 答案。"""

from __future__ import annotations


class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def format(self, **kw: str | int | float) -> str:
        """格式化模板，返回新字符串，不修改实例状态。

        Args:
            **kw: 要替换的键值对

        Returns:
            格式化后的字符串
        """
        result = self.template
        for k, v in kw.items():
            result = result.replace("{" + k + "}", str(v))
        return result
