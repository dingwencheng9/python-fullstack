"""

from __future__ import annotations

练习 1: 向量嵌入管道

任务：
实现高效的文本向量化管道，支持批处理和缓存优化。

学习目标：
- 实现文本预处理和分词
- 使用批处理提升向量化性能
- 实现向量缓存机制
- 优化内存使用

预计时间: 60 分钟
难度: ⭐⭐⭐⭐☆
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

# ============================================================================
# TODO 1: 定义嵌入配置
# ============================================================================


@dataclass
class EmbeddingConfig:
    """嵌入配置

    Args:
        model_name: 嵌入模型名称
        dimension: 向量维度
        batch_size: 批处理大小
        cache_dir: 缓存目录
    """

    model_name: str = "text-embedding-ada-002"
    dimension: int = 1536
    batch_size: int = 32
    cache_dir: str = "./embedding_cache"


# ============================================================================
# TODO 2: 实现文本预处理
# ============================================================================


class TextPreprocessor:
    """文本预处理器"""

    def __init__(self):
        # TODO: 初始化
        pass

    def clean_text(self, text: str) -> str:
        """清理文本

        任务:
        1. 移除多余空格
        2. 转换为小写
        3. 移除特殊字符（可选）

        Args:
            text: 原始文本

        Returns:
            清理后的文本
        """
        # TODO: 实现文本清理

    def tokenize(self, text: str) -> list[str]:
        """分词

        Args:
            text: 清理后的文本

        Returns:
            词汇列表
        """
        # TODO: 实现简单分词（按空格分割）

    def truncate(self, text: str, max_tokens: int = 512) -> str:
        """截断文本

        Args:
            text: 原始文本
            max_tokens: 最大token数

        Returns:
            截断后的文本
        """
        # TODO: 实现文本截断


# ============================================================================
# TODO 3: 实现嵌入缓存
# ============================================================================


class EmbeddingCache:
    """嵌入缓存（避免重复计算）"""

    def __init__(self, cache_dir: str = "./embedding_cache"):
        # TODO: 初始化缓存目录
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, text: str, model_name: str) -> str:
        """生成缓存键

        Args:
            text: 文本内容
            model_name: 模型名称

        Returns:
            缓存键（MD5哈希）
        """
        # TODO: 实现缓存键生成
        # 提示: 使用 hashlib.md5

    def get(self, text: str, model_name: str) -> np.ndarray | None:
        """从缓存获取嵌入

        Args:
            text: 文本内容
            model_name: 模型名称

        Returns:
            嵌入向量，如果不存在返回None
        """
        # TODO: 实现缓存读取

    def set(self, text: str, model_name: str, embedding: np.ndarray) -> None:
        """保存嵌入到缓存

        Args:
            text: 文本内容
            model_name: 模型名称
            embedding: 嵌入向量
        """
        # TODO: 实现缓存写入

    def clear(self) -> None:
        """清空缓存"""
        # TODO: 删除所有缓存文件


# ============================================================================
# TODO 4: 实现批处理嵌入器
# ============================================================================


class BatchEmbedder:
    """批处理嵌入器（提升性能）"""

    def __init__(self, config: EmbeddingConfig):
        # TODO: 初始化
        self.config = config
        self.preprocessor = TextPreprocessor()
        self.cache = EmbeddingCache(config.cache_dir)

    def _mock_embedding_api(self, texts: list[str]) -> list[np.ndarray]:
        """模拟嵌入API调用

        生产环境中替换为真实的API:
        - OpenAI: openai.embeddings.create()
        - HuggingFace: sentence_transformers

        Args:
            texts: 文本列表

        Returns:
            嵌入向量列表
        """
        # TODO: 实现模拟嵌入（随机向量）
        # 提示: 使用 np.random.randn

    def embed_batch(self, texts: list[str], use_cache: bool = True) -> list[np.ndarray]:
        """批量嵌入文本

        Args:
            texts: 文本列表
            use_cache: 是否使用缓存

        Returns:
            嵌入向量列表
        """
        # TODO: 实现批量嵌入
        # 1. 预处理文本
        # 2. 检查缓存
        # 3. 批量调用API
        # 4. 保存到缓存

    def embed_documents(self, documents: list[str], show_progress: bool = True) -> np.ndarray:
        """嵌入文档列表（带进度显示）

        Args:
            documents: 文档列表
            show_progress: 是否显示进度

        Returns:
            嵌入矩阵 (n_docs, dimension)
        """
        # TODO: 实现文档嵌入
        # 1. 分批处理
        # 2. 显示进度
        # 3. 拼接结果


# ============================================================================
# TODO 5: 实现嵌入管道
# ============================================================================


class EmbeddingPipeline:
    """完整的嵌入管道"""

    def __init__(self, config: EmbeddingConfig | None = None):
        # TODO: 初始化组件
        self.config = config or EmbeddingConfig()
        self.embedder = BatchEmbedder(self.config)
        self.statistics: dict[str, Any] = {}

    def process(self, documents: list[str], use_cache: bool = True) -> dict[str, Any]:
        """处理文档并返回嵌入

        Args:
            documents: 文档列表
            use_cache: 是否使用缓存

        Returns:
            结果字典，包含嵌入和统计信息
        """
        # TODO: 实现完整管道
        # 1. 嵌入文档
        # 2. 计算统计信息
        # 3. 返回结果

    def get_statistics(self) -> dict[str, Any]:
        """获取统计信息"""
        # TODO: 返回处理统计


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1: 向量嵌入管道")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现文本预处理")
    print("  2. 实现嵌入缓存")
    print("  3. 实现批处理嵌入")
    print("  4. 构建完整管道")
    print("\n核心优化：")
    print("  - 批处理: 减少API调用次数")
    print("  - 缓存: 避免重复计算")
    print("  - 预处理: 提高嵌入质量")
    print("\n提示：")
    print("  - 使用 numpy 向量化操作")
    print("  - 缓存使用 MD5 哈希作为键")
    print("  - 批处理大小建议 32-128")
    print()
