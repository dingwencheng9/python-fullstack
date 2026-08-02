"""示例代码：HTML 页面解析基础"""
from dataclasses import dataclass


@dataclass
class ProductInfo:
    """商品信息数据模型"""
    name: str
    price: str
    shop: str
    url: str


def parse_product_card(html: str) -> ProductInfo | None:
    """解析商品卡片 HTML，提取商品信息。
    
    示例 HTML 结构：
    <div class="product">
      <a class="name" href="...">商品名称</a>
      <span class="price">¥99.00</span>
      <span class="shop">店铺名</span>
    </div>
    """
    # TODO: 使用正则或 BeautifulSoup 解析
    return None


if __name__ == "__main__":
    sample = '''<div class="product">
      <a class="name" href="/item/123">iPhone 15</a>
      <span class="price">¥5999</span>
      <span class="shop">Apple 旗舰店</span>
    </div>'''
    print("解析示例页面...")
