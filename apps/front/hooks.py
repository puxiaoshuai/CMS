from .views import front_bp
import config
from  flask import session,g,render_template
from .models import FrontUser
@front_bp.before_app_request
def before_app_request():
    if config.FRONT_USER_ID in session:
        user_id=session.get(config.FRONT_USER_ID)
        uer=FrontUser.query.get(user_id)
        if uer:
            g.front_user=uer

