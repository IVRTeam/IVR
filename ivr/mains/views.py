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
        name = request.session.get('name')
        img = request.session.get('img')
        return render(request, 'mains/index.html',{'name':name,'img':img})
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

def user(request):
    if 'uid' in request.session:
        name = request.session.get('name')
        img = request.session.get('img')
        return render(request, 'mains/user.html',{'name':name,'img':img})
    else:
        return redirect('/')

def getInfo(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        name = request.session.get('name')
        img = request.session.get('img')
        obj = User.objects.get(pk=uid)
        phone = obj.phone
        data ={'name':name,'img':img, 'phone':phone}
        return JsonResponse(data)
    else:
        return redirect('/')

def uploadImg(request):
    if 'uid' in request.session:
        if request.method == "POST" and request.is_ajax():
            uid = request.session.get('uid')
            f = request.FILES.get('file')
            try:
                user = User.objects.get(pk=uid)
                user.img = f
                user.save()
                data = {'status': '200'}
                #修改session的img值
                request.session['img'] = user.img.url
            except:
                data = {'status': '500'} #头像上传失败
        else:
            data = {'status': '500'} #500表示不是POST方式提交，上传失败
        return JsonResponse(data)
    else:
        return redirect('/')