# Exercise 01: Embedding Pipeline 实现

**难度**: ⭐⭐⭐  
**预计时间**: 45 分钟  
**学习目标**: 掌握文本分块与 Embedding 流水线的异步实现

---

## 📋 任务描述

实现一个完整的 Embedding Pipeline，包含文本分块、向量生成和存储三个阶段。

---

## 🎯 核心要求

### 1. 实现文本分块器

基于 `core/text_chunker.py` 中的 `chunk_text()` 函数，实现一个异步的文本分块器类：

```python
class TextChunker:
    """文本分块器

    将长文本切分为固定大小的块，支持重叠。
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        """
        初始化分块器

        Args:
            chunk_size: 每个块的最大字符数
            overlap: 块之间的重叠字符数
        """
        pass  # TODO: 实现初始化逻辑

    async def chunk(self, text: str) -> list[str]:
        """
        异步分块文本

        Args:
            text: 输入文本

        Returns:
            分块后的文本列表
        """
        pass  # TODO: 实现分块逻辑
```

### 2. 实现 Embedding Pipeline

创建一个完整的 Pipeline 类，集成分块、向量生成和存储：

```python
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct

class EmbeddingPipeline:
    """Embedding 流水线

    完整流程：文本 → 分块 → 生成向量 → 存储到 Qdrant
    """

    def __init__(
        self,
        qdrant_client: AsyncQdrantClient,
        collection_name: str,
        vector_size: int = 384,
    ) -> None:
        """
        初始化 Pipeline

        Args:
            qdrant_client: Qdrant 异步客户端
            collection_name: 集合名称
            vector_size: 向量维度
        """
        pass  # TODO: 实现初始化

    async def process_document(
        self,
        document: str,
        metadata: dict[str, str] | None = None,
    ) -> int:
        """
        处理单个文档

        Args:
            document: 文档文本
            metadata: 元数据（可选）

        Returns:
            插入的向量数量

        Raises:
            ValueError: 文档为空时
        """
        pass  # TODO: 实现处理逻辑
```

---

## 🔧 实现提示

### 提示 1: 文本分块逻辑

```python
# 基本算法
chunks = []
start = 0
while start < len(text):
    end = min(start + chunk_size, len(text))
    chunk = text[start:end]
    chunks.append(chunk)
    start += chunk_size - overlap
```

### 提示 2: 模拟 Embedding 生成

在实际项目中应使用真实模型，练习中可以使用模拟函数：

```python
import random

def mock_embedding(text: str, size: int) -> list[float]:
    """模拟 embedding 生成"""
    random.seed(hash(text))
    return [random.random() for _ in range(size)]
```

### 提示 3: 异步批量存储

使用 Qdrant 的 `upsert` 方法批量插入：

```python
points = [
    PointStruct(
        id=i,
        vector=embedding,
        payload={"text": chunk, **metadata},
    )
    for i, (chunk, embedding) in enumerate(chunks_with_embeddings)
]

await qdrant_client.upsert(
    collection_name=collection_name,
    points=points,
)
```

---

## ✅ 验收标准

### 功能要求

- [ ] `TextChunker` 正确实现分块逻辑
- [ ] 支持自定义 `chunk_size` 和 `overlap`
- [ ] `EmbeddingPipeline` 完整实现三阶段流程
- [ ] 空文档抛出 `ValueError` 异常
- [ ] 批量插入返回正确的插入数量

### 代码质量

- [ ] 通过 `mypy --strict` 检查
- [ ] 通过 `ruff check` 检查
- [ ] 完整的类型注解
- [ ] 完整的文档字符串

### 测试要求

编写测试用例验证：

```python
async def test_text_chunker():
    """测试文本分块器"""
    chunker = TextChunker(chunk_size=10, overlap=2)
    text = "Hello World! This is a test."
    chunks = await chunker.chunk(text)

    assert len(chunks) > 1
    assert all(len(c) <= 10 for c in chunks)

async def test_embedding_pipeline():
    """测试 Embedding Pipeline"""
    client = AsyncQdrantClient(":memory:")
    pipeline = EmbeddingPipeline(
        qdrant_client=client,
        collection_name="test",
        vector_size=128,
    )

    count = await pipeline.process_document("Test document")
    assert count > 0
```

---

## 💡 扩展挑战

1. **智能分块**: 实现按句子或段落分块
2. **进度反馈**: 添加处理进度的 callback 机制
3. **错误重试**: 实现失败自动重试逻辑
4. **批量处理**: 支持多文档并发处理

---

## 📚 参考资源

- `core/text_chunker.py` - 文本分块工具
- `core/vector_store.py` - 向量存储参考实现
- `demos/demo_02_vector_store.py` - Qdrant 使用示例
- `demos/demo_04_rag_pipeline.py` - Pipeline 模式参考

---

**提交方式**: 将代码保存为 `exercises/ex01_embedding_pipeline.py`  
**验收命令**: `python -m pytest exercises/test_ex01.py -v`
