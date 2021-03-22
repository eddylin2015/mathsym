from flask import current_app, Flask, redirect, request, render_template,send_file
import os
import base64
import pickle
from io import BytesIO
from matplotlib.figure import Figure
from datetime import datetime
import esmathlib as lib    # 自定義,數學出題庫

QAMT = 6  # 出題數目
NTE_Storage = {}

def create_app():
    # Flask 框架實例 app
    app = Flask(__name__)

    # 根路由
    @app.route("/")
    def index():
        return redirect('/trythisapps')

    # [START CODE 數學出題及比對答案]
    # 使用模版list.html, 顯示列表
    @app.route("/trythisapps")
    def list():
        return render_template(
            "list.html",
            books=lib.GetQList()
        )

    # GET 顯示QAMT題QID相關算式
    # POST 收集作答,並對比答案.
    @app.route("/trythisapps/<QID>", methods=['GET', 'POST'])
    def MathPanel(QID):
        Tx = int(request.args.get('Tx', "-1"))
        QIID = QID.split(".")[0]
        if request.method == 'POST':
            # 取得題目及電腦標準答案 (NTE)
            SID = request.form["SID"]
            NTE_blob = NTE_Storage.get(SID,None)
            NTE = pickle.loads(NTE_blob)
            # 更新NTE中的 作答(Ans)㯗位資料.
            lib.Post_Expr_UpdateAns(request.form, NTE)
            # 檢查比對作答與電腦答案.
            lib.Post_Expr_CheckAns(QIID, NTE)
            # 清理Session空間.
            NTE_Storage.pop(SID, None)
            return render_template("result.html", title=QID, NTE=NTE)

        # GET 顯示QAMT題QID相關算式
        NTE = lib.Get_Expr(QIID, QAMT, Tx)
        SID = lib.GetKey()
        NTE_blob = pickle.dumps(NTE)
        NTE_Storage[SID] = NTE_blob
        return render_template("form.html", title=QID, NTE=NTE, sid=SID)

    @app.route('/trythisapps/img/<filename>')
    def showimage(filename):
        try:
            FilePath = os.getcwd()+"/static/"+filename
            return send_file(FilePath,
                             mimetype='image/*')
        except:
            pass

    @app.route("/trythisapps/showPlt")
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

    # 容錯處理
    @app.errorhandler(500)
    def server_error(e):
        return """
        內部錯誤: <pre>{}</pre> 查看日誌 full stacktrace.
        """.format(e), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=83, debug=True)
