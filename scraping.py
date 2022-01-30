import time

import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = "https://doda.jp/DodaFront/View/JobSearchList.action?ss=1&pic=1&ds=0&oc=0112M%2C0113M%2C010401S%2C010402S%2C010404S&so=50&tp=1&page={}&usrclk_searchList=PC-logoutJobSearchList_searchResultFooterArea_pagination_pos-2"

company_list = []

for i in range(1, 4):
    url = base_url.format(i)

    time.sleep(2)

    r = requests.get(url, timeout=3)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "lxml")
    companies = soup.find_all("div", class_="layout layoutList02")
    for i, company in enumerate(companies):
        print("="*20, i, "="*20)
        company_name = company.find("span").text
        
        detail_url = company.find("a",class_="btnJob03 _JobListToDetail").get("href")
        detail_url = detail_url.replace("-tab__pr", "-tab__jd")
        
        time.sleep(2)
        r2 = requests.get(detail_url, timeout=2)
        r2.raise_for_status()

        soup2 = BeautifulSoup(r2.content, "lxml")
        companies_url = soup2.find("table", id="company_profile_table")
        company_url = companies_url.find("a")
        if company_url:
            company_url = company_url.get("href")

        company_list.append({
            "company_name": company_name,
            "company_url": company_url
            })

df = pd.DataFrame(company_list)
df.to_csv("company_list.csv", index=None, encoding="utf-8-sig")

'''
https://doda.jp/DodaFront/View/JobSearchList.action?ss=1&pic=1&ds=0&oc=0112M%2C0113M%2C010401S%2C010402S%2C010404S&so=50&tp=1&page={}&usrclk_searchList=PC-logoutJobSearchList_searchResultFooterArea_pagination_pos-2
https://doda.jp/DodaFront/View/JobSearchList.action?pic=1&ds=0&oc=0112M%2C0113M%2C010401S%2C010402S%2C010404S&so=50&pf=0&tp=1&page=2&usrclk_searchList=PC-logoutJobSearchList_searchResultFooterArea_pagination_pos-2
https://doda.jp/DodaFront/View/JobSearchList.action?pic=1&ds=0&oc=0112M%2C0113M%2C010401S%2C010402S%2C010404S&so=50&pf=0&tp=1&page=3&usrclk_searchList=PC-logoutJobSearchList_searchResultFooterArea_pagination_pos-2

'''