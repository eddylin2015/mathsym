
import os

MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

SECRET_KEY = '123'
SESSION_COOKIE_NAME='connect.sid'

#Set Image Path
UPLOAD_FOLDER=os.getcwd()+"\\TEMP"

#6379  not need
REDIS_PORT=6378

SQLITE_PATH=os.getcwd()+"\\bookshelf.db"
SQLALCHEMY_DATABASE_URI = ( 'sqlite:///{path}').format(path=SQLITE_PATH)


