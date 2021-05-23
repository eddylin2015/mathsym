import remi.gui as gui
#  import time
import datetime
import numpy as np
from remi.gui import *
from remi import start, App


# ------ 命题,評量,上傳 ------              
def Get_Tm(tx):                            # 命题函数(包括答案)
    if tx==1:
       Tm_Str="题型1：1+1"                  # 暂時模擬，以便检测操控逻辑
    if tx==2:
       Tm_Str="题型2：2+2"
    if tx==3:
       Tm_Str="题型3：3+3"
    if tx==4:
       Tm_Str="题型4：4+4"
    return Tm_Str                          # 输出题目和答案

# ------- 介面設計 --------
Rs=np.zeros((11,3))                         # 評量表
                                            # Rs的下標從 0計起 R:0..10, C:0..2
Title="有理數運算"                           # 項目名

# ----  说明文字 -------
St="操作说明：\n "
St+="1. 先填上班级，姓名。\n "
St+="2. 選擇题型 --- 一次選擇之後，只有當题號为0時才能更新题型。\n " 
St+="3. 【下一题】--- 項目自動根据题型命题，一卷10题。\n "
St+="4. 答题後【确定】 --- 項目給出評量并記入右面表格。\n "
St+="5. 10题完成後【提交】 --- 項目自動將評量上傳；\n "
St+="6. 【提交】上傳之前，若不满意你的評量，可【重置】再做一卷。\n "
St+="7. 根式的输入格式规定：用大写“J”代替根号‎√‎，根号内容要用括弧括住,\n     例如J(123),表示123的平方根。\n"
St+="8. 指数的输入格式规定：用“^”表示指数，例如a的5次方，键入 a^5。\n "

# ----- 介面佈局 --------
class TestMySelf(App):
    def main(self):
        mainContainer = Container(width=800, height=640,style='background-color:#cdf2ff')
        SubCtn = HBox(width=780, height=500, style='position: absolute; left: 10px; top:130px; background-color:#a0a0a0')
        HboxL = Container(width=460, height=490,style='position: absolute;background-color:#fde9d9')
        HboxR = Container(width=300, height=490,style='position:absolute;background-color:#e9fdd9')

        lblTitle = gui.Label(Title,margin="5px",style='position:absolute; left:300px; top:0px')
        lblTitle.style['font-family'] = '隶书'
        lblTitle.style['font-size'] = '30px'
        lblTitle.style['font-color'] = 'rgb(0,0,255)'   # 字色未作用？
        lblTitle.style['font-weight'] = 'bold'
        mainContainer.append(lblTitle)

        lbl1=gui.Label("班级",margin="0px",style='position:absolute; left:10px; top:50px')
        tin1=gui.Input(width=80,height=20,margin="3px",style='position:absolute; left:38px; top:45px')
        lbl2=gui.Label("姓名",margin="0px",style='position:absolute; left:150px; top:50px')
        tin2=gui.Input(width=80,height=20,margin="3px",style='position:absolute; left:178px; top:45px')
        mainContainer.append([lbl1,tin1,lbl2,tin2])

        lbl3=gui.Label("日期",margin="0px",style='position:absolute; left:320px; top:50px')
        self.tin3=gui.Input(width=70,height=20,margin="3px",style='position:absolute; left:348px; top:45px')
        self.tin3.set_read_only(True)
        lbl4=gui.Label("時間",margin="0px",style='position:absolute; left:440px; top:50px')
        self.tin4=gui.Input(width=60,height=20,margin="3px",style='position:absolute; left:468px; top:45px')
        self.tin4.set_read_only(True)
        mainContainer.append([lbl3,self.tin3,lbl4,self.tin4])

        lbl5=gui.Label("總耗時",margin="0px",style='position:absolute; left:562px; top:50px')
        self.tin5=gui.Input(width=50,height=20,margin="3px",style='position:absolute; left:605px; top:45px')
        self.tin5.set_read_only(True)
        lbl6=gui.Label("總得分",margin="0px",style='position:absolute; left:678px; top:50px')
        self.tin6=gui.Input(width=50,height=20,margin="3px",style='position:absolute; left:720px; top:45px')
        self.tin6.set_read_only(True)
        mainContainer.append([lbl5,self.tin5,lbl6,self.tin6])

        lbl7=gui.Label("題型",margin="0px",style='position:absolute; left:345px; top:90px')
        self.tin7=gui.Input(width=40,height=20,margin="3px",style='position:absolute; left:375px; top:85px')
        self.tin7.set_read_only(True)
        lbl8=gui.Label("題號",margin="0px",style='position:absolute; left:458px; top:90px')
        self.tin8=gui.Input(width=40,height=20,margin="3px",style='position:absolute; left:488px; top:85px')
        self.tin8.set_read_only(True)
        lbl13=gui.Label("等级",margin="0px",style='position:absolute; left:690px; top:90px')
        self.tin13=gui.Input(width=50,height=20,margin="3px",style='position:absolute; left:720px; top:85px')
        self.tin13.set_read_only(True)
        mainContainer.append([lbl7,self.tin7,lbl8,self.tin8,lbl13,self.tin13])

        self.bt1 = Button('題型1', width=60, height=25,margin="0px",style='position:absolute; left:10px; top:85px')
        self.bt1.onclick.do(self.Tx_Select,1)
        self.bt2 = Button('題型2', width=60, height=25,margin="0px",style='position:absolute; left:80px; top:85px')
        self.bt2.onclick.do(self.Tx_Select,2)
        self.bt3 = Button('題型3', width=60, height=25,margin="0px",style='position:absolute; left:150px; top:85px')
        self.bt3.onclick.do(self.Tx_Select,3)
        self.bt4 = Button('題型4', width=60, height=25,margin="0px",style='position:absolute; left:220px; top:85px')
        self.bt4.onclick.do(self.Tx_Select,4)
        mainContainer.append([self.bt1,self.bt2,self.bt3,self.bt4])

        lbl9=gui.Label('命題',mragin="0px",style='position:absolute; left:10px; top:25px')
        self.tin9=gui.Input(width=320,height=140,style='position:absolute; left:45px; top:15px')
        self.bt9=gui.Button('下一題',width=60, height=25,style='position:absolute; left:380px; top:25px')
        self.tin9.set_read_only(True)
        self.bt9.onclick.do(self.Th_Next)
        HboxL.append([lbl9,self.tin9,self.bt9])

        lbl10=gui.Label('答題',mragin="0px",style='position:absolute; left:10px; top:185px')
        self.tin10=gui.Input(width=240,height=40,style='position:absolute; left:45px; top:175px')
        self.bt10=gui.Button('确定',width=60, height=25,style='position:absolute; left:310px; top:185px')
        self.bt10.onclick.do(self.Ok)
        HboxL.append([lbl10,self.tin10,self.bt10])

        lbl11=gui.Label('答案',mragin="0px",style='position:absolute; left:10px; top:245px')
        self.tin11=gui.Input(width=240,height=40,style='position:absolute; left:45px; top:235px')
        self.tin11.set_read_only(True)
        self.bt11=gui.Button('提交',width=60, height=25,style='position:absolute; left:310px; top:250px')
        self.bt11.onclick.do(self.submit)
        self.bt12=gui.Button('重置',width=60, height=25,style='position:absolute; left:380px; top:250px')
        self.bt12.onclick.do(self.Reset)
        HboxL.append([lbl11,self.tin11,self.bt11,self.bt12])
        
        tin12=gui.Label(St,width=450,height=200,style='position:absolute; left:10px;top:290px;background-color:#ffffda')
        tin12.style['white-space']='pre'
        tin12.style['font-size'] = '14px'
        HboxL.append([tin12])
        SubCtn.append(HboxL)


        
        self.Tb1 = gui.TableWidget(12, 4, True, False, width=290, height=275,style='position:relative; left:5px;top:210px')
        self.Tb1.style['font-size'] = '14px'
        self.Tb1.item_at(0,0).set_text("题號")
        self.Tb1.item_at(0,1).set_text("對/錯")
        self.Tb1.item_at(0,2).set_text("耗時")
        self.Tb1.item_at(0,3).set_text("得分")
        for i in range(1,12):
           self.Tb1.item_at(i,0).set_text(str(i))           
        self.Tb1.item_at(11,0).set_text("總計")
        HboxR.append(self.Tb1)

        SubCtn.append(HboxR)
        mainContainer.append(SubCtn)
        self.mainContainer = mainContainer
        self.Reset(self)
        return self.mainContainer
    
# ------ 操作嚮應 -----------
    def Update_now(self,widget):            # 日期時間更新
        global today
        global now
        today=datetime.date.today()
        now = datetime.datetime.now()
        self.tin3.set_value(today)
        nowtime=str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        self.tin4.set_value(nowtime)
        return today,now

# ------ 监察嚮應 ----------
    def Reset(self,widget):                 # 重置
        global Tx          # 题型
        global Th          # 题號
        global Hs          # 總耗時
        global Df          # 總得分
        global Gd          # 等级
        global Sw_Th       # 有题號被选,取值(0,1)
        Tx=0
        Th=0
        Hs=0
        Df=0
        Gd=0
        Sw_Th=0
        self.Update_now(self)
        self.tin5.set_value(Hs)
        self.tin6.set_value(Df)
        self.tin7.set_value(Tx)
        self.tin8.set_value(Th)
        self.tin13.set_value(Gd)
        self.tin9.set_value("")
        self.tin10.set_value("")
        self.tin11.set_value("")
        for i in range(1,12):
            for j in range(1,4):
               Rs[i-1,j-1]=0
               self.Tb1.item_at(i,j).set_text(str(Rs[i-1,j-1]))  

    def Tx_Select(self,widget,tx):          # 题型选择
        if Th==0:
           global Tx
           Tx=tx
           self.tin7.set_value(Tx)

    def Th_Next(self,widget):               # 下一题
        global St_Time                      # 某题的起始時間
        global Th
        global Sw_Th
        if Sw_Th==0:
           self.Update_now(self)
           St_Time=now
           if Th<10 and Tx>0:
              Th+=1
              self.tin8.set_value(Th)
           Sw_Th=1
           Tm=Get_Tm(Tx)
           self.tin9.set_value(Tm)
           self.tin10.set_value("")
           self.tin11.set_value("")
            
        return Sw_Th,Th

    def Ok(self,widget):                    # 确定
        global Sw_Th
        global Hs
        global Df
        global Gd
        Gd=5
        self.Update_now(self)
        if Sw_Th==1:
           Dt=(now-St_Time).seconds
           self.Update_Rs(Th,2,Dt)
           Hs=Rs[10,1]
           self.tin5.set_value(Hs)
# 在此加入： 出示答案，進行評量，更新評量表
           df=Dt                         # 暂時假設单题得分是df
           self.Update_Rs(Th,3,df)
           Df=Rs[10,2]
           self.tin6.set_value(Df)
           if Df<95:Gd=4
           if Df<80:Gd=3
           if Df<60:Gd=2
           if Df<40:Gd=1
           self.tin13.set_value(Gd)
           self.tin11.set_value("在此給出参考答案")
           Sw_Th=0
        return Hs,Sw_Th

    def submit(self,widget):                # 提交
# 在此加入上傳處理上傳                        # 待寫

        self.Reset(self)

    def Update_Rs(self,R,C,vl):             # 更新評量表，
        Rs[R-1,C-1]=vl
        self.Tb1.item_at(R,C).set_text(str(vl))
        Hs=0
        for i in range(0,10):
           Hs+=Rs[i,C-1]
        Rs[10,C-1]=Hs
        self.Tb1.item_at(11,C).set_text(str(Hs))

#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 0, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'TestMySelf', 'config_resourcepath': './res/'}
 
if __name__ == "__main__":
    start(TestMySelf, address=configuration['config_address'], port=configuration['config_port'], 
          multiple_instance=configuration['config_multiple_instance'], 
          enable_file_cache=configuration['config_enable_file_cache'],
          start_browser=configuration['config_start_browser'])
