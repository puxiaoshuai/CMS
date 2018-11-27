from flask import Blueprint, jsonify

common_bp = Blueprint("common", __name__, url_prefix='/common')
import qiniu


@common_bp.route('/')
def index():
    return "common"


@common_bp.route("/uptoken/")
def uptoken():
    access_key = ""
    secret_key = ""
    q = qiniu.Auth(access_key, secret_key)
    bucket = ""
    token = q.upload_token(bucket=bucket)
    return jsonify({"uptoken": token})
