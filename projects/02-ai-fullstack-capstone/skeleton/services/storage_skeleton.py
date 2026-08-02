# ruff: noqa: F821
# 骨架代码：学生填空用教学模板，类型未定义为设计意图

"""

from __future__ import annotations

【骨架代码】文档存储服务

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

# TODO: 导入类型注解
# from typing import Any

# TODO: 导入 Document 模型
# from ..models import Document


class DocumentStorage:
    """内存文档存储"""

    def __init__(self):
        # TODO: 初始化 self.documents: dict[str, Document] = {}
        # ← 你的代码写在这里
        pass

    def save(self, doc: Document) -> Document:
        """保存文档"""
        # TODO: 保存到字典，返回文档
        # ← 你的代码写在这里

    def get(self, doc_id: str) -> Document | None:
        """获取文档"""
        # TODO: 根据 ID 获取文档，不存在返回 None
        # ← 你的代码写在这里

    def delete(self, doc_id: str) -> bool:
        """删除文档

        返回 True 如果删除成功，False 如果不存在
        """
        # TODO: 删除文档
        # ← 你的代码写在这里

    def list_all(self) -> list[Document]:
        """列出所有文档"""
        # TODO: 返回所有文档列表
        # ← 你的代码写在这里
