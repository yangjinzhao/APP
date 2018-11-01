from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from App.models import AXFUser
from django.shortcuts import redirect,reverse
#JSON 请求路径列表
LOGIN_JSON_PATH = [
    '/app/addCart/',
    '/app/subCart/',
    '/app/changecartstate/',
    '/app/subshopping/',
    '/app/addshopping/',
    '/app/allselect/',
    '/app/unallselect/',

]
#普通request 请求的路径列表
LOGIN_PATH = [
'/app/cart/',
    '/app/makeorder/',
]
class LoginMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        if request.path in LOGIN_JSON_PATH:

            username=request.session.get('username','')
            if username:
                user=AXFUser.objects.filter(username=username)
                if user.exists():
                    request.user = user.first()
                else:
                    return JsonResponse({'status':'fail','msg':'用户不存在'})
            else:
                return JsonResponse({'status':'fail','msg':'用户未登录'})


        if request.path in LOGIN_PATH:
            username = request.session.get('username', '')
            if username:
                user = AXFUser.objects.filter(username=username)
                if user.exists():
                    request.user = user.first()
                else:
                    return redirect(reverse('app:user_login'))
            else:
                 return redirect(reverse('app:user_login'))

