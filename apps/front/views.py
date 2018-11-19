from flask import (Blueprint,
                   render_template,make_response,
                   views)
from io import BytesIO
from  utils.captcha import Captcha
front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    return "front"

@front_bp.route("/captcha/")
def graph_captcha():
    text,image=Captcha.gene_graph_captcha()
    out=BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type='image/png'
    return resp




class RegistView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')


front_bp.add_url_rule('/sign_up/', endpoint="sign_up", view_func=RegistView.as_view('sign_up'))
