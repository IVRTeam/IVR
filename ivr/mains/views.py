# _*_ coding:utf-8 _*_
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from mains.models import User
# 引入密码加密模块
from django.contrib.auth.hashers import make_password
# Create your views here.


def index(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        name = request.session.get('name')
        img = request.session.get('img')
        obj = User.objects.get(uid=uid)
        phone = obj.phone
        return render(request, 'mains/index.html',{'uid':uid,'name':name,'img':img, 'phone':phone})
    else:
        return redirect('/')


def quit(request):
    #清除session
    logout(request)
    return redirect('/')


def modify(request):
    if 'uid' in request.session:
        if request.method == "POST":
            uid = request.session.get('uid')
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')
            phone = request.POST.get('phone')
            data = {'status': '200'}# 表示修改成功
            try:
                user = User.objects.get(uid=uid)
                user.name = name
                user.pwd = make_password(pwd)
                user.phone = phone
                user.save()
                #修改session的值
                request.session['name'] = name
            except:
                data = {'status': '500'}#表示修改失败
            return JsonResponse(data)
        else:
            data = {'status':'500'}#表示不是用POST的提交方式，修改失败
            return JsonResponse(data)
    else:
        return redirect('/')