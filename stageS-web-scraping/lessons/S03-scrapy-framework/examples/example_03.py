"""示例代码：反爬应对策略"""
import random
import httpx


class AntiCrawler:
    """反爬应对策略集合。"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ]
    
    def __init__(self) -> None:
        self.session = httpx.Client(timeout=30.0)
    
    def random_ua(self) -> str:
        """随机选择 User-Agent。"""
        return random.choice(self.USER_AGENTS)
    
    def fetch(self, url: str) -> httpx.Response:
        """带随机 UA 的请求。"""
        headers = {"User-Agent": self.random_ua()}
        return self.session.get(url, headers=headers)
    
    def close(self) -> None:
        self.session.close()


if __name__ == "__main__":
    print("反爬策略示例")
