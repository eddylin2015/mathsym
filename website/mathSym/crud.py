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
mathsym = Blueprint('trythisapps', __name__)

import esmathlib as lib    # 自定義,數學出題庫
# [START CODE 數學出題及比對答案]
# 使用模版list.html, 顯示列表
@mathsym.route("/")
def index():
    return redirect('/trythisapps/apps')  

@mathsym.route("/apps")
def list():
    return render_template(
        "mathsym/list.html",
        books=lib.GetQList()
        )    

@mathsym.route("/apps/<QID>/view", methods=['GET', 'POST'])
@login_required_auth
def MathViewPanel(QID):
    Title_=QID.split(".")
    QIID=Title_[0]
    book = None # get_model().QIZTXReadByGid(QIID)
    return render_template("mathsym/view_remi.html", title=QID,book=book, mtitle=Title_[2],Tx=0,cno="",name="",xtgrade=4)

# GET 顯示QAMT題QID相關算式
# POST 收集作答,並對比答案.
@mathsym.route("/apps/<QID>", methods=['GET', 'POST'])
@login_required_auth
def MathPanel(QID):
    Tx = int(request.args.get('Tx', "-1"))
    cno = (request.args.get('cno', ""))
    name = (request.args.get('name', ""))
    Title_=QID.split(".")
    QIID=Title_[0]
    book = None #get_model().QIZTXReadByGid(QIID)
    if request.method == 'POST':
        # 取得題目及電腦標準答案 (NTE)
        SID = request.form["SID"]
        NTE_blob = NTE_Storage.get(SID,None)
        if NTE_blob==None:
            return "試題過期!"
        NTE = pickle.loads(NTE_blob)
        TEid=int(request.args.get('TEid', "-1"))
        if int(TEid)>-1:
            # 更新NTE中的 作答(Ans)㯗位資料.
            lib.Post_Expr_UpdateAns(request.form, NTE,TEid)
            # 檢查比對作答與電腦答案.
            lib.Post_Expr_CheckAns(QIID, NTE,TEid)
        # 清理Session空間.
        fmt = request.args.get('fmt', "")
        if fmt=="JSON":
            TE=NTE[TEid]
            ValFmt="" if TE["ValFmt"]==None else TE["ValFmt"]
            ValSt="" if TE["ValSt"]==None else TE["ValSt"]
            j={"OK":str(TE["OK"]),"Val":str(TE["Val"]),"ValFmt":ValFmt,"ValSt":ValSt,"Mark":str(TE["Mark"]),"Minute":TE["Minute"],"Ans":str(TE["Ans"])}
            return  json.dumps(j, separators=(',', ':')) 
        elif fmt=="REMI":    
            NTE_Storage.pop(SID, None)
            return render_template("mathsym/result_remi.html", title=QID, NTE=NTE)
        else:
            NTE_Storage.pop(SID, None)
            return render_template("mathsym/result_remi.html", title=QID, NTE=NTE)
    # GET 顯示QAMT題QID相關算式
    NTE = lib.Get_Expr(QIID, QAMT, Tx)
    SID = lib.GetKey()
    NTE_blob = pickle.dumps(NTE)
    NTE_Storage[SID] = NTE_blob
    return render_template("mathsym/form_remi.html", title=QID, book=book, mtitle=Title_[2], NTE=NTE, sid=SID,Tx=Tx,cno=cno,name=name,xtgrade=4)      #_remi

@mathsym.route('/apps/img/<filename>')
@login_required_auth
def showimage(filename):
    try:
        FilePath = os.getcwd()+"/static/"+filename
        return send_file(FilePath,
                         mimetype='image/*')
    except:
        pass

@mathsym.route("/apps/showPlt")
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


