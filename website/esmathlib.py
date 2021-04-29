
import random  # 亂數
import math  # math 內置數學函數
import numpy as np  # 數字矩陣
import sympy as sp  # sympy 簡易別名 sp
from sympy.parsing.sympy_parser import parse_expr  # 文字字串, 解釋成, Sympy 運算式
from sympy.plotting import plot  # 繪圖表
import json  # JSON 結構化資料
import datetime
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy.solvers.inequalities import reduce_rational_inequalities
from sympy import lambdify
from matplotlib.figure import Figure
import re
import esutils as lib
import os

"""
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
NTE 多條題目.
NTE=[]; NTE.append(GetTE(Qid,St,Val))
for TE in NTE:  pass
"""

def GetKey(QIID="None"):
    return r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())

def GetTE(Qid, St, Val, Tx=0):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = {}
    #TE["Key"] =r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())
    TE["Id"] = Qid
    TE["Tx"] = Tx
    TE["St"] = St
    TE["Val"] = Val
    TE["Ans"] = ""
    TE["OK"] = 0
    TE["Mark"] = 0
    TE["Minute"]= datetime.datetime.now().strftime("%M:%S")   #"%m-%d-%Y %H:%M:%S")
    TE["Tip"] = ""
    TE["PotImg"]=None
    return TE

def GetQList():
    return  [
        "PF101.4.有理數運算",          
        "PF102.6.整數指數冪運算",
        "PF103.4.一元一次方程",
        "PF104.4.整式的加減法練習",    
        "PF105.4.二元一次方程","PF106.4.一元一次不等式",
        "PF107.4.一元一次不等式組",    
        "PF108.4.整式的乘法練習","PF201.4.根式的運算",
        "PF202.4.整式的乘法公式",
        "PF203.4.因式分解提公因式",
        "PF204.4.分式的乘除",
        "PF205.4.分式的加減",         
        "PF206.4.分式方程",
        "PF207.4.一次函數圖像的性質",
        "PF291.4.一元二次方程式十字相乘法求因式",
        "PF292.4.一元二次方程式求解",
        "PF293.4.整式的乘法練習",  
        "PF301.4.一元二次方程式",
        "PF302.4.解可化為一元二次方程的分式方程",
        "PF303.4.解二元二次方程組",
        "PF304.4.二次函數圖像的性質",
        "PF305.4.解直角三角形",
        "PF306.2.解直角三角形",]

"""
算式
"""
def Get_Expr(QIID,QAMT,Tx=-1):
    NTE=None
    if QIID=="P301":     NTE=Get_P301_Expr(QAMT,Tx)
    elif QIID=="P302":   NTE=Get_P302_Expr(QAMT,Tx)    
    elif QIID=="PF101":  NTE=Get_PF101_Expr(QAMT,Tx)
    elif QIID=="PF102" : NTE=Get_PF102_Expr(QAMT,Tx)
    elif QIID=="PF103" : NTE=Get_PF103_Expr(QAMT,Tx)
    elif QIID=="PF104" : NTE=Get_PF104_Expr(QAMT,Tx)
    elif QIID=="PF105" : NTE=Get_PF105_Expr(QAMT,Tx)
    elif QIID=="PF106" : NTE=Get_PF106_Expr(QAMT,Tx)
    elif QIID=="PF107" : NTE=Get_PF107_Expr(QAMT,Tx)
    elif QIID=="PF108" : NTE=Get_PF108_Expr(QAMT,Tx)
    elif QIID=="PF201" : NTE=Get_PF201_Expr(QAMT,Tx)
    elif QIID=="PF202" : NTE=Get_PF202_Expr(QAMT,Tx)
    elif QIID=="PF203" : NTE=Get_PF203_Expr(QAMT,Tx)
    elif QIID=="PF204" : NTE=Get_PF204_Expr(QAMT,Tx)
    elif QIID=="PF205" : NTE=Get_PF205_Expr(QAMT,Tx)
    elif QIID=="PF206" : NTE=Get_PF206_Expr(QAMT,Tx)
    elif QIID=="PF207" : NTE=Get_PF207_Expr(QAMT,Tx)
    elif QIID=="PF291" : NTE=Get_PF291_Expr(QAMT,Tx)
    elif QIID=="PF292" : NTE=Get_PF292_Expr(QAMT,Tx)
    elif QIID=="PF293" : NTE=Get_PF293_Expr(QAMT,Tx)
    elif QIID=="PF301" : NTE=Get_PF301_Expr(QAMT,Tx)
    elif QIID=="PF302" : NTE=Get_PF302_Expr(QAMT,Tx)
    elif QIID=="PF303" : NTE=Get_PF303_Expr(QAMT,Tx)
    elif QIID=="PF304" : NTE=Get_PF304_Expr(QAMT,Tx)
    elif QIID=="PF305" : NTE=Get_PF305_Expr(QAMT,Tx)
    elif QIID=="PF306" : NTE=Get_PF306_Expr(QAMT,Tx)
    else:
        return None
    return NTE

def Post_Expr_UpdateAns(ReqForm,NTE):
    for key in ReqForm.keys():
        if key=="SID": continue
        for value in ReqForm.getlist(key):
            for TE in NTE:
                if int(key)>=1000:
                    if int(TE["Id"])==int(key)-1000:
                        TE["Minute"]=value
                elif int(TE["Id"])==int(key):
                    if TE["Ans"] != "" :  
                        TE["Ans"]=TE["Ans"]+";"+ value 
                    else:
                        TE["Ans"]=value

def Post_Expr_CheckAns(QIID,NTE,TEid=-1,MxMunites=6):
    for TE in NTE:
        if TEid > 0 and TE["Id"] != TEid:
            continue
        if QIID=="PF101" :   Put_PF101_Expr(TE)
        elif QIID=="PF102" : Put_PF102_Expr(TE)
        elif QIID=="PF103" : Put_PF103_Expr(TE)
        elif QIID=="PF104" : Put_PF104_Expr(TE)
        elif QIID=="PF105" : Put_PF105_Expr(TE)
        elif QIID=="PF106" : Put_PF106_Expr(TE)
        elif QIID=="PF107" : Put_PF107_Expr(TE)
        elif QIID=="PF108" : Put_PF108_Expr(TE)
        elif QIID=="PF201" : Put_PF201_Expr(TE)
        elif QIID=="PF202" : Put_PF202_Expr(TE)
        elif QIID=="PF203" : Put_PF203_Expr(TE)
        elif QIID=="PF204" : Put_PF204_Expr(TE)
        elif QIID=="PF205" : Put_PF205_Expr(TE)
        elif QIID=="PF206" : Put_PF206_Expr(TE)
        elif QIID=="PF207" : Put_PF207_Expr(TE)
        elif QIID=="PF291" : Put_PF291_Expr(TE)
        elif QIID=="PF292" : Put_PF292_Expr(TE)
        elif QIID=="PF293" : Put_PF293_Expr(TE)
        elif QIID=="PF301" : Put_PF301_Expr(TE)
        elif QIID=="PF302" : Put_PF302_Expr(TE)
        elif QIID=="PF303" : Put_PF303_Expr(TE)
        elif QIID=="PF304" : Put_PF304_Expr(TE)
        elif QIID=="PF305" : Put_Expr_V1(TE)  
        elif QIID=="PF306" : Put_Expr_V1(TE)
        else:  Put_Expr_V1(TE)
        Get_Expr_CheckAnsMark(QIID,TE)

def Get_Expr_CheckAnsMark(QIID,TE,MxMunites=3):
    if TE["OK"]==1:
        try:
            stepM = MxMunites / 3 * 60
            m,s=TE["Minute"].split(":")
            m=int(m)
            s=int(s)
            m=m*60+s
            print(m)
            print(stepM)
            if m<stepM : TE["Mark"]=12
            elif m< stepM*2 : TE["Mark"]=10
            elif m< stepM*8 : TE["Mark"]=8
            else: TE["Mark"]=6
        except:
            TE["Mark"]=8

                
def Put_Expr_V1(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False


"""
P301
""" 
def Get_P301_Expr(QN,Tx=-1):
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            e1=sp.Rational(b, a)
            e2=sp.Rational(c, a)
            if e1+e2 <0:
                e1=e1*-1
                e2=e2*-1
            qiz = sp.Add(e1,e2, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
        elif Tx == 2:
            print(Tx)
            a = random.choice(range(10,50))  # 亂數a,b,c, 不為零
            b = random.choice(range(10,100))
            qiz = sp.Mul(a,b, evaluate=False)
            St = r" %s \times %s "%(a,b)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
        elif Tx == 3:
            a = random.choice(range(2,10))  # 亂數a,b,c, 不為零
            b = random.choice(range(10,100))
            c = a *b
            St = r" %s \div %s "%(c,a)  # 題目
            Val = sp.S(c)/a

        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            if a+b+c <0 :
                a=a*-1
                b=b*-1
                c=c*-1
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案


        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "用分數表逹值: -(a/b)"
        NTE.append(TE)
    return NTE
"""
P302
""" 
def Get_P302_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag:Tx = 0 if Qid < (QN//2) else 1  # Tx -半題型1 ,-半題型 2
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案

        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案


        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "用分數表逹值: -(a/b)"
        NTE.append(TE)
    return NTE

"""
PF101有理數運算
"""

def Put_PF101_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Get_PF101_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag:Tx = 0 if Qid < (QN//2) else 1  # Tx -半題型1 ,-半題型 2
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案

        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案


        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "用分數表逹值: -(a/b)"
        NTE.append(TE)
    return NTE


"""
PF102整數指數冪運算
"""

def Put_PF102_Expr(TE):
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "-3.1415926"
    try:
        if parse_expr(ans) == Val:
            TE["OK"] = 1
            return True
    except:
        pass
    return False


def Get_PF102_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    a,b,c,x,y,z=sp.symbols("a,b,c,x,y,z")
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag: Tx=int(Qid % 6)
        if Tx==1:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,2,3,4,5]))
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Mul(a1**b1 , a1**c1, evaluate=False)
            Val=sp.simplify(St)
            St=r" {%s}^{%s} \cdot  {%s}^{%s} " % (a1,b1,a1,c1) #Latex    
        elif Tx==2:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            if op=="Div":
                St=a**b1 / a**c1
                Val=sp.simplify(St)
                St=r" a^{%s} \div  a^{%s} " % (b1,c1) #Latex   \times
            else:
                St=sp.Mul(a**b1 , a**c1, evaluate=False)
                Val=sp.simplify(St)
                St=r" a^{%s} \cdot  a^{%s} " % (b1,c1) #Latex 

        elif Tx==3:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Pow(sp.Mul(b1*a,evaluate=False) , c1, evaluate=False)
            Val=sp.simplify(St)
            St=r" ({%s}*a)^{%s} " % (b1,c1) #Latex 
            #St=sp.latex(St)

        elif Tx==4:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            Val=sp.simplify(St1)
            St=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 

        elif Tx==5:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St11=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St2=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St22=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            op=random.choice(["cdot","div"])
            if op=="div":
                St=St1 / St2
                Val=sp.simplify(St)
                #St=r" {%s} \div  {%s} " % (sp.latex(St1),sp.latex(St2)) #Latex   \times
            else:
                St=sp.Mul(St1 , St2, evaluate=False)
                Val=sp.simplify(St)
            St=r" {%s} \%s  {%s} " % (St11,op,St22) #Latex   \times
        else:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]))
            b1=random.choice([-9,-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9])
            c1=random.choice([-3,-2,-1,2,3])
            St=r" {\large (%s)}^{%s} " % (sp.latex(sp.Rational(a1,b1)),c1) #Latex 
            expr=sp.Pow(sp.Rational(a1,b1), c1 ,evaluate=False)
            Val=sp.simplify(expr) #標準答案 
        #運算方法1:
        #運算方法2:
        #Val=(a / sp.S(b))** c
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)    
    return NTE


"""
PF103一元一次方程
"""
def Put_PF103_Expr(TE):
    print(TE)
    Val=TE["Val"]
    ans=TE["Ans"] if TE["Ans"] != "" else "3.14159"
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans) == Val[0]:  # 比對答案:
            TE["OK"] = 1
            return True
    except:
        pass
    return False

def Get_PF103_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=int(Qid % 4)
        if Tx==1:
            # 2:  ax+b=cx+d a,b,c,d均為-99至99的整数,
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq(a*x+b,c*x+d,evaluate=False)
            St=sp.latex(expre)
            Val=sp.solve(expre)
        elif Tx==2:
            #3： m(a+bx) + n(c+dx) = p(e+fx) 所有字母均為-9至9整数
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq(m*(a+b*x)+n*(c+d*x),p*(e+f*x),evaluate=False)
            St=r" %s *(%s+%s*x)+%s*(%s+%s*x)= %s* (%s+%s*x) "%(m,a,b,n,c,d,p,e,f)
            Val=sp.solve(expre)
        elif Tx==3:
            #4： (ax+b)/m + (cx+d)/n = (ex+f)/p 字母a,b,c,d,e,f均為-9至9整数;m,n,f均為1至9的整數
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq((a+b*x)/m+(c+d*x)/n,(e+f*x)/p,evaluate=False)
            St=r" \frac{%s+%s*x}{%s}+\frac{%s+%s*x}{%s}=\frac{%s+%s*x}{%s} "%(a,b,m,c,d,n,e,f,p)
            Val=sp.solve(expre)
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            express_str=f" {a}*x + {b} "                    # f(x)= ax + b
            QizStat=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            fx=sp.Eq( QizStat, c )                           #sympy.Eq 方程式 f(x)=c ,
            St=sp.latex(fx)                                  #題目 latex 數學格式
            Val=sp.solve(fx)                                 #sympy.solve求根,得出標準答案
        TE=GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "請填x的值"
        NTE.append(TE)
    return NTE


"""
PF104整式的加減法練習
"""

def Put_PF104_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415"
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
            TE["OK"] = 1
        else:  
            TE["OK"] = 0
    except:
        pass


def Get_PF104_Expr(QN,Tx=-1):
    TxFlag=Tx==-1    
    x,y,z=sp.symbols('x,y,z')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=int(Qid % 2)
        if Tx==1:
            #( mx2+px)+(nx2+qx) = ax2 + bx  |p|,|q| < 16 整数
            #   p, q = 16以内随机±整数
            #   a=m+n,    b=p∙q 
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expr1=m*x**2+p*x
            expr2=n*x**2+q*x
            op=random.choice(["-","-","+"])
            if op=="-":
                Val=expr1-expr2
            else:
                Val=expr1+expr2
            St=r"(%s) %s (%s)"%(sp.latex(expr1),op,sp.latex(expr2))
            
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            express_str=f"{a}*x + {b}*x + {c}  "       #題型 express_str ax+bx+c
            St=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
            Val=sp.simplify(St)
            St=sp.latex(St)
        TE=GetTE(Qid,St,Val,Tx)        
        NTE.append(TE)    
    return NTE

"""
PF105二元一次方程
"""

def Put_PF105_Expr(TE):
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
        ans = {x: parse_expr(ans1), y: parse_expr(ans2)}
        if ans == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass
    TE["Val"] = r"\( {} \)".format(sp.latex(Val))


def Get_PF105_Expr(QN,Tx=-1):
    TxFlag=Tx==-1    
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    for Qid in range(0, QN):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        eq1 = sp.Eq(a*x+b*y, m)
        eq2 = sp.Eq(c*x+d*y, n)
        St = [eq1, eq2]
        Val = (sp.solve([eq1, eq2], [x, y]))
        TE = GetTE(Qid, sp.latex(St), Val)
        TE["Tip"] = "求x ,y ?"
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF106一元一次不等式
"""


def Put_PF106_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans == "":
        TE["OK"] = 0
        return
    try:
        if sp.solve(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF106_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   


    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
        if Tx==1:
            #ax+b<cx+d a,b,c,d均為-99至99的整数,
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" {a}*x + {b} {op} {c}*x+{d}"       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==2:
            #m(a+bx)+n(c+dx)<p(e+fx)  所有字母均為-9至9整数            
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" {m}*({a}*x + {b})+{n}*({c}*x+{d}) {op} {p}*({f}*x+{e})  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==3:
            #(a+bx)/m+(c+dx)/n<(e+fx)/p  所有字母均為-9至9整数
            
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" ({a}*x+ {b})/{m} +({c}*x+{d})/{n} {op} ({f}*x+{e})/{p}  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            op=random.choice([">=",">","<=","<"])
            St=a*x +b
            if op==">=":
                St= St >= c
            elif op==">":
                St= St > c
            elif op=="<=":
                St= St <= c
            elif op=="<":
                St= St < c
            Val=solve_univariate_inequality(St,x)      #solve_univariate_inequality 解不等式   
        
        TE = GetTE(Qid, sp.latex(St), Val,Tx)
        NTE.append(TE)
    return NTE


"""
PF107一元一次不等式組
"""
def Put_PF107_Expr(TE):
    x = sp.symbols('x')
    Val = TE["Val"]
    Flag = False
    ans = TE["Ans"]
    ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
    ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)        
    if ans == "": ans = "(-oo < x) & (x < oo)"
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
        elif ans == '0'  or ans=='False' or ans=="false":
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

def Get_PF107_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
        if Tx==1:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            
            express_str=f" {a}* x+ {b}  {op1} {c}* x+ {d} "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" {e}* x+ {f}   {op2} {g}* x+ {h} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2

        elif Tx==2:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            i=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            j=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            k=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            l=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            r=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            s=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])            
            express_str=f" {m}* ({a}* x+ {b})+{n}* ({c}* x+ {d})   {op1} {p}*({f}* x+ {e}) "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" ({g}* x+ {h})/{q}+ ({i}* x+ {j})/{r}  {op2} ({k}* x+ {l})/{s} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2
        elif Tx==3:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            if m==n: n=int(math.copysign(abs(n)+5,m))
            if m>n:
                temp=n
                n=m
                m=temp
            expr1=R"\frac{%s * x + (%s)}{%s}"%(a,b,c)
            if op1==">":
                express_str=f"{n} > {expr1}  > {m} "                    # f(x)= ax + b
                fx1=parse_expr(f"{n} > ({a}* x+ {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x+ {b})/{c} > {m}" , evaluate=False) #字串解釋為可運算式子 expression 
            else:
                express_str=f"{m} < {expr1}  < {n} "                    # f(x)= ax + b
                fx1=parse_expr(f"{m} < ({a}* x + {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x + {b})/{c} < {n}" , evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=express_str
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2            
        else:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            fx1= x > p if op1==">" else x < p
            fx2=  x > q if op2==">" else x < q
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "請作答 空集輸入 false;  "
        NTE.append(TE)
    return NTE


"""
PF108整式的乘法練習
"""


def Put_PF108_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF108_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF201根式的運算
"""


def Put_PF201_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

def Get_PF201_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    sample_list0= list(range(-39,29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1= list(range(8,20))    #sample_list1.remove(0)    # 非零數列
    b_li=list(range(1,18))
    b_li.remove(4)
    b_li.remove(9)
    b_li.remove(16)
    
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid%4
        if Tx==1:
            a=random.choice(range(2,18))
            b=random.choice(b_li)
            c=random.choice(range(2,15))
            d=random.choice(range(2,15))
            m=c*c*b
            n=d*d*b
            St=r"\sqrt{%s} + \sqrt{%s} "% (m,n)
            Val=sp.sqrt(m)+sp.sqrt(n)
        elif Tx==2:
            a=random.choice(range(1,11))
            b=random.choice(b_li)
            c=random.choice(range(1,10))
            d=random.choice(range(1,10))
            e=random.choice([-1,-1,1])
            m=c*c*b
            n=d*d*b
            if e==-1:
                St=r"\sqrt{%s} \times {(\sqrt{%s})}^{%s} "% (m,n,e)
            else:
                St=r"\sqrt{%s} \times {\sqrt{%s}} "% (m,n)
            Val=sp.sqrt(m)*sp.sqrt(n)**e
        elif Tx==3:
            a=random.choice(range(1,11))
            c=random.choice(range(1,10))
            b=random.choice(b_li)
            d=random.choice(b_li)
            l=random.choice(range(1,10))
            e=random.choice([-1,1])
            m=a*a*b
            n=c*c*d
            if m==n: e=1
            if e==-1:
                St=r"\frac{\sqrt{%s}}{  \sqrt{%s} - (\sqrt{%s})} "% (l,m,n)
            else:
                St=r"\frac{\sqrt{%s}}{  \sqrt{%s} + (\sqrt{%s})} "% (l,m,n)
            Val=sp.sqrt(l) /( sp.sqrt(m) +e* sp.sqrt(n))
            Val=sp.simplify(Val)

            
        else:
            a=random.choice(range(2,18))
            b=random.choice(b_li)
            m=a*a*b
            St=r"\sqrt{%s}"% m
            Val=sp.sqrt(m)    
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"]='請作答sqrt(2) 可寫 J(2 ):'
        NTE.append(TE)
    return NTE


"""
PF202整式的乘法公式平方差
"""


def Put_PF202_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2St(ans)
    if ans.strip()=="":ans="3.1415"
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF202_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    sample_list1 = list(range(-19, 19))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag : Tx=Qid % 2
        if Tx==0:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
        elif Tx==1:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            op=random.choice(["-","-","+"])
            express_str = f"({p}*x  {op} ({q}) *  y )**2   "  # 題型 express_str ax+bx+c
        else:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF203因式分解提公因式
"""


def Put_PF203_Expr(TE):
    x,y,z=sp.symbols('x,y,z')
    Val = TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    if ans.strip()=="": ans="3.1415"
    subsV={x:7,y:11,z:17}
    try:
        if parse_expr(ans).subs(subsV)==Val.subs(subsV):                   #比對答案:
            TE["OK"]=1
    except:
        pass
    TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF203_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    NTE = []
    for Qid in range(0, QN):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        ab = a*b
        ac = a*c
        p = random.choice([0, 1, 2, 3, 4, 5])
        q = random.choice([0, 1, 2, 3, 4, 5])
        u = random.choice([0, 1, 2, 3, 4, 5])
        v = random.choice([0, 1, 2, 3, 4, 5])
        # 題型 express_str ax+bx+c
        express_str = f"{ab} * x**{p} * y**{q}  + {ac} * x**{u}*y**{v}  "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF204分式的乘除
"""


def Put_PF204_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF204_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x, y, z, m, n = sp.symbols('x,y,z,m,n')
    op_list = ["*", "/"]
    sample_list0 = list(range(1, 17))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        p = random.choice(sample_list0)
        q = random.choice(sample_list0)
        r = random.choice(sample_list0)
        u = random.choice(sample_list0)
        v = random.choice(sample_list0)
        p1 = random.choice(sample_list0)
        q1 = random.choice(sample_list0)
        r1 = random.choice(sample_list0)
        u1 = random.choice(sample_list0)
        v1 = random.choice(sample_list0)
        fx1 = (a*x**p*y**q*z**r)/(b*m**u*n**v)
        fx2 = (d*m**u1*n**v1)/(c*x**p1*y**q1*z**r1)
        TE = GetTE(Qid, None, None, Tx)
        if op == "*":
            St = sp.Mul(fx1, fx2, evaluate=False)
            TE["St"] = sp.latex(St)
        elif op == "/":
            St = fx1/fx2
            fx1latex = sp.latex(fx1)
            fx2latex = sp.latex(fx2)
            TE["St"] = f" {fx1latex} \div {fx2latex}"
        Val = sp.simplify(St)
        TE["Val"] = Val
        NTE.append(TE)
    return NTE


"""
PF205分式的加減
"""


def Put_PF205_Expr(TE):
    x, y, z = sp.symbols('x,y,z')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    TE["Val"] = r"\(%s\)" % sp.latex(Val)


def Get_PF205_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    op_list = ["+", "-"]
    sample_list0 = list(range(1, 16))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 11))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag : Tx= 0
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        h = random.choice(sample_list1)
        k = random.choice(sample_list1)
        h1 = random.choice(sample_list1)
        k1 = random.choice(sample_list1)
        e = lib.lcm(a, b)
        f = lib.lcm(a, b) // a
        g = lib.lcm(a, b) // b
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        if p+q==0: q=int(math.copysign((abs(q)+2),q))
        b = p+q
        c = p*q
        fx1 = c / (a*x**h*y**k)
        fx2 = d / (b*x**h1*y**k1)
        St = sp.S(0)
        if op == "+":
            St = sp.Add(fx1, fx2)
        if op == "-":
            St = fx1-fx2
        Val = sp.simplify(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF206分式方程
"""


def Put_PF206_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val[0].subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF206_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x = sp.Symbol('x')
    sample_list0 = list(range(1, 8))     # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 10))
    sample_list2 = list(range(-10, 10))  # sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list0)
        a1 = random.choice(sample_list0)
        c = random.choice(sample_list1)
        c1 = random.choice(sample_list1)
        ac1 = a*c1
        a1c = a1*c
        aclcm = lib.lcm(ac1, a1c)
        c1 = aclcm//a
        c = aclcm//a1
        b = random.choice(sample_list2)
        b1 = random.choice(sample_list2)
        d = random.choice(sample_list2)
        d1 = random.choice(sample_list2)
        expr1 = (c * x+d)/(a*x+b)
        expr2 = (c1 * x+d1)/(a1*x+b1)
        St = sp.Eq(expr1, expr2)  # f1(x)=f2(x)
        Val = sp.solve(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF207一次函數圖像的性質
"""


def Put_PF207_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans)==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF207_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        k = random.choice(sample_list1)
        b = random.choice(sample_list0)
        St = sp.Eq(y, k*x+b)  
        Val = 1
        if k < 0:
            Val = -1
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = " y 隨 x 的增大而____  (  +1 表示 增大  或  -1 表示  減少 )"
        
        try:
            TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
            expr= k*x+b
            lam_x = lambdify(x, expr, modules=['numpy'])
            x_vals = np.linspace(-5, 5, 10)
            y_vals = lam_x(x_vals)
            fig = Figure()
            fig.set_figheight(3)
            fig.set_figwidth(3)            
            ax = fig.subplots()
            ax.plot(x_vals, y_vals)
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')            
            fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
            # Save it to a temporary buffer.
            #buf = BytesIO()
            #fig.savefig(buf, format="png")
            #data = base64.b64encode(buf.getbuffer()).decode("ascii")
            #return f"<img src='data:image/png;base64,{data}'/>"        
        except:
            TE["PlotImg"]=None
        NTE.append(TE)

    return NTE


"""
PF291一元二次方程式十字相乘法求因式
"""


def Put_PF291_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

def Get_PF291_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "十字相乘法因式分解"
        NTE.append(TE)
    return NTE


"""
PF292一元二次方程式求解
"""


def Put_PF292_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    try:
        cnt=0
        for idx in ans_:
            for v_ in Val:
                if int(idx)==v_ : cnt+=1
        if cnt>1:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
        


def Get_PF292_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "解方程 x1, x2?"
        NTE.append(TE)
    return NTE


"""
PF293整式的乘法練習
"""


def Put_PF293_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    

def Get_PF293_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = {}
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "整式的乘法練習,開展式子"
        NTE.append(TE)
    return NTE


"""
PF301一元二次方程式
"""
def Put_PF301_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    ans=[]
    ans_idx=[]
    try:
        cnt=0
        for value in ans_:
            ans.append(parse_expr(value))
        
        for idx, a_ in enumerate(ans):
            for vidx, v_ in enumerate(Val):
                if a_==v_ : 
                    if vidx in ans_idx:
                        pass
                    else:
                        cnt+=1
                        ans_idx.append(vidx)
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF301_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = 1
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        if Tx == 2:
            p = random.choice(range(-15, 15))
            q = random.choice(range(-15, 15))
            b = p+q
            c = p*q
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass

        St = sp.Add(a*x**2, b*x, c, evaluate=False)
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "因式分解"
        NTE.append(TE)
    return NTE


"""
PF302解可化為一元二次方程的分式方程
"""


def Put_PF302_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    ans=[]
    ans_idx=[]
    try:
        cnt=0
        for value in ans_:
            ans.append(parse_expr(lib.Text2St(value)))
        
        for idx, a_ in enumerate(ans):
            for vidx, v_ in enumerate(Val):
                if a_==v_ : 
                    if vidx in ans_idx:
                        pass
                    else:
                        cnt+=1
                        ans_idx.append(vidx)
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

    


def Get_PF302_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = random.choice(sample_list1)
        b = random.choice(sample_list1)
        b = sp.Integer(math.copysign(b, a))
        fx1 = a / (x**2)
        St = sp.Eq(fx1, b)  # f(x)=0
        if Tx == 2:
            if a*a+4*b >= 0:
                fx1 = a / x
                fx2 = b / (x**2)
                fx = sp.Add(fx1, fx2, evaluate=False)
                St = sp.Eq(fx, sp.Integer(1))  # f(x)=0
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF303解二元二次方程組
"""


def Put_PF303_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    try:
        cnt=0
        for idx in ans_:
            for v_ in Val:
                if int(idx)==v_ : cnt+=1
        if cnt>1:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF303_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y = sp.symbols('x,y')
    NTE = []
    for Qid in range(0, QN):
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        f = p*q
        l = (p+q)
        eq1 = sp.Eq(x+y, b)
        eq2 = sp.Eq(x*y, c)
        St = [eq1, eq2]
        Val = sp.solve([eq1, eq2], x, y)
        #Val=sp.solve([x+y+f,x*y+l],x,y)
        St = [sp.latex(eq1), sp.latex(eq2)]  # 題目
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "分別給出,x 和 y 值"
        NTE.append(TE)
    return NTE


"""
PF304二次函數圖像的性質
"""


def Put_PF304_Expr(NTE):
    Val=TE["Val"]
    ans=TE["Ans"].split(";")
    anss=[]
    try:
        for idx in ans:
            if idx=="" : idx="0"
            anss.append(parse_expr(lib.Text2St(idx)))
        Flag=0
        for v_ in Val:
            for a_ in ans:
                if(v_==a_): Flag+=1
        if Flag>1:                   #比對答案:
            TE["OK"]=1
        else:                                           #不則
            TE["OK"]=0
    except:
        pass

def Get_PF304_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list1)
        h = random.choice(sample_list0)
        k = random.choice(sample_list0)
        St = sp.Eq(y, a*(x-h)**2+k)  # , evaluate=False) #字串解釋為可運算式子 expression
        Val = [h, k]
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "頂點坐標x ,y ?"
        #TE["Plot"]=a*(x-h)**2+k
        NTE.append(TE)
    return NTE


"""
PF305解直角三角形    
"""


def sjstr(a, d, e):
    triang_fnc = ["", "sin", "cos", "tan"]
    str = triang_fnc[a]
    if e == 2:
        str += "^2"
    ang_degree = ["", "0^o", "30^o", "45^o", "60^o", "90^o"]
    return str+ang_degree[d]


def ang_expre(a, d, e):
    ad = [sp.pi, sp.pi*0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2]
    f = sp.S(1)
    if a == 1:
        f = sp.sin(ad[d])
    elif a == 2:
        f = sp.cos(ad[d])
    elif a == 3:
        f = sp.tan(ad[d])
    elif a == 4:
        f = sp.atan(ad[d])
    if e == 2:
        f = f**2
    return f
############################################################################


def Get_PF305_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    NTE = []
    for Qid in range(0, QN):
        op = random.choice([" + ", " - ", " * ", " / "])
        e = random.choice([1, 2])
        a = random.choice([1, 2, 3])
        b = random.choice([1, 2, 3])
        d1 = random.choice([1, 2, 3, 4, 5])
        d2 = random.choice([1, 2, 3, 4, 5])

        if a == 3 and d1 == 5:
            d1 = 4
        if b == 3 and d2 == 5:
            d2 = 4
        St = sjstr(a, d1, e) + op + sjstr(b, d2, 1)
        if op == " / ":
            St = sjstr(a, d1, e) + "\div " + sjstr(b, d2, 1)
        Val = sp.S(0)
        print(ang_expre(a, d1, e))
        print(ang_expre(b, d2, 1))

        if op == " + ":
            Val = ang_expre(a, d1, e) + ang_expre(b, d2, 1)
        elif op == " - ":
            Val = ang_expre(a, d1, e) - ang_expre(b, d2, 1)
        elif op == " * ":
            Val = ang_expre(a, d1, e) * ang_expre(b, d2, 1)
        elif op == " / ":
            Val = ang_expre(a, d1, e) / ang_expre(b, d2, 1)

        TE = GetTE(Qid, St, Val, Tx)
        NTE.append(TE)
    return NTE

#######################

def Plot_RightTriangle(A,O,H,Path_):
    try:
        #plt.close('all')
        # Triangle 1
        x=np.array([0,A,A,0])
        y=np.array([0,0,O,0])
        # Figure and Axes
        fig1=Figure()
        fig1.set_figheight(3)
        fig1.set_figwidth(3)
        #ax1=fig1.add_subplot(111)
        ax1=fig1.subplots()
        ax1.axis('square')
        ax1.plot(x,y)
        # Axes Limits
        ax1.set_xlim([-1,A+2])
        ax1.set_ylim([-1,O+2])
        ax1.text(0.5,0.25,'θ')
        ax1.text(A-0.5,0.25,'90')
        ax1.text(A-0.25,O-0.35,'γ')
        ax1.text(A/2,-0.5,f'a={A}')
        ax1.text(A+0.5,O/2,f'b={O}')
        #ax1.text(A/2-1,O/2,f'c=${sp.latex(H)}$')
        ax1.text(A/2-1,O/2,f'c')
        fig1.savefig(os.getcwd()+"\\static\\"+Path_)
        return Path_
    except Exception as e:
        print(e)
        return None

def Plot_RightTriangle2(A,O,H,r,Path_):
    try:
        #plt.close('all')
        # Triangle 1
        a=A.evalf()
        o=O.evalf()
        h=H.evalf()
        x=np.array([0,a,a,0])
        y=np.array([0,0,o,0])
        # Figure and Axes
        fig1=Figure()
        fig1.set_figheight(3)
        fig1.set_figwidth(3)
        #ax1=fig1.add_subplot(111)
        ax1=fig1.subplots()
        ax1.axis('square')
        ax1.plot(x,y)
        # Axes Limits
        ax1.set_xlim([-1,int(a)+2])
        ax1.set_ylim([-1,int(o)+2])
        ax1.text(0.5,0.25,'θ')
        ax1.text(a-0.5,0.25,'90')
        ax1.text(a-0.35,o-0.4,f'γ(${r}^o$)')
        ax1.text(a/2,-0.5,f'a=${sp.latex(A)}$')
        #ax1.text(A+0.5,O/2,f'b={O}')
        ax1.text(a+0.5,o/2,f'b')
        #ax1.text(A/2-1,O/2,f'c=${sp.latex(H)}$')
        ax1.text(a/2-1,o/2,f'c')
        fig1.savefig(os.getcwd()+"\\static\\"+Path_)
        return Path_
    except Exception as e:
        print(e)
        return None
        
    
def Get_PF306_Expr(QN,Tx=-1):
    NTE = []
    for Qid in range(0, QN):
        if Tx == 1:
            x=random.choice([2,3,4,5])
            theta = random.choice([30,45,60,37,53])
            gamma=90-theta
            if theta==30:
                A=x*sp.sqrt(3)
                O=sp.S(x)
                H=sp.S(2*x)
            elif theta==45:
                A=sp.S(x)
                O=sp.S(x)
                H=x*sp.sqrt(2)
            elif theta==60:
                A=sp.S(x)
                O=x*sp.sqrt(3)
                H=sp.S(2*x)
            elif theta==37:
                A=sp.S(4*x)
                O=sp.S(3*x)
                H=sp.S(5*x)
            elif theta==53:
                A=sp.S(3*x)
                O=sp.S(4*x)
                H=sp.S(5*x)
            bian_=["b","c"]
            bian=random.choice(bian_)
            trig_=["sin","cos","tan"]
            trig=random.choice(trig_)

            #St=["設直角三角形:", r"a=%s,b=%s,c=%s, 求 %s \%s = ?"%(A,O,sp.latex(H) , trig,ang)]
            St=["設直角三角形:", r"a=%s, \gamma=%s^o, 求 %s  = ?"%(sp.latex(A),gamma, bian)]
            Val = 1
            if bian=="b":
                Val=O
            if bian=="c":
                Val=H
            TE = GetTE(Qid, St, Val, Tx)
            TE["PlotImg"]=Plot_RightTriangle2(A,O,H,gamma,"img"+GetKey()+str(Qid)+".png")
            NTE.append(TE)
            
        else:
            A=random.choice([2,3,4,5,7])
            O=random.choice([2,3,4,5,7])
            H=sp.sqrt(A**2+O**2)
            angle_=["theta","gamma"]
            trig_=["sin","cos","tan"]
            trig=random.choice(trig_)
            ang=random.choice(angle_)
            #St=["設直角三角形:", r"a=%s,b=%s,c=%s, 求 %s \%s = ?"%(A,O,sp.latex(H) , trig,ang)]
            St=["設直角三角形:", r"a=%s, b=%s, 求 %s \%s = ?"%(A,O, trig,ang)]
            Val = 1
            if trig=="sin":
                if ang=="theta":             
                    Val=O/H
                if ang=="gamma":             
                    Val=A/H
            if trig=="cos":
                if ang=="theta":             
                    Val=A/H
                if ang=="gamma":             
                    Val=O/H
            if trig=="tan":
                if ang=="theta":             
                    Val=sp.S(O)/A
                if ang=="gamma":             
                    Val=sp.S(A)/O
            
            TE = GetTE(Qid, St, Val, Tx)
            #TE["Tip"] = " y 隨 x 的增大而____  (  +1 表示 增大  或  -1 表示  減少 )"
            TE["PlotImg"]=Plot_RightTriangle(A,O,H,"img"+GetKey()+str(Qid)+".png")
            NTE.append(TE)

    return NTE
