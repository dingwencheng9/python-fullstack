# M02: LlamaIndex 高级 RAG

> **课程编号**: M02
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 5-6 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: L57 (RAG 基础)、L54 (Agent 基础)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **深入理解 RAG**：掌握 Advanced RAG 的核心原理
2. **优化检索质量**：实现语义检索、混合检索、重排序
3. **构建生产级系统**：处理大规模文档、高并发场景
4. **评估与调优**：建立 RAG 系统评估体系

---

## 📚 课程内容

### 第一部分：Advanced RAG 架构

#### 1.1 标准 RAG 的局限性

```
标准 RAG 流程：
用户查询 → 嵌入模型 → 向量检索 → Top-K 返回 → LLM 生成

问题：
- 语义相似 ≠ 相关性
- 丢失上下文信息
- 检索结果质量参差不齐
```

#### 1.2 Advanced RAG 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Advanced RAG 架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ 查询变换 │ → │ 混合检索 │ → │  重排序  │ → │  生成  │  │
│  │(Query    │    │(Hybrid   │    │(Rerank)  │    │(Generate)│  │
│  │Transform)│    │Retrieval)│    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       ↓               ↓               ↓                         │
│  - HyDE          - 向量检索        - Cross-Encoder              │
│  - 查询扩展       - 关键词检索      - Cohere Rerank             │
│  - 查询分解       - 语义缓存        - BGE Rerank                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1.3 核心技术栈

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| **向量数据库** | Qdrant / Milvus / Weaviate | 存储和检索向量 |
| **嵌入模型** | BGE / M3E / OpenAI Embedding | 文本向量化 |
| **重排序模型** | BGE-Reranker / Cohere | 优化检索结果 |
| **LLM** | GPT-4 / Claude / 本地模型 | 答案生成 |

---

### 第二部分：查询变换

#### 2.1 HyDE（假设性文档嵌入）

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.prompts import PromptTemplate
from pydantic import BaseModel
import asyncio

class HyDEQueryTransform(BaseModel):
    """HyDE 查询变换"""
    llm: any  # LLM 实例

    async def atransform(self, query_str: str) -> str:
        """
        HyDE 核心思想：
        1. 让 LLM 生成一个"假设性答案"
        2. 用这个假设性答案去检索
        3. 因为假设性答案包含了答案的结构，更容易找到相关文档
        """
        hyde_prompt = f"""Given a question, generate a hypothetical passage
that directly answers the question:

Question: {query_str}

Hypothetical Passage:"""

        # 调用 LLM 生成假设性答案
        hypothetical_doc = await self.llm.acomplete(hyde_prompt)

        # 用假设性答案进行检索
        return str(hypothetical_doc)


class AdvancedRAGPipeline:
    """高级 RAG 管道"""

    def __init__(self, llm, embed_model, reranker):
        self.llm = llm
        self.embed_model = embed_model
        self.reranker = reranker
        self.hyde_transform = HyDEQueryTransform(llm=llm)

    async def query(self, question: str) -> str:
        """执行高级 RAG 查询"""
        # Step 1: HyDE 查询变换
        transformed_query = await self.hyde_transform.atransform(question)

        # Step 2: 混合检索（向量 + 关键词）
        vector_results = await self._vector_search(transformed_query, top_k=20)
        bm25_results = await self._bm25_search(question, top_k=20)

        # Step 3: 合并检索结果
        merged_results = self._merge_results(vector_results, bm25_results)

        # Step 4: 重排序
        reranked_results = await self.reranker.rerank(
            query=question,
            documents=merged_results,
            top_n=5
        )

        # Step 5: 生成答案
        context = self._format_context(reranked_results)
        answer = await self._generate(question, context)

        return answer

    async def _vector_search(self, query: str, top_k: int):
        """向量检索"""
        # 实现向量检索逻辑
        pass

    async def _bm25_search(self, query: str, top_k: int):
        """BM25 关键词检索"""
        # 实现 BM25 检索逻辑
        pass

    def _merge_results(self, vector_results, bm25_results):
        """合并检索结果"""
        # 使用 Reciprocal Rank Fusion 合并
        fused_scores = {}
        k = 60  # RRF 参数

        for rank, doc in enumerate(vector_results):
            doc_id = doc["id"]
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank + 1)

        for rank, doc in enumerate(bm25_results):
            doc_id = doc["id"]
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1 / (k + rank + 1)

        # 按分数排序
        sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc for doc_id, _ in sorted_docs]

    async def _generate(self, question: str, context: str) -> str:
        """生成答案"""
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
        return await self.llm.acomplete(prompt)

    def _format_context(self, documents: list) -> str:
        """格式化上下文"""
        return "\n\n".join([
            f"[Document {i+1}]\n{doc.content}"
            for i, doc in enumerate(documents)
        ])
```

#### 2.2 查询分解

```python
from typing import List
from dataclasses import dataclass

@dataclass
class SubQuery:
    """子查询"""
    query_text: str
    reasoning: str
    expected_docs: List[str]

class QueryDecomposer:
    """查询分解器"""

    def __init__(self, llm):
        self.llm = llm

    async def decompose(self, question: str) -> List[SubQuery]:
        """
        将复杂问题分解为多个简单子问题
        """
        decompose_prompt = f"""Decompose the following question into simpler sub-questions
that can be answered independently.

Question: {question}

分解要求：
1. 每个子问题应该能够独立回答
2. 子问题的答案需要能够组合成完整答案
3. 识别需要多跳推理的问题

请以 JSON 格式输出：
{{
    "sub_queries": [
        {{"query": "子问题1", "reasoning": "为什么需要这个子问题"}},
        {{"query": "子问题2", "reasoning": "为什么需要这个子问题"}}
    ]
}}"""

        response = await self.llm.acomplete(decompose_prompt)
        # 解析 JSON 并返回子查询列表
        import json
        data = json.loads(str(response))
        return [
            SubQuery(
                query_text=sq["query"],
                reasoning=sq["reasoning"],
                expected_docs=[]
            )
            for sq in data["sub_queries"]
        ]
```

---

### 第三部分：混合检索与重排序

#### 3.1 混合检索实现

```python
import numpy as np
from typing import List, Tuple

class HybridRetriever:
    """混合检索器"""

    def __init__(self, vector_store, bm25_index, alpha: float = 0.5):
        """
        alpha: 向量检索权重 (1-alpha) 为 BM25 权重
        """
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.alpha = alpha

    async def retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Tuple[dict, float]]:
        """
        执行混合检索
        """
        # 并行执行两种检索
        vector_results = await self.vector_store.search(
            query, top_k=top_k * 2
        )
        bm25_results = self.bm25_index.search(
            query, top_k=top_k * 2
        )

        # 归一化分数
        vector_scores = self._normalize_scores(vector_results)
        bm25_scores = self._normalize_scores(bm25_results)

        # 加权融合
        fused_scores = {}
        for doc_id, score in vector_scores.items():
            fused_scores[doc_id] = self.alpha * score

        for doc_id, score in bm25_scores.items():
            fused_scores[doc_id] = fused_scores.get(doc_id, 0) + (1 - self.alpha) * score

        # 排序返回
        sorted_results = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            (self._get_document(doc_id), score)
            for doc_id, score in sorted_results
        ]

    def _normalize_scores(self, results: dict) -> dict:
        """Min-Max 归一化"""
        if not results:
            return {}

        scores = list(results.values())
        min_score, max_score = min(scores), max(scores)

        if max_score == min_score:
            return {doc_id: 1.0 for doc_id in results}

        return {
            doc_id: (score - min_score) / (max_score - min_score)
            for doc_id, score in results.items()
        }

    def _get_document(self, doc_id: str) -> dict:
        """获取文档"""
        return self.vector_store.get(doc_id)
```

#### 3.2 Cross-Encoder 重排序

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class CrossEncoderReranker:
    """Cross-Encoder 重排序"""

    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()

    async def rerank(
        self,
        query: str,
        documents: List[dict],
        top_n: int = 5
    ) -> List[dict]:
        """
        使用 Cross-Encoder 对文档进行重排序
        """
        if not documents:
            return []

        # 准备输入
        pairs = [(query, doc["content"]) for doc in documents]
        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )

        # 计算相关性分数
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = outputs.logits.squeeze(-1).tolist()

        # 按分数排序
        doc_scores = list(zip(documents, scores))
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        # 添加分数并返回
        reranked = []
        for doc, score in doc_scores[:top_n]:
            doc["rerank_score"] = score
            reranked.append(doc)

        return reranked


class CohereReranker:
    """Cohere Rerank API"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def rerank(
        self,
        query: str,
        documents: List[dict],
        top_n: int = 5,
        model: str = "rerank-multilingual-v2.0"
    ) -> List[dict]:
        """使用 Cohere API 进行重排序"""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.cohere.ai/v1/rerank",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "query": query,
                    "documents": [doc["content"] for doc in documents],
                    "top_n": top_n,
                    "model": model
                }
            )

            result = response.json()

            # 构建映射
            reranked = []
            for item in result["results"]:
                doc = documents[item["index"]].copy()
                doc["rerank_score"] = item["relevance_score"]
                reranked.append(doc)

            return reranked
```

---

### 第四部分：评估体系

#### 4.1 RAG 评估指标

```python
from dataclasses import dataclass
from typing import List
from enum import Enum

class EvaluationMetric(Enum):
    """RAG 评估指标"""
    # 检索指标
    HIT_RATE = "hit_rate"           # 命中率
    MRR = "mrr"                      # 平均倒数排名
    NDCG = "ndcg"                    # 归一化折损累积增益

    # 生成指标
    ROUGE_L = "rouge_l"              # ROUGE-L
    BLEU = "bleu"                    # BLEU
    FIDELITY = "fidelity"            # 答案忠实度

    # 端到端指标
    ANSWER_RELEVANCY = "answer_relevancy"  # 答案相关性
    CONTEXT_PRECISION = "context_precision"      # 上下文精确度
    CONTEXT_RECALL = "context_recall"            # 上下文召回率

@dataclass
class RAGEvaluationResult:
    """RAG 评估结果"""
    retrieval_hit_rate: float
    retrieval_mrr: float
    answer_rouge_l: float
    answer_bleu: float
    answer_relevancy: float
    context_precision: float

    def overall_score(self) -> float:
        """综合得分"""
        weights = {
            "retrieval": 0.3,
            "answer": 0.4,
            "context": 0.3
        }
        return (
            weights["retrieval"] * (self.retrieval_hit_rate + self.retrieval_mrr) / 2 +
            weights["answer"] * (self.answer_rouge_l + self.answer_bleu + self.answer_relevancy) / 3 +
            weights["context"] * self.context_precision
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "retrieval_hit_rate": f"{self.retrieval_hit_rate:.3f}",
            "retrieval_mrr": f"{self.retrieval_mrr:.3f}",
            "answer_rouge_l": f"{self.answer_rouge_l:.3f}",
            "answer_bleu": f"{self.answer_bleu:.3f}",
            "answer_relevancy": f"{self.answer_relevancy:.3f}",
            "context_precision": f"{self.context_precision:.3f}",
            "overall_score": f"{self.overall_score():.3f}"
        }


class RAGEvaluator:
    """RAG 评估器"""

    def __init__(self, llm):
        self.llm = llm

    async def evaluate(
        self,
        test_cases: List[dict],
        rag_pipeline
    ) -> RAGEvaluationResult:
        """
        评估 RAG 系统

        test_cases 格式：
        {
            "question": "问题",
            "ground_truth_contexts": ["相关文档1", "相关文档2"],
            "ground_truth_answer": "标准答案"
        }
        """
        retrieval_hits = []
        retrieval_rrs = []
        answer_rouges = []
        answer_bleus = []
        answer_relevancies = []
        context_precisions = []

        for case in test_cases:
            # 执行 RAG
            answer = await rag_pipeline.query(case["question"])
            retrieved_docs = await rag_pipeline.retrieve(case["question"])

            # 评估检索
            hit = self._evaluate_hit_rate(
                retrieved_docs,
                case["ground_truth_contexts"]
            )
            retrieval_hits.append(hit)

            mrr = self._evaluate_mrr(
                retrieved_docs,
                case["ground_truth_contexts"]
            )
            retrieval_rrs.append(mrr)

            # 评估生成
            rouge = self._evaluate_rouge(answer, case["ground_truth_answer"])
            answer_rouges.append(rouge)

            bleu = self._evaluate_bleu(answer, case["ground_truth_answer"])
            answer_bleus.append(bleu)

            relevancy = await self._evaluate_answer_relevancy(
                answer,
                case["question"]
            )
            answer_relevancies.append(relevancy)

            # 评估上下文
            precision = self._evaluate_context_precision(
                retrieved_docs,
                case["ground_truth_contexts"]
            )
            context_precisions.append(precision)

        return RAGEvaluationResult(
            retrieval_hit_rate=sum(retrieval_hits) / len(retrieval_hits),
            retrieval_mrr=sum(retrieval_rrs) / len(retrieval_rrs),
            answer_rouge_l=sum(answer_rouges) / len(answer_rouges),
            answer_bleu=sum(answer_bleus) / len(answer_bleus),
            answer_relevancy=sum(answer_relevancies) / len(answer_relevancies),
            context_precision=sum(context_precisions) / len(context_precisions)
        )

    def _evaluate_hit_rate(
        self,
        retrieved: List[dict],
        ground_truth: List[str]
    ) -> float:
        """评估命中率"""
        for doc in retrieved:
            if any(gt in doc["content"] for gt in ground_truth):
                return 1.0
        return 0.0

    def _evaluate_mrr(
        self,
        retrieved: List[dict],
        ground_truth: List[str]
    ) -> float:
        """评估 MRR"""
        for i, doc in enumerate(retrieved):
            if any(gt in doc["content"] for gt in ground_truth):
                return 1.0 / (i + 1)
        return 0.0

    def _evaluate_rouge(self, answer: str, reference: str) -> float:
        """评估 ROUGE-L（简化版）"""
        # 实际应使用 rouge_score 库
        common = sum(1 for a, b in zip(answer, reference) if a == b)
        return common / max(len(reference), 1)

    def _evaluate_bleu(self, answer: str, reference: str) -> float:
        """评估 BLEU（简化版）"""
        # 实际应使用 nltk.translate.bleu_score
        return self._evaluate_rouge(answer, reference)  # 简化

    async def _evaluate_answer_relevancy(
        self,
        answer: str,
        question: str
    ) -> float:
        """评估答案相关性"""
        prompt = f"""评估答案与问题的相关性，输出 0-1 之间的分数。

问题：{question}
答案：{answer}

相关性分数："""
        result = await self.llm.acomplete(prompt)
        try:
            return float(str(result).strip())
        except:
            return 0.5

    def _evaluate_context_precision(
        self,
        retrieved: List[dict],
        ground_truth: List[str]
    ) -> float:
        """评估上下文精确度"""
        if not retrieved:
            return 0.0

        relevant = sum(
            1 for doc in retrieved
            if any(gt in doc["content"] for gt in ground_truth)
        )
        return relevant / len(retrieved)
```

---

## 🚀 实战案例

### 案例：企业知识库问答系统

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import asyncio

@dataclass
class Document:
    """文档"""
    id: str
    content: str
    metadata: dict = field(default_factory=dict)
    embedded_at: datetime = field(default_factory=datetime.now)

@dataclass
class QueryResult:
    """查询结果"""
    document: Document
    score: float
    rerank_score: Optional[float] = None

class EnterpriseKnowledgeBase:
    """企业知识库"""

    def __init__(
        self,
        vector_store,
        bm25_index,
        reranker,
        llm
    ):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.reranker = reranker
        self.llm = llm
        self.hybrid_retriever = HybridRetriever(
            vector_store,
            bm25_index,
            alpha=0.7
        )

    async def add_documents(self, documents: List[Document]) -> None:
        """添加文档"""
        for doc in documents:
            # 向量化
            embedding = await self._embed(doc.content)
            self.vector_store.add(doc.id, embedding, doc.content)

            # BM25 索引
            self.bm25_index.add(doc.id, doc.content)

    async def query(
        self,
        question: str,
        top_k: int = 5,
        use_hyde: bool = True
    ) -> dict:
        """查询"""
        # 查询变换
        if use_hyde:
            transformed_query = await self._hyde_transform(question)
        else:
            transformed_query = question

        # 混合检索 + 重排序
        results = await self.hybrid_retriever.retrieve(
            transformed_query,
            top_k=top_k * 2
        )

        reranked = await self.reranker.rerank(
            question,
            [r[0] for r in results],
            top_n=top_k
        )

        # 生成答案
        context = "\n\n".join([
            f"[{i+1}] {doc['content']}"
            for i, doc in enumerate(reranked)
        ])

        answer = await self._generate_answer(question, context)

        return {
            "answer": answer,
            "sources": reranked,
            "transformed_query": transformed_query
        }

    async def _embed(self, text: str) -> list:
        """获取嵌入向量"""
        # 调用嵌入模型
        pass

    async def _hyde_transform(self, query: str) -> str:
        """HyDE 查询变换"""
        prompt = f"Generate a hypothetical passage answering: {query}"
        return str(await self.llm.acomplete(prompt))

    async def _generate_answer(self, question: str, context: str) -> str:
        """生成答案"""
        prompt = f"""Based on the context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
        return str(await self.llm.acomplete(prompt))
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 Advanced RAG 的核心组件和工作原理
- [ ] 实现 HyDE、查询分解等查询变换技术
- [ ] 构建混合检索系统（向量 + BM25）
- [ ] 使用 Cross-Encoder 或 Cohere 进行重排序
- [ ] 建立完整的 RAG 评估体系
- [ ] 优化企业知识库问答系统的性能

---

## 🔗 相关资源

- [LlamaIndex 文档](https://docs.llamaindex.ai/)
- [BGE 嵌入模型](https://github.com/FlagOpen/FlagEmbedding)
- [Cohere Rerank API](https://docs.cohere.com/reference/rerank)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M03: MLOps 实验追踪
- 学习 M04: Litestar 框架
- 探索 M05: RAG 深度优化

---

**最后更新**: 2026-07-18
