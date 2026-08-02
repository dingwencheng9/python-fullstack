"""

from __future__ import annotations

L48练习: LangChain基础

任务: 实现一个问答Chain
"""


def create_qa_chain(topic: str):
    """
    创建问答Chain

    要求:
    1. 使用ChatPromptTemplate创建提示模板
    2. 模板应该包含system和human消息
    3. 组合成完整的chain

    参数:
        topic: 问答主题 (如 "Python编程")

    返回:
        可调用的Chain对象
    """
    # ========================================
    # 👉 TODO: 实现 QA Chain
    # ========================================

    # 步骤 1: 导入必要的模块
    # from langchain_core.prompts import ChatPromptTemplate
    # from langchain_openai import ChatOpenAI
    # 或用于测试: from langchain_core.language_models.fake_chat_models import FakeChatModel

    # 步骤 2: 创建 Prompt Template
    # 使用 ChatPromptTemplate.from_messages() 创建模板
    #
    # 示例:
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", f"你是一个{topic}领域的专家，请回答用户的问题"),
    #     ("human", "{question}")
    # ])
    #
    # 说明:
    # - system 消息: 设定 AI 的角色和行为
    # - human 消息: 用户输入，使用 {question} 作为占位符

    # 步骤 3: 创建 LLM
    #
    # 生产环境:
    # llm = ChatOpenAI(
    #     model="gpt-3.5-turbo",
    #     temperature=0  # 0 = 确定性输出，1 = 更有创意
    # )
    #
    # 测试环境（不需要 API key）:
    # llm = FakeChatModel(responses=["这是一个模拟回答"])

    # 步骤 4: 组合 Chain
    # 使用 LCEL (LangChain Expression Language) 的 | 操作符
    #
    # chain = prompt | llm
    #
    # 说明:
    # - | 操作符将组件连接成 Chain
    # - 数据流: 输入 → prompt → llm → 输出
    # - prompt.invoke() 返回 ChatPromptValue
    # - llm.invoke() 返回 AIMessage

    # 步骤 5: 返回 Chain
    # return chain

    # 💡 完整示例:
    # from langchain_core.prompts import ChatPromptTemplate
    # from langchain_core.language_models.fake_chat_models import FakeChatModel
    #
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", f"你是一个{topic}领域的专家"),
    #     ("human", "{question}")
    # ])
    # llm = FakeChatModel(responses=["这是一个关于问题的详细回答"])
    # chain = prompt | llm
    # return chain

    # 👉 在下方实现你的代码
    raise NotImplementedError("请实现 create_qa_chain 函数")


# 使用示例
# chain = create_qa_chain("Python")
# result = chain.invoke({"question": "什么是装饰器?"})
# print(result)
