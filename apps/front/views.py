from flask import Blueprint

front_bp = Blueprint("front", __name__)


@front_bp.route('/')
def index():
    return "front"
