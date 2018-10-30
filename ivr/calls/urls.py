from django.conf.urls import url
from . import views
app_name = 'calls'

urlpatterns = [
    #显示网页
    url(r'^$', views.phoneManager),
    #返回网页所需数据
    url(r'^datas/$', views.datas),
    #增加数据
    url(r'^addPhone/$', views.addPhone),
    #删除数据
    url(r'^deletePhone/$', views.deletePhone),
    #修改号码
    url(r'^alterPhone/$', views.alterPhone),
    #呼叫号码
    url(r'^callNumber/$', views.callNumber),
    #显示状态
    url(r'^stateManager/$', views.stateManager),
]