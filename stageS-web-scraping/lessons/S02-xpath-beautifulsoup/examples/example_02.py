"""示例代码：lxml XPath 高级用法"""
from lxml import etree


html = """
<html>
  <body>
    <div id="list">
      <a href="/movie/1">肖申克的救赎 <em>TOP1</em></a>
      <a href="/movie/2">霸王别姬 <em>TOP2</em></a>
    </div>
  </body>
</html>
"""


def xpath_advanced() -> list[dict[str, str]]:
    """XPath 高级表达式示例。"""
    tree = etree.HTML(html)
    results = []
    
    # 获取所有链接的 href 和文本
    links = tree.xpath("//a")
    for link in links:
        results.append({
            "href": link.get("href", ""),
            "text": "".join(link.itertext()).strip(),
            "class": link.get("class", ""),
        })
    
    # 使用 XPath 函数
    tree.xpath("//a[contains(@href, '/movie/')]/text()")
    tree.xpath("//em[contains(text(), 'TOP')]/../text()")
    
    return results


if __name__ == "__main__":
    print("XPath 高级用法示例")
