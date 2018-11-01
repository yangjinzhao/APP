from django.forms import Form
from django.forms import fields,widgets
class UserRegisterForm(Form):
    username = fields.CharField(max_length=30,min_length=2,error_messages={'required':'用户名必须填写',
                                                              'max_length':'用户名不能超过30位',
                                                                           'min_length':'用户名不能少于2位'})
    password = fields.CharField(max_length=16, min_length=6, error_messages={'required': '密码必须填写',
                                                                             'max_length': '密码不能超过16位',
                                                                             'min_length': '密码不能少于6位'})
    repassword = fields.CharField(max_length=16, min_length=6, error_messages={'required': '确认密码必须填写',
                                                                             'max_length': '确认密码不能超过16位',
                                                                             'min_length': '确认密码不能少于6位'})
    email = fields.EmailField(error_messages={'required':'邮箱必须填写','validators':'邮箱格式错误'})
    uicon = fields.ImageField()

class UserLoginForm(Form):
    username = fields.CharField(max_length=30,min_length=2,error_messages={'required':'用户名必须填写',
                                                              'max_length':'用户名不能超过30位',
                                                                           'min_length':'用户名不能少于2位'})
    password = fields.CharField(max_length=16, min_length=6, error_messages={'required': '密码必须填写',
                                                                             'max_length': '密码不能超过16位',
                                                                             'min_length': '密码不能少于6位'})

