from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from exts import db
from apps.cms import models as cms_models
from apps.front import models as font_models

from bbs import create_app

app = create_app()
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)
FontUser = font_models.FrontUser
CMSUser = cms_models.CMSUser
CMsRole = cms_models.CMSRole
CMSPerssion = cms_models.CMSPersmission


# 参数名字要对应
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
@manage.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    cms_user = CMSUser(username=username, password=password, email=email)
    db.session.add(cms_user)
    db.session.commit()
    print("CMS用户添加成功")


##测试命令 python manage.py create_cms_user -u 王二麻子  -p 123456 -e 12345678@qq.com


@manage.command
def create_role():
    # 访问者（可以修改个人资料）
    vistor = CMsRole(name="访问者", desc="只能查看，不能修改")
    vistor.permissions = CMSPerssion.Visitor
    # 运营者（修改个人信息，管理帖子，管理评论）
    oparator = CMsRole(name="运营", desc="管理帖子,管理评论,管理前后台用户")
    oparator.permissions = CMSPerssion.Visitor | CMSPerssion.COMMENTER | CMSPerssion.POSTOR | CMSPerssion.FRONTUSER
    # 管理员,拥有绝大部分权限，
    admin = CMsRole(name="管理员", desc="拥有所有权限")
    admin.permissions = CMSPerssion.Visitor | CMSPerssion.POSTOR | CMSPerssion.CMSUSER | CMSPerssion.COMMENTER | CMSPerssion.FRONTUSER | CMSPerssion.BORDER
    # 开发人员
    develpoer = CMsRole(name="开发者", desc="开发人员专用角色")
    develpoer.permissions = CMSPerssion.All_Persmission
    db.session.add_all([vistor, oparator, admin, develpoer])
    db.session.commit()


# 以前的用户是没添加权限的，所有还的增加权限
@manage.command
def test_permission():
    user = CMSUser.query.first()
    if user.is_developer:
        print("这个用户有访问者的权限")
    else:
        print("这个用户没有访问者的权限")


@manage.option('-e' '--email', dest='email')
@manage.option('-n', '--name', dest='name')  # 角色名
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMsRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加角色成功")
        else:
            print("没有这个角色")

    else:
        print("该邮箱没注册")


# python manage.py add_user_to_role -e 1234578@qq.com -n 访问者

@manage.option('-t', '--telephone', dest='telephone')
@manage.option('-u', '--username', dest='username')
@manage.option('-p', '--password', dest='password')
def create_fontuser(telephone, username, password):
    font_user = FontUser(telephone=telephone, username=username, password=password)
    db.session.add(font_user)
    db.session.commit()


# python manage.py create_fontuser -t 18381021332 -u 周冬冬 -p 123456


if __name__ == '__main__':
    manage.run()
