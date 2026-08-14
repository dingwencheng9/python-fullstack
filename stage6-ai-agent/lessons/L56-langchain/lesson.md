L56: LangChain 与应用编排 - 详细教程

> **课程编号**: L56
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 6-7 小时
> **难度**: ⭐⭐⭐☆☆（中级）
> **前置课程**: L55 MCP 协议
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

>
> 1. 理解 LLM 基本原理和 API 调用方式
> 2. 掌握 Prompt Engineering 基础
> 3. 能使用 LCEL53 表达式构建 Chain
> 4. 能解析 LLM 结构化输出

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L54**: Agent 基础（理解 LLM 与工具调用）
- **L55**: MCP 协议（理解标准化工具集成）
- **可选** L19（异步编程）：了解 async/await 基础

**如果你还没有学习以上课程，建议先完成前置课程。**

> 💡 **跃升预警**: 本课程是 Stage 4（数据智能）→ Stage 5（AI Agent）的桥梁。
> 如果你刚完成 Stage 4 的数据分析，这一课会帮你理解"数据分析完了，AI Agent 怎么用这些数据"。

---

## Part 0: LLM 快速入门（新增 2h）

> 本部分解决 Stage 4→5 的跃升问题：很多数据分析师/工程师对 LLM 只有概念认知，缺少动手经验。

### 0.1 什么是大语言模型（LLM）？

**一句话**: LLM 是一个能理解和生成自然语言的超级预测机——你给它一段文本，它预测下一段最合理的文本。

**通俗类比**:

```yaml
传统程序:  输入 → 规则推理 → 输出  (if-else)
LLM:      输入 + 上下文 → 概率预测 → 输出  (神经网络)
```python
**关键概念**:

| 概念                | 含义               | 类比               |
| ------------------- | ------------------ | ------------------ |
| **模型 (Model)**    | 训练好的神经网络   | 一个训练有素的员工 |
| **提示词 (Prompt)** | 你发给模型的指令   | 任务描述           |
| **Token**           | 模型处理的基本单位 | 单词或子词的碎片   |
| **Temperature**     | 0=确定性, 1=创造性 | 严谨 vs 发散思维   |
| **Completion**      | 模型返回的文本     | 员工完成的成果     |

### 0.2 第一次 API 调用

```python
import os
from openai import OpenAI

# 从环境变量读取 API Key（不要在代码中硬编码！）
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 最简单的调用
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "什么是 Python？用一句话回答。"},
    ],
    temperature=0.7,
    max_tokens=100,
)

print(response.choices[0].message.content)
```ini
**核心参数解读**:

```python
# temperature: 0.0 → 确定性强（适合事实问答）
# temperature: 1.0 → 创意性强（适合写作、头脑风暴）
# max_tokens: 限制输出长度，节省成本

# 不同场景的选择:
# 数学计算: temperature=0.0, max_tokens=500
# 客服回复: temperature=0.3, max_tokens=200
# 创意写作: temperature=0.8, max_tokens=2000
```yaml
### 0.3 使用本地模型（Ollama / 无需 API Key）

不需要 OpenAI 付费也能运行 LLM：

```bash
# 安装 Ollama
curl -fsSL53 https://ollama.com/install.sh | sh

# 下载模型（下载一次，之后本地可用）
ollama pull llama3.2  # 约 2GB
# 或更小的模型
ollama pull qwen2.5:0.5b  # 约 400MB

# 启动服务
ollama serve
from langchain_ollama import ChatOllama

# 本地模型，无需 API Key
llm = ChatOllama(model="llama3.2", temperature=0)
response = llm.invoke("什么是 Python？")
print(response.content)
```yaml
**OpenAI vs Ollama 对比**:

| 维度         | OpenAI (云端) | Ollama (本地)   |
| ------------ | ------------- | --------------- |
| 需要 API Key | ✅ 是         | ❌ 否           |
| 需要网络     | ✅ 是         | ❌ 否（下载后） |
| 费用         | 按 Token 计费 | 免费            |
| 质量         | 最高          | 取决于模型      |
| 适用         | 生产/研究     | 本地开发/学习   |

### 0.4 Prompt Engineering 基础

**原则 1: 角色设定**

```python
# ❌ 差
"写一个排序函数"

# ✅ 好 — 给 LLM 设定角色和约束
"""你是一个 Python 高级工程师。请：
1. 写一个 merge_sort 函数
2. 包含类型标注
3. 包含 docstring
4. 处理空列表的边界条件
"""
```yaml
**原则 2: Few-Shot（给示例）**

```python
# Few-Shot: 给 2-3 个示例，LLM 会模仿格式
prompt = """将以下英文翻译为中文：

示例 1:
EN: Hello, world!
ZH: 你好，世界！

示例 2:
EN: Machine learning is powerful.
ZH: 机器学习很强大。

现在翻译:
EN: {user_input}
ZH:"""
```yaml
**原则 3: Chain of Thought（思维链）**

```python
# 简单的"问→答"容易出错，让 LLM "展示推理过程"
prompt = """问题: 一个篮子里有 5 个苹果，小明吃掉 2 个，小红又放了 3 个。
现在有几个苹果？

请逐步推理:
步骤 1: 初始有几个苹果？
步骤 2: 小明做了什么？还剩几个？
步骤 3: 小红做了什么？现在有几个？
步骤 4: 最终答案。
"""
```python
### 0.5 Token 与成本

**Token 是什么**: LLM 不直接看"汉字/字母"，而是把文本切成 token。

```python
# 粗略估算（实际因模型而异）
"Hello"        → 1 token
"Python"       → 1 token
"机器学习"     → 2-3 tokens
"一个很长的句子" → 4-6 tokens

# 1000 tokens ≈ 750 个英文单词 ≈ 400 个汉字
```python
**成本估算**（以 gpt-4o-mini 为例）:

```yaml
输入:   $0.15/1M tokens
输出:   $0.60/1M tokens

一个典型对话 (1000 tokens 输入 + 200 tokens 输出):
成本 ≈ $0.00015 + $0.00012 = $0.00027 ≈ 0.2 分人民币
```python
> 💡 这就是为什么用 `max_tokens` 限制输出长度：100 tokens vs 4000 tokens 成本差 40 倍。

### 0.6 实战：写一个完整的 LLM 调用

```python
import os
from openai import OpenAI


def ask_llm(
    question: str,
    role: str = "你是一个有帮助的助手。",
    temperature: float = 0.3,
) -> str:
    """封装一个可复用的 LLM 调用函数。

    这是进入 LangChain 之前的"原生体验"——
    理解这些参数，才能理解 LangChain 在封装什么。
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": question},
        ],
        temperature=temperature,
        max_tokens=500,
    )

    return response.choices[0].message.content or ""


# 使用
if __name__ == "__main__":
    answer = ask_llm("什么是 Docker？用一句话解释。")
    print(answer)
```python
> 📖 这个函数就是 LangChain 在封装的底层逻辑。理解了它，再看下面的 LCEL53 就会明白 LangChain 的价值：帮你管理 prompt 模板、输出解析、流式调用等重复模式。

---

## 📚 目录

- [Part 0: LLM 快速入门](#part-0-llm-快速入门新增-2h)
- [第一章：LCEL53 表达式语言](#第一章lcel-表达式语言)
- [第二章：Prompt 工程](#第二章prompt-工程)
- [第三章：Chain 组合模式](#第三章chain-组合模式)
- [第四章：输出解析与结构化](#第四章输出解析与结构化)

---

## 第一章：LCEL53 表达式语言

### 1.1 基础 Chain (管道符 |)

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 定义组件
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_template("告诉我关于 {topic} 的 3 个事实")
parser = StrOutputParser()

# 2. LCEL53 管道组合
chain = prompt | llm | parser

# 3. 调用
result = chain.invoke({"topic": "Python"})
print(result)
```python
**LCEL53 核心优势**:

- ✅ 声明式语法 (可读性强)
- ✅ 自动批处理支持
- ✅ 流式输出支持
- ✅ 异步/并发支持

---

### 1.2 Runnable 接口

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# 所有 LangChain 组件都是 Runnable
chain = (
    RunnablePassthrough.assign(topic=lambda x: x["input"].upper())
    | prompt
    | llm
    | parser
)

result = chain.invoke({"input": "python"})
```python
**Runnable 核心方法**:

- `invoke()`: 单次调用
- `batch()`: 批量调用
- `stream()`: 流式调用
- `ainvoke()`: 异步调用

---

### 1.3 流式输出

```python
# 流式生成
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```python
---

## 第二章：Prompt 工程

### 2.1 ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

# 方式 1: 简单模板
prompt = ChatPromptTemplate.from_template(
    "你是一个 {role}，回答关于 {topic} 的问题"
)

# 方式 2: 多消息模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的 {role}"),
    ("human", "{input}"),
    ("ai", "我理解了，让我来回答"),
    ("human", "请详细说明")
])

# 格式化
messages = prompt.format_messages(
    role="Python 导师",
    input="什么是装饰器？"
)
```python
---

### 2.2 Few-Shot Prompt

```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

# 示例数据
examples = [
    {"input": "快乐", "output": "😊"},
    {"input": "悲伤", "output": "😢"},
]

# Few-shot 模板
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# 完整 Prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "将情绪词转换为 emoji"),
    few_shot_prompt,
    ("human", "{input}"),
])

chain = final_prompt | llm | parser
result = chain.invoke({"input": "兴奋"})  # 输出: 🎉
```yaml
---

### 2.3 Prompt 模板变量

```python
# 部分变量绑定
prompt = ChatPromptTemplate.from_template(
    "角色: {role}\n语言: {language}\n任务: {task}"
)

# 绑定固定变量
partial_prompt = prompt.partial(role="Python 导师", language="中文")

# 后续只需提供 task
chain = partial_prompt | llm | parser
result = chain.invoke({"task": "讲解列表推导式"})
```python
---

## 第三章：Chain 组合模式

### 3.1 Sequential Chain (顺序)

```python
from langchain_core.runnables import RunnablePassthrough

# Chain 1: 生成主题
topic_chain = (
    ChatPromptTemplate.from_template("为 {subject} 生成一个有趣的话题")
    | llm
    | StrOutputParser()
)

# Chain 2: 详细说明
detail_chain = (
    ChatPromptTemplate.from_template("详细解释: {topic}")
    | llm
    | StrOutputParser()
)

# 组合: Chain1 输出 → Chain2 输入
full_chain = (
    {"topic": topic_chain}
    | RunnablePassthrough.assign(detail=detail_chain)
)

result = full_chain.invoke({"subject": "量子计算"})
print(result["topic"])   # 主题
print(result["detail"])  # 详细说明
```python
---

### 3.2 Parallel Chain (并行)

```python
from langchain_core.runnables import RunnableParallel

# 并行执行多个 Chain
parallel_chain = RunnableParallel({
    "summary": ChatPromptTemplate.from_template("总结: {text}") | llm,
    "keywords": ChatPromptTemplate.from_template("提取关键词: {text}") | llm,
    "sentiment": ChatPromptTemplate.from_template("情感分析: {text}") | llm,
})

result = parallel_chain.invoke({"text": "今天天气很好，心情愉快！"})
# 返回: {"summary": ..., "keywords": ..., "sentiment": ...}
```python
---

### 3.3 Router Chain (路由)

```python
from langchain_core.runnables import RunnableBranch

# 根据输入路由到不同 Chain
branch_chain = RunnableBranch(
    (
        lambda x: "代码" in x["input"],
        ChatPromptTemplate.from_template("生成代码: {input}") | llm
    ),
    (
        lambda x: "解释" in x["input"],
        ChatPromptTemplate.from_template("解释概念: {input}") | llm
    ),
    ChatPromptTemplate.from_template("通用回答: {input}") | llm  # 默认
)

result = branch_chain.invoke({"input": "生成代码: 快速排序"})
```python
---

## 第四章：输出解析与结构化

### 4.1 Pydantic 输出解析器

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 定义输出结构
class Person(BaseModel):
    name: str = Field(description="人名")
    age: int = Field(description="年龄")
    hobbies: list[str] = Field(description="爱好列表")

# 创建解析器
parser = PydanticOutputParser(pydantic_object=Person)

# Prompt 包含格式说明
prompt = ChatPromptTemplate.from_template(
    "提取人物信息:\n{format_instructions}\n\n文本: {text}"
)

chain = (
    prompt.partial(format_instructions=parser.get_format_instructions())
    | llm
    | parser
)

result = chain.invoke({"text": "小明今年25岁，喜欢编程和阅读"})
print(result.name)      # "小明"
print(result.age)       # 25
print(result.hobbies)   # ["编程", "阅读"]
```python
---

### 4.2 JSON 输出解析器

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    "以 JSON 格式返回: {query}\n\n{format_instructions}"
)

chain = (
    prompt.partial(format_instructions=parser.get_format_instructions())
    | llm
    | parser
)

result = chain.invoke({"query": "列出 3 种编程语言"})
# 返回: {"languages": ["Python", "JavaScript", "Go"]}
```python
---

### 4.3 Structured Output (推荐)

```python
from langchain_openai import ChatOpenAI

# OpenAI 原生结构化输出
class MovieReview(BaseModel):
    title: str
    rating: int = Field(ge=1, le=5)
    summary: str

llm_structured = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
    MovieReview
)

prompt = ChatPromptTemplate.from_template("评价电影: {movie}")
chain = prompt | llm_structured

result = chain.invoke({"movie": "肖申克的救赎"})
print(result.title)   # "肖申克的救赎"
print(result.rating)  # 5
```text
---

## 🎯 最佳实践总结

### ✅ LangChain 使用清单

- [ ] 优先使用 LCEL53 (管道符 |)
- [ ] Prompt 模板化管理
- [ ] 使用 Pydantic 定义输出结构
- [ ] 并行执行独立任务 (RunnableParallel)
- [ ] 异常处理和重试机制
- [ ] 使用流式输出改善用户体验

### 常见模式

**模式 1: 数据提取**

```python
Prompt (提取指令) | LLM | Pydantic 解析器
```python
**模式 2: 多步推理**

```python
Chain1 (生成) | Chain2 (验证) | Chain3 (格式化)
```python
**模式 3: 并行分析**

```yaml
RunnableParallel({
    "维度1": Chain1,
    "维度2": Chain2,
    "维度3": Chain3
})
```

---

## 🔗 延伸阅读

### 相关课程

- **L53 RAG 系统** - LangChain 实战应用
- **L53 Agent 基础** - 基于 LangChain 的 Agent
- **L53 LangGraph** - 复杂 Agent 编排

### 推荐资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LCEL53 表达式语言](https://python.langchain.com/docs/expression_language/)
- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)

---

## 📝 练习题

### 练习 1: 多语言翻译 Chain

创建翻译管道:

- 检测输入语言
- 翻译为目标语言
- 返回结构化结果 (原文/译文/语言)

### 练习 2: 文本分析 Pipeline

并行分析:

- 情感分析
- 关键词提取
- 摘要生成
- 语言检测

### 练习 3: 智能路由

根据问题类型路由:

- 代码问题 → 代码生成 Chain
- 概念问题 → 解释 Chain
- 数学问题 → 计算 Chain

---

**练习答案**: 参见 `solutions/` 目录

## 🔗 下一步


[L56: Agent 基础与工具调用](../L54-agent-basics/)
