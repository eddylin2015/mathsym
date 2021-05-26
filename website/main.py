from flask import current_app, Flask, redirect, request, render_template,send_file,\
     session,url_for,Blueprint
import os
import json
import base64
import pickle
from io import BytesIO
from matplotlib.figure import Figure
from datetime import datetime
import esmathlib as lib    # 自定義,數學出題庫
from functools import wraps
from flask_session import Session
import random
import config
from esapp import login_required_auth, get_model

QAMT = 10  # 出題數目
NTE_Storage = {}

def create_app(config):
    # Flask 框架實例 app
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = app.config["SECRET_KEY"]      
    Session(app)
    with app.app_context():
        model = get_model()
        model.init_app(app)
    from  qiztxitem.crud import qiztxitemcrud
    app.register_blueprint(qiztxitemcrud, url_prefix='/trythisapps/qizitem')        
        
    # 根路由
    @app.route("/")
    def index():
        return redirect('/trythisapps')

    # [START CODE 數學出題及比對答案]
    # 使用模版list.html, 顯示列表
    @app.route("/trythisapps")
    def list():
        items=lib.GetQList()
        if request.args.get('s', "")=="PP" :
            token = request.args.get('page_token', None)
            if token:
                token = token.encode('utf-8')
            books, next_page_token = get_model().QIZTXList(cursor=token)
            print(books)
            return render_template(
                "list_PP.html",
                books=books,
                s=request.args.get('s', "PF"),
                next_page_token=next_page_token)
            #items=["PP301.4.加減除法"]
        else:
            return render_template(
                "list.html",
                books=items,
                s=request.args.get('s', "PF")
            )

    @app.route("/trythisapps/<QID>/view", methods=['GET', 'POST'])
    @login_required_auth
    def MathViewPanel(QID):
        Title_=QID.split(".")
        QIID=Title_[0]
        book = get_model().QIZTXReadByGid(QIID)
        return render_template("view_remi.html", title=QID,book=book, mtitle=Title_[2],Tx=0,cno="",name="") 

    # GET 顯示QAMT題QID相關算式
    # POST 收集作答,並對比答案.
    @app.route("/trythisapps/<QID>", methods=['GET', 'POST'])
    @login_required_auth
    def MathPanel(QID):

        Tx = int(request.args.get('Tx', "-1"))
        cno = (request.args.get('cno', ""))
        name = (request.args.get('name', ""))
        Title_=QID.split(".")
        QIID=Title_[0]
        book = get_model().QIZTXReadByGid(QIID)
        if request.method == 'POST':
            # 取得題目及電腦標準答案 (NTE)
            SID = request.form["SID"]
            NTE_blob = NTE_Storage.get(SID,None)
            if NTE_blob==None:
                return "試題過期!"
            NTE = pickle.loads(NTE_blob)
            # 更新NTE中的 作答(Ans)㯗位資料.
            lib.Post_Expr_UpdateAns(request.form, NTE)
            # 檢查比對作答與電腦答案.
            TEid=int(request.args.get('TEid', "-1"))
            lib.Post_Expr_CheckAns(QIID, NTE,TEid)
            # 清理Session空間.
            fmt = request.args.get('fmt', "")
            if fmt=="JSON":
                TE=NTE[TEid]
                j={"OK":str(TE["OK"]),"Val":str(TE["Val"]),"Mark":str(TE["Mark"]),"Minute":TE["Minute"],"Ans":str(TE["Ans"])}
                return  json.dumps(j, separators=(',', ':')) 
            elif fmt=="REMI":    
                NTE_Storage.pop(SID, None)
                return render_template("result_remi.html", title=QID, NTE=NTE)
            else:
                NTE_Storage.pop(SID, None)
                return render_template("result2.html", title=QID, NTE=NTE)

        # GET 顯示QAMT題QID相關算式
        NTE = lib.Get_Expr(QIID, QAMT, Tx)
        SID = lib.GetKey()
        NTE_blob = pickle.dumps(NTE)
        NTE_Storage[SID] = NTE_blob
        return render_template("form_remi.html", title=QID, book=book, mtitle=Title_[2], NTE=NTE, sid=SID,Tx=Tx,cno=cno,name=name)      

    @app.route('/trythisapps/img/<filename>')
    @login_required_auth
    def showimage(filename):
        try:
            FilePath = os.getcwd()+"/static/"+filename
            return send_file(FilePath,
                             mimetype='image/*')
        except:
            pass

    @app.route("/trythisapps/showPlt")
    @login_required_auth
    def showPlt():
        # Generate the figure **without using pyplot**.
        fig = Figure()
        ax = fig.subplots()
        ax.plot([1, 2])
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
    # [END CODE]

    @app.route('/trythisapps/logout', methods=['GET', 'POST'])
    def logout():
        session['profile'] =  None
        return redirect('/trythisapps')


    @app.route('/trythisapps/login', methods=['GET', 'POST'])
    def login():
        records =config.records
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            for record in records:
              if username == record['user'] and  password == record['Pass'] :
                 session['profile'] =  record
                 #return redirect(url_for('index'))
                 return redirect(config.IndexURL)
        username=records[random.choice([0,1])]["user"]
        return f'''
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <div style="margin-top: 20%;margin-left:50%;margin-right:50%">
            <form method="post">
                <p>USER:<input type=text name=username value="{username}">
                <p>PASS:<input type=password name=password>
                <p><input type=submit value=Login>
            </form>
            </div>
        </body>
        </html>
        '''

    # 容錯處理
    @app.errorhandler(500)
    def server_error(e):
        return """
        內部錯誤: <pre>{}</pre> 查看日誌 full stacktrace.
        """.format(e), 500

    return app

app = create_app(config)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=83, debug=True)