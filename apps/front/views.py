from flask import (Blueprint, redirect, url_for, session,
                   render_template, make_response, request, flash,
                   views, g, abort)
from io import BytesIO

from sqlalchemy import func

from .decorators import login_required
import config
from exts import db
from utils.captcha import Captcha
from ..front.forms import RegistFrontForm, LoginFrontForm, AddPostForm, AddCommentForm
from ..common.models import PostModel
from ..cms.models import HighlightPostModel
from .models import FrontUser, CommentModel
from ..cms import Banner
from ..common.models import BoardModel
from utils import resful
from flask_paginate import Pagination, get_page_parameter

front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    ##前端点击链接，给后台返回，板块的id,设置的排序sort,
    #后台根据得到的bd,st来查询数据，并且把，获取到的值也传给前端，这样子，循环形成整体
    board_id = request.args.get('bd', type=int, default=None)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sort = request.args.get("st", type=int, default=1)
    banners = Banner.query.order_by(Banner.weight_url.desc()).all()
    boards = BoardModel.query.all()
    start = (page - 1) * config.PAGE_SIZE
    end = start + config.PAGE_SIZE
    posts = None
    total = 0
    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精时间倒叙,没加精的，按照时间倒叙
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.crete_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 查询帖子，并加入评论，用帖子id分组，进行数量的排序，
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    if board_id:
        query_obj = query_obj.filter(PostModel.board_id == board_id)
        posts = query_obj.slice(start, end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start, end)  # 注意不能加.all()  .order_by(PostModel.create_time.desc())
        total = query_obj.count()
    pagination = Pagination(bs_version=4, page=page, total=total)

    content = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
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
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
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
            post.author_id = g.front_user.id
            db.session.add(post)
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error(form.get_error())


@front_bp.route('/p/<post_id>/')
@login_required
def p_details(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template('front/front_pdetail.html', post=post)


@front_bp.route("/acomment/", methods=["POST"])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        conment = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=conment)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return resful.success()
        else:
            return resful.params_error()
    else:
        return resful.params_error(form.get_error())
