from flask import (Blueprint,
                   render_template,
                   views)

front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    return "front"




class RegistView(views.MethodView):
    def get(self):
        return render_template('front/front_regist.html')


front_bp.add_url_rule('/sign_up/', endpoint="sign_up", view_func=RegistView.as_view('sign_up'))
