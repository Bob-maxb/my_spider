import requests
from bs4 import BeautifulSoup
import time
import json

def fetch_page(url):
    """获取单个页面，包含异常处理"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print(f"⏰ 请求超时: {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"🔌 网络连接错误: {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return None

def parse_page(html):
    """解析页面，提取名言和标签"""
    soup = BeautifulSoup(html, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    page_quotes = []
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
        page_quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })
    return page_quotes

def save_to_txt(quotes, filename="quotes.txt"):
    """保存为 TXT 格式"""
    with open(filename, "w", encoding="utf-8") as f:
        for q in quotes:
            f.write(f"“{q['text']}” — {q['author']}\n")
            f.write(f"  标签: {', '.join(q['tags'])}\n\n")
    print(f"✅ 已保存到 {filename}")

def save_to_json(quotes, filename="quotes.json"):
    """保存为 JSON 格式"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存到 {filename}")

def main():
    base_url = "http://quotes.toscrape.com"
    page_url = "/"
    all_quotes = []
    page_num = 1

    print("🚀 开始爬取名言...\n")

    while True:
        full_url = base_url + page_url
        print(f"📄 正在爬取第 {page_num} 页: {full_url}")

        response = fetch_page(full_url)
        if response is None:
            print("⚠️ 跳过此页，尝试继续...")
            # 尝试寻找下一页链接（简单处理）
            try:
                soup = BeautifulSoup(requests.get(full_url).text, "html.parser")
                next_btn = soup.find("li", class_="next")
                if next_btn:
                    page_url = next_btn.find("a")["href"]
                    page_num += 1
                    time.sleep(2)
                    continue
                else:
                    break
            except:
                break

        page_quotes = parse_page(response.text)
        all_quotes.extend(page_quotes)
        print(f"   ✅ 本页获取 {len(page_quotes)} 条名言")

        # 查找下一页
        soup = BeautifulSoup(response.text, "html.parser")
        next_btn = soup.find("li", class_="next")
        if next_btn:
            page_url = next_btn.find("a")["href"]
            page_num += 1
            time.sleep(1)  # 延迟，避免服务器压力
        else:
            print("\n🏁 已到达最后一页！")
            break

    print(f"\n📊 总计爬取: {len(all_quotes)} 条名言")

    if all_quotes:
        save_to_txt(all_quotes)
        save_to_json(all_quotes)
    else:
        print("⚠️ 没有爬取到任何数据")

if __name__ == "__main__":
    main()