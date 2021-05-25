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
' ------------ 检测鼠标着点 -------------------------
Private Sub Worksheet_SelectionChange(ByVal Target As Range)
Dim DTm As Single, s1 As String
On Error Resume Next
TZD = "A2"
Select Case Target.Address
Case "$A$1"
   Range(TZD).Select
   ActiveWorkbook.Save
   ActiveWorkbook.Close
Case "$D$5"                                               '设置题型格式
   Fmt_Tx 1
Case "$E$5"
   Fmt_Tx 2
Case "$F$5"
   Fmt_Tx 3
Case "$G$5"
   Fmt_Tx 4
Case "$Q$6"
   Reset
Case "$O$7"                                                ' 【下一题】出题
   TiXing = Range("K5")
   TiHao = Range("M5")
    If Over Or TiXing = 0 Or StdTime(TiXing) = 0 Then
      s1 = Range("C17")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
    ElseIf Not SwJie Then
      s1 = Range("C18")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
    ElseIf TiHao < 10 Then                                     ' 未满10题，
      Range("F10:G12") = ""
      Range("K10:L12") = ""
      Range("G114:L116") = ""
      TiXing = Range("K5")
      TiHao = TiHao + 1
      Range("M5") = TiHao
      ' -----  出题  ------
      Select Case TiXing
      Case 1                                                       ' 可化为一次方程
         s1 = CreatAExp(9, 1)
         FmtOut s1, 1
      Case 2                                                        '可化为二次方程
         s1 = CreatAExp(5, 2)
         FmtOut s1, 2
      Case 3                                                        ' 整数+指数题型
         s1 = CreatAExp(5, 3)                               '最大7，整数指数, 3项
         FmtOut s1, 3
      Case 4                                                          ' 分数+指数题型
         s1 = CreatAExp(5, 4)                                ' 最大7，整数指数, 3项
         FmtOut s1, 4
      End Select
      t1 = Timer                                                   ' 记下起始时间
      SwJie = False                                               ' 允许作答(未解答)
      Over = TiHao = 10
    End If
Case "$O$9"                                                      ' 【确定】
   If SwJie Or TiXing = 0 Or StdTime(TiXing) = 0 Then                            ' 只能作答一次
      Range(TZD).Select
      Exit Sub
   End If
   DTm = Timer - t1
   ToAns TiXing
   CheckAns TiXing, Epslon, DTm
   SwJie = True
   If TiHao = 10 Then ToReport
Case "$C$3:$D$3", "$G$3:$H$3"
   Exit Sub
Case "$K$10", "$K$11", "$K$12", "$K$10:$L$10", "$K$11:$L$11"                          ' 答题
   If SwJie = False Then Exit Sub
Case "$L$12"
   If Range("L12") = "" Then
      Range("L12") = Range("C20")
   Else
      Range("L12") = ""
   End If
End Select
Range(TZD).Select
End Sub


' ----------------   重置  ------------------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Reset()
   Range("C7:G8") = ""
   Range("I7:L8") = ""
   Range("F10:G12") = ""
   Range("K10:L12") = ""
   Range("G114:L116") = ""
   Range("C7:G8").Merge
   Range("I7:L8").Merge
   Range("C7:G8").Characters.Font.Size = 16
   Range("I7:L8").Characters.Font.Size = 16
   Range("C7").HorizontalAlignment = xlRight
   Range("I7").HorizontalAlignment = xlLeft
   Range("O13:Q22") = ""
   Range("O23") = 0
   Range("Q3") = 0
   Range("Q8") = 0
   Range("Q10") = 0
   Range("K3") = Date
   Range("O3") = Time
   Range("P23") = "=Sum(P13:P22)"
   Range("Q23") = "=Sum(Q13:Q22)"
   TiXing = Range("K5")
   If TiXing < 1 Then TiXing = 1
   Range("K5") = TiXing
   TiHao = 0
   Range("M5") = TiHao
   TZD = "A2"
   Over = False
   SwJie = True
   StdTime(1) = 60
   StdTime(2) = 60
   StdTime(3) = 60
   StdTime(4) = 60
   Epslon = 0.01
   Shapes.Range(2).Visible = False
End Sub

' -------- 设定各种题型的显示格式 和基准时间 ---------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Fmt_Tx(Tx As Integer)
Dim Ad As String, i As Integer
Range(TZD).Select
Reset
TiXing = Tx
Range("K5") = TiXing
Range("D5").Interior.ColorIndex = 33
Range("E5").Interior.ColorIndex = 33
Range("F5").Interior.ColorIndex = 33
Range("G5").Interior.ColorIndex = 33
Select Case Tx
Case 1
   Range("I9") = Range("C22")
   Range("E10") = "a ="
   Range("E11") = "b ="
   Range("E12") = "c ="
   Range("J10") = "a ="
   Range("J11") = "b ="
   Range("J12") = "c ="
   Range("D5").Interior.ColorIndex = 20
Case 2
   Range("I9") = Range("F22")
   Range("E10") = "x1 ="
   Range("E11") = "x2 ="
   Range("E12") = ""
   Range("J10") = "x1 ="
   Range("J11") = "x2 ="
   Range("J12") = ""
   Range("E5").Interior.ColorIndex = 20
Case 3, 4
   If Tx = 3 Then
      Range("F5").Interior.ColorIndex = 20
   Else
      Range("G5").Interior.ColorIndex = 20
   End If
   Range("I9") = Range("I23")
   Range("E10") = "x1 ="
   Range("E11") = "x2 ="
   Range("E12") = "k ="
   Range("J10") = Range("C23")
   Range("J11") = "x2 ="
   Range("J12") = "k ="
End Select
End Sub

' ----- 将题目按常用格式佈放 -------------
' ------ 不同课题会有不同的佈放格式 -------
Private Sub FmtOut(Tst As String, Tx As Integer)
Dim s1 As String, s2 As String, s3 As String, s4 As String, Ad As String
Dim a As Single, b As Single, c As Single
Dim i As Integer, j As Integer, k As Integer
Dim TF As AFrc, Sn(4) As String
Select Case Tx
Case 1                  '题型1
   s1 = ExpA.Note + "(" + ExpA.St + ")(" + ExpB.St + ")"
   s2 = ExpC.Note + "(" + ExpC.St + ")"
   Range("C7") = s1
   Range("I7") = s2
Case 2, 3, 4                '题型2
   DisplayExpn 7, 3, Tst
   Range("I7") = 0
End Select
End Sub

' ------------ 给出正确答案  ------------------------
Private Sub ToAns(Tx)
Dim a As Single, f As AFrc
Select Case Tx
Case 1, 3, 4
   Range("F10") = Range("K114")
   Range("F11") = Range("K115")
   Range("F12") = Range("K116")
Case 2
   If Range("K114") = "@" Then
      Range("G12") = Range("C20")
   Else
      DisplayRoot 10, 6, Range("K114")
      DisplayRoot 11, 6, Range("K115")
   End If
End Select
End Sub
' -------------------  检测对/错 ，计算得分 --------------------
' -----------  Tx: 题型，Eps 允许误差，Dt 耗时 --------
' ----- 此处仅为例， 不同课题，有不同的答案形式 ------------
Private Function CheckAns(Tx As Integer, Eps As Single, Dt As Single) As Single
Dim s1  As String, s2 As String, s3  As String, s4 As String, Mark As Single
Dim i As Integer, j As Integer, k As Single, t As Single, m As Single
Dim a As Single, b As Single, c As Single, d As Single
On Error Resume Next
If Eps = 0 Then Eps = 0.0001
If TiHao = 0 Then Exit Function
Select Case Tx
Case 1
   m = 0
   s1 = Trim(Range("F10"))
   s2 = Trim(Range("F11"))
   s3 = Trim(Range("F12"))
   If Trim(Range("K10")) = s1 Then m = 1 / 3
   If Trim(Range("K11")) = s2 Then m = m + 1 / 3
   If Trim(Range("K12")) = s3 Then m = m + 1 / 3
Case 2
   s1 = Range("K10")
   s2 = Range("K11")
   DisplayRoot 10, 11, s1
   DisplayRoot 11, 11, s2
   If Range("K114") <> "@" Then
      s1 = Replace(s1, "J", "sqrt")
      s2 = Replace(s2, "J", "sqrt")
      Range("F19") = "=" + s1
      Range("F20") = "=" + s2
      If Range("E19") = Range("F19") Or Range("E19") = Range("F20") Then m = 0.5
      If Range("E20") = Range("F19") Or Range("E20") = Range("F20") Then m = m + 0.5
   Else
      m = 1
      If Range("L12") = "" Then m = 0
   End If
Case 3, 4
   s1 = Range("K11")
   s2 = Trim(Range("K12"))
   Range("F20") = "=" + s1
   If Range("E20") = Range("F20") Then m = 0.5
   If Trim(Range("F12")) = s2 Then m = m + 0.5
End Select
If m = 1 Then
   Cells(12 + TiHao, 15) = Range("D16")
   Range("O23") = Range("O23") + 1
ElseIf m > 0 Then
   Cells(12 + TiHao, 15) = Range("D16") + Range("E16")
   Range("O23") = Range("O23") + 1
Else
   Cells(12 + TiHao, 15) = Range("E16")
End If

k = 1
t = 1 + (StdTime(Tx) - Dt) / StdTime(Tx)                 '以耗时与标准时间的相对比率，计算折扣
If t < 0.1 Then t = 0.1
If t > 2 Then t = 2
k = k * t
Mark = 10 * m * k
Cells(12 + TiHao, 16) = Dt
Cells(12 + TiHao, 17) = Mark
Range("Q8") = Range("P23")
Range("Q10") = Range("Q23")
a = Range("Q10")
If a > 90 Then
   c = 4
ElseIf a > 70 Then
   c = 3
ElseIf a > 50 Then
   c = 2
Else
   c = 1
End If
Range("Q3") = c
CheckAns = Mark
End Function

' ---------- 填寫報表 -------
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

