from flask import Blueprint

common_bp = Blueprint("common", __name__, url_prefix='/common')


@common_bp.route('/')
def index():
    return "common"
