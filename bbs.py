from flask import Flask
from apps.cms import cms_bp
from apps.common import common_bp
from apps.front import front_bp
import config
from exts import db,mail
from  flask_wtf import CSRFProtect




def create_app():
    app = Flask(__name__)
    #绑定了配置文件
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    db.init_app(app)
    CSRFProtect(app)
    mail.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=1113,debug=True)
