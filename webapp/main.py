from flask import current_app, Flask, redirect, request
import datetime
import random
import sympy as sp
import numpy as np

TE_Storage = {}

def create_app():
    app = Flask(__name__)
 
    @app.route("/")
    def index():
        return redirect('/app')

    @app.route("/app", methods=['GET', 'POST'])
    def MathPanel():
        if request.method == 'POST':
            # 取得題目及電腦標準答案
            SID = request.form["SID"]
            Ans = request.form["Ans"]
            TE=TE_Storage.get(SID)
            if TE==None :
                return "超時! <a href=/app> 下一題 </a>"
            Val=TE["Val"]
            return f""" OK! 答案:{Val}<a href=/app> 下一題 </a>"""
        # GET 顯示題目
        TE={"St":"A+B","Val":1}
        SID=datetime.datetime.now().isoformat()
        TE_Storage[SID]=TE
        return f"""
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            <form method="post">
                <input type=hidden name="SID" value="{SID}">
                <table>
                   <tr><td style="vertical-align: top;">命題:
                       <td><div style="width:200x;height:100px;">
                           \\( \large {TE["St"]} \\)
                           </div>
                    <tr><td>答題:<td><input type=text name=Ans value=""><input type=submit value="提交">
                </table>
            </form>
        </body>
        </html>
        """

    # 容錯處理
    @app.errorhandler(500)
    def server_error(e):
        return """<pre>{}</pre>full stacktrace.""".format(e), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=83, debug=True)