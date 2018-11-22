from wtforms import Form


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message
    # {'email': ['请输入正确的邮箱'], 'password': ['请输入正确的密码']}
    # popitem() 方法随机返回并删除字典中的一对键和值(),结果是元组（"email",["xx"]）
    # [1]获取元组中的第2个值，第一个值是数组，所用用[0]
