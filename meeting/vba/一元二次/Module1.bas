Attribute VB_Name = "Module1"
Option Explicit
Type AFrc                                      ' 分数的结构
   FenZ     As Single                          ' 分子，正整型数
   FenM    As Single                         ' 分母，正整型数
   Sgn        As Integer                       ' 符号，只取±1
   Val        As Single                         ' 分数的值，单精型数
    Xs        As Single
   St          As String                         ' 分数的单行表达式，字串型
   Note      As String
End Type
 
Type AExps1                                   ' 一次式结构  k(ax+b)
   Nm          As String
   Xs           As Single                         '  系数
   a              As Single
   b              As Single
   St             As String                       ' 分数的单行表达式，字串型
   Note         As String                      ' 可能另有的特别说明
End Type

Type AExpsF                                     '分式的结构    k(ax+b)/m(cx+d)
   Nm          As String
   FenZ        As AExps1                     ' 变量暂定为 x
   FenM       As AExps1                      '
   St             As String                        ' 分数的单行表达式，字串型
   Note         As String                        ' 可能另有的特别说明
End Type

Public TiHao              As Integer               ' 题号
Public TiXing              As Integer                 ' 题型
Public Epslon              As Single                  ' 允许误差
Public t1                     As Single                  ' 起始计时
Public StdTime(4)      As Single                  ' 标准时间(解题的限定时间)
Public Over                As Boolean              ' 10题练习完成
Public SwJie               As Boolean               ' 是否已经解答
Public TZD                 As String                   ' 鼠标停驻点
Public ExpA              As AExps1
Public ExpB              As AExps1
Public ExpC              As AExps1


' -------出题：题型   Tx，------- Tk 是最大数字 -----------
Public Function CreatAExp(Tk As Single, Tx As Integer) As String
Dim TOp(4) As String, TF1 As AFrc, TF2 As AFrc
Dim s1 As String, s2 As String, s3 As String, x1 As Single, x2 As Single, t1 As Single, t2 As Single
Dim Ts1 As String, Ts2 As String
Dim a As Single, b As Single, c As Single, d As Single, e As Single, f As Single, g As Single, h As Single
Dim p As Single, q As Single, r As Single, u As Single, v As Single, m As Single, n As Single
Dim Aa As Single, Bb As Single, Cc As Single
Dim i As Single, j As Single, k As Single

On Error Resume Next
TOp(0) = "+"
TOp(1) = "- "
TOp(2) = Range("D15")
TOp(3) = Range("D16")
Range("E20:G21") = ""
Range("G15:L16") = ""
Select Case Tx
Case 1
   k = 2
   Do While k > 1
      m = TakeARnd(2, 7, 0, 1, -1, 1)
      n = TakeARnd(2, 7, 0, 1, -1, 1)
      k = HCF(m, n)
      m = m / k
      n = n / k
   Loop
   a = TakeARnd(1, 4, 0, 1, 0, 0)
   b = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   c = TakeARnd(1, 4, 0, 1, 0, 0)
   d = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   e = TakeARnd(1, 4, 0, 1, 0, 0)
   f = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   ExpA = FmtAExps1(a, b, "x", False)
   ExpB = FmtAExps1(c, d, "x", False)
   ExpC = FmtAExps1(e, f, "x", False)
   a = ExpA.a: b = ExpA.b
   c = ExpB.a: d = ExpB.b
   e = ExpC.a: f = ExpC.b
   ExpA.Note = Str(m)
   ExpC.Note = Str(n)
   Aa = m * a * c
   Bb = m * (a * d + b * c) - n * e
   Cc = m * b * d - n * f
   Range("K114") = Aa
   Range("K115") = Bb
   Range("K116") = Cc
Case 2
   i = Int(100 * Rnd) Mod 2
   If i = 0 Then
      Aa = TakeARnd(1, Tk, 0, 1, 0, 0)
      Bb = TakeARnd(-Tk, Tk, 0, 0, 0, 0)
      Cc = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   Else
      a = TakeARnd(1, Tk, 0, 1, 0, 0)
      b = TakeARnd(-Tk, Tk, 0, 0, 0, 0)
      c = TakeARnd(1, Tk, 0, 1, 0, 0)
      d = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
      Aa = a * c
      Bb = a * d + b * c
      Cc = b * d
   End If
   Ts1 = FmtAExp2(Aa, Bb, Cc, "x")
   Ts2 = SoluExp2(Aa, Bb, Cc)
   i = InStr(Ts2, ",")
   s1 = Left(Ts2, i - 1)
   s2 = Mid(Ts2, i + 1)
   s2 = Left(s2, Len(s2) - 1)
   Range("K114") = s1
   Range("K115") = s2
   If s1 <> "@" Then
      s1 = Replace(s1, "J", "sqrt")
      s2 = Replace(s2, "J", "sqrt")
      Range("E19") = "=" + s1
      Range("E20") = "=" + s2
   End If
Case 3                                                          ' ax2+kx+c=0, ax2 + k(x+c) = 0
   a = TakeARnd(1, Tk, 0, 1, 0, 0)
   k = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   x1 = TakeARnd(-Tk, Tk, 0, 1, 0, 0)
   Range("K10") = x1
   Range("K114") = x1
   TF1 = FmtAFrc(a * x1 + k, -a)
   Range("K115") = TF1.St
   Range("K116") = k
   c = -(a * x1 * x1 + k * x1)
   s1 = "": If a > 1 Then s1 = Str(a)
   s2 = "": If c <> 0 Then s2 = Str(c)
   If c > 0 Then s2 = "+" + s2
   Ts1 = s1 + "x^2+kx" + s2
   Range("E20") = "=" + TF1.St
Case 4
   a = TakeARnd(1, Tk, 0, 1, 0, 0)
   k = TakeARnd(-5, 5, 0, 1, 0, 0)
   x1 = TakeARnd(-3, 3, 0, 1, 0, 0) * k
   Range("K10") = x1
   Range("K114") = x1
   TF1 = FmtAFrc(a * x1 + k, -a)
   Range("K115") = TF1.St
   Range("K116") = k
   c = -(a * x1 * x1 + k * x1) / k
   s1 = "": If a > 1 Then s1 = Str(a)
   s2 = "": If c <> 0 Then s2 = Str(c)
   If c > 0 Then s2 = "+" + s2
   If s2 = "" Then
      Ts1 = s1 + "x^2+kx"
   Else
      Ts1 = s1 + "x^2+k(x" + s2 + ")"
   End If
   Range("E20") = "=" + TF1.St
End Select
eeee:
CreatAExp = Ts1
End Function


'------ 取得[Ta, Tb] 间随机数, 小数位 Desm --------
' ------ 限制范围 [Tc, Td]
 ' ------Sw 是 限制 开关, 0 不限制, 1 限制
Public Function TakeARnd(Ta As Single, Tb As Single, Desm As Integer, SwIs As Integer, Tc As Single, Td As Single) As Single
Dim r As Single
Randomize
If SwIs = 0 Then                                                     ' 如果不限制
  r = Ta + (Tb - Ta) * Rnd
  r = Int(r * 10 ^ Desm + 0.5) / 10 ^ Desm
Else                                                                          ' 有限制
   r = (Tc + Td) / 2
   Do While r >= Tc And r <= Td
      r = Ta + (Tb - Ta) * Rnd
      r = Int(r * 10 ^ Desm + 0.5) / 10 ^ Desm
   Loop
End If
TakeARnd = r
End Function


' ------ 建构一个随机分数, 不允整数(例  4/2) ，允许未约分 (例 2/4) ---------------
' ----- 分子为(-k , k) 内的整数 ，分母为(2 , k) 内的整数-------
Public Function TakeAFrc(k As Single) As AFrc
Dim a As Single, b As Single, r As Integer
Dim f As AFrc
   Randomize
   Do While r = 0                                     '分子分母不能整除，排除出现整数的情况。
      a = TakeARnd(-k, k, 0, 1, 0, 0)        ' 分子排除0
      b = TakeARnd(-k, k, 0, 1, 0, 0)
      r = a Mod b
   Loop
   TakeAFrc = FmtAFrc(a, b)
End Function


'------- 格式化一个分数 -----------
Public Function FmtAFrc(Ta As Single, Tb As Single) As AFrc
Dim a As Single, b As Single, r As Single
Dim s1 As String
a = Ta: b = Tb
r = HCF(a, b)
FmtAFrc.Sgn = Sgn(a) * Sgn(b)
a = Abs(a / r): b = Abs(b / r)
FmtAFrc.FenZ = a
FmtAFrc.FenM = b
FmtAFrc.Val = FmtAFrc.Sgn * a / b
If a = 0 Then
   s1 = "0"
ElseIf b = 1 Then
   s1 = Str(a)
Else
   s1 = Str(a) + "/" + Str(b)
End If
If FmtAFrc.Sgn < 0 Then s1 = "-" + s1
FmtAFrc.St = AllTrim(s1)
End Function


'  ------ 由系数 a , b 构建一次式 (带格式化)   k(ax+b)  --------------
' ------ SwXs = False 不保留系数(系数为1)
Public Function FmtAExps1(Ta As Single, Tb As Single, Nm As String, SwXs As Boolean) As AExps1
Dim s1 As String, s2 As String, Ts As String
Dim a As Single, b As Single, n As Single
If Ta = 0 And Tb = 0 Then Exit Function
If Tb = 0 Then
   FmtAExps1.a = 1
   FmtAExps1.b = 0
   FmtAExps1.Xs = Ta
   FmtAExps1.Nm = Nm
   Ts = Nm
   If Ta = -1 Then
      Ts = "-" + Ts
   ElseIf Ta <> 1 Then
      Ts = Str(Ta) + Nm
   End If
ElseIf Ta = 0 Then
   FmtAExps1.a = 0
   FmtAExps1.b = 1
   FmtAExps1.Xs = Tb
   FmtAExps1.Nm = Nm
   Ts = Str(Tb)
Else
   n = HCF(CLng(Ta), CLng(Tb))
   a = Ta / n
   b = Tb / n
   If a < 0 Then a = -a: b = -b: n = -n
   If Not SwXs Then n = 1
   FmtAExps1.a = a
   FmtAExps1.b = b
   FmtAExps1.Xs = n
   FmtAExps1.Nm = Nm
   If a = 0 Then
      s1 = ""
   ElseIf a = 1 Then
      s1 = Nm
   ElseIf a = -1 Then
      s1 = "-" + Nm
   Else
      s1 = Str(a) + Nm
   End If
   If b > 0 Then
      If a = 0 Then
         s1 = Str(b)
      Else
         s1 = s1 + "+" + Str(b)
      End If
   ElseIf b < 0 Then
      s1 = s1 + Str(b)
   End If
   If n = -1 Then
      Ts = "-(" + s1 + ")"
   ElseIf n = 1 Then
      Ts = s1
   Else
      Ts = Str(n) + "(" + s1 + ")"
   End If
End If
FmtAExps1.St = AllTrim(Ts)
End Function


'  ------ 由系数 a , b ,c 构建二次式 (带格式化)   ax2+bx+c  --------------
Public Function FmtAExp2(Ta As Single, Tb As Single, Tc As Single, Nm As String) As String
Dim s1 As String, s2 As String, s3 As String, Ts As String
Dim a As Single, b As Single, c As Single, n As Single, m As Single
If Ta = 0 Then Exit Function
a = Ta: b = Tb: c = Tc
n = HCF(a, b)
If b = 0 Then n = a
m = HCF(n, c)
If c = 0 Then m = n
a = a / m: b = b / m: c = c / m
If a = 1 Then
   s1 = "x^2"
Else
   s1 = Str(a) + "x^2"
End If
If b = 0 Then
   s2 = ""
ElseIf b = 1 Then
   s2 = "+x"
ElseIf b = -1 Then
   s2 = "-x"
ElseIf b < 0 Then
   s2 = Str(b) + "x"
Else
   s2 = "+" + Str(b) + "x"
End If
s3 = ""
If c > 0 Then
   s3 = "+" + Str(c)
ElseIf c < 0 Then
   s3 = Str(c)
End If
Ts = s1 + s2 + s3
FmtAExp2 = Ts
End Function


'------- 格式化一个分数 的平方根 J(a/b) ==> aJ(b)/c -----------
Public Function FmtAFR(Ta As Single, Tb As Single) As AFrc
 Dim a As Single, b As Single, c As Single, x As Single, n As Single
 Dim i As Integer, j As Integer, k As Single, r As Single
 Dim s1 As String
If Ta * Tb < 0 Then
   FmtAFR.Xs = -9999
   Exit Function
End If
a = Abs(Ta)
b = Abs(Tb)
n = HCF(a, b)
a = a / n
b = b / n
x = a * b
i = 1
k = 1
Do While x > i * i
i = i + 1
j = i * i
r = x Mod j
If r = 0 Then
   k = k * i
   i = 1
   x = x / j
End If
Loop
n = HCF(k, b)
k = k / n
b = b / n
If k = 1 Then
   If x = 1 Then
      s1 = "1"
   Else
      s1 = "J" + "( " + Str(x) + ")"
   End If
Else
   If x = 1 Then
      s1 = Str(k)
   Else
      s1 = Str(k) + "J" + "( " + Str(x) + ")"
   End If
End If
If b > 1 Then s1 = s1 + "/" + Str(b)
FmtAFR.FenM = b
FmtAFR.FenZ = x
FmtAFR.Xs = k
FmtAFR.Val = k * Sqr(x) / b
FmtAFR.St = AllTrim(s1)
FmtAFR.Sgn = 1
End Function


' ------ 格式化二次方程的解 ax2+bx+c= 0
' ------  输出两根用逗号“，”分隔。
Public Function SoluExp2(Ta As Single, Tb As Single, Tc As Single) As String
Dim a As Single, b As Single, c As Single, d As Single, n As Single, m As Single, u As Single
Dim s1 As String, s2 As String, s3 As String, Ts As String
Dim i As Integer, j As Integer, k As Integer
Dim TF1 As AFrc, TF2 As AFrc
a = Ta: b = Tb: c = Tc
n = HCF(a, b)
m = HCF(n, c)
a = a / m: b = b / m: c = c / m
 d = b * b - 4 * a * c
 Select Case Sgn(d)
 Case -1
    s1 = "@": s2 = "@"
 Case 0
    TF1 = FmtAFrc(-b, 2 * a)
    s1 = TF1.St
    s2 = s1
 Case 1
   TF1 = FmtAFR(d, 1)
   n = TF1.Xs
   m = TF1.FenZ
   If m = 1 Then
      s1 = FmtAFrc(-b + n, 2 * a).St
      s2 = FmtAFrc(-b - n, 2 * a).St
   Else
      TF2 = FmtAFrc(n, 2 * a)
      If b = 0 Then
         s3 = "": If TF2.FenZ > 1 Then s3 = Str(TF2.FenZ)
         If TF2.FenM = 1 Then
            s1 = s3 + "J(" + Str(m) + ")"
            s2 = "-" + s1
         Else
            s1 = s3 + "J(" + Str(m) + ")/" + Str(TF2.FenM)
            s2 = "-" + s1
         End If
      Else
         s3 = Str(b) + "," + Str(n) + "," + Str(2 * a) + ","
         j = HCF2(s3)
         b = b / j: n = n / j: u = 2 * a / j
         s3 = "": If n > 1 Then s3 = Str(n)
         If u = 1 Then
            s1 = Str(-b) + "+" + s3 + "J(" + Str(m) + ")"
            s2 = Str(-b) + "-" + s3 + "J(" + Str(m) + ")"
         Else
            s1 = "(" + Str(-b) + "+" + s3 + "J(" + Str(m) + "))/" + Str(u)
            s2 = "(" + Str(-b) + "-" + s3 + "J(" + Str(m) + "))/" + Str(u)
         End If
      End If
   End If
 End Select
Ts = s1 + "," + s2 + ","
SoluExp2 = AllTrim(Ts)
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


'在 Cells(Tr,Tc) 处显示根式, 约定：根指数都是2次。
'例：将表达式-3J(x+2)+2J(x-2)显示在Range("C7") 上：
' DisplayRoot(7,3,"-3J(x+2)+2J(x-2)"), 得到 -3√(x+2)+2√(x-2) 的显示形式。
Public Sub DisplayRoot(TR As Integer, Tc As Integer, Ts As String)
Dim s1 As String, s2 As String, s3 As String, Gh As String
Dim i As Integer, j As Integer, k As Integer, Start As Integer
Dim L(5) As Integer, Pos(5) As Integer
s1 = AllTrim(UCase(Ts))
Gh = Range("C15")
s1 = Replace(s1, "J", Gh)
i = 1:  k = 0
Do While i > 0
 i = InStr(i, s1, Gh + "(")
   If i = 0 Then Exit Do
   j = InStr(i + 2, s1, ")")
   If j = 0 Then Exit Do
   s2 = Mid(s1, i + 2, j - i - 2)
   k = k + 1
   Pos(k) = i
   L(k) = Len(s2)
   s1 = Left(s1, i) + s2 + Mid(s1, j + 1)
Loop
Cells(TR, Tc) = s1
Cells(TR, Tc).Select
With Selection.Phonetics.Font
    .Name = "SimSun-ExtB"
    .Size = 12
End With
For i = 1 To k
   Cells(TR, Tc).Characters(Pos(i) + 1, 1).PhoneticCharacters = String(L(i), Range("C16"))
Next
Cells(TR, Tc).Phonetic.Visible = True
End Sub





' ----- 借用 C22计算一个表达式的值 -----
' --------- 在式 St 中，以x 的值代入 Nm 计算所得的值 ----------
' ----- 例： 要对 3(4x+1) 计算在 x=2.5时的值 -------
Public Function Valuation(St As String, Nm As String, x As Single) As Single
Dim s1 As String, s2 As String, a As Single
Dim i As Integer
On Error GoTo eeee
s1 = IntoStr(St, Nm, "*", "0,1,2,3,4,5,6,7,8,9,")       ' 在Nm 前如果是数字，则要插入乘号*
s1 = IntoStr(s1, "(", "*", "0,1,2,3,4,5,6,7,8,9,")                     '在 "(" 前如果是数字，则要插入乘号*
s1 = Replace(s1, "J", "sqr")
i = InStr(s1, "/")
If i > 0 Then s2 = Mid(s1, i + 1)
Range("C22") = "=" + Replace(s2, Nm, Str(x))
a = Range("C22")
If Abs(a) < 0.0001 Then
   Valuation = -9999
   Exit Function
End If
Range("C22") = "=" + Replace(s1, Nm, Str(x))
Valuation = Range("C22")
eeee:
If Err <> 0 Then Valuation = -9999
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

' ----- 从位置 Start 开始，搜索 Ss 中，含Sa 中元素的位置 ----
' ------ 与 Instr不同，此处的Sa可含多个单字母元素，例如：“+,-,*,/" 运算符。
Public Function Instr2(Start As Integer, Ss As String, Sa As String) As Integer
Dim i As Integer, St As String
i = Start
Do While i < Len(Ss) + 1
   St = Mid(Ss, i, 1) + ","
   If InStr(Sa, St) > 0 Then Exit Do
   i = i + 1
Loop
If i > Len(Ss) Then i = 0
Instr2 = i
End Function

Public Function Max(a As Single, b As Single) As Single
Max = a
If a < b Then Max = b
End Function

Public Function Min(a As Single, b As Single) As Single
Min = a
If a > b Then Min = b
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



