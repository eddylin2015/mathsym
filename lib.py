"""
####################初始化,文件頭,匯入組件#####################################
import random                                     #亂數 
import math                                       #math 內置數學函數
import re
import numpy as np                                #數字矩陣
import sympy as sp                                #sympy 簡易別名 sp    
from sympy.parsing.sympy_parser import parse_expr #文字字串, 解釋成, Sympy 運算式
from sympy.plotting import plot                   #繪圖表
from IPython.display import Latex,HTML                 #網頁顯示數學符號
import json                                       #JSON 結構化資料
sp.init_printing("mathjax")                       #sp.init_printing()  168 
"""    
import datetime
import math
import re

### math
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)    

### input ans 
def Text2St(ans):
    if ans.strip() == "": ans = "-3.1415926"
    ans = re.sub(r"X", r"x", ans)
    ans = re.sub(r"(\d)x", r"\1*x", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)x", r"\1*x", ans))
    ans=re.sub(r"x[(]", r"x*(", ans)
    ans = re.sub(r"x[ ]*", r"x", ans)
    ans = ans.replace(r"x^", r"x**")

    ans = re.sub(r"Y", r"y", ans)
    ans = re.sub(r"(\d)y", r"\1*y", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)y", r"\1*y", ans))
    ans=re.sub(r"y[(]", r"y*(", ans)
    ans = re.sub(r"y[ ]*", r"y", ans)
    ans = ans.replace(r"y^", r"y**")
    
    ans=re.sub(r"(\d)[(]", r"\1*(", ans)
    ans=re.sub(r"(\d)J[(]", r"\1*J(", ans)
    ans = ans.replace(r"J(", r"sqrt(")
    return ans


### HTML LIST TABLE
def LIST2TBL(data):
    return   '<table><tr>{}</tr></table>'.format(
           '</tr><tr>'.join(
               '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
           )

def NTE2TBL(data):
    return '<table><tr>{}</tr></table>'.format(
           '</tr><tr>'.join(
               '<td>{}</td>'.format(
                   '</td><td>'.join("%s" % r[_] if i>0 else "$%s$" % r[_] for i, _ in enumerate(r))) for r in data)
           )

def NTE2HTMLTABLE(NTE):
    HtmlTableContext="<table><tr><td>{}</td></tr>".format("</td><td>".join(_ for _ in ["St","Val","Ans","OK"]))
    for row in NTE:
        St=row["St"]
        if isinstance(St,list):
            HtmlTableContext+=r'<tr><td>{}</td>'.format('</td><td>'.join("$$"+str(_)+"$$" for _ in St))
        else:
            HtmlTableContext+=r'<tr><td>{}</td>'.format("$$"+str(St)+"$$")
        Val=row["Val"]
        Ans=row["Ans"]
        OK=row["OK"]
        HtmlTableContext+=f"<td>{Val}</td><td>{Ans}</td><td>{OK}</td></tr>"
    HtmlTableContext+="</table>"
    return HtmlTableContext  

def NTE2HTML(NTE, Titles = None, LatexFlag = None):
    if Titles == None:
        Titles =  ["St","Val","Ans","OK"]
    if LatexFlag == None:
        LatexFlag=[1,0,0,0]
        
    HtmlTableContext="<table><tr><td>{}</td></tr>".format("</td><td>".join(_ for _ in Titles))
    for row in NTE:
        HtmlTableContext+=f"<tr>"
        idx=0
        for f_ in Titles:
            txt=row[f_]
            if LatexFlag==None:
                HtmlTableContext+=f"<td>{txt}</td>"
            elif LatexFlag[idx]==1:
                HtmlTableContext+=f"<td>$${txt}$$</td>"
            else:
                HtmlTableContext+=f"<td>{txt}</td>"
            idx+=1
        HtmlTableContext+=f"</tr>"    
    HtmlTableContext+="</table>"
    return HtmlTableContext  

def NTE2MD(NTE, Titles = None,LatexFlag = None):
    TableContext =""
    titles=[["Qiz","Val","Ans","OK"],["---","---","---","---"]]
    for t_ in titles:
        TableContext +="|{}|\n".format("|".join(_ for _ in t_))
    for TE in NTE:
        for idx,iteN in enumerate(TE):
            ite=TE[iteN]
            if isinstance(ite,list):
                TableContext+=r'|{}|'.format(' '.join("$$"+str(_)+"$$" for _ in ite))
            elif idx<1:
                TableContext+=r'|{}|'.format("$$"+str(ite)+"$$")
            else:
                TableContext+=r'{}|'.format(str(ite))
        TableContext+="\n"
    return TableContext



### datetime
class DateHelper:
    '''Some helper functions to quickly calculate date.'''
    today_date = datetime.date.today()
    def days_later(self, days):
        '''Return days later in YYYY-MM-DD format.'''
        date = self.today_date + datetime.timedelta(days=days)
        return date.isoformat()
    def days_ago(self, days):
        '''Return days ago in YYYY-MM-DD format.'''
        date = self.today_date - datetime.timedelta(days=days)
        return date.isoformat()
    def today(self):
        '''Return today in YYYY-MM-DD format.'''
        return self.today_date.isoformat()        
    def tomorrow(self):
        '''Return tomorrow in YYYY-MM-DD format.'''
        return self.days_later(1)
    def yesterday(self):
        '''Return yesterday in YYYY-MM-DD format.'''
        return self.days_ago(1)

### txt log file
def txt_log(msg):
    with open(f"news_log_{DateHelper().today()}.txt", 'a',encoding='utf-8') as the_file:
        the_file.write(datetime.date.today().isoformat())
        the_file.write(":")
        the_file.write(str(msg))
        the_file.write('\n')

### submit by mail
def mail_noti(msg,title="news"):
    return requests.post(
        f"https://mail.mbc.edu.mo/mailnoti",
        auth=("api", "API_KEY"),
        data={"from": "FROM",
        "to": "TO",
        "subject": title,
        "text": msg})