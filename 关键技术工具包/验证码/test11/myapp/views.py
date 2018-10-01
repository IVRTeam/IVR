from django.shortcuts import render

from io import BytesIO
from myapp import check_codes




# Create your views here.
from django.http import HttpResponse

def create_code_img(request):
    #在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = check_codes.gene_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())
def test_code(request):
    #GET方法返回表单
    if request.method == 'GET':
        return render(request, 'myapp/test_code.html')
    #POST方法用来验证提交的验证码是否正确
    else:
        code = request.POST.get('code', '')
        if code == request.session.get('check_code', 'error'):
            return HttpResponse("yes")
        return HttpResponse("no")

def index(request):
	return render(request, 'myapp/test_code.html')
