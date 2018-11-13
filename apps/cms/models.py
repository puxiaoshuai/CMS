from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 为了命令行中，_password找不到
    def __init__(self, username, password, email):
        self.username = username
        self.password = password #这是方法password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        # 进行加密
        self._password = generate_password_hash(raw_pwd)

    def check_pwd(self, pwd):
        #界面并对照
        result = check_password_hash(self.password, pwd)
        return result

# 密码对外的字段是password ,对内是下划线_password
