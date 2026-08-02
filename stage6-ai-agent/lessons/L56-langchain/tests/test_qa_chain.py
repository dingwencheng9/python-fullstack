"""L48 LangChain 基础测试用例。"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

pytest.importorskip("langchain")
pytest.importorskip("langchain_core")
pytest.importorskip("langchain_openai")


@pytest.fixture
def qa_module() -> Any:
    """加载参考答案模块。"""
    return importlib.import_module("solutions.01_qa_chain")


@pytest.mark.parametrize("topic", ["Python", "FastAPI", ""])
def test_create_qa_chain_returns_invokable_chain(
    monkeypatch: pytest.MonkeyPatch,
    qa_module: Any,
    topic: str,
) -> None:
    """测试不同主题都能创建可调用 Chain，包含空主题边界。"""
    runnable_module = pytest.importorskip("langchain_core.runnables")
    fake_llm = runnable_module.RunnableLambda(lambda _messages: "模拟回答")
    monkeypatch.setattr(qa_module, "ChatOpenAI", lambda **_kwargs: fake_llm)

    chain = qa_module.create_qa_chain(topic)

    assert hasattr(chain, "invoke")
    assert chain.invoke({"question": "什么是测试？"}) == "模拟回答"


def test_create_qa_chain_propagates_llm_initialization_error(
    monkeypatch: pytest.MonkeyPatch,
    qa_module: Any,
) -> None:
    """测试 LLM 初始化失败时异常不会被静默吞掉。"""

    def raise_llm_error(**_kwargs: object) -> None:
        raise RuntimeError("LLM 不可用")

    monkeypatch.setattr(qa_module, "ChatOpenAI", raise_llm_error)

    with pytest.raises(RuntimeError, match="LLM 不可用"):
        qa_module.create_qa_chain("Python")


def test_create_qa_chain_accepts_empty_topic(
    monkeypatch: pytest.MonkeyPatch,
    qa_module: Any,
) -> None:
    """测试空主题不会导致异常。"""
    runnable_module = pytest.importorskip("langchain_core.runnables")
    fake_llm = runnable_module.RunnableLambda(lambda _msgs: "空回答")
    monkeypatch.setattr(qa_module, "ChatOpenAI", lambda **_kw: fake_llm)
    chain = qa_module.create_qa_chain("")
    assert chain.invoke({"question": "hi"}) == "空回答"


@pytest.mark.parametrize("question", [None, "", "  "], ids=["none", "empty", "whitespace"])
def test_qa_chain_parametrized_questions(
    monkeypatch: pytest.MonkeyPatch,
    qa_module: Any,
    question: str | None,
) -> None:
    """参数化：各种边界输入。"""
    runnable_module = pytest.importorskip("langchain_core.runnables")
    fake_llm = runnable_module.RunnableLambda(lambda _msgs: "安全回答")
    monkeypatch.setattr(qa_module, "ChatOpenAI", lambda **_kw: fake_llm)
    chain = qa_module.create_qa_chain("default")
    result = chain.invoke({"question": question or ""})
    assert isinstance(result, str)
