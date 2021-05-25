Attribute VB_Name = "Module1"
Option Explicit
 
 Type AFrc
   FenZ           As Single
   FenM          As Single
   Sgn              As Integer
   St                As String
   Val              As Single
   Note            As String
End Type
 
Type AExps                                         ' 多项式结构
   n                 As Integer                      ' 次数
   Nm             As String                        ' 变量名
   Prop           As Integer                      ' 0：整系数，1：分系数
   Xs()            As AFrc                         '  各项系数
   XsG            As AFrc                        ' 整体的系数
   St                As String                       ' 单行表达式，字串型
   Note           As String                        ' 可能另有的特别说明
End Type

Public TiHao              As Integer               ' 题号
Public TiXing            As Integer                 ' 题型
Public Epslon            As Single                  ' 允许误差
Public T1                  As Single                  ' 起始计时
Public StdTime(5)      As Single                  ' 标准时间(解题的限定时间)
Public Over               As Boolean              ' 10题练习完成
Public SwJie             As Boolean               ' 是否已经解答
Public TZD               As String                   ' 鼠标停驻点
Public Exp1              As AExps
Public Exp2              As AExps


' -------出题：题型   Tx，------- Tk 是最大数字 -----------
Public Function CreatAExp(Tk As Single, Tx As Integer) As String
Dim i As Integer, j As Integer, n As Single, m As Single, k As Single
Dim TF1 As AFrc, TF2 As AFrc
Dim Txp As AExps, Txp1 As AExps, Txp2 As AExps
Dim Ts1 As String, Ts2 As String, Ts3 As String, Ts4 As String
Dim s1 As String, s2 As String, s3 As String, s4 As String
Dim a As Single, b As Single, c As Single, Sk As String, Sm As String, Sn As String
Dim Ss As Variant
On Error Resume Next
Ss = Array("x", "k", "y", "u", "r", "(s-t)", "(a+b)", "(p-q)")
Select Case Tx
Case 1                                                       ' 整系数平方差公式           (A+B)(A-B) = A2 - B2
   Ts1 = "(M+N)(M-N)"                             '
   Ts2 = "M^2-N^2"
   i = Int(10 * Rnd) Mod 2
   If i = 0 Then
      m = TakeARnd(0, 7, 0, 0, 0, 0)
      n = TakeARnd(0, 7, 0, 1, m, m)
      Sn = Ss(n): Sm = Ss(m)
      Ts1 = Replace(Ts1, "M", Sm)
      Ts1 = Replace(Ts1, "N", Sn)
      Ts2 = Replace(Ts2, "M", Sm)
      Ts2 = Replace(Ts2, "N", Sn)
      s3 = Sm + "," + Sn + ","
   Else
      a = TakeARnd(1, 9, 0, 0, 0, 0)
      b = TakeARnd(1, 9, 0, 0, 0, 0)
      n = HCF(CLng(a), CLng(b))
      a = a / n: b = b / n
      m = TakeARnd(0, 7, 0, 0, 0, 0)
      n = TakeARnd(0, 7, 0, 1, m, m)
      Sm = Ss(m): If a > 1 Then Sm = Str(a) + Sm
      Sn = Ss(n): If b > 1 Then Sn = Str(b) + Sn
      Ts1 = Replace(Ts1, "M", Sm)
      Ts1 = Replace(Ts1, "N", Sn)
      Sm = Ss(m): If a > 1 Then Sm = Str(a * a) + Sm
      Sn = Ss(n): If b > 1 Then Sn = Str(b * b) + Sn
      Ts2 = Replace(Ts2, "M", Sm)
      Ts2 = Replace(Ts2, "N", Sn)
      s3 = Ss(m) + "," + Ss(n) + ","
   End If
   Range("D119") = AllTrim(Ts1)                                 ' 命题
   Range("D121") = AllTrim(Ts2)                                 ' 答案
Case 2                                                                      ' 分系数平方差公式           (A+B)(A-B) = A2 - B2
   n = TakeARnd(0, 7, 0, 0, 0, 0)
   Sn = Ss(n)
   s3 = Sn + ","
   Txp1 = TakeAExp(1, 9, Sn, 0, 1)
   a = Txp1.Xs(1).FenZ
   If a = 1 Then
      If Left(Sn, 1) = "(" Then
         s1 = Mid(Sn, 2, Len(Sn) - 2)
      Else
         s1 = Sn
      End If
   Else
      s1 = Str(a) + Sn
   End If
   Range("D119") = Trim(s1)
   Range("D120") = Trim(Str(Txp1.Xs(1).FenM))
   Range("G119") = Trim(Str(Txp1.Xs(0).Sgn * Txp1.Xs(0).FenZ))
   Range("G120") = Trim(Str(Txp1.Xs(0).FenM))
   a = Txp1.Xs(1).FenZ: a = a * a
   b = Txp1.Xs(1).FenM: b = b * b
   s1 = Sn + "^2": If a <> 1 Then s1 = Str(a) + s1
   Range("D121") = Trim(s1)
   Range("D122") = Trim(Str(b))
   a = Txp1.Xs(0).FenZ: a = a * a
   b = Txp1.Xs(0).FenM: b = b * b
   Range("G121") = Trim(Str(a))
   Range("G122") = Trim(Str(b))
Case 3                                                         '整系数完全平方公式  (A+B)^2
   i = Int(10 * Rnd) Mod 2
   If i = 0 Then                                               ' (A+B)^2
      Ts1 = "(M+N)^2"
      Txp1 = TakeAExp(1, 9, "x", 0, 0)          '常数项不为0,可正可负
      Txp2 = TxpXTxp1(Txp1, Txp1)
      s1 = "(" + Txp1.St + ")^2"
      m = TakeARnd(0, 7, 0, 0, 0, 0)
      Ts1 = Replace(s1, "x", Ss(m))
      s2 = Txp2.St
      Ts2 = Replace(s2, "x", Ss(m))
      s3 = Ss(m) + ","
   Else                                                           ' (A+B+C)^2
      Ts1 = "(K+M+N)^2"
      Ts2 = "K^2+M^2+N^2+2KM+2KN+2MN"
      i = Int(10 * Rnd) Mod 2
      If i = 0 Then
         k = TakeARnd(0, 7, 0, 0, 0, 0)
         m = 7 - k
         n = m
         Do While n = m Or n = k
            n = TakeARnd(0, 4, 0, 0, 0, 0)
         Loop
         Sk = Ss(k): Sm = Ss(m): Sn = Ss(n)
         Ts1 = Replace(Ts1, "K", Sk)
         Ts1 = Replace(Ts1, "M", Sm)
         Ts1 = Replace(Ts1, "N", Sn)
         Ts2 = Replace(Ts2, "K", Sk)
         Ts2 = Replace(Ts2, "M", Sm)
         Ts2 = Replace(Ts2, "N", Sn)
         s3 = Sk + "," + Sm + "," + Sn + ","
      Else
         a = TakeARnd(1, 9, 0, 0, 0, 0)
         b = TakeARnd(-9, 9, 0, 1, 0, 0)
         c = TakeARnd(-9, 9, 0, 1, 0, 0)
         s1 = Str(a) + "," + Str(b) + "," + Str(c) + ","
         n = HCF2(s1)
         a = a / n: b = b / n: c = c / n
         k = TakeARnd(0, 5, 0, 0, 0, 0)
         m = TakeARnd(0, 5, 0, 1, k, k)
         Sk = Ss(k): If a <> 1 Then Sk = Str(a) + Sk
         Sm = Ss(m)
         If b = -1 Then
            Sm = "-" + Sm
         ElseIf b <> 1 Then
            Sm = Str(b) + Sm
         End If
         If b > 0 Then Sm = "+" + Sm
         Sn = Str(c):  If c > 0 Then Sn = "+" + Sn
         Ts1 = Replace(Ts1, "K", Sk)
         Ts1 = Replace(Ts1, "+M", Sm)
         Ts1 = Replace(Ts1, "+N", Sn)
         s1 = "": If Abs(a) <> 1 Then s1 = Str(a * a)
         s2 = "": If Abs(b) <> 1 Then s2 = Str(b * b)
         Ts2 = s1 + Ss(k) + "^2" + "+" + s2 + Ss(m) + "^2" + "+" + Str(c * c)
         s1 = Str(2 * a * b): If a * b > 0 Then s1 = "+" + s1
         s2 = Str(2 * a * c):: If a * c > 0 Then s2 = "+" + s2
         s3 = Str(2 * b * c): If b * c > 0 Then s3 = "+" + s3
         Ts2 = Ts2 + s1 + Ss(k) + Ss(m) + s2 + Ss(k) + s3 + Ss(m)
         s3 = Ss(k) + "," + Ss(m) + ","
      End If
   End If
   Range("D119") = AllTrim(Ts1)                                 ' 命题
   Range("D121") = AllTrim(Ts2)                                 ' 答案
Case 4                                                                       ' 分系数完全平方公式  (A+B)^2
   Ts1 = "(M+N)^2"
   m = TakeARnd(0, 7, 0, 0, 0, 0)
   s3 = Ss(m) + ","
   Txp1 = TakeAExp(1, 9, "x", 0, 1)
   s1 = Ss(m)
   a = Txp1.Xs(1).Sgn * Txp1.Xs(1).FenZ
   If a = -1 Then
      s1 = "-" + s1
   ElseIf a <> 1 Then
      s1 = Str(a) + s1
   End If
   Range("D119") = AllTrim(s1)
   Range("D120") = Trim(Str(Txp1.Xs(1).FenM))
   Range("G119") = Trim(Str(Txp1.Xs(0).Sgn * Txp1.Xs(0).FenZ))
   Range("G120") = Trim(Str(Txp1.Xs(0).FenM))
   Txp2 = TxpXTxp1(Txp1, Txp1)
   s1 = Ss(m) + "^2"
   a = Txp2.Xs(2).Sgn * Txp2.Xs(2).FenZ
   If a <> 1 Then s1 = Str(a) + s1
   Range("D121") = AllTrim(s1)
   Range("D122") = Trim(Str(Txp2.Xs(2).FenM))
   s2 = Ss(m)
   b = Txp2.Xs(1).Sgn * Txp2.Xs(1).FenZ
   If b = -1 Then
      s2 = "-" + s2
   ElseIf b <> 1 Then
      s2 = Str(b) + s2
   End If
   Range("F121") = AllTrim(s2)
   Range("F122") = Trim(Str(Txp2.Xs(1).FenM))
   Range("G121") = Trim(Str(Txp2.Xs(0).Sgn * Txp2.Xs(0).FenZ))
   Range("G122") = Trim(Str(Txp2.Xs(0).FenM))
Case 5                                                                 ' 完全立方
   Txp1 = TakeAExp(1, 6, "x", 1, 0)                      '常数项不为0,可正可负
   Txp1.XsG.FenZ = 1
   Txp1 = PlasticExp(Txp1, 0)
   Txp2 = TxpXTxp1(Txp1, Txp1)
   Txp2 = TxpXTxp1(Txp2, Txp1)
   s1 = "(" + Txp1.St + ")^3"
   m = TakeARnd(0, 7, 0, 0, 0, 0)
   Ts1 = Replace(s1, "x", Ss(m))
   s2 = Txp2.St
   Ts2 = Replace(s2, "x", Ss(m))
   s3 = Ss(m) + ","
   Range("D119") = AllTrim(Ts1)                                 ' 命题
   Range("D121") = AllTrim(Ts2)                                 ' 答案
End Select
Range("D123") = s3
CreatAExp = s3
End Function


 '------ 取得[Ta, Tb] 间随机数, 小数位 Desm --------
 ' ------ 限制范围 [Tc, Td]
 ' ------SwIs 是 限制 开关, 0 不限制, 1 限制区域， 2 限制2点
Public Function TakeARnd(Ta As Single, Tb As Single, Desm As Integer, SwIs As Integer, Tc As Single, Td As Single) As Single
Dim r As Single, BL As Boolean
Randomize
BL = True
Do While BL
   r = Ta + (Tb - Ta) * Rnd
   r = Int(r * 10 ^ Desm + 0.5) / 10 ^ Desm
   Select Case SwIs
   Case 0
      BL = False
   Case 1
      BL = (r >= Tc) And (r <= Td)
   Case Else
      BL = (r = Tc) Or (r = Td)
   End Select
Loop
TakeARnd = r
End Function


 ' ------ 建构一个随机分数,  ---------------
 ' ----- 分子为(-k , k) 内的整数-------
 ' ------  分数的SwIs ：0  不允许整数，1 允许整数，2 真分数，3 假分数
Public Function TakeAFrc(k As Single, SwIs As Integer) As AFrc
Dim a As Single, b As Single, c As Single, r As Integer
Dim f As AFrc, BL As Boolean
 BL = True
 Randomize
Do While BL                                          '
   a = TakeARnd(-k, k, 0, 1, 0, 0)           '  分子
   b = TakeARnd(1, k, 0, 1, 0, 0)             ' 分母
   r = HCF(a, b)
   a = a / r: b = b / r
   Select Case SwIs
   Case 0
      BL = b = 1
   Case 1
      BL = False
   Case 2
      BL = Abs(a) >= Abs(b) Or b = 1
   Case Else
      BL = Abs(a) <= Abs(b) Or b = 1
   End Select
Loop
 f.Sgn = Sgn(a)                                  ' 分母总为正, 从分子取得符号
 f.FenZ = Abs(a)                                ' 取的符号後，分子改为正
 f.FenM = b
f.Val = f.Sgn * (f.FenZ / f.FenM)
f.St = Str(f.Sgn * f.FenZ) + "/" + Str(f.FenM)
TakeAFrc = f
End Function


' ------ 产生一个随机多项式(最高4次) ------
' ------ 最高4次，最大数字 Tk , 分系数------
' ------ n 次数， Nm 变量名 -------
' ------ Sw:  0  不允许整数，1 允许整数，2 真分数，3 假分数
' ------ Prop=0  整系数，Prop=1 分系数
Public Function TakeAExp(n As Integer, Tk As Single, Nm As String, Sw As Integer, Prop As Integer) As AExps
Dim i As Integer, j As Integer, k As Integer, m As Integer
Dim s1 As String, s2 As String
Dim a As Single, p() As Single, q() As Single
Dim Texp As AExps
If n > 4 Then n = 4
ReDim Texp.Xs(n)
ReDim p(n)
ReDim q(n)
s1 = "": s2 = ""
k = 0
Do While k <> 1 Or m <> 1
   For i = 0 To n
      Texp.Xs(i) = TakeAFrc(Tk, Sw)                    ' 不允许整数
      s1 = s1 + Str(Texp.Xs(i).FenZ) + ","
      If Prop = 0 Then Texp.Xs(i).FenM = 1
      s2 = s2 + Str(Texp.Xs(i).FenM) + ","
   Next
   k = HCF2(s1)
   m = HCF2(s2)
Loop
Texp.Xs(n).Sgn = 1
Texp.XsG.FenZ = 1
Texp.XsG.FenM = 1
Texp.XsG.Sgn = 1
Texp.n = n
Texp.Nm = Nm
Texp = PlasticExp(Texp, Prop)
TakeAExp = Texp
End Function


' ------ 一元的两个多项式相乘 -------
Public Function TxpXTxp1(Texp1 As AExps, Texp2 As AExps) As AExps
Dim i As Integer, j As Integer, k As Integer
Dim TN As Integer, Txp As AExps, Txp1 As AExps, Txp2 As AExps
Dim s1 As String, a As Single, b As Single

If Texp1.Nm <> Texp2.Nm Then Exit Function
' ---- 将分系数化为整系数 -----
Txp1 = Texp1
s1 = ""
For i = 0 To Txp1.n
   s1 = s1 + Str(Txp1.Xs(i).FenM) + ","
Next
k = LCMn(s1)
For i = 0 To Txp1.n
   Txp1.Xs(i).FenZ = Txp1.Xs(i).FenZ * k / Txp1.Xs(i).FenM
   Txp1.Xs(i).FenM = 1
Next
Txp1.XsG.FenM = Txp1.XsG.FenM * k
' -----------
Txp2 = Texp2
s1 = ""
For i = 0 To Txp2.n
   s1 = s1 + Str(Txp2.Xs(i).FenM) + ","
Next
k = LCMn(s1)
For i = 0 To Txp2.n
   Txp2.Xs(i).FenZ = Txp2.Xs(i).FenZ * k / Txp2.Xs(i).FenM
   Txp2.Xs(i).FenM = 1
Next
Txp2.XsG.FenM = Txp2.XsG.FenM * k

TN = Texp1.n + Texp2.n
Txp.n = TN
Txp.Nm = Texp1.Nm
ReDim Txp.Xs(TN)
For k = 0 To TN
   For i = 0 To Texp1.n
      For j = 0 To Texp2.n
         If i + j = k Then
            Txp.Xs(k).FenZ = Txp.Xs(k).FenZ + Txp1.Xs(i).Sgn * Txp1.Xs(i).FenZ * Txp2.Xs(j).Sgn * Txp2.Xs(j).FenZ
         End If
      Next
   Next
   a = Txp.Xs(k).FenZ
   Txp.Xs(k).Sgn = Sgn(a)
   Txp.Xs(k).FenZ = Abs(a)
   Txp.Xs(k).FenM = 1
Next
a = Txp1.XsG.FenZ * Txp2.XsG.FenZ
b = Txp1.XsG.FenM * Txp2.XsG.FenM
k = HCF(a, b)
a = a / k: b = b / k
Txp.XsG.FenZ = a
Txp.XsG.FenM = b
Txp.XsG.Sgn = Txp1.XsG.Sgn * Txp2.XsG.Sgn
Txp = PlasticExp(Txp, 1)
TxpXTxp1 = Txp
End Function


' ------ 由多项式系数整理成 多项式的单行表达式 ------
' ------ 例 2,4,6 ==> 2(x^2+2x+3)  --- 次数递减 ----
' ------ Prop:  0 -- 整系数， 1 -- 分系数
Public Function PlasticExp(Txp As AExps, Prop As Integer) As AExps
Dim i As Integer, k As Integer, n As Integer
Dim s1 As String, Ts As String
Dim Texp As AExps, a As Single, b As Single, p() As Single, q() As Single
Texp = Txp
n = Texp.n
If n = 0 Then
  Texp.St = Texp.Xs(0).St
  Texp.Prop = 0
  PlasticExp = Texp
  Exit Function
End If
s1 = ""
For i = 0 To n
   a = Texp.XsG.Sgn * Texp.XsG.FenZ * Texp.Xs(i).Sgn * Texp.Xs(i).FenZ
   b = Texp.XsG.FenM * Texp.Xs(i).FenM
   k = HCF(a, b)
   a = a / k: b = b / k
   Texp.Xs(i).Sgn = Sgn(a)
   Texp.Xs(i).FenZ = Abs(a)
   Texp.Xs(i).FenM = b
Next
Texp.XsG.Sgn = 1
Texp.XsG.FenZ = 1
Texp.XsG.FenM = 1
For i = n To 0 Step -1
   a = Texp.Xs(i).Sgn * Texp.Xs(i).FenZ
   If a <> 0 Then
      If i > 0 Then
         Ts = Texp.Nm
         If i > 1 Then Ts = Ts + "^" + Str(i)
         If a = -1 Then
            Ts = "-" + Ts
         ElseIf Abs(a) <> 1 Then
            Ts = Str(a) + Ts
         End If
         If a > 0 And i < n Then Ts = "+" + Ts
         s1 = s1 + Ts
         If Prop = 1 Then
            b = Texp.Xs(i).FenM
            If b <> 1 Then s1 = s1 + "/" + Str(b)
         End If
      Else
         If a < 0 Then
            s1 = s1 + Str(a)
         Else
            s1 = s1 + "+" + Str(a)
         End If
         If Prop = 1 Then
            b = Texp.Xs(0).FenM
            If b <> 1 Then s1 = s1 + "/" + Str(b)
         End If
      End If
  End If
Next
If Prop = 0 Then
   i = Texp.XsG.Sgn * Texp.XsG.FenZ
   If i > 1 Then s1 = Str(i) + "(" + s1 + ")"
End If
Texp.St = AllTrim(s1)
Texp.Prop = Prop
PlasticExp = Texp
End Function

' ------ 在（TR，Tc) 显示指数
Public Sub DisplayExpn(TR As Integer, Tc As Integer, Ts As String)
Dim i As Integer, k As Integer, Pos() As Integer
Dim s1 As String
ReDim Pos(0)
Pos(0) = 0
s1 = Ts
i = 1
k = 0
Do While i < Len(s1)
   i = InStr(i, s1, "^")
   If i = 0 Then
      Exit Do
  Else
      k = k + 1
      ReDim Preserve Pos(k)
      Pos(0) = k
      Pos(k) = i
      s1 = Left(s1, i - 1) + Mid(s1, i + 1)
  End If
Loop
Cells(TR, Tc) = s1
If Pos(0) > 0 Then
   For i = 1 To Pos(0)
      Cells(TR, Tc).Characters(Pos(i), 1).Font.Superscript = True
   Next
End If
End Sub

' ------ 检查两个表达式是否相等 ------
' ------ 表达式的形式可以多变，但其值应该不变  ---
Public Function CheckExps(Tx As Integer, Eps As Single) As Single
Dim i As Integer, j As Integer, k As Integer, n As Integer, m As Single
Dim s1 As String, s2 As String, Sv As String, St1 As String, St2 As String, Bst As String
Dim Bv() As String, Av() As String
Dim BL As Boolean, v1 As Single, v2 As Single
Dim a As Single, b As Single
Select Case Tx
Case 1, 3, 5
   St1 = Range("D121")
   St2 = Range("D122")
   Bst = Range("D123")
   If St1 = "" Or St2 = "" Then
      CheckExps = 0
      Exit Function
   End If
   s1 = Bst
   Sv = ""
   Do While s1 <> ""
      i = InStr(s1, ",")
      If i > 0 Then
         n = n + 1
         ReDim Preserve Bv(n)
         Bv(0) = n
         Bv(n) = Left(s1, i - 1)
         s1 = Mid(s1, i + 1)
         Sv = Sv + Bv(n) + ","
      End If
   Loop
   Sv = "0,1,2,3,4,5,6,7,8,9,)," + Sv
   s1 = AllTrim(St1)
   s2 = AllTrim(St2)
   For i = 1 To n
      s1 = IntoStr(s1, Bv(i), "*", Sv)
      s2 = IntoStr(s2, Bv(i), "*", Sv)
   Next
   BL = True
   For j = 1 To 5
      For i = 1 To n
         a = TakeARnd(-5, 5, 2, 1, 0, 0)
         Range("L120") = a
         Sv = Trim(Str(a))
         s1 = Replace(s1, Bv(i), Sv)
         s2 = Replace(s2, Bv(i), Sv)
      Next
      Range("L121") = "=" + s1
      Range("L122") = "=" + s2
      v1 = Range("L121")
      v2 = Range("L121")
      BL = BL And Abs(v1 - v2) < Eps
   Next
   m = 0
   If BL Then m = 0.2
   ReDim Av(0)
   s1 = St1: Sv = "1"
   j = 0: k = 0: i = 0
   Do While s1 <> "" And Sv <> ""
      i = i + 1
      Sv = Mid(s1, i, 1)
      If j = 0 And (Sv = "+" Or Sv = "-") Then
          k = k + 1
          ReDim Preserve Av(k)
          Av(0) = k
          Av(k) = Left(s1, i - 1)
          s1 = Mid(s1, i)
          i = 1
      ElseIf Sv = "(" Then
         j = j + 1
      ElseIf Sv = ")" Then
        j = j - 1
      End If
   Loop
   If s1 <> "" Then
      k = k + 1
      ReDim Preserve Av(k)
      Av(0) = k
      Av(k) = s1
   End If
   If Left(St2, 1) <> "-" Then St2 = "+" + St2
   For i = 1 To k
      j = InStr(St2, Av(i))
      If j > 0 Then m = m + 0.8 / k
   Next
Case 2
   m = 0
   s1 = LCase(Range("D121"))
   s2 = LCase(Range("I121"))
   If AllTrim(s1) = AllTrim(s2) Then m = m + 0.25
   If Range("D122") = Range("I122") Then m = m + 0.25
   If Range("G121") = Range("K121") Then m = m + 0.25
   If Range("G122") = Range("K122") Then m = m + 0.25
Case 4
   m = 0
   s1 = LCase(Range("D121"))
   s2 = LCase(Range("I121"))
   If AllTrim(s1) = AllTrim(s2) Then m = m + 1 / 6
   If Range("D122") = Range("I122") Then m = m + 1 / 6
   If LCase(Range("F121")) = LCase(Range("K121")) Then m = m + 1 / 6
   If Range("F122") = Range("K122") Then m = m + 1 / 6
   If Range("G121") = Range("L121") Then m = m + 1 / 6
   If Range("G122") = Range("L122") Then m = m + 1 / 6
End Select
CheckExps = m
End Function


' ------------- 两个数的 HCF ------------
' ------- i, j 可以为负可以为0，但HCF 总是正的 ------
Public Function HCF(i As Single, j As Single) As Single
Dim m As Long, n As Long, r As Single, k As Single
m = Abs(CLng(i)): n = Abs(CLng(j))
If Sgn(m) * Sgn(n) = 0 Then
   n = 1
Else
   If m < n Then r = m: m = n: n = r
   r = m Mod n
   k = n
   If r > 0 Then n = HCF(k, r)
End If
HCF = n
End Function

' ------ 多个数的HCF ------
Public Function HCF2(Ts As String) As Integer
Dim m As Single, n As Single, r As Single
Dim Ss() As Single, s1 As String, s2 As String
Dim i As Integer, j As Integer, k As Integer, Sn As Integer
s1 = Ts
If Right(s1, 1) <> "," Then s1 = s1 + ","
Sn = 0
Do While s1 <> ""
   i = InStr(s1, ",")
   s2 = Left(s1, i - 1)
   Sn = Sn + 1
   ReDim Preserve Ss(Sn)
   Ss(Sn) = Abs(Val(s2))
   s1 = Mid(s1, i + 1)
Loop
For i = 1 To Sn - 1
   For j = i + 1 To Sn
     If Ss(j) < Ss(i) Then k = Ss(i): Ss(i) = Ss(j): Ss(j) = k
   Next
Next
n = Ss(1)
For i = 2 To Sn
   m = Ss(i)
   If Sgn(m) * Sgn(n) = 0 Then
      n = 1
   Else
      r = m Mod n
      If r > 0 Then n = HCF(n, r)
   End If
Next
HCF2 = n
End Function

' ------ 2数的最小公倍数 ------
Public Function LCM2(a As Single, b As Single) As Single
Dim Ta As Single, n As Integer
Ta = a * b
n = HCF(a, b)
LCM2 = Ta / n
End Function

' ------ 多个数的最小公倍数 ------
' ------ Ss ="1,2,3,4,5,6," 的形式
Public Function LCMn(Ss As String) As Single
Dim s1 As String, s2 As String
Dim a() As Single, b As Single, i As Integer, n As Integer
s1 = Ss
Do While s1 <> ""
   i = InStr(s1, ",")
   If i > 1 Then
      n = n + 1
      ReDim Preserve a(n)
      a(0) = n
      s2 = Left(s1, i - 1)
      a(n) = Val(s2)
      s1 = Mid(s1, i + 1)
   End If
Loop
b = 1
For i = 1 To n
   b = LCM2(b, a(i))
Next
LCMn = b
End Function



' ------ 在Ss中寻找s1, 如果s1前面一个符号在s2中，则在s1前插入Sk ---
' ------ 例： Ss="3x+1", 要在x前插入一个"*"
' ------ s2="0,1,2,3,4,5,6,7,8,9,"
' ------ Ss=IntoStr(Ss,"x","*",s2)   ==> Ss = 3*x+1    (由不可运算变成可运算)
Public Function IntoStr(Ss As String, s1 As String, Sk As String, s2 As String) As String
Dim i As Integer, j As Integer, Sd As String, St As String
On Error Resume Next
Sd = Ss
i = 1
j = 0
Do While i > 0
  i = InStr(j + 1, Sd, s1)
  If i > 1 Then
     St = Mid(Sd, i - 1, 1) + ","
     If InStr(s2, St) > 0 Then Sd = Left(Sd, i - 1) + Sk + Mid(Sd, i)
  End If
  j = i + 1
Loop
IntoStr = Sd
End Function

' ------- 排除字串前後、中间的所有空格 -------
Public Function AllTrim(Ss As String) As String
Dim i As Integer
Dim s1 As String, s2 As String
s1 = ""
For i = 1 To Len(Ss)
   s2 = Mid(Ss, i, 1)
   If s2 <> " " Then s1 = s1 + s2
Next
AllTrim = s1
End Function

' ----- 文字框捉模弹跳 ----------
Sub TextBox1_Click()
Range("A2").Select
End Sub
' ----------  代替MsgBox ----------
Sub TextBox2_Click()
Sheet01.Shapes.Range(2).Visible = False
Range("A2").Select
End Sub



