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
Case "$H$5"
   Fmt_Tx 5
Case "$Q$6"
   Reset
Case "$O$7"                                                ' 【下一题】出题
    If Over Or TiXing = 0 Or StdTime(TiXing) = 0 Then
      s1 = Range("C17")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
    ElseIf Not SwJie Then
      s1 = Range("C18")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
    ElseIf TiHao < 10 Then
      Range("D7:L12") = ""
      Range("D119:L123") = ""
      TiXing = Range("K5")
      TiHao = Range("M5")
      TiHao = TiHao + 1
      Range("M5") = TiHao
      ' -----  出题  ------
      Select Case TiXing
      Case 1
         s1 = CreatAExp(9, 1)
         FmtOut s1, 1
      Case 2
         s1 = CreatAExp(9, 2)
         FmtOut s1, 2
      Case 3
         s1 = CreatAExp(5, 3)
         FmtOut s1, 3
      Case 4
         s1 = CreatAExp(5, 4)
         FmtOut s1, 4
      Case 5
         s1 = CreatAExp(5, 5)
         FmtOut s1, 5
      End Select
      T1 = Timer                                                   ' 记下起始时间
      SwJie = False                                               ' 允许作答(未解答)
      Over = TiHao = 10
    End If
Case "$O$9"                                                      ' 【确定】
   If SwJie Or TiXing = 0 Or StdTime(TiXing) = 0 Then                            ' 只能作答一次
      Range(TZD).Select
      Exit Sub
   End If
   DTm = Timer - T1
   ToAns TiXing
   CheckAns TiXing, Epslon, DTm
   SwJie = True
   If TiHao = 10 Then ToReport
Case "$C$3:$D$3", "$G$3:$H$3"
   Exit Sub
Case "$D$9:$L$10", "$D$9:$E$9", "$D$10:$E$10", "$F$9:$F$10", "$G$9", "$G$10", "$H$9:$H$10", "$I$9", "$I$10"                    ' 答题
   If SwJie = False Then Exit Sub
End Select
Range(TZD).Select
End Sub

' ----------------   重置 ------------------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Reset()
   Application.DisplayAlerts = False
   Range("D7:L12") = ""
   Range("D119:L123") = ""
   ' -----------------------------
   Range("O13:Q22") = ""
   Range("O23") = 0
   Range("Q3") = 0
   Range("Q8") = 0
   Range("Q10") = 0
   Range("K3") = Date
   Range("O3") = Time
   Range("P23") = "=Sum(P13:P22)"
   Range("Q23") = "=Sum(Q13:Q22)"
   TiHao = 0
   Range("M5") = TiHao
   TiXing = Range("K5")
   TZD = "A2"
   StdTime(1) = 30
   StdTime(2) = 60
   StdTime(3) = 60
   StdTime(4) = 60
   StdTime(5) = 60
   Epslon = 0.01
   Over = False
   SwJie = True
   Shapes.Range(2).Visible = False
   Application.DisplayAlerts = True
End Sub

' -------- 设定各种题型的显示格式 和基准时间 ---------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Fmt_Tx(Tx As Integer)
Dim Ad As String, i As Integer
Range(TZD).Select
Reset
Application.DisplayAlerts = False
Range("D5").Interior.ColorIndex = 33
Range("E5").Interior.ColorIndex = 33
Range("F5").Interior.ColorIndex = 33
Range("G5").Interior.ColorIndex = 33
Range("H5").Interior.ColorIndex = 33
Range("K5") = Tx
Range("M5") = 0
Range("D7:L8").UnMerge
Range("D9:L10").UnMerge
Range("D11:L12").UnMerge
Range("D7:L7").Borders(xlEdgeBottom).LineStyle = 0
Range("D9:L9").Borders(xlEdgeBottom).LineStyle = 0
Range("D11:L11").Borders(xlEdgeBottom).LineStyle = 0
Range("D7:L8").Font.Size = 12
Range("D9:L10").Font.Size = 12
Range("D11:L12").Font.Size = 12
Select Case Tx
Case 1, 3, 5
   If Tx = 1 Then
      Range("D5").Interior.ColorIndex = 20
   ElseIf Tx = 3 Then
      Range("F5").Interior.ColorIndex = 20
   Else
      Range("H5").Interior.ColorIndex = 20
   End If
   Range("D7:L8").Merge
   Range("D9:L10").Merge
   Range("D11:L12").Merge
   Range("D7:L8").HorizontalAlignment = xlLeft
   Range("D9:L10").HorizontalAlignment = xlLeft
   Range("D11:L12").HorizontalAlignment = xlLeft
Case 2
   Range("E5").Interior.ColorIndex = 20
   Range("D7:D8").Merge
   Range("F7:F8").Merge
   Range("H7:H8").Merge
   Range("J7:J8").Merge
   Range("L7:L8").Merge
   Range("D9:E9").Merge
   Range("D10:E10").Merge
   Range("F9:F10").Merge
   Range("D11:E11").Merge
   Range("D12:E12").Merge
   Range("F11:F12").Merge
   Range("E7").Borders(xlEdgeBottom).Weight = 2
   Range("G7").Borders(xlEdgeBottom).Weight = 2
   Range("I7").Borders(xlEdgeBottom).Weight = 2
   Range("K7").Borders(xlEdgeBottom).Weight = 2
   Range("D9:E9").Borders(xlEdgeBottom).Weight = 2
   Range("G9").Borders(xlEdgeBottom).Weight = 2
   Range("D11:E11").Borders(xlEdgeBottom).Weight = 2
   Range("G11").Borders(xlEdgeBottom).Weight = 2
   Range("D7:L8").HorizontalAlignment = xlCenter
   Range("D9:L10").HorizontalAlignment = xlCenter
   Range("D11:L12").HorizontalAlignment = xlCenter
   Range("D7").Font.Size = 20
   Range("F7").Font.Size = 20
   Range("H7").Font.Size = 20
   Range("J7").Font.Size = 20
   Range("L7").Font.Size = 20
   Range("F9").Font.Size = 20
   Range("F11").Font.Size = 20
Case 4
   Range("G5").Interior.ColorIndex = 20
   Range("D7:D8").Merge
   Range("E7:F7").Merge
   Range("E8:F8").Merge
   Range("G7:G8").Merge
   Range("I7:I8").Merge
   Range("D9:E9").Merge
   Range("D10:E10").Merge
   Range("F9:F10").Merge
   Range("H9:H10").Merge
   Range("D11:E11").Merge
   Range("D12:E12").Merge
   Range("F11:F12").Merge
   Range("H11:H12").Merge
   Range("E7:F7").Borders(xlEdgeBottom).Weight = 2
   Range("H7").Borders(xlEdgeBottom).Weight = 2
   Range("D9:E9").Borders(xlEdgeBottom).Weight = 2
   Range("G9").Borders(xlEdgeBottom).Weight = 2
   Range("I9").Borders(xlEdgeBottom).Weight = 2
   Range("D11:E11").Borders(xlEdgeBottom).Weight = 2
   Range("G11").Borders(xlEdgeBottom).Weight = 2
   Range("I11").Borders(xlEdgeBottom).Weight = 2
   Range("D7").Font.Size = 20
   Range("G7").Font.Size = 20
   Range("I7").Font.Size = 20
   Range("F9").Font.Size = 20
   Range("H9").Font.Size = 20
   Range("F11").Font.Size = 20
   Range("H11").Font.Size = 20
   Range("E7:L12").HorizontalAlignment = xlCenter
   Range("D7").HorizontalAlignment = xlRight
   Range("I7").HorizontalAlignment = xlLeft
   Range("D9:L10").HorizontalAlignment = xlCenter
   Range("D11:L12").HorizontalAlignment = xlCenter
End Select
Application.DisplayAlerts = True
End Sub

' ----- 将题目按常用格式佈放 -------------
' ------ 不同课题会有不同的佈放格式 -------
Private Sub FmtOut(Tst As String, Tx As Integer)
Dim s1 As String, a As Single, b As Single
On Error Resume Next
Select Case Tx
Case 1
   s1 = Range("D119")
   Range("D7") = s1
Case 2
   a = Range("G119")
   Range("D7") = "("
   Range("E7") = Range("D119")
   Range("E8") = Range("D120")
   If Sgn(a) = 1 Then
      Range("F7") = "+"
   Else
      Range("F7") = "-"
   End If
   Range("G7") = Abs(a)
   Range("G8") = Range("G120")
   Range("H7") = ")("
   Range("I7") = Range("D119")
   Range("I8") = Range("D120")
   If Sgn(-a) = 1 Then
      Range("J7") = "+"
   Else
      Range("J7") = "-"   '
   End If
   Range("K7") = Abs(a)
   Range("K8") = Range("G120")
   Range("L7") = ")"
Case 3, 5
   s1 = Range("D119")
   DisplayExpn 7, 4, s1
Case 4
   Range("D7") = "("
   Range("E7") = Range("D119")
   Range("E8") = Range("D120")
   a = Range("G119")
   If Sgn(a) = 1 Then
      Range("G7") = "+"
   Else
      Range("G7") = "-"
   End If
   Range("H7") = Abs(a)
   Range("H8") = Range("G120")
   s1 = ")^2"
   DisplayExpn 7, 9, s1
End Select
End Sub

' ------------ 给出正确答案  ------------------------
Private Sub ToAns(Tx)
Dim s1 As String, s2 As String, s3 As String, s4 As String
Dim a As Single, b As Single, i As Integer
On Error Resume Next
Select Case Tx
Case 1, 3, 5
   s1 = LCase(Range("D9"))
   Range("D122") = s1
   DisplayExpn 9, 4, s1
   s1 = Range("D121")
   DisplayExpn 11, 4, s1
Case 2
   Range("I121") = Range("D9")
   Range("I122") = Range("D10")
   Range("K121") = Range("G9")
   Range("K122") = Range("G10")
   DisplayExpn 9, 4, Range("I121")
   DisplayExpn 11, 4, Range("D121")
   Range("D12") = Range("D122")
   Range("F11") = "-"
   Range("G11") = Range("G121")
   Range("G12") = Range("G122")
Case 4
   Range("I121") = Range("D9")
   Range("I122") = Range("D10")
   Range("K121") = Range("G9")
   Range("K122") = Range("G10")
   Range("L121") = Range("I9")
   Range("L122") = Range("I10")
   DisplayExpn 9, 4, Range("D9")
   DisplayExpn 11, 4, Range("D121")
   Range("D12") = Range("D122")
   s1 = Range("F121")
   If Left(s1, 1) = "-" Then
      Range("F11") = "-"
      s1 = Mid(s1, 2)
   Else
      Range("F11") = "+"
   End If
   Range("G11") = s1
   Range("G12") = Range("F122")
   Range("H11") = "+"
   Range("I11") = Range("G121")
   Range("I12") = Range("G122")
End Select
End Sub


' -------------------  检测对/错 ，计算得分 --------------------
' -----------  Tx: 题型，Eps 允许误差，Dt 耗时 --------
' ----- 此处仅为例， 不同课题，有不同的答案形式 ------------
Private Function CheckAns(Tx As Integer, Eps As Single, Dt As Single) As Single
Dim s1  As String, s2 As String, s3  As String, s4 As String, Mark As Single
Dim i As Integer, k As Single, t As Single, m As Single
Dim a As Single, b As Single, c As Single
Dim BL As Boolean
On Error Resume Next
If Tx = 0 Or TiHao = 0 Or StdTime(Tx) = 0 Then Exit Function
m = CheckExps(Tx, Eps)
Range("K123") = m
t = 1 + (StdTime(Tx) - Dt) / StdTime(Tx)                 '以耗时与标准时间的相对比率，计算折扣
If t < 0.1 Then t = 0.1
If t > 1.9 Then t = 1.9
Mark = 10 * m * t
eeee:
If m = 0 Then
    Cells(12 + TiHao, 15) = Range("E16")
ElseIf m = 1 Then
   Cells(12 + TiHao, 15) = Range("D16")
   Range("O23") = Range("O23") + 1
Else
   Cells(12 + TiHao, 15) = Range("D16") + Range("E16")
   Range("O23") = Range("O23") + 1
End If
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

