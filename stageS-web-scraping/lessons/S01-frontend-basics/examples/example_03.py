"""示例代码：XPath 表达式实战"""


def xpath_examples() -> dict[str, str]:
    """常用 XPath 表达式示例。
    
    XPath 轴与节点关系：
    - /div: 根节点下的 div
    - //div: 文档中任意位置的 div
    - div/span: div 下的 span 子节点
    - div//span: div 下任意位置的 span 后代
    - @href: 获取 href 属性值
    - text(): 获取文本节点
    """
    examples = {
        "商品名称列表": "//div[@class='product']//a[@class='name']/text()",
        "商品价格": "//span[@class='price'][1]/text()",
        "下一页链接": "//a[@rel='next']/@href",
        "店铺名称": "//span[contains(@class,'shop')]/text()",
        "带属性元素": "//div[@data-id and @data-type='product']",
    }
    return examples


if __name__ == "__main__":
    for name, xpath in xpath_examples().items():
        print(f"{name}: {xpath}")
