from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mains.models import User, Auth
# 引入密码加密模块
from django.contrib.auth.hashers import make_password, check_password
# 引入绘图模块
from PIL import Image, ImageDraw, ImageFont
# 引入随机函数模块
import random
import io

# Create your views here.
def login(request):
    return render(request, "logins/login.html")
def error(request):
    return render(request, "logins/version.html")
def vertifycode(request):
	font_path = '/Library/Fonts/arial.ttf'
	#定义变量，用于画面的背景色、宽、高
	bgcolor = (random.randrange(20, 100), random.randrange(20,100), random.randrange(20, 100))
	width = 100
	height = 40
	#创建画面对象
	im = Image.new('RGB', (width, height),bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0,100):
		xy = (random.randrange(0,width), random.randrange(0, height))
		#点的颜色
		fill = (random.randrange(0, 255), 255, random.randrange(0,255))
		#实心点
		draw.point(xy, fill=fill)
	#定义验证码的备选值
	str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
	#堆积选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str[random.randrange(0, len(str))]
	#构造字体对象(字体和大小)
	font = ImageFont.truetype(font_path,25)
	#构造字体颜色（如果想要不同的颜色，可以创建4个颜色）
	fontcolor1 = (255, random.randrange(0,255), random.randrange(0,255))
	fontcolor2 = (255, random.randrange(0,255), random.randrange(0,255))
	fontcolor3 = (255, random.randrange(0,255), random.randrange(0,255))
	fontcolor4 = (255, random.randrange(0,255), random.randrange(0,255))
	#绘制4个字
	draw.text((5,2), rand_str[0], font=font, fill=fontcolor1)
	draw.text((25,2), rand_str[1], font=font, fill=fontcolor2)
	draw.text((50,2), rand_str[2], font=font, fill=fontcolor3)
	draw.text((75,2), rand_str[3], font=font, fill=fontcolor4)
	#释放画笔
	del draw
	#存入session，用于做进一步验证
	request.session['vertify'] = rand_str
	#内存文件操作
	buf = io.BytesIO()
	#将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'image/png')
# 登录检查
def loginCheck(request):
    code1 = request.POST.get("authCode")
    code2 = request.session["vertify"]
    data = {'status': '400'}
    if code1 == code2:
        uid = request.POST.get("uid")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(pk=uid)
        if user and check_password(pwd, user[0].pwd):
            request.session['uid'] = uid
            request.session['name'] = user[0].name
            #request.session['auth'] = user.auth
            request.session['img'] = user[0].img
            data['status'] = 200
            return JsonResponse(data)
            # return redirect("/logins/testSession/")
        else:
            data['status'] = 500
            return JsonResponse(data)
    else:
        return JsonResponse(data)
def register(request):
    return render(request, "logins/register.html")
def registerCheck(request):
    uid = request.POST.get("uid")
    pwd = request.POST.get("pwd")
    name = request.POST.get("username")
    phone = request.POST.get("phone")
    auth = Auth.objects.get(pk=2)
    img = '/static/image/big.jpg'
    user = User.createUser(uid, make_password(pwd), name, phone, img, auth)
    user.save()
    data = {'status': '200'}
    return JsonResponse(data)
def testSession(request):
    uid = request.session.get('uid')
    name = request.session.get('name')
    #auth = request.session.get('auth')
    img = request.session.get('img')
    #data = {'uid': uid, "name": name, "img": img}
    return render(request, 'logins/testSession.html', {'uid': uid, "name": name, "img": img})
def checkUid(request):
    uid = request.GET.get("uid")
    num = User.objects.filter(pk=uid).count()
    status = '没有'
    if num > 0:
        status = '有'
    data = {'status': status}
    return JsonResponse(data)
def test(request):
    return render(request, "logins/test.html")
def tests(request):
    return render(request, "logins/tests.html")


