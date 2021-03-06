from flask import Flask, redirect, request
import random    
import datetime

NTE={}

def GetKey(QIID="None"):
    return r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())

def GetTE( St, Val):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = { "St": St,"Val": Val,"Ans": "","OK": 0, "Tip": "", "MaxTry":10, "TryCnt": 0 }
    return TE

def Get_Expr(QID):
    MaxNum=10
    if QID=="PF102":MaxNum=100
    elif QID=="PF103":MaxNum=1000
    else:MaxNum=10
    Val= random.choice(range(1,MaxNum))
    St=f"Guess 1-{MaxNum}"
    return GetTE(St,Val)

def Post_Expr_CheckAns(TE):
    if TE["TryCnt"]>TE["MaxTry"]:
        TE["OK"]=-1
        TE["Tip"]="over times!"
        return 
    try:
        Ans=int(TE["Ans"])
        if TE["Val"]==Ans:
            TE["OK"]=1
            TE["Tip"]="Good job!"
        elif TE["Val"]<Ans:
            TE["OK"]=0
            TE["Tip"]="Too Large"
        elif TE["Val"]>Ans:
            TE["OK"]=0
            TE["Tip"]="Too small"
    except:
        pass

def html_template( title, TE, SID):  
    return r"""<form method=POST>
    <div>%s</div>
    <div>%s</div>
    <input name=Ans>
    <input type=hidden name=SID value='%s'>
    <div>Try %s</div>
    <input type=submit>
    </form>""" % (TE["St"],TE["Tip"],SID,TE["TryCnt"])
     

def create_app():
    app = Flask(__name__)

    # 根路由
    @app.route("/")
    def index():
        return redirect('/apps')

    @app.route("/apps")
    def list():
        books=["PF101.10.1-10","PF102.10.1-100","PF103.10.1-1000"]
        return "<ul>{}</ul>".format("<br>".join(f"<li><a href=apps/{r}>{r}</a></li>"  for r in books))

    @app.route("/apps/<QID>", methods=['GET', 'POST'])
    def MathPanel(QID):
        QIID=QID.split(".")[0]
        if request.method == 'POST':
            SID = request.form["SID"]
            TE=NTE.get(SID,None)
            TE["TryCnt"]+=1
            TE["Ans"]=request.form["Ans"]
            Post_Expr_CheckAns(TE)          
            if TE["OK"]==-1 or TE["OK"]==1:
                return r"""
                        <p>%s</p>
                        <a href=/apps>return</a>
                        """ % TE["Tip"]
            else:
                NTE[SID] =TE 
                return html_template(QID,TE,SID)
        TE=Get_Expr(QIID)
        SID=GetKey()
        NTE[SID] =TE        
        return html_template(QID,TE,SID)

    # 容錯處理
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app

app = create_app()

# the application.
if __name__ == '__main__':
    app.run( host="0.0.0.0",port=8881, debug=True)