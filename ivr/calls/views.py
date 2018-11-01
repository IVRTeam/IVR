# _*_ coding:utf-8 _*_
from django.shortcuts import render,redirect
from mains.models import Phonelist, State, User
from django.http import JsonResponse,HttpResponse
import datetime
from django.db import connection
import xlrd
import xlwt
#from util.dialNumber import dial_number

# Create your views here.
def phoneManager(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        name = request.session.get('name')
        img = request.session.get('img')
        obj = User.objects.get(uid=uid)
        phone = obj.phone
        return render(request, 'calls/phoneManager.html', {'uid': uid, 'name': name, 'img': img, 'phone': phone})
    else:
        return redirect('/')
def datas(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        size = request.POST.get("length")
        startIndex = request.POST.get("start")
        pageindex = (int(startIndex) / int(size) + 1)
        draw = request.POST.get("draw")
        order = request.POST.get("order[0][column]")
        if order == '2':
            order = 'number'
        elif order == '5':
            order = 'num'
        elif order == '6':
            order = 'star'
        elif order == '7':
            order = 'createTime'
        else:
            order = 'pid'
        orderDir = request.POST.get("order[0][dir]")
        searchValue = request.POST.get("search[value]")
        #print('size:' + size + ';startIndex:' + str(pageindex) + ';draw:' + draw + ';order:' + order + ';orderDir:' + orderDir +';searchValue:' + searchValue + ';uid:'+uid)
        # 取数据
        cursor = connection.cursor()
        cursor.callproc("calls", (int(size), pageindex, order, orderDir, searchValue, uid, 1))
        #cursor.callproc("calls", (2, startIndex, 'pid', orderDir, searchValue, '2014', 1))
        list = []
        phones = cursor.fetchall()
        for ph in phones:
            list.append(
                {"pid": ph[0], "number": ph[1], "name": ph[2], "address": ph[3], "num": ph[4], "star": ph[5],
                 "createTime": ph[6]})
        cursor.execute('select @_calls_6')
        numbers = cursor.fetchone()[0]
        data = {"draw": draw, "recordsFiltered": numbers, "recordsTotal": numbers, "data": list}
        cursor.close()
        connection.close()
        return JsonResponse(data)
    else:
        return redirect('/')
# 增加电话号码，status为200表示成功，400表示增加的号码已存在，500表示增加失败
def addPhone(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        phone = request.POST.get("phone")
        name = request.POST.get("name")
        address = request.POST.get("address")
        star = request.POST.get("star")
        createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        u = User.objects.get(pk=uid)
        num = Phonelist.objects.filter(user=u, number=phone).count()
        status = '200'
        if num > 0:
            status = '400'
            data = {'status': status}
            return JsonResponse(data)
        else:
            try:
                ph = Phonelist.createPhonelist(phone, name, address, star, createTime, u)
                ph.save()
            except:
                status = '500'
        data = {'status': status}
        return JsonResponse(data)
    else:
        return redirect('/')
def deletePhone(request):
    if 'uid' in request.session:
        recordstr = request.POST.get("recordstr")
        cursor = connection.cursor()
        cursor.callproc("deletePhone", (recordstr, 1))
        cursor.execute('select @_deletePhone_1')
        flag = cursor.fetchone()[0]
        status = '删除成功'
        if flag == 500:
            status = '删除失败'
        data = {'status': status}
        return JsonResponse(data)
    else:
        return redirect('/')
def alterPhone(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        pid = request.POST.get("pid")
        phone = request.POST.get("phone")
        name = request.POST.get("name")
        address = request.POST.get("address")
        star = request.POST.get("star")
        #createTime = request.POST.get("createTime")
        # flag为判断用户是否修改了电话号码，如果修改了，flag为1
        flag = request.POST.get("flag")
        status = '200'
        if flag == '0':
            u = User.objects.get(pk=uid)
            num = Phonelist.objects.filter(user=u, number=phone).count()
            if num > 0:
                status = '400'
                data = {'status': status}
                return JsonResponse(data)
        #print('number='+phone+'name='+name+'address='+address+'star='+star+'id='+pid)
        try:
            # 如果执行异常，会自动跳到except里面去
            cursor = connection.cursor()
            cursor.execute("update phonelist set number=%s,name=%s,address=%s,star=%s where id=%s", [phone, name, address, star, pid])
            #cursor.execute("update phonelist set number=%s,name=%s,address=%s,star=%s,createTime=%s where id=%s", [phone, name, address, star, createTime, pid])
        except:
            status = '500'
        data = {'status': status}
        return JsonResponse(data)
    else:
        return redirect('/')
#呼叫从前端传过来的电话号码
def callNumber(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        number = request.GET.get("recordstr")
        number_list = number.strip(',').split(',')
        print(number_list)
        for phone in number_list:
            print("序号：%s   值：%s" % (number_list.index(phone) + 1, phone))
        data = {"data": '200'}
        return JsonResponse(data)

    else:
        return redirect('/')
# 呼叫从前端传过来的电话号码
# def callNumber(request):
#     if 'uid' in request.session:
#         uid = request.session.get('uid')
#         number = request.GET.get("recordstr")
#         number_list = number.strip(',').split(',')
#         for phone in number_list:
#             print('dial number is ' + phone)
#             dial_number(phone, uid)
#         data = {"data": '200'}
#         return JsonResponse(data)
#     else:
#         return redirect('/')

# 显示电话状态页面
def stateManager(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        name = request.session.get('name')
        img = request.session.get('img')
        obj = User.objects.get(uid=uid)
        phone = obj.phone
        return render(request, 'calls/stateManager.html', {'uid': uid, 'name': name, 'img': img, 'phone': phone})
    else:
        return redirect('/')
def stateDatas(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        size = request.POST.get("length")
        startIndex = request.POST.get("start")
        pageindex = (int(startIndex) / int(size) + 1)
        draw = request.POST.get("draw")
        order = request.POST.get("order[0][column]")
        callState = request.POST.get("callState")
        lengthStart = request.POST.get("lengthStart")
        lengthEnd = request.POST.get("lengthEnd")
        timeStart = request.POST.get("timeStart")
        timeEnd = request.POST.get("timeEnd")
        if order == '2':
            order = 'number'
        elif order == '3':
            order = 'status'
        elif order == '4':
            order = 'callTime'
        elif order == '5':
            order = 'callLength'
        else:
            order = 'id'
        orderDir = request.POST.get("order[0][dir]")
        searchValue = request.POST.get("search[value]")
        # print('size:' + size + ';startIndex:' + str(
        #     pageindex) + ';draw:' + draw + ';order:' + order + ';orderDir:' + orderDir + ';searchValue:' + searchValue + ';uid:' + uid + ';callState:' + callState + ';lengthStart:' + lengthStart + ';lengthEnd:' + lengthEnd + ';timeStart:' + timeStart + ';timeEnd:' + timeEnd)
        # 取数据
        cursor = connection.cursor()
        cursor.callproc("states", (int(size), pageindex, order, orderDir, searchValue, uid, callState, lengthStart, lengthEnd, timeStart, timeEnd, 1))
        # cursor.callproc("calls", (2, startIndex, 'pid', orderDir, searchValue, '2014', 1))
        list = []
        states = cursor.fetchall()
        for st in states:
            list.append(
                {"sid": st[0], "phone": st[1], "status": st[2], "callTime": st[3], "callLength": st[4], "digits": st[5]})
        cursor.execute('select @_states_11')
        numbers = cursor.fetchone()[0]
        data = {"draw": draw, "recordsFiltered": numbers, "recordsTotal": numbers, "data": list}
        cursor.close()
        connection.close()
        return JsonResponse(data)
    else:
        return redirect('/')
# 删除呼叫状态
def deleteState(request):
    if 'uid' in request.session:
        recordstr = request.POST.get("recordstr")
        cursor = connection.cursor()
        cursor.callproc("deleteState", (recordstr, 1))
        cursor.execute('select @_deleteState_1')
        flag = cursor.fetchone()[0]
        status = '删除成功'
        if flag == 500:
            status = '删除失败'
        data = {'status': status}
        return JsonResponse(data)
    else:
        return redirect('/')


#导入excel文件
def fileImport(request):
    if 'uid' in request.session:
        if request.method == "POST" and request.is_ajax():
            uid = request.session.get('uid')
            type = request.POST.get('type')
            # 开始解析上传的excel表格
            f = request.FILES.get('file')
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())  #打开excel文件读取数据
            table = wb.sheet_by_index(0)  #获取工作表
            colnames = table.row_values(0) #行头
            try:
                if colnames[4] != '4520ef70-d390-11e8-a545-c3341d76a8a0': #判断是否使用模板文件,可能会溢出
                    data = {'status': '400'}#400表示上传的不是模板文件
                    return JsonResponse(data)
                else:
                    WorkList = []
                    x = y = z = 0
                    nrows = table.nrows  # 行数
                    if type == '1':  # 追加模式
                        for i in range(2, nrows):  # 忽略前2行,0开始
                            row = table.row_values(i)  # 获取每行的数据
                            if ''.join(row) != '':
                                if Phonelist.objects.filter(number=row[0], user_id=uid).exists():  # 电话号码在数据库中重复
                                    x = x + 1  # 重复值计数
                                else:
                                    y = y + 1  # 非重复值计数
                                    WorkList.append(Phonelist(number=row[0], name=row[1], address=row[2], star=row[3], user_id=uid))
                            else:
                                z = z + 1  # 空行值计数
                        try:
                            Phonelist.objects.bulk_create(WorkList)  # 批量存进数据库
                            data = {'status': '200', 'x': x, 'y': y, 'z': z}  # 200表示追加模式上传成功
                        except:
                            data = {'status': '500'}
                    else:   #覆盖模式
                        for i in range(2, nrows):  # 忽略前2行,0开始
                            row = table.row_values(i)  # 获取每行的数据
                            if ''.join(row) != '':
                                y = y + 1  # 非重复值计数
                                WorkList.append(Phonelist(number=row[0], name=row[1], address=row[2], star=row[3], user_id=uid))
                            else:
                                z = z + 1  # 空行值计数
                        try:
                            phone = Phonelist.objects.filter(user_id=uid)
                            phone.delete()
                            Phonelist.objects.bulk_create(WorkList)  # 批量存进数据库
                            data = {'status': '201', 'y': y, 'z': z} #201表示覆盖模式上传成功
                        except:
                            data = {'status': '500'}
            except:
                data = {'status': '400'} #400表示上传的不是模板文件
                return JsonResponse(data)
        else:
            data = {'status': '500'} #500表示上传失败
        return JsonResponse(data)
    else:
        return redirect('/')

#导出excel文件
def fileExport(request):
    if 'uid' in request.session:
        uid = request.session.get('uid')
        star = request.GET.get('star')
        if star == '0': #全部星级
            ph_list = Phonelist.objects.filter(user_id=uid).values_list('number','name','address','star','createTime','user_id')
        else: #过滤星级
            ph_list = Phonelist.objects.filter(user_id=uid,star=star).values_list('number','name','address','star','createTime','user_id')

        # 设置HttpResponce的类型
        response = HttpResponse(content_type='application/vnd.ms.excel')
        response['Content-Disposition'] = 'atttachment;filename=phonelists.xls' #返回下载文件的名称
        # new一个工作簿文件
        workbook = xlwt.Workbook(encoding='utf-8')
        #new 一个sheet
        mysheet =workbook.add_sheet(u'电话清单')
        #设置表头样式
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        style = xlwt.XFStyle()  # Create Style
        style.alignment = alignment  # 给样式添加文字居中属性
        style.font.height = 200  # 设置字体大小10px

        rows = ph_list
        cols = 6 #每行的列
        mysheet.write_merge(0, 0, 0, 5, '电话号码信息统计表',style)
        title = ['电话号码','用户姓名','电话地区','用户星级','导入时间','用户账号']#表头名
        for c in range(len(title)):
            mysheet.write(1,c,title[c],style) #表头写进第一行

        if ph_list.count()>0: #生成excel文件
            for r in range(0,len(rows)): #对行进行遍历
                for c in range(0,cols): #对列进行遍历
                    mysheet.write(r+2,c,str(rows[r][c]))
        else:
            mysheet.write_merge(2, 2, 0, 5, '没有符合条件的电话清单', style)
        workbook.save(response)
        return response
    else:
        return redirect('/')