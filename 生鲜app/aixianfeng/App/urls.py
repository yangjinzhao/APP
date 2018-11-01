"""aixianfeng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App.views import *
app_name='App'
urlpatterns = [
    path('',index,name='index'),
    path('market/',show_market,name='show_market'),
    path('mine/',show_mine,name='show_mine'),
    path('login/',user_login,name='user_login'),
    path('register/', user_register, name=' user_register'),
    path('checkname/',check_username,name='check_username'),
    path('active/',user_active,name= 'user_active'),
    path('logout/',user_logout,name = 'user_logout'),
    path('cart/',show_cart,name='show_cart'),
    path('addCart/',add_cart,name='add_cart'),
    path('subCart/',sub_cart, name='sub_cart'),
    path('changecartstate/',change_cart_state,name='change_cart_state'),
    path('subshopping/',sub_shopping,name='sub_shopping'),
    path('addshopping/',add_shopping, name='add_shopping'),
    path('makeorder',make_order,name='make_order'),
    path('allselect/', all_select, name='all_select'),
    path('unallselect/',unall_select, name='unall_select'),



]
