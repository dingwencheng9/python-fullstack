"""

from __future__ import annotations

【骨架代码】数据模型 — Pydantic 模型定义

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from pydantic import BaseModel


class Document(BaseModel):
    """文档模型

    TODO: 定义以下字段：
    1. id: str - 文档唯一ID
    2. content: str - 文档内容
    3. chunks: list[str] - 分块后的内容列表
    4. created_at: datetime - 创建时间
    5. filename: str | None = None - 原始文件名
    """

    # ← 你的代码写在这里


class DocumentUploadRequest(BaseModel):
    """文档上传请求

    TODO: 定义以下字段：
    1. content: str - 文档内容
    2. filename: str | None = None - 文件名
    """

    # ← 你的代码写在这里


class SearchRequest(BaseModel):
    """搜索请求

    TODO: 定义以下字段：
    1. query: str - 查询文本
    2. top_k: int = 5 - 返回结果数量
    """

    # ← 你的代码写在这里


class SearchResult(BaseModel):
    """搜索结果

    TODO: 定义以下字段：
    1. content: str - 片段内容
    2. document_id: str - 所属文档ID
    3. score: float - 相似度分数
    """

    # ← 你的代码写在这里


class ChatRequest(BaseModel):
    """聊天请求

    TODO: 定义以下字段：
    1. query: str - 用户问题
    2. conversation_id: str | None = None - 会话ID
    """

    # ← 你的代码写在这里


class ChatResponse(BaseModel):
    """聊天响应（非流式）

    TODO: 定义以下字段：
    1. answer: str - 回答文本
    2. sources: list[SearchResult] - 引用的来源片段
    """

    # ← 你的代码写在这里


class HealthResponse(BaseModel):
    """健康检查响应

    TODO: 定义以下字段：
    1. status: str - 状态
    2. timestamp: float - 当前时间戳
    3. version: str - 应用版本
    """

    # ← 你的代码写在这里
