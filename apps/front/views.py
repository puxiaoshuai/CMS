from flask import (Blueprint, redirect, url_for, session,
                   render_template, make_response, request, flash,
                   views, g)
from io import BytesIO
from .decorators import login_required
import config
from exts import db
from utils.captcha import Captcha
from ..front.forms import RegistFrontForm, LoginFrontForm, AddPostForm
from ..common.models import PostModel
from .models import FrontUser
from ..cms import Banner
from ..common.models import BoardModel
from utils import resful

front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    banners = Banner.query.order_by(Banner.weight_url.desc()).all()
    boards = BoardModel.query.all()
    content = {
        'banners': banners,
        'boards': boards
    }
    return render_template('front/front_index.html', **content)


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


@front_bp.route('/apost/', methods=["GET", "POST"])
@login_required
def apost():
    if request.method == "GET":
        boards=BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return resful.params_error("没有这个版块")
            post = PostModel(title=title, content=content)
            post.board = board
            post.author_id=g.front_user.id
            db.session.add(post)
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error(form.get_error())
