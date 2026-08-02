"""示例代码：Selenium 反检测爬虫"""
from selenium import webdriver
from selenium_stealth import stealth


def create_stealth_driver():
    """创建反检测 WebDriver。"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    stealth(driver,
        languages=["zh-CN", "zh", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


if __name__ == "__main__":
    print("反检测爬虫示例")
