"""示例代码：CSS 选择器实战"""


def css_select_demo() -> list[str]:
    """演示常用 CSS 选择器。
    
    常用选择器类型：
    - 标签选择器: div, span, a
    - 类选择器: .product, .price
    - ID 选择器: #container, #header
    - 属性选择器: [href], [type="text"]
    - 组合选择器: .product .name, div#container > a
    - 伪类: :first-child, :nth-child(2)
    """
    selectors = {
        "商品卡片名称": ".product-name,\n        .item .title a",
        "商品价格": ".price,\n        [data-price]",
        "店铺名称": ".shop-name,\n        .seller-info span",
        "分页链接": ".pagination a[href*='page']",
    }
    # TODO: 在实际页面中验证选择器
    return list(selectors.keys())


if __name__ == "__main__":
    print("CSS 选择器示例")
