"""

from __future__ import annotations

练习 1: 向量嵌入管道 - 标准答案

【解题思路】

1. 文本预处理策略：
   - 清理：移除多余空格、转小写、移除特殊字符
   - 分词：简单按空格分割（中文需要jieba等工具）
   - 截断：限制最大token数（避免超过模型限制）

2. 嵌入缓存实现：
   - 使用MD5哈希作为缓存键（text + model_name）
   - 缓存文件命名：{md5_hash}.npy
   - 读取时先检查缓存，不存在则计算

3. 批处理优化：
   - 将documents分批（batch_size=32）
   - 每批并行处理，减少API调用次数
   - 显示进度条提升用户体验

4. 嵌入管道设计：
   - 预处理 → 缓存检查 → 批量嵌入 → 缓存保存
   - 统计信息：缓存命中率、总耗时、平均每文档耗时

【关键知识点】

- 文本预处理提升嵌入质量
- 缓存避免重复计算，降低成本
- 批处理提升10-100倍性能
- numpy数组序列化（.npy格式）
- 哈希函数保证缓存一致性

【生产级考量】

- 使用Redis/Memcached做分布式缓存
- 实现异步批处理
- 添加重试机制（API失败）
- 监控缓存命中率
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

import numpy as np

# ============================================================================
# 1. 嵌入配置
# ============================================================================


@dataclass
class EmbeddingConfig:
    """嵌入配置"""

    model_name: str = "text-embedding-ada-002"
    dimension: int = 1536
    batch_size: int = 32
    cache_dir: str = "./embedding_cache"


# ============================================================================
# 2. 文本预处理
# ============================================================================


class TextPreprocessor:
    """文本预处理器"""

    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空格
        text = " ".join(text.split())
        # 转小写
        text = text.lower()
        # 移除特殊字符（保留基本标点）
        # 这里简化处理，生产环境需要更复杂的规则
        return text.strip()

    def tokenize(self, text: str) -> list[str]:
        """分词（简单版本）"""
        return text.split()

    def truncate(self, text: str, max_tokens: int = 512) -> str:
        """截断文本"""
        tokens = self.tokenize(text)
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
        return " ".join(tokens)


# ============================================================================
# 3. 嵌入缓存
# ============================================================================


class EmbeddingCache:
    """嵌入缓存"""

    def __init__(self, cache_dir: str = "./embedding_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)

    def _get_cache_key(self, text: str, model_name: str) -> str:
        """生成缓存键（MD5哈希）"""
        # 组合text和model_name
        combined = f"{model_name}:{text}"
        # 计算MD5哈希
        md5_hash = hashlib.md5(combined.encode("utf-8")).hexdigest()
        return md5_hash

    def get(self, text: str, model_name: str) -> np.ndarray | None:
        """从缓存获取嵌入"""
        cache_key = self._get_cache_key(text, model_name)
        cache_file = self.cache_dir / f"{cache_key}.npy"

        if cache_file.exists():
            try:
                return np.load(cache_file)
            except Exception as e:
                print(f"⚠️  缓存读取失败: {e}")
                return None

        return None

    def set(self, text: str, model_name: str, embedding: np.ndarray) -> None:
        """保存嵌入到缓存"""
        cache_key = self._get_cache_key(text, model_name)
        cache_file = self.cache_dir / f"{cache_key}.npy"

        try:
            np.save(cache_file, embedding)
        except Exception as e:
            print(f"⚠️  缓存写入失败: {e}")

    def clear(self) -> None:
        """清空缓存"""
        for cache_file in self.cache_dir.glob("*.npy"):
            cache_file.unlink()
        print("✅ 缓存已清空")


# ============================================================================
# 4. 批处理嵌入器
# ============================================================================


class BatchEmbedder:
    """批处理嵌入器"""

    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.preprocessor = TextPreprocessor()
        self.cache = EmbeddingCache(config.cache_dir)

    def _mock_embedding_api(self, texts: list[str]) -> list[np.ndarray]:
        """模拟嵌入API调用

        生产环境替换为：
        import openai
        response = openai.embeddings.create(
            model=self.config.model_name,
            input=texts
        )
        """
        embeddings = []
        for text in texts:
            # 使用文本哈希生成一致的随机向量
            seed = hash(text) % (2**32)
            np.random.seed(seed)
            vec = np.random.randn(self.config.dimension)
            vec = vec / np.linalg.norm(vec)  # 归一化
            embeddings.append(vec)

        return embeddings

    def embed_batch(self, texts: list[str], use_cache: bool = True) -> list[np.ndarray]:
        """批量嵌入文本"""
        embeddings = []
        cache_hits = 0
        texts_to_embed = []
        text_indices = []

        # 1. 预处理和缓存检查
        for i, text in enumerate(texts):
            # 预处理
            cleaned = self.preprocessor.clean_text(text)
            cleaned = self.preprocessor.truncate(cleaned, max_tokens=512)

            # 检查缓存
            if use_cache:
                cached = self.cache.get(cleaned, self.config.model_name)
                if cached is not None:
                    embeddings.append(cached)
                    cache_hits += 1
                    continue

            # 需要嵌入
            texts_to_embed.append(cleaned)
            text_indices.append(i)
            embeddings.append(None)  # 占位

        # 2. 批量调用API（仅对缓存未命中的文本）
        if texts_to_embed:
            new_embeddings = self._mock_embedding_api(texts_to_embed)

            # 3. 保存到缓存并填充结果
            for idx, embedding in zip(text_indices, new_embeddings, strict=False):
                embeddings[idx] = embedding
                if use_cache:
                    self.cache.set(texts_to_embed[text_indices.index(idx)], self.config.model_name, embedding)

        if use_cache:
            cache_hit_rate = cache_hits / len(texts) * 100 if texts else 0
            print(f"  缓存命中率: {cache_hit_rate:.1f}% ({cache_hits}/{len(texts)})")

        return embeddings

    def embed_documents(self, documents: list[str], show_progress: bool = True) -> np.ndarray:
        """嵌入文档列表（带进度）"""
        all_embeddings = []
        batch_size = self.config.batch_size

        # 分批处理
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]

            if show_progress:
                print(f"处理批次 {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}...")

            batch_embeddings = self.embed_batch(batch)
            all_embeddings.extend(batch_embeddings)

        # 转换为numpy数组
        return np.array(all_embeddings)


# ============================================================================
# 5. 嵌入管道
# ============================================================================


class EmbeddingPipeline:
    """完整的嵌入管道"""

    def __init__(self, config: EmbeddingConfig | None = None):
        self.config = config or EmbeddingConfig()
        self.embedder = BatchEmbedder(self.config)
        self.statistics: dict[str, any] = {}

    def process(self, documents: list[str], use_cache: bool = True) -> dict[str, any]:
        """处理文档并返回嵌入"""
        import time

        start_time = time.time()

        print(f"\n开始处理 {len(documents)} 个文档...")
        print(f"  模型: {self.config.model_name}")
        print(f"  维度: {self.config.dimension}")
        print(f"  批大小: {self.config.batch_size}")

        # 嵌入文档
        embeddings = self.embedder.embed_documents(documents, show_progress=True)

        elapsed = time.time() - start_time

        # 统计信息
        self.statistics = {
            "total_documents": len(documents),
            "embedding_dimension": self.config.dimension,
            "total_time_seconds": elapsed,
            "avg_time_per_doc": elapsed / len(documents) if documents else 0,
            "cache_enabled": use_cache,
        }

        print("\n✅ 处理完成！")
        print(f"  总耗时: {elapsed:.2f}秒")
        print(f"  平均: {elapsed / len(documents):.4f}秒/文档")

        return {
            "embeddings": embeddings,
            "statistics": self.statistics,
        }

    def get_statistics(self) -> dict[str, any]:
        """获取统计信息"""
        return self.statistics


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1: 向量嵌入管道 - 标准答案")
    print("=" * 70)

    # 创建测试文档
    documents = [
        "Python是一种高级编程语言",
        "机器学习需要大量的数据",
        "深度学习是机器学习的一个分支",
        "自然语言处理用于理解人类语言",
        "向量嵌入是NLP的核心技术",
    ]

    # 创建管道
    config = EmbeddingConfig(dimension=128, batch_size=2)
    pipeline = EmbeddingPipeline(config)

    # 第一次处理（无缓存）
    print("\n第一次处理（无缓存）：")
    result1 = pipeline.process(documents, use_cache=True)

    # 第二次处理（有缓存）
    print("\n第二次处理（应该命中缓存）：")
    result2 = pipeline.process(documents, use_cache=True)

    print("\n嵌入结果：")
    print(f"  形状: {result1['embeddings'].shape}")
    print(f"  第一个向量: {result1['embeddings'][0][:5]}... (前5维)")
