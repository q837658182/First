# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from models import UserInfo
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收数据
    post=request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    if upwd2!=upwd or upwd=='':
        return redirect('/user/register/')
    # 创建实例对象
    user = UserInfo()
    user.uname=uname
    # 加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    return redirect('/user/login/')


def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    # print (uname)
    # print (count)
    return JsonResponse({'count':count})


def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0, 'error_pwd':0, 'uname':uname,}
    return render(request, 'df_user/login.html',context)


def login_handle(request):
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    user = UserInfo.objects.filter(uname=uname)
    print len(user)
    if len(user)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==user[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie(uname,'',max_age=-1)
            request.session['user_id']=user[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title':'用户登录', 'error_name': 0, 'error_pwd': 1, 'uname':uname }
            return render(request,'df_user/login.html',context)
    else:
        context = {'title': '用户登录', 'error_name':1, 'error_pwd': 0, 'uname': uname}
        return render(request,'df_user/login.html',context)


def info(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    context={'title':'用户中心', 'user':user,'page_name':1}
    return render(request,'df_user/user_center_info.html', context)


def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {'title': '用户中心', 'user': user,'page_name':1}
    return render(request,'df_user/user_center_order.html', context)


def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user,'page_name':1}
    return render(request,'df_user/user_center_site.html', context)