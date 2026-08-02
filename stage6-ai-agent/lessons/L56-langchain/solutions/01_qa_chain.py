"""

from __future__ import annotations

L48练习参考答案
"""

from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI


def create_qa_chain(topic: str):
    """创建问答Chain"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [("system", f"你是{topic}领域的专家，请简洁回答问题。"), ("human", "{question}")]
    )

    chain = prompt | llm | StrOutputParser()
    return chain
