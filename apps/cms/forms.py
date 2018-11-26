from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, length, EqualTo
from flask import g
from ..baseforms import BaseForm

from utils import zlcache


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的邮箱"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[length(6, 20, message="请输入正确的密码")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    old_pwd = StringField(validators=[length(6, 20, message="请输入正确的旧密码")])
    new_pwd = StringField(validators=[length(6, 20, message="请输入正确的新密码")])
    sure_pwd = StringField(validators=[EqualTo('new_pwd', message="新密码两次不一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确的格式的邮箱")])
    captcha = StringField(validators=[length(min=6, max=6, message="验证码长度不对")])

    # 定义这个方法，直接就能进行判断样，很方便，名字要匹配
    def validate_captcha(self, filed):
        yzm = filed.data
        email = self.email.data
        yanzengma_cache = zlcache.get(email)
        if not yanzengma_cache or yzm.lower() != yanzengma_cache().lower():
            raise ValidationError("邮箱验证码错误")

    def validate_eamil(self, filed):
        email = filed.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("不能修改相同的邮箱哟")


class AddbannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图图片链接")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图跳转地址")])
    weight_url = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])
class EditbannerForm(AddbannerForm):
    banner_id=IntegerField(validators=[InputRequired(message="请输入轮播图的ID")])
