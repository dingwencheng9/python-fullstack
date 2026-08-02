"""L48示例: 使用 mock LLM 演示 LCEL 组合。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableLambda

try:
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnableLambda

    _LANGCHAIN_AVAILABLE = True
except ImportError:
    StrOutputParser = None  # type: ignore[assignment]
    ChatPromptTemplate = None  # type: ignore[assignment]
    RunnableLambda = None  # type: ignore[assignment]
    _LANGCHAIN_AVAILABLE = False


def mock_llm(messages: Any) -> str:
    """模拟 LLM 响应，避免真实网络调用。"""
    last_message = messages[-1].content
    return f"模拟回答: 已收到问题《{last_message}》"


if _LANGCHAIN_AVAILABLE:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个Python课程助教，请用一句话回答。"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | RunnableLambda(mock_llm) | StrOutputParser()
else:
    prompt = None  # type: ignore[assignment]
    chain = None  # type: ignore[assignment]


if __name__ == "__main__":
    if not _LANGCHAIN_AVAILABLE:
        raise SystemExit("请先安装 langchain-core: uv add langchain-core")
    result = chain.invoke({"question": "LCEL 的核心价值是什么？"})
    print(result)
