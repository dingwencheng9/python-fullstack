"""Capstone 数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4


@dataclass(frozen=True)
class Document:
    """导入的文档。"""

    id: str
    title: str
    content: str
    source: str = "manual"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, title: str, content: str, source: str = "manual") -> Document:
        return cls(id=str(uuid4()), title=title, content=content, source=source)


@dataclass(frozen=True)
class Chunk:
    """文档切片。"""

    id: str
    document_id: str
    text: str
    score: float = 0.0


@dataclass(frozen=True)
class ChatMessage:
    """聊天消息。"""

    role: Literal["user", "assistant", "system"]
    content: str


@dataclass(frozen=True)
class Answer:
    """Agent 回答。"""

    question: str
    answer: str
    sources: list[Chunk]
