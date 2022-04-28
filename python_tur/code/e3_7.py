from bs4 import BeautifulSoup
import requests
_url=f"http://www.macaodaily.com/html/2020-12/20/node_1.htm"
_res = requests.get(_url)
_res.encoding = "utf-8"      #_res.text 完整HTML內容, 包含標籤指今文字, 不是直觀宜懂
soup = BeautifulSoup(_res.text, "html.parser")
links = soup.select("#all_article_list a")   #需學習CSS設定篩選選擇條件,篩選出新聞標題
for link in links:
    print(link.getText() )
