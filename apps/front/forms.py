from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import InputRequired, length, EqualTo, DataRequired
from ..baseforms import BaseForm


class RegistFrontForm(BaseForm):
    telephone = StringField(DataRequired("请输入手机号码"), validators=[length(6, 11, message="请输入正确的手机号")])
    username = StringField(validators=[length(min=2, message="取个长点的用户名吧")])
    password1 = StringField(validators=[length(6, 12, message="密码长度6-12")])
    password2 = StringField(validators=[EqualTo('password1', message="两次密码长度不一致哦")])


class LoginFrontForm(BaseForm):
    telephone = StringField(validators=[length(6, 11, message="请输入正确的手机号码")])
    password = StringField(validators=[length(6, 12,message="密码长度6-12位")])
    remember = IntegerField()
