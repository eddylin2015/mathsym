from .. import get_model, login_required_auth, storage
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
import json    
import random

import sympy as sp

from sympy.parsing.sympy_parser import parse_expr
import esmathlib
import esutils
from functools import wraps
from flask_session import Session
#from sympy.plotting import plot
sp.init_printing("mathjax")     #sp.init_printing()

mathsym = Blueprint('mathsym', __name__)

def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url

@mathsym.route("/")
@login_required_auth
def list():
    str(session["profile"])
    return esmathlib.foo()


@mathsym.route("/PF101", methods=['GET', 'POST'])
@login_required_auth
def get_RationalNumExpr():
    Tx = request.args.get('Tx', None)
    QizAmt = request.args.get('QizAmt', None)
    if Tx==None: Tx=1
    if QizAmt==None : QizAmt=1
    QizAmt=int(QizAmt)
    return json.dumps(esmathlib.get_RationalNumExpr(Tx,QizAmt))


@mathsym.route("/<QID>", methods=['GET', 'POST'])
@login_required_auth
def MathPanel(QID):
    QIID=QID.split(".")[0]
    if request.method == 'POST':
        f = request.form["SID"]
        NTE=session.get(f,None)
        del session[f]
        for key in request.form.keys():
            if key=="SID": continue
            for value in request.form.getlist(key):
                #print (key+":"+value)
                TE= NTE[int(key)]
                if TE["Ans"] != "" :  
                    TE["Ans"]=TE["Ans"]+";"+ value 
                else:
                    TE["Ans"]=value
        if QIID=="PF101" : esmathlib.Post_PF101_Expr(NTE)
        elif QIID=="PF102" : esmathlib.Post_PF102_Expr(NTE)
        elif QIID=="PF103" : esmathlib.Post_PF103_Expr(NTE)
        elif QIID=="PF104" : esmathlib.Post_PF104_Expr(NTE)
        elif QIID=="PF105" : esmathlib.Post_PF105_Expr(NTE)
        elif QIID=="PF106" : esmathlib.Post_PF106_Expr(NTE)
        elif QIID=="PF107" : esmathlib.Post_PF107_Expr(NTE)
        elif QIID=="PF108" : esmathlib.Post_PF108_Expr(NTE)
        elif QIID=="PF201" : esmathlib.Post_PF201_Expr(NTE)
        elif QIID=="PF202" : esmathlib.Post_PF202_Expr(NTE)
        elif QIID=="PF203" : esmathlib.Post_PF203_Expr(NTE)
        elif QIID=="PF204" : esmathlib.Post_PF204_Expr(NTE)
        elif QIID=="PF205" : esmathlib.Post_PF205_Expr(NTE)
        elif QIID=="PF206" : esmathlib.Post_PF206_Expr(NTE)
        elif QIID=="PF207" : esmathlib.Post_PF207_Expr(NTE)
        elif QIID=="PF291" : esmathlib.Post_PF291_Expr(NTE)
        elif QIID=="PF292" : esmathlib.Post_PF292_Expr(NTE)
        elif QIID=="PF293" : esmathlib.Post_PF293_Expr(NTE)
        elif QIID=="PF301" : esmathlib.Post_PF301_Expr(NTE)
        elif QIID=="PF302" : esmathlib.Post_PF302_Expr(NTE)
        elif QIID=="PF303" : esmathlib.Post_PF303_Expr(NTE)
        elif QIID=="PF304" : esmathlib.Post_PF304_Expr(NTE)
        elif QIID=="PF305" : esmathlib.Post_PF305_Expr(NTE)
        return render_template("mathUI/result.html", title=QID, NTE=NTE)    
        #return str(NTE)
    NTE=None
    if QIID=="PF101": NTE=esmathlib.Get_PF101_Expr(4)
    elif QIID=="PF102" : NTE=esmathlib.Get_PF102_Expr(4)
    elif QIID=="PF103" : NTE=esmathlib.Get_PF103_Expr(4)
    elif QIID=="PF104" : NTE=esmathlib.Get_PF104_Expr(4)
    elif QIID=="PF105" : NTE=esmathlib.Get_PF105_Expr(4)
    elif QIID=="PF106" : NTE=esmathlib.Get_PF106_Expr(4)
    elif QIID=="PF107" : NTE=esmathlib.Get_PF107_Expr(4)
    elif QIID=="PF108" : NTE=esmathlib.Get_PF108_Expr(4)
    elif QIID=="PF201" : NTE=esmathlib.Get_PF201_Expr(4)
    elif QIID=="PF202" : NTE=esmathlib.Get_PF202_Expr(4)
    elif QIID=="PF203" : NTE=esmathlib.Get_PF203_Expr(4)
    elif QIID=="PF204" : NTE=esmathlib.Get_PF204_Expr(4)
    elif QIID=="PF205" : NTE=esmathlib.Get_PF205_Expr(4)
    elif QIID=="PF206" : NTE=esmathlib.Get_PF206_Expr(4)
    elif QIID=="PF207" : NTE=esmathlib.Get_PF207_Expr(4)
    elif QIID=="PF291" : NTE=esmathlib.Get_PF291_Expr(4)
    elif QIID=="PF292" : NTE=esmathlib.Get_PF292_Expr(4)
    elif QIID=="PF293" : NTE=esmathlib.Get_PF293_Expr(4)
    elif QIID=="PF301" : NTE=esmathlib.Get_PF301_Expr(4)
    elif QIID=="PF302" : NTE=esmathlib.Get_PF302_Expr(4)
    elif QIID=="PF303" : NTE=esmathlib.Get_PF303_Expr(4)
    elif QIID=="PF304" : NTE=esmathlib.Get_PF304_Expr(4)
    elif QIID=="PF305" : NTE=esmathlib.Get_PF305_Expr(4)
    else:
        return "None"
    session[NTE[0]['Key']] =NTE        
    if NTE==None: return "None"
    return render_template("mathUI/form.html", title=QID, books=NTE,sid=NTE[0]['Key'])    

