# 每次请求之前，查看是session是否有user_id,有的话表明已经等了
from apps.front import front_bp
from .views import cms_bp
import config
from flask import session, g, render_template
from .models import CMSUser, CMSPersmission


@cms_bp.before_request
def before_app_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


@cms_bp.context_processor
def cms_context():
    return {"CMSPersmission": CMSPersmission}


@front_bp.errorhandler(404)
def page_not_found():
    return render_template('front/front_404.html'), 404
