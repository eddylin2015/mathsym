Attribute VB_Name = "Module1"
Option Explicit
Type AFrc                                      ' 分数的结构
   FenZ     As String                          ' 分子，正整型数
   FenM    As String                          ' 分母，正整型数
   Sgn        As Integer                       ' 符号，只取±1
   Val        As Single                         ' 分数的值，单精型数
   St          As String                         ' 分数的单行表达式，字串型
End Type

Public TiHao              As Integer               ' 题号
Public TiXing            As Integer                 ' 题型
Public Epslon            As Single                  ' 允许误差
Public T1                  As Single                  ' 起始计时
Public StdTime(4)     As Single                  ' 标准时间(解题的限定时间)
Public Over               As Boolean              ' 10题练习完成
Public SwJie             As Boolean               ' 是否已经解答
Public TZD               As String                   ' 鼠标停驻点




' ------- Tk 是最大数字 ------
' -------题型   Tx
Public Function CreatAExp(Tx As Integer) As String
Dim s1 As String, s2 As String, s3 As String, s4 As String, s5 As String
Dim St As String, Ts As String
Dim a As Single, b As Single, c As Single
Dim Ts1 As String, Ts2 As String, Xx As String
Dim Ss1 As Variant, Ss2 As Variant, Ss3 As Variant
Dim i As Single, j As Single, k As Integer, p As Integer, q As Integer, r As Single
Dim x As AFrc, y As AFrc
Ss1 = Array("sin", "cos", "tan", "cot", "sec", "csc")
Ss3 = Array("I", "II", "III", "IV")
i = TakeARnd(1, 6, 0, 0, 0, 0)
j = TakeARnd(1, 6, 0, 1, i, i)
s1 = Ss1(i - 1): s2 = Ss1(j - 1)                              '已知s1, 求 s2
St = Sheet02.Cells(j + 1, i + 1)                             '答案的公式

Select Case Tx
Case 1, 2
   If Tx = 1 Then
      St = Replace(St, "k^2", s1 + "^2x")
      St = Replace(St, "k", s1 + " x")
   Else
      St = Replace(St, "k", "A")
   End If
   k = InStr(St, "/")
   If k = 0 Then
      Ts1 = St
      Ts2 = ""
   Else
      Ts1 = Left(St, k - 1)
      Ts2 = Mid(St, k + 1)
   End If
   If Tx = 1 Then
      s1 = s1 + " x"
      s2 = s2 + " x"
   Else
      s1 = s1 + " x = A"
      s2 = s2 + " x"
   End If
   Xx = Ss3(0)
Case 3                                                              ' 给定函数值，指定象限
   If i < 3 Then
      x = TakeAFrc(9, 2)                                     ' sin,cos 取真分数
   ElseIf i < 5 Then
      x = TakeAFrc(9, 1)                                     ' tan,coe, 不限
   Else
      x = TakeAFrc(9, 3)                                     ' sec,csc 取假分数
   End If
   k = Int(100 * Rnd) Mod 4
   Xx = Ss3(k):
   r = Sheet02.Cells(i + 1, 8 + k)
   If r = -1 Then
      x.St = "-" + x.St
      x.Val = -1 * x.Val
      x.Sgn = -1
   End If
   s1 = s1 + " x = " + x.St                                     ' 其值的正负要跟象限而定
   s2 = s2 + " x"
   ' ---- 答案计算，化简
   p = InStr(St, "J(")
   q = InStr(St, ")")
   If p > 0 Then
      s3 = Left(St, p + 1)
      s5 = Mid(St, p + 2, q - p - 2)
      s4 = Mid(St, q)
   Else
      s3 = ""
      s5 = St
      s4 = ""
   End If
   s3 = Replace(s3, "k", "(" + x.St + ")")
   s4 = Replace(s4, "k", "(" + x.St + ")")
   s5 = Replace(s5, "k", "(" + x.St + ")")
   Range("H23") = "=" + s5
   a = Range("H23")
   y = DcmToFrc(CDbl(a), 0.000001)
   s5 = s3 + y.St + s4
   If InStr(s5, "J(") > 0 Then
      Ts1 = SimpSqr2(s5)
   Else
      Ts1 = AllTrim(s5)
   End If
   r = InStr(Ts1, "/")
   If r > 0 Then
      Ts2 = Mid(Ts1, r + 1)
      Ts1 = Left(Ts1, r - 1)
   Else
      Ts2 = ""
   End If
   If Left(Ts1, 1) = "-" Then Ts1 = Mid(Ts1, 2)
   r = Sheet02.Cells(j + 1, 8 + k)
   If r = -1 Then Ts1 = "-" + Ts1
   If Ts1 = "" Then Stop
Case 4                                                              '特殊角，例 sin A = J(3)/2   A∈ II, ==> A=? tanA =?
   Range("J10") = "A="
   Range("J11") = s2 + "A="
   s5 = "**"
   Do While s5 = "**"
      r = TakeARnd(1, 16, 0, 0, 0, 0)                      ' 角
      s5 = Sheet02.Cells(i + 1, 11 + r)
   Loop
   s1 = s1 + "A =" + s5
   s2 = "A,   " + s2 + "A"
   a = Sheet02.Cells(1, 11 + r)
   Ts1 = Str(a) + Range("C20")
   Ts2 = Sheet02.Cells(j + 1, 11 + r)
   k = Int(a / 91)
   Xx = Ss3(k)
End Select
Range("G116") = s1  'AllTrim(s1)                          ' 命题
Range("H117") = s2   'AllTrim(s2)
Range("H118") = Xx
Range("H119") = x.St
Range("E116") = Ts1                        ' 答案
Range("E117") = Ts2
Range("E118") = St
CreatAExp = s1
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
 ' ------ 本课题规定，只取正分数
Public Function TakeAFrc(k As Single, SwIs As Integer) As AFrc
Dim a As Single, b As Single, c As Single, r As Integer
Dim F As AFrc, BL As Boolean
 BL = True
 Randomize
Do While BL                                          '
   a = TakeARnd(1, k, 0, 1, 0, 0)            '  分子， 本课题规定，只取正分数
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
F.Sgn = Sgn(a)                                  ' 分母总为正, 从分子取得符号
F.FenZ = Abs(a)                                ' 取的符号後，分子改为正
F.FenM = b
F.Val = F.Sgn * (F.FenZ / F.FenM)
F.St = Str(F.Sgn * F.FenZ)
If F.FenM <> 1 Then F.St = F.St + "/" + Str(F.FenM)
F.St = AllTrim(F.St)
TakeAFrc = F
End Function



' ------------- HCF ------------
Public Function HCF(i As Single, j As Single) As Single
Dim m As Long, n As Long, p As Long, r As Single, k As Single
On Error Resume Next
m = CLng(Abs(i)): n = CLng(Abs(j))
If Sgn(m) * Sgn(n) = 0 Then
   n = 1
Else
   If m < n Then p = m: m = n: n = p
   r = m Mod n
   k = n
   If r > 0 Then n = HCF(k, r)
End If
HCF = n
End Function


' ------ 根式化简1. -------
' ------ 例 3J(8)    ==> 6J(2)
' ------ 例 2J(8/6) ==> 4J(6)/3
' ------ 例 3J(8/6) ==> 2J(3)
' ------ 例 3J(16)  ==> 12
Public Function SimpSqr1(Tst As String) As String
Dim i As Integer, j As Integer, k As Single, r As Single
Dim x As Single, a As Single, b As Single, c As Single, d As Single
Dim s1 As String, s2 As String, Ts As String, FenZ As String, FenM As String
Ts = AllTrim(Tst)
For i = 1 To Len(Ts)
   s1 = Mid(Ts, i, 1)
   If s1 = "(" Then j = j + 1
   If s1 = ")" Then j = j - 1
   If s1 = "/" And j = 0 Then Exit For
Next
If i > 1 And i < Len(Ts) Then
   Ts = Left(Ts, i - 1)
   d = Val(Mid(Tst, i + 1))
End If
i = InStr(Ts, "J(")
If i = 0 Then
   If Left(Ts, 1) = "(" And Right(Ts, 1) = ")" Then
      s1 = Mid(Ts, 2, Len(Ts) - 2)
   Else
      s1 = Ts
   End If
   SimpSqr1 = s1
   Exit Function
End If
s1 = Left(Ts, i - 1)
a = Val(s1)
If a = 0 Then
   If s1 = "" Then
      a = 1
   ElseIf s1 = "-" Then
      a = -1
   End If
End If
j = InStr(Ts, ")")
s1 = Mid(Ts, i + 2, j - i - 2)
i = InStr(s1, "/")
If i > 0 Then                                            '被开方数是分数
    b = Val(Left(s1, i - 1))
    c = Val(Mid(s1, i + 1))
    r = HCF(b, c)
    b = b / r: c = c / r                                '·约分
    b = b * c                                            ' J(b/c) ==> J(b*c)/c
Else                                                        ' 被开方数是整数
    b = Val(s1)
    c = 1
End If
x = b
i = 1
k = 1
Do While x > i * i                                     ' 对J(b) 开方
   i = i + 1
   j = i * i
   r = x Mod j
   If r = 0 Then
      k = k * i
      i = 1
      x = x / j
   End If
Loop
k = a * k                                                    ' 得到 kJ(x)/c
If d > 0 Then c = c * d
r = HCF(k, c)                                             ' 整理
k = k / r: c = c / r
s1 = ""
If k = -1 Then
   s1 = "-"
ElseIf k <> 1 Then
   s1 = Str(k)
End If
If x <> 1 Then s1 = s1 + "J(" + Str(x) + ")"
If c <> 1 Then s1 = s1 + "/" + Str(c)
SimpSqr1 = AllTrim(s1)
End Function


' ------ 根式化简2 ------
' ------ 例，-3J(32)/5        ==> -12J(2)/6
' ------ 例，5/2J(50)          ==> J(2)/4
' ------ 例，3J(32)/J(8)      ==> 6
' ------ 例，3J(32)/J(6)      ==> 4J(3)
' ------ 例，"3J(32)/-J(10) ==> -12J(5)/5
Public Function SimpSqr2(Ts As String) As String
Dim s1 As String, s2 As String, s3 As String, s4 As String
Dim i As Integer, j As Integer, k As Single, r As Single
Dim a As Single, b As Single, c As Single, d As Single

For i = 1 To Len(Ts)
   s1 = Mid(Ts, i, 1)
   If s1 = "(" Then j = j + 1
   If s1 = ")" Then j = j - 1
   If s1 = "/" And j = 0 Then Exit For
Next
If i = 0 Or i > Len(Ts) Then
   s1 = Ts
   s2 = ""
Else
   s1 = Left(Ts, i - 1)
   s2 = Mid(Ts, i + 1)
End If
s1 = SimpSqr1(s1)
s2 = SimpSqr1(s2)
If s2 = "" Then
   SimpSqr2 = s1
   Exit Function
End If
i = InStr(s1, "/")
If i > 0 Then
   b = Val(Mid(s1, i + 1))
   s1 = Left(s1, i - 1)
Else
   b = 1
End If
i = InStr(s1, "J(")
j = InStr(s1, ")")
If i > 0 Then
   a = Val(Left(s1, i - 1))
   If a = 0 Then a = 1
   s1 = Mid(s1, i, j - i + 1)
Else
   a = Val(s1)
   s1 = ""
End If
i = InStr(s2, "/")
If i > 0 Then
   d = Val(Mid(s2, i + 1))
   s2 = Left(s2, i - 1)
Else
   d = 1
End If
i = InStr(s2, "J(")
j = InStr(s2, ")")
If i > 0 Then
   c = Val(Left(s2, i - 1))
   If c = 0 Then c = 1
   s2 = Mid(s2, i, j - i + 1)
Else
   c = Val(s2)
   s2 = ""
End If
a = a * d: c = c * b                                       '系数处理
a = a * Sgn(c): c = Abs(c)
k = HCF(a, c)
a = a / k: c = c / k
If s1 <> "" And s2 = "" Then
   s3 = s1
   If a = -1 Then
      s3 = "-" + s1
   ElseIf a <> 1 Then
      s3 = Str(a) + s1
   End If
   If c <> 1 Then s3 = s3 + "/" + Str(c)
ElseIf s1 = "" And s2 <> "" Then
   i = InStr(s2, "J(")
   j = InStr(s2, ")")
   d = Val(Mid(s2, i + 2, Len(s2) - i - 2))
   c = c * d
   k = HCF(a, c)
   a = a / k: c = c / k
   s3 = s2
   If a = -1 Then
      s3 = "-" + s3
   ElseIf a <> 1 Then
      s3 = Str(a) + s3
   End If
   If c <> 1 Then s3 = s3 + "/" + Str(c)
ElseIf s1 <> "" And s2 <> "" Then
   i = InStr(s1, "J(")
   j = InStr(s1, ")")
   b = Val(Mid(s1, i + 2, Len(s1) - i - 2))
   i = InStr(s2, "J(")
   j = InStr(s2, ")")
   d = Val(Mid(s2, i + 2, Len(s2) - i - 2))
   b = b * d: c = c * d
   s3 = "J(" + Str(b)
   If a = -1 Then
      s3 = "-" + s3
   ElseIf a <> 1 Then
      s3 = Str(a) + s3
   End If
   If c <> 1 Then s3 = s3 + "/" + Str(c) Else
   s3 = Str(a) + "/" + Str(c)
End If
SimpSqr2 = s3
End Function



' ------ 小数化分数， Eps 误差 ------
' ------ 最多得7位有效数字 ------
Public Function DcmToFrc(Ta As Double, Eps As Single) As AFrc
Dim F1 As AFrc, a As Double, b As Double
Dim u As Single, v As Single
Dim i As Integer, j As Integer, k As Integer
Dim s1 As String
a = Abs(Ta)
If Abs(Ta - Int(Ta)) <= Eps Then
   F1.FenZ = Abs(Ta)
   F1.FenM = 1
ElseIf Eps = 0 Then
   s1 = Trim(Str(a))
   i = InStr(s1, ".")
   j = Len(Mid(s1, i + 1))
   u = a * 10 ^ j
   v = 10 ^ j
   j = HCF(u, v)
   u = u / j
   v = v / j
   F1.FenZ = u
   F1.FenM = v
Else
   k = Int(a)
   a = a - k
   u = 1: v = 1
   b = u / v + a
   Do While Abs(b - a) > Eps
      If b < a Then
         u = u + 1
      Else
         v = v + 1
      End If
      b = u / v
   Loop
   F1.FenZ = k * v + u
   F1.FenM = v
End If
F1.Sgn = Sgn(Ta)
F1.Val = F1.Sgn * F1.FenZ / F1.FenM
F1.St = Str(F1.Sgn * F1.FenZ)
If F1.FenM <> 1 Then F1.St = F1.St + "/" + Str(F1.FenM)
DcmToFrc = F1
End Function


 ' ------ 分数加法 ---------------
 ' ------- Ts 是 ± 号
Public Function FPlusF(Tf1 As AFrc, Tf2 As AFrc, Ts As String) As AFrc
Dim a1 As Integer, b1 As Integer, a2 As Integer, b2 As Integer
Dim u As Single, v As Single, n As Integer, F As AFrc
If Tf1.Sgn = 0 Then Tf1.Sgn = 1
If Tf2.Sgn = 0 Then Tf2.Sgn = 1
a1 = Tf1.Sgn * Tf1.FenZ                                            ' 将符号加到分子上
b1 = Tf1.FenM
a2 = Tf2.Sgn * Tf2.FenZ
b2 = Tf2.FenM
If Ts = "+" Then
   u = a1 * b2 + a2 * b1                                                   ' 通分加减後的分子计算
Else
   u = a1 * b2 - a2 * b1                                                   ' 通分加减後的分子计算
End If
F.Sgn = Sgn(u)                                                                ' 提取和(差)的符号
u = Abs(u)
v = b1 * b2                                                                    ' 通分的分母
n = HCF(u, v)
u = u / n                                                                           ' 约分
v = v / n
F.FenZ = u
F.FenM = v
F.Val = F.Sgn * (F.FenZ / F.FenM)
If F.FenZ = 0 Then
    F.St = "0"
ElseIf F.FenM = 1 Then
    F.St = AllTrim(Str(F.Sgn * F.FenZ))
Else
    F.St = AllTrim(Str(F.Sgn * F.FenZ) + "/" + Str(F.FenM))
End If
FPlusF = F
End Function


 ' ------ 分数乘法 ------
 ' ----- 分数 x 分数 -------
Public Function FxF(Tf1 As AFrc, Tf2 As AFrc) As AFrc
Dim u As Single, v As Single, n As Integer, F As AFrc
If Tf1.Sgn = 0 Then Tf1.Sgn = 1
If Tf2.Sgn = 0 Then Tf2.Sgn = 1
F.Sgn = Tf1.Sgn * Tf2.Sgn
u = Tf1.FenZ * Tf2.FenZ
v = Tf1.FenM * Tf2.FenM
n = HCF(u, v)
u = u / n
v = v / n
F.FenZ = u
F.FenM = v
F.Val = F.Sgn * (F.FenZ / F.FenM)
F.St = AllTrim(Str(F.Sgn * F.FenZ) + "/ " + Str(F.FenM))
FxF = F
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



' ------ 显示指数 ---------
Public Sub DisplayExpn(TR As Integer, Tc As Integer, Ts1 As String)
Dim i As Integer, k As Integer, u As Integer
Dim Pos() As Integer, L() As Integer, BL As Boolean
Dim s1 As String
If Ts1 = "" Then Exit Sub
ReDim Pos(0)
Pos(0) = 0
s1 = Ts1
i = 1
k = 0
Do While i < Len(s1)
   i = InStr(i, s1, "^")
   If i = 0 Then
      Exit Do
   Else
      k = k + 1
      ReDim Preserve Pos(k)
      ReDim Preserve L(k)
      Pos(0) = k
      Pos(k) = i
      BL = True
      u = 0
      Do While BL
         If IsNumeric(Mid(s1, i + 1 + u, 1)) Then
             u = u + 1
         Else
           BL = False
         End If
      Loop
      L(k) = u
      s1 = Left(s1, i - 1) + Mid(s1, i + 1)
   End If
   i = i + 1
Loop
Cells(TR, Tc) = s1
If Pos(0) > 0 Then
   For i = 1 To Pos(0)
      Cells(TR, Tc).Characters(Pos(i), L(i)).Font.Superscript = True
   Next
End If
End Sub

'在 Cells(Tr,Tc) 处显示根式, 约定：根指数都是2次。
'例：将表达式-3J(x+2)+2J(x-2)显示在Range("C7") 上：
' DisplayRoot(7,3,"-3J(x+2)+2J(x-2)"), 得到 -3√(x+2)+2√(x-2) 的显示形式。
Public Sub DisplayRoot(TR As Integer, Tc As Integer, Ts As String)
Dim s1 As String, s2 As String, s3 As String, Gh As String
Dim i As Integer, j As Integer, k As Integer, p As Integer, q As Integer, m As Integer, Start As Integer
Dim L(5) As Integer, Pos(5) As Integer, BL As Boolean
On Error Resume Next
s1 = AllTrim(Ts)
Gh = Range("C16")
s1 = Replace(s1, "j", "J")
s1 = Replace(s1, "J", Gh)
m = 0: k = 0: BL = False
For i = 1 To Len(s1)
   s2 = Mid(s1, i, 1)
   If s2 = "(" Then
      m = m + 1
      If m = 1 Then p = i
      BL = True
   ElseIf s2 = ")" Then
      m = m - 1
   End If
   If m = -1 Then
      Exit For
   ElseIf m = 0 And BL Then
      s3 = Mid(s1, p + 1, i - p - 1)
      k = k + 1
      Pos(k) = p
      L(k) = Len(s3)
      s1 = Left(s1, p - 1) + s3 + Mid(s1, i + 1)
      BL = False
      m = 0
   End If
Next
DisplayExpn TR, Tc, s1
Cells(TR, Tc).Select
With Selection.Phonetics.Font
    .Size = 12
    .Name = "SimSun-ExtB "         '"Microsoft YaHei UI Light" , "Microsoft YaHei UI ",  "SimSun-ExtB"
End With
For i = 1 To k
   Cells(TR, Tc).Characters(Pos(i), L(i)).PhoneticCharacters = String(L(i), Range("C17"))
Next
Cells(TR, Tc).Phonetic.Visible = True
End Sub



' -------------- 显示根式： J((x+1)^2)   --------------

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

' ----- 从位置 Start 开始，搜索 Ss 中，含Sa 中元素的位置 ----
' ------ 与 Instr不同，此处的Sa可含多个单字母元素，例如：“+,-,*,/," 运算符。
' ------ 得到的是一个千位数 k，包含2个最多3位数，一般地够用了
' ------ i = Int(k/1000) 得到第1个数，表示在 Ss中第 i 位置找到，
' ------ j = k - i*1000 得到第2个数，表示找到的是 Sa 中第 j 个元素
Public Function Instr2(Start As Single, Ss As String, Sa As String) As Single
Dim i As Single, j As Single, St As String
If Right(Sa, 1) <> "," Then Sa = Sa + ","
i = Start
Do While i < Len(Ss) + 1
   St = Mid(Ss, i, 1) + ","
   j = InStr(Sa, St)
   If j > 0 Then Exit Do
   i = i + 1
Loop
If i > Len(Ss) Then i = 0
Instr2 = i * 1000 + (j + 1) / 2
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


