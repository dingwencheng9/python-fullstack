"""练习 2 答案。"""

from __future__ import annotations


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, fn):
        self._tools[name] = fn

    def call(self, name, **kw):
        if name not in self._tools:
            raise KeyError(f"tool {name} not found")
        return self._tools[name](**kw)

    def list(self):
        return list(self._tools.keys())
