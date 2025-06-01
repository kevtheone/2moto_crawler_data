import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re

BASE_URL = "https://shop.2motor.tw"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 這裡只列出指定三個分店的白牌檔車頁面
STORE_URLS = {
    "新北中和店": f"{BASE_URL}/collections/2motor123/白牌檔車",
    "新北新莊店": f"{BASE_URL}/collections/2motor700/白牌擋車",
    "桃園中壢店": f"{BASE_URL}/collections/2motor178/檔車"
}

def get_product_links(store_url):
    response = requests.get(store_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_cards = soup.select('div.card-wrapper a[href]')
    links = [BASE_URL + card['href'] for card in product_cards]
    return links

def get_product_details(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 名稱
    title_tag = soup.find('h1', class_='product__title')
    title = title_tag.get_text(strip=True) if title_tag else 'N/A'
    
    # 分店名稱
    store_name_match = re.search(r'【(.*?)】', title)
    store_name = store_name_match.group(1) if store_name_match else 'N/A'

    # 售價
    price_tag = soup.find('span', class_='money')
    price = price_tag.get_text(strip=True) if price_tag else 'N/A'

    # 圖片
    image_url = 'N/A'
    ul_tag = soup.find('ul', id='main-image-wrapper')
    if ul_tag:
        first_li = ul_tag.find('li')
        if first_li:
            img_tag = first_li.find('img')
            if img_tag and 'src' in img_tag.attrs:
                image_url = img_tag['src']

    # 里程
    mileage = 'N/A'  # 預設值
    mileage_tag = soup.find('div', class_='fr-view')
    if mileage_tag:
        p_tags = mileage_tag.find_all('p')
        for p in p_tags:
            text = p.get_text(strip=True)
            if "里程數" in text:
                match = re.search(r'里程數[:：]?(.*)', text)
                if match:
                    mileage = match.group(1).strip()
                break  # 找到就跳出

    return {
        '名稱': title,
        '售價': price,
        '圖片': image_url,
        '里程': mileage,
        '分店名稱': store_name,
        '詳細頁面': url
    }

def main():
    all_products = []
    for store_name, store_url in STORE_URLS.items():
        print(f"正在處理：{store_name}")
        product_links = get_product_links(store_url)
        for link in product_links:
            details = get_product_details(link)
            all_products.append(details)
            time.sleep(1)  # 每次請求間隔 1 秒

    # 輸出 JSON
    with open('../data/moto.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

    print("✅ 資料已儲存至 moto.json")

if __name__ == "__main__":
    main()