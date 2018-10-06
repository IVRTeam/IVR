#下面这个语句是为了能在此文件中编写中文信息
# _*_ encoding: utf-8 _*_
from django.db import models

# Create your models here.

# 权限表
class Auth(models.Model):
    # 权限名称
    aname = models.CharField(max_length=20)
    def __str__(self):
        return self.aname
    class Meta:
        db_table = "auth"
# 用户表
class User(models.Model):
    # 用户账号
    uid = models.CharField(primary_key=True, max_length=20)
    # 用户密码
    pwd = models.CharField(max_length=20)
    # 用户姓名
    name = models.CharField(max_length=20)
    # 用户手机号
    phone = models.CharField(max_length=20)
    # 用户头像
    img = models.CharField(max_length=100)
    # 用户注册时间
    regTime = models.DateField(auto_now=True)
    # 外键
    # 对应用户
    auth = models.ForeignKey(Auth, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "user"

    @classmethod
    def createUser(cls, uid, pwd, name, phone, auth):
        user = cls(uid=uid, pwd=pwd, name=name, phone=phone, auth=auth)
        return user


# 模板表
class Templates(models.Model):
    # 模板名称
    tname = models.CharField(max_length=100)
    # 外键
    # 对应用户
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.tname
    class Meta:
        db_table = "templates"
    @classmethod
    def createTemplates(cls, tname, user):
        templates = cls(tname=tname, user=user)
        return templates
# 模板存储表
class Template_store(models.Model):
    # 问题id
    vid = models.CharField(max_length=100)
    # 问题位置
    pos = models.CharField(max_length=100)
    # 对应按键
    digit = models.CharField(max_length=100)
    # 对应问题id
    cid = models.CharField(max_length=100)
    # 是否为最后一个问题，1表示是，0表示不是
    flag = models.CharField(max_length=20)
    # 外键
    # 对应模板
    template = models.ForeignKey(Templates, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "template_store"

    @classmethod
    def createTemplate_store(cls, vid, pos, digit, cid, flag, template):
        template_store = cls(vid=vid, pos=pos, digit=digit, cid=cid, flag=flag, template=template)
        return template_store
# 消息表
class Message(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # 内容
    content = models.CharField(max_length=100)
    # 消息时间
    time = models.CharField(max_length=50)
    # 是否阅读,0表示没有阅读，1表示阅读
    isRead = models.CharField(max_length=20, default='0')
    # 外键
    # 对应用户
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "message"
    @classmethod
    def createMessage(cls, title, content, time, isRead, user):
        message = cls(title=title, content=content, time=time, isRead=isRead, user=user)
        return message
# 电话清单表
class Phonelist(models.Model):
    # 电话号码
    number = models.CharField(max_length=50)
    # 姓名
    name = models.CharField(max_length=50)
    # 地区
    address = models.CharField(max_length=200)
    # 等级,数字越大，等级越高，默认为0
    star = models.CharField(max_length=20, default='普通')
    # 导入时间
    createTime = models.DateField(auto_now=True)
    # 外键
    # 对应用户
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "phonelist"

    @classmethod
    def createPhonelist(cls, number, name, address, star, user):
        phonelist = cls(number=number, name=name, address=address, star=star, user=user)
        return phonelist
# 电话状态表
class State(models.Model):
    # 状态
    status = models.CharField(max_length=50)
    # 呼叫时间
    callTime = models.CharField(max_length=50)
    # 呼叫时长
    callLength = models.CharField(max_length=50)
    # 用户按键（列表）
    digits = models.CharField(max_length=100)
    # 外键
    # 对应电话号码
    phone = models.ForeignKey(Phonelist, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = "state"
    @classmethod
    def createState(cls, number, status, callTime, callLength, digits, phone):
        state = cls(number=number, status=status, callTime=callTime, callLength=callLength, digits=digits, phone=phone)
        return state
# 公告表
class Notification(models.Model):
    # 标题
    title = models.CharField(max_length=100)
    # 内容
    content = models.CharField(max_length=500)
    # 时间
    time = models.CharField(max_length=50)
    class Meta:
        db_table = "notification"
    @classmethod
    def createNotification(cls, title, content, time):
        notification = cls(title=title, content=content, time=time)
        return notification
