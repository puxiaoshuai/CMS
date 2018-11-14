# 每次请求之前，查看是session是否有user_id,有的话表明已经等了
from .views import cms_bp
import config
from flask import session, g
from .models import CMSUser


@cms_bp.before_request
def before_app_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user
