#進め方
# 1.トップページのスクロール
# スクロールが終わったHTMLファイルを保存

# 2.各ページにアクセスしてスクレイピング
# 保存したHTMLファイルを読み込み、スクレイピング


from time import time, sleep
from selenium import webdriver

options = webdriver.ChromeOptions()
# ヘッドレスモードでの使用
options.add_argument("--headless")
# シークレットモードでの使用
options.add_argument("--incognito")

# driverを作成する
driver = webdriver.Chrome(
    executable_path="/Users/ogawa/Desktop/hayatasu_websc/scraping_corporate_jobs/tools/chromedriver",
    options=options
    )
driver.implicitly_wait(5)

# driver.get()でサイトにアクセスする
driver.get("https://atsumaru.jp/area/7/list?sagid=all")
sleep(3)

#スクロール前のページの高さを取得
last_height = driver.execute_script("return document.body.scrollHeight")
new_last_height = 0

while True:
    print(last_height)
    driver.execute_script(f"window.scrollTo(0, {last_height})")
    sleep(2)
    new_last_height = driver.execute_script("return document.body.scrollHeight")
    #スクロール前後でページの高さに変化がなくなったら無限スクロール終了とみなしてループを抜ける
    if last_height == new_last_height:
        break
    last_height = new_last_height


content = driver.page_source
with open('webpage.html', 'w') as f:
    f.write(content)


# ブラウザを終了する。
driver.quit()
