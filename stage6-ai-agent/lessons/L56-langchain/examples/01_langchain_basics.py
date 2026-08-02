"""

from __future__ import annotations

L48示例: LangChain基础

学习目标:
- LangChain架构
- Chain组合
- Prompt模板
"""

from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. 基础Chain
print("=== 1. 基础Chain ===")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_template("告诉我关于{topic}的3个要点")

chain = prompt | llm | StrOutputParser()

# result = chain.invoke({"topic": "Python"})
# print(result)
print("Chain结构: Prompt → LLM → Parser")

# 2. Prompt模板
print("\n=== 2. Prompt模板 ===")

prompt_with_system = ChatPromptTemplate.from_messages(
    [("system", "你是一个{role}助手"), ("human", "{input}")]
)

chain2 = prompt_with_system | llm | StrOutputParser()
print("Prompt模板已创建")

# 3. 多步Chain
print("\n=== 3. 多步Chain ===")

# 第一步: 生成主题
topic_prompt = ChatPromptTemplate.from_template("给我一个关于{subject}的有趣主题")
topic_chain = topic_prompt | llm | StrOutputParser()

# 第二步: 详细说明
explain_prompt = ChatPromptTemplate.from_template("详细解释: {topic}")
explain_chain = explain_prompt | llm | StrOutputParser()

print("多步Chain结构:")
print("  Step 1: 生成主题")
print("  Step 2: 详细解释")

# 4. 实际应用示例
print("\n=== 4. 实际应用 ===")


def create_qa_chain():
    """创建问答Chain"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的Python导师"),
            ("human", "问题: {question}\n\n请提供简洁的答案。"),
        ]
    )

    return qa_prompt | llm | StrOutputParser()


qa_chain = create_qa_chain()
print("✅ QA Chain已创建")

print("\n示例用法:")
print("qa_chain.invoke({'question': 'Python中async/await如何工作?'})")
