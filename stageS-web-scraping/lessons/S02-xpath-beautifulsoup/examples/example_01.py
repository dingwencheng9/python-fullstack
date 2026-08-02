"""示例代码：BeautifulSoup 解析 HTML"""
from bs4 import BeautifulSoup


html = """
<html>
  <body>
    <div class="movie">
      <h2>肖申克的救赎</h2>
      <span class="rating">9.7</span>
      <span class="quote">希望是人类最珍贵的东西</span>
    </div>
    <div class="movie">
      <h2>霸王别姬</h2>
      <span class="rating">9.6</span>
      <span class="quote">不疯魔不成活</span>
    </div>
  </body>
</html>
"""


def parse_movies(html: str) -> list[dict[str, str]]:
    """解析豆瓣电影页面。
    
    返回格式: [{"title": "...", "rating": "...", "quote": "..."}, ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    movies = []
    for item in soup.select(".movie"):
        title = item.select_one("h2").get_text(strip=True) if item.select_one("h2") else ""
        rating = item.select_one(".rating").get_text(strip=True) if item.select_one(".rating") else ""
        quote = item.select_one(".quote").get_text(strip=True) if item.select_one(".quote") else ""
        movies.append({"title": title, "rating": rating, "quote": quote})
    return movies


if __name__ == "__main__":
    movies = parse_movies(html)
    for m in movies:
        print(f"{m["title"]} - 评分: {m["rating"]} - {m["quote"]}")
