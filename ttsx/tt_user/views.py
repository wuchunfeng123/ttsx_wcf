# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from hashlib import sha1

from user_decorators import user_login
from .models import UserInfo
import datetime

# Create your views here.
def register(request):
    context={'title':'注册'}
    return render(request,'tt_user/register.html',context)

def register_username(request):
    user = UserInfo.objects.all()
    #print user
    list2 = []
    for temp in user:
        list2.append(temp.uname)
    #print(list2)
    return JsonResponse({'list':'list2'})

def register_handle(request):
    dict=request.POST
    uname=dict.get('user_name')
    upwd=dict.get('pwd')
    upwd2=dict.get('cpwd')
    uemail=dict.get('email')

    if upwd!=upwd2:
        return redirect('/user/register')
    if uname=='' or upwd=='' or upwd2=='' or uemail=='':
        return redirect('/user/register/')

    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    user=UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.email=uemail
    user.save()

    return redirect('/user/login/')

def login(request):
    uname=request.COOKIES.get('uname')
    context={'title':'登录','top':'0','uname':uname}
    return render(request,'tt_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    uname_jz = post.get('name_jz','0')
    s1=sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    context = {'title':'登录','uname': uname,'upwd':upwd,'top':'0'}

    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 0:
       #用户名错误
        context['name_error'] = '1'

        return render(request, 'tt_user/login.html',context)
    else:

        if users[0].upwd == upwd_sha1: #登陆成功
            #记录当前登陆的用户
            request.session['uid'] = users[0].id
            request.session['uname'] = uname
            #重定向，从哪儿来，回哪去
            path = request.session.get('url_path', '/user/')
            print(path)
            response = redirect(path)
            #记住用户名
            if uname_jz == '1':
                response.set_cookie('uname',uname,expires=datetime.datetime.now() + datetime.timedelta(days=7))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:
            #密码错误
            context['pwd_error'] = '1'
            return render(request,'tt_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def islogin(request):
    result = 0
    if request.session.has_key('uid'):
        result = 1
    return JsonResponse({'islogin':result})

@user_login
def center(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'title':'用户中心','user': user}
    return render(request,'tt_user/center.html',context)

@user_login
def order(request):
    context = {'title':'用户订单'}
    return render(request, 'tt_user/order.html',context)

@user_login
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'收货地址','user':user}
    return render(request,'tt_user/site.html',context)
'''
user.addressinfo_set.all

将当前地址进行判断，如果不是注册、登录等地址的话，则记录下来，当登录成功后，则转向此地址
解决方案：中间件
        process_view

'''
def user_center_info(request):
    return render(request,'tt_user/user_center_info.html',{'title':'用户中心'})


def index(request):
    return render(request, 'tt_user/index.html',{'title':'首页'})

def register_valid(request):
    uname = request.GET.get('uname')
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'valid':result}
    return JsonResponse(context)

