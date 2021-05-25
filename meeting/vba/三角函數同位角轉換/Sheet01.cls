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
      s1 = Range("E20")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
   ElseIf Not SwJie Then
      s1 = Range("E21")
      Sheet01.Shapes.Range(2).TextFrame.Characters.Text = s1
      Sheet01.Shapes.Range(2).Visible = True
   ElseIf TiHao < 10 Then                                     ' 未满10题，
      Range("K7:M8") = ""
      Range("K10:M11") = ""
      Range("K13:M14") = ""
      Range("J10:J11") = ""
      Range("J13:J14") = ""
      Range("E116:L119") = ""
      TiXing = Range("K5")
      TiHao = TiHao + 1
      Range("M5") = TiHao
      ' -----  出题  ------
      Select Case TiXing
      Case 1
         CreatAExp 1
         FmtOut 1
      Case 2
         CreatAExp 2
         FmtOut 2
      Case 3                                                        ' 整数+指数题型
         CreatAExp 3                               '最大7，整数指数, 3项
         FmtOut 3
      Case 4                                                          ' 分数+指数题型
         CreatAExp 4                                ' 最大7，整数指数, 3项
        FmtOut 4
      End Select
      T1 = Timer                                                   ' 记下起始时间
      SwJie = False                                               ' 允许作答(未解答)
    Else
      Over = True
    End If
Case "$O$9"                                                      ' 【确定】
   If SwJie Or TiXing = 0 Or StdTime(TiXing) = 0 Then                            ' 只能作答一次
      Range(TZD).Select
      Exit Sub
   End If
   DTm = Timer - T1
   TiXing = Range("K5")
   ToAns TiXing
   CheckAns TiXing, Epslon, DTm
   SwJie = True
   If TiHao = 10 Then ToReport
Case "$C$3:$D$3", "$G$3:$H$3"
      Exit Sub
Case "$K$10:$L$10", "$K$11:$L$11"                                       ' 答题
      If SwJie = False Then Exit Sub
End Select
Range(TZD).Select
End Sub

' ----------------   重置 ------------------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Reset()
   Range("K7:M8") = ""
   Range("K10:M11") = ""
   Range("K13:M14") = ""
   Range("J10:J11") = ""
   Range("J13:J14") = ""
   Range("E116:L119") = ""
' -----------------------------
   Range("O14:Q23") = ""
   Range("O24") = 0
   Range("Q3") = 0
   Range("Q8") = 0
   Range("Q10") = 0
   Range("K3") = Date
   Range("O3") = Time
   Range("P24") = "=Sum(P14:P23)"
   Range("Q24") = "=Sum(Q14:Q23)"
   TiHao = 0
   Range("M5") = TiHao
   TiXing = Range("K5")
   TZD = "A26"
   StdTime(1) = 60
   StdTime(2) = 120
   StdTime(3) = 180
   StdTime(4) = 210
   Epslon = 0.001
   Over = False
   SwJie = True
   Sheet01.Shapes.Range(2).Visible = False
End Sub

' -------- 设定各种题型的显示格式 和基准时间 ---------------
' ------ 此处仅为例(有理式运算) , 不同课题会有不同的显示格式 -------
Private Sub Fmt_Tx(Tx As Integer)
Dim Ad As String, i As Integer
Reset
Application.DisplayAlerts = False
Range("D5:G5").Interior.ColorIndex = 33
TiXing = Tx
Range("K5") = TiXing
Select Case Tx
Case 1
   Range("D5").Interior.ColorIndex = 20
Case 2
   Range("E5").Interior.ColorIndex = 20
Case 3
   Range("F5").Interior.ColorIndex = 20
Case 4
   Range("G5").Interior.ColorIndex = 20
End Select
Range(TZD).Select
End Sub

' ----- 命题： 将题目按常用格式佈放 -------------
' ------ 不同课题会有不同的佈放格式 -------
Private Sub FmtOut(Tx As Integer)
Range("K7") = Range("G116")
Range("K8") = Range("H117")
Range("K9") = Range("H22")
If Tx < 4 Then
   Range("M7") = AllTrim("x" + Range("C18") + Range("H118") + Range("G22"))
Else
   Range("M7") = AllTrim("A" + Range("C18") + Range("H118") + Range("G22"))
   Range("M10") = Range("C20")
   DisplayRoot 7, 11, Range("K7")
   Range("K7").VerticalAlignment = xlBottom
End If
End Sub


' ------------ 给出正确答案 ------------------------
Private Sub ToAns(Tx)
Dim a As Single, s1 As String, s2 As String, s3 As String, s4 As String
Dim i As Integer
s1 = Range("E116")
s2 = Range("E117")
s3 = Range("K10")
s4 = Range("K11")
Range("J116") = s3
Range("J117") = s4
If InStr(s1, "J") > 0 Then
   DisplayRoot 13, 11, s1
   Range("K13").VerticalAlignment = xlBottom
Else
   Cells(13, 11).Phonetic.Visible = False
   Range("K13").VerticalAlignment = xlCenter
   Range("K13") = s1
End If
If InStr(s2, "J") > 0 Then
   DisplayRoot 14, 11, s2
   Range("K14").VerticalAlignment = xlBottom
Else
   Cells(14, 11).Phonetic.Visible = False
   Range("K14").VerticalAlignment = xlCenter
   Range("K14") = s2
End If
If InStr(s3, "J") > 0 Then
   DisplayRoot 10, 11, s3
   Range("K10").VerticalAlignment = xlBottom
Else
   Cells(10, 11).Phonetic.Visible = False
   Range("K10").VerticalAlignment = xlCenter
   Range("K10") = s3
End If
If InStr(s4, "J") > 0 Then
   DisplayRoot 11, 11, s4
   Range("K11").VerticalAlignment = xlBottom
Else
   Cells(11, 11).Phonetic.Visible = False
   Range("K11").VerticalAlignment = xlCenter
   Range("K11") = s4
End If
Range("J13") = Range("J10")
Range("J14") = Range("J11")
End Sub



' -------------------  检测对/错 ，计算得分 --------------------
' -----------  Tx: 题型，Eps 允许误差，Dt 耗时 --------
' ----- 此处仅为例， 不同课题，有不同的答案形式 ------------
Private Function CheckAns(Tx As Integer, Eps As Single, Dt As Single) As Single
Dim s1  As String, s2 As String, s3 As String, s4 As String, Mark As Single
Dim i As Integer, j As Integer, k As Single, t As Single, m As Single
Dim a As Single, b As Single, c As Single, d As Single
On Error GoTo eeee
If Eps = 0 Then Eps = 0.0001
m = 0
s1 = Range("K10"): s1 = AllTrim(s1)
s2 = Range("K13"): s2 = AllTrim(s2)
s3 = Range("K11"): s3 = AllTrim(s3)
s4 = Range("K14"): s4 = AllTrim(s4)
If Tx = 4 Then s2 = Left(s2, Len(s2) - 1)
If s1 = s2 Then m = 0.5
If s3 = s4 Then m = m + 0.5
If s1 = "" And s3 = "" Then m = 0
k = m
t = 1 + (StdTime(Tx) - Dt) / StdTime(Tx)               '以耗时与标准时间的相对比率，计算折扣
If t < 0.1 Then t = 0.1
If t > 1.9 Then t = 1.9
k = k * t
If m = 1 Then
   Cells(13 + TiHao, 15) = Range("D18")
ElseIf m > 0 Then
   Cells(13 + TiHao, 15) = Range("D18") + Range("D19")
Else
   Cells(13 + TiHao, 15) = Range("D19")
End If
eeee:
Mark = 10 * k
Cells(13 + TiHao, 16) = Dt
Cells(13 + TiHao, 17) = Mark
Range("Q8") = Range("P24")
Range("Q10") = Range("Q24")
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
Cells(2 + i, 29) = Range("O24")
Cells(2 + i, 30) = Range("Q3")
End Sub
