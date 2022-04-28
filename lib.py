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
import sympy as sp                                #sympy 簡易別名 sp    
from sympy.parsing.sympy_parser import parse_expr #文字字串, 解釋成, Sympy 運算式
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy.solvers.inequalities import reduce_rational_inequalities

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
    return {"Id": i,"St": St,"Val": Val,"Ans": "","OK": 0,"Tx":Tx,"Tip":"","PlainText":0}

def NTE2TBL(t, fmt="md"):
    if fmt=="md":
        return '號|題|值|答|檢查|題型|提示\n--|--|--|--|--|--|--\n{}'.format(
            '\n'.join('|'.join("$$%s$$" % r[_] if i==1 else str(r[_]) for i, _ in enumerate(r)) for r in t))
    elif fmt=="html":
        return '<table><tr>{}</tr><tr>{}</tr></table>'.format(
           '<th>{}</th>'.format('</th><th>'.join( r for r in  r"編號,題目,答案,作答,檢查,提示".split(","))),
           '</tr><tr>'.join(
               '<td>{}</td>'.format(
                   '</td><td>'.join("$$%s$$" % r[_] if i==1 else "%s" % r[_] for i, _ in enumerate(r))) for r in t)
           )
    elif fmt=="list":
        return '<table><tr>{}</tr><tr>{}</tr></table>'.format(
           '<th>{}</th>'.format('</th><th>'.join( r for r in  r"編號,題目,答案,作答,檢查,提示".split(","))),
           '</tr><tr>'.join(
               '<td>{}</td>'.format(
                   '</td><td>'.join("<br>".join("$$%s$$" % rr_ for rr_ in r[_]) if i==1 else "%s" % r[_] 
                                    for i, _ in enumerate(r))) for r in t)
           )
    
        
                
def Put_Expr_V1(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Put_Expr_V2(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    ans1 = ans[0]
    ans2 = ans[1] if len(ans) > 1 else "3.1415"
    if ans1.strip() == "":
        ans1 = "3.1415"
    if ans2.strip() == "":
        ans2 = "3.1415"
    try:
        ans = [ parse_expr(ans1),  parse_expr(ans2)]
        if ans == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass    

def Put_Expr_V6(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    ans1=[]
    try:    
        for temp in ans:
            if temp.strip() == "":
                ans1.append(parse_expr(  "3.1415"))
            else:
                ans1.append(parse_expr(Text2St(temp)))
    
        if ans1 == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass    

def Put_Expr_S6(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    TE["OK"] = 0
    try:    
        for i_, temp in enumerate(ans):
            if lib.S6Compare(Val[i_], temp):
                TE["OK"] = 1
            else:
                TE["OK"] = 0
                return
    except:
        pass   

def Put_Expr_InequV1(TE):
    x = sp.symbols('x')
    Val = TE["Val"]
    Flag = False
    ans = TE["Ans"]
    ans = lib.Text2Inequ(TE["Ans"])
    #ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
    #ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)        
    #if ans == "" or  ans == "R" or ans == "r": ans = "(-oo < x) & (x < oo)"
    a1 = ans.split("|")
    a2 = ans.split("&")
    try:
        if len(a1) > 1:
            a_ = []
            for aa_ in a1:
                a_.append(sp.solve(aa_))
            Flag = (a_[0] | a_[1]) == Val
        elif len(a2) > 1:
            a_ = []
            for aa_ in a2:
                a_.append(sp.parse_expr(aa_))
            Flag = reduce_rational_inequalities([[a_[0], a_[1]]], x) == Val
        elif ans == '空集' or ans == '0'  or ans=='False' or ans=="false":
            if str(Val) == "False":
                Flag = True
        else:
            Flag = sp.solve(ans) == Val
        if Flag:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Put_Expr_X1(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    ans=Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


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