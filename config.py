import os

DEBUG = True
SECRET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'cms'
USENAME = 'root'
PASSWORD = 'puhao'
DB_URI = "mysql://{}:{}@{}:{}/{}?charset=utf8".format(USENAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
####常量
CMS_USER_ID = 'CMS_USER_ID'
# 邮箱常量
# 发送邮箱的服务器地址
MAIL_SERVER = 'smtp.qq.com'
# 端口号,
MAIL_PORT = "587"
MAIL_USE_TLS = True
# MAIL_USE_SSL :  False

MAIL_USERNAME = '1372553910@qq.com'
MAIL_PASSWORD = 'tsnmmzpprcfyjabc'
MAIL_DEFAULT_SENDER = '1372553910@qq.com'
