
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
import re
import esutils

"""
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
NTE 多條題目.
NTE=[]; NTE.append(GetTE(i,St,Val))
for TE in NTE:  pass
"""


def GetTE(i, St, Val):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = {}
    TE["Key"] = datetime.datetime.now().isoformat()
    TE["Id"] = i
    TE["St"] = St
    TE["Val"] = Val
    TE["Ans"] = ""
    TE["OK"] = 0
    TE["Tip"] = ""
    return TE


"""
PF101有理數運算
"""


def Put_PF101_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = TE["Ans"]
    if ans.strip() == "":
        ans = "-3.1415926"
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
           TE["OK"] = 1
           return True
    except:
        pass
    return False


def Post_PF101_Expr(NTE):
    for TE in NTE:
        Put_PF101_Expr(TE)


def Get_PF101_Expr(QizAmt):
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for i in range(0, QizAmt):
        Tx = "1" if i < (QizAmt//2) else "2"  # Tx -半題型1 ,-半題型 2
        if Tx == "1":
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案
        elif Tx == "2":
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
        TE = GetTE(i, St, Val)
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


def Post_PF102_Expr(NTE):
    for TE in NTE:
        Put_PF102_Expr(TE)


def Get_PF102_Expr(QizAmt):
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice(
            [-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9])
        c = random.choice([-3, -2, -1, 2, 3])
        St = r" {\large (%s)}^{%s} " % (sp.latex(sp.Rational(a, b)), c)
        #運算方法1:
        expr = sp.Pow(sp.Rational(a, b), sp.Integer(c), evaluate=False)
        Val = sp.simplify(expr)  # 標準答案
        #運算方法2:
        #fenM=sp.Integer(b)
        #fenX=a / fenM
        #Val= fenX ** c     #標準答案
        TE = GetTE(i, St, Val)
        NTE.append(TE)
    return NTE


"""
PF103一元一次方程
"""


def Post_PF103_Expr(NTE):
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"] if TE["Ans"] != "" else "3.14159"
        try:
            if parse_expr(ans) == Val[0]:  # 比對答案:
                TE["OK"] = 1
        except:
            pass


def Get_PF103_Expr(QizAmt):
    x = sp.Symbol('x')
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        #express_str=f" {a}*x + {b} "                    # f(x)= ax + b
        #QizStat=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
        fx = sp.Eq(a*x+b, c)  # sympy.Eq 方程式 f(x)=c ,
        St = sp.latex(fx)  # 題目 latex 數學格式
        Val = sp.solve(fx)  # sympy.solve求根,得出標準答案
        TE = GetTE(i, St, Val)
        TE["Tip"] = "請填x的值"
        NTE.append(TE)
    return NTE


"""
PF104整式的加減法練習
"""


def Post_PF104_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans.strip() == "": ans = "3.1415"
        ans = esutils.Txt2EqSt(ans)
        try:

            if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF104_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x + {b}*x + {c}  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.simplify(St)
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF105二元一次方程
"""


def Post_PF105_Expr(NTE):
    x, y, z = sp.symbols('x,y,z')
    for TE in NTE:
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


def Get_PF105_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    for i in range(0, QizAmt):
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
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "求x ,y ?"
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF106一元一次不等式
"""


def Post_PF106_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans == "":
            continue
        try:
            if sp.solve(ans) == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF106_Expr(QizAmt):
    x = sp.symbols('x')
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q

        op = random.choice([">=", ">", "<=", "<"])
        St = a*x + b
        if op == ">=":
            St = St >= c
        elif op == ">":
            St = St > c
        elif op == "<=":
            St = St <= c
        elif op == "<":
            St = St < c

        # solve_univariate_inequality 解不等式
        Val = solve_univariate_inequality(St, x)

        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF107一元一次不等式組
"""


def Post_PF107_Expr(NTE):
    x = sp.symbols('x')
    for TE in NTE:
        Val = TE["Val"]
        Flag = False
        ans = TE["Ans"]
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
            elif ans == '0':
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


def Get_PF107_Expr(QizAmt):
    x = sp.symbols('x')
    NTE = []
    for i in range(0, QizAmt):
        op1 = random.choice([">", "<"])
        op2 = random.choice([">", "<"])
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        fx1 = x > p if op1 == ">" else x < p
        fx2 = x > q if op2 == ">" else x < q
        St = [sp.latex(fx1), sp.latex(fx2)]  # 題目
        Val = reduce_rational_inequalities([[fx1, fx2]], x)   # and
        TE = GetTE(i, St, Val)
        TE["Tip"] = "請作答 空集輸入 0; 等於某值  Ne(x,0) "
        NTE.append(TE)
    return NTE


"""
PF108整式的乘法練習
"""


def Post_PF108_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans.strip() == "": ans = "3.1415926"
        ans = esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF108_Expr(QizAmt):
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF201根式的運算
"""


def Post_PF201_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        if ans.strip() == "": ans = "3.1415926"
        ans=esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass

def Get_PF201_Expr(QizAmt):
    sample_list1 = list(range(8, 20))  # sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        p = random.choice(sample_list1)
        q = random.choice(sample_list1)
        b = p+q
        c = p*q

        St = f"\\sqrt{c}"
        Val = sp.sqrt(c)

        TE = GetTE(i, St, Val)
        TE["Tip"]='請作答sqrt(2) 可寫 J(2 ):'
        NTE.append(TE)
    return NTE


"""
PF202整式的乘法公式平方差
"""


def Post_PF202_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = esutils.Txt2EqSt(ans)
        if ans.strip()=="":ans="3.1415"
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF202_Expr(QizAmt):
    sample_list1 = list(range(-19, 19))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = random.choice(sample_list1)
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF203因式分解提公因式
"""


def Post_PF203_Expr(NTE):
    x,y,z=sp.symbols('x,y,z')
    for TE in NTE:
        Val = TE["Val"]
        ans=TE["Ans"]
        ans=esutils.Txt2EqSt(ans)
        if ans.strip()=="": ans="3.1415"
        subsV={x:7,y:11,z:17}
        try:
            if parse_expr(ans).subs(subsV)==Val.subs(subsV):                   #比對答案:
                TE["OK"]=1
        except:
            pass
        TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF203_Expr(QizAmt):
    NTE = []
    for i in range(0, QizAmt):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        ab = a*b
        ac = a*c
        ad = a*d
        p = random.choice([0, 1, 2, 3, 4, 5])
        q = random.choice([0, 1, 2, 3, 4, 5])
        u = random.choice([0, 1, 2, 3, 4, 5])
        v = random.choice([0, 1, 2, 3, 4, 5])

        # 題型 express_str ax+bx+c
        express_str = f"{ab} * x**{p} * y**{q}  + {ac} * x**{u}*y**{v}  "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF204分式的乘除
"""


def Post_PF204_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
        TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF204_Expr(QizAmt):
    x, y, z, m, n = sp.symbols('x,y,z,m,n')
    op_list = ["*", "/"]
    sample_list0 = list(range(1, 17))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
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
        TE = GetTE(i, None, None)
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


def Post_PF205_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
        TE["Val"] = r"\(%s\)" % sp.latex(Val)


def Get_PF205_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    op_list = ["+", "-"]
    sample_list0 = list(range(1, 16))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 11))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        h = random.choice(sample_list1)
        k = random.choice(sample_list1)
        h1 = random.choice(sample_list1)
        k1 = random.choice(sample_list1)
        e = esutils.lcm(a, b)
        f = esutils.lcm(a, b) // a
        g = esutils.lcm(a, b) // b
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
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
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF206分式方程
"""


def Post_PF206_Expr(NTE):
    for TE in NTE:
        x=sp.Symbol('x')
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val[0].subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF206_Expr(QizAmt):
    x = sp.Symbol('x')
    sample_list0 = list(range(1, 8))     # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 10))
    sample_list2 = list(range(-10, 10))  # sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = random.choice(sample_list0)
        a1 = random.choice(sample_list0)
        c = random.choice(sample_list1)
        c1 = random.choice(sample_list1)
        ac1 = a*c1
        a1c = a1*c
        aclcm = esutils.lcm(ac1, a1c)
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
        TE = GetTE(i, sp.latex(St), Val)
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF207一次函數圖像的性質
"""


def Post_PF207_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans)==Val:                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF207_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        k = random.choice(sample_list1)
        b = random.choice(sample_list0)
        St = sp.Eq(y, k*x+b)  # , evaluate=False) #字串解釋為可運算式子 expression
        Val = 1
        if k < 0:
            Val = -1
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = " y 隨 x 的增大而____  (  +1 表示 增大  或  -1 表示  減少 )"
        #TE["Plot"]=k*x+b
        NTE.append(TE)

    return NTE


"""
PF291一元二次方程式十字相乘法求因式
"""


def Post_PF291_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
    



def Get_PF291_Expr(QizAmt):
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)  # 因式分解,得出標準答案
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "十字相乘法因式分解"
        NTE.append(TE)
    return NTE


"""
PF292一元二次方程式求解
"""


def Post_PF292_Expr(NTE):
    for TE in NTE:
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
        


def Get_PF292_Expr(QizAmt):
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "解方程 x1, x2?"
        NTE.append(TE)
    return NTE


"""
PF293整式的乘法練習
"""


def Post_PF293_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = esutils.Txt2EqSt(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
    

def Get_PF293_Expr(QizAmt):
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = {}
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "整式的乘法練習,開展式子"
        NTE.append(TE)
    return NTE


"""
PF301一元二次方程式
"""


def Post_PF301_Expr(NTE):
    for TE in NTE:
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


def Get_PF301_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        Tx = i % 4 + 1
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
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "因式分解"
        NTE.append(TE)
    return NTE


"""
PF302解可化為一元二次方程的分式方程
"""


def Post_PF302_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"].split(";")
        for idx in range(0,len(Val)):
            ans1=input(f"請作答x{idx+1}:")  
            ans.append(int(ans1))
        TE["Ans"]=ans
        if ans==Val:                   #比對答案:
            print("答對!")                              #答對加一分
            Mark+=1
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
            display(Latex(f"答案錯誤, 標準答案: $ {Val} $"))
    


def Get_PF302_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        Tx = i % 4 + 1
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
        TE = GetTE(i, sp.latex(St), Val)
        NTE.append(TE)
    return NTE


"""
PF303解二元二次方程組
"""


def Post_PF303_Expr(NTE):
    for TE in NTE:
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


def Get_PF303_Expr(QizAmt):
    x, y = sp.symbols('x,y')
    NTE = []
    for i in range(0, QizAmt):
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
        TE = GetTE(i, St, Val)
        TE["Tip"] = "分別給出,x 和 y 值"
        NTE.append(TE)
    return NTE


"""
PF304二次函數圖像的性質
"""


def Post_PF304_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"].split(";")
        anss=[]
        try:
            for idx in ans:
                if idx=="" : idx="0"
                anss.append(parse_expr(esutils.Txt2EqSt(idx)))
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

def Get_PF304_Expr(QizAmt):
    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for i in range(0, QizAmt):
        a = random.choice(sample_list1)
        h = random.choice(sample_list0)
        k = random.choice(sample_list0)
        St = sp.Eq(y, a*(x-h)**2+k)  # , evaluate=False) #字串解釋為可運算式子 expression
        Val = [h, k]
        TE = GetTE(i, sp.latex(St), Val)
        TE["Tip"] = "頂點坐標x ,y ?"
        #TE["Plot"]=a*(x-h)**2+k
        NTE.append(TE)
    return NTE


"""
PF305解直角三角形    
"""


def Post_PF305_Expr(NTE):
    pass


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


def Get_PF305_Expr(QizAmt):
    NTE = []
    for i in range(0, QizAmt):
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

        TE = GetTE(i, St, Val)
        NTE.append(TE)
    return NTE
