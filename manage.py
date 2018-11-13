from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from exts import db
from apps.cms import models as cms_models
from bbs import create_app

app = create_app()
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)

CMSUser = cms_models.CMSUser


# 参数名字要对应
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    cms_user = CMSUser(username=username, password=password, email=email)
    db.session.add(cms_user)
    db.session.commit()
    print("CMS用户添加成功")


if __name__ == '__main__':
    manage.run()
