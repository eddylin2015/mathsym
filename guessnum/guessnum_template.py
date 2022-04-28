from flask import current_app, Flask, redirect, request, session, url_for,render_template
from flask_session import Session
import random    # 自定義,數學出題庫
import datetime

def GetKey(QIID="None"):
    return r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())

def GetTE(St, Val):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = { "St": St,"Val": Val,"Ans": "","OK": 0, "Tip": "", "MaxTry":10, "TryCnt": 0 }
    return TE

def Get_Expr(QID):
    MaxNum=10
    Val= random.choice(range(1,MaxNum))
    St=f"Guess 1-{MaxNum}"
    return GetTE(St,Val)

def Post_Expr_UpdateAns(ReqForm,TE):
    TE["TryCnt"]+=1
    for key in ReqForm.keys():
        if key=="SID": continue
        for value in ReqForm.getlist(key):
            if "Ans"==key:
                TE["Ans"]=value

def Post_Expr_CheckAns(TE):
    if TE["TryCnt"]>TE["MaxTry"]:
        TE["OK"]=-1
        TE["Tip"]="over try times!"
        return False
    try:
        Ans=int(TE["Ans"])
        if TE["Val"]==Ans:
            TE["OK"]=1
            TE["Tip"]="Good job!"
            return True
        elif TE["Val"]<Ans:
            TE["OK"]=0
            TE["Tip"]="Too Large"
        elif TE["Val"]>Ans:
            TE["OK"]=0
            TE["Tip"]="Too small"
    except:
        pass
    return False

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'        
    app.config['SESSION_TYPE'] = 'filesystem'  # session类型为redis, filesystem
    app.config['SESSION_USE_SIGNER'] = True  # 是否对发送到浏览器上session的cookie值进行加密
    app.config['SESSION_PERMANENT'] = True  # 如果设置为True，则关闭浏览器session就失效。
    Session(app)
    # Add a default root route.
    # 根路由
    @app.route("/")
    def index():
        return redirect('/apps')

    # Template Show MathQiz list.
    # 使用模版list.html, 顯示列表 
    @app.route("/apps")
    def list():
        books=["PF101.10.1-10","PF102.10.1-100","PF103.10.1-1000"]
        return render_template(
            "list.html",
            books=books
        )        

    @app.route("/apps/<QID>", methods=['GET', 'POST'])
    def MathPanel(QID):
        QIID=QID.split(".")[0]
        if request.method == 'POST':
            SID = request.form["SID"]
            TE=session.get(SID,None)
            Post_Expr_UpdateAns(request.form,TE) 
            Post_Expr_CheckAns(TE)          
            if TE["OK"]==0:
                session[SID] =TE 
            else:
                session.pop(SID,None)
            return render_template("guessnum.html", title=QID, TE=TE, SID=SID)                

        TE=Get_Expr(QIID)
        SID=GetKey()
        session[SID] =TE        
        return render_template("guessnum.html", title=QID, TE=TE, SID=SID)                                

    # Add an error handler. 
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