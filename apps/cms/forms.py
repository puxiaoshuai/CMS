from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, length


class LoginForm(Form):
    email = StringField(validators=[Email(message="请输入正确的邮箱"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[length(6, 20, message="请输入正确的密码")])
    remember = IntegerField()
