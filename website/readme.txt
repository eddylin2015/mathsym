config__.py replace config.py


# config.py  (local evn)
import os
IndexURL="http://d8.mbc.edu.mo:83/trythisapps"
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
SECRET_KEY = 'catcatcat'
SESSION_COOKIE_NAME='connect.sid'
SESSION_TYPE = 'filesystem'   # session类型为redis
SESSION_USE_SIGNER = True     # 是否对发送到浏览器上session的cookie值进行加密
SESSION_KEY_PREFIX = 'sess:'  # 保存到session中的值的前缀
SESSION_PERMANENT = False     # 如果设置为True，则关闭浏览器session就失效。
UPLOAD_FOLDER=os.getcwd()+"\\TEMP"
#6379  not need
REDIS_PORT=6378
SQLITE_PATH=os.getcwd()+"\\bookshelf.db"
SQLALCHEMY_DATABASE_URI = ( 'sqlite:///{path}').format(path=SQLITE_PATH)
records = [ { "id":1,"user":"abc","Pass":"123","Name":"","Classno":"","Seat":"","Role":"9", "displayName":"Zu"}]
# end config.py

# config.py (serv env)

import os
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER="/IMAGEPATH/"
SECRET_KEY = '123'
SESSION_COOKIE_NAME='connect.sid'
DATA_BACKEND = 'mysql'
MYSQL_HOST='127.0.0.1'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'bookshelf'
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@{host}:3306/{database}').format(
        user=MYSQL_USER, password=MYSQL_PASSWORD,host=MYSQL_HOST,
        database=MYSQL_DATABASE)
records = [{ "id":1,"user":"abc","Pass":"123","Name":"","Classno":"","Seat":"500","Role":"1", "displayName":"Zu"}]
#end config.py



#mysql
my.ini
[mysqld]
basedir=c:/appserv/mysql
datadir=c:/appserv/mysql/data
[mysqld-8.0]
sql_mode=TRADITIONAL

bin\mysqld --defaults-file=my.ini --initialize --console
A temporary password is generated for root@localhost: qk-nm1!hE/4r

mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '新密碼';

#redis
https://github.com/microsoftarchive/redis/releases

#pip install virtualenv
virtualenv --python "c:\python36\python.exe" env

#pip instal -r requirements.txt
env\scripts\activate
bookshelf>python model_cloudsql.py
python main.py