from datetime import datetime

from django.db import models

#insert into axf_wheel(img,name,trackid
from App.app_constants import ORDER_NOT_PAY


class Main(models.Model):
    img = models.CharField(max_length=255, verbose_name='图片链接地址',default=None)
    name = models.CharField(max_length=64, verbose_name='图片名称',default=None)
    trackid = models.CharField(max_length=50, default='1', verbose_name='图片id')

    class Meta:
        abstract = True  # 如果要作为一个父类

    def __str__(self):
        return self.name
class  MainWheel(Main):

    class Meta:
        db_table='axf_wheel'
        verbose_name='轮播图'
        verbose_name_plural=verbose_name

class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'
        verbose_name = '导航表'
        verbose_name_plural = verbose_name

#每日必买
class MainMustBuy(Main):
    class Meta :
        db_table = 'axf_mustbuy'
        verbose_name = '每日必买'
        verbose_name_plural = verbose_name

class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

class MainShow(Main):
    categoryid = models.CharField(max_length=20,verbose_name='分类ID')
    brandname = models.CharField(max_length=50,verbose_name='品牌名')

    img1 = models.CharField(max_length=255,verbose_name='图片1')
    childcid1 = models.CharField(max_length=20,verbose_name='商品1ID')
    productid1 = models.CharField(max_length=20,verbose_name='产品1编号')
    longname1 = models.CharField(max_length=100,verbose_name='商品1名称')
    price1 = models.FloatField(default=1,verbose_name='商品1价格')
    marketprice1 = models.FloatField(default=1,verbose_name='市场价')

    img2 = models.CharField(max_length=255, verbose_name='图片2')
    childcid2 = models.CharField(max_length=20, verbose_name='商品1ID')
    productid2 = models.CharField(max_length=20, verbose_name='产品2编号')
    longname2= models.CharField(max_length=100, verbose_name='商品2名称')
    price2 = models.FloatField(default=1, verbose_name='商品2价格')
    marketprice2 = models.FloatField(default=1, verbose_name='市场价')


    img3 = models.CharField(max_length=255, verbose_name='图片3')
    childcid3 = models.CharField(max_length=20, verbose_name='商品3ID')
    productid3 = models.CharField(max_length=20, verbose_name='产品3编号')
    longname3= models.CharField(max_length=100, verbose_name='商品3名称')
    price3 = models.FloatField(default=1, verbose_name='商品3价格')
    marketprice3 = models.FloatField(default=1, verbose_name='市场价')

    class Meta:
        db_table = 'axf_mainshow'
        verbose_name = '商品展示'
        verbose_name_plural = verbose_name

class MainFoodTypes(models.Model):
    typeid = models.IntegerField(default=1,verbose_name='产品类型ID')
    typename = models.CharField(max_length=100,verbose_name='产品名称')
    childtypenames = models.CharField(max_length=255,verbose_name='子类型名称')
    typesort = models.IntegerField(default=1,verbose_name='类型顺序')
    def __str__(self):
        return self.typename

    class Meta:
        db_table = 'axf_foodtypes'
        verbose_name = '食品类型'
        verbose_name_plural=verbose_name

class Goods(models.Model):
    productid = models.IntegerField(default=1)
    productimg  = models.CharField(max_length=255)
    productname  = models.CharField(max_length=255)
    productlongname  = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=80)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=80)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    def __str__(self):
        return self.productname

    class Meta:
        db_table = 'axf_goods'
        verbose_name = '商品信息表'
        verbose_name_plural = verbose_name

class AXFUser(models.Model):
    username = models.CharField(max_length=30,unique=True,)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=50,unique=True)
    uicon = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'axf_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

class Cart(models.Model):
    user = models.ForeignKey(AXFUser,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table='cart'
        verbose_name='购物车'
        verbose_name_plural = verbose_name

class Order(models.Model):
    o_user = models.ForeignKey(AXFUser,on_delete=models.CASCADE)
    o_price = models.FloatField(default=0)
    o_time = models.DateTimeField(default=datetime.now)
    o_status = models.IntegerField(default=ORDER_NOT_PAY)

    def __str__(self):
        return self.o_user

    class Meta:
        db_table = 'axf_order'
        verbose_name = '订单表'
        verbose_name_plural=verbose_name

class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order,on_delete=models.CASCADE)
    o_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    o_goods_num = models.IntegerField(default=1)
    def __str__(self):
        return self.o_order_id
    class Meta:
        db_table = 'axf_ordergoods'
        verbose_name = '订单商品表'
        verbose_name_plural= verbose_name




