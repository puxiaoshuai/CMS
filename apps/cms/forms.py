from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, length, EqualTo

from ..baseforms import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[length(6, 20, message="请输入正确的密码")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    old_pwd = StringField(validators=[length(6, 20, message="请输入正确的旧密码")])
    new_pwd = StringField(validators=[length(6, 20, message="请输入正确的新密码")])
    sure_pwd = StringField(validators=[EqualTo('new_pwd', message="新密码两次不一致")])
