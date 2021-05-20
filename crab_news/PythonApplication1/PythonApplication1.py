import datetime
from bs4 import BeautifulSoup
import requests
import re
import module1 as uti
"""
   搜查有關教學,升學相關資料,資料來源以本地高教局,教青局,澳門日報
   本例子先完成目標1
   教育,教青,教青局,德育,校,學校,學生,學習,校舍,校園,校際,機械人,科普,幼稚,高校,招生
   目標1
   http://www.macaodaily.com/html/2019-05/01/node_1.htm
   打開第二層內容搜查關鍵字
   目標2
   https://www.dses.gov.mo/news
   目標3
   https://portal.dsej.gov.mo/webdsejspace/internet/Inter_main_page.jsp?id=53180
"""

dateHlp=uti.DateHelper()
print(f"today is　{dateHlp.today() }")
keywords="教育,教青,教青局,教局,學校,學生,校舍,校園,校際,幼稚,高校,招生".split(",")
today = datetime.datetime.today()
year = str(today.year).zfill(2)
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)

todaynews_baseurl=f"http://www.macaodaily.com/html/{year}-{month}/{day}/"
todaynews_url=f"{todaynews_baseurl}node_1.htm"
title_res = requests.get(todaynews_url)
title_res.encoding = "utf-8"
soup = BeautifulSoup(title_res.text, "html.parser")
links = soup.select("#all_article_list a")
mail_noti_ctx=[]
for link in links:
    news_title = link.getText()
    detail_url=f"{todaynews_baseurl}{link.get('href')}"
    found=False;
    for keyword in keywords:
        if keyword in news_title:
             mail_noti_ctx.append(f"{year}-{month}-{day}: {news_title}")
             mail_noti_ctx.append(detail_url)
             uti.txt_log(f"{year}-{month}-{day}: {news_title}")
             uti.txt_log(detail_url)
             detail_res = requests.get(detail_url)
             detail_res.encoding = "utf-8"
             soup1 = BeautifulSoup(detail_res.text, "html.parser")
             ctx = soup1.select("founder-content")
             uti.txt_log(ctx)
             print(ctx)
             found=True
             break
    
    if found==False and "content_" in link.get('href'):
        detail_res = requests.get(detail_url)
        detail_res.encoding = "utf-8"
        soup1 = BeautifulSoup(detail_res.text, "html.parser")
        ctx = soup1.select("founder-content")
        for keyword in keywords:
            if keyword in str(ctx):
                mail_noti_ctx.append(f"{year}-{month}-{day}: {news_title}")
                mail_noti_ctx.append(detail_url)
                uti.txt_log(f"{year}-{month}-{day}: {news_title}")
                uti.txt_log(detail_url)
                print(ctx)
                uti.txt_log(ctx)
                break
#uti.mail_noti("\n".join(mail_noti_ctx))
print("finished .")

