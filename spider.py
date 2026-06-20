import requests
from bs4 import BeautifulSoup

# 1. 目标网址（这是一个公开的练习网站）
url = "http://quotes.toscrape.com/"

# 2. 发送 GET 请求获取网页
response = requests.get(url)

# 3. 检查请求是否成功
if response.status_code == 200:
    # 4. 解析网页内容
    soup = BeautifulSoup(response.text, "html.parser")

    # 5. 找到所有名言所在的 div 元素
    quotes = soup.find_all("div", class_="quote")

    # 6. 遍历并提取信息
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        print(f"“{text}” — {author}")
else:
    print("请求失败，状态码：", response.status_code)