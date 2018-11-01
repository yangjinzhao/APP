import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,reverse
from django.template import loader

from App.app_constants import *
from App.models import *
from aixianfeng.settings import DEFAULT_FROM_EMAIL
from .forms import UserRegisterForm,UserLoginForm
from users.models import *
def index(request):
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shop_goods = MainShop.objects.all()
    shop_goods_1 = shop_goods[0:1]
    shop_goods_1_3 = shop_goods[1:3]
    shop_goods_3_7 = shop_goods[3:7]
    shop_goods_7_11 = shop_goods[7:11]
    mainshows=MainShow.objects.all()

    return  render(request,'main/home.html',{'wheels':wheels,'navs':navs,'title':'首页','mustbuys':mustbuys,
                                             'shop_goods_1':shop_goods_1,'shop_goods_1_3':shop_goods_1_3,
                                             ' shop_goods_3_7': shop_goods_3_7,' shop_goods_7_11': shop_goods_7_11,
                                             'mainshows':mainshows})
#闪购
def show_market(request):

    foodtypes=MainFoodTypes.objects.all()
    foodtype_childname_list = []
    typeid= request.GET.get('typeid','103541')
    childid = request.GET.get('childid','0')
    rule_sort= request.GET.get('sort','0')
    order_list = [
       ["综合排序",ORDER_TOTAL] ,
        ['价格升序',ORDER_PRICE_UP],
        ['价格降序',ORDER_PRICE_DOWN],
        ['销量升序',ORDER_SALE_UP],
        ['销量降序',ORDER_SALE_DOWN]
    ]
    if typeid:
        goods_list = Goods.objects.filter(categoryid=typeid)
        if childid=='0':
            pass
        else:
            goods_list = Goods.objects.filter(categoryid=typeid,childcid=childid)
        if rule_sort ==ORDER_TOTAL:
            pass
        elif rule_sort == ORDER_PRICE_UP:
            goods_list = goods_list.order_by('price')
        elif rule_sort == ORDER_PRICE_DOWN:
            goods_list = goods_list.order_by('-price')
        elif rule_sort == ORDER_SALE_UP:
            goods_list = goods_list.order_by('productnum')
        elif rule_sort == ORDER_SALE_DOWN:
            goods_list = goods_list.order_by('-productnum')
        foodtype= MainFoodTypes.objects.get(typeid=typeid)
        foodtypechildnames_list = foodtype.childtypenames.split('#')
        for childname in foodtypechildnames_list:
            foodtype_childname_list.append(childname.split(':'))

    return render(request,'main/market.html',{'foodtypes': foodtypes,
                                              'goods_list':goods_list,'foodtype_childname_list':foodtype_childname_list,
                                              'typeid':int(typeid),'childid':childid,'order_list':order_list,
                                             'rule_sort':rule_sort,})

#我的
def show_mine(request):
    username=request.session.get('username','')
    if username:
        user=AXFUser.objects.get(username=username)
        return render(request, 'main/mine.html',{'user':user})
    else:
        return render(request,'main/mine.html',{'user':''})

def user_login(request):
    if request.method =='GET':
        return render(request,'user/login.html',{'title':'登录'})
    else:
        user_login_form =UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']

            user = AXFUser.objects.filter(username=username)
            if user.exists():
                user = user.first()
                if user.is_active:
                    if check_password(password,user.password):
                        request.session['username'] = username
                        return  redirect(reverse('app:show_mine'))
                    else:
                        return render(request,'user/login.html',{'title':'登录','msg':'密码不正确'})
                else:
                    return render(request,'user/login.html',{'title':'登录','msg':'用户名未被激活，请赶紧到邮箱激活'})

        else:
            return render(request,'user/login.html',{'user_loginform':user_login_form,'title':'登录'})
def user_register(request):
    if request.method == 'GET':

        return render(request,'user/register.html',{'title':'用户注册'})

    else:
        user_register_form = UserRegisterForm(request.POST,request.FILES)
        if user_register_form.is_valid():
            datas = user_register_form.cleaned_data
            if datas['password']  == datas['repassword']:
                user = AXFUser()
                user.username = datas['username']
                password = datas['password']
                password = make_password(password)
                user.password = password
                user.email = datas['email']
                user.uicon = datas['uicon']
                user.save()

                #发送邮件

               # message = '<a herf = "#">激活</a>'
                u_token = uuid.uuid4().hex
                '设置u_token 和用户名进行绑定'
                cache.set(u_token,user.username,timeout=60*60*24)
                data = {
                    'username': user.username,
                    'active_url': 'http://127.0.0.1:8000/app/active',
                    'u_token': u_token  # 27fd7800670e4c78b8189bc4dfb061d7
                }
                message=loader.get_template('user/active.html').render(data)
                send_mail('爱鲜蜂用户激活',message,DEFAULT_FROM_EMAIL,[user.email,],html_message=message)

                return redirect(reverse('app:user_login'))

            else:
                return render(request,'user/register.html',{'title':'用户注册','msg':'密码不一致'})

        else:
            return render(request,'user/register.html',{'user_register_form':user_register_form})


def check_username(request):
    username= request.GET.get('username')
    result=AXFUser.objects.filter(username=username)
    if result.exists():
        return JsonResponse({"status":'fail','msg':'用户名已存在'})

    else:
        return JsonResponse({"status": 'ok', 'msg': '用户名可用'})

def user_active(request):
    u_token = request.GET.get('u_token')
    value=cache.get(u_token)
    user=AXFUser.objects.filter(username=value).first()
    user.is_active=True
    user.save()
    return redirect(reverse('app:user_login'))

def user_logout(request):
    request.session.flush()
    return redirect(reverse('app:show_mine'))

def show_cart(request):

        cart_goods=Cart.objects.filter(user_id=request.user.id)
        total_price = get_totalprice(request)
        return render(request,'main/cart.html',{'cart_goods':cart_goods,'total_price':total_price})

def add_cart(request):

        gid = request.GET.get('gid','')
        goods = Goods.objects.get(pk = gid)
        carts=Cart.objects.filter(user_id=request.user.id).filter(goods_id=goods.id)
        if carts.exists():
            cart = carts.first()
            cart.goods_num+=1
        else:
            cart = Cart()
            cart.goods = goods
            cart.user = request.user
        cart.save()
        datas={
                'status': 'ok',
                'goods_num':cart.goods_num
            }
        return JsonResponse(datas)
def sub_cart(request):
    gid = request.GET.get('gid', '')
    goods = Goods.objects.get(pk=gid)
    carts = Cart.objects.filter(user_id=request.user.id).filter(goods_id=goods.id)
    if carts.exists():
        cart = carts.first()
        if cart.goods_num>=1:
            cart.goods_num -= 1
    else:
        cart = Cart()
        cart.goods_num = 0
        cart.goods = goods
        cart.user = request.user
    cart.save()
    datas = {
        'status': 'ok',
        'goods_num': cart.goods_num
    }
    return JsonResponse(datas)
#商品总价
def get_totalprice(request):
        carts= Cart.objects.filter(user=request.user).filter(is_select=True)
        total_price = 0
        for goods in carts:
            price= goods.goods.price
            num = goods.goods_num
            t_price = price * num
            total_price+=t_price

        return  total_price


def change_cart_state(request):
    cartid=request.GET.get('cartid')
    cart=Cart.objects.get(pk=cartid)
    cart.is_select = not cart.is_select
    cart.save()
    #print(cart.is_select)
    return JsonResponse({'status': 'ok', 'is_select': cart.is_select, 'total_price': get_totalprice(request)})

def sub_shopping(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk = cartid)
    datas ={}
    if cart.goods_num>1:
        cart.goods_num -=1
        cart.save()
        datas['cart_goods_num']  = cart.goods_num
    else:
        cart.delete()
        datas['cart_goods_num'] = 0
    datas['status'] =  'ok'
    datas['total_price'] = get_totalprice(request)

    return JsonResponse(datas)

def add_shopping(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    if cart:
        cart.goods_num = cart.goods_num + 1
        cart.save()
        return JsonResponse({'status': 'ok', 'cart_goods_num': cart.goods_num, 'total_price': get_totalprice(request)})

def all_select(request):
    carts = Cart.objects.filter(user=request.user).filter(is_select=False)
    for cart in carts:
        cart.is_select = not cart.is_select
        cart.save()
    return  JsonResponse({'status': 'ok', 'total_price': get_totalprice(request)})

# 购物车商品的取消全选操作


def unall_select(request):
    carts = Cart.objects.filter(user=request.user).filter(is_select=True)
    #print(carts)
    for cart in carts:
        cart.is_select = not cart.is_select
        cart.save()
    return JsonResponse({'status': 'ok', 'total_price': get_totalprice(request)})

def make_order(request):

    carts = Cart.objects.filter(user = request.user).filter(is_select=True)
    order = Order()
    order.o_user = request.user
    order.o_price = get_totalprice(request)
    order.save()
    for cart in carts:
      ordergoods = OrderGoods()
      ordergoods.o_order = order
      ordergoods.o_goods = cart.goods
      ordergoods.save()
      return HttpResponse('SS')