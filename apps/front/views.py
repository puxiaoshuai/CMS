from flask import (Blueprint, redirect, url_for, session,
                   render_template, make_response, request, flash,
                   views)
from io import BytesIO
from .decorators import login_required
import config
from exts import db
from utils.captcha import Captcha
from ..front.forms import RegistFrontForm, LoginFrontForm
from .models import FrontUser

front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    return render_template('front/front_index.html')


@front_bp.route("/logout/")
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.sign_in'))


class LoginFrontView(views.MethodView):
    def get(self):
        return render_template('front/front_signin.html')

    def post(self):
        loginForm = LoginFrontForm(request.form)
        if loginForm.validate():
            tel = loginForm.telephone.data
            pwd = loginForm.password.data
            rember = loginForm.remember.data
            user = FrontUser.query.filter_by(telephone=tel).first()
            if user:
                if user.check_pwd(pwd=pwd):
                    # 保存用户信息
                    session[config.FRONT_USER_ID] = user.id
                    if rember:
                        # 设置缓存时间
                        session.permanent = True
                    return redirect(url_for("front.index"))
                else:
                    flash("密码不对，请重新输入密码")
                    return self.get()
            else:
                flash("该号码没注册，请去注册")
                return self.get()
        else:
            flash(loginForm.get_error())
            return self.get()


@front_bp.route("/captcha/")
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


class RegistView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        registForm = RegistFrontForm(request.form)
        # 如果验证通过
        if registForm.validate():
            tel = registForm.telephone.data
            username = registForm.username.data
            pwd = registForm.password1.data
            # 先查询当前有无这个手机号码，有表示注册了
            user = FrontUser.query.filter_by(telephone=tel).first()
            if user:
                flash("该手机号码已经被注册了哦")
                return self.get()
            else:
                newUser = FrontUser()
                newUser.telephone = tel
                newUser.username = username
                newUser.password = pwd
                db.session.add(newUser)
                db.session.commit()
                flash("恭喜，注册成功")
                return redirect(url_for('front.sign_in'))
        else:
            flash(registForm.get_error())
            return self.get()


front_bp.add_url_rule('/sign_up/', endpoint="sign_up", view_func=RegistView.as_view('sign_up'))
front_bp.add_url_rule('/sign_in/', endpoint='sign_in', view_func=LoginFrontView.as_view('sign_in'))
