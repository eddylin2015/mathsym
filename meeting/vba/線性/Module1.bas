Attribute VB_Name = "Module1"
Option Explicit


Type APnt
   Name     As String
   x              As Single
   y              As Single
End Type

Type ApSet
   n                 As Integer
   Pnt()           As APnt
   Cp              As APnt
End Type


Type ALine
   a              As Single
   b              As Single
   c              As Single
   Op           As String
   OPF         As Integer
   St             As String
   St1         As String
End Type



' ----- 產生受限的隨機數 -------
' ----- 範圍(a, b),  受限 (c, d)
' ----- Sw = 0  不受限,  Sw = 1, 受限， [c, d] 內的數不接受 -----
Public Function GetARnd(a As Single, b As Single, e As Integer, Sw As Integer, c As Single, D As Single) As Single
Dim x As Single, BL As Boolean
If a > b Then x = a: a = b: b = x                       '若a>b 則 a, b 交換
If c > D Then x = c: c = D: D = x                       '若c>d 則 c, d 交換
BL = False
Do                                                                   ' 設置循環
   x = a + (b - a) * Rnd                                     ' 取得 [a, b)範圍內的隨机數
   x = Round(x, e)                                             ' 截取 x 的 e 位四舍五入小數
   If Sw = 1 Then BL = x >= c And x <= D       ' 若x落在 [c, d] 內，則返回再取 x
Loop Until BL = False                                      ' 若x不在 [c, d] 內，則終止循環
GetARnd = x                                                    ' 輸出 x
End Function

' -----  HCF -------
Public Function HCF(i As Single, j As Single) As Single
Dim m As Single, n As Single, r As Single, k As Single
m = Abs(i): n = Abs(j)
If m = 0 And n = 0 Then
   n = 1
ElseIf n = 0 Then
   n = m
ElseIf m > 0 Then
   If m < n Then r = m: m = n: n = r
   r = m Mod n
   k = n
   If r > 0 Then n = HCF(k, r)
End If
HCF = n
End Function

' -------
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


' ----- 文字框觸摸彈跳 ----------
Sub TextBox1_Click()
Range("A2").Select
End Sub

' ----------  代替MsgBox ----------
Sub TextBox2_Click()
Sheet01.Shapes.Range(2).Visible = False
Range("A2").Select
End Sub


