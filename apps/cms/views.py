from flask import Blueprint, views, render_template, request, session,redirect,url_for
from .forms import LoginForm
from .models import CMSUser
from  .decorators import login_requied
import config

cms_bp = Blueprint("cms", __name__, url_prefix='/cms')


@cms_bp.route('/')
@login_requied
def index():
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

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
            #{'email': ['请输入正确的邮箱'], 'password': ['请输入正确的密码']}
            # popitem() 方法随机返回并删除字典中的一对键和值(),结果是元组（"email",[]）
            #[1]获取元组中的第2个值，第一个值是数组，所用用[0]
            print(form.errors.popitem())
            message=form.errors.popitem()[1][0]
            return self.get(message=message)


cms_bp.add_url_rule('/login/', endpoint='login', view_func=LoginView.as_view('login'))
