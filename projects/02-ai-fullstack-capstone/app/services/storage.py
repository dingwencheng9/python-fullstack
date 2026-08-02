"""轻量持久化服务。"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.models import Document

logger = logging.getLogger(__name__)


class JsonStorage:
    """JSON 文件存储，用于离线作品集演示。"""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save_documents(self, docs: list[Document]) -> None:
        """保存文档列表。"""
        data = [
            {"id": d.id, "title": d.title, "content": d.content, "source": d.source} for d in docs
        ]
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def load_documents(self) -> list[Document]:
        """加载文档列表。"""
        if not self.path.exists():
            return []
        raw = self.path.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error("存储文件 JSON 解析失败: %s — %s", self.path, e, exc_info=True)
            return []
        return [Document.create(d["title"], d["content"], d.get("source", "manual")) for d in data]
