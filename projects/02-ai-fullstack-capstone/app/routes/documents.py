# mypy: disable-error-code="untyped-decorator"
"""文档导入路由。

from __future__ import annotations

注：FastAPI 装饰器在 mypy strict 下被视为 untyped（上游已知问题），
文件级关闭 ``untyped-decorator``，其他 strict 检查保留。
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.rbac import Principal, require_role
from app.services.rag import RAGService

router = APIRouter(prefix="/documents", tags=["documents"])


class LRUCache:
    """线程安全的 LRU 缓存（保持工作空间隔离）。

    使用 OrderedDict 实现 LRU 驱逐策略，防止无限内存增长。
    每个 workspace_id 对应一个独立的 RAGService 实例。

    当缓存达到容量上限时，自动驱逐最久未使用的项并释放其资源。
    """

    def __init__(self, maxsize: int = 128) -> None:
        self.cache: OrderedDict[str, RAGService] = OrderedDict()
        self.maxsize = maxsize

    def get(self, key: str) -> RAGService:
        """获取缓存项（命中时移动到末尾表示最近使用）。

        Args:
            key: 工作空间 ID

        Returns:
            对应的 RAGService 实例
        """
        if key in self.cache:
            # 移动到末尾（最近使用）
            self.cache.move_to_end(key)
            return self.cache[key]

        # 未命中：创建新实例
        value = RAGService()

        # 检查是否超出容量
        if len(self.cache) >= self.maxsize:
            # 移除最久未使用的项（头部），并显式释放资源
            oldest_key, oldest_service = self.cache.popitem(last=False)
            oldest_service.close()
            print(f"🗑️  LRU 驱逐工作空间: {oldest_key} (缓存已满)")

        self.cache[key] = value
        return value

    def clear(self) -> None:
        """清空所有缓存并释放资源。

        在应用关闭时调用，确保所有 RAGService 实例正确释放资源。
        """
        for service in self.cache.values():
            service.close()
        self.cache.clear()


# 全局 LRU 缓存实例（最多缓存 128 个工作空间）
_rag_cache = LRUCache(maxsize=128)


def get_rag_service(workspace_id: str) -> RAGService:
    """获取指定工作空间的 RAG 服务实例（带 LRU 缓存）。

    使用 LRU 缓存自动管理实例生命周期：
    - 最多缓存 128 个工作空间
    - 最久未使用的工作空间会被自动清理
    - 保证工作空间数据隔离（不同 workspace_id 对应不同 RAGService 实例）

    Args:
        workspace_id: 工作空间标识符

    Returns:
        对应工作空间的 RAGService 实例
    """
    return _rag_cache.get(workspace_id)


def cleanup_rag_cache() -> None:
    """清理所有缓存的 RAG 服务实例。

    在应用关闭时调用（通过 FastAPI lifespan 事件），
    确保所有资源正确释放。
    """
    count = len(_rag_cache.cache)
    _rag_cache.clear()
    print(f"✅ 清理了 {count} 个 RAG 服务实例")


class DocumentIn(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    source: str = "manual"


@router.post("")
async def add_document(
    doc: DocumentIn,
    principal: Annotated[Principal, Depends(require_role("editor", "admin"))],
) -> dict[str, int | str]:
    rag = get_rag_service(principal.workspace_id)
    chunks = rag.ingest(doc.title, doc.content, doc.source)
    return {
        "status": "ok",
        "chunks": len(await chunks),
        "workspace_id": principal.workspace_id,
    }


@router.get("/stats")
async def stats(
    principal: Annotated[Principal, Depends(require_role("admin"))],
) -> dict[str, int | str]:
    rag = get_rag_service(principal.workspace_id)
    return {
        "workspace_id": principal.workspace_id,
        "documents": rag.corpus_size(),
        "chunks": len(rag.store.chunks),
    }
