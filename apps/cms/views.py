import random

from flask import (Blueprint, views, render_template, request,
                   session, redirect, url_for, g, jsonify)

from exts import db, mail
from utils import resful, zlcache
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .models import CMSUser,CMSPersmission
from .decorators import login_requied,permission_requied
from flask_mail import Message
import string
import config

cms_bp = Blueprint("cms", __name__, url_prefix='/cms')


@cms_bp.route('/')
@login_requied
def index():
    return render_template('cms/cms_index.html')


@cms_bp.route('/logout/')
@login_requied
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 个人中心界面
@cms_bp.route('/profile/')
@login_requied
def profile():
    return render_template('cms/cms_profile.html')


# 帖子模块
@cms_bp.route("/posts/")
@login_requied
@permission_requied(CMSPersmission.POSTOR)
def posts():
    return render_template('cms/cms_posts.html')


# 评论模块
@cms_bp.route("/comments/")
@login_requied
@permission_requied(CMSPersmission.COMMENTER)
def commment():
    return render_template('cms/cms_comments.html')


# 版块管理
@cms_bp.route("/boards/")
@login_requied
@permission_requied(CMSPersmission.BORDER)
def boards():
    return render_template('cms/cms_borders.html')


# 前台用户管理
@cms_bp.route("/users/")
@login_requied
@permission_requied(CMSPersmission.FRONTUSER)
def users():
    return render_template('cms/cms_userfront.html')


# 后台用户管理
@login_requied
@permission_requied(CMSPersmission.CMSUSER)
@cms_bp.route("/cms_usermanage/")
def cms_usermanage():
    return render_template('cms/cms_userback.html')


# 后台用户z组管理
@cms_bp.route("/cms_usergroup/")
@login_requied
@permission_requied(CMSPersmission.CMSUSER_Admin)
def cms_usergroup():
    return render_template('cms/cms_usergroup.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_pwd(password):
                # 如果有这个用户，并且密码是正确的的,保存用户登录信息
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True  # 默认31天，设置长点
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱或者密码错误")
        else:
            # {'email': ['请输入正确的邮箱'], 'password': ['请输入正确的密码']}
            # popitem() 方法随机返回并删除字典中的一对键和值(),结果是元组（"email",[]）
            # [1]获取元组中的第2个值，第一个值是数组，所用用[0]
            print(form.errors.popitem())
            return self.get(message=form.get_error())


class ResetPwdView(views.MethodView):
    decorators = [login_requied]

    def get(self, message=None):
        return render_template('cms/cms_modifpwd.html', message=message)

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.old_pwd.data
            newpwd = form.new_pwd.data
            user = g.cms_user
            if user.check_pwd(oldpwd):
                user.password = newpwd
                db.session.commit()
                ###{"code":200,message:"修改成功",}
                return resful.success(message="密码修改成功")
            else:
                return resful.params_error("旧密码错误")
        # 给android，ios写后台用restful更合适
        else:
            return resful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_requied]

    def get(self):
        return render_template('cms/cms_modifyemail.html')

    def post(self):
        # 获取邮箱和验证码
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email == email
            db.session.commit()
            return resful.success("修改成功")
        else:
            return resful.params_error(form.get_error())


#
# @cms_bp.route("/email/")
# def send_eamil():
#     message = Message("测试邮件的发送", recipients=['1223765504@qq.com'])
#     message.body='数据测试'
#     message.html='<h1>哈哈哈哈</h1>'
#     mail.send(message)
#
#     return "发送邮件"
@cms_bp.route('/email_captcha/')
def email_captcha():
    # /email_captcha/?email=xx.com
    email = request.args.get('email')
    if not email:
        return resful.params_error("请传递邮箱参数")
    source = list(string.ascii_letters)  # ['a','b'..z ..Z]
    source.extend(map(lambda x: str(x), range(0, 10)))
    # source.extend(["0","1","2","3","4","5","6","7","8","9"])
    # 随机采用
    yanzhengma = "".join(random.sample(source, 6))
    message = Message("趣论坛验证码", recipients=[email])
    message.body = '您的验证码是 %s,请复制验证码到网址进行邮箱修改' % yanzhengma
    message.html = '<h3>您的验证码是 %s,请复制验证码到网址进行邮箱修改</h3>' % yanzhengma
    try:
        mail.send(message=message)
    except:
        return resful.params_error("发送验证码异常")
    ##把邮箱，验证码绑定在一起，60s缓存
    zlcache.set(email, yanzhengma)
    return resful.success("发送成功")


cms_bp.add_url_rule("/resetemail/", endpoint='resetemail', view_func=ResetEmailView.as_view('resetemail'))
cms_bp.add_url_rule('/resetpwd/', endpoint='resetpwd', view_func=ResetPwdView.as_view('resetpwd'))

cms_bp.add_url_rule('/login/', endpoint='login', view_func=LoginView.as_view('login'))
