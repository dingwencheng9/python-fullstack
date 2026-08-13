"""
L56 LangChain 基础测试用例。

注意：此测试需要完整的 LangChain 包（langchain, langchain-openai），
当前环境仅安装了 langchain-core。测试将在导入时跳过。
"""

from __future__ import annotations

import pytest

# 条件跳过：如果 langchain 包不可用，跳过整个测试
try:
    from langchain.prompts import ChatPromptTemplate  # noqa: F401
    from langchain.schema import StrOutputParser  # noqa: F401
    from langchain_openai import ChatOpenAI  # noqa: F401
except ImportError:
    pytest.skip("需要 langchain 包（uv add langchain langchain-openai）", allow_module_level=True)

from langchain_core.runnables import RunnableLambda


def create_qa_chain(topic: str):
    """创建问答Chain"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [("system", f"你是{topic}领域的专家，请简洁回答问题。"), ("human", "{question}")]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


def test_create_qa_chain_returns_invokable_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    """测试不同主题都能创建可调用 Chain，包含空主题边界。"""
    fake_llm = RunnableLambda(lambda _messages: "模拟回答")
    monkeypatch.setattr("langchain_openai.ChatOpenAI", lambda **_kwargs: fake_llm)

    for topic in ["Python", "FastAPI", ""]:
        chain = create_qa_chain(topic)
        assert callable(chain), f"主题 {topic} 应该返回可调用 chain"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
