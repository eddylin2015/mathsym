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

def GetTE(i, St, Val, Tx=-1):#記錄:Id號,St題,Val值,Ans答,OK檢查,Tx,題型,Tip提示'''    
    return {"Id": i,"St": St,"Val": Val,"Ans": "","OK": 0,"Tx":Tx,"Tip":""}

def NTE2TBL(t):
    return '號|題|值|答|檢查|題型|提示\n--|--|--|--|--|--|--\n{}'.format(
    '\n'.join('|'.join("$$%s$$" % r[_] if i==1 else str(r[_]) for i, _ in enumerate(r)) for r in t))

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