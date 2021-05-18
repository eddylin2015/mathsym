""" This example permits to play with VBox and HBox layouts.
    Different style parameters plays a specific role in layout arrangement,
     and this little application allows to test each parameter behavior.
"""
 
import remi.gui as gui
from remi.gui import *
from remi import start, App
import esmathlib as lib    # 自定義,數學出題庫  

def Tb(num_rows, num_cols):
    data = [['' for j in range(num_cols)] for i in range(num_rows)]
    data[0] = ['题号','对/错','耗时','得分']
    data[1]=['1','','','']
    data[2]=['2','','','']
    data[3]=['3','','','']
    data[4]=['4','','','']
    data[5]=['5','','','']
    data[6]=['6','','','']
    data[7]=['7','','','']
    data[8]=['8','','','']
    data[9]=['9','','','']
    data[10]=['10','','','']
    data[11]=['总计','','','']
    return data
MarkTb = Tb(12,4)


class untitled(App):
    def main(self):

        self.NTE = lib.Get_Expr("PF304", 10, 2)
        self.TxIdx=0
        #custom additional html head tags
        my_html_head = """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.css" integrity="sha384-zB1R0rpPzHqg7Kpt0Aljp8JPLqbXI3bhnPWROx27a9N0Ll6ZP/+DiW/UqRcLbRjq" crossorigin="anonymous">
            """

        #custom js
        my_js_head = """
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/katex.min.js" integrity="sha384-y23I5Q6l+B6vatafAwxRu/0oK/79VlbSz7Q9aiSZUvyWYIYsd+qj+o24G5ZU2zJz" crossorigin="anonymous"></script>
            """
        #appending elements to page header
        self.page.children['head'].add_child('myhtml', my_html_head)
        self.page.children['head'].add_child('myjs', my_js_head)

        mainContainer = Container(width=800, height=540)
        lblTitle = gui.Label("有理数运算",margin="5px",style='position:absolute; left:340px; top:0px')
        mainContainer.append(lblTitle)

        lbl1=gui.Label("班级",margin="0px",style='position:absolute; left:10px; top:40px')
        tin1=gui.TextInput(width=80,height=20,margin="3px",style='position:absolute; left:40px; top:37px')
        mainContainer.append(lbl1)
        mainContainer.append(tin1)

        lbl2=gui.Label("姓名",margin="0px",style='position:absolute; left:140px; top:40px')
        tin2=gui.TextInput(width=80,height=20,margin="3px",style='position:absolute; left:170px; top:37px')
        mainContainer.append(lbl2)
        mainContainer.append(tin2)

        lbl3=gui.Label("日期",margin="0px",style='position:absolute; left:340px; top:40px')
        tin3=gui.TextInput(width=60,height=20,margin="3px",style='position:absolute; left:370px; top:37px')
        mainContainer.append(lbl3)
        mainContainer.append(tin3)

        lbl4=gui.Label("时间",margin="0px",style='position:absolute; left:450px; top:40px')
        tin4=gui.TextInput(width=60,height=20,margin="3px",style='position:absolute; left:480px; top:37px')
        mainContainer.append(lbl4)
        mainContainer.append(tin4)

        lbl5=gui.Label("總耗時",margin="0px",style='position:absolute; left:560px; top:40px')
        tin5=gui.TextInput(width=50,height=20,margin="3px",style='position:absolute; left:605px; top:37px')
        mainContainer.append(lbl5)
        mainContainer.append(tin5)

        lbl6=gui.Label("總得分",margin="0px",style='position:absolute; left:670px; top:40px')
        tin6=gui.TextInput(width=50,height=20,margin="3px",style='position:absolute; left:715px; top:37px')
        mainContainer.append(lbl6)
        mainContainer.append(tin6)

        bt1 = Button('題型1', width=60, height=25,margin="0px",style='position:absolute; left:10px; top:80px')
        mainContainer.append(bt1,'bt1')
        bt2 = Button('題型2', width=60, height=25,margin="0px",style='position:absolute; left:80px; top:80px')
        mainContainer.append(bt2,'bt2')
        bt3 = Button('題型3', width=60, height=25,margin="0px",style='position:absolute; left:150px; top:80px')
        mainContainer.append(bt3,'bt3')
        bt4 = Button('題型4', width=60, height=25,margin="0px",style='position:absolute; left:220px; top:80px')
        mainContainer.append(bt4,'bt4')

        lbl7=gui.Label("題型",margin="0px",style='position:absolute; left:370px; top:85px')
        tin7=gui.TextInput(width=40,height=20,margin="3px",style='position:absolute; left:405px; top:82px')
        mainContainer.append(lbl7)
        mainContainer.append(tin7)

        lbl8=gui.Label("題號",margin="0px",style='position:absolute; left:465px; top:85px')
        tin8=gui.TextInput(width=40,height=20,margin="3px",style='position:absolute; left:500px; top:82px')
        mainContainer.append(lbl8)
        mainContainer.append(tin8)

        SubCtn = HBox(width=780, height=400, style='position: absolute; left: 10px; top:130px; background-color:#fde9d9')
 
        HboxL = Container(width=500, height=380,style='position: absolute; left: 10px; top:130px')
        lbl9=gui.Label('命題',mragin="0px",style='position:absolute; left:10px; top:25px')
        
        tin9=gui.TextInput(width=240,height=50,style='position:absolute; left:45px; top:10px')
        self.tin9_1=gui.Label(r"$ \frac{a}{b} $",width=240,height=50,style='position:absolute; left:45px; top:10px')

        self.bt9=gui.Button('下一題',width=60, height=25,style='position:absolute; left:300px; top:25px')
        self.bt9.onclick.do(self.on_button_pressed)        
        HboxL.append([lbl9,self.tin9_1,self.bt9])
     
        lbl10=gui.Label('答題',mragin="0px",style='position:absolute; left:10px; top:90px')
        tin10=gui.TextInput(width=240,height=50,style='position:absolute; left:45px; top:75px')
        bt10=gui.Button('提交',width=60, height=25,style='position:absolute; left:300px; top:85px')
        HboxL.append([lbl10,tin10,bt10])
     
        lbl11=gui.Label('答案',mragin="0px",style='position:absolute; left:10px; top:155px')
        tin11=gui.TextInput(width=240,height=50,style='position:absolute; left:45px; top:140px')
        HboxL.append([lbl11,tin11])
        
        St="说明："
        lbl12=gui.Label(St,width=500,height=175,style='position:absolute; left:10px;top:215px;background-color:#ffffd8')
        HboxL.append([lbl12])
        SubCtn.append(HboxL)

        HboxR = VBox(width=240, height=380,style='position:absolute; left:510px;top:130px')
        Tb1=gui.Table.new_from_list(content=MarkTb,width='240px',height='380px')        
        HboxR.append(Tb1)
        SubCtn.append(HboxR)
        mainContainer.append(SubCtn)

        self.mainContainer = mainContainer
        return self.mainContainer

    # listener function
    def on_button_pressed(self, widget):
        self.TxIdx=self.TxIdx+1
        TE=self.NTE[self.TxIdx]
        if self.TxIdx<len(self.NTE):
            self.execute_javascript("""katex.render("%s", document.getElementById("%s"), {throwOnError: false});"""%(TE["St"],self.tin9_1.identifier))

    def onload(self, emitter):
        self.execute_javascript("""katex.render("c =  \\sqrt{a^2 + b^2}", document.getElementById("%s"), {throwOnError: false});"""%self.tin9_1.identifier)
        super(untitled, self).onload(emitter)    
 
#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 0, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'untitled', 'config_resourcepath': './res/'}
 
if __name__ == "__main__":
    #start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)

    start(untitled,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    '''
    start(untitled, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
    '''
