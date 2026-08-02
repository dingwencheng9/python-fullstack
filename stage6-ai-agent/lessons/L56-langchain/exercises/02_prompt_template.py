"""练习 2: Prompt 模板。

from __future__ import annotations

创建 PromptTemplate 并使用格式化的参数调用。
"""

from langchain.prompts import PromptTemplate


# ========================================
# 📝 练习：实现 LangChain Prompt 模板
#
# 🎯 目标：掌握 LangChain PromptTemplate 的创建和使用
#
# 📌 要求：
# 1. 创建一个带变量的 PromptTemplate
# 2. 使用 format() 方法格式化 prompt
# 3. 处理多个变量的情况
# 4. 实现一个简单的翻译 prompt
#
# 💡 实现提示：
# - 使用 PromptTemplate.from_template() 或直接初始化
# - 变量用 {variable_name} 表示
# - format() 方法接收关键字参数
# - 可以使用 partial() 预填充部分变量
#
# ✅ 验收标准：
# - 成功创建 PromptTemplate
# - 正确格式化输出
# - 处理多变量场景
# - 输出格式符合预期
# ========================================


def create_simple_prompt() -> PromptTemplate:
    """创建简单的 Prompt 模板

    创建一个包含 {topic} 变量的简单模板。

    Returns:
        PromptTemplate: 配置好的 prompt 模板

    Examples:
        >>> prompt = create_simple_prompt()
        >>> result = prompt.format(topic="Python")
        >>> "Python" in result
        True
    """
    # 👉 TODO: 创建 PromptTemplate
    # 模板示例: "请写一篇关于 {topic} 的文章"
    # 使用 PromptTemplate.from_template() 或
    # PromptTemplate(template="...", input_variables=["topic"])
    raise NotImplementedError


def create_translation_prompt() -> PromptTemplate:
    """创建翻译 Prompt 模板

    创建一个支持 {source_lang}, {target_lang}, {text} 的翻译模板。

    Returns:
        PromptTemplate: 翻译 prompt 模板

    Examples:
        >>> prompt = create_translation_prompt()
        >>> result = prompt.format(
        ...     source_lang="中文",
        ...     target_lang="英文",
        ...     text="你好"
        ... )
        >>> "中文" in result and "英文" in result
        True
    """
    # 👉 TODO: 创建翻译 PromptTemplate
    # 模板示例:
    # """
    # 请将以下 {source_lang} 文本翻译成 {target_lang}：
    #
    # {text}
    #
    # 翻译：
    # """
    raise NotImplementedError


def format_with_partial() -> str:
    """使用 partial 预填充变量

    创建一个模板，使用 partial() 预填充部分变量。

    Returns:
        str: 格式化后的 prompt

    Examples:
        >>> result = format_with_partial()
        >>> isinstance(result, str)
        True
        >>> len(result) > 0
        True
    """
    # 👉 TODO: 实现 partial 使用
    # 1. 创建包含多个变量的 PromptTemplate
    # 2. 使用 prompt.partial(variable="value") 预填充
    # 3. 然后只需要填充剩余变量
    #
    # 示例：
    # prompt = PromptTemplate.from_template("语言: {language}, 主题: {topic}")
    # partial_prompt = prompt.partial(language="Python")
    # result = partial_prompt.format(topic="异步编程")
    raise NotImplementedError


if __name__ == "__main__":
    print("=" * 60)
    print("📝 LangChain Prompt 模板练习")
    print("=" * 60)

    print("\n💡 完成上述函数后，取消下面的注释测试：")
    print()

    # # 测试 1: 简单 prompt
    # print("1. 测试简单 Prompt:")
    # simple_prompt = create_simple_prompt()
    # result1 = simple_prompt.format(topic="人工智能")
    # print(f"   结果: {result1}")
    #
    # # 测试 2: 翻译 prompt
    # print("\n2. 测试翻译 Prompt:")
    # trans_prompt = create_translation_prompt()
    # result2 = trans_prompt.format(
    #     source_lang="英文",
    #     target_lang="中文",
    #     text="Hello, World!"
    # )
    # print(f"   结果: {result2}")
    #
    # # 测试 3: Partial 使用
    # print("\n3. 测试 Partial:")
    # result3 = format_with_partial()
    # print(f"   结果: {result3}")

    print("\n" + "=" * 60)
    print("📚 参考资源:")
    print("   - LangChain Prompts 文档")
    print("   - PromptTemplate API 参考")
    print("=" * 60)
