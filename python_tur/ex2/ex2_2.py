#2.2 BeautifulSoup & requests
#2.2.1 soup.select("#all_article_list a")
##all_article_list  <div id=”all_article_list>
#A              <a href="content_1483173.htm">我疫苗無現嚴重不良反應</a>
#<div class="list" id="all_article_list">
#<ul>
#<li><span class="default"> <a href="content_1483173.htm">我疫苗無現嚴重不良反應</a> </span></li> 
#<li> <span class="default"> <a href="content_1483175.htm">衛健委：打完疫苗仍要戴口罩</a> </span></li> 
#</ul>
#</div>

def out_txt(msg):
    print(msg)
    with open(f"./out/news_title.txt", 'a',encoding='utf-8') as the_file:
        the_file.write(str(msg))
        the_file.write('\n')

from bs4 import BeautifulSoup
import requests

_url=f"http://www.macaodaily.com/html/2020-12/20/node_1.htm"
title_res = requests.get(_url)
title_res.encoding = "utf-8"
soup = BeautifulSoup(title_res.text, "html.parser")
#links = soup.find_all(["h1","h2","h3","h4","h5"])
links = soup.select("#all_article_list a")
for link in links:
    news_title = link.getText()
    out_txt(news_title)
print("finished .")