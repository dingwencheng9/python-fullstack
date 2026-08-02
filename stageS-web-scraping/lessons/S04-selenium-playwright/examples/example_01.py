"""示例代码：Selenium 基础爬虫"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass


@dataclass
class Product:
    title: str
    price: str
    link: str


def scrape_products(url: str) -> list[Product]:
    """爬取商品列表。"""
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待商品加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item"))
    )
    
    items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    products = []
    for item in items:
        title = item.find_element(By.CSS_SELECTOR, ".title").text
        price = item.find_element(By.CSS_SELECTOR, ".price").text
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        products.append(Product(title=title, price=price, link=link))
    
    driver.quit()
    return products


if __name__ == "__main__":
    print("Selenium 爬虫示例")
