
import os
IndexURL="http://localhost:83/trythisapps"
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
SECRET_KEY = 'catcatcat'
SESSION_COOKIE_NAME='connect.sid'
SESSION_TYPE = 'filesystem'  # session类型为redis
SESSION_USE_SIGNER = True  # 是否对发送到浏览器上session的cookie值进行加密
SESSION_KEY_PREFIX = 'sess:'  # 保存到session中的值的前缀
SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效。
#SESSION_REDIS = redis.Redis(host='127.0.0.1',port=app.config["REDIS_PORT"])  
#Set Image Path
UPLOAD_FOLDER=os.getcwd()+"\\TEMP"

#6379  not need
REDIS_PORT=6378

SQLITE_PATH=os.getcwd()+"\\bookshelf.db"
SQLALCHEMY_DATABASE_URI = ( 'sqlite:///{path}').format(path=SQLITE_PATH)

records = [
  { "id":1,"user":"aa","Pass":"123","Name":"之","Classno":"南北朝","Seat":"500","Role":"1", "displayName":"Zu"}  ,
  { "id":2,"user":"bb","Pass":"123","Name":"之","Classno":"南北朝","Seat":"500","Role":"1", "displayName":"Zu"}  
]
