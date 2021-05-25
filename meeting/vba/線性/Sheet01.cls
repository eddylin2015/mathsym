VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Sheet01"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Option Explicit
Dim TL(5)             As ALine
Dim TPs                As ApSet
Dim TiHao             As Integer                ' 題號
Dim TiXing             As Integer                ' 題型
Dim Epslon              As Single                ' 允許誤差
Dim T1                    As Single                 ' 起計時簡
Dim StdTime(3)       As Single                  ' 標準時簡
Dim Over                As Boolean              ' 10題完成
Dim SwJie               As Boolean              ' 是否已經解答
Dim TZD                  As String                  ' 停駐點


Private Sub Worksheet_Activate()
Range("C3") = ""
Range("G3") = ""
Range("K3") = ""
Range("O3") = ""
Range("Q3") = ""
Reset
End Sub

' ------------ 檢測鼠標著點 -------------------------
Private Sub Worksheet_SelectionChange(ByVal Target As Range)
Dim DTm As Single, s1 As String, s2 As String
On Error Resume Next
TZD = "A2"
Select Case Target.Address
Case "$A$1"
   Range(TZD).Select
   ActiveWorkbook.Save
   ActiveWorkbook.Close
Case "$E$5"                                               '設置題系的型格式
   Fmt_Tx 1
Case "$F$5"
   Fmt_Tx 2
Case "$G$5"
   Fmt_Tx 3
Case "$Q$6"                                              '重置
   Range(TZD).Select
   Reset
Case "$O$7"                                              ' 下一題
   Range(TZD).Select
   TiXing = Range("K5")
   TiHao = Range("M5")
    If Over Or TiXing = 0 Or StdTime(TiXing) = 0 Then
      s1 = Range("A48")
      Shapes.Range(2).TextFrame.Characters.Text = s1
      Shapes.Range(2).Visible = True
    ElseIf Not SwJie Then
      s1 = Range("A49")
      Shapes.Range(2).TextFrame.Characters.Text = s1
      Shapes.Range(2).Visible = True
    ElseIf TiHao < 10 Then
      Range("D7:F13") = ""
      Range("D16:D17") = "":  Range("D20:D21") = ""
      Range("H7:L12") = ""
      Range("H20:L21") = ""
      TiXing = Range("K5")
      TiHao = TiHao + 1
      Range("M5") = TiHao
      MingTi TiXing + 2
      T1 = Timer
      SwJie = False
    Else
      Over = True
       ToReport
    End If
Case "$O$9"                                                      ' 提交
   Range(TZD).Select
   If SwJie Or TiXing = 0 Then                            ' 硐夔釬湘珨棒
       Range(TZD).Select
       Exit Sub
   End If
   DTm = Timer - T1
   ToAns
   CheckAns TiXing, Epslon, DTm
   SwJie = True
   If TiHao = 10 Then ToReport
Case "$U$2"
    Range("V3:AD25") = ""
Case "$C$3:$D$3", "$G$3:$H$3"
   Exit Sub
Case "$D$16", "$D$17", "$D$20", "$D$21"              ' 學生輸入答案
   If SwJie = False Then Exit Sub
   Range(TZD).Select
Case Else
      Range(TZD).Select
End Select
End Sub

' ----------------   重置 -------------------
Private Sub Reset()
Dim i As Integer, j As Integer
Application.DisplayAlerts = False
Range("D7:F13") = ""
Range("D16:D17") = "": Range("D20:D21") = ""
Range("H20:L21") = ""
Range("B51:F71") = ""
Range("H7:L12") = ""
Range("O13:Q22") = ""
Range("Q3") = 0
Range("Q8") = 0
Range("Q10") = 0
Range("O23") = 0
Range("K3") = Date
Range("O3") = Time
Range("P23") = "=Sum(P13:P22)"
Range("Q23") = "=Sum(Q13:Q22)"
TiHao = 0
Range("M5") = TiHao
TiXing = Range("K5")
StdTime(1) = 60
StdTime(2) = 120
StdTime(3) = 180
Epslon = 0.001
TZD = "A2"
Over = False
SwJie = True
Shapes.Range(1).Visible = True
Shapes.Range(2).Visible = False
End Sub


' ---------- 命題 --------------
Private Sub MingTi(n As Integer)
Dim s1 As String, s2 As String, i As Integer
Dim Max As Single, Min As Single, a As Single
Dim j As Integer, k As Integer
Randomize
GetALset n
TL(0).a = GetARnd(-9, 9, 0, 1, -1, 1)
TL(0).b = GetARnd(-9, 9, 0, 1, -1, 1)
s1 = Str(TL(0).a) + "x":   s2 = Trim(Str(TL(0).b)) + "y"
If TL(0).b > 0 Then s2 = "+" + s2
s1 = s1 + s2
TL(0).St = s1
Range("D13") = s1
j = 1: k = 1
Min = 99999: Max = -99999
For i = 1 To n
   a = Val_PinExp(TPs.Pnt(i), s1)
   Cells(6 + i, 8) = TPs.Pnt(i).x
   Cells(6 + i, 9) = TPs.Pnt(i).y
   Cells(6 + i, 10) = a
   If a > Max Then
      Max = a
      j = i
      Range("L10") = Max              '最大值
   End If
   If a < Min Then
      Min = a
      k = i
      Range("L11") = Min                '最小值
   End If
Next
Range("L7") = j               ' 最大/小點的點號
Range("L8") = k
End Sub


' -------- 題型選擇 ---------------
Private Sub Fmt_Tx(Tx As Integer)
Dim i As Integer, j As Integer, m As Integer, n As Integer
Reset
If Tx = 0 Then Tx = Range("K5")
TiXing = Tx
Range("K5") = TiXing
Range("E5:G5").Interior.ColorIndex = 33
Select Case Tx
Case 1
      Range("E5").Interior.ColorIndex = 20
Case 2
      Range("F5").Interior.ColorIndex = 20
Case 3
      Range("G5").Interior.ColorIndex = 20
End Select
End Sub



' ------ 建立隨機的線性不等式方程組  3 <=  n <=5 -----
' ------ 不是任意的隨機， 而是可圍成一個封閉的凸多邊形的邊 ------
Private Sub GetALset(n As Integer)
Dim i As Integer, j As Integer, u As Single
Dim P1 As APnt, P2 As APnt
Dim s1 As String
Range("B51:F71") = ""
TPs = GetAPset(n)                                      ' 得到隨机的凸n邊形的頂點
For i = 1 To n
   j = i + 1
   If i = n Then j = 1
   TL(i) = MakeAL(TPs.Pnt(i), TPs.Pnt(j))   '相鄰的兩點連為直線
   For j = -10 To 10
      s1 = Replace(TL(i).St1, "x", Str(j))
      Range("H50") = "=" + s1
      Cells(61 + j, 1 + i) = Range("H50")
   Next
Next
For i = 1 To n
   j = Int((100 * Rnd)) Mod 2
   If j = 0 Then
      Cells(6 + i, 4) = TL(i).St
      Cells(6 + i, 6) = Str(TL(i).c)
   Else
      s1 = Trim(Str(-TL(i).c))
      If Left(s1, 1) <> "-" Then s1 = "+" + s1
      Cells(6 + i, 4) = TL(i).St + s1
      Cells(6 + i, 6) = "0"
   End If
   u = Val_PinExp(TPs.Cp, TL(i).St)              ' 為使凸多邊形內部成為可行域，
   If u >= TL(i).c Then                                    '以凸多邊形的几何中心進行測試，
      TL(i).Op = Range("J15")                         ' >= 符號
   Else
      TL(i).Op = Range("K15")                         '<=符號
   End If
   Cells(6 + i, 5) = TL(i).Op
Next
End Sub


' ------  選取凸多邊形點集 ------
Private Function GetAPset(n As Integer) As ApSet
Dim i As Integer, Tp(5) As APnt, Cp As APnt
Dim x As Single, y As Single
Select Case n
Case 3
   Tp(1).x = GetARnd(0, 8, 0, 1, 0, 0)
   Tp(1).y = GetARnd(0, 8, 0, 1, 0, 0)
   Tp(2).x = GetARnd(-8, 0, 0, 1, 0, 0)
   Tp(2).y = GetARnd(0, 8, 0, 1, 0, 0)
   Tp(3).x = GetARnd(-8, 8, 0, 1, 0, 0)
   Tp(3).y = GetARnd(-8, 0, 0, 1, 0, 0)
Case 4
   Tp(1).x = GetARnd(4, 8, 0, 0, 0, 0)
   Tp(1).y = GetARnd(-2, 2, 0, 0, 0, 0)
   Tp(2).x = GetARnd(-2, 2, 0, 0, 0, 0)
   Tp(2).y = GetARnd(4, 8, 0, 0, 0, 0)
   Tp(3).x = GetARnd(-8, -4, 0, 0, 0, 0)
   Tp(3).y = GetARnd(-2, 2, 0, 0, 0, 0)
   Tp(4).x = GetARnd(-2, 2, 0, 0, 0, 0)
   Tp(4).y = GetARnd(-8, -4, 0, 0, 0, 0)
Case 5
   Tp(1).x = GetARnd(4, 7, 0, 0, 0, 0)
   Tp(1).y = GetARnd(-1, 2, 0, 0, 0, 0)
   Tp(2).x = GetARnd(0, 3, 0, 0, 0, 0)
   Tp(2).y = GetARnd(4, 7, 0, 0, 0, 0)
   Tp(3).x = GetARnd(-7, -4, 0, 0, 0, 0)
   Tp(3).y = GetARnd(1, 4, 0, 0, 0, 0)
   Tp(4).x = GetARnd(-6, -3, 0, 0, 0, 0)
   Tp(4).y = GetARnd(-5, -2, 0, 0, 0, 0)
   Tp(5).x = GetARnd(0, 3, 0, 0, 0, 0)
   Tp(5).y = GetARnd(-7, -4, 0, 0, 0, 0)
End Select
GetAPset.n = n
ReDim GetAPset.Pnt(n)
x = 0: y = 0
For i = 1 To n
   GetAPset.Pnt(i) = Tp(i)
    x = x + Tp(i).x
    y = y + Tp(i).y
Next
GetAPset.Cp.x = x / n                         ' 几何中心
GetAPset.Cp.y = y / n
End Function


' ----- 由 2 點建立直線方程 --------
' ----- ax + by = c --------
Private Function MakeAL(Tp1 As APnt, Tp2 As APnt) As ALine
Dim a As Single, Sw As Integer, k As Integer
Dim Tx As ALine, s1 As String, s2 As String
Dim Op(1) As String
Op(0) = Range("J15"): Op(1) = Range("K15")
Tx.a = Tp2.y - Tp1.y
Tx.b = Tp1.x - Tp2.x
Tx.c = Tx.a * Tp1.x + Tx.b * Tp1.y
Tx.c = Int(Tx.c + 0.5)
k = HCF(CLng(Tx.a), CLng(Tx.b)): k = HCF(CLng(k), CLng(Tx.c))
Tx.a = Tx.a / k: Tx.b = Tx.b / k: Tx.c = Tx.c / k
If Tx.a < 0 Then Tx.a = -Tx.a: Tx.b = -Tx.b: Tx.c = -Tx.c
s1 = ""
If Tx.a = -1 Then s1 = "-x "
If Tx.a = 1 Then s1 = "x "
If Abs(Tx.a) > 1 Then s1 = Str(Tx.a) + "x "
s2 = ""
If Tx.b = -1 Then s2 = "-y "
If Tx.b = 1 Then s2 = "y "
If Abs(Tx.b) > 1 Then s2 = Str(Tx.b) + "y "
If Tx.b > 0 And Tx.a <> 0 Then s2 = "+" + s2
If Abs(Tx.b) > 0.01 Then
   Tx.St = s1 + s2
Else
   Tx.St = s1
   Tx.b = 0.01
End If
Tx.St1 = "(" + Str(Tx.c) + "-" + Str(Tx.a) + "*x)/" + Str(Tx.b)
MakeAL = Tx
End Function


' -----  計算一點Tp在表達式的值 -----
' ----- Exp = " ax + by" 的形式 -----
Private Function Val_PinExp(Tp As APnt, Exp As String) As Single
Dim St As String, a As Single
Dim i As Integer
St = LCase(Exp)
i = InStr(St, "x")
If i > 1 Then
   If IsNumeric(Mid(St, i - 1, 1)) Then St = Left(St, i - 1) + "*" + Mid(St, i)
End If
i = InStr(St, "y")
If i > 1 Then
   If IsNumeric(Mid(St, i - 1, 1)) Then St = Left(St, i - 1) + "*" + Mid(St, i)
End If
St = Replace(St, "x", Str(Tp.x))
St = Replace(St, "y", Str(Tp.y))
Range("J13") = "=" + St
a = Range("J13")
Val_PinExp = a
End Function


' ------ 給出參考答案-------
Private Sub ToAns()
Dim i As Integer, j As Integer
Dim s1 As String, x As Integer, y As Integer
i = Range("L7")
j = Range("L8")
Range("H20") = Range("L10")
s1 = "(" + Str(TPs.Pnt(i).x) + ", " + Str(TPs.Pnt(i).y) + ")"
Range("K20") = s1
Range("H21") = Range("L11")
s1 = "(" + Str(TPs.Pnt(j).x) + ", " + Str(TPs.Pnt(j).y) + ")"
Range("K21") = s1
End Sub


' -------------------  檢查答案--------------------

Private Sub CheckAns(Tx As Integer, Eps As Single, Dt As Single)
Dim x As Single, y As Single, x0 As Single, y0 As Single
Dim Max As Single, Min As Single, Max0 As Single, Min0 As Single
Dim Dx As Single, Dy As Single, Dz As Single
Dim r As Single, D As Single, s1 As String
Dim i As Integer, j As Integer, k As Integer

D = 0                 ' 得分
' -----  最值 -------
Max0 = Range("L10")                                '師答
Min0 = Range("L11")
Max = Range("D16")                                  '生答
Min = Range("D17")
If Max = Max0 Then D = 3
If Min = Min0 Then D = D + 3
' ----- 最點 -----
i = Range("L7")
x0 = TPs.Pnt(i).x: y0 = TPs.Pnt(i).y
s1 = AllTrim(Range("D20"))
If s1 <> "" Then
   s1 = Mid(s1, 2, Len(s1) - 2)
   k = InStr(s1, ",")
   x = Val(Left(s1, k - 1))
   y = Val(Mid(s1, k + 1))
   If x = x0 Then D = D + 1                            ' 最大點
   If y = y0 Then D = D + 1
End If
j = Range("L8")
x0 = TPs.Pnt(j).x: y0 = TPs.Pnt(j).y
s1 = AllTrim(Range("D21"))
If s1 <> "" Then
   s1 = Mid(s1, 2, Len(s1) - 2)
   k = InStr(s1, ",")
   x = Val(Left(s1, k - 1))
   y = Val(Mid(s1, k + 1))
   If x = x0 Then D = D + 1                            ' 最小點
   If y = y0 Then D = D + 1
End If
If D = 10 Then
   Cells(12 + TiHao, 15) = Range("J16")
   Range("O23") = Range("O23") + 1
ElseIf D > 0 Then
   Cells(12 + TiHao, 15) = Range("J16") + Range("K16")
   Range("O23") = Range("O23") + 1
Else
   Cells(12 + TiHao, 15) = Range("K16")
End If
r = 1 + (StdTime(Tx) - Dt) / StdTime(Tx)
If r < 0.2 Then r = 0.2
If r > 1.8 Then r = 1.8
D = D * r
Cells(12 + TiHao, 16) = Dt
Cells(12 + TiHao, 17) = D
Range("Q8") = Range("P23")
Range("Q10") = Range("Q23")
D = Range("Q10")
If D > 90 Then
   Range("Q3") = 4
ElseIf D > 70 Then
   Range("Q3") = 3
ElseIf D > 50 Then
   Range("Q3") = 2
Else
   Range("Q3") = 1
End If
End Sub

' ---------- 去報表 -------
Private Sub ToReport()
Dim i As Integer, s1 As String
s1 = "*"
Do While s1 <> ""
  i = i + 1
  s1 = Cells(2 + i, 23)
Loop
Cells(2 + i, 22) = Range("C3")
Cells(2 + i, 23) = Range("G3")
Cells(2 + i, 24) = Range("K3")
Cells(2 + i, 25) = Range("O3")
Cells(2 + i, 26) = Range("Q10")
Cells(2 + i, 27) = Range("Q8")
Cells(2 + i, 28) = Range("K5")
Cells(2 + i, 29) = Range("O23")
Cells(2 + i, 30) = Range("Q3")
End Sub
