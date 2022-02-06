#進め方
# 1.トップページのスクロール
# スクロールが終わったHTMLファイルを保存

# 2.各ページにアクセスしてスクレイピング
# 保存したHTMLファイルを読み込み、スクレイピング

from time import sleep
from urllib import request

import requests
from bs4 import BeautifulSoup
import pandas as pd

# HTMLを読み込む
with open('webpage.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
a_tags = soup.select("span.exe > a")
print(len(a_tags))

d_list = []
for i, a_tag in enumerate(a_tags):
    url = 'https://atsumaru.jp/' + a_tag.get("href")
    r = requests.get(url)
    r.raise_for_status()
    sleep(3)

    page_soup = BeautifulSoup(r.content, "lxml")
    company_name = page_soup.select_one("#detailBox > h2").text
    address = page_soup.select_one("td:-soup-contains('地図はこちら') > p").text
    tel = page_soup.select_one("div.telNo > p > strong > a").text

    d_list.append({
        "company_name": company_name,
        "address": address,
        "tel": tel
        })
    print("="*10, i, "="*10) 
    print(d_list[-1])

    if i > 30:
        break
df = pd.DataFrame(d_list)
df.to_csv("company_list2.csv", index=None, encoding="utf-8-sig")

