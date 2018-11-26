from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPersmission(object):
    # 255的二进制方式 1111 1111
    All_Persmission = 0b11111111  # 255
    # 访问权限
    Visitor = 0b00000001  # 1
    # 管理帖子权限
    POSTOR = 0b00000010  # 2
    # 管理评论的权限
    COMMENTER = 0b00000100  # 4
    # 管理板块的权限
    BORDER = 0b00001000  # 8
    # 管理前台用户的权限
    FRONTUSER = 0b00010000  # 16
    # 管理后台用户的权限
    CMSUSER = 0b00100000  # 32
    # 管理后台的管理员的权限
    CMSUSER_Admin = 0b01000000


cms_role_user = db.Table(
    'cms_user_role',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id')),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'))
)


# 角色
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPersmission.Visitor)
    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')


#
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
        self.password = password  # 这是方法password
        self.email = email

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

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_per = 0
        for role in self.roles:
            permission = role.permissions
            all_per |= permission
        return all_per

    def has_perssion(self, per):
        # all_perssions=self.permissions
        # if per & all_perssions==per:
        #     return  True
        return self.permissions & per == per

    @property
    def is_developer(self):
        return self.has_perssion(CMSPersmission.All_Persmission)


# 密码对外的字段是password ,对内是下划线_password

# 轮播图
class Banner(db.Model):
    __tablename__ = 'cms_banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    weight_url = db.Column(db.Integer, default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)
