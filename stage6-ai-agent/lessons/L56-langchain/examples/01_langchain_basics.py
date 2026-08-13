"""

from __future__ import annotations

L48示例: LangChain基础

学习目标:
- LangChain架构
- Chain组合
- Prompt模板

注意: 此示例需要 langchain 和 langchain-openai 包。
运行前请确保已安装: uv add langchain langchain-openai
"""

# 条件导入：如果包不可用，跳过执行
try:
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import StrOutputParser
    from langchain_openai import ChatOpenAI

    _LANGCHAIN_AVAILABLE = True
except ImportError:
    _LANGCHAIN_AVAILABLE = False
    print("⚠️ 警告: langchain 或 langchain-openai 未安装")
    print("   请运行: uv add langchain langchain-openai")
    print("   示例代码将在下方显示，请阅读理解。")

# 1. 基础Chain
print("=== 1. 基础Chain ===")

if _LANGCHAIN_AVAILABLE:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_template("告诉我关于{topic}的3个要点")
    chain = prompt | llm | StrOutputParser()
    # result = chain.invoke({"topic": "Python"})
    # print(result)
    print("Chain结构: Prompt → LLM → Parser")
else:
    # 演示用代码结构
    print("# llm = ChatOpenAI(model='gpt-3.5-turbo')")
    print("# prompt = ChatPromptTemplate.from_template('告诉我关于{topic}的3个要点')")
    print("# chain = prompt | llm | StrOutputParser()")

# 2. Prompt模板
print("\n=== 2. Prompt模板 ===")

if _LANGCHAIN_AVAILABLE:
    prompt_with_system = ChatPromptTemplate.from_messages(
        [("system", "你是一个{role}助手"), ("human", "{input}")]
    )
    chain2 = prompt_with_system | llm | StrOutputParser()
    print("Prompt模板已创建")
else:
    print("# prompt_with_system = ChatPromptTemplate.from_messages([")
    print("#     ('system', '你是一个{role}助手'),")
    print("#     ('human', '{input}')")
    print("# ])")

# 3. 多步Chain
print("\n=== 3. 多步Chain ===")

if _LANGCHAIN_AVAILABLE:
    topic_prompt = ChatPromptTemplate.from_template("给我一个关于{subject}的有趣主题")
    topic_chain = topic_prompt | llm | StrOutputParser()
    explain_prompt = ChatPromptTemplate.from_template("详细解释: {topic}")
    explain_chain = explain_prompt | llm | StrOutputParser()
    print("多步Chain结构:")
    print("  Step 1: 生成主题")
    print("  Step 2: 详细解释")
else:
    print("# topic_prompt = ChatPromptTemplate.from_template('给我一个关于{subject}的有趣主题')")
    print("# topic_chain = topic_prompt | llm | StrOutputParser()")
    print("# explain_prompt = ChatPromptTemplate.from_template('详细解释: {topic}')")
    print("# explain_chain = explain_prompt | llm | StrOutputParser()")

# 4. 实际应用示例
print("\n=== 4. 实际应用 ===")


def create_qa_chain():
    """创建问答Chain"""
    if not _LANGCHAIN_AVAILABLE:
        return None
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的Python导师"),
            ("human", "问题: {question}\n\n请提供简洁的答案。"),
        ]
    )
    return qa_prompt | llm | StrOutputParser()


if _LANGCHAIN_AVAILABLE:
    qa_chain = create_qa_chain()
    print("✅ QA Chain已创建")
    print("\n示例用法:")
    print("qa_chain.invoke({'question': 'Python中async/await如何工作?'})")
else:
    print("✅ create_qa_chain() 函数已定义（需要 langchain 包才能运行）")
