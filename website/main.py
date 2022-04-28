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
    from qiztxitem.crud import qiztxitemcrud
    from mathSym.crud import mathsym
    app.register_blueprint(mathsym, url_prefix='/trythisapps')    
    #app.register_blueprint(qiztxitemcrud, url_prefix='/trythisapps/qizitem')        
        
    # 根路由
    @app.route("/")
    def index():
        return redirect('/trythisapps/apps')


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
        #username=records[random.choice([0,1])]["user"]
        username=records[0]["user"]
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