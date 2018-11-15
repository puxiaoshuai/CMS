from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from exts import db
import shortuuid
import enum


class GenderEnum(enum.Enum):
    MAIL = 1,
    FEMAIL = 2,
    SECRET = 3,
    UNKONE = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)  # 自增长对商业信息不好，使用唯一字符串，shortuuid
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKONE)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 为了命令行中，_password找不到
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(FrontUser,self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        # 进行加密
        self._password = generate_password_hash(raw_pwd)

    def check_pwd(self, pwd):
        # 界面并对照
        result = check_password_hash(self.password, pwd)
        return result
