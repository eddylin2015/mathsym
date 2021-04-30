from esapp import get_model,login_required_auth
from flask import flash,Blueprint, current_app, redirect, render_template, request, \
    session, url_for,send_file,Flask,send_from_directory
import os
import zipfile

from urllib.parse import quote

qiztxitemcrud = Blueprint('qizitem', __name__) 

@qiztxitemcrud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().QIZTXList(cursor=token)
    return render_template(
        "qizitem/list.html",
        books=books,
        next_page_token=next_page_token)

# [START list_mine]
@qiztxitemcrud.route("/mine")
@login_required_auth
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().QIZTXList_by_user(
        user_id=session['profile']['id'],
        cursor=token)
    return render_template(
        "qizitem/list.html",
        books=books,
        next_page_token=next_page_token)
# [END list_mine]

@qiztxitemcrud.route('/<id>')
@login_required_auth
def view(id):
    book = get_model().QIZTXRead(id)
    return render_template("qizitem/view.html", book=book)

# [START add]
@qiztxitemcrud.route('/add', methods=['GET', 'POST'])
@login_required_auth
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        # If the user is logged in, associate their profile with the new book.
        if 'profile' in session:
            data['createbyid'] = session['profile']['id']
        book = get_model().QIZTXCreate(data)
        return redirect(url_for('.view', id=book['id']))
    return render_template("qizitem/form.html", action="Add", book={})
# [END add]

@qiztxitemcrud.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_auth
def edit(id):
    book = get_model().QIZTXRead(id)
    if (book["createbyid"]==str(session['profile']['id'])) :        
        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            book = get_model().QIZTXUpdate(data, id)
            return redirect(url_for('.view', id=book['id']))
        return render_template("qizitem/form.html", action="Edit", book=book)
    else:
        return redirect("/trythisapps/qizitem/")    


@qiztxitemcrud.route('/<id>/delete')
@login_required_auth
def delete(id):
    get_model().QIZTXDelete(id)        
    return redirect(url_for('.list'))

    
@qiztxitemcrud.route('/<id>/downloadall')
@login_required_auth
def download_all(id):
    book = get_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    path = current_app.config['HW_UPLOAD_FOLDER']
    UPLOAD_FOLDER = os.path.join(path, crspath)
    ZIP_PATH = os.path.join(path, "ZIPFILE")
    if not os.path.isdir(ZIP_PATH):
        os.mkdir(ZIP_PATH)
    # Zip file Initialization and you can change the compression type
    ZipFileName=f"HW{crspath}.zip"
    ZipFilePath=ZIP_PATH+"/"+ZipFileName
    zipfolder = zipfile.ZipFile(ZipFilePath,'w', compression = zipfile.ZIP_STORED)
    # zip all the files which are inside in the folder
    for root,dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            zipfolder.write(UPLOAD_FOLDER+'/'+file)
    zipfolder.close()
    return send_file(ZipFilePath,
            mimetype = 'zip',
            attachment_filename= ZipFileName,
            as_attachment = True)
    os.remove(ZipFilePath)

@qiztxitemcrud.route('/<id>/download/<filename>')
@login_required_auth
def download_file(id,filename):
    book = get_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    #return render_template("view.html", book=book)
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    UPLOAD_FOLDER = os.path.join(path, crspath)
    FilePath=UPLOAD_FOLDER+"/"+filename
    basename, extension = filename.rsplit('.', 1)
    _file=basename.split('-_')[0]+"."+extension    
    return send_file(FilePath,
            mimetype = 'zip',
            attachment_filename= _file,
            as_attachment = True)
    # Delete the zip file if not needed

@qiztxitemcrud.route('/<id>/downloadlecture/<filename>')
@login_required_auth
def download_lecturefile(id,filename):
    book = get_model().read(id)
    crspath=book["Path"]
    #seat=session['profile']['Seat']
    #return render_template("view.html", book=book)
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    UPLOAD_FOLDER = os.path.join(path, crspath+"LECTURE")
    FilePath=UPLOAD_FOLDER+"/"+filename
    basename, extension = filename.rsplit('.', 1)
    _file=basename.split('-_')[0]+"."+extension    
    return send_file(FilePath,
            mimetype = 'zip',
            attachment_filename= _file,
            as_attachment = True)
    # Delete the zip file if not needed

@qiztxitemcrud.route('/<id>/img/<filename>')
def showimage(id,filename):
    # Get current path os.getcwd()
    path = current_app.config['HW_UPLOAD_FOLDER']
    # file Upload
    #UPLOAD_FOLDER = os.path.join(path, filename)
    FilePath=path+"/"+filename
    return send_file(FilePath,
            mimetype = 'image/*')
    # Delete the zip file if not needed

@qiztxitemcrud.route('/<id>/upload', methods=['GET', 'POST'])
@login_required_auth
def uploadfiles(id):
    book = get_model().read(id)
    crspath=book["Path"]
    seat=session['profile']['Seat']
    classno=session['profile']['Classno']
    path = current_app.config['HW_UPLOAD_FOLDER']
    LECTURE_FOLDER = os.path.join(path, crspath+"LECTURE")
    if not os.path.isdir(LECTURE_FOLDER):
        os.mkdir(LECTURE_FOLDER)
    UPLOAD_FOLDER = os.path.join(path, crspath)
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if session['profile']['Role']=="1":
        UPLOAD_FOLDER=LECTURE_FOLDER
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return render_template("view.html", book=book)
        files = request.files.getlist('files[]')
        for file in files:
            upload_hw_file(file,UPLOAD_FOLDER,f"{classno}{seat}")
        flash('File(s) successfully uploaded')
        return redirect(f"/classwork/{id}")
        #return render_template("view.html", book=book)




@qiztxitemcrud.route('/<id>/cleanclasswork')
@login_required_auth
def cleanclasswork(id):
    book = get_model().read(id)
    crspath=book["Path"]
    if (book["createbyid"]==str(session['profile']['id']))  :
        path = current_app.config['HW_UPLOAD_FOLDER']
        UPLOAD_FOLDER = os.path.join(path, crspath)
        for root,dirs, files in os.walk(UPLOAD_FOLDER):
           for file in files:      
               os.remove(UPLOAD_FOLDER+"/"+file)
        #get_model().delete(id)        
    return redirect(url_for('.list'))
