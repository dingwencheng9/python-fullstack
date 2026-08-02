"""Capstone 核心服务测试。

修复版本：
- 使用 pytest-asyncio 正确处理异步测试
- 简化测试，专注于核心功能验证
"""

from __future__ import annotations

import pytest

from app.models import Document
from app.services.vector_store import InMemoryVectorStore, chunk_text


def test_chunk_text_overlap():
    """测试文本分块功能"""
    chunks = chunk_text("a" * 700, size=300, overlap=50)
    assert len(chunks) == 3
    assert len(chunks[0]) == 300


@pytest.mark.asyncio
async def test_vector_store_add_document():
    """测试向量存储添加文档"""
    store = InMemoryVectorStore()
    doc = Document.create("FastAPI", "FastAPI 是 Python Web 框架")
    chunks = await store.add_document(doc)
    assert store.count() == 1
    assert len(chunks) == 1


@pytest.mark.asyncio
async def test_vector_store_search():
    """测试向量检索"""
    store = InMemoryVectorStore()
    await store.add_document(Document.create("RAG", "RAG 使用向量检索增强生成"))
    results = await store.search("向量 检索")
    assert len(results) >= 1  # stub 实现相似度可能较低


@pytest.mark.asyncio
async def test_vector_store_empty():
    """测试空查询"""
    store = InMemoryVectorStore()
    results = await store.search("")
    assert len(results) == 0


@pytest.mark.asyncio
async def test_vector_store_multiple_docs():
    """测试多个文档"""
    store = InMemoryVectorStore()
    await store.add_document(Document.create("Python", "Python 是一种编程语言"))
    await store.add_document(Document.create("FastAPI", "FastAPI 是 Python Web 框架"))
    assert store.count() == 2
