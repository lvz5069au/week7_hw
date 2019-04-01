from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator

from common.models import Users,Types,Goods,Orders,Detail

# 公共信息加载函数
def loadinfo(request):
    lists = Types.objects.filter(pid=0)
    context = {'typelist':lists}
    return context

def viporders(request):
    '''浏览订单信息'''
    context = loadinfo(request)
    #获取当前登录者的订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id'])
    #遍历订单信息，查询对应的详情信息
    for od in odlist:
        delist = Detail.objects.filter(orderid=od.id)
        #遍历订单详情，并且获取对应的商品信息（图片）
        for og in delist:
            og.picname = Goods.objects.only("picname").get(id=og.goodsid).picname
        od.detaillist = delist

    context['orderslist'] = odlist
    return render(request,"web/viporders.html",context)

def odstate(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")

def info(request):
    context = loadinfo(request)
    #获取当前登录者的个人信息
    user = Users.objects.get(id=request.session['vipuser']['id'])
    context['user'] = user

    return render(request,"web/info.html",context)

def update(request):
    context = loadinfo(request)
    #获取当前登录者的个人信息
    user = Users.objects.get(id=request.session['vipuser']['id'])
    context['user'] = user

    return render(request,"web/update.html",context)

def doupdate(request):
    '''执行修改'''
    context = loadinfo(request)
    #获取当前登录者的个人信息
    ob = Users.objects.get(id=request.session['vipuser']['id'])
    try:
        ob.name=request.POST.get('name')
        ob.sex=request.POST.get('sex')
        ob.address=request.POST.get('address')
        ob.code=request.POST.get('code')
        ob.email=request.POST.get('email')
        ob.save()
        context = {'info':'修改成功！'}
        user = Users.objects.get(id=request.session['vipuser']['id'])
        context['user'] = user
        return render(request,"web/update.html",context)
    except Exception as err:
        print(err)
        context = {'info':'修改失败！'}
        user = Users.objects.get(id=request.session['vipuser']['id'])
        context['user'] = user
        return render(request,"web/update.html",context)

def resetps(request):
    context = loadinfo(request)
    #获取当前登录者的个人信息
    user = Users.objects.get(id=request.session['vipuser']['id'])
    context['user'] = user

    return render(request,"web/resetps.html",context)

def doresetps(request):
    '''执行修改'''
    context = loadinfo(request)
    try:
        #判断两次密码是否正确
        password=request.POST['password']
        repassword=request.POST['repassword']
        if password!=repassword:
            context = {'info':'两次密码不一样！'}
            return render(request,"web/resetps.html",context)
        ob = Users.objects.get(id=request.session['vipuser']['id'])
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password=m.hexdigest()
        ob.username=request.POST['username']
        ob.save()
        context = {'info':'修改成功！'}
        user = Users.objects.get(id=request.session['vipuser']['id'])
        context['user'] = user
        return render(request,"web/resetps.html",context)
    except Exception as err:
        print(err)
        context = {'info':'修改失败！'}
        user = Users.objects.get(id=request.session['vipuser']['id'])
        context['user'] = user
        return render(request,"web/resetps.html",context)
